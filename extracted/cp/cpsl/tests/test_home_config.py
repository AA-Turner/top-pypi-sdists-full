import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import cpsl


class HomeConfigTests(unittest.TestCase):
    def test_home_config_serializes_static_dynamic_and_body(self):
        app = cpsl.App(name="home-test", image=cpsl.Image(), channels=[cpsl.Chat()])
        app.home(
            title="Research loop",
            subtitle="Run the next best action.",
            suggestions=[
                cpsl.Suggestion("Research Beam", prompt="Research Beam Cloud", icon="search"),
                cpsl.Suggestion(
                    "Open Results", page="Results", description="Review recent outputs"
                ),
            ],
        )

        @app.home_body()
        def home_body():
            return cpsl.ui.Page(
                [
                    cpsl.ui.ImageGallery(
                        [
                            {"src": "https://example.com/a.png", "alt": "Example A"},
                            "https://example.com/b.png",
                        ]
                    ),
                    cpsl.ui.ActionCard(
                        "Run scan",
                        workflow="Weekly Scan",
                        image="https://example.com/scan.png",
                        primary=True,
                    ),
                ]
            )

        @app.home_suggestions(ttl=300)
        async def suggestions(ctx: cpsl.HomeContext):
            return [cpsl.Suggestion("Resume Acme", prompt="Resume Acme research")]

        home = app._serialize()["home"]

        self.assertEqual(home["title"], "Research loop")
        self.assertEqual(home["subtitle"], "Run the next best action.")
        self.assertTrue(home["dynamic_suggestions"])
        self.assertEqual(home["dynamic_suggestions_access"], "public")
        self.assertEqual(home["dynamic_suggestions_ttl"], 300)
        self.assertEqual(home["suggestions"][0]["target"], "prompt")
        self.assertEqual(home["suggestions"][1]["target"], "page")
        self.assertEqual(home["widget_tree"]["children"][0]["type"], "image_gallery")
        self.assertEqual(home["widget_tree"]["children"][1]["type"], "action_card")

    def test_action_suggestion_allows_payload(self):
        suggestion = cpsl.Suggestion(
            "Approve",
            action="approve_company",
            payload={"company_id": "co_123"},
            icon="check",
            primary=True,
        )

        self.assertEqual(
            suggestion.to_dict(),
            {
                "label": "Approve",
                "target": "action",
                "value": "approve_company",
                "icon": "check",
                "primary": True,
                "payload": {"company_id": "co_123"},
            },
        )

    def test_suggestion_requires_exactly_one_target(self):
        with self.assertRaises(ValueError):
            cpsl.Suggestion("Bad", prompt="hello", page="Home")

        with self.assertRaises(ValueError):
            cpsl.Suggestion("Bad")

        with self.assertRaises(ValueError):
            cpsl.Suggestion("Bad", prompt="hello", payload={"unused": True})

    def test_workflow_suggestion_and_action_card_allow_payload(self):
        app = cpsl.App(name="workflow-link-test", image=cpsl.Image())
        workflow = app.workflow("Find Leads")

        suggestion = cpsl.Suggestion(
            "Run example",
            workflow=workflow,
            input={"company_url": "beam.cloud"},
        )
        self.assertEqual(suggestion.to_dict()["target"], "workflow")
        self.assertEqual(suggestion.to_dict()["value"], "Find Leads")
        self.assertEqual(suggestion.to_dict()["payload"], {"company_url": "beam.cloud"})

        card = cpsl.ui.ActionCard(
            "Run example",
            workflow=workflow,
            input={"company_url": "beam.cloud"},
        )
        self.assertEqual(card.to_dict()["value"], "Find Leads")
        self.assertEqual(card.to_dict()["payload"], {"company_url": "beam.cloud"})

        image = cpsl.ui.Image(
            "https://example.com/run.png",
            workflow=workflow,
            input={"company_url": "beam.cloud"},
            caption="Run example",
        )
        self.assertEqual(image.to_dict()["value"], "Find Leads")
        self.assertEqual(image.to_dict()["payload"], {"company_url": "beam.cloud"})

        with self.assertRaises(ValueError):
            cpsl.ui.ActionCard("Bad", prompt="hello", payload={"unused": True})

        with self.assertRaises(ValueError):
            cpsl.Suggestion("Bad", workflow=workflow, input={"a": 1}, payload={"b": 2})


if __name__ == "__main__":
    unittest.main()
