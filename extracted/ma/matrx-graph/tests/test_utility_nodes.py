"""Tests for the text-manipulate, datetime, and crypto utility packs."""

from __future__ import annotations

import re

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)

from tests._fixtures import make_app_context


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    return reg


async def _run(
    node_type: str,
    inputs: dict,
    config: dict | None = None,
) -> dict:
    registry = _registry()
    data: dict = {}
    if config is not None:
        data["config"] = config
    # A single-node definition DECLARES its inputs (W68: a definition that
    # saves is a definition that can start) — the run below still delivers the
    # same values over the broadcast channel, last-writer-wins.
    data["inputs"] = inputs
    defn = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "n",
                    "type": node_type,
                    "position": {"x": 0, "y": 0},
                    "data": data,
                }
            ],
            "edges": [],
        }
    )
    graph = compile_graph(defn, registry=registry)
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=registry)
    result = await scheduler.run(run_id=f"t-{node_type}", inputs=inputs)
    assert result.status is RunStatus.COMPLETED, result.status
    return result.last_outputs["n"]


# ---------------------------------------------------------------------------
# text.template
# ---------------------------------------------------------------------------


async def test_template_fills_placeholders():
    out = await _run(
        "text.template",
        {
            "template": "Hello {{user.name}}, you have {{count}} msgs.",
            "variables": {"user": {"name": "Ada"}, "count": 3},
        },
    )
    assert out["text"] == "Hello Ada, you have 3 msgs."
    assert out["missing_keys"] == []


async def test_template_reports_missing_keys():
    out = await _run(
        "text.template",
        {"template": "Hi {{name}} / {{age}}", "variables": {"name": "x"}},
    )
    assert out["text"] == "Hi x / "
    assert out["missing_keys"] == ["age"]


# ---------------------------------------------------------------------------
# text.split + text.join
# ---------------------------------------------------------------------------


async def test_split_literal_delimiter():
    out = await _run(
        "text.split",
        {"text": "a,b,,c"},
        {"delimiter": ","},
    )
    assert out["parts"] == ["a", "b", "", "c"]
    assert out["count"] == 4


async def test_split_with_strip_and_drop_empty():
    out = await _run(
        "text.split",
        {"text": " a , , b , c "},
        {"delimiter": ",", "strip": True, "drop_empty": True},
    )
    assert out["parts"] == ["a", "b", "c"]


async def test_split_regex_mode():
    out = await _run(
        "text.split",
        {"text": "one1two22three333four"},
        {"delimiter": r"\d+", "regex": True},
    )
    assert out["parts"] == ["one", "two", "three", "four"]


async def test_split_max_splits_means_the_same_thing_on_both_branches():
    """``max_splits`` is a cap on SPLITS — N splits ⇒ N+1 parts, literal or regex.

    Regression: the literal branch subtracted one, so ``max_splits=1`` performed
    ZERO splits and returned the text unsplit while the regex branch split once.
    """
    for regex, delimiter in ((False, ","), (True, ",")):
        one = await _run(
            "text.split",
            {"text": "a,b,c,d"},
            {"delimiter": delimiter, "regex": regex, "max_splits": 1},
        )
        assert one["parts"] == ["a", "b,c,d"], (regex, one)

        two = await _run(
            "text.split",
            {"text": "a,b,c,d"},
            {"delimiter": delimiter, "regex": regex, "max_splits": 2},
        )
        assert two["parts"] == ["a", "b", "c,d"], (regex, two)

        unlimited = await _run(
            "text.split",
            {"text": "a,b,c,d"},
            {"delimiter": delimiter, "regex": regex, "max_splits": 0},
        )
        assert unlimited["parts"] == ["a", "b", "c", "d"], (regex, unlimited)


async def test_join_with_separator_prefix_suffix():
    out = await _run(
        "text.join",
        {"parts": ["a", "b", "c"]},
        {"separator": ", ", "prefix": "[", "suffix": "]"},
    )
    assert out["text"] == "[a, b, c]"


# ---------------------------------------------------------------------------
# text.slug
# ---------------------------------------------------------------------------


async def test_slug_basic():
    out = await _run(
        "text.slug",
        {"text": "Hello, World! Matrx Graph v1.0"},
    )
    assert out["slug"] == "hello-world-matrx-graph-v1-0"


async def test_slug_unicode_normalized_to_ascii():
    out = await _run(
        "text.slug",
        {"text": "Café Olé — résumé"},
    )
    assert out["slug"] == "cafe-ole-resume"


