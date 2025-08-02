import pickle  # nosec B403
from unittest import TestCase

import numpy as np

from encoders.encoder import BytesLabelEncoder, StringLabelEncoder


class EncoderTest(TestCase):
    def test_bytes(self):
        stuff = [b"asd", b"qwe", b"zxc"] * 2

        le = BytesLabelEncoder()
        le.partial_fit(stuff)
        le.partial_fit(stuff)
        self.assertEqual(le.labels, {b"asd": 0, b"qwe": 1, b"zxc": 2})
        np.testing.assert_array_equal(le.transform(stuff), np.array([0, 1, 2, 0, 1, 2]))

    def test_bytes_finalize_empty(self):
        le = BytesLabelEncoder()
        le.finalize()
        np.testing.assert_array_equal(le.classes, np.array([]))

    def test_bytes_inv(self):
        stuff = [b"asd", b"qwe", b"zxc"] * 2

        le = BytesLabelEncoder()
        le.partial_fit(stuff)
        encoded = le.transform(stuff)
        le.finalize()
        np.testing.assert_array_equal(le.classes, np.array(stuff[:3]))
        result = le.inverse_transform(encoded)
        np.testing.assert_array_equal(result, np.array(stuff))

    def test_bytes_transform_fail(self):
        stuff = [b"asd", b"qwe", b"zxc"] * 2

        le = BytesLabelEncoder()
        le.finalize()
        with self.assertRaises(IndexError):
            le.transform(stuff)

    def test_bytes_typeerror(self):
        with self.assertRaises(TypeError):
            le = BytesLabelEncoder()
            le.partial_fit(["asd"])

    def test_bytes_pickle(self):
        stuff = [b"asd", b"qwe", b"zxc"] * 2

        le = BytesLabelEncoder()
        le.partial_fit(stuff)
        le2 = pickle.loads(pickle.dumps(le))  # nosec B301
        self.assertEqual(le.labels, le2.labels)

    def test_str(self):
        stuff = ["asü", "😀", "zxä"] * 2

        le = StringLabelEncoder()
        le.partial_fit(stuff)
        le.partial_fit(stuff)
        self.assertEqual(le.labels, {"asü": 0, "😀": 1, "zxä": 2})
        np.testing.assert_array_equal(le.transform(stuff), np.array([0, 1, 2, 0, 1, 2]))

    def test_str_finalize_empty(self):
        le = StringLabelEncoder()
        le.finalize()
        np.testing.assert_array_equal(le.classes, np.array([]))

    def test_str_inv(self):
        stuff = ["asü", "😀", "zxä"] * 2

        le = StringLabelEncoder()
        le.partial_fit(stuff)
        encoded = le.transform(stuff)
        le.finalize()
        np.testing.assert_array_equal(le.classes, np.array(stuff[:3]))
        result = le.inverse_transform(encoded)
        np.testing.assert_array_equal(result, np.array(stuff))

    def test_str_transform_fail(self):
        stuff = ["asü", "😀", "zxä"] * 2

        le = StringLabelEncoder()
        le.finalize()
        with self.assertRaises(IndexError):
            le.transform(stuff)

    def test_str_typeerror(self):
        with self.assertRaisesRegex(TypeError, "expected str, bytes found"):
            le = StringLabelEncoder()
            le.partial_fit([b"asd"])

    def test_str_pickle(self):
        stuff = ["asü", "😀", "zxä"] * 2

        le = StringLabelEncoder()
        le.partial_fit(stuff)
        le2 = pickle.loads(pickle.dumps(le))  # nosec B301
        self.assertEqual(le.labels, le2.labels)


if __name__ == "__main__":
    import unittest

    unittest.main()
