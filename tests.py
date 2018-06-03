import unittest
import os
import resource

import fuzzyhashlib

class BaseFuzzyHashTest(unittest.TestCase):
    """Base fuzzyhashlib test class."""

    FUZZY_HASH_CLASS = None
    TEST_DATA_PATH = None
    KNOWN_RESULT = None
    MEM_LEAK_ITERATIONS = 1000
    MEM_LEAK_TOLERANCE = 64

    @classmethod
    def setUpClass(cls):
        if cls is BaseFuzzyHashTest:
            raise unittest.SkipTest()
        super(BaseFuzzyHashTest, cls).setUpClass()

    @property
    def known_data(self):
        dir_path = os.path.dirname(__file__)
        data_path = os.path.join(dir_path, "LICENSE")
        with open(data_path, "rb") as data_file:
            return data_file.read()
    
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
        self.h2 = self.FUZZY_HASH_CLASS(self.test_data_2)

    def test_known_result(self):
        computed = self.FUZZY_HASH_CLASS(self.known_data)
        known = self.FUZZY_HASH_CLASS(hash=self.KNOWN_RESULT)
        self.assertEquals(computed, known)

    def test_comparisons(self):
        # Test with .compare() method.
        self.assertNotEqual(self.h1.hexdigest(), self.h2.hexdigest())
        self.assertNotEqual(self.h1.compare(self.h2), 100)
        self.assertEqual(self.h1.compare(self.h2),
                         self.h2.compare(self.h1),
                         msg="commutative test failed")

        # Test with subtraction operator.
        self.assertNotEqual(self.h1.hexdigest(), self.h2.hexdigest())
        self.assertNotEqual(self.h1 - self.h2, 100)
        self.assertEqual(self.h1 - self.h2, self.h2 - self.h1,
                         msg="commutative test failed")

        # Test .compare and subtraction are the same.
        self.assertEqual(self.h1 - self.h2, self.h1.compare(self.h2))

        # Test comparisons with self a score of 100.
        msg = "(%s) comparing self to self did not score 100"
        self.assertEqual(self.h1 - self.h1, 100, msg=msg % self.h1.name)
        self.assertEqual(self.h2 - self.h2, 100, msg=msg % self.h2.name)

    def test_equalities(self):
        # gclen's PR enables digest-to-object comparisons. Test combinations.
        msg = "(%s) comparing self to self was not equal"
        self.assertEqual(self.h1,
                         self.h1,
                         msg=msg % self.h1.name)
        self.assertEqual(self.h1,
                         self.h1.hexdigest(),
                         msg=msg % self.h1.name)
        self.assertEqual(self.h1.hexdigest(),
                         self.h1,
                         msg=msg % self.h1.name)
        self.assertEqual(self.h1.hexdigest(),
                         self.h1.hexdigest(),
                         msg=msg % self.h1.name)
        self.assertEqual(self.h2,
                         self.h2,
                         msg=msg % self.h2.name)
        self.assertEqual(self.h2,
                         self.h2.hexdigest(),
                         msg=msg % self.h2.name)
        self.assertEqual(self.h2.hexdigest(),
                         self.h2,
                         msg=msg % self.h2.name)
        self.assertEqual(self.h2.hexdigest(),
                         self.h2.hexdigest(),
                         msg=msg % self.h2.name)

    def test_copy(self):
        h3 = self.h1.copy()
        self.assertEqual(self.h1.hexdigest(), h3.hexdigest())
        self.assertTrue(self.h1 == h3)
        self.assertEqual(self.h1, self.h1)
        self.assertEqual(self.h1 - h3, h3 - self.h1,
                         msg="commutative test failed")

    def test_update(self):
        self.h1.update(self.test_data_2)
        self.assertNotEqual(self.h1, self.h1.hexdigest())

    def test_create_from_hash(self):
        h3 = self.FUZZY_HASH_CLASS(hash=self.h1.hexdigest())
        self.assertEquals(h3, self.h1)

        # So far all algorithms created from hashes cannot be updated. Test.
        with self.assertRaises(fuzzyhashlib.InvalidOperation) as exc:
            h3.update("this should error")

    def test_leak(self):
        initial = resource.getrusage(resource.RUSAGE_SELF)[2]
        threshold = initial + self.MEM_LEAK_TOLERANCE
        x = 0
        delta = 0
        buf = 100000 * chr(x & 0xff)
        while x < self.MEM_LEAK_ITERATIONS:
            # Compute hash for arbitrary data, check if more mem is used.
            h1 = self.FUZZY_HASH_CLASS(buf)
            current = \
                resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            delta = current - initial
            self.assertLessEqual(current, threshold,
                "memory usage increased %s after %d iterations (%s); "
                "tolerance: %d" % \
		    (delta, x, self.h1.name, self.MEM_LEAK_TOLERANCE))
            x += 1


