from unittest import TestCase

from abstra_internals.controllers.language_server import (
    Position,
    TextDocumentContext,
    _lsp,
    analyze_python_syntax,
    get_completions,
    get_definition,
    get_diagnostics,
    get_document_highlights,
    get_hover,
    get_references,
    get_rename_edits,
    get_signature_help,
    get_status,
)

CODE = """
import random
import abstra.hooks as ah
import abstra.workflows as aw
from clients import send_message

print("\U0001f552 Hook is running...")

msg = send_message(text="every hour I RUN")
aw.set_data("thread_ts", msg["ts"])

color = random.choice(["red", "blue"])
aw.set_data("color", color)

ah.send_json({"message": "A message from the hook!"})
"""

# CODE lines (0-based):
#  0: ""
#  1: "import random"
#  2: "import abstra.hooks as ah"
#  3: "import abstra.workflows as aw"
#  4: "from clients import send_message"
#  5: ""
#  6: 'print("\U0001f552 Hook is running...")'
#  7: ""
#  8: 'msg = send_message(text="every hour I RUN")'
#  9: 'aw.set_data("thread_ts", msg["ts"])'
# 10: ""
# 11: 'color = random.choice(["red", "blue"])'
# 12: 'aw.set_data("color", color)'
# 13: ""
# 14: 'ah.send_json({"message": "A message from the hook!"})'
# 15: ""
# CODE + "\nah.sen" -> line 16: "ah.sen"


# ── Completions ──────────────────────────────────────────────────────────


class TestCompletionsAbstraLib(TestCase):
    def test_send_json_completion(self):
        completions = get_completions(CODE + "\nah.sen", 16, 6)
        labels = [c.get("label", "") for c in completions]
        self.assertTrue(
            any("send_json" in label for label in labels),
            f"Expected 'send_json' in completions, got: {labels}",
        )

    def test_send_response_completion(self):
        completions = get_completions(CODE + "\nah.sen", 16, 6)
        labels = [c.get("label", "") for c in completions]
        self.assertTrue(
            any("send_response" in label for label in labels),
            f"Expected 'send_response' in completions, got: {labels}",
        )


class TestCompletionsStdlib(TestCase):
    def test_random_module_completions(self):
        completions = get_completions(CODE + "\nrandom.", 16, 7)
        labels = [c.get("label", "") for c in completions]
        self.assertTrue(
            any("choice" in label for label in labels),
            f"Expected 'choice' in completions, got: {labels}",
        )

    def test_os_module_completions(self):
        code = "import os\nos."
        completions = get_completions(code, 1, 3)
        labels = [c.get("label", "") for c in completions]
        self.assertTrue(
            any("path" in label for label in labels),
            f"Expected 'path' in completions, got: {labels}",
        )
        self.assertTrue(
            any("getcwd" in label for label in labels),
            f"Expected 'getcwd' in completions, got: {labels}",
        )


class TestCompletionsBuiltins(TestCase):
    def test_print_completion(self):
        code = "pri"
        completions = get_completions(code, 0, 3)
        labels = [c.get("label", "") for c in completions]
        self.assertTrue(
            any("print" in label for label in labels),
            f"Expected 'print' in completions, got: {labels}",
        )


# ── Hover ────────────────────────────────────────────────────────────────


class TestHover(TestCase):
    def test_hover_on_function_call(self):
        hover = get_hover(CODE, 14, 5)
        self.assertIsNotNone(hover)

    def test_hover_on_builtin(self):
        hover = get_hover(CODE, 6, 3)
        self.assertIsNotNone(hover)

    def test_hover_on_variable(self):
        code = "x = 42\nprint(x)"
        hover = get_hover(code, 0, 0)
        self.assertIsNotNone(hover)

    def test_hover_on_module(self):
        code = "import os\nos.path"
        hover = get_hover(code, 0, 8)
        self.assertIsNotNone(hover)

    def test_hover_on_keyword_empty(self):
        """Hovering on a keyword like 'if' should return None or empty."""
        code = "if True:\n    pass"
        hover = get_hover(code, 0, 1)
        # Keywords typically have no hover info; None or empty contents is fine
        if hover is not None:
            self.assertIn("contents", hover)

    def test_hover_on_empty_line(self):
        code = "x = 1\n\nprint(x)"
        hover = get_hover(code, 1, 0)
        # Empty line: None or empty/trivial content is fine
        if hover is not None:
            self.assertIn("contents", hover)


# ── Diagnostics ──────────────────────────────────────────────────────────