async def test_slug_respects_max_length():
    out = await _run(
        "text.slug",
        {"text": "a " * 200},
        {"max_length": 20},
    )
    assert len(out["slug"]) <= 20
    assert not out["slug"].endswith("-")


# ---------------------------------------------------------------------------
# text.word_count
# ---------------------------------------------------------------------------


async def test_word_count_basic():
    out = await _run(
        "text.word_count",
        {"text": "Hello world. This is Matrx! Yes."},
    )
    assert out["words"] == 6
    assert out["sentences"] == 3
    assert out["characters"] == 32


# ---------------------------------------------------------------------------
# datetime.*
# ---------------------------------------------------------------------------


async def test_datetime_now_returns_iso_and_unix():
    out = await _run("datetime.now", {})
    assert "T" in out["iso"]
    assert out["unix_ms"] > 1_700_000_000_000  # > 2023
    assert 0 <= out["weekday"] <= 6


async def test_datetime_parse_iso():
    # Node Result System: the scheduler unwraps Success — the bare payload
    # carries iso/unix_ms only (the old ok/error payload fields are gone).
    out = await _run(
        "datetime.parse",
        {"text": "2026-04-23T12:34:56"},
    )
    assert out["iso"].startswith("2026-04-23T12:34:56")
    assert "ok" not in out and "error" not in out


async def test_datetime_parse_naive_input_is_read_as_utc():
    """A timezone-less input resolves to a MACHINE-INDEPENDENT instant.

    Arman's ruling (2026-08-21): "a workflow's answer must not depend on which
    box ran it." ``datetime.timestamp()`` on a naive value assumes the WORKER's
    local timezone, so this same call used to return a different ``unix_ms`` on
    a UTC box than on a US-Eastern one. The ambiguity is still reported —
    ``has_timezone`` says the INPUT never stated an offset.
    """
    out = await _run("datetime.parse", {"text": "2026-04-23T12:34:56"})
    # 2026-04-23T12:34:56Z — fixed, whatever TZ this test runs in.
    assert out["unix_ms"] == 1776947696000
    assert out["iso"] == "2026-04-23T12:34:56+00:00"
    assert out["has_timezone"] is False, "the input carried no offset and must say so"
    assert out["utc_offset_seconds"] == 0


async def test_datetime_parse_keeps_a_stated_offset():
    """An input that DOES state its offset is never re-interpreted."""
    out = await _run("datetime.parse", {"text": "2026-04-23T12:34:56-04:00"})
    assert out["has_timezone"] is True
    assert out["utc_offset_seconds"] == -14400
    assert out["unix_ms"] == 1776962096000


async def test_datetime_add_naive_input_is_read_as_utc():
    out = await _run("datetime.add", {"iso": "2026-04-23T12:34:56"}, {"hours": 2})
    assert out["iso"] == "2026-04-23T14:34:56+00:00"
    assert out["unix_ms"] == 1776954896000
    assert out["has_timezone"] is False


async def test_datetime_parse_custom_format():
    out = await _run(
        "datetime.parse",
        {"text": "23/04/2026 12:34"},
        {"format": "%d/%m/%Y %H:%M"},
    )
    assert out["iso"].startswith("2026-04-23T12:34")


async def _run_expect_error(node_type: str, inputs: dict, config: dict | None = None):
    registry = _registry()
    data: dict = {}
    if config is not None:
        data["config"] = config
    # A single-node definition DECLARES its inputs (W68: a definition that
    # saves is a definition that can start) — the run below still delivers the
    # same values over the broadcast channel, last-writer-wins.
    data["inputs"] = inputs
    defn = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "n",
                    "type": node_type,
                    "position": {"x": 0, "y": 0},
                    "data": data,
                }
            ],
            "edges": [],
        }
    )
    graph = compile_graph(defn, registry=registry)
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=registry)
    result = await scheduler.run(run_id=f"t-fail-{node_type}", inputs=inputs)
    assert result.status is RunStatus.ERRORED, result.status
    return result


async def test_datetime_parse_invalid_string_is_node_failure():
    # A parse failure is a node Failure with a stable code — never an
    # ok=false payload flowing downstream as data.
    result = await _run_expect_error("datetime.parse", {"text": "not a date"})
    assert "parse_failed" in (result.error or "")


async def test_datetime_format_strftime():
    out = await _run(
        "datetime.format",
        {"iso": "2026-04-23T12:34:56"},
        {"format": "%Y-%m-%d"},
    )
    assert out["text"] == "2026-04-23"
    assert "ok" not in out


