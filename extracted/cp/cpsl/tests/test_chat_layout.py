import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import cpsl
from cpsl.runner import _wants_session


class ChatLayoutTests(unittest.TestCase):
    def test_chat_page_and_shell_serialize(self):
        app = cpsl.App(name="chat-layout-test", image=cpsl.Image(), channels=[cpsl.Chat()])
        app.shell(home="chat", show_sidebar=True, show_pages=False)

        @app.chat_page()
        def chat_page():
            return cpsl.ui.Page([
                cpsl.ui.Row([
                    cpsl.ui.Column([cpsl.ui.Text("Sources")], fill=True, gap=12),
                    cpsl.ui.ChatPanel(
                        title="Chat",
                        placeholder="Ask about your sources...",
                        height=520,
                    ),
                ], columns=[0.8, 1.2], min_widths=[220, 320], gap=16, fill=True)
            ])

        cfg = app._serialize()

        self.assertEqual(cfg["shell"], {
            "home": "chat",
            "show_sidebar": True,
            "show_pages": False,
        })
        tree = cfg["chat"]["widget_tree"]
        self.assertEqual(tree["type"], "page")
        self.assertEqual(tree["children"][0]["columns"], [0.8, 1.2])
        self.assertEqual(tree["children"][0]["min_widths"], [220, 320])
        self.assertEqual(tree["children"][0]["gap"], 16)
        self.assertTrue(tree["children"][0]["fill"])
        self.assertTrue(tree["children"][0]["children"][0]["fill"])
        panel = tree["children"][0]["children"][1]
        self.assertEqual(panel["type"], "chat_panel")
        self.assertEqual(panel["title"], "Chat")
        self.assertEqual(panel["placeholder"], "Ask about your sources...")
        self.assertEqual(panel["height"], 520)
        self.assertTrue(panel["show_header"])

    def test_chat_page_requires_one_chat_panel(self):
        app = cpsl.App(name="chat-layout-validation", image=cpsl.Image())

        with self.assertRaises(ValueError):
            @app.chat_page()
            def missing_panel():
                return cpsl.ui.Page([cpsl.ui.Text("No chat")])

        with self.assertRaises(ValueError):
            @app.chat_page()
            def duplicate_panel():
                return cpsl.ui.Page([cpsl.ui.ChatPanel(), cpsl.ui.ChatPanel()])

    def test_shell_home_validation(self):
        app = cpsl.App(name="shell-validation", image=cpsl.Image())

        with self.assertRaises(ValueError):
            app.shell(home="landing")

    def test_data_handler_can_request_session(self):
        def by_name(session: cpsl.Session):
            return {"session_id": session.id}

        def by_string(session: "cpsl.Session"):
            return {"session_id": session.id}

        def no_session(ctx: cpsl.RequestContext):
            return {"user_id": ctx.user.id}

        self.assertTrue(_wants_session(by_name))
        self.assertTrue(_wants_session(by_string))
        self.assertFalse(_wants_session(no_session))


if __name__ == "__main__":
    unittest.main()
