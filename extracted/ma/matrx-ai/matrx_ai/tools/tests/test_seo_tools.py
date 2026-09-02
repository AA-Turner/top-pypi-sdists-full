"""SEO tool test suite with assertion-based validation.

Run:
    python -m ai.tools.tests.test_seo_tools

Change the RUN variable at the bottom to pick which test to execute.
Each test case is defined as data — add new rows to the lists below
to expand coverage without touching any logic.

Exit codes: 0 = all pass, 1 = at least one failure.
"""

from __future__ import annotations

import asyncio
import json
import sys
from dataclasses import dataclass, field
from typing import Any

from matrx_utils import cleanup_async_resources, clear_terminal

from matrx_ai._ext import get_ext
from matrx_ai.tools.implementations.seo import (
    seo_check_meta_descriptions,
    seo_check_meta_tags_batch,
    seo_check_meta_titles,
)

create_test_app_context = get_ext("create_test_app_context")
create_test_tool_context = get_ext("create_test_tool_context")
initialize = get_ext("initialize")

initialize()
_ctx_token = create_test_app_context(is_admin=False)


# ============================================================================
# Colors / formatting
# ============================================================================

_GREEN = "\033[92m"
_RED = "\033[91m"
_YELLOW = "\033[93m"
_CYAN = "\033[96m"
_DIM = "\033[2m"
_BOLD = "\033[1m"
_RESET = "\033[0m"


def _pass(msg: str) -> str:
    return f"{_GREEN}PASS{_RESET} {msg}"


def _fail(msg: str) -> str:
    return f"{_RED}FAIL{_RESET} {msg}"


def _section(title: str) -> None:
    print()
    print(f"{_CYAN}{'═' * 80}{_RESET}")
    print(f"{_CYAN}  {title}{_RESET}")
    print(f"{_CYAN}{'═' * 80}{_RESET}")


def _subsection(title: str) -> None:
    print(f"\n{_YELLOW}  ── {title} ──{_RESET}")


# ============================================================================
# Test-case data classes
# ============================================================================


@dataclass
class TitleTestCase:
    """One title with expected outcomes. Add rows to TITLE_CASES below."""

    title: str
    label: str = ""
    expect_title_ok: bool | None = None
    expect_seo_length_ok: bool | None = None
    expect_desktop_ok: bool | None = None
    expect_mobile_ok: bool | None = None
    expect_too_short: bool | None = None
    expect_has_issues: bool | None = None
    expect_pixel_range: tuple[int, int] | None = None  # (min, max) inclusive


@dataclass
class DescriptionTestCase:
    """One description with expected outcomes."""

    description: str
    label: str = ""
    expect_description_ok: bool | None = None
    expect_seo_length_ok: bool | None = None
    expect_desktop_ok: bool | None = None
    expect_mobile_ok: bool | None = None
    expect_too_short: bool | None = None
    expect_has_issues: bool | None = None
    expect_pixel_range: tuple[int, int] | None = None


@dataclass
class BatchTestCase:
    """One batch item with expected outcomes."""

    title: str
    description: str
    label: str = ""
    expect_title_ok: bool | None = None
    expect_description_ok: bool | None = None
    expect_overall_ok: bool | None = None


@dataclass
class ValidationTestCase:
    """Input expected to trigger validation error."""

    tool: str  # "titles" | "descriptions" | "batch"
    args: dict[str, Any] = field(default_factory=dict)
    label: str = ""
    expect_success: bool = False
    expect_error_type: str | None = "validation"


# ============================================================================
# TEST DATA — edit these lists to add or change test cases
# ============================================================================

