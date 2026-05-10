import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import cpsl
from cpsl.image import Image
from cpsl.msg import Event
from cpsl.page_bundle import bundle_cache_key, external_args, package_root
from cpsl.page_source import resolve_page_module


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

    def test_page_bundle_external_args_include_package_roots(self):
        self.assertEqual(package_root("lucide-react@0.468.0"), "lucide-react")
        self.assertEqual(package_root("@scope/pkg@1.2.3"), "@scope/pkg")
        args = external_args(["lucide-react", "@scope/pkg@1.2.3"])
        self.assertIn("--external:react", args)
        self.assertIn("--external:@capsule/page", args)
        self.assertIn("--external:lucide-react", args)
        self.assertIn("--external:@scope/pkg", args)


if __name__ == "__main__":
    unittest.main()
