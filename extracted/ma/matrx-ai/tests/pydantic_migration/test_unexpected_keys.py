"""`unexpected_keys` — the user-facing half of `_unrecognized_keys`.

`_unrecognized_keys` deliberately holds TWO populations: keys the platform does
not know, and keys in `_KNOWN_PASSTHROUGH_KEYS` that downstream code consumes on
purpose. Every user-facing consumer must subtract the second set, or it reports
honoured features as ignored.

Measured motivation: `multi_speaker` appears on 114 production runs and
`variables` on 1 — both are declared passthrough, and both were producing a
client-facing "not recognized by the server … they have been ignored" warning.
"""

from matrx_ai.config.models.unified import UnifiedConfigModel
from matrx_ai.config.unified_config import _KNOWN_PASSTHROUGH_KEYS, UnifiedConfig


REQUIRED = {"model": "gpt-4o", "messages": []}


def _dc(keys: list[str]) -> UnifiedConfig:
    config = UnifiedConfig(**REQUIRED)
    config._unrecognized_keys = list(keys)
    return config


def _pyd(keys: list[str]) -> UnifiedConfigModel:
    model = UnifiedConfigModel(**REQUIRED)
    model._unrecognized_keys = list(keys)
    return model


def test_passthrough_keys_are_not_reported_as_unexpected():
    """The forcing function: a podcast run sends multi_speaker BY DESIGN.

    Reading `_unrecognized_keys` here yields ['multi_speaker'] and the user is
    told their config was ignored. This test fails against that behaviour.
    """
    assert "multi_speaker" in _KNOWN_PASSTHROUGH_KEYS
    config = _dc(["multi_speaker"])
    assert config._unrecognized_keys == ["multi_speaker"]  # still carried, on purpose
    assert config.unexpected_keys == []  # but nothing to tell the user about


def test_genuinely_unknown_keys_still_surface():
    """A validator that cannot fire is worse than none — `image_urls` is NOT
    passthrough, and must still reach the user."""
    assert "image_urls" not in _KNOWN_PASSTHROUGH_KEYS
    assert _dc(["image_urls"]).unexpected_keys == ["image_urls"]


def test_mixed_set_reports_only_the_unknown_half():
    config = _dc(["multi_speaker", "image_urls", "variables", "presence_penalty"])
    assert config.unexpected_keys == ["image_urls", "presence_penalty"]


def test_result_is_sorted_and_deduped():
    assert _dc(["image_urls", "image_urls", "file_urls"]).unexpected_keys == [
        "file_urls",
        "image_urls",
    ]


def test_empty_stays_empty():
    assert _dc([]).unexpected_keys == []


def test_direct_construction_initializes_unrecognized_keys():
    """Conversation execution constructs UnifiedConfig directly, then reads
    ``unexpected_keys``. That exact production path must never depend on
    ``from_dict`` having attached a private attribute first.
    """
    config = UnifiedConfig(**REQUIRED)

    assert config._unrecognized_keys == []
    assert config.unexpected_keys == []
    assert "_unrecognized_keys" not in config.to_dict()


def test_unexpected_keys_tolerates_pre_fix_restored_instance():
    """A legacy/in-flight object without the transient attribute fails soft."""
    config = UnifiedConfig(**REQUIRED)
    del config._unrecognized_keys

    assert config.unexpected_keys == []


def test_twin_matches_the_dataclass_exactly():
    """Parity: the twin must not diverge on the field it had to special-case."""
    for keys in (
        [],
        ["multi_speaker"],
        ["image_urls"],
        ["multi_speaker", "image_urls", "variables", "presence_penalty"],
        ["file_urls", "image_urls", "image_urls"],
    ):
        assert _dc(keys).unexpected_keys == _pyd(keys).unexpected_keys, keys


def test_unexpected_keys_is_not_persisted():
    """`to_dict` must still emit `_unrecognized_keys` and NOT the derived view —
    4,178 stored rows carry the former; adding a second key would change the
    persisted shape."""
    model = _pyd(["multi_speaker", "image_urls"])
    out = model.to_dict()
    assert out["_unrecognized_keys"] == ["multi_speaker", "image_urls"]
    assert "unexpected_keys" not in out