async def test_datetime_format_invalid_iso_is_node_failure():
    result = await _run_expect_error("datetime.format", {"iso": "nope"}, {"format": "%Y-%m-%d"})
    assert "parse_failed" in (result.error or "")


async def test_datetime_add_invalid_iso_is_node_failure():
    result = await _run_expect_error("datetime.add", {"iso": "nope"}, {"days": 1})
    assert "parse_failed" in (result.error or "")


async def test_datetime_add_days():
    out = await _run(
        "datetime.add",
        {"iso": "2026-04-23T00:00:00"},
        {"days": 7},
    )
    assert out["iso"].startswith("2026-04-30T00:00:00")


async def test_datetime_add_negative_hours():
    out = await _run(
        "datetime.add",
        {"iso": "2026-04-23T12:00:00"},
        {"hours": -3, "minutes": -30},
    )
    assert out["iso"].startswith("2026-04-23T08:30:00")


# ---------------------------------------------------------------------------
# crypto.*
# ---------------------------------------------------------------------------


async def test_hash_sha256():
    out = await _run(
        "crypto.hash",
        {"text": "hello"},
    )
    assert out["algorithm"] == "sha256"
    assert out["digest"] == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"


async def test_hash_truncate_and_uppercase():
    out = await _run(
        "crypto.hash",
        {"text": "hello"},
        {"algorithm": "sha256", "truncate": 12, "uppercase": True},
    )
    assert len(out["digest"]) == 12
    assert out["digest"] == out["digest"].upper()


async def test_hash_md5_matches_known_value():
    out = await _run(
        "crypto.hash",
        {"text": "hello"},
        {"algorithm": "md5"},
    )
    assert out["digest"] == "5d41402abc4b2a76b9719d911017c592"


async def test_uuid_v4_format():
    out = await _run("crypto.uuid", {})
    assert re.match(
        r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
        out["uuid"],
    )


async def test_uuid_no_hyphens_when_flag_false():
    out = await _run("crypto.uuid", {}, {"hyphenated": False})
    assert "-" not in out["uuid"]
    assert len(out["uuid"]) == 32


async def test_uuid_version_7_really_is_version_7_and_time_ordered():
    """``version: 7`` must deliver an RFC 9562 timestamp-ordered UUID.

    Regression: the node read ``getattr(uuid, "uuid7", uuid.uuid4)`` on a
    comment claiming 3.13 had ``uuid.uuid7``. It does not (that is 3.14), so
    every ``version=7`` request silently returned a RANDOM v4 — an author who
    chose time-ordering for database insert locality never got it, and nothing
    said so.
    """
    import uuid as uuid_module

    first = await _run("crypto.uuid", {}, {"version": 7})
    second = await _run("crypto.uuid", {}, {"version": 7})

    import time

    assert uuid_module.UUID(first["uuid"]).version == 7
    assert uuid_module.UUID(second["uuid"]).version == 7
    # The payload reports the version it ACTUALLY produced, read from the value.
    assert first["version"] == 7

    # Time-ordered at MILLISECOND granularity — which is what RFC 9562's basic
    # method guarantees. Asserting the whole string is ordered would be flaky:
    # two ids minted inside the same millisecond share a timestamp and differ
    # only in random bits, so their relative order is undefined.
    def timestamp_ms(value: str) -> int:
        return uuid_module.UUID(value).int >> 80

    assert timestamp_ms(second["uuid"]) >= timestamp_ms(first["uuid"])
    # And it is a REAL timestamp, not zeros or random bits: within a minute of
    # now. This is the assertion the v4 fallback could never have passed.
    now_ms = time.time_ns() // 1_000_000
    assert abs(now_ms - timestamp_ms(first["uuid"])) < 60_000


async def test_uuid_version_4_is_still_random_and_self_reported():
    import uuid as uuid_module

    out = await _run("crypto.uuid", {}, {"version": 4})
    assert uuid_module.UUID(out["uuid"]).version == 4
    assert out["version"] == 4


async def test_random_string_uses_configured_length_and_alphabet():
    out = await _run(
        "crypto.random_string",
        {},
        {"length": 20, "alphabet": "digits"},
    )
    assert len(out["value"]) == 20
    assert out["value"].isdigit()


async def test_random_string_url_safe_alphabet():
    out = await _run(
        "crypto.random_string",
        {},
        {"length": 30, "alphabet": "url_safe"},
    )
    for ch in out["value"]:
        assert ch.isalnum() or ch in {"-", "_"}
