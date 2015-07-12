from __future__ import print_function, absolute_import
import inspect
from . import libssdeep_wrapper
from . import sdhash_wrapper


"""Wrapper for various fuzzy hashing libraries which attempts to be as similar
in interface to hashlib as possible.

Supports:
    * ssdeep
    * sdhash

This also ships with built libraries for the supported algorithms in order
to minimise extenal dependencies.

[sptonkin@outlook.com]"""


class InvalidOperation(Exception):
    """Raised when the use of a fuzzyhashlib object is incorrect or
    unsupported."""
    pass


class ssdeep(object):
    """A ssdeep represents ssdeep's computed fuzzy hash of a string of
    information.
    
    ssdeep objects can be created either with a buffer or with a 
    previously computed hexdigest, although it should be noted that
    objects created with a previously computed hash cannoy be updated
    with calls to their .update() method. Doing so will result in an
    InvalidOperation exception.

    Methods:
    
    update() -- updates the current digest with an additional string
    hexdigest() -- return the current digest as a string of hex digits
    copy() -  returns a copy of the current hash object

    Attributes:

    name -- the name of the alogorthm being used (ie. "ssdeep")
    digest_size -- the maximum size in bytes
    
    Operators:
        
    __sub__ -- instances can have hashes compared with subtraction (-)
    __eq__ -- instances can be tested for hash equivalency (==)"""

    name = "ssdeep"
    digest_size = libssdeep_wrapper.FUZZY_MAX_RESULT

    def __init__(self, buf=None, hash=None):
        """Initialises a ssdeep object. Can be initialised with either a
        a buffer through the use of the keyword argument 'buf' or a
        previously computed ssdeep hash using the keyword agument ('hash').
        Note that only objects initialised using a buffer can be updated."""
        self.name = "ssdeep"
        self.digest_size = libssdeep_wrapper.FUZZY_MAX_RESULT
        self._state = libssdeep_wrapper.fuzzy_new()
        if buf is not None:
            self._updatable = True
            self._pre_computed_hash = None
            self.update(buf)
        elif hash is not None:
            self._updatable = False
            self._pre_computed_hash = hash
        else:
            raise ValueError("one of buf or hash must be set")
            
    def __del__(self):
        try:
            libssdeep_wrapper.fuzzy_free(self._state)
        except AttributeError:
            # On Python shutdown it seems like libssdeep_wrapper may get
            # freed first, it seems?
            #print("?", end="")
            pass

    def hexdigest(self):
        """Return the digest value as a string of hexadecimal digits."""
        if self._pre_computed_hash is None:
            return libssdeep_wrapper.fuzzy_digest(self._state, 0)
        else:
            return self._pre_computed_hash

    def update(self, buf):
        """Update this hash object's state with the provided string."""
        if self._updatable:
            return libssdeep_wrapper.fuzzy_update(self._state, buf)
        else:
            raise InvalidOperation("cannot update sdeep created from hash")

    def copy(self):
        """Returns a new instance which identical to this instance."""
        if self._pre_computed_hash is None:
            temp = ssdeep(buf="")
        else:
            temp = ssdeep(hash=hash)
        libssdeep_wrapper.fuzzy_free(temp._state)
        temp._state = libssdeep_wrapper.fuzzy_clone(self._state)
        temp._updatable = self._updatable
        temp._pre_computed_hash = self._pre_computed_hash
        return temp

    def __sub__(self, b):
        return libssdeep_wrapper.compare(self.hexdigest(), b.hexdigest())

    def __eq__(self, b):
        return \
            libssdeep_wrapper.compare(self.hexdigest(), b.hexdigest()) == 100


class sdhash(object):
    """A sdhash represents sdhash's computed fuzzy hash of a string of
    information.

    sdhash objects can be created either with a buffer or with a 
    previously computed hexdigest. sdhash objects cannot be updated
    with calls to .update() method. Doing so will result in an
    InvalidOperation exception.

    Methods:
    
    hexdigest() -- return the current digest as a string of hex digits
    copy() -  returns a copy of the current hash object

    Attributes:

    name -- the name of the alogorthm being used (ie. "sdhash")
    
    Operators:
        
    __sub__ -- instances can have hashes compared with subtraction (-)
    __eq__ -- instances can be tested for hash equivalency (==)"""

    name = "sdhash"

    def __init__(self, buf=None, hash=None):
        """Initialises a ssdeep object. Can be initialised with either a
        a buffer through the use of the keyword argument 'buf' or a
        previously computed ssdeep hash using the keyword agument ('hash').
        Note that sdhash objects cannot be updated()"""
        if buf is not None:
            self._sdbf = sdhash_wrapper.sdbf_from_buffer(buf)
        elif hash is not None:
            self._sdbf = sdhash_wrapper.sdbf_from_hash(hash)
        else:
            raise ValueError("One of buf or hash must be set.")

    def __del__(self):
       del self._sdbf 

    def hexdigest(self):
        """Return the digest value as a string of hexadecimal digits."""
        return self._sdbf.to_string()

    def copy(self):
        """Returns a new instance which identical to this instance."""
        return sdhash(hash=self.hexdigest())

    def update(self, *args):
        """Not supported."""
        raise InvalidOperation("update() not supported for sdhash.")

    def __sub__(self, b):
        score = self._sdbf.compare(b._sdbf, 0)
        #print("SDHASH\n%s - %s = %d" % \
        #        (self.hexdigest()[:32], b.hexdigest()[:32], score))
        return score

    def __eq__(self, b):
        return self._sdbf.compare(b._sdbf, 0) == 100
