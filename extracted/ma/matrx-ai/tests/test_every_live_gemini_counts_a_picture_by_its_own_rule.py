"""Every live Gemini counts a picture by its OWN rule — the estimate and the wire agree (CGU-10 IMG8 #1/#6).

Live (IMG8): a 300² picture on gemini-3.5-flash was estimated 258 and billed 1,089 — the vision class
was a prefix list (``gemini-3-pro`` / ``gemini-3-flash``) and every later name (3.1, 3.5–3.8, 4,
``*-latest``) fell to the 2.5 class. Measured with ``countTokens`` on every live picture-reading Gemini
(2026-11-11, a 1,536² picture at the model's default resolution):

* a text-making Gemini 3+ (or an un-numbered current one) counts by media resolution — 1,089
  (gemini-4-argon 1,120) — and takes a per-picture ``mediaResolution``;
* Gemini 2.x and a picture/video-MAKING Gemini of any generation count a flat 258 and refuse a
  per-picture ``mediaResolution`` with a 400 (so the translator must remove it).

``LIVE_GEMINI`` is the catalog as read 2026-11-11 (``ai.model_definition``: name, ``capabilities.output``;
available offering) with the count Google returned. The class each lands in is decided from the catalog
facts (generation + outputs), never a name list — the synthetic names below prove a new release lands
right with no code change.

What each test is FOR (each seen red under its plant):
* restore the prefix list → 3.1/3.5–3.8/4/latest/robotics land in the flat class;
* classify by version only (ignore outputs) → the image/omni makers land in the resolution class;
* restore the 768-tile rule → a 1,536² picture on 2.5 counts 1,032, not 258;
* restore the translator's own regex → a 3.x picture maker keeps ``mediaResolution`` (a live 400).

Opt-in live walk: ``MATRX_LIVE_GEMINI=1`` with ``GEMINI_API_KEY`` re-measures every row (free
``countTokens``) and fails when Google's count no longer matches the class.
"""

from __future__ import annotations

import os
from typing import Any

import pytest
from dotenv import load_dotenv

from matrx_ai.catalog.manager import AiCatalogManager

# Resolve the opt-in gate identically when this file is collected alone or in the host suite.
load_dotenv()

# name -> (catalog outputs, Google's countTokens for one 1,536² picture at the default resolution)
LIVE_GEMINI: dict[str, tuple[tuple[str, ...], int]] = {
    "gemini-2.5-flash": (("text",), 258),
    "gemini-2.5-pro": (("text",), 258),
    "gemini-2.5-flash-image": (("image", "text"), 258),
    "gemini-3-flash-preview": (("text",), 1_089),
    "gemini-3-pro-image": (("image", "text"), 258),
    "gemini-3.1-flash-image": (("image", "text"), 258),
    "gemini-3.1-flash-lite": (("text",), 1_089),
    "gemini-3.1-flash-lite-image": (("text", "image"), 258),
    "gemini-3.1-pro-preview": (("text",), 1_089),
    "gemini-3.5-flash": (("text",), 1_089),
    "gemini-3.5-flash-lite": (("text",), 1_089),
    "gemini-3.6-flash": (("text",), 1_089),
    "gemini-3.7-flash": (("text",), 1_089),
    "gemini-3.8-flash": (("text",), 1_089),
    "gemini-4-argon": (("text",), 1_120),
    "gemini-flash-latest": (("text",), 1_089),
    "gemini-flash-lite-latest": (("text",), 1_089),
    "gemini-pro-latest": (("text",), 1_089),
    "gemini-nano-banana-2.1": (("image", "text"), 258),
    "gemini-omni-1.1-flash": (("video",), 258),
    "gemini-omni-flash-preview": (("video",), 258),
    "gemini-robotics-er-2-preview": (("text",), 1_089),
    "gemini-3-pro-image-preview": (("image", "text"), 258),  # deprecated, still offered (AND-IMG11)
    "gemini-3.1-flash-image-preview": (("image", "text"), 258),
}
FLAT = 258


