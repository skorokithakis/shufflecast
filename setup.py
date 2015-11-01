#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    "pychromecast"
]

test_requirements = [
]

setup(
    name='shufflecast',
    version='0.1.0',
    description="A TV channel with all your favorite shows.",
    long_description=readme,
    author="Stavros Korokithakis",
    author_email='hi@stavros.io',
    url='https://github.com/skorokithakis/shufflecast',
    packages=[
        'shufflecast',
    ],
    package_dir={'shufflecast':
                 'shufflecast'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    entry_points={
        'console_scripts': ['shufflecast=shufflecast.shufflecast:main'],
    },
    keywords='shufflecast',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
