import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import cpsl
from cpsl.image import Image
from cpsl.msg import Event


class OnboardingTests(unittest.TestCase):
    def test_functional_app_serializes_react_onboarding_and_actions(self):
        app = cpsl.App(name="onboarding-react", image=Image())

        @app.action("analyze_inbox")
        async def analyze_inbox(session, event):
            return None

        app.add_onboarding(component="pages/onboarding.tsx", packages=["confetti"])

        cfg = app._serialize()

        self.assertEqual(
            cfg["onboarding"],
            {"type": "react", "component": "pages/onboarding.tsx", "packages": ["confetti"]},
        )
        self.assertEqual(cfg["actions"], ["analyze_inbox"])
        self.assertEqual(Event(name="x", payload={"a": 1}).payload["a"], 1)

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


if __name__ == "__main__":
    unittest.main()