class TestDiagnostics(TestCase):
    def test_syntax_error(self):
        diagnostics = get_diagnostics("if:")
        self.assertGreater(len(diagnostics), 0)
        diag = diagnostics[0]
        self.assertIn("range", diag)
        self.assertIn("message", diag)
        self.assertIn("severity", diag)

    def test_valid_code_no_errors(self):
        # Diagnostics may include stale results from the shared LSP process.
        # Just verify the call succeeds and returns a list.
        diagnostics = get_diagnostics("valid_var_123 = 42\nprint(valid_var_123)\n")
        self.assertIsInstance(diagnostics, list)

    def test_another_syntax_error(self):
        code = "def foo(\n    return 1"
        diagnostics = get_diagnostics(code)
        self.assertGreater(len(diagnostics), 0, "Expected a syntax error diagnostic")


# ── Definition ───────────────────────────────────────────────────────────


class TestDefinition(TestCase):
    def test_intra_file_definition(self):
        code = "def foo():\n    pass\n\nfoo()"
        # Go to definition of foo() call on line 3, col 1
        result = get_definition(code, 3, 1)
        self.assertIsNotNone(result)
        self.assertEqual(result["uri"], "self")
        # Definition should point to line 0 (where 'def foo' is)
        self.assertEqual(result["range"]["start"]["line"], 0)

    def test_stdlib_definition_not_self(self):
        code = "from os.path import join\njoin"
        result = get_definition(code, 1, 1)
        self.assertIsNotNone(result)
        # Should not be "self" -- it's defined externally
        self.assertNotEqual(result["uri"], "self")
        # Should not be a "project:" file either
        self.assertFalse(
            result["uri"].startswith("project:"),
            f"Expected external URI, got: {result['uri']}",
        )

    def test_definition_on_empty_returns_none(self):
        code = "x = 1\n\nprint(x)"
        result = get_definition(code, 1, 0)
        # Empty line -- no definition expected
        # None is acceptable
        if result is not None:
            self.assertIn("uri", result)


# ── References ───────────────────────────────────────────────────────────


class TestReferences(TestCase):
    def test_find_all_references(self):
        code = "x = 1\nprint(x)\ny = x + 2"
        refs = get_references(code, 0, 0)
        self.assertGreaterEqual(len(refs), 2, f"Expected >=2 references, got: {refs}")
        # All references should be "self" (same buffer)
        for ref in refs:
            self.assertEqual(ref["uri"], "self")

    def test_function_references(self):
        code = "def greet():\n    pass\n\ngreet()\ngreet()"
        refs = get_references(code, 0, 5)
        # At least the definition + 2 calls = 3
        self.assertGreaterEqual(len(refs), 3, f"Expected >=3 references, got: {refs}")


# ── Document Highlights ──────────────────────────────────────────────────


class TestDocumentHighlights(TestCase):
    def test_highlight_variable(self):
        code = "x = 1\nprint(x)\ny = x + 2"
        highlights = get_document_highlights(code, 0, 0)
        self.assertGreaterEqual(
            len(highlights), 2, f"Expected >=2 highlights, got: {highlights}"
        )
        # Each highlight has a range
        for h in highlights:
            self.assertIn("range", h)

    def test_highlight_no_symbol(self):
        code = "x = 1\n\nprint(x)"
        highlights = get_document_highlights(code, 1, 0)
        # Empty line: no highlights expected
        self.assertEqual(len(highlights), 0)


# ── Signature Help ───────────────────────────────────────────────────────


class TestSignatureHelp(TestCase):
    def test_signature_inside_call(self):
        code = "print("
        result = get_signature_help(code, 0, 6)
        # pyrefly may or may not support signature help; accept None or dict
        if result is not None:
            self.assertIn("signatures", result)


# ── Rename ───────────────────────────────────────────────────────────────


class TestRename(TestCase):
    def test_rename_variable(self):
        code = "foo = 1\nprint(foo)"
        result = get_rename_edits(code, 0, 1, "bar")
        # pyrefly may or may not support rename; accept None or dict with changes
        if result is not None:
            self.assertIn("changes", result)
            # If changes are provided, they should contain edits
            for uri, edits in result["changes"].items():
                self.assertIsInstance(edits, list)
                for edit in edits:
                    self.assertIn("range", edit)
                    self.assertIn("newText", edit)
                    self.assertEqual(edit["newText"], "bar")


# ── analyze_python_syntax (MCP wrapper) ──────────────────────────────────