@pytest.fixture
def live_catalog(monkeypatch: pytest.MonkeyPatch) -> AiCatalogManager:
    catalog = AiCatalogManager()
    catalog.load_from_rows(
        endpoints=[],
        apis=[],
        offerings=[],
        settings=[],
        providers={},
        models=[
            {"id": f"id-{name}", "name": name, "is_deprecated": False,
             "capabilities": {"input": ["text", "image"], "output": list(outputs)}}
            for name, (outputs, _count) in LIVE_GEMINI.items()
        ],
        aliases=[],
    )
    monkeypatch.setattr("matrx_ai.catalog.manager.ai_catalog_manager", catalog)
    return catalog


def _estimate(name: str) -> int:
    from matrx_ai.processing.vision.image_tokens import image_tokens
    from matrx_ai.processing.vision.vision_classes import resolve_vision_class

    return image_tokens(1536, 1536, resolve_vision_class(name, "google_chat"), name)


@pytest.mark.parametrize("name", sorted(LIVE_GEMINI))
def test_every_live_gemini_lands_in_the_class_google_counts_it_by(name: str, live_catalog: Any) -> None:
    from matrx_ai.processing.vision.vision_classes import gemini_reads_by_resolution, resolve_vision_class

    measured = LIVE_GEMINI[name][1]
    cls = resolve_vision_class(name, "google_chat")
    estimate = _estimate(name)
    if measured == FLAT:
        assert not cls.name.startswith("gemini3"), f"{name} counts a flat 258 but resolves to {cls.name}"
        assert estimate == FLAT, f"{name}: estimated {estimate}, Google counts {measured}"
        assert gemini_reads_by_resolution(name) is False, f"{name} refuses a per-picture resolution"
    else:
        assert cls.name.startswith("gemini3"), f"{name} counts {measured} but resolves to {cls.name}"
        # Never under (an under-count promises a fit the provider refuses); at most the published budget.
        assert measured <= estimate <= 1_120, f"{name}: estimated {estimate}, Google counts {measured}"
        assert gemini_reads_by_resolution(name) is True


@pytest.mark.parametrize(
    ("name", "outputs", "by_resolution"),
    [
        ("gemini-5-flash", ("text",), True),  # a later generation needs no code change
        ("gemini-3.9-pro-preview", ("text",), True),
        ("gemini-3.10-flash", ("text",), True),
        ("gemini-ultra-latest", ("text",), True),  # an un-numbered current name
        ("gemini-4.2-flash-image", ("image", "text"), False),  # a picture maker of any generation
        ("gemini-2.0-flash", ("text",), False),
        ("models/gemini-3.5-flash", ("text",), True),  # the API's own spelling
    ],
)
def test_a_new_gemini_release_lands_right_with_no_code_change(
    name: str, outputs: tuple[str, ...], by_resolution: bool, monkeypatch: pytest.MonkeyPatch
) -> None:
    from matrx_ai.processing.vision.vision_classes import gemini_reads_by_resolution

    catalog = AiCatalogManager()
    bare = name.removeprefix("models/")
    catalog.load_from_rows(
        endpoints=[], apis=[], offerings=[], settings=[], providers={}, aliases=[],
        models=[{"id": "x", "name": bare, "capabilities": {"input": ["image"], "output": list(outputs)}}],
    )
    monkeypatch.setattr("matrx_ai.catalog.manager.ai_catalog_manager", catalog)
    assert gemini_reads_by_resolution(name) is by_resolution


