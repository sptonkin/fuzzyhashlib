import unittest
import os
import resource

import fuzzyhashlib

class BaseFuzzyHashTest(unittest.TestCase):
    """Test fuzzyhashlib.ssdeep"""

    FUZZY_HASH_CLASS = None
    TEST_DATA_PATH = None

    @classmethod
    def setUpClass(cls):
        if cls is BaseFuzzyHashTest:
            raise unittest.SkipTest()
        super(BaseFuzzyHashTest, cls).setUpClass()
    
    def setUp(self):
        # Ensure inheriting class specifies the class to test.
        if self.FUZZY_HASH_CLASS is None:
            msg = "%s did not set FUZZY_HASH_CLASS" % self.__class__.__name__
            raise NotImplementedError(msg)

        # Ensure inheriting class specifies where to find its library.
        if self.TEST_DATA_PATH is None:
            msg = "%s did not set TEST_DATA_PATH" % self.__class__.__name__
            raise NotImplementedError(msg)
        self.assertTrue(os.path.exists(self.TEST_DATA_PATH))
        with open(self.TEST_DATA_PATH, "rb") as test_data_file:
            self.test_data_1 = test_data_file.read()
        with open(__file__, "rb") as test_data_file:
            self.test_data_2 = test_data_file.read()

        # Generate some test hash objects.
        self.h1 = self.FUZZY_HASH_CLASS(self.test_data_1)
        self.d1 = self.h1.hexdigest()
        self.h2 = self.FUZZY_HASH_CLASS(self.test_data_2)
        self.d2 = self.h2.hexdigest()

    def test_comparisons(self):
        # Start comparing things.
        self.assertNotEqual(self.d1, self.d2)
        self.assertNotEqual(self.h1 - self.h2, 100)
        self.assertEqual(self.h1 - self.h2, self.h2 - self.h1,
                         msg="commutative test failed")
        self.assertEqual(self.h1, self.h1)
        self.assertEqual(self.h2, self.h2)
        self.assertEqual(self.h1 - self.h1, 100)
        self.assertEqual(self.h2 - self.h2, 100)

    def test_copy(self):
        h3 = self.h1.copy()
        d3 = self.h1.hexdigest()
        self.assertEqual(self.d1, d3)
        self.assertTrue(self.h1 == h3)
        self.assertEqual(self.h1, self.h1)
        self.assertEqual(self.h1 - h3, h3 - self.h1,
                         msg="commutative test failed")

    def test_update(self):
        self.h1.update(self.test_data_2)
        self.assertNotEqual(self.d1, self.h1.hexdigest())

    def test_leak(self):
        initial = resource.getrusage(resource.RUSAGE_SELF)[2]
        for x in xrange(0, 1000):
            # Compute hash for arbitrary data, check if more mem is used.
            self.h1 = self.FUZZY_HASH_CLASS(100000 * chr(x & 0xff))
            current = \
                resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            self.assertEquals(current, initial,
                "memory usage increased after %d iterations (%s)" % \
                (x, self.h1.name))



class TestSsdeep(BaseFuzzyHashTest):
    """Test fuzzyhashlib.ssdeep"""

    FUZZY_HASH_CLASS = fuzzyhashlib.ssdeep
    TEST_DATA_PATH = fuzzyhashlib.libssdeep_wrapper.libssdeep_path


class TestSdhash(BaseFuzzyHashTest):
    """Test fuzzyhashlib.sdhash"""

    FUZZY_HASH_CLASS = fuzzyhashlib.sdhash
    TEST_DATA_PATH = fuzzyhashlib.sdhash_wrapper.sdbf_library_path

    def test_update(self):
        # Override default to capture .update() being unsupported.
        with self.assertRaises(Exception) as context:
            self.h1.update(self.test_data_2)
        self.assertEquals(context.exception.message,
                          "Update not supported for sdbf.")
