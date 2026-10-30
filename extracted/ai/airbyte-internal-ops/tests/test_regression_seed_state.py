# Copyright (c) 2026 Airbyte, Inc., all rights reserved.
"""The seed state's shape, and how it reaches the READ step without reaching the log."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from airbyte_ops_mcp.regression_tests import seed_state
from airbyte_ops_mcp.regression_tests.seed_state import (
    MASK_MIN_LENGTH,
    SEED_STATE_NEEDS_CONNECTION,
    SEED_STATE_NEEDS_DISPATCH,
    mask_values,
    seed_state_error,
    seeded_streams,
)

pytestmark = pytest.mark.unit


def stream_state(name: str, cursor: object) -> dict:
    return {
        "type": "STREAM",
        "stream": {
            "stream_descriptor": {"name": name},
            "stream_state": {"updated_at": cursor},
        },
    }


SEED = json.dumps(
    [
        stream_state("users", "2026-01-01T00:00:00Z"),
        stream_state("orders", "2026-01-02T00:00:00Z"),
    ]
)

REFUSED_SEEDS = [
    pytest.param("{not json", "not valid JSON", id="not-json"),
    pytest.param('"[]"', "got a string", id="a-string"),
    pytest.param("42", "got a number", id="a-number"),
    pytest.param("null", "got null", id="null"),
    pytest.param("[]", "empty list", id="empty-list"),
    pytest.param(
        json.dumps(stream_state("users", "x")),
        "wrap it in a list",
        id="a-single-message-not-a-list",
    ),
    pytest.param(
        '{"type": "GLOBAL", "global": {"shared_state": {}, "stream_states": []}}',
        "GLOBAL state message, which cannot seed a read",
        id="global",
    ),
    pytest.param(
        '{"type": "LEGACY", "data": {"users": {"updated_at": "x"}}}',
        "LEGACY state message, which cannot seed a read",
        id="legacy",
    ),
    pytest.param(
        '{"users": {"updated_at": "x"}}', "the legacy state shape", id="bare-object"
    ),
    pytest.param(
        '["STREAM"]',
        "state_json[0] is a string, not a state message",
        id="a-list-of-strings",
    ),
    pytest.param(
        '[{"stream": {"stream_descriptor": {"name": "users"}}}]',
        "state_json[0] has no type",
        id="untyped-message",
    ),
    pytest.param(
        json.dumps([stream_state("users", "x"), {"type": "GLOBAL", "global": {}}]),
        "state_json[1] is a 'GLOBAL' state message",
        id="global-among-streams",
    ),
    pytest.param(
        '[{"type": "STREAM", "stream": {"stream_state": {}}}]',
        "state_json[0] names no stream",
        id="nameless-stream",
    ),
]


@pytest.mark.parametrize(("state_json", "reason"), REFUSED_SEEDS)
def test_a_seed_that_is_not_a_list_of_stream_messages_is_refused_and_told_why(
    state_json: str, reason: str
) -> None:
    error = seed_state_error(state_json)

    assert error is not None
    assert reason in error
    assert "state_json" in error


def test_a_refusal_never_echoes_the_seed() -> None:
    """The message reaches a job log the seed is kept out of."""
    cursor = "2026-01-01T00:00:00Z"
    seeds = [
        json.dumps(stream_state("users", cursor)),
        json.dumps({"type": "GLOBAL", "global": {"shared_state": {"c": cursor}}}),
        json.dumps({"users": {"updated_at": cursor}}),
        json.dumps([{"type": "LEGACY", "data": {"updated_at": cursor}}]),
    ]

    for seed in seeds:
        error = seed_state_error(seed)
        assert error is not None
        assert cursor not in error


def test_a_refusal_shows_a_strange_type_quoted_escaped_and_cut() -> None:
    """The type is the seed's own text, headed for a job log."""
    strange = "X" * 100 + "\n::add-mask::"

    error = seed_state_error(json.dumps([{"type": strange}]))

    assert error is not None
    assert error.startswith("state_json[0] is a 'XXXX")
    assert "\n" not in error
    assert "add-mask" not in error
    assert len(error) < 140


def test_a_list_of_stream_messages_is_accepted() -> None:
    assert seed_state_error(SEED) is None
    assert seeded_streams(SEED) == [(None, "users"), (None, "orders")]


def test_a_seeded_stream_keeps_its_namespace() -> None:
    """`users` in two namespaces is two streams; an empty namespace is none."""
    seed = [
        stream_state("users", "x"),
        stream_state("users", "y"),
        stream_state("orders", "z"),
    ]
    seed[0]["stream"]["stream_descriptor"]["namespace"] = "public"
    seed[1]["stream"]["stream_descriptor"]["namespace"] = "reporting"
    seed[2]["stream"]["stream_descriptor"]["namespace"] = ""

    assert seeded_streams(json.dumps(seed)) == [
        ("public", "users"),
        ("reporting", "users"),
        (None, "orders"),
    ]


def test_a_one_line_seed_is_masked_whole_and_by_its_cursors() -> None:
    assert mask_values(SEED) == [
        SEED,
        "2026-01-01T00:00:00Z",
        "2026-01-02T00:00:00Z",
    ]


def test_a_pretty_printed_seed_is_masked_by_its_cursors_only() -> None:
    """Its structural lines would redact every brace in the job log."""
    pretty = json.dumps(json.loads(SEED), indent=2)

    values = mask_values(pretty)

    assert values == ["2026-01-01T00:00:00Z", "2026-01-02T00:00:00Z"]
    assert all(len(value) >= MASK_MIN_LENGTH for value in values)


def test_a_numeric_cursor_is_masked_and_a_short_one_is_not() -> None:
    seed = json.dumps([stream_state("users", 123456789), stream_state("orders", 7)])

    assert mask_values(seed) == [seed, "123456789"]


