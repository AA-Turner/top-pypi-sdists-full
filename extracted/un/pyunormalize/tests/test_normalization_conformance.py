"""Unicode normalization conformance tests.

This module loads and validates the Unicode Character Database (UCD) files
used by the normalization conformance tests. It verifies that `NFC`, `NFD`,
`NFKC`, and `NFKD` satisfy the invariants defined in `NormalizationTest.txt`.
It also uses `DerivedAge.txt` to verify that assigned code points not listed
in `@Part1` preserve identity in every normalization form.

Conformance data is provided by the UCD:
- https://www.unicode.org/Public/18.0.0/ucd/NormalizationTest.txt
- https://www.unicode.org/Public/18.0.0/ucd/DerivedAge.txt
"""

import unittest
from pathlib import Path

from pyunormalize import NFC, NFD, NFKC, NFKD, UNICODE_VERSION

DATA_DIR = Path(__file__).resolve().parent / "data"

NORMALIZATION_TEST_TXT = "NormalizationTest.txt"
DERIVED_AGE_TXT = "DerivedAge.txt"


def _read_ucd_file(filename):
    path = DATA_DIR / filename
    lines = path.read_text(encoding="utf-8").splitlines()

    expected_header = f"# {filename[:-4]}-{UNICODE_VERSION}.txt"
    actual_header = lines[0] if lines else None

    if actual_header != expected_header:
        raise RuntimeError(
            f"Unicode version mismatch in {filename!r} "
            f"(expected header {expected_header!r}, got {actual_header!r})."
        )

    return lines


def _parse_assigned_codepoints():
    assigned = set()

    for lineno, line in enumerate(_read_ucd_file(DERIVED_AGE_TXT), 1):
        line = line.partition("#")[0].strip()

        if not line:
            continue

        field = line.partition(";")[0].strip()
        start, separator, end = field.partition("..")

        try:
            first = int(start, 16)
            last = int(end, 16) if separator else first
        except ValueError as error:
            raise RuntimeError(
                f"Invalid code point range at line {lineno} "
                f"in {DERIVED_AGE_TXT!r}: {field!r}."
            ) from error

        if first > last:
            raise RuntimeError(
                f"Invalid descending range at line {lineno} "
                f"in {DERIVED_AGE_TXT!r}: {field!r}."
            )

        assigned.update(range(first, last + 1))

    return assigned


def _codepoints_to_string(field, lineno):
    try:
        return "".join([chr(int(cp, 16)) for cp in field.split()])
    except ValueError as error:
        raise RuntimeError(
            f"Invalid code point at line {lineno} "
            f"in {NORMALIZATION_TEST_TXT!r}: {field!r}."
        ) from error


def _parse_test_data():
    normalization_cases = []
    part1_points = set()
    in_part1 = False

    for lineno, line in enumerate(_read_ucd_file(NORMALIZATION_TEST_TXT), 1):
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        if line.startswith("@"):
            in_part1 = line.startswith("@Part1")
            continue

        content = line.partition("#")[0].strip()
        fields = [field.strip() for field in content.split(";")]

        if fields and fields[-1] == "":
            fields.pop()

        if len(fields) != 5:
            raise RuntimeError(
                f"Expected five fields at line {lineno} "
                f"in {NORMALIZATION_TEST_TXT!r}: {line!r}."
            )

        case = tuple(
            _codepoints_to_string(field, lineno)
            for field in fields
        )
        normalization_cases.append((lineno, case))

        if in_part1:
            codepoints = fields[0].split()

            if len(codepoints) != 1:
                raise RuntimeError(
                    f"Expected one c1 code point at line {lineno} "
                    f"in @Part1: {fields[0]!r}."
                )

            part1_points.add(int(codepoints[0], 16))

    assigned = _parse_assigned_codepoints()
    identity_codepoints = assigned - part1_points

    return normalization_cases, identity_codepoints


def _format_case(case):
    return "; ".join(
        " ".join([f"{ord(char):04X}" for char in field])
        for field in case
    )


class TestUnicodeNormalization(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data, cls.identity_codepoints = _parse_test_data()

    def _check_normalization(self, func, expected_index, input_indices):
        for lineno, case in self.data:
            expected = case[expected_index]
            actuals = tuple(func(case[index]) for index in input_indices)

            if any(actual != expected for actual in actuals):
                input_columns = ", ".join(
                    [f"c{index + 1}" for index in input_indices]
                )
                self.fail(
                    f"{func.__name__} mismatch at line {lineno}: "
                    f"expected c{expected_index + 1}, "
                    f"got normalizations of {input_columns} "
                    f"(case: {_format_case(case)})."
                )

    def test_nfc(self):
        # c2 == toNFC(c1) == toNFC(c2) == toNFC(c3)
        self._check_normalization(
            NFC,
            expected_index=1,
            input_indices=(0, 1, 2),
        )

        # c4 == toNFC(c4) == toNFC(c5)
        self._check_normalization(
            NFC,
            expected_index=3,
            input_indices=(3, 4),
        )

    def test_nfd(self):
        # c3 == toNFD(c1) == toNFD(c2) == toNFD(c3)
        self._check_normalization(
            NFD,
            expected_index=2,
            input_indices=(0, 1, 2),
        )

        # c5 == toNFD(c4) == toNFD(c5)
        self._check_normalization(
            NFD,
            expected_index=4,
            input_indices=(3, 4),
        )

    def test_nfkc(self):
        # c4 == toNFKC(c1) == ... == toNFKC(c5)
        self._check_normalization(
            NFKC,
            expected_index=3,
            input_indices=(0, 1, 2, 3, 4),
        )

    def test_nfkd(self):
        # c5 == toNFKD(c1) == ... == toNFKD(c5)
        self._check_normalization(
            NFKD,
            expected_index=4,
            input_indices=(0, 1, 2, 3, 4),
        )

    def test_identity_for_assigned_codepoints(self):
        # X == toNFC(X) == toNFD(X) == toNFKC(X) == toNFKD(X)
        forms = (NFC, NFD, NFKC, NFKD)

        for codepoint in self.identity_codepoints:
            char = chr(codepoint)
            for func in forms:
                if func(char) != char:
                    self.fail(
                        f"{func.__name__} did not preserve identity "
                        f"for U+{codepoint:04X}."
                    )


if __name__ == "__main__":
    unittest.main()
