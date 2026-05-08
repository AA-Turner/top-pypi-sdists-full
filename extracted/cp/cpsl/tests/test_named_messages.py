import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import cpsl
from cpsl.image import Image


class NamedMessageTests(unittest.TestCase):
    def test_functional_app_serializes_named_message_handlers(self):
        app = cpsl.App(name="named-chat", image=Image())

        @app.message()
        async def default_chat(session, msg):
            return None

        @app.message("acquisition", label="Acquisition")
        async def acquisition(session, msg):
            return None

        cfg = app._serialize()

        self.assertTrue(cfg["has_message_handler"])
        self.assertEqual(cfg["message_handlers"], [{"name": "acquisition", "label": "Acquisition"}])

    def test_class_app_serializes_named_message_handlers(self):
        app = cpsl.App(name="named-class-chat")

        @app.cls(image=Image())
        class Agent:
            @cpsl.message()
            async def default_chat(self, session, msg):
                return None

            @cpsl.message("research", label="Research")
            async def research(self, session, msg):
                return None

        cfg = app._serialize()

        self.assertTrue(cfg["has_message_handler"])
        self.assertEqual(cfg["message_handlers"], [{"name": "research", "label": "Research"}])


if __name__ == "__main__":
    unittest.main()
