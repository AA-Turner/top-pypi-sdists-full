"""
NX CLI — computer-use VISION planning (nx_computer vision path) unit tests.

Proves the pure vision layer with NO real model + NO GUI: PNG dimension parse, base64 data-URI encode, the
multimodal message shape, Retina coordinate scaling, and — critically — that plan_next_action_vision DEGRADES to
the existing text planner on every failure mode (no vision fn / no screenshot / empty reply / raise) and never
fakes a click. The GLM vision call + screencapture are device-proven (fireworks/deepinfra key + macOS), not CI.

Run: python3 tests/test_nx_computer_vision.py
"""
import base64
import os
import struct
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import nx_computer as nc  # noqa: E402


def _png_bytes(w, h):
    """A minimal valid-enough PNG header (signature + IHDR length/type + width/height) for dimension parsing."""
    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">I", 13) + b"IHDR" + struct.pack(">II", w, h)
    return sig + ihdr + b"\x08\x06\x00\x00\x00" + b"\x00" * 8


def _write_png(w, h):
    fd, path = tempfile.mkstemp(suffix=".png")
    with os.fdopen(fd, "wb") as f:
        f.write(_png_bytes(w, h))
    return path


class TestPngDims(unittest.TestCase):
    def test_reads_width_height(self):
        p = _write_png(2880, 1800)
        self.addCleanup(os.remove, p)
        self.assertEqual(nc.png_dimensions(p), (2880, 1800))

    def test_non_png_is_none(self):
        fd, p = tempfile.mkstemp()
        os.write(fd, b"not a png at all, just text bytes here")
        os.close(fd)
        self.addCleanup(os.remove, p)
        self.assertIsNone(nc.png_dimensions(p))

    def test_missing_file_is_none(self):
        self.assertIsNone(nc.png_dimensions("/no/such/file.png"))


class TestEncode(unittest.TestCase):
    def test_encodes_data_uri(self):
        p = _write_png(10, 10)
        self.addCleanup(os.remove, p)
        uri = nc.encode_image_data_uri(p)
        self.assertTrue(uri.startswith("data:image/png;base64,"))
        # round-trips to the file bytes
        raw = base64.b64decode(uri.split(",", 1)[1])
        self.assertEqual(raw, _png_bytes(10, 10))

    def test_missing_or_empty_is_none(self):
        self.assertIsNone(nc.encode_image_data_uri(""))
        self.assertIsNone(nc.encode_image_data_uri("/no/such.png"))


class TestVisionMessages(unittest.TestCase):
    def test_multimodal_shape(self):
        obs = {"context": {"app": "Safari", "window": "GitHub"}, "history": []}
        msgs = nc.build_vision_messages("click sign in", obs, "data:image/png;base64,AAAA")
        self.assertEqual(msgs[0]["role"], "system")
        self.assertEqual(msgs[1]["role"], "user")
        parts = msgs[1]["content"]
        self.assertEqual(parts[0]["type"], "text")
        self.assertIn("click sign in", parts[0]["text"])
        self.assertIn("app=Safari", parts[0]["text"])
        self.assertEqual(parts[1]["type"], "image_url")
        self.assertEqual(parts[1]["image_url"]["url"], "data:image/png;base64,AAAA")


class TestScalePoint(unittest.TestCase):
    def test_retina_2x_maps_to_logical(self):
        self.assertEqual(nc.scale_point(200, 100, 2880, 1800, 1440, 900), (100, 50))

    def test_identity_degrade_on_missing_dims(self):
        self.assertEqual(nc.scale_point(200, 100, None, None, 1440, 900), (200, 100))
        self.assertEqual(nc.scale_point(200, 100, 2880, 1800, 0, 900), (200, 100))


class TestPlanNextActionVision(unittest.TestCase):
    def _obs(self, screenshot="/tmp/x.png"):
        return {"screenshot": screenshot, "screen_size": (1440, 900), "context": {"app": "Safari"}, "history": []}

    def test_happy_path_scales_and_clamps(self):
        p = _write_png(2880, 1800)  # 2x screenshot
        self.addCleanup(os.remove, p)
        vision_fn = lambda _m: '{"kind":"click","x":400,"y":200,"target":"the Save button"}'
        a = nc.plan_next_action_vision("save it", self._obs(p), vision_fn, text_model_fn=lambda _p: "TEXT")
        self.assertEqual(a["kind"], "click")
        self.assertEqual((a["x"], a["y"]), (200, 100))  # 400/2, 200/2

    def test_no_vision_fn_falls_to_text(self):
        spy = {"called": False}
        def text_fn(_p):
            spy["called"] = True
            return '{"kind":"done"}'
        nc.plan_next_action_vision("x", self._obs(), None, text_model_fn=text_fn)
        self.assertTrue(spy["called"])

    def test_no_screenshot_falls_to_text(self):
        spy = {"called": False}
        def text_fn(_p):
            spy["called"] = True
            return '{"kind":"done"}'
        nc.plan_next_action_vision("x", self._obs(screenshot=None), lambda _m: "{}", text_model_fn=text_fn)
        self.assertTrue(spy["called"])

    def test_empty_vision_reply_falls_to_text(self):
        p = _write_png(100, 100)
        self.addCleanup(os.remove, p)
        spy = {"called": False}
        def text_fn(_p):
            spy["called"] = True
            return '{"kind":"open_app","app":"Notes"}'
        a = nc.plan_next_action_vision("x", self._obs(p), lambda _m: "", text_model_fn=text_fn)
        self.assertTrue(spy["called"])
        self.assertEqual(a["kind"], "open_app")

    def test_vision_fn_raises_falls_to_text(self):
        p = _write_png(100, 100)
        self.addCleanup(os.remove, p)
        spy = {"called": False}
        def text_fn(_p):
            spy["called"] = True
            return '{"kind":"done"}'
        def boom(_m):
            raise RuntimeError("model down")
        nc.plan_next_action_vision("x", self._obs(p), boom, text_model_fn=text_fn)
        self.assertTrue(spy["called"])


class TestLogicalScreenSize(unittest.TestCase):
    def test_none_off_mac(self):
        from unittest import mock
        with mock.patch.object(nc, "is_macos", return_value=False):
            self.assertIsNone(nc.logical_screen_size())


if __name__ == "__main__":
    unittest.main()
