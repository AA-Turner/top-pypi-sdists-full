"""Maddog batch 5 — close ALL integration CRUD gaps (from the 11-integration audit).

The audit found one dominant systemic failure: "resolve container/id → act". Every
create needs a parent/list/team/workspace id; every update/delete needs an entity id
that only exists after a prior list/search or the just-run create. Plus two structural
risks: the schema cap could truncate write tools, and relevant_slugs disabled the
native path when no integration was named.

Locks in: op-rank priority ordering (write tools survive the cap), relevant_slugs
action-intent fallback, created-id carry-forward, and the per-integration required-arg
recipes in rule 7.
"""
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import nx_cli as N        # noqa: E402
import nx_mcp_tools as T  # noqa: E402


class OpRankAndCap(unittest.TestCase):
    def test_op_rank_buckets(self):
        self.assertEqual(T._op_rank("asana_list_workspaces"), 0)   # resolver
        self.assertEqual(T._op_rank("get_lists"), 0)
        self.assertEqual(T._op_rank("asana_create_task"), 1)       # mutator
        self.assertEqual(T._op_rank("clickup_delete_task"), 1)
        self.assertEqual(T._op_rank("export-design"), 1)
        self.assertEqual(T._op_rank("get_issue"), 2)               # plain read

    def test_cap_keeps_resolvers_and_mutators_not_reads(self):
        fs = {"asana": {"name": "Asana", "tools": [
            {"name": "get_a"}, {"name": "get_b"}, {"name": "get_c"},
            {"name": "asana_create_task"}, {"name": "asana_list_workspaces"}]}}
        with mock.patch.object(T, "gather_tools", lambda slugs=None, **k: fs):
            sch = T.tools_schema(max_tools=2)
        names = [f["function"]["name"] for f in sch]
        self.assertIn("asana__asana_list_workspaces", names)   # resolver survived
        self.assertIn("asana__asana_create_task", names)       # mutator survived
        self.assertNotIn("asana__get_a", names)                # plain read dropped first


class SlugFallback(unittest.TestCase):
    def test_named_scopes_intent_falls_back_chat_none(self):
        with mock.patch.object(T, "connected_slugs", lambda: ["asana", "linear"]), \
             mock.patch.object(T._oauth, "get_server", lambda s: {"name": s}):
            self.assertEqual(T.relevant_slugs("create a linear issue"), ["linear"])  # named → scoped
            self.assertEqual(sorted(T.relevant_slugs("create a new task for me")),
                             ["asana", "linear"])                                     # intent → all
            self.assertIsNone(T.relevant_slugs("how are you today"))                  # chat → none


class CreatedIdCarryForward(unittest.TestCase):
    def test_extract_entity_id(self):
        self.assertEqual(N._extract_entity_id('{"id":"NIC-5","title":"x"}'), "NIC-5")
        self.assertEqual(N._extract_entity_id('{"data":{"gid":"12345"}}'), "12345")
        self.assertEqual(N._extract_entity_id('{"result":{"public_id":"NX-PROOF"}}'), "NX-PROOF")
        self.assertIsNone(N._extract_entity_id("not json"))
        self.assertIsNone(N._extract_entity_id('{"nothing":"here"}'))


class Rule7Recipes(unittest.TestCase):
    def test_required_arg_recipes_present(self):
        fs = {"notion": {"name": "Notion", "tools": [{"name": "notion-create-pages"}]}}
        with mock.patch.object(T, "gather_tools", lambda slugs=None, **k: fs), \
             mock.patch.object(T, "connected_slugs", lambda: ["notion"]):
            tp = T.tools_prompt()
        self.assertIn("notion-search", tp)              # Notion parent recipe
        self.assertIn('assignee="me"', tp)              # Asana low-friction path
        self.assertIn("list_teams", tp)                 # Linear team resolution
        self.assertIn("REUSE IDS", tp)                  # carry-forward guidance
        self.assertIn("HARD DELETE", tp)                # destructive guard


if __name__ == "__main__":
    unittest.main()