TITLE_CASES: list[TitleTestCase] = [
    # ── Good titles ──────────────────────────────────────────────────────
    TitleTestCase(
        label="standard good title",
        title="Best Python Frameworks 2026 - Complete Guide",
        expect_title_ok=True,
        expect_seo_length_ok=True,
        expect_desktop_ok=True,
        expect_mobile_ok=True,
        expect_too_short=False,
        expect_has_issues=False,
    ),
    TitleTestCase(
        label="15-char minimum boundary (exactly 15)",
        title="Fifteen Chars!?",
        expect_seo_length_ok=True,
        expect_too_short=False,
    ),
    TitleTestCase(
        label="60-char maximum boundary (exactly 60)",
        title="This Title Has Exactly Sixty Characters If You Count Them!!!",
        expect_seo_length_ok=True,
    ),
    # ── Too short ────────────────────────────────────────────────────────
    TitleTestCase(
        label="single char",
        title="A",
        expect_title_ok=False,
        expect_too_short=True,
        expect_seo_length_ok=False,
        expect_has_issues=True,
    ),
    TitleTestCase(
        label="5-char title",
        title="Short",
        expect_title_ok=False,
        expect_too_short=True,
        expect_seo_length_ok=False,
    ),
    TitleTestCase(
        label="14-char (one below minimum)",
        title="Fourteen Char!",
        expect_too_short=True,
        expect_seo_length_ok=False,
    ),
    TitleTestCase(
        label="empty string",
        title="",
        expect_title_ok=False,
        expect_too_short=True,
        expect_has_issues=True,
    ),
    TitleTestCase(
        label="whitespace only",
        title="   ",
        expect_title_ok=False,
        expect_too_short=True,
    ),
    # ── Too long ─────────────────────────────────────────────────────────
    TitleTestCase(
        label="61-char (one over max)",
        title="This Title Has Sixty-One Characters If You Count Carefully!!!",
        expect_seo_length_ok=False,
    ),
    TitleTestCase(
        label="extremely long title",
        title="This is an extremely long title that probably exceeds the recommended character limit for search engine optimization and will get truncated in search results pages",
        expect_title_ok=False,
        expect_seo_length_ok=False,
        expect_desktop_ok=False,
        expect_mobile_ok=False,
        expect_has_issues=True,
    ),
    # ── Pixel edge cases ─────────────────────────────────────────────────
    TitleTestCase(
        label="60 wide 'A' chars (within char limit, exceeds pixel)",
        title="A" * 60,
        expect_seo_length_ok=True,
        expect_desktop_ok=False,
        expect_mobile_ok=False,
        expect_title_ok=False,
    ),
    TitleTestCase(
        label="120 narrow 'i' chars (exceeds char limit, borderline pixels)",
        title="i" * 120,
        expect_seo_length_ok=False,
        expect_desktop_ok=True,
        expect_title_ok=False,
    ),
    TitleTestCase(
        label="all wide 'W' chars x30 (within char limit, exceeds mobile pixel only)",
        title="W" * 30,
        expect_seo_length_ok=True,
        expect_desktop_ok=True,
        expect_mobile_ok=False,
        expect_title_ok=False,
        expect_pixel_range=(550, 580),
    ),
    TitleTestCase(
        label="all wide 'W' chars x33 (exceeds desktop pixel limit)",
        title="W" * 33,
        expect_seo_length_ok=True,
        expect_desktop_ok=False,
        expect_mobile_ok=False,
        expect_title_ok=False,
        expect_pixel_range=(610, 640),
    ),
]

