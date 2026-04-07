import unittest

from contentstack_utils.utils import Utils


class TestEditableTags(unittest.TestCase):
    def test_add_tags_mutates_entry_with_dollar_map(self):
        entry = {"uid": "e1", "title": "Hello", "count": 1}
        Utils.addTags(entry, "Blog_Post", tags_as_object=True, locale="EN-us")
        self.assertIn("$", entry)
        self.assertEqual(entry["$"]["title"], {"data-cslp": "blog_post.e1.en-us.title"})
        self.assertEqual(entry["$"]["count"], {"data-cslp": "blog_post.e1.en-us.count"})

    def test_add_tags_string_mode(self):
        entry = {"uid": "e1", "title": "Hello"}
        Utils.addTags(entry, "blog_post", tags_as_object=False, locale="en-us")
        self.assertEqual(entry["$"]["title"], "data-cslp=blog_post.e1.en-us.title")

    def test_array_tags_add_index_and_parent_keys(self):
        entry = {"uid": "e1", "array": ["hello", "world"]}
        Utils.addTags(entry, "blog", tags_as_object=True, locale="en-us")
        self.assertEqual(entry["$"]["array"], {"data-cslp": "blog.e1.en-us.array"})
        self.assertEqual(entry["$"]["array__0"], {"data-cslp": "blog.e1.en-us.array.0"})
        self.assertEqual(entry["$"]["array__1"], {"data-cslp": "blog.e1.en-us.array.1"})
        self.assertEqual(entry["$"]["array__parent"], {"data-cslp-parent-field": "blog.e1.en-us.array"})

    def test_reference_entry_inside_array_gets_own_dollar(self):
        entry = {
            "uid": "e1",
            "refs": [
                {
                    "uid": "r1",
                    "_content_type_uid": "ref_ct",
                    "title": "Ref Title",
                }
            ],
        }
        Utils.addTags(entry, "blog", tags_as_object=True, locale="en-us")
        ref = entry["refs"][0]
        self.assertIn("$", ref)
        self.assertEqual(ref["$"]["title"], {"data-cslp": "ref_ct.r1.en-us.title"})

    def test_variantised_field_applies_v2_prefix_and_uid_suffix(self):
        entry = {
            "uid": "e1",
            "_applied_variants": {"title": "v123"},
            "title": {"value": "Hello"},
        }
        Utils.addTags(entry, "blog", tags_as_object=True, locale="en-us")
        # title is an object; ensure we tag the object itself (like JS) and apply variant.
        self.assertEqual(entry["$"]["title"], {"data-cslp": "v2:blog.e1_v123.en-us.title"})


if __name__ == "__main__":
    unittest.main()

