from __future__ import absolute_import
from ctypes import *

from .common import find_library, load_library, tobyte, frombyte

"""
A ctypes wrapper for ssdeep version 2.9

[sptonkin@outlook.com]
"""

# Load libssdeep
libssdeep_path = find_library("libssdeep")
libssdeep = load_library(libssdeep_path)

# defines (from fuzzy.h)
SPAMSUM_LENGTH = 64
FUZZY_MAX_RESULT = 2 * SPAMSUM_LENGTH + 20
FUZZY_FLAG_ELIMSEQ = 1
FUZZY_FLAG_NOTRUNC = 2


class SsdeepError(Exception):
    """Base exception class for SSDeep errors."""
    pass


# fuzzy_new C API (from fuzzy.h)
# extern /*@only@*/ /*@null@*/ struct fuzzy_state *fuzzy_new(void);
libssdeep.fuzzy_new.restype = c_void_p


def fuzzy_new():
    result = libssdeep.fuzzy_new()
    if result is None:
        raise SsdeepError("Could not create fuzzy_state")
    return result


# fuzzy_clone C API (from fuzzy.h)
# extern /*@only@*/ /*@null@*/ struct fuzzy_state *fuzzy_clone(const struct fuzzy_state *state);
libssdeep.fuzzy_clone.restype = c_void_p
libssdeep.fuzzy_clone.argtypes = [c_void_p]


def fuzzy_clone(state):
    return libssdeep.fuzzy_clone(state)


# fuzzy_free C API (from fuzzy.h)
# extern void fuzzy_free(/*@only@*/ struct fuzzy_state *state);
libssdeep.fuzzy_clone.argtypes = [c_void_p]


def fuzzy_free(state):
    libssdeep.fuzzy_free(state)


# fuzzy_update C API (from fuzzy.h)
# extern int fuzzy_update(struct fuzzy_state *state,
#            const unsigned char *buffer,
#            size_t buffer_size);
libssdeep.fuzzy_update.restype = c_int
libssdeep.fuzzy_update.argtypes = [c_void_p, c_char_p, c_size_t]


def fuzzy_update(state, buf):
    ret_code = libssdeep.fuzzy_update(state, tobyte(buf), len(buf))
    if ret_code != 0:
        raise SsdeepError("Could not update digest from passed buf.")


# fuzzy_digest C API (from fuzzy.h)
# extern int fuzzy_digest(const struct fuzzy_state *state,
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


# fuzzy_set_total_input_length C API (from fuzzy.h)
# extern int fuzzy_set_total_input_length(struct fuzzy_state *state, uint_least64_t total_fixed_length);
# libssdeep.fuzzy_set_total_input_length.restype = c_int
# libssdeep.fuzzy_set_total_input_length.argtypes = [c_void_p, c_ulonglong]
# def fuzzy_set_total_input_length(state, total_fixed_length):
#     return libssdeep.fuzzy_set_total_input_length(state, total_fixed_length)


# fuzzy_compare C API (from fuzzy.h)
# extern int fuzzy_compare(const char *sig1, const char *sig2);
# libssdeep.fuzzy_compare.restype = c_int
# libssdeep.fuzzy_compare.argtypes = [c_char_p, c_char_p]
def compare(sig1, sig2):
    """Computes the match score between the two two passed fuzzy hashes.
    This will be an integer score between 0 and 100.

    Note: This function wraps ssdeep's fuzzy_compare function."""
    return libssdeep.fuzzy_compare(sig1, sig2)
