import logging

import pytest
from contributors_txt.create_content import create_content
from pytest import LogCaptureFixture


@pytest.mark.parametrize(  # type: ignore[untyped-decorator]
    "shortlog_output,expected",
    [
        [
            "1 name <email@net.com>",
            "<email@net.com>",
        ],
        [
            "1 another_name <email@net.com>",
            "- another_name",
        ],
        [
            "\n1 name <aemail@net.com>\n2 another_name <email@net.com>",
            """- another_name <email@net.com>
- name <aemail@net.com>
""",
        ],
        [
            """
    42  Pierre Sassoulas <pierre.sassoulas@gmail.com>
     2  dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>
""",
            "- Pierre Sassoulas <pierre.sassoulas@gmail.com>",
        ],
    ],
)
def test_basic(shortlog_output: str, expected: str, caplog: LogCaptureFixture) -> None:
    caplog.set_level(logging.DEBUG)
    result = create_content(
        aliases=[], shortlog_output=shortlog_output, configuration_file="foo.conf"
    )
    assert expected in result
    assert "using the configuration in 'foo.conf'" in result