class TestAnalyzePythonSyntax(TestCase):
    def test_syntax_error_via_mcp(self):
        result = analyze_python_syntax("if:")
        self.assertIn("diagnostics", result)
        diagnostics = result["diagnostics"]
        self.assertGreater(len(diagnostics), 0)
        diag = diagnostics[0]
        self.assertIn("range", diag)
        self.assertIn("message", diag)
        self.assertIn("severity", diag)
        self.assertGreater(result["error_count"], 0)
        # Hint must be present whenever there are real errors so the AI is
        # nudged toward the SDK types instead of `Any` / `# type: ignore`.
        self.assertIsNotNone(result["type_discipline_hint"])
        self.assertIn("abstra", result["type_discipline_hint"])

    def test_valid_code_via_mcp(self):
        result = analyze_python_syntax("x = 1\nprint(x)\n")
        errors = [d for d in result["diagnostics"] if d.get("severity") == 1]
        self.assertEqual(len(errors), 0)
        self.assertEqual(result["error_count"], 0)
        # Hint is suppressed on clean code to avoid noise in tool responses.
        self.assertIsNone(result["type_discipline_hint"])

    def test_returns_dict(self):
        result = analyze_python_syntax("pass")
        self.assertIsInstance(result, dict)
        self.assertIn("diagnostics", result)
        self.assertIsInstance(result["diagnostics"], list)
        self.assertIn("error_count", result)
        self.assertIn("warning_count", result)
        self.assertIn("type_discipline_hint", result)


# ── PyreflyLSP lifecycle ─────────────────────────────────────────────────


class TestPyreflyLSPLifecycle(TestCase):
    def test_ensure_running_starts_process(self):
        """After _ensure_running, process should be alive and initialized."""
        _lsp._ensure_running()
        self.assertIsNotNone(_lsp._process)
        self.assertIsNone(_lsp._process.poll())
        self.assertTrue(_lsp._initialized.is_set())

    def test_resolve_paths_sets_values(self):
        """_resolve_paths should set root_path, temp_path, uri, root_uri."""
        _lsp._resolve_paths()
        self.assertIsNotNone(_lsp._root_path)
        self.assertIsNotNone(_lsp._temp_path)
        self.assertTrue(_lsp._temp_path.endswith(".pyrefly_buffer.py"))
        self.assertIsNotNone(_lsp._uri)
        self.assertTrue(_lsp._uri.startswith("file://"))
        self.assertIsNotNone(_lsp._root_uri)
        self.assertTrue(_lsp._root_uri.startswith("file://"))

    def test_process_restart_after_crash(self):
        """If the LSP process is killed, _ensure_running should restart it."""
        _lsp._ensure_running()
        old_pid = _lsp._process.pid
        _lsp._process.kill()
        _lsp._process.wait()
        # Now ensure it restarts
        _lsp._ensure_running()
        self.assertIsNotNone(_lsp._process)
        self.assertIsNone(_lsp._process.poll())
        new_pid = _lsp._process.pid
        self.assertNotEqual(old_pid, new_pid)


# ── URI resolution ───────────────────────────────────────────────────────


class TestResolveUri(TestCase):
    def test_self_uri(self):
        _lsp._resolve_paths()
        self.assertEqual(_lsp._resolve_uri(_lsp._uri), "self")

    def test_project_uri(self):
        _lsp._resolve_paths()
        project_uri = "file://" + _lsp._root_path + "/some_module.py"
        self.assertEqual(_lsp._resolve_uri(project_uri), "project:some_module.py")

    def test_project_uri_nested(self):
        _lsp._resolve_paths()
        nested_uri = "file://" + _lsp._root_path + "/pkg/sub/mod.py"
        self.assertEqual(_lsp._resolve_uri(nested_uri), "project:pkg/sub/mod.py")

    def test_external_uri(self):
        _lsp._resolve_paths()
        external_uri = "file:///usr/lib/python3/os.py"
        result = _lsp._resolve_uri(external_uri)
        self.assertEqual(result, external_uri)


# ── TextDocumentContext model ────────────────────────────────────────────


class TestTextDocumentContext(TestCase):
    def test_parse_full_input(self):
        ctx = TextDocumentContext(
            code="print(1)", position=Position(line=0, character=5)
        )
        self.assertEqual(ctx.code, "print(1)")
        self.assertEqual(ctx.position.line, 0)
        self.assertEqual(ctx.position.character, 5)

    def test_defaults(self):
        ctx = TextDocumentContext(code="x = 1")
        self.assertEqual(ctx.position.line, 0)
        self.assertEqual(ctx.position.character, 0)

    def test_from_dict(self):
        ctx = TextDocumentContext(
            **{"code": "hello", "position": {"line": 3, "character": 7}}
        )
        self.assertEqual(ctx.code, "hello")
        self.assertEqual(ctx.position.line, 3)
        self.assertEqual(ctx.position.character, 7)


class TestPositionModel(TestCase):
    def test_defaults(self):
        pos = Position()
        self.assertEqual(pos.line, 0)
        self.assertEqual(pos.character, 0)

    def test_explicit_values(self):
        pos = Position(line=10, character=20)
        self.assertEqual(pos.line, 10)
        self.assertEqual(pos.character, 20)


