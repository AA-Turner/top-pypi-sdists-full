import os
import sys
import tempfile
import unittest
import zipfile
from io import BytesIO
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import cpsl
from cpsl.image import Image
from cpsl.msg import Event
from cpsl.page_bundle import bundle_cache_control, bundle_cache_key, external_args, package_root
from cpsl.page_source import resolve_page_module, safe_component_path
from cpsl.utils import collect_source_archive, react_page_bundle_specs


class OnboardingTests(unittest.TestCase):
    def test_functional_app_serializes_react_onboarding_and_actions(self):
        app = cpsl.App(name="onboarding-react", image=Image(), npm_packages=["lucide-react"])

        @app.action("analyze_inbox")
        async def analyze_inbox(session, event):
            return None

        app.add_onboarding(component="pages/onboarding.tsx", packages=["confetti"])

        cfg = app._serialize()

        self.assertEqual(
            cfg["onboarding"],
            {
                "type": "react",
                "component": "pages/onboarding.tsx",
                "packages": ["lucide-react", "confetti"],
            },
        )
        self.assertEqual(cfg["npm_packages"], ["lucide-react"])
        self.assertEqual(cfg["actions"], ["analyze_inbox"])
        self.assertEqual(Event(name="x", payload={"a": 1}).payload["a"], 1)

    def test_functional_app_merges_global_npm_packages_into_pages(self):
        app = cpsl.App(name="npm-packages", image=Image(), npm_packages=["lucide-react"])
        app.add_npm_packages("date-fns")
        app.add_page("Tasks", component="pages/task.tsx", packages=["recharts", "lucide-react"])

        cfg = app._serialize()

        self.assertEqual(cfg["npm_packages"], ["lucide-react", "date-fns"])
        self.assertEqual(cfg["pages"][0]["packages"], ["lucide-react", "date-fns", "recharts"])

    def test_functional_app_serializes_dsl_onboarding(self):
        app = cpsl.App(name="onboarding-dsl", image=Image())

        @app.onboarding()
        def onboarding():
            return cpsl.ui.Page([cpsl.ui.Text("Welcome")])

        cfg = app._serialize()

        self.assertEqual(cfg["onboarding"]["type"], "dsl")
        self.assertEqual(cfg["onboarding"]["widget_tree"]["type"], "page")

    def test_onboarding_definitions_are_mutually_exclusive(self):
        app = cpsl.App(name="duplicate-onboarding", image=Image())
        app.add_onboarding(component="pages/onboarding.tsx")

        with self.assertRaisesRegex(ValueError, "only one onboarding surface"):
            app.add_onboarding(component="pages/other.tsx")

    def test_runner_resolves_page_modules_safely(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = os.getcwd()
            try:
                os.chdir(tmp)
                os.makedirs("pages/components")
                with open("pages/task.tsx", "w") as f:
                    f.write("export default function Task() { return null }")
                with open("pages/components/header.tsx", "w") as f:
                    f.write("export function Header() { return null }")
                with open("pages/components/index.tsx", "w") as f:
                    f.write("export const X = 1")
                with open("escape.tsx", "w") as f:
                    f.write("export const nope = 1")

                exact = resolve_page_module("pages/task.tsx", "components/header.tsx")
                extensionless = resolve_page_module("pages/task.tsx", "components/header")
                index = resolve_page_module("pages/task.tsx", "components")
                escaped = resolve_page_module("pages/task.tsx", "../escape")
            finally:
                os.chdir(cwd)

        self.assertTrue(exact and str(exact).endswith("pages/components/header.tsx"))
        self.assertTrue(
            extensionless and str(extensionless).endswith("pages/components/header.tsx")
        )
        self.assertTrue(index and str(index).endswith("pages/components/index.tsx"))
        self.assertIsNone(escaped)

    def test_safe_component_path_restricts_dynamic_ui_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = os.getcwd()
            try:
                os.chdir(tmp)
                os.makedirs("components")
                os.makedirs("node_modules/pkg")
                with open("components/panel.tsx", "w") as f:
                    f.write("export default function Panel() { return null }")
                with open("components/readme.md", "w") as f:
                    f.write("# no")
                with open("node_modules/pkg/panel.tsx", "w") as f:
                    f.write("export default function Panel() { return null }")

                valid = safe_component_path("components/panel.tsx")
                wrong_extension = safe_component_path("components/readme.md")
                ignored = safe_component_path("node_modules/pkg/panel.tsx")
                escaped = safe_component_path("../outside.tsx")
            finally:
                os.chdir(cwd)

        self.assertEqual(valid, "components/panel.tsx")
        self.assertIsNone(wrong_extension)
        self.assertIsNone(ignored)
        self.assertIsNone(escaped)

    def test_page_bundle_cache_key_tracks_sources_and_packages(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = os.getcwd()
            try:
                os.chdir(tmp)
                os.makedirs("pages/components")
                with open("pages/task.tsx", "w") as f:
                    f.write('import { Header } from "./components/header"; export default Header')
                with open("pages/components/header.tsx", "w") as f:
                    f.write("export function Header() { return null }")

                first = bundle_cache_key("pages/task.tsx", ["lucide-react"])
                package_changed = bundle_cache_key("pages/task.tsx", ["date-fns"])
                with open("pages/components/header.tsx", "w") as f:
                    f.write("export function Header() { return 'changed' }")
                source_changed = bundle_cache_key("pages/task.tsx", ["lucide-react"])
            finally:
                os.chdir(cwd)

        self.assertNotEqual(first, package_changed)
        self.assertNotEqual(first, source_changed)

    def test_page_bundle_cache_key_tracks_entry_component(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = os.getcwd()
            try:
                os.chdir(tmp)
                os.makedirs("pages")
                with open("pages/mailbox.tsx", "w") as f:
                    f.write("export default function Mailbox() { return null }")
                with open("pages/simulator.tsx", "w") as f:
                    f.write("export default function Simulator() { return null }")

                mailbox = bundle_cache_key("pages/mailbox.tsx", [])
                simulator = bundle_cache_key("pages/simulator.tsx", [])
            finally:
                os.chdir(cwd)

        self.assertNotEqual(mailbox, simulator)

    def test_page_bundle_external_args_include_package_roots(self):
        self.assertEqual(package_root("lucide-react@0.468.0"), "lucide-react")
        self.assertEqual(package_root("@scope/pkg@1.2.3"), "@scope/pkg")
        args = external_args(["lucide-react", "@scope/pkg@1.2.3"])
        self.assertIn("--external:react", args)
        self.assertIn("--external:@capsule/page", args)
        self.assertIn("--external:lucide-react", args)
        self.assertIn("--external:@scope/pkg", args)

    def test_page_bundle_cache_control_is_immutable_for_versions(self):
        self.assertEqual(bundle_cache_control(None), "no-cache")
        self.assertEqual(bundle_cache_control("latest"), "no-cache")
        self.assertEqual(bundle_cache_control("serve_123", "serve"), "no-cache")
        self.assertEqual(bundle_cache_control("ver_123"), "public, max-age=31536000, immutable")

    def test_archive_includes_only_page_bundle_cache_from_capsule_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = os.getcwd()
            try:
                os.chdir(tmp)
                os.makedirs(".capsule/cache/page-bundles")
                os.makedirs(".capsule/cache/bin")
                with open("app.py", "w") as f:
                    f.write("print('ok')")
                with open(".capsule/cache/page-bundles/abc123.js", "w") as f:
                    f.write("export default null")
                with open(".capsule/cache/bin/esbuild", "w") as f:
                    f.write("binary")

                archive = collect_source_archive([
                    Path(".capsule/cache/page-bundles/abc123.js"),
                ])
            finally:
                os.chdir(cwd)

        with zipfile.ZipFile(BytesIO(archive)) as zf:
            names = set(zf.namelist())

        self.assertIn("app.py", names)
        self.assertIn(".capsule/cache/page-bundles/abc123.js", names)
        self.assertNotIn(".capsule/cache/bin/esbuild", names)

    def test_react_page_bundle_specs_include_onboarding(self):
        specs = react_page_bundle_specs({
            "pages": [
                {
                    "name": "Tasks",
                    "type": "react",
                    "component": "pages/tasks.tsx",
                    "packages": ["x"],
                },
                {"name": "Home", "type": "dsl", "widget_tree": {}},
            ],
            "onboarding": {
                "type": "react",
                "component": "pages/onboarding.tsx",
                "packages": ["y"],
            },
        })

        self.assertEqual(specs, [
            ("Tasks", "pages/tasks.tsx", ["x"]),
            ("__onboarding__", "pages/onboarding.tsx", ["y"]),
        ])


if __name__ == "__main__":
    unittest.main()
