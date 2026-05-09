import os
import sys
import unittest
import asyncio
import types as pytypes

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import cpsl
from cpsl.image import Image
from cpsl.runner import Runner, _resolve_message_handler


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

    def test_unknown_named_chat_does_not_fallback_to_default(self):
        async def default_chat(session, msg):
            return None

        async def acquisition(session, msg):
            return None

        with self.assertRaisesRegex(RuntimeError, "Unknown chat surface 'missing'"):
            _resolve_message_handler(
                {"acquisition": acquisition},
                default_chat,
                "missing",
            )

    def test_default_chat_still_uses_default_handler(self):
        async def default_chat(session, msg):
            return None

        self.assertIs(_resolve_message_handler({}, default_chat, ""), default_chat)

    def test_runner_boot_loads_functional_named_handlers(self):
        module_name = "_tmp_named_runner_app"
        mod = pytypes.ModuleType(module_name)
        app = cpsl.App(name="named-runner", image=Image())

        @app.message()
        async def default_chat(session, msg):
            return None

        @app.message("deal-desk", label="Deal Desk")
        async def deal_chat(session, msg):
            return None

        mod.app = app
        sys.modules[module_name] = mod
        try:
            runner = Runner(module_name, "app")
            asyncio.run(runner.boot())
            self.assertIs(runner._message_handlers["deal-desk"], deal_chat)
            self.assertIs(runner._message_handlers[""], default_chat)
        finally:
            sys.modules.pop(module_name, None)


if __name__ == "__main__":
    unittest.main()
