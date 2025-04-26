from unittest import TestCase

from tecton._internals.display import Displayable
from tecton_proto.data.summary__client_pb2 import FcoSummary
from tecton_proto.data.summary__client_pb2 import SummaryItem


class DisplayTest(TestCase):
    def test_fco_metadata(self):
        summary_pb = FcoSummary()
        summary_pb.fco_metadata.name = "my_ds"
        summary_pb.fco_metadata.workspace = "dev"
        summary_pb.fco_metadata.created_at.seconds = 1657932800
        summary_pb.fco_metadata.description = "develop"
        summary_pb.fco_metadata.owner = "joe@pizza.com"
        summary_pb.fco_metadata.tags["a"] = "b"
        summary_pb.fco_metadata.source_filename = "foo.py"

        actual = Displayable.from_fco_summary(summary_pb).to_dict()
        expected = {
            "Name": "my_ds",
            "Created At": "2022-07-16 00:53:20 UTC",
            "Workspace": "dev",
            "Description": "develop",
            "Owner": "joe@pizza.com",
            "Tags": {"a": "b"},
            "Last Modified By": "",  # FCO metadata defaults to "" if not specified
            "Source Filename": "foo.py",
        }
        self.assertDictEqual(actual, expected)

    def test_fco_summary(self):
        summary_pb = FcoSummary()

        item = SummaryItem()
        item.display_name = "Some Property"
        item.value = "Some Value"
        summary_pb.summary_items.append(item)

        multi_item = SummaryItem()
        multi_item.display_name = "Some List"
        multi_item.multi_values.extend(["A", "B"])
        summary_pb.summary_items.append(multi_item)

        nested = SummaryItem()
        nested.display_name = "Some Nested Item"
        nested_item1 = SummaryItem()
        nested_item1.display_name = "Some Attribute"
        nested_item1.value = "Value!"
        nested_item2 = SummaryItem()
        nested_item2.display_name = "Some List Attr"
        nested_item2.multi_values.extend(["C", "D"])
        nested_item3 = SummaryItem()
        nested_item3.display_name = "Some Double Nested"
        nested_item3.nested_summary_items.append(nested_item1)
        nested.nested_summary_items.extend([nested_item1, nested_item2, nested_item3])
        summary_pb.summary_items.append(nested)

        actual = Displayable.from_fco_summary(summary_pb).to_dict()
        expected_subset = {
            "Some Property": "Some Value",
            "Some List": ["A", "B"],
            "Some Nested Item": {
                "Some Attribute": "Value!",
                "Some List Attr": ["C", "D"],
                "Some Double Nested": {"Some Attribute": "Value!"},
            },
        }
        self.assertDictContainsSubset(expected_subset, actual)

    def test_display_table(self):
        headings = ["A", "B", "C"]
        rows = [("a1", "b1", "c1"), ("a2", "b2", "c2")]
        actual = Displayable.from_table(headings=headings, rows=rows).to_dict()
        expected = {
            "data": [
                {"A": "a1", "B": "b1", "C": "c1"},
                {"A": "a2", "B": "b2", "C": "c2"},
            ]
        }
        self.assertDictEqual(actual, expected)

        items = [("a1", "b1"), ("a2", "b2")]
        actual = Displayable.from_table(headings=["A", "B"], rows=items).to_dict()
        expected = {
            "data": [
                {
                    "A": "a1",
                    "B": "b1",
                },
                {
                    "A": "a2",
                    "B": "b2",
                },
            ]
        }
        self.assertDictEqual(actual, expected)

    def test_display_properties(self):
        items = [("a1", "b1"), ("a2", "b2")]
        actual = Displayable.from_properties(items=items).to_dict()
        expected = {"a1": "b1", "a2": "b2"}
        self.assertDictEqual(actual, expected)
