import unittest

import fuzzyhashlib
from fuzzyhashlib import libssdeep_wrapper
from fuzzyhashlib.libssdeep_wrapper import library as libpath

class TestSsdeep(unittest.TestCase):
    """Test fuzzyhashlib.ssdeep"""

    def test_ssdeep(self):
        # Get the hash of the library being used
        f1 = fuzzyhashlib.fuzzy(open(libpath, "rb").read())
        h1 = f1.hexdigest()

        # Get the hash of something else
        f2 = fuzzyhashlib.fuzzy(open(__file__, "r").read())
        h2 = f2.hexdigest()

        # Start comparing things
        self.assertEqual(f1.name, "ssdeep")
        self.assertNotEqual(h1, h2)
        self.assertNotEqual(f1 - f2, 100)
        self.assertEqual(f1 - f2, f2 - f1, msg="commutative test failed")
        self.assertEqual(f1, f1)
        self.assertEqual(f2, f2)
        self.assertEqual(f1 - f1, 100)
        self.assertEqual(f2 - f2, 100)

        # Test copy()
        f3 = f1.copy()
        h3 = f1.hexdigest()
        self.assertEqual(h1, h3)
        self.assertTrue(f1 == f3)
        self.assertEqual(f1, f1)
        self.assertEqual(f1 - f3, f3 - f1, msg="commutative test failed")

        # Test update()
        f3.update(open(__file__, "r").read())
        h3 = f3.hexdigest()
        self.assertNotEqual(h1, h3)
        self.assertFalse(f1 == f3)



class TestLibFuzzyWrapper(unittest.TestCase):

    def test_wrapper(self):
        #get the hash of the library being used
        ret, h1 = libssdeep_wrapper.hash_filename(libssdeep_wrapper.library)
        self.assertEqual(0, ret)

        #get hash of buf represented by the library - assert same as before
        buf = open(libssdeep_wrapper.library, "rb").read()
        ret, h2 = libssdeep_wrapper.hash(buf)
        self.assertEqual(0, ret)
        self.assertEqual(h1, h2)
        self.assertEqual(100, libssdeep_wrapper.compare(h1, h2))
        self.assertEqual(100, libssdeep_wrapper.compare(h2, h1))

        #get the hash of something else and compare
        buf = open(__file__, "r").read()
        ret, h3 = libssdeep_wrapper.hash(buf)
        self.assertEqual(0, ret)
        self.assertNotEqual(h1, h3)
        self.assertEqual(0, libssdeep_wrapper.compare(h1, h3))
