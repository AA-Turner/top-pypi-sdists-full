from abstra_internals.agents.tools.browser import _prepare_script


class TestPrepareScript:
    def test_simple_expression_unchanged(self):
        assert _prepare_script("window.location.href") == "window.location.href"

    def test_bare_return_wrapped_in_iife(self):
        result = _prepare_script("return window.location.href;")
        assert result == "(async () => { return window.location.href; })()"

    def test_multiline_with_return_wrapped(self):
        script = "const x = 1;\nreturn x;"
        result = _prepare_script(script)
        assert result == f"(async () => {{ {script} }})()"

    def test_expression_without_return_unchanged(self):
        assert (
            _prepare_script("document.querySelectorAll('a').length")
            == "document.querySelectorAll('a').length"
        )

    def test_return_inside_function_not_matched(self):
        script = "(function() { return 42; })()"
        assert _prepare_script(script) == script

    def test_return_at_start_of_line_after_statements(self):
        script = "let a = 1;\n  return a + 1;"
        result = _prepare_script(script)
        assert result.startswith("(async () => {")
