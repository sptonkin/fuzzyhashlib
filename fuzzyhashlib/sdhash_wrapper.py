from __future__ import print_function
import sys
import os

from . common import find_library

"""
Shim between fuzzyhashlib code and sdhash's existing sdbf_class module (which
imports from _sdbf_class.so, which needs to be added to the path for 
importing).

[sptonkin@outlook.com]
"""

# Load library
sdbf_library_path = find_library("_sdbf_class")
sys.path.append(os.path.dirname(sdbf_library_path))
from . import sdbf_class


class SdbfError(Exception):
    """Base exception for SDBF hash errors."""
    pass


def sdbf_from_buffer(buf, name=None):
    #TODO - see if you can restore name to this. not needed for initial cut.
    #if len(buf) < 512:
    #    raise ValueError("Buffer must be > 512 bytes in size.")
    #if name is None:
    #    name = hashlib.sha1(buf).hexdigest()
    #print("name: %s (%s)" % (name, type(name)))
    name = ""
    return sdbf_class.sdbf(name, buf, 0, len(buf), None)


def sdbf_from_hash(sdhash):
    return sdbf_class.sdbf(sdhash)
