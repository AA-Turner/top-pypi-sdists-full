import os
import sys
import unittest
from types import SimpleNamespace

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from cpsl.constants import CollectionDecl
from cpsl.db import CollectionRef, reset_active_identity, set_active_identity
from cpsl.session import UserInfo


class ScopedIdentityTests(unittest.TestCase):
    def test_user_info_owner_id_prefixes_orgs(self):
        user = UserInfo(id="user_hash", org_id="org_123")

        self.assertEqual(user.owner_id, "org:org_123")
        self.assertEqual(UserInfo.org_id_from_owner_id("org:org_123"), "org_123")
        self.assertIsNone(UserInfo.org_id_from_owner_id("user_hash"))

    def test_collection_ref_uses_context_local_identity(self):
        ref = CollectionRef("property_listings", CollectionDecl(name="property_listings", scope="owner"))
        ref._bound = object()

        token = set_active_identity(
            SimpleNamespace(id="", user=UserInfo(id="user_hash", org_id="org_123"))
        )
        try:
            resolved = ref._resolve()
        finally:
            reset_active_identity(token)

        self.assertEqual(resolved._scope_filter, {"_team_id": "org:org_123"})


if __name__ == "__main__":
    unittest.main()