DESCRIPTION_CASES: list[DescriptionTestCase] = [
    # ── Good descriptions ────────────────────────────────────────────────
    DescriptionTestCase(
        label="standard good description",
        description="Learn about the best Python frameworks in 2026. Compare FastAPI, Django, and Flask with benchmarks.",
        expect_description_ok=True,
        expect_seo_length_ok=True,
        expect_desktop_ok=True,
        expect_mobile_ok=True,
        expect_too_short=False,
        expect_has_issues=False,
    ),
    DescriptionTestCase(
        label="69-char (one below minimum) — should be too short",
        description="This is a meta description that has exactly seventy characters in it!",
        expect_too_short=True,
        expect_seo_length_ok=False,
    ),
    DescriptionTestCase(
        label="70-char minimum boundary (exactly 70) — should pass",
        description="This is a meta description that has exactly seventy characters right!!",
        expect_too_short=False,
        expect_seo_length_ok=True,
    ),
    DescriptionTestCase(
        label="160-char maximum boundary (exactly 160)",
        description="This is a meta description that has been carefully crafted to be exactly one hundred and sixty characters, which is the maximum recommended SEO limit for meta!!",
        expect_seo_length_ok=True,
    ),
    # ── Too short ────────────────────────────────────────────────────────
    DescriptionTestCase(
        label="very short",
        description="Short.",
        expect_description_ok=False,
        expect_too_short=True,
        expect_seo_length_ok=False,
        expect_has_issues=True,
    ),
    DescriptionTestCase(
        label="empty description",
        description="",
        expect_description_ok=False,
        expect_too_short=True,
        expect_has_issues=True,
    ),
    # ── Too long ─────────────────────────────────────────────────────────
    DescriptionTestCase(
        label="over 160 chars",
        description="This is an extremely long meta description that goes well beyond the recommended one hundred and sixty character limit for SEO optimization purposes and will likely be truncated by Google in search results.",
        expect_description_ok=False,
        expect_seo_length_ok=False,
        expect_has_issues=True,
    ),
    DescriptionTestCase(
        label="175 chars (exceeds both char and pixel)",
        description="Explore the top Python web frameworks in 2026 including FastAPI, Django, Flask, and Tornado with extensive benchmarks, real-world production comparisons, and migration guides.",
        expect_description_ok=False,
        expect_seo_length_ok=False,
        expect_desktop_ok=False,
        expect_mobile_ok=False,
    ),
    # ── Pixel edge cases ─────────────────────────────────────────────────
    DescriptionTestCase(
        label="160 narrow 'i' chars (within char+pixel, narrow chars)",
        description="i" * 160,
        expect_seo_length_ok=True,
        expect_desktop_ok=True,
        expect_mobile_ok=True,
    ),
    DescriptionTestCase(
        label="160 wide 'W' chars (within char limit, huge pixel)",
        description="W" * 160,
        expect_seo_length_ok=True,
        expect_desktop_ok=False,
        expect_mobile_ok=False,
        expect_description_ok=False,
    ),
]

BATCH_CASES: list[BatchTestCase] = [
    BatchTestCase(
        label="both good",
        title="Best Python Frameworks 2026 - Complete Guide",
        description="Learn about the best Python frameworks in 2026. Compare FastAPI, Django, and Flask with benchmarks.",
        expect_title_ok=True,
        expect_description_ok=True,
        expect_overall_ok=True,
    ),
    BatchTestCase(
        label="good title, bad description",
        title="Good Title Here Yay Works",
        description="Short.",
        expect_title_ok=True,
        expect_description_ok=False,
        expect_overall_ok=False,
    ),
    BatchTestCase(
        label="bad title, good description",
        title="A",
        description="A good description that is long enough to pass the minimum length requirement for SEO optimization.",
        expect_title_ok=False,
        expect_description_ok=True,
        expect_overall_ok=False,
    ),
    BatchTestCase(
        label="both bad",
        title="X",
        description="Bad.",
        expect_title_ok=False,
        expect_description_ok=False,
        expect_overall_ok=False,
    ),
]

VALIDATION_CASES: list[ValidationTestCase] = [
    ValidationTestCase(
        label="empty titles list",
        tool="titles",
        args={"titles": []},
        expect_success=False,
        expect_error_type="validation",
    ),
    ValidationTestCase(
        label="missing titles key",
        tool="titles",
        args={},
        expect_success=False,
        expect_error_type="validation",
    ),
    ValidationTestCase(
        label="empty descriptions list",
        tool="descriptions",
        args={"descriptions": []},
        expect_success=False,
        expect_error_type="validation",
    ),
    ValidationTestCase(
        label="empty batch list",
        tool="batch",
        args={"meta_data": []},
        expect_success=False,
        expect_error_type="validation",
    ),
    ValidationTestCase(
        label="batch item missing title and description",
        tool="batch",
        args={"meta_data": [{"foo": "bar"}]},
        expect_success=False,
        expect_error_type="validation",
    ),
    ValidationTestCase(
        label="string input auto-wraps to list (should succeed)",
        tool="titles",
        args={"titles": "A single title string for testing"},
        expect_success=True,
        expect_error_type=None,
    ),
    ValidationTestCase(
        label="descriptions string input auto-wraps (should succeed)",
        tool="descriptions",
        args={
            "descriptions": "A single description string for testing purposes to meet min length"
        },
        expect_success=True,
        expect_error_type=None,
    ),
]


# ============================================================================
# Assertion engine
# ============================================================================


@dataclass
class AssertionFailure:
    field: str
    expected: Any
    actual: Any


