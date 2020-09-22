#!/usr/bin/env python
from setuptools import setup

import re
import platform
import os
import sys


def load_version(filename='fuzzyhashlib/version.py'):
    """Parse a __version__ number from a source file"""
    with open(filename) as source:
        text = source.read()
        match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", text)
        if not match:
            msg = "Unable to find version number in {}".format(filename)
            raise RuntimeError(msg)
        version = match.group(1)
        return version


# See if we have a pre-built libfuzzyhashlib for this platform.
arch, exetype = platform.architecture()
system = platform.system().lower()
machine = platform.machine().lower()

if machine in ['i686', 'x86']:
    machine = 'x86_32'

if machine in ['amd64']:
    machine = 'x86_64'

if system == 'windows':
    ext = '.dll'
else:
    ext = '.so'

#build the yara package data (shipped yar files)
package_data = []
for path, _, files in os.walk(os.path.join('fuzzyhashlib', 'libs')):
    rootpath = path[len('fuzzyhashlib') + 1:]
    for f in files:
        if f.endswith('.so') or f.endswith('.dll'):
            package_data.append(os.path.join(rootpath, f))

setup(
    name="fuzzyhashlib",
    version=load_version(),
    packages=['fuzzyhashlib'],
    #data_files=data_files,
    package_data=dict(fuzzyhashlib=package_data),
    zip_safe=False,
    author="Stephen Tonkin",
    author_email="sptonkin@outlook.com",
    url="https://github.com/sptonkin/fuzzyhashlib",
    description="Hashlib-like wrapper for several fuzzy hash algorithms.",
    long_description=open('README.rst').read(),
    license="GNU General Public License v3",
    install_requires = [],
    platforms=['linux'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        #'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    test_suite="tests"
)

#if not data_files:
#    print("\nWARNING: Could not find %s" % fuzzyhashlib_path)
#    print("fuzzyhashlib may be unsupported on your system.")
