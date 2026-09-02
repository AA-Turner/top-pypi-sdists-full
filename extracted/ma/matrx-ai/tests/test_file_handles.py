"""Tests for the agent file-handles primitive (matrx_ai.media.file_handles).

No network, no provider SDKs — the primitive is pure functions.
Spec: common-docs/projects/agent-file-handles/PLAN.md §2 + §4,
adjustments a/b/d from ebay-store-management/REVIEW-RESPONSE.md §3-L.
"""

from __future__ import annotations

import pytest

from matrx_ai.media.file_handles import (
    HANDLE_ALPHABET,
    HandleMap,
    OrdinalError,
    ReconcileSpec,
    UnknownHandleError,
    generate_handle,
    inject_file_handles,
    resolve_file_handles,
)

FILES = [
    ("file-aaa", {"type": "image", "source": {"type": "base64", "data": "AAA="}}),
    ("file-bbb", {"type": "image", "source": {"type": "base64", "data": "BBB="}}),
    ("file-ccc", {"type": "image", "source": {"type": "base64", "data": "CCC="}}),
]
HANDLES = ["IMG-AAAA", "IMG-BBBB", "IMG-CCCC"]


def _inject(provider="anthropic"):
    return inject_file_handles(FILES, provider=provider, handles=HANDLES)


# ── injection: interleaving + map, all three provider shapes ──


@pytest.mark.parametrize(
    ("provider", "text_key", "extra"),
    [
        ("anthropic", "text", {"type": "text"}),
        ("openai", "text", {"type": "text"}),
        ("gemini", "text", {}),
    ],
)
def test_injection_interleaves_label_immediately_before_each_file(provider, text_key, extra):
    result = _inject(provider)
    parts = result.content_parts
    assert len(parts) == 6  # label, media, label, media, label, media
    for i, (file_ref, media_part) in enumerate(FILES):
        label_part, got_media = parts[2 * i], parts[2 * i + 1]
        assert got_media is media_part  # transport part passed through untouched
        assert label_part[text_key] == f"Image {i + 1} [{HANDLES[i]}]:"
        for k, v in extra.items():
            assert label_part[k] == v
    assert result.handle_map.by_handle == {h: f for h, (f, _) in zip(HANDLES, FILES)}
    assert result.handle_map.ordered_handles == tuple(HANDLES)


def test_generated_token_alphabet_excludes_confusables():
    for ch in "0O1Il":
        assert ch not in HANDLE_ALPHABET
    for _ in range(500):
        h = generate_handle()
        assert h.startswith("IMG-")
        assert all(c in HANDLE_ALPHABET for c in h[4:])


# ── resolution: round trip, raise, DEGRADED ──


def test_round_trip_resolve_replaces_handles_with_file_refs():
    hm = _inject().handle_map
    result = {
        "best_image": "IMG-BBBB",
        "products": [
            {"images": ["IMG-AAAA", "IMG-BBBB"]},
            {"images": ["IMG-CCCC"]},
        ],
    }
    resolved, report = resolve_file_handles(
        result,
        hm,
        [ReconcileSpec("best_image"), ReconcileSpec("products.*.images.*")],
    )
    assert resolved["best_image"] == "file-bbb"
    assert resolved["products"][0]["images"] == ["file-aaa", "file-bbb"]
    assert resolved["products"][1]["images"] == ["file-ccc"]
    assert result["best_image"] == "IMG-BBBB"  # input not mutated
    assert not report.is_degraded
    assert report.agreement == "token_only"  # no ordinals supplied


def test_corrupted_handle_raises_loudly_naming_handle_and_path():
    hm = _inject().handle_map
    with pytest.raises(UnknownHandleError) as exc:
        resolve_file_handles({"best_image": "IMG-ZZZZ"}, hm, [ReconcileSpec("best_image")])
    assert exc.value.handle == "IMG-ZZZZ"
    assert exc.value.field_path == "best_image"
    assert "IMG-ZZZZ" in str(exc.value)
    assert "mandate failure" in str(exc.value)