def _check(actual: dict, field: str, expected: Any) -> AssertionFailure | None:
    if expected is None:
        return None
    val = actual.get(field)
    if val != expected:
        return AssertionFailure(field=field, expected=expected, actual=val)
    return None


def _check_range(
    actual: dict, field: str, expected_range: tuple[int, int] | None
) -> AssertionFailure | None:
    if expected_range is None:
        return None
    val = actual.get(field)
    lo, hi = expected_range
    if val is None or not (lo <= val <= hi):
        return AssertionFailure(
            field=f"{field} in [{lo}, {hi}]", expected=f"[{lo}, {hi}]", actual=val
        )
    return None


# ============================================================================
# Test runners
# ============================================================================

_pass_count = 0
_fail_count = 0


def _record(passed: bool, label: str, failures: list[AssertionFailure]) -> None:
    global _pass_count, _fail_count
    if passed:
        _pass_count += 1
        print(f"  {_pass(label)}")
    else:
        _fail_count += 1
        print(f"  {_fail(label)}")
        for f in failures:
            print(f"    {_RED}→ {f.field}: expected={f.expected!r}, got={f.actual!r}{_RESET}")


async def _run_title_tests() -> None:
    _section("META TITLE TESTS")
    ctx = create_test_tool_context("seo_check_meta_titles")

    all_titles = [tc.title for tc in TITLE_CASES]
    result = await seo_check_meta_titles({"titles": all_titles}, ctx)

    if not result.success:
        print(f"  {_RED}Tool execution failed: {result.error}{_RESET}")
        return

    content = result.to_tool_result_content()["content"]
    data = json.loads(content) if isinstance(content, str) else content
    analysis = data["title_analysis"]

    for i, tc in enumerate(TITLE_CASES):
        item = analysis[i]
        label = tc.label or f"title[{i}]"
        failures: list[AssertionFailure] = []

        for chk in [
            _check(item, "title_ok", tc.expect_title_ok),
            _check(item, "seo_length_ok", tc.expect_seo_length_ok),
            _check(item, "desktop_ok", tc.expect_desktop_ok),
            _check(item, "mobile_ok", tc.expect_mobile_ok),
            _check(item, "too_short", tc.expect_too_short),
            _check_range(item, "pixel_width", tc.expect_pixel_range),
        ]:
            if chk:
                failures.append(chk)

        if tc.expect_has_issues is not None:
            has = len(item.get("issues", [])) > 0
            if has != tc.expect_has_issues:
                failures.append(AssertionFailure("has_issues", tc.expect_has_issues, has))

        _record(len(failures) == 0, label, failures)

        if failures:
            _print_item_detail(item, "title")


async def _run_description_tests() -> None:
    _section("META DESCRIPTION TESTS")
    ctx = create_test_tool_context("seo_check_meta_descriptions")

    all_descs = [tc.description for tc in DESCRIPTION_CASES]
    result = await seo_check_meta_descriptions({"descriptions": all_descs}, ctx)

    if not result.success:
        print(f"  {_RED}Tool execution failed: {result.error}{_RESET}")
        return

    content = result.to_tool_result_content()["content"]
    data = json.loads(content) if isinstance(content, str) else content
    analysis = data["description_analysis"]

    for i, tc in enumerate(DESCRIPTION_CASES):
        item = analysis[i]
        label = tc.label or f"desc[{i}]"
        failures: list[AssertionFailure] = []

        for chk in [
            _check(item, "description_ok", tc.expect_description_ok),
            _check(item, "seo_length_ok", tc.expect_seo_length_ok),
            _check(item, "desktop_ok", tc.expect_desktop_ok),
            _check(item, "mobile_ok", tc.expect_mobile_ok),
            _check(item, "too_short", tc.expect_too_short),
            _check_range(item, "pixel_width", tc.expect_pixel_range),
        ]:
            if chk:
                failures.append(chk)

        if tc.expect_has_issues is not None:
            has = len(item.get("issues", [])) > 0
            if has != tc.expect_has_issues:
                failures.append(AssertionFailure("has_issues", tc.expect_has_issues, has))

        _record(len(failures) == 0, label, failures)

        if failures:
            _print_item_detail(item, "description")


