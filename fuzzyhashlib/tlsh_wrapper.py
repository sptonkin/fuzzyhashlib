from __future__ import print_function
import sys
import os

from . common import find_library

"""
Shim between fuzzyhashlib code and tlsh's existing tlsh.so python extension.

[sptonkin@outlook.com]
"""

# Load library
tlsh_library_path = find_library("tlsh")
sys.path.append(os.path.dirname(tlsh_library_path))
from tlsh import *
