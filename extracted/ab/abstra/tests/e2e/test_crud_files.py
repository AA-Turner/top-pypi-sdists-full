from tests.fixtures import BaseTest


class TestCRUDFiles(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.client = self.get_editor_flask_client()

    def test_api_update(self):
        self.client.put(
            "/_editor/api/workspace",
            json={"name": "test-workspace-updated", "brand_name": "test-brand-name"},
        )
        workspace = self.client.get("/_editor/api/workspace").get_json()
        self.assertEqual(workspace["name"], "test-workspace-updated")
        self.assertEqual(workspace["brand_name"], "test-brand-name")

    def test_list_files(self):
        res = self.client.get("/_editor/api/codebase/files")
        self.assertEqual(res.status_code, 200)

        files = res.json or []
        self.assertGreater(len(files), 0)

        # Each item should have file and stages keys
        for item in files:
            self.assertIn("file", item)
            self.assertIn("stages", item)
            self.assertIn("pathParts", item["file"])
            self.assertIn("type", item["file"])

        file_names = [f["file"]["pathParts"][-1] for f in files]
        self.assertIn("abstra.json", file_names)

    def test_list_files_with_subdir(self):
        (self.root / "subdir").mkdir()
        (self.root / "subdir" / "test.txt").touch()

        res = self.client.get("/_editor/api/codebase/files?path=subdir")
        self.assertEqual(res.status_code, 200)

        files = res.json or []
        file_items = [f for f in files if f["file"]["type"] == "file"]
        self.assertEqual(len(file_items), 1)
        self.assertEqual(file_items[0]["file"]["pathParts"][-1], "test.txt")

    def test_shallow_module_mode(self):
        (self.root / "subdir").mkdir()
        (self.root / "subdir" / "__init__.py").touch()
        (self.root / "subdir" / "test.py").touch()

        res = self.client.get("/_editor/api/codebase/files?mode=module")
        if res.json is None:
            raise Exception("No json response")

        names = [f["file"]["pathParts"][-1] for f in res.json]
        types = [f["file"]["type"] for f in res.json]
        self.assertIn("subdir", names)
        idx = names.index("subdir")
        self.assertEqual(types[idx], "package")

    def test_nested_module_mode(self):
        (self.root / "subdir").mkdir()
        (self.root / "subdir" / "__init__.py").touch()
        (self.root / "subdir" / "test.py").touch()

        res = self.client.get("/_editor/api/codebase/files?mode=module&path=subdir")
        if res.json is None:
            raise Exception("No json response")

        names = [f["file"]["pathParts"][-1] for f in res.json]
        types = [f["file"]["type"] for f in res.json]
        self.assertIn("test", names)
        idx = names.index("test")
        self.assertEqual(types[idx], "module")

    def test_always_hidden_dirs_are_not_listed(self):
        always_hidden = [".git", ".venv", "venv", "__pycache__"]
        for name in always_hidden:
            (self.root / name).mkdir()
            (self.root / name / "file.txt").touch()

        res = self.client.get("/_editor/api/codebase/files")
        self.assertEqual(res.status_code, 200)

        names = [f["file"]["pathParts"][-1] for f in res.json or []]
        for name in always_hidden:
            self.assertNotIn(
                name, names, f"{name} should be hidden but appeared in response"
            )

    def test_dotenv_and_dotabstra_are_visible(self):
        (self.root / ".env").write_text("SECRET=123")
        (self.root / ".abstra").mkdir(exist_ok=True)

        res = self.client.get("/_editor/api/codebase/files")
        self.assertEqual(res.status_code, 200)

        names = [f["file"]["pathParts"][-1] for f in res.json or []]
        self.assertIn(".env", names, ".env should be visible")
        self.assertIn(".abstra", names, ".abstra should be visible")