async def _run_batch_tests() -> None:
    _section("META TAGS BATCH TESTS")
    ctx = create_test_tool_context("seo_check_meta_tags_batch")

    meta_data = [{"title": tc.title, "description": tc.description} for tc in BATCH_CASES]
    result = await seo_check_meta_tags_batch({"meta_data": meta_data}, ctx)

    if not result.success:
        print(f"  {_RED}Tool execution failed: {result.error}{_RESET}")
        return

    content = result.to_tool_result_content()["content"]
    data = json.loads(content) if isinstance(content, str) else content
    analysis = data["batch_analysis"]

    for i, tc in enumerate(BATCH_CASES):
        item = analysis[i]
        label = tc.label or f"batch[{i}]"
        failures: list[AssertionFailure] = []

        for chk in [
            _check(item, "title_ok", tc.expect_title_ok),
            _check(item, "description_ok", tc.expect_description_ok),
            _check(item, "overall_ok", tc.expect_overall_ok),
        ]:
            if chk:
                failures.append(chk)

        _record(len(failures) == 0, label, failures)


async def _run_validation_tests() -> None:
    _section("VALIDATION TESTS")

    tool_fns = {
        "titles": seo_check_meta_titles,
        "descriptions": seo_check_meta_descriptions,
        "batch": seo_check_meta_tags_batch,
    }

    for tc in VALIDATION_CASES:
        fn = tool_fns[tc.tool]
        ctx = create_test_tool_context(f"seo_{tc.tool}_validation")
        result = await fn(tc.args, ctx)

        label = tc.label or f"validation_{tc.tool}"
        failures: list[AssertionFailure] = []

        if result.success != tc.expect_success:
            failures.append(AssertionFailure("success", tc.expect_success, result.success))

        if tc.expect_error_type is not None:
            if result.error is None:
                failures.append(AssertionFailure("error_type", tc.expect_error_type, None))
            elif result.error.error_type != tc.expect_error_type:
                failures.append(
                    AssertionFailure("error_type", tc.expect_error_type, result.error.error_type)
                )
        elif tc.expect_error_type is None and tc.expect_success:
            if result.error is not None:
                failures.append(
                    AssertionFailure("error (should be None)", None, result.error.error_type)
                )

        _record(len(failures) == 0, label, failures)


def _print_item_detail(item: dict, item_type: str) -> None:
    text_key = item_type  # "title" or "description"
    ok_key = f"{item_type}_ok"
    text = item.get(text_key, "")
    display = text[:60] + "..." if len(text) > 60 else text
    print(f'    {_DIM}text: "{display}"{_RESET}')
    print(
        f"    {_DIM}chars={item.get('character_count')}  px={item.get('pixel_width')}  {ok_key}={item.get(ok_key)}  "
        f"seo_len={item.get('seo_length_ok')}  desktop={item.get('desktop_ok')}  "
        f"mobile={item.get('mobile_ok')}  too_short={item.get('too_short')}{_RESET}"
    )
    issues = item.get("issues", [])
    if issues:
        print(f"    {_DIM}issues: {issues}{_RESET}")


# ============================================================================
# Calculator-level direct tests (bypasses the tool layer)
# ============================================================================


