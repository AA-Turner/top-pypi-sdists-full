import json
import unittest

from contentstack_utils.utils import Utils


class TestVariantAliases(unittest.TestCase):

    def _sample_entry(self):
        return {
            "uid": "blt3e91e3812a44ba90",
            "_content_type_uid": "landing_page",
            "publish_details": {
                "variants": {
                    "cs669f1759b774fe1d": {
                        "alias": "cs_personalize_0_2",
                        "environment": "bltb5963e2163c24eb6",
                        "locale": "en",
                    },
                    "csbf165536748bdee2": {
                        "alias": "cs_personalize_0_1",
                        "environment": "bltb5963e2163c24eb6",
                        "locale": "en",
                    },
                }
            },
        }

    def test_single_entry_extracts_aliases(self):
        result = Utils.get_variant_aliases(self._sample_entry())
        self.assertEqual(result["entry_uid"], "blt3e91e3812a44ba90")
        self.assertEqual(result["contenttype_uid"], "landing_page")
        self.assertEqual(
            result["variants"],
            ["cs_personalize_0_2", "cs_personalize_0_1"],
        )

    def test_content_type_from_parameter_when_missing_on_entry(self):
        entry = {
            "uid": "blt1",
            "publish_details": {"variants": {}},
        }
        result = Utils.get_variant_aliases(entry, "landing_page")
        self.assertEqual(result["contenttype_uid"], "landing_page")

    def test_empty_contenttype_when_missing(self):
        entry = {"uid": "blt1", "publish_details": {"variants": {}}}
        result = Utils.get_variant_aliases(entry)
        self.assertEqual(result["contenttype_uid"], "")

    def test_missing_publish_details(self):
        entry = {"uid": "blt1", "_content_type_uid": "page"}
        result = Utils.get_variant_aliases(entry)
        self.assertEqual(result["variants"], [])

    def test_missing_variants_key(self):
        entry = {"uid": "blt1", "publish_details": {}}
        result = Utils.get_variant_aliases(entry)
        self.assertEqual(result["variants"], [])

    def test_empty_variants_object(self):
        entry = {"uid": "blt1", "publish_details": {"variants": {}}}
        result = Utils.get_variant_aliases(entry)
        self.assertEqual(result["variants"], [])

    def test_skips_variant_without_alias(self):
        entry = {
            "uid": "blt1",
            "publish_details": {
                "variants": {
                    "a": {"alias": "ok"},
                    "b": {},
                    "c": {"alias": ""},
                    "d": {"alias": "   "},
                }
            },
        }
        result = Utils.get_variant_aliases(entry)
        self.assertEqual(result["variants"], ["ok"])

    def test_non_dict_variant_value_skipped(self):
        entry = {
            "uid": "blt1",
            "publish_details": {"variants": {"x": "not-a-dict"}},
        }
        result = Utils.get_variant_aliases(entry)
        self.assertEqual(result["variants"], [])

    def test_none_entry_raises(self):
        with self.assertRaises(ValueError):
            Utils.get_variant_aliases(None)

    def test_missing_uid_raises(self):
        with self.assertRaises(ValueError):
            Utils.get_variant_aliases({"publish_details": {}})

    def test_empty_uid_raises(self):
        with self.assertRaises(ValueError):
            Utils.get_variant_aliases({"uid": ""})

    def test_whitespace_uid_raises(self):
        with self.assertRaises(ValueError):
            Utils.get_variant_aliases({"uid": "   "})

    def test_non_dict_entry_raises(self):
        with self.assertRaises(TypeError):
            Utils.get_variant_aliases("not-a-dict")

    def test_multiple_entries(self):
        results = Utils.get_variant_aliases(
            [
                {
                    "uid": "blt123",
                    "_content_type_uid": "page",
                    "publish_details": {
                        "variants": {
                            "v1": {"alias": "cs_personalize_3_1"},
                            "v2": {"alias": "cs_personalize_4_0"},
                        }
                    },
                },
                {"uid": "blt456", "_content_type_uid": "page"},
            ]
        )
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["entry_uid"], "blt123")
        self.assertEqual(
            results[0]["variants"],
            ["cs_personalize_3_1", "cs_personalize_4_0"],
        )
        self.assertEqual(results[1]["variants"], [])

    def test_list_entry_none_raises(self):
        with self.assertRaises(ValueError):
            Utils.get_variant_aliases([None])

    def test_get_variant_metadata_tags(self):
        entries = [
            {
                "uid": "blt123",
                "_content_type_uid": "page",
                "publish_details": {
                    "variants": {"v1": {"alias": "cs_personalize_3_1"}}
                },
            }
        ]
        tag = Utils.get_variant_metadata_tags(entries)
        self.assertIn("data-csvariants", tag)
        parsed = json.loads(tag["data-csvariants"])
        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0]["entry_uid"], "blt123")
        self.assertEqual(parsed[0]["variants"], ["cs_personalize_3_1"])

    def test_get_variant_metadata_tags_none_raises(self):
        with self.assertRaises(ValueError):
            Utils.get_variant_metadata_tags(None)

    def test_get_variant_metadata_tags_not_list_raises(self):
        with self.assertRaises(TypeError):
            Utils.get_variant_metadata_tags({})


if __name__ == "__main__":
    unittest.main()
