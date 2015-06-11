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

        # Get the hash of something else
        f2 = fuzzyhashlib.sdhash(open(__file__, "r").read())
        h2 = f2.hexdigest()

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
        self.assertEqual(h1, h3)
        self.assertTrue(f1 == f3)
        self.assertEqual(f1, f1)
        self.assertEqual(f1 - f3, f3 - f1, msg="commutative test failed")

        # Test update()
        with self.assertRaises(Exception) as ctx:
            f3.update(open(__file__, "r").read())
        self.assertEquals(ctx.exception.message,
                           "Update not supported for sdbf.")