async def _run_calculator_tests() -> None:
    _section("CALCULATOR DIRECT TESTS (matrx_scraper/meta_metrics.py)")

    from matrx_scraper.meta_metrics import (
        calculate_meta_description_metrics,
        calculate_meta_title_metrics,
        calculate_text_width,
    )

    _subsection("Text width sanity checks")

    width_cases = [
        ("empty string", "", 20, 0.0, 0.0),
        ("single space", " ", 20, 5.0, 6.0),
        ("single 'A'", "A", 20, 13.0, 14.0),
        ("single 'i'", "i", 20, 4.0, 6.0),
        ("single 'W'", "W", 20, 18.0, 19.0),
    ]
    for label, text, font_size, min_w, max_w in width_cases:
        w = calculate_text_width(text, font_size=font_size)
        ok = min_w <= w <= max_w
        failures = (
            []
            if ok
            else [AssertionFailure(f"width in [{min_w}, {max_w}]", f"[{min_w}, {max_w}]", w)]
        )
        _record(ok, f"width({label}) = {w:.1f}px", failures)

    _subsection("Title metrics consistency")

    for title_str in ["Good SEO Title Example", "", "   ", "A" * 100]:
        m = calculate_meta_title_metrics(title_str)
        label = repr(title_str[:30])
        failures = []

        expected_ok = m["desktop_ok"] and m["mobile_ok"] and m["seo_length_ok"]
        if m["title_ok"] != expected_ok:
            failures.append(
                AssertionFailure(
                    "title_ok == desktop_ok & mobile_ok & seo_length_ok",
                    expected_ok,
                    m["title_ok"],
                )
            )

        expected_count = 0 if not title_str.strip() else len(title_str)
        if m["character_count"] != expected_count:
            failures.append(
                AssertionFailure("character_count", expected_count, m["character_count"])
            )

        _record(len(failures) == 0, f"consistency({label})", failures)

    _subsection("Description metrics consistency")

    for desc_str in [
        "A good long description for testing purposes that meets the minimum requirement easily.",
        "",
        "   ",
        "X",
    ]:
        m = calculate_meta_description_metrics(desc_str)
        label = repr(desc_str[:30])
        failures = []

        expected_ok = m["desktop_ok"] and m["mobile_ok"] and m["seo_length_ok"]
        if m["description_ok"] != expected_ok:
            failures.append(
                AssertionFailure(
                    "description_ok == desktop_ok & mobile_ok & seo_length_ok",
                    expected_ok,
                    m["description_ok"],
                )
            )

        expected_count = 0 if not desc_str.strip() else len(desc_str)
        if m["character_count"] != expected_count:
            failures.append(
                AssertionFailure("character_count", expected_count, m["character_count"])
            )

        _record(len(failures) == 0, f"consistency({label})", failures)


# ============================================================================
# REAL-WORLD SAMPLE INPUTS
# ============================================================================
# Add your own dicts here. Each must have a "meta_data" key with a list of
# {"title": ..., "description": ...} objects. They get run through the batch
# tool and printed — no assertions, just inspect the output.
# ============================================================================

SAMPLES: dict[str, dict[str, Any]] = {
    "sample_1": {
        "meta_data": [
            {
                "title": "Breast Augmentation Surgery | Natural-Looking Results",
                "description": "Learn breast augmentation options, implant types, recovery time, and what to expect before surgery.",
            },
            {
                "title": "Breast Augmentation: Implants, Options & Recovery",
                "description": "Explore breast augmentation benefits, implant choices, costs, and recovery for a confident treatment plan.",
            },
            {
                "title": "Breast Augmentation Procedure | Enhance Your Shape",
                "description": "Compare breast augmentation techniques and recovery steps to choose the best approach for your goals.",
            },
            {
                "title": "Breast Augmentation Benefits, Cost & Recovery",
                "description": "Find clear guidance on breast augmentation, including implants, candidacy, and expected results.",
            },
            {
                "title": "Breast Augmentation Consultation & Treatment Guide",
                "description": "Understand breast augmentation surgery, from consultation to recovery and final results.",
            },
        ],
    },
    "sample_2": {
        "meta_data": [
            {
                "title": "Breast Augmentation Surgery | Natural-Looking Results",
                "description": "Learn about breast augmentation surgery, implant options, recovery, and expected results to help you choose the right procedure with confidence.",
            },
            {
                "title": "Breast Augmentation: Implants, Options & Recovery",
                "description": "Discover breast augmentation options, from implant types to recovery timelines, and get clear guidance for planning your procedure and results.",
            },
            {
                "title": "Breast Augmentation Procedure | Enhance Your Shape",
                "description": "Considering breast augmentation? Explore benefits, candidacy, implant choices, recovery, and what to expect before and after surgery.",
            },
            {
                "title": "Breast Augmentation Benefits, Cost & Recovery",
                "description": "Get expert insight on breast augmentation, including saline vs. silicone implants, healing time, costs, and how to achieve balanced, natural-looking results.",
            },
            {
                "title": "Breast Augmentation Consultation & Treatment Guide",
                "description": "Compare breast augmentation techniques, understand recovery, and learn how to select the best implant size and approach for your goals.",
            },
        ],
    },
}


# ============================================================================
# Sample runner — no assertions, just formatted output
# ============================================================================


