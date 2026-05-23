from tests.fixtures import BaseTest


class TestPlayerApi(BaseTest):
    def test_version(self):
        res = self.get_cloud_flask_client().get("/_version")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.text, "dev")

    def test_get_page_by_path(self):
        page = self.controller.create_stage(
            "page",
            title="My Page",
            file="page_test.py",
        )
        self.controller.update_stage(page.id, {"path": "my-page"})

        client = self.get_cloud_flask_client()
        res = client.get("/_pages/my-page")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("page", data)
        self.assertEqual(data["page"]["id"], page.id)
        self.assertEqual(data["page"]["path"], "my-page")
        self.assertEqual(data["page"]["title"], "My Page")

    def test_get_page_empty_path(self):
        page = self.controller.create_stage(
            "page",
            title="Homepage Page",
            file="page_home.py",
        )
        self.controller.update_stage(page.id, {"path": ""})

        client = self.get_cloud_flask_client()
        res = client.get("/_pages-home")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("page", data)
        self.assertEqual(data["page"]["id"], page.id)
        self.assertEqual(data["page"]["path"], "")

    def test_get_form_by_path_still_works(self):
        form = self.controller.create_stage(
            "form",
            title="My Form",
            file="form_test.py",
        )
        self.controller.update_stage(form.id, {"path": "my-form"})

        client = self.get_cloud_flask_client()
        res = client.get("/_pages/my-form")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("form", data)

    def test_page_not_found(self):
        client = self.get_cloud_flask_client()
        res = client.get("/_pages/nonexistent")
        # Guard returns 401 when path is not in secured_stages
        self.assertEqual(res.status_code, 401)

    def test_workspace_includes_pages_in_sidebar(self):
        page = self.controller.create_stage(
            "page",
            title="Dashboard",
            file="page_dashboard.py",
        )
        self.controller.update_stage(page.id, {"path": "dashboard"})

        client = self.get_cloud_flask_client()
        res = client.get("/_workspace")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        sidebar = data.get("sidebar", [])
        page_items = [item for item in sidebar if item.get("type") == "page"]
        self.assertTrue(len(page_items) > 0, "Pages should appear in sidebar")
        self.assertEqual(page_items[0]["id"], page.id)
        self.assertEqual(page_items[0]["path"], "dashboard")
