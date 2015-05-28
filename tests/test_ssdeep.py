import unittest

import fuzzyhashlib
from fuzzyhashlib import libssdeep_wrapper
from fuzzyhashlib.libssdeep_wrapper import library as libpath

class TestSsdeep(unittest.TestCase):
    """Test fuzzyhashlib.ssdeep"""

    def test_ssdeep(self):
        # Get the hash of the library being used
        f1 = fuzzyhashlib.ssdeep(open(libpath, "rb").read())
        h1 = f1.hexdigest()

        # Get the hash of something else
        f2 = fuzzyhashlib.ssdeep(open(__file__, "r").read())
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