class TestSsdeep(BaseFuzzyHashTest):
    """Test fuzzyhashlib.ssdeep"""

    FUZZY_HASH_CLASS = fuzzyhashlib.ssdeep
    TEST_DATA_PATH = fuzzyhashlib.libssdeep_wrapper.libssdeep_path
    KNOWN_RESULT = "192:nU6G5KXSD9VYUKhu1JVF9hFGvV/QiGkS594drFjuHYx5dvTrLh3k" \
        "TSEn7HbHR:U9vlKM1zJlFvmNz5VrlkTS07Ht"


class TestSdhash(BaseFuzzyHashTest):
    """Test fuzzyhashlib.sdhash"""

    FUZZY_HASH_CLASS = fuzzyhashlib.sdhash
    TEST_DATA_PATH = fuzzyhashlib.sdhash_wrapper.sdbf_library_path
    KNOWN_RESULT = "sdbf:03:0::11358:sha1:256:5:7ff:160:1:160:IoFBClI" \
        "QqFAxCa4JCEns8ACBIAQ1UEwAAkUiSoDIEiyNm5QQCJQDhEGISPghTIDWVVaATIMjJC" \
        "hQK4CkgSAgtGCEbIacfGUQgxygkgBEgaRBigAhCoCQO4ZGCEtuB8RgLuQKaAk2AgKA6" \
        "SAQGCirEEa1doFBwTwyKiAxLEhRKHAYArAUgAkICheDgGY0QVtLKByAwQSQ4CoFAwBW" \
        "eQHyCIqy4IiACikBBKsAAjXoGAhgFEgCpAzEjYYAFoZT0AAB4QEQCDQC0EoiCkpCUVI" \
        "I33eqdIAJGioMmBXseEq9Wgg4MxhVNCIRPFMLH6pJyZgRDJDRKAIkcaBC4AEgjIjqAQ=="

    def test_invalid_buffer_size_raises(self):
        with self.assertRaises(ValueError) as context:
            fuzzyhashlib.sdhash("buffer_too_short")
        self.assertEquals(context.exception.message,
                          "sdhash requires buffer >= 512 in size")

    def test_update(self):
        # Override default to capture .update() being unsupported.
        with self.assertRaises(Exception) as context:
            self.h1.update(self.test_data_2)
        self.assertEquals(context.exception.message,
                          "sdhash does not support update()")

class TestTlsh(BaseFuzzyHashTest):
    """Test fuzzyhashlib.tlsh"""

    FUZZY_HASH_CLASS = fuzzyhashlib.tlsh
    TEST_DATA_PATH = fuzzyhashlib.tlsh_wrapper.tlsh_library_path
    KNOWN_RESULT = \
        "1632623FBA48037706C20162BB9764CBF2" \
        "1E903F3B552568354CC1681F6BA6543FB6EA"
    MEM_LEAK_ITERATIONS = 10000
    MEM_LEAK_TOLERANCE = 1024

    def test_invalid_buffer_size_raises(self):
        with self.assertRaises(ValueError) as context:
            fuzzyhashlib.tlsh("buffer_too_short").hexdigest()
        self.assertTrue(
            context.exception.message.startswith("tlsh requires buffer"))
