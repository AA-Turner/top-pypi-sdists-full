#
# Copyright 2019 Stephan Müller
#
# Licensed under the GPLv3 license

"""Tests for ``pylint_gitlab.reporter``."""

import json
import os
from io import StringIO

import pytest
from pylint.lint import PyLinter


@pytest.mark.parametrize("reporter_name", ["gitlab-pages-html", "pylint_gitlab.GitlabPagesHtmlReporter"])
def test_gitlab_pages_html_reporter(reporter_name):
    """Tests for ``pylint_gitlab.reporter.GitlabPagesHtmlReporter()``."""

    output = StringIO()
    linter = PyLinter()

    linter.load_plugin_modules(["pylint_gitlab"])
    linter.set_option("output-format", reporter_name)
    linter.set_option("persistent", False)
    linter.load_default_plugins()

    reporter = linter.reporter
    reporter.out = output
    reporter.CI_PROJECT_URL = "https://example.org"
    reporter.CI_COMMIT_REF_NAME = "branch"

    linter.open()

    linter.set_current_module("b")
    linter.add_message("line-too-long", line=2, args=(1, 2))
    linter.add_message("line-too-long", line=1, args=(1, 2))

    linter.set_current_module("a")
    linter.add_message("line-too-long", line=1, args=(1, 2))

    # we call this method because we didn't actually run the checkers
    reporter.display_messages(None)

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "report.html"), "r", encoding="UTF-8") as file:
        expected_result = file.read()
    assert output.getvalue() == expected_result


@pytest.mark.parametrize("reporter_name", ["gitlab-codeclimate", "pylint_gitlab.GitlabCodeClimateReporter"])
def test_gitlab_code_climate_reporter(reporter_name):
    """Tests for ``pylint_gitlab.reporter.GitlabCodeClimateReporter()``."""

    output = StringIO()
    linter = PyLinter()

    linter.load_plugin_modules(["pylint_gitlab"])
    linter.set_option("output-format", reporter_name)
    linter.set_option("persistent", False)
    linter.load_default_plugins()

    reporter = linter.reporter
    reporter.out = output

    linter.open()

    linter.set_current_module("0123")
    linter.add_message("line-too-long", line=1, args=(1, 2))
    linter.add_message("line-too-long", line=2, args=(1, 2))

    # we call this method because we didn't actually run the checkers
    reporter.display_messages(None)

    expected_result = [{
        "type": "issue",
        "check_name": "C0301",
        "description": "C0301: Line too long (1/2)",
        "categories": ["Style"],
        "severity": "minor",
        "location": {
            "path": "0123",
            "lines": {
                "begin": 1,
            }
        },
        "fingerprint": "9703ca1a3553b7910f69f11f69170187c19b7ea47a3e2c4b086a97f5ab5f098d"
    },
    {
        "type": "issue",
        "check_name": "C0301",
        "description": "C0301: Line too long (1/2)",
        "categories": ["Style"],
        "severity": "minor",
        "location": {
            "path": "0123",
            "lines": {
                "begin": 2,
            }
        },
        "fingerprint": "94f082bd47cc09000b6902b071b25413e86488a5389f04f579ab92983a74896b"
    }]
    report_result = json.loads(output.getvalue())
    assert report_result == expected_result


@pytest.mark.parametrize(
    "reporter_name",
    ["gitlab-codeclimate-nohash", "pylint_gitlab.GitlabCodeClimateReporterNoHash"]
)
def test_gitlab_code_climate_reporter_no_hash(reporter_name):
    """Tests for ``pylint_gitlab.reporter.GitlabCodeClimateReporterNoHash()``."""

    output = StringIO()
    linter = PyLinter()

    linter.load_plugin_modules(["pylint_gitlab"])
    linter.set_option("output-format", reporter_name)
    linter.set_option("persistent", False)
    linter.load_default_plugins()

    reporter = linter.reporter
    reporter.out = output

    linter.open()

    linter.set_current_module("0123")
    linter.add_message("line-too-long", line=1, args=(1, 2))

    # we call this method because we didn't actually run the checkers
    reporter.display_messages(None)

    expected_result = [{
        "type": "issue",
        "check_name": "C0301",
        "description": "C0301: Line too long (1/2)",
        "categories": ["Style"],
        "severity": "minor",
        "location": {
            "path": "0123",
            "lines": {
                "begin": 1,
            }
        },
        "fingerprint": "0123:1:C0301"
    }]
    report_result = json.loads(output.getvalue())
    assert report_result == expected_result