def test_stream_names_are_not_masked() -> None:
    """A stream name shows up in every summary; masking it would eat them."""
    assert "users" not in mask_values(SEED)


def test_a_percent_is_escaped_as_the_runner_unescapes_it() -> None:
    seed = json.dumps([stream_state("users", "2026-01-01T00%3A00%3A00")])

    assert mask_values(seed) == [
        seed.replace("%", "%25"),
        "2026-01-01T00%253A00%253A00",
    ]


def test_a_line_break_in_a_cursor_is_escaped_so_the_mask_stays_one_line() -> None:
    """The runner reads a command's value to the end of the line and unescapes
    %0D and %0A; unescaped, the second half would go unmasked."""
    seed = json.dumps([stream_state("users", "2026-01-01\r\nT00:00:00Z")])

    values = mask_values(seed)

    assert values == [
        seed,
        "2026-01-01%0D%0AT00:00:00Z",
        "2026-01-01\\r\\nT00:00:00Z",
    ]
    assert all("\n" not in value and "\r" not in value for value in values)


def test_a_cursor_is_also_masked_as_json_writes_it_inside_a_string() -> None:
    """A connector that logs its state as JSON prints a cursor escaped. The
    runner masks the quote and backslash escapes itself, not `\\uXXXX`."""
    quoted = 'he said "hi" \\ ok'
    accented = "Zürich-2026-01-01"
    seed = json.dumps(
        [stream_state("users", quoted), stream_state("orders", accented)],
        ensure_ascii=False,
    )

    assert mask_values(seed) == [
        seed,
        quoted,
        'he said \\"hi\\" \\\\ ok',
        accented,
        "Z\\u00fcrich-2026-01-01",
    ]


def test_a_short_cursor_is_not_masked_in_its_longer_escaped_form() -> None:
    """`Zürich` is six characters; `json.dumps` writes it in eleven."""
    seed = json.dumps([stream_state("users", "Zürich")], ensure_ascii=False)

    assert mask_values(seed) == [seed]


def test_a_seed_that_is_not_json_is_masked_by_its_lines() -> None:
    assert mask_values("{not json\nat all, truly") == ["{not json", "at all, truly"]


def _run_main(
    tmp_path: Path, capsys, *, inputs: dict, connection_id: str = "c0ffee"
) -> tuple[int, list[str], Path]:
    event = tmp_path / "event.json"
    event.write_text(json.dumps({"inputs": inputs}))
    seed_path = tmp_path / "seed_state.json"

    status = seed_state.main([str(event), str(seed_path), connection_id])

    return status, capsys.readouterr().out.splitlines(), seed_path


def test_main_masks_before_it_judges(tmp_path: Path, capsys) -> None:
    """A malformed seed is not shown either."""
    seed = json.dumps(
        {"type": "GLOBAL", "global": {"shared_state": {"c": "2026-01-01T00:00:00Z"}}}
    )

    status, lines, seed_path = _run_main(tmp_path, capsys, inputs={"state_json": seed})

    assert status == 1
    assert lines[0] == f"::add-mask::{seed}"
    assert lines[-1].startswith("::error::")
    assert "GLOBAL" in lines[-1]
    assert not seed_path.exists()


def test_main_writes_the_seed_verbatim_and_names_the_streams(
    tmp_path: Path, capsys
) -> None:
    status, lines, seed_path = _run_main(tmp_path, capsys, inputs={"state_json": SEED})

    assert status == 0
    assert seed_path.read_text() == SEED
    assert lines == [
        f"::add-mask::{SEED}",
        "::add-mask::2026-01-01T00:00:00Z",
        "::add-mask::2026-01-02T00:00:00Z",
        "Seeding the READ with state for 2 stream(s): users, orders",
    ]


def test_main_names_a_seeded_stream_with_its_namespace(tmp_path: Path, capsys) -> None:
    message = stream_state("users", "2026-01-01T00:00:00Z")
    message["stream"]["stream_descriptor"]["namespace"] = "public"

    status, lines, _ = _run_main(
        tmp_path, capsys, inputs={"state_json": json.dumps([message])}
    )

    assert status == 0
    assert lines[-1] == "Seeding the READ with state for 1 stream(s): public.users"


def test_main_refuses_a_seed_without_a_connection(tmp_path: Path, capsys) -> None:
    status, lines, seed_path = _run_main(
        tmp_path, capsys, inputs={"state_json": SEED}, connection_id=""
    )

    assert status == 1
    assert lines[-1] == f"::error::{SEED_STATE_NEEDS_CONNECTION}"
    assert lines[0].startswith("::add-mask::")
    assert not seed_path.exists()


def test_main_refuses_a_run_whose_payload_has_no_seed(tmp_path: Path, capsys) -> None:
    """A calling workflow's inputs are not in the event payload."""
    status, lines, seed_path = _run_main(tmp_path, capsys, inputs={})

    assert status == 1
    assert lines == [f"::error::{SEED_STATE_NEEDS_DISPATCH}"]
    assert not seed_path.exists()


def test_the_script_runs_on_a_bare_interpreter(tmp_path: Path) -> None:
    """The workflow runs it with the runner's python3 from the checkout, before
    anything is installed; `-I` keeps the package off the path here."""
    event = tmp_path / "event.json"
    event.write_text(json.dumps({"inputs": {"state_json": SEED}}))
    seed_path = tmp_path / "seed_state.json"

    result = subprocess.run(
        [
            sys.executable,
            "-I",
            seed_state.__file__,
            str(event),
            str(seed_path),
            "c0ffee",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert seed_path.read_text() == SEED
    assert result.stdout.startswith(f"::add-mask::{SEED}\n")
