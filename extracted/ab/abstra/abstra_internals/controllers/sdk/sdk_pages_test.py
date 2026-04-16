import base64
import json
import os
import pathlib
import tempfile
import unittest
from typing import List, Tuple
from unittest.mock import MagicMock, call

from abstra_internals.controllers.execution.execution_client_page import PageClient
from abstra_internals.controllers.sdk.sdk_pages import PageSDKController
from abstra_internals.entities.execution_context import PageContext, Request, Response
from abstra_internals.settings import Settings

Settings.set_root_path("/tmp")


def _build_multipart_body(boundary: str, fields: List[Tuple[str, object]]) -> str:
    """Build a base64-encoded multipart/form-data body for tests.

    Each field is ``(name, value)``. ``value`` may be:
    - ``str`` → text field
    - ``(filename, content_type, bytes)`` → file field
    """
    boundary_bytes = boundary.encode("ascii")
    buf = bytearray()
    for name, value in fields:
        buf += b"--" + boundary_bytes + b"\r\n"
        if isinstance(value, tuple):
            filename, content_type, content = value
            buf += (
                f'Content-Disposition: form-data; name="{name}"; '
                f'filename="{filename}"\r\n'
            ).encode("ascii")
            buf += f"Content-Type: {content_type}\r\n\r\n".encode("ascii")
            buf += content
            buf += b"\r\n"
        else:
            buf += f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode(
                "ascii"
            )
            buf += str(value).encode("utf-8")
            buf += b"\r\n"
    buf += b"--" + boundary_bytes + b"--\r\n"
    return base64.b64encode(bytes(buf)).decode("ascii")


def _make_sdk(page_path: str = "my-page") -> tuple[PageSDKController, PageClient]:
    context = PageContext(
        request=Request(headers={}, body="", query_params={}, method="POST"),
        response=Response(headers={}, status=200, body=""),
        page_path=page_path,
    )
    conn = MagicMock()
    client = PageClient(context=context, conn=conn, production_mode=False)
    client._send = MagicMock()  # type: ignore
    users_repo = MagicMock()
    sdk = PageSDKController(client, users_repo)
    return sdk, client


class TestRegisterFunction(unittest.TestCase):
    def test_regular_function_sets_json_response(self):
        sdk, client = _make_sdk()

        @sdk.register_function
        def greet(name: str):
            return {"hello": name}

        client.context.request = Request(
            headers={},
            method="POST",
            query_params={},
            body=json.dumps({"function": "greet", "params": {"name": "world"}}),
        )
        sdk.handle_request()

        self.assertEqual(client.response.status, 200)
        data = json.loads(client.response.body)
        self.assertEqual(data["result"]["hello"], "world")

    def test_generator_function_streams(self):
        sdk, client = _make_sdk()

        @sdk.register_function
        def numbers():
            yield 1
            yield 2
            yield 3

        client.context.request = Request(
            headers={},
            method="POST",
            query_params={},
            body=json.dumps({"function": "numbers", "params": {}}),
        )
        sdk.handle_request()

        # Should have streamed via conn.send, not set response
        self.assertTrue(client._streamed)
        send_mock: MagicMock = client.conn.send  # type: ignore[assignment]
        calls = send_mock.call_args_list
        self.assertEqual(
            calls[0],
            call(
                {
                    "__page_stream__": "start",
                    "status": 200,
                    "headers": {"Content-Type": "application/x-ndjson"},
                }
            ),
        )
        self.assertEqual(calls[1], call({"__page_stream__": "chunk", "data": 1}))
        self.assertEqual(calls[2], call({"__page_stream__": "chunk", "data": 2}))
        self.assertEqual(calls[3], call({"__page_stream__": "chunk", "data": 3}))
        self.assertEqual(calls[4], call({"__page_stream__": "end"}))

    def test_generator_error_mid_stream(self):
        sdk, client = _make_sdk()

        @sdk.register_function
        def failing():
            yield "ok"
            raise ValueError("boom")

        client.context.request = Request(
            headers={},
            method="POST",
            query_params={},
            body=json.dumps({"function": "failing", "params": {}}),
        )
        sdk.handle_request()

        send_mock: MagicMock = client.conn.send  # type: ignore[assignment]
        calls = send_mock.call_args_list
        self.assertEqual(calls[0][0][0]["__page_stream__"], "start")
        self.assertEqual(calls[1], call({"__page_stream__": "chunk", "data": "ok"}))
        self.assertEqual(calls[2], call({"__page_stream__": "error", "error": "boom"}))

    def test_unknown_function_returns_404(self):
        sdk, client = _make_sdk()

        client.context.request = Request(
            headers={},
            method="POST",
            query_params={},
            body=json.dumps({"function": "nonexistent", "params": {}}),
        )
        sdk.handle_request()
        self.assertEqual(client.response.status, 404)


