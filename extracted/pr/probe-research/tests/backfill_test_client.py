"""Authenticated metadata-only client for review and planning tests.

Delivery/recovery tests use the real SDK harness in
test_backfill_scoped_orchestration instead of inventing delivery receipts.
"""

from types import SimpleNamespace
from uuid import NAMESPACE_URL, uuid5


class ScopedClient:
    def __init__(self):
        self.settings = SimpleNamespace(base_url="https://backfill.test", workspace="workspace")
        self.projects = {}

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def me(self):
        return {"customer_id": "tenant", "user_id": "user"}

    def get_workspace(self, ident):
        return {"id": ident, "customer_id": "tenant", "kind": "personal", "owner_user_id": "user"}

    def project_row(self, slug, **values):
        row = {
            "id": str(uuid5(NAMESPACE_URL, "backfill-test/" + slug)),
            "slug": slug, "customer_id": "tenant", "workspace_id": "workspace", **values,
        }
        self.projects[row["id"]] = row
        return row

    def list_projects(self, **kwargs):
        return list(self.projects.values())

    def resolve_project(self, slug, **kwargs):
        return next((row for row in self.projects.values() if row["slug"] == slug), None)

    def get_project(self, ident):
        return self.projects[ident]

    def create_project(self, slug, name=None, **kwargs):
        return self.project_row(slug, name=name or slug)

    def list_project_code_sources(self, project_id):
        return []

    def delivery_receipt(self, correlation):
        return None

    def delivery_state(self, correlation):
        return {"state": "unknown"}