def test_a_latest_alias_resolves_through_the_catalog(monkeypatch: pytest.MonkeyPatch) -> None:
    """An ``ai.model_alias`` row is followed to its model before the generation is read."""
    from matrx_ai.processing.vision.vision_classes import gemini_major_version

    catalog = AiCatalogManager()
    catalog.load_from_rows(
        endpoints=[], apis=[], offerings=[], settings=[], providers={},
        models=[{"id": "m1", "name": "gemini-3.8-live", "capabilities": {"output": ["text", "audio"]}}],
        aliases=[{"id": "a1", "alias": "gemini-live-latest", "model_id": "m1"}],
    )
    monkeypatch.setattr("matrx_ai.catalog.manager.ai_catalog_manager", catalog)
    assert gemini_major_version("gemini-live-latest") == 3


@pytest.mark.parametrize("name", sorted(LIVE_GEMINI))
def test_the_wire_keeps_a_per_picture_resolution_only_where_google_takes_it(name: str, live_catalog: Any) -> None:
    from matrx_ai.providers.google.translator import _drop_part_resolution_before_gemini_3

    contents = [{"role": "user", "parts": [{"inlineData": {}, "mediaResolution": {"level": "MEDIA_RESOLUTION_LOW"}}]}]
    _drop_part_resolution_before_gemini_3(contents, name)
    kept = "mediaResolution" in contents[0]["parts"][0]
    assert kept is (LIVE_GEMINI[name][1] != FLAT), f"{name}: resolution kept={kept} (Google 400s it when flat)"


# ── CGU-10 IMG9 #6: a WALK of the loaded catalog, never only this table ─────────────────────────────
#: Socket-only rows (Live API) as the catalog holds them: countTokens refuses them, so they are classed
#: by the rule from their own facts and listed as inferred (``gemini_picture_walk`` documents why).
SOCKET_ONLY_ROWS = {
    "gemini-3.8-live": ("text", "audio"),
    "gemini-3.8-live-extended-thinking": ("text", "audio"),
    "gemini-robotics-er-2-streaming-preview": ("text",),
}


#: Measured rows the rule does NOT yet class right — each is an open finding the walk reports. Empty since
#: AND-IMG11 gave the 2.x computer-use Gemini its tiled class.
KNOWN_MISCLASSED: set[str] = set()
#: Rows measured with a rule of their own (not flat, not by resolution) — the tiling Gemini.
TILED_ROWS = {"gemini-2.5-computer-use-preview-10-2025": (("text",), ("computer_use", "function_calling"))}


def test_the_measured_table_is_the_walks_own() -> None:
    from matrx_ai.processing.vision.gemini_picture_walk import MEASURED

    assert {name: count for name, (_o, count) in LIVE_GEMINI.items()} == {
        n: c for n, c in MEASURED.items() if n not in KNOWN_MISCLASSED and n not in TILED_ROWS
    }


# ── CGU-10 AND-IMG11: the 2.x computer-use Gemini TILES a picture ───────────────────────────────────
def _tiled_catalog(monkeypatch: pytest.MonkeyPatch, rows: dict[str, tuple[tuple[str, ...], tuple[str, ...]]]) -> None:
    catalog = AiCatalogManager()
    catalog.load_from_rows(
        endpoints=[], apis=[], offerings=[], settings=[], providers={}, aliases=[],
        models=[
            {"id": f"id-{n}", "name": n, "is_deprecated": False,
             "capabilities": {"input": ["text", "image"], "output": list(o), "features": list(f)}}
            for n, (o, f) in rows.items()
        ],
    )
    monkeypatch.setattr("matrx_ai.catalog.manager.ai_catalog_manager", catalog)


def _tiled_cases() -> list[tuple[str, int, int, int]]:
    from matrx_ai.processing.vision.gemini_picture_walk import TILED_MEASURED

    return [(n, w, h, c) for n, sizes in TILED_MEASURED.items() for (w, h), c in sizes.items()]


@pytest.mark.parametrize(("name", "width", "height", "measured"), _tiled_cases())
def test_the_tiled_rule_reproduces_every_size_google_counted(
    name: str, width: int, height: int, measured: int
) -> None:
    """The fitted rule against every ``countTokens`` measurement — exact, not "close"."""
    from matrx_ai.processing.vision.image_tokens import _gemini_tiled_tokens

    assert _gemini_tiled_tokens(width, height) == measured, f"{name} {width}x{height}: Google counts {measured}"