class TestRegisterFunctionMultipart(unittest.TestCase):
    def test_file_upload_delivers_bytes(self):
        sdk, client = _make_sdk()

        captured = {}

        @sdk.register_function
        def upload(name: str, file):
            captured["name"] = name
            captured["file"] = file
            return {"size": len(file["content"])}

        boundary = "----TestBoundary123"
        body = _build_multipart_body(
            boundary,
            [
                ("__function__", "upload"),
                ("name", json.dumps("report")),
                ("file", ("hello.txt", "text/plain", b"hello world")),
            ],
        )
        client.context.request = Request(
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
            method="POST",
            query_params={},
            body=body,
        )
        sdk.handle_request()

        self.assertEqual(client.response.status, 200)
        self.assertEqual(captured["name"], "report")
        self.assertEqual(captured["file"]["filename"], "hello.txt")
        self.assertEqual(captured["file"]["content_type"], "text/plain")
        self.assertEqual(captured["file"]["content"], b"hello world")

    def test_non_file_params_roundtrip_via_json(self):
        sdk, client = _make_sdk()

        captured = {}

        @sdk.register_function
        def mixed(count: int, tags: list, file):
            captured["count"] = count
            captured["tags"] = tags
            captured["file_bytes"] = file["content"]
            return None

        boundary = "----MixedBoundary"
        body = _build_multipart_body(
            boundary,
            [
                ("__function__", "mixed"),
                ("count", json.dumps(3)),
                ("tags", json.dumps(["a", "b"])),
                ("file", ("x.bin", "application/octet-stream", b"\x00\x01\x02")),
            ],
        )
        client.context.request = Request(
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
            method="POST",
            query_params={},
            body=body,
        )
        sdk.handle_request()

        self.assertEqual(client.response.status, 200)
        self.assertEqual(captured["count"], 3)
        self.assertEqual(captured["tags"], ["a", "b"])
        self.assertEqual(captured["file_bytes"], b"\x00\x01\x02")

    def test_multiple_files_same_name_become_list(self):
        sdk, client = _make_sdk()

        captured = {}

        @sdk.register_function
        def upload_many(files):
            captured["files"] = files
            return None

        boundary = "----MultiBoundary"
        body = _build_multipart_body(
            boundary,
            [
                ("__function__", "upload_many"),
                ("files", ("a.txt", "text/plain", b"AAA")),
                ("files", ("b.txt", "text/plain", b"BBB")),
            ],
        )
        client.context.request = Request(
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
            method="POST",
            query_params={},
            body=body,
        )
        sdk.handle_request()

        self.assertEqual(client.response.status, 200)
        self.assertIsInstance(captured["files"], list)
        self.assertEqual(len(captured["files"]), 2)
        self.assertEqual(captured["files"][0]["content"], b"AAA")
        self.assertEqual(captured["files"][1]["content"], b"BBB")

    def test_generator_with_file_streams(self):
        sdk, client = _make_sdk()

        @sdk.register_function
        def scan(file):
            for byte in file["content"]:
                yield byte

        boundary = "----GenBoundary"
        body = _build_multipart_body(
            boundary,
            [
                ("__function__", "scan"),
                ("file", ("x.bin", "application/octet-stream", b"\x05\x06")),
            ],
        )
        client.context.request = Request(
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
            method="POST",
            query_params={},
            body=body,
        )
        sdk.handle_request()

        send_mock: MagicMock = client.conn.send  # type: ignore[assignment]
        calls = send_mock.call_args_list
        self.assertEqual(calls[0][0][0]["__page_stream__"], "start")
        self.assertEqual(calls[1], call({"__page_stream__": "chunk", "data": 5}))
        self.assertEqual(calls[2], call({"__page_stream__": "chunk", "data": 6}))
        self.assertEqual(calls[3], call({"__page_stream__": "end"}))

    def test_invalid_multipart_returns_400(self):
        sdk, client = _make_sdk()

        client.context.request = Request(
            headers={"Content-Type": "multipart/form-data; boundary=----X"},
            method="POST",
            query_params={},
            body="not-valid-base64-or-body!!!",
        )
        sdk.handle_request()
        self.assertEqual(client.response.status, 400)

    def test_filename_traversal_is_sanitized(self):
        sdk, client = _make_sdk()

        captured = {}

        @sdk.register_function
        def upload(file):
            captured["file"] = file
            return None

        boundary = "----TraversalBoundary"
        body = _build_multipart_body(
            boundary,
            [
                ("__function__", "upload"),
                (
                    "file",
                    ("../../etc/passwd", "application/octet-stream", b"root:x:0"),
                ),
            ],
        )
        client.context.request = Request(
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
            method="POST",
            query_params={},
            body=body,
        )
        sdk.handle_request()

        self.assertEqual(client.response.status, 200)
        self.assertEqual(captured["file"]["filename"], "passwd")

    def test_backslash_traversal_is_sanitized(self):
        sdk, client = _make_sdk()

        captured = {}

        @sdk.register_function
        def upload(file):
            captured["file"] = file
            return None

        boundary = "----BackslashBoundary"
        body = _build_multipart_body(
            boundary,
            [
                ("__function__", "upload"),
                (
                    "file",
                    ("..\\..\\secret.txt", "text/plain", b"secret"),
                ),
            ],
        )
        client.context.request = Request(
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
            method="POST",
            query_params={},
            body=body,
        )
        sdk.handle_request()

        self.assertEqual(client.response.status, 200)
        self.assertEqual(captured["file"]["filename"], "secret.txt")


