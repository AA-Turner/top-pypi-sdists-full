import pytest

from agentql import QuerySyntaxError
from agentql._core._syntax.lexer import Lexer
from agentql._core._syntax.source import Source
from agentql._core._syntax.token_kind import TokenKind

VALID_QUERY_TEST_DATA = [
    (
        # Single element
        """
        {
            sign_in_btn
        }
        """,
        [
            (TokenKind.BRACE_L, None),
            (TokenKind.IDENTIFIER, "sign_in_btn"),
            (TokenKind.BRACE_R, None),
            (TokenKind.EOF, None),
        ],
    ),
    (
        # Single element with empty description
        """
        {
            sign_in_btn()
        }
        """,
        [
            (TokenKind.BRACE_L, None),
            (TokenKind.IDENTIFIER, "sign_in_btn"),
            (TokenKind.DESCRIPTION, ""),
            (TokenKind.BRACE_R, None),
            (TokenKind.EOF, None),
        ],
    ),
    (
        # Single element with description
        """
        {
            sign_in_btn(Logs into the website using the provided email and phone number)
        }
        """,
        [
            (TokenKind.BRACE_L, None),
            (TokenKind.IDENTIFIER, "sign_in_btn"),
            (
                TokenKind.DESCRIPTION,
                "Logs into the website using the provided email and phone number",
            ),
            (TokenKind.BRACE_R, None),
            (TokenKind.EOF, None),
        ],
    ),
    (
        # Single element with description that starts and end with same character (that is not quotation mark)
        """
        {
            sign_in_btn(aa)
            sign_in_box("aba")
        }
        """,
        [
            (TokenKind.BRACE_L, None),
            (TokenKind.IDENTIFIER, "sign_in_btn"),
            (
                TokenKind.DESCRIPTION,
                "aa",
            ),
            (TokenKind.IDENTIFIER, "sign_in_box"),
            (
                TokenKind.DESCRIPTION,
                "aba",
            ),
            (TokenKind.BRACE_R, None),
            (TokenKind.EOF, None),
        ],
    ),
    (
        # Multiple element
        """
        {
            sign_in_btn
            sign_in_box
        }
        """,
        [
            (TokenKind.BRACE_L, None),
            (TokenKind.IDENTIFIER, "sign_in_btn"),
            (TokenKind.IDENTIFIER, "sign_in_box"),
            (TokenKind.BRACE_R, None),
            (TokenKind.EOF, None),
        ],
    ),
    (
        # Multiple element with description
        """
        {
            sign_in_btn(Logs into the website using the provided email and phone number)
            sign_in_box(Input field for email and phone number)
        }
        """,
        [
            (TokenKind.BRACE_L, None),
            (TokenKind.IDENTIFIER, "sign_in_btn"),
            (
                TokenKind.DESCRIPTION,
                "Logs into the website using the provided email and phone number",
            ),
            (TokenKind.IDENTIFIER, "sign_in_box"),
            (TokenKind.DESCRIPTION, "Input field for email and phone number"),
            (TokenKind.BRACE_R, None),
            (TokenKind.EOF, None),
        ],
    ),
    (
        # Element with children
        """
        {
            header {
                sign_in_btn
            }
            about
        }
        """,
        [
            (TokenKind.BRACE_L, None),
            (TokenKind.IDENTIFIER, "header"),
            (TokenKind.BRACE_L, None),
            (TokenKind.IDENTIFIER, "sign_in_btn"),
            (TokenKind.BRACE_R, None),
            (TokenKind.IDENTIFIER, "about"),
            (TokenKind.BRACE_R, None),
            (TokenKind.EOF, None),
        ],
    ),
    (
        # Element with children and description
        """
        {
            header(The container at the top of the website which contains all the navigation elements) {
                sign_in_btn(Logs into the website (using the pro)vided email and phone number)
            }
            about
        }
        """,
        [
            (TokenKind.BRACE_L, None),
            (TokenKind.IDENTIFIER, "header"),
            (
                TokenKind.DESCRIPTION,
                "The container at the top of the website which contains all the navigation elements",
            ),
            (TokenKind.BRACE_L, None),
            (TokenKind.IDENTIFIER, "sign_in_btn"),
            (
                TokenKind.DESCRIPTION,
                "Logs into the website (using the pro)vided email and phone number",
            ),
            (TokenKind.BRACE_R, None),
            (TokenKind.IDENTIFIER, "about"),
            (TokenKind.BRACE_R, None),
            (TokenKind.EOF, None),
        ],
    ),
    (
        # List element
        """
        {
            footer {
                links[]
            }
        }
        """,
        [
            (TokenKind.BRACE_L, None),
            (TokenKind.IDENTIFIER, "footer"),
            (TokenKind.BRACE_L, None),
            (TokenKind.IDENTIFIER, "links"),
            (TokenKind.BRACKET_L, None),
            (TokenKind.BRACKET_R, None),
            (TokenKind.BRACE_R, None),
            (TokenKind.BRACE_R, None),
            (TokenKind.EOF, None),
        ],
    ),
    (
        # List element with description
        """
        {
            footer {
                links(The animated links that relate to discounts)[]
            }
        }
        """,
        [
            (TokenKind.BRACE_L, None),
            (TokenKind.IDENTIFIER, "footer"),
            (TokenKind.BRACE_L, None),
            (TokenKind.IDENTIFIER, "links"),
            (TokenKind.DESCRIPTION, "The animated links that relate to discounts"),
            (TokenKind.BRACKET_L, None),
            (TokenKind.BRACKET_R, None),
            (TokenKind.BRACE_R, None),
            (TokenKind.BRACE_R, None),
            (TokenKind.EOF, None),
        ],
    ),
    (
        # Tab + preceding + trailing spaces in query
        """
            {
    header {
                                sign_in_btn
                }
                     about(Explanation of what the company does)
            }
        """,
        [
            (TokenKind.BRACE_L, None),
            (TokenKind.IDENTIFIER, "header"),
            (TokenKind.BRACE_L, None),
            (TokenKind.IDENTIFIER, "sign_in_btn"),
            (TokenKind.BRACE_R, None),
            (TokenKind.IDENTIFIER, "about"),
            (TokenKind.DESCRIPTION, "Explanation of what the company does"),
            (TokenKind.BRACE_R, None),
            (TokenKind.EOF, None),
        ],
    ),
    (
        # Deeply nested query
        """
        {
            header {
                sign_in_btn {
                    hello {
                        world
                    }
                }
            }
            about
        }
        """,
        [
            (TokenKind.BRACE_L, None),
            (TokenKind.IDENTIFIER, "header"),
            (TokenKind.BRACE_L, None),
            (TokenKind.IDENTIFIER, "sign_in_btn"),
            (TokenKind.BRACE_L, None),
            (TokenKind.IDENTIFIER, "hello"),
            (TokenKind.BRACE_L, None),
            (TokenKind.IDENTIFIER, "world"),
            (TokenKind.BRACE_R, None),
            (TokenKind.BRACE_R, None),
            (TokenKind.BRACE_R, None),
            (TokenKind.IDENTIFIER, "about"),
            (TokenKind.BRACE_R, None),
            (TokenKind.EOF, None),
        ],
    ),
    (
        # Extra lines in the query
        """
        {

            header(Information container at the top of the website) {
                sign_in_btn
            }
            about
        }
        """,
        [
            (TokenKind.BRACE_L, None),
            (TokenKind.IDENTIFIER, "header"),
            (TokenKind.DESCRIPTION, "Information container at the top of the website"),
            (TokenKind.BRACE_L, None),
            (TokenKind.IDENTIFIER, "sign_in_btn"),
            (TokenKind.BRACE_R, None),
            (TokenKind.IDENTIFIER, "about"),
            (TokenKind.BRACE_R, None),
            (TokenKind.EOF, None),
        ],
    ),
    (
        # Properly closed parantheses within the description
        """
        {
            sign_in_btn(Frank (favorite) restaurant)
        }
        """,
        [
            (TokenKind.BRACE_L, None),
            (TokenKind.IDENTIFIER, "sign_in_btn"),
            (TokenKind.DESCRIPTION, "Frank (favorite) restaurant"),
            (TokenKind.BRACE_R, None),
            (TokenKind.EOF, None),
        ],
    ),
    (
        # Double enclosing quotation marks in the description
        """
        {
            sign_in_btn("Pasha")
        }
        """,
        [
            (TokenKind.BRACE_L, None),
            (TokenKind.IDENTIFIER, "sign_in_btn"),
            (TokenKind.DESCRIPTION, "Pasha"),
            (TokenKind.BRACE_R, None),
            (TokenKind.EOF, None),
        ],
    ),
    (
        # Double enclosing apostrophes in the description
        """
        {
            sign_in_btn('Pasha')
        }
        """,
        [
            (TokenKind.BRACE_L, None),
            (TokenKind.IDENTIFIER, "sign_in_btn"),
            (TokenKind.DESCRIPTION, "Pasha"),
            (TokenKind.BRACE_R, None),
            (TokenKind.EOF, None),
        ],
    ),
    (
        # Extra quotation mark in the description post unwrapping
        """
        {
            sign_in_btn("Pasha"")
        }
        """,
        [
            (TokenKind.BRACE_L, None),
            (TokenKind.IDENTIFIER, "sign_in_btn"),
            (TokenKind.DESCRIPTION, 'Pasha"'),
            (TokenKind.BRACE_R, None),
            (TokenKind.EOF, None),
        ],
    ),
    (
        # Single quotation mark in the description
        """
        {
            sign_in_btn(Frank's favorite restaurant)
        }
        """,
        [
            (TokenKind.BRACE_L, None),
            (TokenKind.IDENTIFIER, "sign_in_btn"),
            (TokenKind.DESCRIPTION, "Frank's favorite restaurant"),
            (TokenKind.BRACE_R, None),
            (TokenKind.EOF, None),
        ],
    ),
    (
        # Extra apostrophe in the description post unwrapping
        """
        {
            sign_in_btn("Pasha'")
        }
        """,
        [
            (TokenKind.BRACE_L, None),
            (TokenKind.IDENTIFIER, "sign_in_btn"),
            (TokenKind.DESCRIPTION, "Pasha'"),
            (TokenKind.BRACE_R, None),
            (TokenKind.EOF, None),
        ],
    ),
    (
        # No associated apostrophe or quotation in the description so no unwrapping
        """
        {
            sign_in_btn('"Pasha'")
        }
        """,
        [
            (TokenKind.BRACE_L, None),
            (TokenKind.IDENTIFIER, "sign_in_btn"),
            (TokenKind.DESCRIPTION, "'\"Pasha'\""),
            (TokenKind.BRACE_R, None),
            (TokenKind.EOF, None),
        ],
    ),
    (
        """
        {
            sign_in_btn,
        }
        """,
        [
            (TokenKind.BRACE_L, None),
            (TokenKind.IDENTIFIER, "sign_in_btn"),
            (TokenKind.COMMA, None),
            (TokenKind.BRACE_R, None),
            (TokenKind.EOF, None),
        ],
    ),
    (
        """
        {
            sign_in_btn[],
        }
        """,
        [
            (TokenKind.BRACE_L, None),
            (TokenKind.IDENTIFIER, "sign_in_btn"),
            (TokenKind.BRACKET_L, None),
            (TokenKind.BRACKET_R, None),
            (TokenKind.COMMA, None),
            (TokenKind.BRACE_R, None),
            (TokenKind.EOF, None),
        ],
    ),
    (
        """
        {
            form {
                btn1
                btn2,
                btn3
            },
        }
        """,
        [
            (TokenKind.BRACE_L, None),
            (TokenKind.IDENTIFIER, "form"),
            (TokenKind.BRACE_L, None),
            (TokenKind.IDENTIFIER, "btn1"),
            (TokenKind.IDENTIFIER, "btn2"),
            (TokenKind.COMMA, None),
            (TokenKind.IDENTIFIER, "btn3"),
            (TokenKind.BRACE_R, None),
            (TokenKind.COMMA, None),
            (TokenKind.BRACE_R, None),
            (TokenKind.EOF, None),
        ],
    ),
    # valid non-ascii characters
    (
        """
        {
            copyright(text after the © symbol, 版权信息, 著作権情報。)
        }
        """,
        [
            (TokenKind.BRACE_L, None),
            (TokenKind.IDENTIFIER, "copyright"),
            (TokenKind.DESCRIPTION, "text after the © symbol, 版权信息, 著作権情報。"),
            (TokenKind.BRACE_R, None),
            (TokenKind.EOF, None),
        ],
    ),
]