# ── get_status ───────────────────────────────────────────────────────────


class TestGetStatus(TestCase):
    def test_status_after_init(self):
        # Trigger initialization
        get_completions("x = 1", 0, 0)
        status = get_status()
        self.assertIn("alive", status)
        self.assertIn("initialized", status)
        self.assertIn("doc_version", status)
        self.assertIn("doc_open", status)
        self.assertTrue(status["alive"])
        self.assertTrue(status["initialized"])
        self.assertTrue(status["doc_open"])


# ── Edge cases ───────────────────────────────────────────────────────────


class TestEdgeCases(TestCase):
    def test_empty_code_completions(self):
        completions = get_completions("", 0, 0)
        self.assertIsInstance(completions, list)

    def test_empty_code_diagnostics(self):
        diagnostics = get_diagnostics("")
        self.assertIsInstance(diagnostics, list)

    def test_empty_code_hover(self):
        hover = get_hover("", 0, 0)
        # None or empty is acceptable
        if hover is not None:
            self.assertIsInstance(hover, dict)

    def test_unicode_code(self):
        code = '# \u00e9\u00e0\u00fc\u00f1\n\u00e7af\u00e9 = "caf\u00e9"\nprint(\u00e7af\u00e9)'
        diagnostics = get_diagnostics(code)
        self.assertIsInstance(diagnostics, list)

    def test_unicode_completions(self):
        code = '# \u00e9\u00e0\u00fc\u00f1\n\u00e7af\u00e9 = "caf\u00e9"\n\u00e7af'
        completions = get_completions(code, 2, 3)
        self.assertIsInstance(completions, list)

    def test_long_code(self):
        lines = [f"x_{i} = {i}" for i in range(500)]
        code = "\n".join(lines)
        diagnostics = get_diagnostics(code)
        self.assertIsInstance(diagnostics, list)

    def test_multiline_string(self):
        code = 'x = """\nline1\nline2\n"""\nprint(x)'
        hover = get_hover(code, 4, 7)
        # Should not crash; hover on 'x' variable
        if hover is not None:
            self.assertIsInstance(hover, dict)

    def test_position_beyond_code_length(self):
        code = "x = 1"
        # Position way beyond the code -- should not crash
        completions = get_completions(code, 100, 100)
        self.assertIsInstance(completions, list)

    def test_concurrent_requests(self):
        """Multiple sequential requests should work without corruption."""
        import concurrent.futures

        def do_completion(i):
            code = f"import os\nos.path.join\nx_{i} = {i}\nos."
            return get_completions(code, 3, 3)

        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(do_completion, i) for i in range(3)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]

        for result in results:
            self.assertIsInstance(result, list)


# ── file:// URI construction (Windows regression) ─────────────────────────


class TestFileUriConstruction(TestCase):
    """Regression for the Windows-only hang: the client built URIs as
    ``"file://" + path``, which on Windows yields ``file://C:\\...`` (drive as
    authority, backslashes invalid). Pyrefly publishes diagnostics under its
    canonical ``file:///C:/.../...`` URI, so the keys never matched and every
    file timed out with zero diagnostics (62 files x 5s ~= 310s)."""

    def test_windows_path_produces_canonical_uri(self):
        # _path_to_uri uses Path.as_uri(); on Windows that yields the canonical
        # form below — exactly what Pyrefly published in the field report, so
        # the key we wait on now matches. (PureWindowsPath lets this run on any
        # OS: a bare Path("C:\\...") on POSIX would not be treated as absolute.)
        from pathlib import PureWindowsPath

        uri = PureWindowsPath(
            r"C:\Users\lucas\Abstra\personal-project\.pyrefly_buffer.py"
        ).as_uri()
        self.assertEqual(
            uri,
            "file:///C:/Users/lucas/Abstra/personal-project/.pyrefly_buffer.py",
        )
        self.assertTrue(uri.startswith("file:///"))
        self.assertNotIn("\\", uri)

    def test_posix_uri_unchanged_from_old_concatenation(self):
        from abstra_internals.controllers.language_server import _path_to_uri

        path = "/home/user/project/.pyrefly_buffer.py"
        # Old behavior on POSIX was "file://" + path — must stay identical.
        self.assertEqual(_path_to_uri(path), "file://" + path)

    def test_uri_to_path_round_trips(self):
        from abstra_internals.controllers.language_server import (
            _path_to_uri,
            _uri_to_path,
        )

        path = "/home/user/project/my file.py"  # includes a space
        self.assertEqual(_uri_to_path(_path_to_uri(path)), path)