class TestJsStubGeneration(unittest.TestCase):
    def test_regular_function_generates_async(self):
        sdk, _ = _make_sdk()

        @sdk.register_function
        def get_data():
            return {}

        js = sdk._build_js_functions()
        self.assertIn("async function get_data()", js)
        self.assertNotIn("async function*", js)
        self.assertIn("return data.result", js)

    def test_generator_function_generates_stream_wrapper(self):
        sdk, _ = _make_sdk()

        @sdk.register_function
        def stream_data():
            yield 1

        js = sdk._build_js_functions()
        self.assertIn("function stream_data()", js)
        self.assertIn("async function* __stream()", js)
        self.assertIn("iter.then", js)
        self.assertIn("iter.forEach", js)
        self.assertIn("iter[Symbol.iterator]", js)
        self.assertIn("yield parsed.data", js)

    def test_js_contains_file_upload_branch(self):
        sdk, _ = _make_sdk()

        @sdk.register_function
        def upload(name: str, file):
            return None

        js = sdk._build_js_functions()
        # The generated wrapper detects Blob params at call time and picks
        # between JSON and FormData transports.
        self.assertIn("instanceof Blob", js)
        self.assertIn("instanceof FileList", js)
        self.assertIn("new FormData()", js)
        self.assertIn('__fd.append("__function__", "upload")', js)
        # JSON path is still present for no-file calls
        self.assertIn("JSON.stringify({ function:", js)

    def test_render_not_exposed_in_js(self):
        sdk, _ = _make_sdk()

        @sdk.register_function
        def __render__():
            return "<h1>Hi</h1>"

        js = sdk._build_js_functions()
        self.assertNotIn("__render__", js)


