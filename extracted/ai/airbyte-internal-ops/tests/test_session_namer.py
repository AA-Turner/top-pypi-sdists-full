"""Unit tests for the session_namer module."""

import pytest

from airbyte_ops_mcp.session_namer import (
    _load_seed_data,
    extract_session_id,
    generate_friendly_name,
    get_namespace_size,
)


@pytest.mark.unit
@pytest.mark.parametrize(
    "identifier",
    [
        pytest.param("test-session-123", id="standard"),
        pytest.param("", id="empty_string"),
        pytest.param("b2a641e838214f91b50d0f88940ac119", id="uuid_like"),
    ],
)
def test_generate_friendly_name_deterministic(identifier: str) -> None:
    """The same identifier always produces the same Title Case two-word name."""
    name_a = generate_friendly_name(identifier)
    name_b = generate_friendly_name(identifier)
    assert name_a == name_b
    parts = name_a.split(" ")
    assert len(parts) == 2, f"Expected 2 words, got {len(parts)}: {name_a!r}"
    assert all(p.isalpha() for p in parts), f"Non-alpha tokens in: {name_a!r}"
    assert name_a == name_a.title(), f"Name not Title Case: {name_a!r}"


@pytest.mark.unit
@pytest.mark.parametrize(
    "id_a,id_b",
    [
        pytest.param("session-alpha", "session-beta", id="different_ids"),
    ],
)
def test_generate_friendly_name_different_ids(id_a: str, id_b: str) -> None:
    """Different identifiers produce different names (probabilistically)."""
    assert generate_friendly_name(id_a) != generate_friendly_name(id_b)


@pytest.mark.unit
def test_get_namespace_size() -> None:
    """The namespace size matches the combinations in the seed lists."""
    assert get_namespace_size() == 156 * 144


@pytest.mark.unit
@pytest.mark.parametrize(
    "identifier,expected_name",
    [
        pytest.param("test-session-123", "Trustworthy Sheriff", id="standard_known"),
        pytest.param(
            "b2a641e838214f91b50d0f88940ac119",
            "Prudent Navigator",
            id="standard_uuid",
        ),
    ],
)
def test_golden_vectors(identifier: str, expected_name: str) -> None:
    """Known identifiers always produce the exact expected name."""
    assert generate_friendly_name(identifier) == expected_name


@pytest.mark.unit
def test_yaml_seed_data_loads() -> None:
    """YAML seed file loads and contains expected keys with non-empty lists."""
    data = _load_seed_data()
    expected_keys = ["adjectives", "nouns"]
    for key in expected_keys:
        assert key in data, f"Missing key: {key}"
        assert isinstance(data[key], list), f"{key} is not a list"
        assert len(data[key]) > 0, f"{key} is empty"


@pytest.mark.unit
def test_yaml_seed_entries_are_strings() -> None:
    """Every seed entry is a string, including YAML boolean-like words."""
    data = _load_seed_data()
    for key in ("adjectives", "nouns"):
        assert all(isinstance(entry, str) for entry in data[key]), (
            f"{key} contains a non-string entry; quote YAML boolean-like words "
            "per the seed file quoting rule"
        )


# ---------------------------------------------------------------------------
# extract_session_id tests
# ---------------------------------------------------------------------------

_KNOWN_ID = "b2a641e838214f91b50d0f88940ac119"


@pytest.mark.unit
@pytest.mark.parametrize(
    "raw_input,expected_id",
    [
        pytest.param(_KNOWN_ID, _KNOWN_ID, id="bare_id"),
        pytest.param(
            f"https://app.devin.ai/sessions/{_KNOWN_ID}",
            _KNOWN_ID,
            id="devin_url",
        ),
        pytest.param(
            f"https://app.devin.ai/sessions/{_KNOWN_ID}/",
            _KNOWN_ID,
            id="devin_url_trailing_slash",
        ),
        pytest.param(
            f"https://app.devin.ai/sessions/{_KNOWN_ID}?pr=1281",
            _KNOWN_ID,
            id="devin_url_query_parameter",
        ),
        pytest.param(
            f"https://app.devin.ai/sessions/{_KNOWN_ID}#tab=shell",
            _KNOWN_ID,
            id="devin_url_fragment",
        ),
        pytest.param(
            f"https://app.devin.ai/sessions/{_KNOWN_ID}/pr/1281",
            _KNOWN_ID,
            id="devin_url_extra_path",
        ),
        pytest.param(
            f"https://app.devin.ai/sessions/devin-{_KNOWN_ID}",
            _KNOWN_ID,
            id="devin_url_prefixed_id",
        ),
        pytest.param(
            f"devin-{_KNOWN_ID}",
            _KNOWN_ID,
            id="devin_prefixed_id",
        ),
        pytest.param(
            "https://app.devin.ai/sessions/deadbeef-zz",
            "https://app.devin.ai/sessions/deadbeef-zz",
            id="devin_url_invalid_id",
        ),
        pytest.param(
            f"https://other.example.com/sessions/{_KNOWN_ID}",
            _KNOWN_ID,
            id="other_host_sessions_url",
        ),
        pytest.param(
            f"https://example.com/some/path/{_KNOWN_ID}",
            _KNOWN_ID,
            id="generic_url_last_segment",
        ),
        pytest.param("plain-string-no-url", "plain-string-no-url", id="plain_string"),
    ],
)
def test_extract_session_id(raw_input: str, expected_id: str) -> None:
    """extract_session_id returns the bare ID from various input formats."""
    assert extract_session_id(raw_input) == expected_id


@pytest.mark.unit
def test_url_and_bare_id_produce_same_name() -> None:
    """A session URL and its bare ID must produce identical names."""
    url = f"https://app.devin.ai/sessions/{_KNOWN_ID}"
    name_from_id = generate_friendly_name(_KNOWN_ID)
    name_from_url = generate_friendly_name(extract_session_id(url))
    assert name_from_id == name_from_url


@pytest.mark.unit
def test_devin_id_and_bare_id_produce_same_name() -> None:
    """All supported forms, including a prefixed URL, produce one name."""
    devin_id = f"devin-{_KNOWN_ID}"
    url = f"https://app.devin.ai/sessions/{_KNOWN_ID}"
    prefixed_url = f"https://app.devin.ai/sessions/{devin_id}"
    names = {
        generate_friendly_name(extract_session_id(identifier))
        for identifier in (devin_id, _KNOWN_ID, url, prefixed_url)
    }
    assert names == {generate_friendly_name(_KNOWN_ID)}
