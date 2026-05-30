import inspect
from unittest import TestCase

from abstra_internals.utils.sdk import SDKContractParser, SilentLogger


def _get_parser() -> SDKContractParser:
    # Constructor takes a module name; `_parse_docstring` does not touch it,
    # so any value works for unit tests. Use SilentLogger to keep test output
    # clean.
    parser = SDKContractParser.__new__(SDKContractParser)
    parser.logger = SilentLogger()
    parser.module_name = "abstra"
    return parser


def _docstring_of(func) -> str:
    # Mirror what the parser sees in production: inspect.getdoc on the live
    # function, which strips leading indentation consistently across all
    # lines.
    return inspect.getdoc(func) or ""


class ParseDocstringTest(TestCase):
    def setUp(self):
        self.parser = _get_parser()

    def test_plain_prose_preserves_paragraphs(self):
        def f():
            """First paragraph.

            Second paragraph.
            """

        result = self.parser._parse_docstring(_docstring_of(f))
        self.assertEqual(
            result["description"],
            "First paragraph.\n\nSecond paragraph.",
        )
        self.assertEqual(result["params"], {})

    def test_args_section_extracted_into_params(self):
        def f():
            """Do something.

            Args:
                x (int): The first value.
                y (str): The second value.
            """

        result = self.parser._parse_docstring(_docstring_of(f))
        self.assertEqual(result["description"], "Do something.")
        self.assertEqual(set(result["params"]), {"x", "y"})
        self.assertEqual(result["params"]["x"]["type"], "int")
        self.assertEqual(result["params"]["x"]["description"], "The first value.")

    def test_returns_section_dropped_from_description(self):
        # The docs site renders a separate `## Return Value` section from the
        # return-type annotation, so duplicating `**Returns:**` in the prose
        # would be redundant. The whole section is dropped.
        def f():
            """Get a thing.

            Returns:
                Thing: The thing.
            """

        result = self.parser._parse_docstring(_docstring_of(f))
        self.assertEqual(result["description"], "Get a thing.")

    def test_returns_dropped_raises_kept(self):
        def f():
            """Get the user.

            Returns:
                UserClaims: User information.

            Raises:
                GetUserFailed: If no valid authentication is found.
            """

        result = self.parser._parse_docstring(_docstring_of(f))
        self.assertEqual(
            result["description"],
            "Get the user.\n\n"
            "**Raises:**\n\n"
            "GetUserFailed: If no valid authentication is found.",
        )

    def test_example_section_preserves_fenced_code_block(self):
        def f():
            """Render the page.

            Example:
                ```python
                from abstra.pages import register_function

                @register_function
                def __render__():
                    return "<h1>Hi</h1>"
                ```
            """

        result = self.parser._parse_docstring(_docstring_of(f))
        expected = (
            "Render the page.\n\n"
            "**Example:**\n\n"
            "```python\n"
            "from abstra.pages import register_function\n\n"
            "@register_function\n"
            "def __render__():\n"
            '    return "<h1>Hi</h1>"\n'
            "```"
        )
        self.assertEqual(result["description"], expected)

    def test_args_then_example_recovers_example_into_description(self):
        # When Args: is followed by Example: (or any other Google-style
        # section), the params parser must stop at the section boundary and
        # the trailing section is put back into the description.
        def f():
            """Do something.

            Args:
                x (int): The value.

            Example:
                ```python
                do_something(1)
                ```
            """

        result = self.parser._parse_docstring(_docstring_of(f))
        self.assertEqual(set(result["params"]), {"x"})
        self.assertEqual(result["params"]["x"]["description"], "The value.")
        self.assertIn("**Example:**", result["description"])
        self.assertIn("```python\ndo_something(1)\n```", result["description"])

    def test_example_before_args(self):
        def f():
            """Do something.

            Example:
                ```python
                do_something(1)
                ```

            Args:
                x (int): The value.
            """

        result = self.parser._parse_docstring(_docstring_of(f))
        self.assertEqual(set(result["params"]), {"x"})
        self.assertIn("**Example:**", result["description"])
        self.assertIn("```python\ndo_something(1)\n```", result["description"])

    def test_no_flattening_of_existing_markdown(self):
        # Docstrings that author Markdown directly (bold headers, bullet
        # lists) must not collapse to a single line.
        def f():
            """Parse a document.

            The parser extracts fields including:

            **Company Information:**
            - cnpj: Tax id
            - razao_social: Legal name

            **Financial Information:**
            - valor_total: Total amount
            """

        result = self.parser._parse_docstring(_docstring_of(f))
        self.assertIn("\n- cnpj: Tax id", result["description"])
        self.assertIn("**Company Information:**", result["description"])
        self.assertIn("**Financial Information:**", result["description"])

    def test_returns_after_args_does_not_bleed_into_last_param(self):
        # Regression: the line-by-line params parser used to absorb the
        # indented Returns:/Raises: bodies into the last Args: parameter's
        # description because it didn't recognize them as section terminators.
        # Returns: itself is dropped from description (covered by Return Value),
        # but Raises: remains.
        def f():
            """Parse a thing.

            Args:
                path (str): The file path.

            Returns:
                dict: The parsed data.

            Raises:
                ValueError: If path is invalid.
            """

        result = self.parser._parse_docstring(_docstring_of(f))
        self.assertEqual(result["params"]["path"]["description"], "The file path.")
        self.assertNotIn("**Returns:**", result["description"])
        self.assertNotIn("dict: The parsed data.", result["description"])
        self.assertIn("**Raises:**", result["description"])
        self.assertIn("ValueError: If path is invalid.", result["description"])

    def test_section_with_indented_sub_bullets_renders_as_list(self):
        # Authors commonly indent sub-bullets under a top-level type/prose
        # line. Markdown would render those as a code block; the rewriter
        # must pull them to column 0 so they become a proper bullet list.
        def f():
            """Iterate items.

            Yields:
                Tuple[str, Dict, Dict]: A tuple containing:
                    - Body as string
                    - Headers as dict
                    - Query params as dict
            """

        result = self.parser._parse_docstring(_docstring_of(f))
        # The "Tuple[...]: A tuple containing:" line stays as-is; the
        # following bullets must be at column 0.
        self.assertIn("\n- Body as string\n", result["description"])
        self.assertIn("\n- Headers as dict\n", result["description"])
        self.assertIn("\n- Query params as dict", result["description"])
        # No leading spaces before bullets.
        self.assertNotIn("    - Body as string", result["description"])

    def test_section_with_empty_body(self):
        def f():
            """Do nothing.

            Note:
            """

        result = self.parser._parse_docstring(_docstring_of(f))
        self.assertEqual(result["description"], "Do nothing.\n\n**Note:**")
