"""Tests for the parse_comment_bodies symbol."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.ci.supervision_control import CONTROL_MARKER
from agentic_devtools.cli.ci.supervision_control_command import parse_comment_bodies


def test_parse_comment_bodies_accepts_valid_payload() -> None:
    assert parse_comment_bodies(
        {
            "data": {
                "repository": {
                    "issue": {
                        "comments": {
                            "nodes": [
                                {"author": {"login": "automation"}, "body": "one"},
                                {"author": {"login": "automation"}, "body": "two"},
                            ]
                        }
                    }
                }
            }
        },
        trusted_author="automation",
    ) == ["one", "two"]


def test_parse_comment_bodies_ignores_untrusted_authors() -> None:
    assert (
        parse_comment_bodies(
            {
                "data": {
                    "repository": {
                        "issue": {"comments": {"nodes": [{"author": {"login": "attacker"}, "body": "forged"}]}}
                    }
                }
            },
            trusted_author="automation",
        )
        == []
    )


@pytest.mark.parametrize(
    "raw",
    [
        "not-a-dict",
        {"data": "not-an-object"},
        {"data": {"repository": "not-an-object"}},
        {"data": {"repository": {"issue": "not-an-object"}}},
        {"data": {"repository": {"issue": {"comments": "not-an-object"}}}},
        {"data": {"repository": {"issue": {"comments": {"nodes": "not-an-array"}}}}},
        {"data": {"repository": {"issue": {"comments": {"nodes": ["not-an-object"]}}}}},
        {"data": {"repository": {"issue": {"comments": {"nodes": [{"author": {"login": "automation"}, "body": 1}]}}}}},
    ],
)
def test_parse_comment_bodies_rejects_malformed_payloads(raw: object) -> None:
    with pytest.raises(ValueError):
        parse_comment_bodies(raw, trusted_author="automation")


def test_parse_comment_bodies_requires_a_trusted_author() -> None:
    with pytest.raises(ValueError, match="trusted author"):
        parse_comment_bodies(
            {"data": {"repository": {"issue": {"comments": {"nodes": []}}}}},
            trusted_author="",
        )


def test_parse_comment_bodies_rejects_malformed_label_on_protocol_state() -> None:
    with pytest.raises(ValueError, match="malformed terminal label"):
        parse_comment_bodies(
            {
                "data": {
                    "repository": {
                        "issue": {
                            "comments": {
                                "nodes": [
                                    {
                                        "author": {"login": "automation"},
                                        "body": f"{CONTROL_MARKER}\n🤖 AI PR Loop ·",
                                    }
                                ]
                            }
                        }
                    }
                }
            },
            trusted_author="automation",
        )


def test_parse_comment_bodies_rejects_whitespace_malformed_label_on_protocol_state() -> None:
    with pytest.raises(ValueError, match="malformed terminal label"):
        parse_comment_bodies(
            {
                "data": {
                    "repository": {
                        "issue": {
                            "comments": {
                                "nodes": [
                                    {
                                        "author": {"login": "automation"},
                                        "body": f"{CONTROL_MARKER}\n{{}}\n\n🤖 AI PR Loop · ",
                                    }
                                ]
                            }
                        }
                    }
                }
            },
            trusted_author="automation",
        )


def test_parse_comment_bodies_skips_malformed_label_without_protocol_state() -> None:
    result = parse_comment_bodies(
        {
            "data": {
                "repository": {
                    "issue": {
                        "comments": {
                            "nodes": [
                                {
                                    "author": {"login": "automation"},
                                    "body": "ordinary text\n🤖 AI PR Loop ·",
                                }
                            ]
                        }
                    }
                }
            }
        },
        trusted_author="automation",
    )

    assert result == []
