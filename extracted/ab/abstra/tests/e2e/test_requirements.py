from pathlib import Path

from tests.fixtures import BaseTest


class TestRequirementsApi(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.client = self.get_editor_flask_client()

    def test_initial_requirements(self):
        requirements = self.client.get("/_editor/api/requirements").get_json()
        self.assertEqual(len(requirements), 1)
        self.assertEqual(requirements[0]["name"], "abstra")

    def test_existing_requirements(self):
        Path("requirements.txt").write_text(
            "foo==1.0.0\nbar\n\n# baz", encoding="utf-8"
        )
        requirements = self.client.get("/_editor/api/requirements").get_json()
        self.assertEqual(
            requirements,
            [
                {
                    "name": "foo",
                    "specifiers": [{"operator": "==", "version": "1.0.0"}],
                    "extras": [],
                    "marker": None,
                    "url": None,
                    "raw_requirement": "foo==1.0.0",
                    "installed_version": None,
                },
                {
                    "name": "bar",
                    "specifiers": [],
                    "extras": [],
                    "marker": None,
                    "url": None,
                    "raw_requirement": "bar",
                    "installed_version": None,
                },
            ],
        )

    def test_post_requirement(self):
        self.client.post("/_editor/api/requirements", json={"name": "foo"})
        requirements = self.client.get("/_editor/api/requirements").get_json()
        self.assertEqual(len(requirements), 2)
        non_abstra_requirements = [
            requirement
            for requirement in requirements
            if requirement["name"] != "abstra"
        ]
        self.assertEqual(
            non_abstra_requirements,
            [
                {
                    "name": "foo",
                    "specifiers": [],
                    "extras": [],
                    "marker": None,
                    "url": None,
                    "raw_requirement": "foo",
                    "installed_version": None,
                }
            ],
        )

        self.assertTrue(Path("requirements.txt").exists())

    def test_delete_requirement(self):
        Path("requirements.txt").write_text(
            "foo==1.0.0\nbar\n\n# baz", encoding="utf-8"
        )
        self.client.delete("/_editor/api/requirements/foo")
        requirements = self.client.get("/_editor/api/requirements").get_json()
        self.assertEqual(
            requirements,
            [
                {
                    "name": "bar",
                    "specifiers": [],
                    "extras": [],
                    "marker": None,
                    "url": None,
                    "raw_requirement": "bar",
                    "installed_version": None,
                }
            ],
        )
        self.assertTrue(Path("requirements.txt").exists())
        self.assertEqual(Path("requirements.txt").read_text(encoding="utf-8"), "bar")

    def test_remove_fixed_version_single(self):
        Path("requirements.txt").write_text(
            "abstra==1.2.3\nfoo==1.0.0\nbar>=2.0\nbaz==3.0",
            encoding="utf-8",
        )
        response = self.client.post("/_editor/api/requirements/foo/remove-version")
        self.assertEqual(response.status_code, 200)

        requirements = self.client.get("/_editor/api/requirements").get_json()
        by_name = {r["name"]: r for r in requirements}

        self.assertEqual(by_name["foo"]["specifiers"], [])
        self.assertEqual(by_name["foo"]["raw_requirement"], "foo")
        self.assertEqual(
            by_name["bar"]["specifiers"], [{"operator": ">=", "version": "2.0"}]
        )
        self.assertEqual(
            by_name["baz"]["specifiers"], [{"operator": "==", "version": "3.0"}]
        )
        self.assertEqual(
            by_name["abstra"]["specifiers"],
            [{"operator": "==", "version": "1.2.3"}],
        )

        order = [r["name"] for r in requirements]
        self.assertEqual(order, ["abstra", "foo", "bar", "baz"])

    def test_remove_all_fixed_versions_skips_abstra(self):
        Path("requirements.txt").write_text(
            "abstra==1.2.3\nfoo==1.0.0\nbar>=2.0\nbaz==3.0",
            encoding="utf-8",
        )
        response = self.client.post("/_editor/api/requirements/remove-fixed-versions")
        self.assertEqual(response.status_code, 200)

        requirements = self.client.get("/_editor/api/requirements").get_json()
        by_name = {r["name"]: r for r in requirements}

        self.assertEqual(
            by_name["abstra"]["specifiers"],
            [{"operator": "==", "version": "1.2.3"}],
        )
        self.assertEqual(by_name["foo"]["specifiers"], [])
        self.assertEqual(by_name["baz"]["specifiers"], [])
        self.assertEqual(
            by_name["bar"]["specifiers"], [{"operator": ">=", "version": "2.0"}]
        )

        order = [r["name"] for r in requirements]
        self.assertEqual(order, ["abstra", "foo", "bar", "baz"])

    def test_remove_fixed_version_ignores_abstra(self):
        Path("requirements.txt").write_text(
            "abstra==1.2.3\nfoo==1.0.0",
            encoding="utf-8",
        )

        for name in ("abstra", "Abstra", "ABSTRA"):
            response = self.client.post(
                f"/_editor/api/requirements/{name}/remove-version"
            )
            self.assertEqual(response.status_code, 200)

        requirements = self.client.get("/_editor/api/requirements").get_json()
        by_name = {r["name"]: r for r in requirements}
        self.assertEqual(
            by_name["abstra"]["specifiers"],
            [{"operator": "==", "version": "1.2.3"}],
        )
        # Other requirements remain untouched too.
        self.assertEqual(
            by_name["foo"]["specifiers"], [{"operator": "==", "version": "1.0.0"}]
        )

    def test_remove_fixed_versions_leaves_url_requirements_untouched(self):
        # URL-based requirements use the `@ url` syntax and can't have
        # an == specifier, so they must be left untouched by both endpoints.
        Path("requirements.txt").write_text(
            "abstra==1.2.3\n"
            "foo==1.0.0\n"
            "mypkg @ https://example.com/mypkg.zip\n"
            "git-client @ git+https://github.com/user/git-client.git\n",
            encoding="utf-8",
        )

        # Calling the single endpoint by name on a URL requirement is a no-op.
        response = self.client.post("/_editor/api/requirements/mypkg/remove-version")
        self.assertEqual(response.status_code, 200)

        # And the bulk endpoint must not touch URL requirements either.
        response = self.client.post("/_editor/api/requirements/remove-fixed-versions")
        self.assertEqual(response.status_code, 200)

        requirements = self.client.get("/_editor/api/requirements").get_json()
        by_name = {r["name"]: r for r in requirements}

        self.assertEqual(by_name["mypkg"]["url"], "https://example.com/mypkg.zip")
        self.assertEqual(by_name["mypkg"]["specifiers"], [])
        self.assertEqual(
            by_name["mypkg"]["raw_requirement"],
            "mypkg @ https://example.com/mypkg.zip",
        )

        self.assertEqual(
            by_name["git-client"]["url"],
            "git+https://github.com/user/git-client.git",
        )
        self.assertEqual(by_name["git-client"]["specifiers"], [])

        # Sanity-check that the bulk operation did its normal job on the
        # other requirements.
        self.assertEqual(by_name["foo"]["specifiers"], [])
        self.assertEqual(
            by_name["abstra"]["specifiers"],
            [{"operator": "==", "version": "1.2.3"}],
        )

        # Order is preserved.
        order = [r["name"] for r in requirements]
        self.assertEqual(order, ["abstra", "foo", "mypkg", "git-client"])

    def test_remove_fixed_version_preserves_extras_and_markers(self):
        Path("requirements.txt").write_text(
            'pandas[excel]==1.5.0; python_version >= "3.7"\n',
            encoding="utf-8",
        )
        response = self.client.post("/_editor/api/requirements/pandas/remove-version")
        self.assertEqual(response.status_code, 200)

        requirements = self.client.get("/_editor/api/requirements").get_json()
        self.assertEqual(len(requirements), 1)
        pandas_req = requirements[0]
        self.assertEqual(pandas_req["name"], "pandas")
        self.assertEqual(pandas_req["specifiers"], [])
        self.assertEqual(pandas_req["extras"], ["excel"])
        self.assertIn("python_version", pandas_req["marker"] or "")

    def test_get_requirements_recommendation(self):
        recommendation = self.client.get(
            "/_editor/api/requirements/recommendations"
        ).get_json()
        self.assertEqual(recommendation, [])

        script = self.controller.create_stage("tasklet", "New script", "script.py")

        Path(script.file_path).write_text("import pandas as pd", encoding="utf-8")

        recommendation = self.client.get(
            "/_editor/api/requirements/recommendations"
        ).get_json()
        self.assertEqual(recommendation[0]["name"], "pandas")

    def test_get_requirements_recommendation_already_met(self):
        Path("requirements.txt").write_text("Pillow", encoding="utf-8")
        script = self.controller.create_stage("tasklet", "New script", "script.py")
        Path(script.file_path).write_text(
            "import pandas as pd\nfrom PIL import Image", encoding="utf-8"
        )

        recommendation = self.client.get(
            "/_editor/api/requirements/recommendations"
        ).get_json()

        self.assertEqual(len(recommendation), 1)
        self.assertEqual(recommendation[0]["name"], "pandas")
