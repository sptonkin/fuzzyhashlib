"""Helper functions for dealing with ctypes, and Python 2-3 strings.

Based heavily off work completed by Michael Dorman (mjdorma@gmail.com) for
his yara-ctypes project, simply shifted into a library because we need
to import multiple libraries here."""

from __future__ import print_function

import sys
import os
import platform
import ctypes


def find_library(library_name):
    # Figure out architecture.
    if platform.architecture()[0].startswith("64"):
        arch = "x86_64"
    else:
        arch = "x86_32"

    # Figure out OS info.
    if sys.platform.startswith("linux"):
        os_platform = "linux"
        extension = "so"
    elif sys.platform.startswith("darwin"):
        os_platform = "dawin"
        extension = "dylib"
    elif sys.platform.startswith("win"):
        os_platform = "windows"
        extension = "dll"
    else:
        raise Exception("Unsupported platform - %s" % sys.platform)

    library_filename = "%s.%s" % (library_name, extension)
    library_path = os.path.join(os.path.dirname(__file__),
                                "libs",
                                os_platform,
                                arch,
                                library_filename)
    return library_path


def load_library(library_path):
    try:
        library = ctypes.cdll.LoadLibrary(library_path)
    except Exception as err:
        print("Failed to import '%s'" % library_path, file=sys.stderr)
        raise

    return library


if sys.version_info[0] < 3:  # major
    def tobyte(s): 
        return s 
else: 
    def tobyte(s): 
        if type(s) is bytes: 
            return s 
        else: 
            return s.encode('utf-8', errors='ignore') 
 

if sys.version_info[0] < 3:  # major
    def frombyte(s): 
        return s 
else: 
    def frombyte(s): 
        if type(s) is bytes: 
            return str(s.decode(encoding='utf-8', errors='ignore')) 
        else: 
            return s