@pytest.mark.parametrize(("width", "height"), [(1920, 1080), (1536, 1536), (385, 385), (300, 100)])
def test_a_computer_use_screenshot_is_estimated_as_google_counts_it(
    width: int, height: int, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The full path (class from the catalog, re-encode fit, count) on the as-sent picture."""
    from matrx_ai.processing.vision.gemini_picture_walk import TILED_MEASURED
    from matrx_ai.processing.vision.image_tokens import image_tokens
    from matrx_ai.processing.vision.vision_classes import resolve_vision_class

    _tiled_catalog(monkeypatch, TILED_ROWS)
    name = "gemini-2.5-computer-use-preview-10-2025"
    cls = resolve_vision_class(name, "google_chat")
    assert cls.name == "gemini25_tiled"
    assert image_tokens(width, height, cls, name) == TILED_MEASURED[name][(width, height)]


@pytest.mark.parametrize(
    ("name", "outputs", "features", "expected"),
    [
        # decided by the catalog's facts, not the name: a renamed 2.x computer-use row tiles …
        ("gemini-2.5-screen-agent", ("text",), ("computer_use",), "gemini25_tiled"),
        # … the measured name WITHOUT the fact does not (the catalog wins over the name words) …
        ("gemini-2.5-computer-use-preview-10-2025", ("text",), ("function_calling",), "gemini25_default"),
        # … a 2.x without it stays flat, and a Gemini 3+ with it still counts by resolution (measured:
        # 3.5-flash-lite, 3.8-flash and robotics-er-2 all carry computer_use and count 1,089) …
        ("gemini-2.5-flash", ("text",), ("function_calling",), "gemini25_default"),
        ("gemini-3.5-flash-lite", ("text",), ("computer_use", "thinking"), "gemini3_high"),
        ("gemini-robotics-er-2-preview", ("text",), ("computer_use",), "gemini3_high"),
        # … and a picture maker never tiles.
        ("gemini-2.5-flash-image", ("image", "text"), ("computer_use",), "gemini_media_maker"),
    ],
)
def test_the_tiled_class_is_decided_from_the_catalog(
    name: str, outputs: tuple[str, ...], features: tuple[str, ...], expected: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    from matrx_ai.processing.vision.vision_classes import resolve_vision_class

    _tiled_catalog(monkeypatch, {name: (outputs, features)})
    assert resolve_vision_class(name, "google_chat").name == expected


def test_with_no_catalog_the_computer_use_gemini_still_tiles(no_catalog: None) -> None:
    """Under-counting a screenshot 7x is the dangerous side: with no catalog the name's own words decide."""
    from matrx_ai.processing.vision.image_tokens import image_tokens
    from matrx_ai.processing.vision.vision_classes import resolve_vision_class

    name = "gemini-2.5-computer-use-preview-10-2025"
    assert image_tokens(1920, 1080, resolve_vision_class(name, "google_chat"), name) == 1_806


def test_the_tiled_gemini_never_gets_a_per_picture_resolution(monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_ai.providers.google.translator import _drop_part_resolution_before_gemini_3

    _tiled_catalog(monkeypatch, TILED_ROWS)
    contents = [{"role": "user", "parts": [{"inlineData": {}, "mediaResolution": {"level": "MEDIA_RESOLUTION_LOW"}}]}]
    _drop_part_resolution_before_gemini_3(contents, "gemini-2.5-computer-use-preview-10-2025")
    assert "mediaResolution" not in contents[0]["parts"][0]


def test_the_walk_checks_the_tiled_computer_use_model(monkeypatch: pytest.MonkeyPatch) -> None:
    """Clean with its real catalog facts; a finding the moment the class is lost (the row drops its
    ``computer_use`` feature → flat 258 against Google's 1,290)."""
    from matrx_ai.processing.vision.gemini_picture_walk import walk_findings

    name = "gemini-2.5-computer-use-preview-10-2025"
    findings, _ = walk_findings(_walk_catalog(monkeypatch, {}, features={name: ("computer_use",)}, extra_names={name: ("text",)}))
    assert not findings, findings
    findings, _ = walk_findings(_walk_catalog(monkeypatch, {}, features={name: ("function_calling",)}, extra_names={name: ("text",)}))
    assert any(f.startswith(f"{name}: Google counts 1290") for f in findings), findings


def _walk_catalog(
    monkeypatch: pytest.MonkeyPatch,
    extra: dict[str, tuple[str, ...]],
    *,
    features: dict[str, tuple[str, ...]] | None = None,
    extra_names: dict[str, tuple[str, ...]] | None = None,
) -> AiCatalogManager:
    catalog = AiCatalogManager()
    rows = {**{n: o for n, (o, _c) in LIVE_GEMINI.items()}, **SOCKET_ONLY_ROWS, **extra, **(extra_names or {})}
    features = features or {}
    catalog.load_from_rows(
        endpoints=[], apis=[], offerings=[], settings=[], providers={}, aliases=[],
        models=[
            {"id": f"id-{n}", "name": n, "is_deprecated": False,
             "capabilities": {"input": ["text", "image"], "output": list(o), "features": list(features.get(n, ()))}}
            for n, o in rows.items()
        ]
        + [  # never walked: deprecated, embedding-only, no picture input, not a Gemini
            {"id": "d", "name": "gemini-2.0-flash-old", "is_deprecated": True,
             "capabilities": {"input": ["image"], "output": ["text"]}},
            {"id": "e", "name": "gemini-embedding-2", "capabilities": {"input": ["image"], "output": ["embedding"]}},
            {"id": "t", "name": "gemini-2.5-flash-preview-tts", "capabilities": {"input": ["text"], "output": ["audio"]}},
            {"id": "c", "name": "claude-x", "capabilities": {"input": ["image"], "output": ["text"]}},
        ],
    )
    monkeypatch.setattr("matrx_ai.catalog.manager.ai_catalog_manager", catalog)
    return catalog


def test_the_walk_checks_every_picture_reading_gemini_in_the_catalog(monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_ai.processing.vision.gemini_picture_walk import walk_findings

    findings, notes = walk_findings(_walk_catalog(monkeypatch, {}))
    assert not findings, "\n".join(findings)
    assert set(notes) == set(SOCKET_ONLY_ROWS), notes
    assert all("gemini3_high" in note for note in notes.values()), notes


def test_a_deprecated_row_that_is_still_offered_is_walked() -> None:
    """Deprecated is not dead: a row a person can still run gets pictures, so it is checked; a deprecated
    row with no available offering (and a retired one) is not callable and is not walked."""
    from matrx_ai.processing.vision.gemini_picture_walk import picture_reading_geminis

    class _Catalog:
        def model_states(self) -> dict[str, dict[str, Any]]:
            caps = {"input": ["image"], "output": ["image", "text"]}
            return {
                "a": {"id": "a", "name": "gemini-9-image-preview", "is_deprecated": True, "capabilities": caps},
                "b": {"id": "b", "name": "gemini-9-gone-preview", "is_deprecated": True, "capabilities": caps},
                "c": {"id": "c", "name": "gemini-9-retired", "retired_at": "2026-11-01", "capabilities": caps},
            }

        def offerings_for(self, model_id: str) -> list[object]:
            return [object()] if model_id in {"a", "c"} else []

    assert [r["name"] for r in picture_reading_geminis(_Catalog())] == ["gemini-9-image-preview"]


def test_a_new_catalog_row_is_checked_the_day_it_appears(monkeypatch: pytest.MonkeyPatch) -> None:
    """A row the frozen table never named is a finding until someone measures it."""
    from matrx_ai.processing.vision.gemini_picture_walk import walk_findings

    findings, _notes = walk_findings(_walk_catalog(monkeypatch, {"gemini-3.9-flash-image": ("image", "text")}))
    assert any("gemini-3.9-flash-image" in f and "nobody measured" in f for f in findings), findings


def test_the_walk_sees_a_measured_row_the_rule_misclasses(monkeypatch: pytest.MonkeyPatch) -> None:
    """A maker whose catalog row lost its picture output is classed by resolution: Google counts 258."""
    from matrx_ai.processing.vision.gemini_picture_walk import walk_findings

    findings, _ = walk_findings(_walk_catalog(monkeypatch, {"gemini-3.1-flash-lite-image": ("text",)}))
    assert any(f.startswith("gemini-3.1-flash-lite-image:") for f in findings), findings


# ── CGU-10 IMG9 #5: with NO catalog, a picture maker is still flat and never gets mediaResolution ────
NO_CATALOG_MAKERS = (
    "gemini-3-pro-image",
    "gemini-3.1-flash-image",
    "gemini-3.1-flash-lite-image",
    "gemini-nano-banana-2.1",
    "gemini-omni-1.1-flash",
    "gemini-omni-flash-preview",
    "gemini-2.5-flash-image",
)


@pytest.fixture
def no_catalog(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("matrx_ai.processing.vision.vision_classes._catalog", lambda: None)


@pytest.mark.parametrize("name", NO_CATALOG_MAKERS)
def test_with_no_catalog_a_picture_maker_counts_flat(name: str, no_catalog: None) -> None:
    from matrx_ai.processing.vision.vision_classes import gemini_reads_by_resolution

    assert _estimate(name) == FLAT, f"{name} with no catalog: estimated {_estimate(name)}, Google counts 258"
    assert gemini_reads_by_resolution(name) is False


@pytest.mark.parametrize("name", [*NO_CATALOG_MAKERS, "gemini-3.5-flash", "gemini-flash-latest", "gemini-4-argon"])
def test_with_no_catalog_the_wire_never_sends_a_per_picture_resolution(name: str, no_catalog: None) -> None:
    """Unknown is not "supported": a 400 for the whole call is worse than the model's own resolution."""
    from matrx_ai.providers.google.translator import _drop_part_resolution_before_gemini_3

    contents = [{"role": "user", "parts": [{"inlineData": {}, "mediaResolution": {"level": "MEDIA_RESOLUTION_LOW"}}]}]
    _drop_part_resolution_before_gemini_3(contents, name)
    assert "mediaResolution" not in contents[0]["parts"][0], f"{name}: kept with no catalog to say it is taken"


@pytest.mark.parametrize("name", ["gemini-3.5-flash", "gemini-3.8-live", "gemini-pro-latest"])
def test_with_no_catalog_a_text_gemini_3_is_still_estimated_by_resolution(name: str, no_catalog: None) -> None:
    """The estimate stays on the safe (high) side for a text maker whose catalog is absent."""
    assert _estimate(name) >= 1_089


@pytest.mark.skipif(
    os.environ.get("MATRX_LIVE_GEMINI") != "1" or not os.environ.get("GEMINI_API_KEY"),
    reason="opt-in live walk (MATRX_LIVE_GEMINI=1 + GEMINI_API_KEY); free countTokens",
)
@pytest.mark.parametrize("name", sorted(LIVE_GEMINI))
def test_live_google_still_counts_each_gemini_as_pinned(name: str) -> None:
    from matrx_ai.providers.google.picture_count import measure_picture_tokens

    picture = measure_picture_tokens(name, os.environ["GEMINI_API_KEY"])
    assert picture == LIVE_GEMINI[name][1], f"{name}: Google now counts {picture} — re-measure and re-pin"
