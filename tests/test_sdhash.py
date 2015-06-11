import unittest

import fuzzyhashlib
from fuzzyhashlib import sdhash_wrapper
from fuzzyhashlib.sdhash_wrapper import sdbf_library_path

class TestSdhash(unittest.TestCase):
    """Test fuzzyhashlib.sdhash"""

    def test_sdhash(self):
        # Get the hash of the library being used
        f1 = fuzzyhashlib.sdhash(open(sdbf_library_path, "rb").read())
        h1 = f1.hexdigest()
        print("\nh1: %s" % h1)

        # Get the hash of something else
        f2 = fuzzyhashlib.sdhash(open(__file__, "r").read())
        h2 = f2.hexdigest()
        print("\nh2: %s" % h2)

        # Start comparing things
        self.assertEqual(f1.name, "sdhash")
        self.assertNotEqual(h1, h2)
        self.assertNotEqual(f1 - f2, 100)
        self.assertEqual(f1 - f2, f2 - f1, msg="commutative test failed")
        self.assertEqual(f1, f1)
        self.assertEqual(f2, f2)
        self.assertEqual(f1 - f1, 100)
        self.assertEqual(f2 - f2, 100)

        # Test copy()
        f3 = f1.copy()
        h3 = f3.hexdigest()
        print("\nh3: %s" % h3)
        self.assertEqual(h1, h3)
        self.assertTrue(f1 == f3)
        self.assertEqual(f1, f1)
        self.assertEqual(f1 - f3, f3 - f1, msg="commutative test failed")

        # Test update()
        f3.update(open(__file__, "r").read())
        h3 = f3.hexdigest()
        self.assertNotEqual(h1, h3)
        self.assertFalse(f1 == f3)