def test_missing_required_reference_is_degraded_not_a_raise_not_a_pass():
    hm = _inject().handle_map
    result = {
        "products": [
            {"name": "a", "hero": "IMG-AAAA"},
            {"name": "b"},  # required hero missing entirely
            {"name": "c", "hero": None},  # present but null
        ]
    }
    resolved, report = resolve_file_handles(
        result, hm, [ReconcileSpec("products.*.hero", required=True)]
    )
    assert resolved["products"][0]["hero"] == "file-aaa"
    assert report.is_degraded
    paths = {d.field_path for d in report.degraded}
    assert paths == {"products[1].hero", "products[2].hero"}


def test_required_top_level_field_absent_is_degraded():
    hm = _inject().handle_map
    _, report = resolve_file_handles({}, hm, [ReconcileSpec("best_image", required=True)])
    assert [d.field_path for d in report.degraded] == ["best_image"]


# ── rule 4: ordinal↔token reconciliation ──


def test_ordinal_token_agreement_recorded_full():
    hm = _inject().handle_map
    result = {"picks": [{"handle": "IMG-AAAA", "position": 1}, {"handle": "IMG-CCCC", "position": 3}]}
    _, report = resolve_file_handles(
        result, hm, [ReconcileSpec("picks.*.handle", ordinal_path="picks.*.position")]
    )
    assert report.agreement == "full"
    assert all(e.agreement == "agree" for e in report.entries)


def test_ordinal_token_disagreement_detected_and_recorded():
    hm = _inject().handle_map
    result = {"picks": [{"handle": "IMG-AAAA", "position": 2}, {"handle": "IMG-BBBB", "position": 2}]}
    _, report = resolve_file_handles(
        result, hm, [ReconcileSpec("picks.*.handle", ordinal_path="picks.*.position")]
    )
    assert report.agreement == "partial"  # one disagrees (AAAA is #1), one agrees
    by_handle = {e.handle: e for e in report.entries}
    assert by_handle["IMG-AAAA"].agreement == "disagree"
    assert by_handle["IMG-AAAA"].issued_ordinal == 1
    assert by_handle["IMG-AAAA"].claimed_ordinal == 2
    assert by_handle["IMG-BBBB"].agreement == "agree"


def test_ordinal_out_of_range_is_a_failure():
    hm = _inject().handle_map
    with pytest.raises(OrdinalError):
        resolve_file_handles(
            {"picks": [{"handle": "IMG-AAAA", "position": 7}]},
            hm,
            [ReconcileSpec("picks.*.handle", ordinal_path="picks.*.position")],
        )


def test_duplicate_ordinal_where_forbidden_is_a_failure():
    hm = _inject().handle_map
    result = {"picks": [{"handle": "IMG-AAAA", "position": 1}, {"handle": "IMG-BBBB", "position": 1}]}
    with pytest.raises(OrdinalError) as exc:
        resolve_file_handles(
            result,
            hm,
            [
                ReconcileSpec(
                    "picks.*.handle",
                    ordinal_path="picks.*.position",
                    forbid_duplicate_ordinals=True,
                )
            ],
        )
    assert "duplicated" in str(exc.value)


def test_non_integer_ordinal_is_a_failure():
    hm = _inject().handle_map
    with pytest.raises(OrdinalError):
        resolve_file_handles(
            {"picks": [{"handle": "IMG-AAAA", "position": "one"}]},
            hm,
            [ReconcileSpec("picks.*.handle", ordinal_path="picks.*.position")],
        )


# ── misc contract ──


def test_unknown_provider_rejected():
    with pytest.raises(ValueError):
        inject_file_handles(FILES, provider="mystery")


def test_handle_map_direct_lookup_raises_on_unknown():
    hm = HandleMap(by_handle={"IMG-AAAA": "f"}, ordered_handles=("IMG-AAAA",))
    with pytest.raises(UnknownHandleError):
        hm.file_ref("IMG-QQQQ", "somewhere")
