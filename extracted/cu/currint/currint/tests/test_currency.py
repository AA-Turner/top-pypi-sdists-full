# encoding: utf8
from __future__ import unicode_literals
from decimal import Decimal
from unittest import TestCase
from ..currency import currencies, Currency


class CurrencyTests(TestCase):

    def test_major_to_minor(self):
        self.assertEqual(
            currencies["GBP"].major_to_minor(1),
            100,
        )
        self.assertEqual(
            currencies["GBP"].major_to_minor(Decimal("1.43")),
            143,
        )
        with self.assertRaises(ValueError):
            currencies["GBP"].major_to_minor(Decimal("1.435"))
        # Non-decimal currency
        self.assertEqual(
            currencies["MRO"].major_to_minor(Decimal(5)),
            25,
        )

    def test_minor_to_major(self):
        self.assertEqual(
            currencies["GBP"].minor_to_major(100),
            Decimal("1"),
        )
        self.assertEqual(
            currencies["GBP"].minor_to_major(143),
            Decimal("1.43"),
        )
        # Non-decimal currency
        self.assertEqual(
            currencies["MRO"].minor_to_major(26),
            Decimal("5.2"),
        )

    def test_format(self):
        self.assertEqual(
            Currency("GBP", "826", 2, 'Pound Sterling', prefix="£").format(100),
            "£1.00",
        )
        self.assertEqual(
            currencies["USD"].format(43),
            "0.43 USD",
        )
        # Non-decimal currency
        self.assertEqual(
            currencies["MRO"].format(7),
            "1.4 MRO",
        )
        # Negative value less than 0 and greater than -1 major unit
        self.assertEqual(
            currencies["USD"].format(-60),
            "-0.60 USD",
        )

        # 0 exponent currency
        self.assertEqual(
            currencies["JPY"].format(100),
            "100 JPY",
        )

    def test_format_decimal(self):
        self.assertEqual(
            currencies["GBP"].format_decimal(100),
            "1.00",
        )
        self.assertEqual(
            currencies["USD"].format_decimal(43),
            "0.43",
        )
        # Non-decimal currency
        self.assertEqual(
            currencies["MRO"].format_decimal(7),
            "1.4",
        )

        # Negative value less than 0 and greater than -1 major unit
        self.assertEqual(
            currencies["USD"].format_decimal(-60),
            "-0.60",
        )

        # 0 exponent currency
        self.assertEqual(
            currencies["JPY"].format_decimal(100),
            "100",
        )

    def test_equality(self):
        self.assertEqual(
            currencies['GBP'],
            currencies['GBP']
        )
        self.assertNotEqual(
            currencies['GBP'],
            currencies['USD']
        )
        self.assertNotEqual(
            currencies['GBP'],
            object(),
        )
