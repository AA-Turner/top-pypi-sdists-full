import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import cpsl
from cpsl.app import _REGISTERED_CLASSES
from cpsl.constants import CollectionDecl, Column
from cpsl.runner.routes import RunnerRouteMixin


class _MetaCollector(RunnerRouteMixin):
    def __init__(self, collections: list[CollectionDecl]) -> None:
        self._instance = None
        self._action_handlers = {}
        self._hooks = {}
        self._message_handler_labels = {}
        self._collections = {decl.name: decl for decl in collections}

    def _get_all_collections(self):
        return self._collections

    def _get_all_settings(self):
        return {}


class TableBrowserTests(unittest.TestCase):
    def test_table_browser_serializes_existing_tables(self):
        browser = cpsl.ui.TableBrowser(
            title="Tables",
            items=[
                cpsl.ui.TableGroup(
                    "CRM",
                    [
                        cpsl.ui.Table("crm_customers", label="Customers"),
                        cpsl.ui.Table("crm_accounts"),
                    ],
                ),
                cpsl.ui.Table("crimson_sirius"),
            ],
        )

        self.assertEqual(
            browser.to_dict(),
            {
                "type": "table_browser",
                "title": "Tables",
                "items": [
                    {
                        "type": "table_group",
                        "label": "CRM",
                        "items": [
                            {
                                "type": "table",
                                "label": "Customers",
                                "collection_ref": "crm_customers",
                            },
                            {"type": "table", "collection_ref": "crm_accounts"},
                        ],
                    },
                    {"type": "table", "collection_ref": "crimson_sirius"},
                ],
            },
        )

    def test_table_browser_requires_collection_backed_tables(self):
        with self.assertRaisesRegex(ValueError, "collection-backed"):
            cpsl.ui.TableBrowser(items=[cpsl.ui.Table(rows=[{"name": "Ada"}])])

    def test_collection_table_editing_flags_serialize(self):
        table = cpsl.ui.Table("crm_customers", editable=True, reorderable=True)

        self.assertEqual(
            table.to_dict(),
            {
                "type": "table",
                "collection": "crm_customers",
                "editable": True,
                "reorderable": True,
            },
        )

    def test_table_browser_leaves_inherit_collection_metadata(self):
        decl = CollectionDecl(
            name="crm_customers",
            scope="owner",
            columns=(Column("name"), Column("email", type="email")),
            sortable=True,
            filterable=True,
            paginate=25,
        )
        tree = cpsl.ui.Page(
            [
                cpsl.ui.TableBrowser(
                    items=[
                        cpsl.ui.TableGroup(
                            "CRM",
                            [cpsl.ui.Table("crm_customers", label="Customers")],
                        )
                    ]
                )
            ]
        ).to_dict()
        reg = {
            "pages": [{"name": "Tables Metadata Test", "type": "dsl", "widget_tree": tree}],
            "collections": [decl.to_dict()],
        }
        _REGISTERED_CLASSES.append(reg)
        try:
            meta = _MetaCollector([decl])._collect_meta()
        finally:
            _REGISTERED_CLASSES.remove(reg)

        page = next(p for p in meta["pages"] if p["name"] == "Tables Metadata Test")
        leaf = page["widget_tree"]["children"][0]["items"][0]["items"][0]
        self.assertEqual(leaf["collection"], "crm_customers")
        self.assertEqual(leaf["label"], "Customers")
        self.assertEqual(leaf["scope"], "owner")
        self.assertEqual(leaf["columns"][0], {"key": "name", "type": "text"})
        self.assertEqual(leaf["columns"][1], {"key": "email", "type": "email"})
        self.assertTrue(leaf["sortable"])
        self.assertTrue(leaf["filterable"])
        self.assertEqual(leaf["paginate"], 25)


if __name__ == "__main__":
    unittest.main()