async def _run_sample(name: str, sample: dict[str, Any]) -> None:
    _section(f"SAMPLE: {name}")
    ctx = create_test_tool_context("seo_check_meta_tags_batch")
    result = await seo_check_meta_tags_batch(sample, ctx)

    if not result.success:
        print(f"  {_RED}Tool error: {result.error}{_RESET}")
        return

    content = result.to_tool_result_content()["content"]
    data = json.loads(content) if isinstance(content, str) else content

    for item in data["batch_analysis"]:
        title = item["title"]
        desc = item["description"]
        t_ok = item["title_ok"]
        d_ok = item["description_ok"]
        overall = item["overall_ok"]

        t_color = _GREEN if t_ok else _RED
        d_color = _GREEN if d_ok else _RED
        o_color = _GREEN if overall else _RED

        print()
        print(f'  {_BOLD}title:{_RESET}  "{title}"')
        print(
            f"    {t_color}title_ok={t_ok}{_RESET}  chars={item['title_chars']}  px={item['title_pixels']}"
        )
        if item["title_issues"]:
            for iss in item["title_issues"]:
                print(f"    {_RED}  -> {iss}{_RESET}")

        print(f'  {_BOLD}desc:{_RESET}   "{desc[:90]}{"..." if len(desc) > 90 else ""}"')
        print(
            f"    {d_color}desc_ok={d_ok}{_RESET}  chars={item['description_chars']}  px={item['description_pixels']}"
        )
        if item["description_issues"]:
            for iss in item["description_issues"]:
                print(f"    {_RED}  -> {iss}{_RESET}")

        print(f"    {o_color}overall_ok={overall}{_RESET}")


async def _run_all_samples() -> None:
    for name, sample in SAMPLES.items():
        await _run_sample(name, sample)


# ============================================================================
# Test registry
# ============================================================================

TESTS: dict[str, Any] = {
    "all": lambda: _run_all_checked(),
    "titles": _run_title_tests,
    "descriptions": _run_description_tests,
    "batch": _run_batch_tests,
    "validation": _run_validation_tests,
    "calculator": _run_calculator_tests,
    "samples": _run_all_samples,
}

for _name, _sample in SAMPLES.items():
    TESTS[_name] = lambda s=_sample, n=_name: _run_sample(n, s)


async def _run_all_checked() -> None:
    await _run_title_tests()
    await _run_description_tests()
    await _run_batch_tests()
    await _run_validation_tests()
    await _run_calculator_tests()
    await _run_all_samples()


def _print_summary() -> None:
    total = _pass_count + _fail_count
    if total == 0:
        return
    print()
    print(f"{_BOLD}{'═' * 60}{_RESET}")
    if _fail_count == 0:
        print(f"  {_GREEN}{_BOLD}ALL {total} ASSERTIONS PASSED{_RESET}")
    else:
        print(
            f"  {_GREEN}{_pass_count} passed{_RESET}  /  {_RED}{_fail_count} failed{_RESET}  /  {total} total"
        )
    print(f"{_BOLD}{'═' * 60}{_RESET}")
    print()


# ============================================================================
# RUN CONFIG — change this to pick what runs
# ============================================================================
#
# Options:
#   "all"          — every assertion test + every sample
#   "titles"       — title assertion tests only
#   "descriptions" — description assertion tests only
#   "batch"        — batch assertion tests only
#   "validation"   — validation/error-handling tests only
#   "calculator"   — direct calculator tests only
#   "samples"      — all real-world samples (no assertions, just output)
#   "sample_1"     — a specific sample by name
#   "sample_2"     — a specific sample by name
#
# To add a new sample, just add a key to the SAMPLES dict above.
# It automatically becomes available here by its key name.

RUN = "sample_1"


async def _main() -> None:
    clear_terminal()
    fn = TESTS.get(RUN)
    if fn is None:
        print(f"{_RED}Unknown RUN value: {RUN!r}{_RESET}")
        print(f"Available: {', '.join(sorted(TESTS.keys()))}")
        return
    print(f"{_BOLD}  Running: {RUN}{_RESET}")
    await fn()
    _print_summary()


if __name__ == "__main__":
    try:
        asyncio.run(_main())
    finally:
        cleanup_async_resources()
    sys.exit(1 if _fail_count > 0 else 0)