class TestPageClientStreaming(unittest.TestCase):
    def test_handle_success_skips_response_when_streamed(self):
        context = PageContext(
            request=Request(headers={}, body="", query_params={}, method="GET"),
            response=Response(headers={}, status=200, body=""),
        )
        conn = MagicMock()
        client = PageClient(context=context, conn=conn, production_mode=False)
        client._send = MagicMock()  # type: ignore

        # Simulate streaming
        client.send_stream_start(200, {"Content-Type": "application/x-ndjson"})
        client.send_stream_chunk("data")
        client.send_stream_end()

        self.assertTrue(client._streamed)

        # handle_success should NOT send self.response
        conn.reset_mock()
        client.handle_success()

        # conn.send should NOT have been called (response skipped)
        conn.send.assert_not_called()

    def test_handle_success_sends_response_when_not_streamed(self):
        context = PageContext(
            request=Request(headers={}, body="", query_params={}, method="GET"),
            response=Response(headers={}, status=200, body=""),
        )
        conn = MagicMock()
        client = PageClient(context=context, conn=conn, production_mode=False)
        client._send = MagicMock()  # type: ignore

        client.set_response(200, "hello", {})
        client.handle_success()

        # conn.send should have been called with the response
        conn.send.assert_called_once()
        sent = conn.send.call_args[0][0]
        self.assertEqual(sent.body, "hello")


class TestRegisterStatic(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        Settings.set_root_path(self.tmpdir)

    def tearDown(self):
        import shutil

        shutil.rmtree(self.tmpdir, ignore_errors=True)
        Settings.set_root_path("/tmp")

    def test_register_static_returns_url_with_token(self):
        sdk, _ = _make_sdk(page_path="my-page")
        src = pathlib.Path(self.tmpdir) / "code.js"
        src.write_text("console.log('hello');")

        url = sdk.register_static(src)

        self.assertIn(f"/_page/my-page/{src}?token=", url)

    def test_register_static_token_contains_asset_path(self):
        import jwt as pyjwt

        from abstra_internals.environment import CLOUD_API_PROD_SHARED_TOKEN

        sdk, _ = _make_sdk(page_path="my-page")
        src = pathlib.Path(self.tmpdir) / "code.js"
        src.write_text("console.log('hello');")

        url = sdk.register_static(src)

        token = url.split("token=")[1]
        payload = pyjwt.decode(
            token, key=CLOUD_API_PROD_SHARED_TOKEN, algorithms=["HS256"]
        )
        self.assertEqual(payload["asset"], str(src))

    def test_register_static_accepts_str_path(self):
        sdk, _ = _make_sdk(page_path="my-page")
        src = pathlib.Path(self.tmpdir) / "style.css"
        src.write_text("body { color: red; }")

        url = sdk.register_static(str(src))

        self.assertIn(f"/_page/my-page/{src}?token=", url)

    def test_register_static_accepts_pathlike(self):
        sdk, _ = _make_sdk(page_path="my-page")
        src = pathlib.Path(self.tmpdir) / "app.js"
        src.write_text("var x = 1;")

        url = sdk.register_static(os.fspath(src))

        self.assertIn(f"/_page/my-page/{src}?token=", url)

    def test_register_static_home_page(self):
        sdk, _ = _make_sdk(page_path="")
        src = pathlib.Path(self.tmpdir) / "app.js"
        src.write_text("var x = 1;")

        url = sdk.register_static(src)

        self.assertIn(f"/_page-home/{src}?token=", url)

    def test_register_static_file_not_found(self):
        sdk, _ = _make_sdk()

        with self.assertRaises(FileNotFoundError):
            sdk.register_static("/nonexistent/file.js")
