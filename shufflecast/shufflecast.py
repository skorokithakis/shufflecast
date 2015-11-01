#!/usr/bin/env python
"""
Shuffle and play all files in a given directory.
"""

import os
import re
import random
import socket
import sys
import time
import urllib
from threading import Thread

import pychromecast
import SimpleHTTPServer
import SocketServer

PORT = random.randint(25000, 30000)


def list_files(directory, refilter):
    """
    Add all files matching the refilter under the current directory to a list.
    """
    files = []
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if not re.search(refilter, filename, re.IGNORECASE):
                continue
            files.append(os.path.join(dirpath[len(directory):], filename))
    return files


def get_my_ip():
    """
    Use a hack to get our external-facing interface's IP.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def cast_factory(videos):
    def cast():
        ip = get_my_ip()
        cc = pychromecast.get_chromecast()
        mc = cc.media_controller
        time.sleep(1)

        if cc.status.app_id:
            print("Killing existing app...")
            cc.quit_app()
            time.sleep(5)

        for video in videos:
            print("Playing %s..." % video)
            url = "http://%s:%s%s" % (ip, PORT, urllib.quote(video))
            cc.play_media(url, "video/mp4")
            time.sleep(15)

            while True:
                mc.update_status()
                try:
                    remaining = (mc.status.duration - mc.status.current_time)
                except:
                    # Something went wrong playing the file, try the next one.
                    print("Invalid status, playing next...")
                    break

                if mc.status.player_is_paused:
                    # The Chromecast was paused for some reason, ruining the
                    # illusion
                    print("Resuming...")
                    mc.play()
                elif mc.status.player_is_idle:
                    # The player stopped for some reason, play next.
                    print("Playing next...")
                    break

                print("%s seconds until next..." % (remaining - 10))
                if remaining <= 10:
                    # The video is almost done, play the next one.
                    break
                time.sleep(4)
    return cast


def serve_http(videos):
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", PORT), Handler)

    server = Thread(target=cast_factory(videos))
    server.setDaemon(True)
    server.start()

    httpd.serve_forever()


def main():
    if len(sys.argv) < 2:
        print("shufflecast <directory>")

    basedir = os.path.realpath(sys.argv[1])
    if not os.path.isdir(basedir):
        print("shufflecast <directory>")

    videos = list_files(basedir, "\.(avi|mkv|mp4)$")
    random.shuffle(videos)
    if not videos:
        sys.exit("No videos in specified directory.")

    os.chdir(basedir)

    serve_http(videos)

if __name__ == "__main__":
    main()