@pytest.mark.parametrize("query, expected", VALID_QUERY_TEST_DATA)
def test_valid_query_element(query, expected):
    """Test if lexer can parse valid query element"""
    source = Source(query)
    lexer = Lexer(source)

    for expected_kind, expected_value in expected:
        token = lexer.advance()
        assert token.kind == expected_kind
        assert token.value == expected_value


INVALID_QUERY_TEST_DATA = [
    (
        # No line breaks in the description
        """
        {
            sign_in_btn(Logs into the website using the
            provided email and phone number)
        }
        """
    ),
    (
        # No double quotation marks in the identifier
        """
        {
            "sign_in_btn"(Pasha)
        }
        """
    ),
    (
        # No newline in the description
        """
        {
            sign_in_btn(Frank\ns favorite restaurant)
        }
        """
    ),
    (
        # Parantheses not closed
        """
        {
            sign_in_btn(Frank favorite restaurant
        }
        """
    ),
    (
        # No nested (not closed) parantheses within the description
        """
        {
            sign_in_btn(Frank (favorite restaurant)
        }
        """
    ),
    (
        # No nested (not opened) parantheses within the description
        """
        {
            sign_in_btn(Frank favorite ) restaurant )
        }
        """
    ),
    (
        # No newline in the description
        """
        {
            sign_in_btn(Franks
            favorite restaurant)
        }
        """
    ),
    (
        # No preceding digit in the identifier
        """
        {
            1_sign_in_btn(Franks favorite restaurant)
        }
        """
    ),
    (
        # No unexpected unicode
        """
        {
            header {
                sign_in_btn
            }
            about
            \u00a9
        }
        """
    ),
    (
        # Paranthesis incorrectly used (with line breaks)
        """
        (
            header {
                sign_in_btn
                hello
            }
            about
        )
        """
    ),
]


@pytest.mark.parametrize("query", INVALID_QUERY_TEST_DATA)
def test_query_invalid(query):
    """Test if lexer can raise an error when an invalid query is encountered"""
    with pytest.raises(QuerySyntaxError):
        source = Source(query)
        lexer = Lexer(source)
        while lexer.token.kind.value != TokenKind.EOF.value:
            lexer.advance()


def test_ignored_tokens():
    """Make sure ignored tokens are not reported, but still registered in the token stream."""
    query = """{\n\nfooter}"""

    source = Source(query)
    lexer = Lexer(source)

    expected = [
        (TokenKind.BRACE_L, None),
        (TokenKind.IDENTIFIER, "footer"),
        (TokenKind.BRACE_R, None),
        (TokenKind.EOF, None),
    ]
    for expected_kind, expected_value in expected:
        token = lexer.advance()
        if token.kind is TokenKind.IDENTIFIER:
            assert token.prev is not None
            assert token.prev.kind is TokenKind.NEWLINE
            assert lexer.last_token.kind is TokenKind.BRACE_L
        assert token.kind == expected_kind
        assert token.value == expected_value
