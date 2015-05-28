import libssdeep_wrapper

"""Wrapper for various fuzzy hashing libraries which attempts to be as similar
in interface to hashlib as possible.

Supports:
    * ssdeep
    * sdhash

This also ships with built libraries for the supported algorithms in order
to minimise extenal dependencies.

[sptonkin@outlook.com]"""


class ssdeep:
    """A ssdeep represents ssdeep's computed fuzzy hash of a string of
    information.

    Methods:
    
    update() -- updates the current digest with an additional string
    hexdigest() -- return the current digest as a string of hex digits
    copy() -  returns a copy of the current hash object

    Attributes:

    name -- the name of the alogorthm being used (ie. "ssdeep")
    digest_size -- the maximum size in bytes
    
    Operators:
        
    __sub__ -- ssdeep objects can have hashes compared with subtraction (-)
    __eq__ -- ssdeep objects can be tested for hash equivalency (==)"""

    name = "ssdeep"
    digest_size = libssdeep_wrapper.FUZZY_MAX_RESULT

    def __init__(self, buf=None):
        """Returns ssdeep hash obj, optionally initialised with with buf."""
        self.name = "ssdeep"
        self.digest_size = libssdeep_wrapper.FUZZY_MAX_RESULT
        self._state = libssdeep_wrapper.fuzzy_new()
        if buf is not None:
            self.update(buf)

    def __del__(self):
        libssdeep_wrapper.fuzzy_free(self._state)

    def hexdigest(self):
        """Return the digest value as a string of hexadecimal digits."""
        return libssdeep_wrapper.fuzzy_digest(self._state, 0)

    def update(self, buf):
        """Update this hash object's state with the provided string."""
        return libssdeep_wrapper.fuzzy_update(self._state, buf)

    def copy(self):
        """Returns a new fuzzy instance which should be identical to this
        instance."""
        temp = ssdeep()
        temp.name = self.name
        temp.digest_size = self.digest_size
        libssdeep_wrapper.fuzzy_free(temp._state)
        temp._state = libssdeep_wrapper.fuzzy_clone(self._state)
        return temp

    def __sub__(self, b):
        return libssdeep_wrapper.compare(self.hexdigest(), b.hexdigest())

    def __eq__(self, b):
        return \
            libssdeep_wrapper.compare(self.hexdigest(), b.hexdigest()) == 100
