"""Tests for geocif.data_prep.build_usa_asd_crosswalk.latest_asd (no network)."""

import unittest

import pandas as pd


def _records(rows):
    cols = ["year", "state_name", "state_fips_code", "county_code", "asd_code", "asd_desc"]
    return pd.DataFrame(rows, columns=cols)


class TestLatestAsd(unittest.TestCase):
    def test_one_row_per_county_from_latest_year(self):
        from geocif.data_prep.build_usa_asd_crosswalk import latest_asd

        table = latest_asd(_records([
            ["2016", "ALABAMA", "01", "001", "40", "BLACK BELT"],
            ["2024", "ALABAMA", "01", "001", "40", "BLACK BELT"],
            ["2020", "IOWA", "19", "169", "40", "WEST CENTRAL"],
            ["2024", "IOWA", "19", "169", "50", "CENTRAL"],
            ["2024", "IOWA", "19", "998", "50", "CENTRAL"],
        ]))
        self.assertEqual(table["region_id"].tolist(), [1001, 19169])
        self.assertEqual(table["district_id"].tolist(), ["0140", "1950"])
        self.assertEqual(table["district_name"].tolist(), ["Black Belt", "Central"])
        self.assertEqual(table["admin_1"].tolist(), ["Alabama", "Iowa"])

    def test_two_asds_in_latest_year_raises(self):
        from geocif.data_prep.build_usa_asd_crosswalk import latest_asd

        with self.assertRaises(ValueError):
            latest_asd(_records([
                ["2024", "IOWA", "19", "169", "40", "WEST CENTRAL"],
                ["2024", "IOWA", "19", "169", "50", "CENTRAL"],
            ]))


if __name__ == "__main__":
    unittest.main()
