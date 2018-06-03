from __future__ import print_function, absolute_import
from . import libssdeep_wrapper
from . import sdhash_wrapper
from . import tlsh_wrapper


"""Wrapper for various fuzzy hashing libraries which attempts to be as similar
in interface to hashlib as possible.

Supports:
    * ssdeep
    * sdhash
    * tlsh

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
    objects created with a previously computed hash cannot be updated
    with calls to their .update() method. Doing so will result in an
    InvalidOperation exception.

    Methods:
    
    update() -- updates the current digest with an additional string
    hexdigest() -- return the current digest as a string of hex digits
    copy() -  returns a copy of the current hash object

    Attributes:

    name -- the name of the algorithm being used (ie. "ssdeep")
    digest_size -- the maximum size in bytes
    
    Operators:
        
    __sub__ -- instances can have hashes compared with subtraction (-)
    __eq__ -- instances can be tested for hash equivalency (==)"""

    name = "ssdeep"
    digest_size = libssdeep_wrapper.FUZZY_MAX_RESULT

    def __init__(self, buf=None, hash=None):
        """Initialises a ssdeep object. Can be initialised with either a
        a buffer through the use of the keyword argument 'buf' or a
        previously computed ssdeep hash using the keyword argument ('hash').
        
        Note that only objects initialised using a buffer can be updated.

        Note that if both buf and hash parameters are provided on
        initialisation, buf will be used and hash will be ignored."""
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
            raise InvalidOperation("Cannot update sdeep created from hash")

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

    def compare(self, b):
        return libssdeep_wrapper.compare(self.hexdigest(), b.hexdigest())

    def __sub__(self, b):
        return self.compare(b)

    def __eq__(self, b):
        if isinstance(b, ssdeep):
            return self.hexdigest() == b.hexdigest()
        elif isinstance(b, basestring):
            return self.hexdigest() == b
        else:
            return False


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

    name -- the name of the algorithm being used (ie. "sdhash")
    
    Operators:
        
    __sub__ -- instances can have hashes compared with subtraction (-)
    __eq__ -- instances can be tested for hash equivalency (==)"""

    name = "sdhash"

    def __init__(self, buf=None, hash=None):
        """Initialises a sdhash object. Can be initialised with either a
        a buffer through the use of the keyword argument 'buf' or a
        previously computed sdhash hash using the keyword argument ('hash').

        Note that sdhash objects do not support update().

        Note that if both buf and hash parameters are provided on
        initialisation, buf will be used and hash will be ignored."""
        if buf is not None:
            if len(buf) < 512:
                raise ValueError("sdhash requires buffer >= 512 in size")
            self._sdbf = sdhash_wrapper.sdbf_from_buffer(buf)
        elif hash is not None:
            self._sdbf = sdhash_wrapper.sdbf_from_hash(hash)
        else:
            raise ValueError("One of buf or hash must be set.")

    def __del__(self):
        if hasattr(self, "_sdbf"):
            del self._sdbf 

    def hexdigest(self):
        """Return the digest value as a string of hexadecimal digits."""
        return self._sdbf.to_string()

    def copy(self):
        """Returns a new instance which identical to this instance."""
        return sdhash(hash=self.hexdigest())

    @staticmethod
    def update(self, *args):
        """Not supported."""
        raise InvalidOperation("sdhash does not support update()")

    def compare(self, b):
        score = self._sdbf.compare(b._sdbf, 0)
        return score

    def __sub__(self, b):
        return self.compare(b)

    def __eq__(self, b):
        if isinstance(b, sdhash):
            return self.hexdigest() == b.hexdigest()
        elif isinstance(b, basestring):
            return self.hexdigest() == b
        else:
            return False


class tlsh(object):
    """Represents tlsh's computed fuzzy hash of a string of
    information.

    tlsh objects can be created either with a buffer or with a
    previously computed hexdigest. tlsh objects can be updated
    with calls to .update() method provided that no prior call
    to the .hexdigest(), .copy() or comparison methods have been
    made.

    Methods:

    hexdigest() -- return the current digest as a string of hex digits
    copy() --  returns a copy of the current hash object
    diff() -- calls the underlying diff method for Tlsh objects
    diffxlen() -- calls the underlying diffxlen method for Tlsh objects,
                  which ignores length checks

    Attributes:

    name -- the name of the algorithm being used (ie. "tlsh")

    Operators:

    __sub__ -- instances can have hashes compared with subtraction (-)
    __eq__ -- instances can be tested for hash equivalency (==)"""

    name = "tlsh"

    _MIN_LEN = 256

    def __init__(self, buf=None, hash=None):
        """Initialises a tlsh object. Can be initialised with either a
        a buffer through the use of the keyword argument 'buf' or a
        previously computed tlsh hash using the keyword argument ('hash').

        Note that tlsh objects only support update() when they are created
        from a buffer and prior to a call to the hexdigest() method.
        Once hexdigest() has been the tlsh object is considered 'final'
        and subsequent calls to update() will raise an exception. Note
        that comparisons implicitly 'finalise' a tlsh object.

        Note that forcing a hash on a buffer smaller than 256 characters
        is not supported.

        Note that if both buf and hash parameters are provided on
        initialisation, buf will be used and hash will be ignored."""

        self._buf_len = 0
	self._final = False
        self._tlsh = tlsh_wrapper.Tlsh()

        if buf is not None:
            self.update(buf)
        elif hash is not None:
            self._tlsh.fromTlshStr(hash)
	    self._final = True
        else:
            raise ValueError("One of buf or hash must be set.")

    def __del__(self):
        if hasattr(self, "_tlsh") and not self._final:
            # TODO: investigate potential small leak in underlying class?
            try:
                self._tlsh.final()
            except ValueError:
                # ValueError on small buffer OK. Else, raise.
                if self._buf_len >= self._MIN_LEN:
                    raise
            del self._tlsh

    def hexdigest(self):
        """Return the digest value as a string of hexadecimal digits."""
        if not self._final:
            if self._buf_len >= self._MIN_LEN:
                self._tlsh.final()
                self._final = True
            else:
                raise ValueError("tlsh requires buffer with length >= %d "
                                 "for mode where force = %s" % \
                                 (self._MIN_LEN, False))
        return self._tlsh.hexdigest()

    def copy(self):
        """Returns a new instance which identical to finalised version
        of this instance. Note: this will 'finalise' this tlsh instance!"""
        return tlsh(hash=self.hexdigest())

    def update(self, buf):
        """Update this hash object's state with the provided string."""
        if self._final:
            raise InvalidOperation("Cannot update finalised tlsh")
        else:
	    self._buf_len += len(buf)
            return self._tlsh.update(buf)

    def diff(self, b):
        if isinstance(b, tlsh):
            return tlsh_wrapper.diff(self.hexdigest(), b.hexdigest())
        elif isinstance(b, basestring):
            return tlsh_wrapper.diff(self.hexdigest(), b)
        else:
            raise ValueError("Comparison object must be instance of "
                             "basestring or tlsh")

    def diffxlen(self, b):
        if isinstance(b, tlsh):
            return tlsh_wrapper.diffxlen(self.hexdigest(), b.hexdigest())
        elif isinstance(b, basestring):
            return tlsh_wrapper.diffxlen(self.hexdigest(), b)
        else:
            raise ValueError("Comparison object must be instance of "
                             "basestring or tlsh")

    def compare(self, b):
        return 100 - self.diff(b)

    def __sub__(self, b):
        return self.compare(b)

    def __eq__(self, b):
        if isinstance(b, tlsh):
            return self.hexdigest() == b.hexdigest()
        elif isinstance(b, basestring):
            return self.hexdigest() ==  b
        else:
            return False
