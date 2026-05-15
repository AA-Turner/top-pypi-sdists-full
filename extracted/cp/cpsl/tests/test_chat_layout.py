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

        @app.chat_page(mode="single", scope="owner", sidebar_label="Notebook")
        def chat_page():
            return cpsl.ui.Page(
                [
                    cpsl.ui.Row(
                        [
                            cpsl.ui.Column([cpsl.ui.Text("Sources")], fill=True, gap=12),
                            cpsl.ui.ChatPanel(
                                title="Chat",
                                placeholder="Ask about your sources...",
                                height=520,
                            ),
                        ],
                        columns=[0.8, 1.2],
                        min_widths=[220, 320],
                        gap=16,
                        fill=True,
                    )
                ]
            )

        cfg = app._serialize()

        self.assertEqual(
            cfg["shell"],
            {
                "home": "chat",
                "show_sidebar": True,
                "show_pages": False,
                "show_chats": True,
            },
        )
        self.assertEqual(cfg["chat"]["mode"], "single")
        self.assertEqual(cfg["chat"]["scope"], "owner")
        self.assertEqual(cfg["chat"]["thread_key"], "chat_page:default")
        self.assertEqual(cfg["chat"]["sidebar_label"], "Notebook")
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

    def test_column_rows_serialize(self):
        tree = cpsl.ui.Column(
            [
                cpsl.ui.ChatPanel(),
                cpsl.ui.ImageGallery(data="generated_images"),
            ],
            rows=[3, 1],
            fill=True,
            gap=12,
        ).to_dict()

        self.assertEqual(tree["type"], "column")
        self.assertEqual(tree["rows"], [3, 1])
        self.assertTrue(tree["fill"])
        self.assertEqual(tree["gap"], 12)

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

        with self.assertRaises(ValueError):

            @app.chat_page(mode="shared")
            def bad_mode():
                return cpsl.ui.Page([cpsl.ui.ChatPanel()])

        with self.assertRaises(ValueError):

            @app.chat_page(sidebar_label="")
            def bad_label():
                return cpsl.ui.Page([cpsl.ui.ChatPanel()])

    def test_shell_routes_and_page_refs_serialize(self):
        app = cpsl.App(name="page-route-test", image=cpsl.Image())

        dashboard = app.add_page(
            "Dashboard",
            icon="layout-dashboard",
            component="pages/dashboard.tsx",
            route="dash",
        )

        @app.page("Deep Dive", icon="chart-line")
        def deep_dive():
            return cpsl.ui.Page(
                [
                    cpsl.ui.ActionCard("Open dashboard", page=dashboard),
                    cpsl.ui.Button("Go to dashboard", on_click="noop", payload={"next": dashboard.route}),
                ]
            )

        app.shell(
            home="hidden",
            show_sidebar=False,
            show_chats=False,
            default_page=dashboard,
        )

        cfg = app._serialize()
        self.assertEqual(
            cfg["shell"],
            {
                "home": "hidden",
                "show_sidebar": False,
                "show_pages": True,
                "show_chats": False,
                "default_page": "dash",
            },
        )
        self.assertEqual(cfg["pages"][0]["route"], "dash")
        self.assertEqual(cfg["pages"][1]["route"], "deep-dive")
        self.assertEqual(cfg["pages"][1]["widget_tree"]["children"][0]["value"], "dash")

    def test_page_routes_avoid_reserved_derived_names(self):
        app = cpsl.App(name="reserved-route-test", image=cpsl.Image())
        home = app.add_page("Home", component="pages/home.tsx")

        self.assertEqual(home.route, "home-page")

        with self.assertRaises(ValueError):
            app.add_page("Explicit Chat", component="pages/chat.tsx", route="chat")

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

    def test_media_widgets_serialize(self):
        image_gallery = cpsl.ui.ImageGallery(
            data="generated_media",
            title="Generated images",
        ).to_dict()
        self.assertEqual(image_gallery["type"], "image_gallery")
        self.assertEqual(image_gallery["data"], "generated_media")
        self.assertEqual(image_gallery["images"], [])

        video = cpsl.ui.Video(
            "https://example.com/render.mp4",
            poster="https://example.com/poster.jpg",
            title="Walkthrough",
            caption="Generated walkthrough",
            autoplay=True,
            muted=True,
            aspect_ratio="16 / 9",
        ).to_dict()
        self.assertEqual(video["type"], "video")
        self.assertEqual(video["src"], "https://example.com/render.mp4")
        self.assertEqual(video["poster"], "https://example.com/poster.jpg")
        self.assertTrue(video["autoplay"])
        self.assertTrue(video["muted"])

        video_gallery = cpsl.ui.VideoGallery(
            data="generated_videos",
            videos=[cpsl.ui.Video("https://example.com/a.mp4", caption="A")],
            title="Generated videos",
        ).to_dict()
        self.assertEqual(video_gallery["type"], "video_gallery")
        self.assertEqual(video_gallery["data"], "generated_videos")
        self.assertEqual(video_gallery["videos"][0]["src"], "https://example.com/a.mp4")


if __name__ == "__main__":
    unittest.main()
