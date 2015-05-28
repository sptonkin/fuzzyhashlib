import sys
import os
import platform

import ctypes
from ctypes import *

"""
A ctypes wrapper for ssdeep version 2.9

[sptonkin@outlook.com]
"""

# Thanks to Michael Dorman (mjdorma@gmail.com) for handy 2-3 string converters.
# Convert unicode to ascii if we're in 3x.
if sys.version_info[0] < 3: #major
    def tobyte(s):
        return s
else:
    def tobyte(s):
        if type(s) is bytes:
            return s
        else:
            return s.encode('utf-8', errors='ignore')

if sys.version_info[0] < 3: #major
    def frombyte(s):
        return s
else:
    def frombyte(s):
        if type(s) is bytes:
            return str(s.decode(encoding='utf-8', errors='ignore'))
        else:
             return s


#ensure we can find our ssdeep binary
if sys.platform == 'win32':
    dllpath = os.path.join(sys.prefix, 'DLLs')
    library = os.path.join(dllpath, 'libssdeep.dll')
else:
    dllpath = os.path.join(sys.prefix, 'lib')
    library = os.path.join(dllpath, 'libssdeep.so')

#FIXME - this should be changed
if platform.architecture()[0].startswith("64"):
    arch = "x86_64"
else:
    arch = "x86_32"

#figure out OS path
if sys.platform.startswith("linux"):
    platform = "linux"
elif sys.platform.startswith("darwin"):
    platform = "dawin"
elif sys.platform.startswith("win"):
    platform = "windows"
else:
    raise Exception("Unsupported platform - %s" % sys.platform)

library = os.path.join(os.path.dirname(__file__),
                        "..", "libs", platform, arch, "libssdeep.so")

tmp = os.environ['PATH']
os.environ['PATH'] += ";%s" % dllpath
try:
    libssdeep = cdll.LoadLibrary(library)
except Exception as err:
    print("Failed to import '%s'" % library)
    print("PATH = %s" % os.environ['PATH'])
    raise
os.environ['PATH'] = tmp

#defines (from fuzzy.h)
SPAMSUM_LENGTH = 64
FUZZY_MAX_RESULT = 2 * SPAMSUM_LENGTH + 20
FUZZY_FLAG_ELIMSEQ = 1
FUZZY_FLAG_NOTRUNC = 2

class SsdeepError(Exception):
    """Base exception class for SSDeep errors."""
    pass

#fuzzy_new C API (from fuzzy.h)
#extern /*@only@*/ /*@null@*/ struct fuzzy_state *fuzzy_new(void);
libssdeep.fuzzy_new.restype = c_void_p
def fuzzy_new():
    result = libssdeep.fuzzy_new()
    if result is None:
        raise SsdeepError("Could not create fuzzy_state")
    return result

#fuzzy_clone C API (from fuzzy.h)
#extern /*@only@*/ /*@null@*/ struct fuzzy_state *fuzzy_clone(const struct fuzzy_state *state);
libssdeep.fuzzy_clone.restype = c_void_p
libssdeep.fuzzy_clone.argtypes = [c_void_p]
def fuzzy_clone(state):
    return libssdeep.fuzzy_clone(state)

#fuzzy_free C API (from fuzzy.h)
#extern void fuzzy_free(/*@only@*/ struct fuzzy_state *state);
libssdeep.fuzzy_clone.argtypes = [c_void_p]
def fuzzy_free(state):
    libssdeep.fuzzy_free(state)

#fuzzy_update C API (from fuzzy.h)
#extern int fuzzy_update(struct fuzzy_state *state,
#            const unsigned char *buffer,
#            size_t buffer_size);
libssdeep.fuzzy_update.restype = c_int
libssdeep.fuzzy_update.argtypes = [c_void_p, c_char_p, c_size_t]
def fuzzy_update(state, buf):
    ret_code = libssdeep.fuzzy_update(state, tobyte(buf), len(buf))
    if ret_code != 0:
        raise SsdeepError("Could not update digest from passed buf.")

#fuzzy_digest C API (from fuzzy.h)
#extern int fuzzy_digest(const struct fuzzy_state *state,
#            /*@out@*/ char *result,
#            unsigned int flags);
libssdeep.fuzzy_digest.restype = c_int
libssdeep.fuzzy_digest.argtypes = [c_void_p, c_char_p, c_uint]
def fuzzy_digest(state, flags):
    result = create_string_buffer(FUZZY_MAX_RESULT)
    ret_code = libssdeep.fuzzy_digest(state, result, flags)
    if ret_code != 0:
        raise SsdeepError("Could not create digest.")
    return frombyte(result).value


#fuzzy_set_total_input_length C API (from fuzzy.h)
#extern int fuzzy_set_total_input_length(struct fuzzy_state *state, uint_least64_t total_fixed_length);
#libssdeep.fuzzy_set_total_input_length.restype = c_int
#libssdeep.fuzzy_set_total_input_length.argtypes = [c_void_p, c_ulonglong]
#def fuzzy_set_total_input_length(state, total_fixed_length):
#    return libssdeep.fuzzy_set_total_input_length(state, total_fixed_length)


#fuzzy_compare C API (from fuzzy.h)
#extern int fuzzy_compare(const char *sig1, const char *sig2);
#libssdeep.fuzzy_compare.restype = c_int
#libssdeep.fuzzy_compare.argtypes = [c_char_p, c_char_p]
def compare(sig1, sig2):
    """Computes the match score between the two two passed fuzzy hashes.
    This will be an integer score between 0 and 100.

    Note: This function wraps ssdeep's fuzzy_compare function."""
    return libssdeep.fuzzy_compare(sig1, sig2)
