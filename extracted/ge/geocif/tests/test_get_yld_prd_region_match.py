"""Regression tests for `geocif.ml.stats.get_yld_prd` region matching.

Bug audited Jun 7 2026 (India soybean threshold-sweep): extract_sweep
writes regions as slugs (``andhra_pradesh``, ``district_of_columbia``)
but AMIS Excel files store canonical Title-Case with spaces
(``Andhra Pradesh``). The old equality on ``.lower()`` left underscores
on the slug side and spaces on the canonical side, so multi-word
regions never matched. Single-word regions (Iowa, Gujarat) passed by
coincidence, masking the bug for most of USA.
"""
import unittest

import numpy as np
import pandas as pd

from geocif.ml.stats import get_yld_prd


def _amis_df():
    """Minimal AMIS-shaped frame with a mix of single- and multi-word
    admin1 names so we cover both the previously-working and previously-
    broken paths in one fixture.
    """
    return pd.DataFrame({
        "ADM0_NAME": [
            "India", "India", "India",
            "United States of America", "United States of America",
        ],
        "ADM1_NAME": [
            "Madhya Pradesh", "Uttar Pradesh", "Gujarat",
            "New Jersey", "Iowa",
        ],
        "ADM2_NAME": [np.nan] * 5,
        2020: [0.789, 0.5, 0.6, 3.094, 3.632],
        2021: [0.80, 0.55, 0.61, 3.10, 3.70],
    })


class TestGetYldPrdRegionNormalization(unittest.TestCase):
    """The Jun 2026 fix replaces underscores with spaces on both sides
    before the lowercase comparison."""

    def setUp(self):
        self.df = _amis_df()

    def test_multi_word_india_slug_matches_canonical(self):
        # Was the headline failure: every multi-word Indian state returned NaN.
        val = get_yld_prd(self.df, "soybean", "India", "madhya_pradesh", 2020)
        self.assertAlmostEqual(val, 0.789)

    def test_multi_word_usa_slug_matches_canonical(self):
        # Latent bug for USA — single-word states masked it.
        val = get_yld_prd(
            self.df, "soybean", "United States of America",
            "new_jersey", 2020,
        )
        self.assertAlmostEqual(val, 3.094)

    def test_canonical_name_still_matches(self):
        # Don't regress callers passing the AMIS-form name directly.
        val = get_yld_prd(self.df, "soybean", "India", "Madhya Pradesh", 2020)
        self.assertAlmostEqual(val, 0.789)

    def test_single_word_slug_still_matches(self):
        # Used to work by coincidence; must keep working after normalization.
        val = get_yld_prd(self.df, "soybean", "India", "gujarat", 2020)
        self.assertAlmostEqual(val, 0.6)

    def test_unknown_region_returns_nan(self):
        # No silent fallback — unknown region → NaN (not a wrong value).
        val = get_yld_prd(self.df, "soybean", "India", "atlantis", 2020)
        self.assertTrue(np.isnan(val))

    def test_india_synonym_orissa_resolves_to_odisha(self):
        # Boundary shapefile still uses pre-2011 "Orissa"; AMIS uses
        # "Odisha". Synonym map bridges the rename.
        df = pd.DataFrame({
            "ADM0_NAME": ["India"],
            "ADM1_NAME": ["Odisha"],
            "ADM2_NAME": [np.nan],
            2020: [2.877],
        })
        val = get_yld_prd(df, "maize", "India", "orissa", 2020)
        self.assertAlmostEqual(val, 2.877)

    def test_india_synonym_uttaranchal_resolves_to_uttarakhand(self):
        # pre-2007 boundary name → post-2007 AMIS name.
        df = pd.DataFrame({
            "ADM0_NAME": ["India"],
            "ADM1_NAME": ["Uttarakhand"],
            "ADM2_NAME": [np.nan],
            2020: [1.921],
        })
        val = get_yld_prd(df, "maize", "India", "uttaranchal", 2020)
        self.assertAlmostEqual(val, 1.921)

    def test_india_synonym_chhattisgarh_resolves_amis_typo(self):
        # AMIS uses 1-t "Chattisgarh"; shapefile has correct 2-h
        # "Chhattisgarh". Synonym bridges the spelling typo without
        # editing the AMIS file.
        df = pd.DataFrame({
            "ADM0_NAME": ["India"],
            "ADM1_NAME": ["Chattisgarh"],
            "ADM2_NAME": [np.nan],
            2020: [2.691],
        })
        val = get_yld_prd(df, "maize", "India", "chhattisgarh", 2020)
        self.assertAlmostEqual(val, 2.691)

    def test_india_synonym_bidirectional(self):
        # Synonyms apply to BOTH sides — if AMIS happened to use the
        # shapefile spelling, lookup with the shapefile slug must still
        # match. Both forms canonicalize to the same key.
        df = pd.DataFrame({
            "ADM0_NAME": ["India"],
            "ADM1_NAME": ["Orissa"],  # AMIS uses the OLD name
            "ADM2_NAME": [np.nan],
            2020: [2.877],
        })
        val = get_yld_prd(df, "maize", "India", "orissa", 2020)
        self.assertAlmostEqual(val, 2.877)

    def test_synonyms_do_not_leak_across_countries(self):
        # Country-keyed: an India synonym must not affect another
        # country's lookup even if the slug happens to match.
        df = pd.DataFrame({
            "ADM0_NAME": ["Brazil"],
            "ADM1_NAME": ["Orissa"],  # contrived
            "ADM2_NAME": [np.nan],
            2020: [9.99],
        })
        # India synonym maps orissa → odisha, but country is Brazil here.
        val = get_yld_prd(df, "maize", "Brazil", "orissa", 2020)
        self.assertAlmostEqual(val, 9.99)

    def test_trailing_period_abbreviation_matches(self):
        # AMIS uses period-suffixed abbreviations for Russian regions
        # ("Adygeya Rep.", "Bashkortostan Rep.") while the sweep slugifies
        # to "adygeya_rep" with no period. Lifted Russia maize match rate
        # from 33% to 49% in the Jun 2026 audit; before the period strip,
        # "adygeya rep." != "adygeya rep" → silent NaN.
        df = pd.DataFrame({
            "ADM0_NAME": ["Russian Federation"] * 2,
            "ADM1_NAME": ["Adygeya Rep.", "Krasnodarskiy Kray"],
            "ADM2_NAME": [np.nan, np.nan],
            2020: [5.2, 4.6],
        })
        val_adygeya = get_yld_prd(
            df, "maize", "Russian Federation", "adygeya_rep", 2020,
        )
        self.assertAlmostEqual(val_adygeya, 5.2)
        # Period-less region still works (no false positives).
        val_krasnodar = get_yld_prd(
            df, "maize", "Russian Federation", "krasnodarskiy_kray", 2020,
        )
        self.assertAlmostEqual(val_krasnodar, 4.6)


if __name__ == "__main__":
    unittest.main()
