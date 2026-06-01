"""Unit tests for the session_namer module."""

import pytest

from airbyte_ops_mcp.session_namer import (
    NamingScheme,
    _load_seed_data,
    extract_session_id,
    generate_all_names,
    generate_friendly_name,
    get_namespace_size,
)


@pytest.mark.unit
@pytest.mark.parametrize(
    "identifier,scheme",
    [
        pytest.param("test-session-123", NamingScheme.SUPERHERO, id="superhero"),
        pytest.param("test-session-123", NamingScheme.SILLY_BUDDY, id="silly_buddy"),
        pytest.param("", NamingScheme.SUPERHERO, id="empty_string"),
        pytest.param(
            "b2a641e838214f91b50d0f88940ac119",
            NamingScheme.SUPERHERO,
            id="uuid_like",
        ),
    ],
)
def test_generate_friendly_name_deterministic(
    identifier: str, scheme: NamingScheme
) -> None:
    """Same identifier + scheme always produces the same Title Case two-word name."""
    name_a = generate_friendly_name(identifier, scheme)
    name_b = generate_friendly_name(identifier, scheme)
    assert name_a == name_b
    parts = name_a.split(" ")
    assert len(parts) == 2, f"Expected 2 words, got {len(parts)}: {name_a!r}"
    assert all(p.isalpha() for p in parts), f"Non-alpha tokens in: {name_a!r}"
    assert name_a == name_a.title(), f"Name not Title Case: {name_a!r}"


@pytest.mark.unit
@pytest.mark.parametrize(
    "id_a,id_b,scheme",
    [
        pytest.param(
            "session-alpha", "session-beta", NamingScheme.SUPERHERO, id="superhero"
        ),
        pytest.param(
            "session-alpha",
            "session-beta",
            NamingScheme.SILLY_BUDDY,
            id="silly_buddy",
        ),
    ],
)
def test_generate_friendly_name_different_ids(
    id_a: str, id_b: str, scheme: NamingScheme
) -> None:
    """Different identifiers produce different names (probabilistically)."""
    assert generate_friendly_name(id_a, scheme) != generate_friendly_name(id_b, scheme)


@pytest.mark.unit
def test_generate_all_names_matches_individual() -> None:
    """generate_all_names returns one entry per scheme, matching individual calls."""
    identifier = "consistency-check"
    all_names = generate_all_names(identifier)
    assert set(all_names.keys()) == {s.value for s in NamingScheme}
    for scheme in NamingScheme:
        assert all_names[scheme.value] == generate_friendly_name(identifier, scheme)


@pytest.mark.unit
@pytest.mark.parametrize(
    "scheme,min_size",
    [
        pytest.param(NamingScheme.SUPERHERO, 40_000, id="superhero"),
        pytest.param(NamingScheme.SILLY_BUDDY, 40_000, id="silly_buddy"),
    ],
)
def test_get_namespace_size(scheme: NamingScheme, min_size: int) -> None:
    """Each scheme has at least 40K combinations."""
    size = get_namespace_size(scheme)
    assert isinstance(size, int)
    assert size >= min_size


@pytest.mark.unit
def test_naming_scheme_members() -> None:
    """Enum has exactly the two expected members with correct string values."""
    assert NamingScheme.SUPERHERO.value == "superhero"
    assert NamingScheme.SILLY_BUDDY.value == "silly-buddy"
    assert len(NamingScheme) == 2


@pytest.mark.unit
@pytest.mark.parametrize(
    "identifier,scheme,expected_name",
    [
        pytest.param(
            "test-session-123",
            NamingScheme.SUPERHERO,
            "Teal Burglar",
            id="superhero_known",
        ),
        pytest.param(
            "test-session-123",
            NamingScheme.SILLY_BUDDY,
            "Sneaky Seymour",
            id="silly_buddy_known",
        ),
        pytest.param(
            "b2a641e838214f91b50d0f88940ac119",
            NamingScheme.SUPERHERO,
            "Hardy Paladin",
            id="superhero_uuid",
        ),
        pytest.param(
            "b2a641e838214f91b50d0f88940ac119",
            NamingScheme.SILLY_BUDDY,
            "Ratty Kate",
            id="silly_buddy_uuid",
        ),
    ],
)
def test_golden_vectors(
    identifier: str, scheme: NamingScheme, expected_name: str
) -> None:
    """Known (identifier, scheme) pairs always produce the exact expected name."""
    assert generate_friendly_name(identifier, scheme) == expected_name


@pytest.mark.unit
def test_yaml_seed_data_loads() -> None:
    """YAML seed file loads and contains expected keys with non-empty lists."""
    data = _load_seed_data()
    expected_keys = [
        "superhero_adjectives",
        "superhero_nouns",
        "silly_buddy_adjectives",
        "silly_buddy_names",
    ]
    for key in expected_keys:
        assert key in data, f"Missing key: {key}"
        assert isinstance(data[key], list), f"{key} is not a list"
        assert len(data[key]) > 100, f"{key} has too few entries: {len(data[key])}"


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
    name_from_id = generate_friendly_name(_KNOWN_ID, NamingScheme.SILLY_BUDDY)
    name_from_url = generate_friendly_name(
        extract_session_id(url), NamingScheme.SILLY_BUDDY
    )
    assert name_from_id == name_from_url == "Ratty Kate"
