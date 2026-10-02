import json

import httpx
import pytest
import respx

import testmu_appium
from testmu_appium import (
    DegenerateViewportCaptureError,
    ViewportCaptureError,
    ViewportResultMissError,
    ViewportResultTypeError,
    ViewportScriptPolicyError,
    ViewportScriptRuntimeError,
    ViewportScriptTimeoutError,
    ViewportSelectionDriftError,
    _config,
)
from testmu_appium._helpers import textual_analyzer as _textual_analyzer_module
from testmu_appium.perception import parse_tree
from testmu_appium._step import current_step, step

_PRODUCTS_XML = """
<hierarchy rotation="0">
  <node class="android.widget.LinearLayout" bounds="[0,0][1080,2340]">
    <node class="android.widget.TextView" resource-id="product-price-1" text="$999.00" bounds="[0,100][400,200]" />
    <node class="android.widget.TextView" resource-id="product-price-2" text="$999.00" bounds="[0,300][400,400]" />
  </node>
</hierarchy>
"""


class _Driver:
    page_source = _PRODUCTS_XML

    def get_window_size(self):
        return {"width": 1080, "height": 2340}


_SELECTION = [{
    "where": {"resource_id__startswith": "product-price-"},
    "matched": 2,
}]
_CONTRACT_FIELDS = {
    "index", "parent_index", "depth", "role", "cls", "resource_id",
    "content_desc", "text", "name", "hint", "bounds", "center",
    "enabled", "checked", "selected", "clickable",
}
_IOS_XML = """
<AppiumAUT>
  <XCUIElementTypeApplication type="XCUIElementTypeApplication" name="Demo"
      enabled="true" visible="true" accessible="false" x="0" y="0"
      width="414" height="896">
    <XCUIElementTypeButton type="XCUIElementTypeButton" name="Pay" label="Pay"
        enabled="true" visible="true" accessible="true" x="20" y="100"
        width="120" height="40" />
  </XCUIElementTypeApplication>
</AppiumAUT>
"""


def _mute_worker(code, rows, connection):
    """A worker that never signals. Module level so spawn can pickle it."""
    import time as _t
    _t.sleep(30)


def _query(driver=None, **overrides):
    code = overrides.pop("code", (
        "def extract(tree):\n"
        "    prices = tree.where(resource_id__startswith='product-price-')\n"
        "    return sum(float(row['text'].replace('$', '')) for row in prices)\n"
    ))
    selection = overrides.pop("selection", _SELECTION)
    total_rows = overrides.pop("total_rows", 3)
    capture_baseline = overrides.pop(
        "capture_baseline", {"total_rows": total_rows, "selection": selection}
    )
    return testmu_appium.textual_analyzer(
        driver or _Driver(), code=code, capture_baseline=capture_baseline, **overrides
    )


def test_textual_analyzer_runs_a_recorded_extraction_against_fresh_rows():
    result = _query()

    assert result == 1998.0


@pytest.mark.parametrize("expression,recorded", [("len(rows) > 0", "true"), ("len(rows) == 0", "false")])
def test_a_boolean_extraction_is_stored_as_authoring_recorded_it(expression, recorded):
    """Authoring canonicalizes a bool result to 'true'/'false' before the
    assertion is recorded against it (expected 'true', no transforms). Replay
    must store the same string, or `equals` compares 'true' against 'True'."""
    result = _query(code=(
        "def extract(tree):\n"
        "    rows = tree.where(resource_id__startswith='product-price-')\n"
        f"    return {expression}\n"
    ))

    assert result == recorded


def test_a_healed_boolean_extraction_is_stored_the_same_way(monkeypatch):
    monkeypatch.setattr(
        _textual_analyzer_module, "_heal_extraction",
        lambda **_kw: _textual_analyzer_module.ViewportHealHit(value=True, code="", reasoning="r"),
    )
    with step("s"):
        result = _query(code=(
            "def extract(tree):\n"
            "    rows = tree.where(resource_id__startswith='product-price-')\n"
            "    if not rows:\n"
            "        raise ValueError('absent')\n"
            "    return True\n"
        ), selection=[{"where": {"resource_id__startswith": "product-price-"}, "matched": 9}])

    assert result == "true"


def test_textual_analyzer_authoring_returns_execution_metadata():
    result = testmu_appium.textual_analyzer_authoring(
        _Driver(),
        code=(
            "def extract(tree):\n"
            "    prices = tree.where(resource_id__startswith='product-price-')\n"
            "    return sum(float(row['text'].replace('$', '')) for row in prices)\n"
        ),
    )

    assert result["value"] == 1998.0
    assert result["selection"] == _SELECTION
    assert result["row_count"] == len(parse_tree(_PRODUCTS_XML, 1080, 2340))
    assert result["duration_ms"] >= 0


def test_textual_analyzer_authoring_refuses_an_unchecked_extraction():
    message = (
        "this extraction records no selection, so replay cannot detect locator drift. "
        "Select with tree.where(...) so the predicates are recorded."
    )
    with pytest.raises(ViewportScriptPolicyError) as raised:
        testmu_appium.textual_analyzer_authoring(
            _Driver(),
            code="def extract(tree):\n    return len(tree)\n",
        )
    assert str(raised.value) == message


@respx.mock
def test_replay_never_heals_an_extraction_that_records_no_selection(monkeypatch):
    """Heal must not rescue the one recording shape the design forbids.

    A script that never calls tree.where cannot be drift-checked, so healing it
    would manufacture a value for an extraction replay can never validate.
    """
    monkeypatch.setattr(_config, "smart", True)
    monkeypatch.setattr(_config, "heal", True)
    monkeypatch.setitem(_config._config, "platform", "android")
    monkeypatch.setitem(_config._config, "ai_api_host", "https://ai.example.test/v16-server")
    route = respx.post(
        "https://ai.example.test/v16-server/api/v1/textual_analyzer/heal"
    ).mock(return_value=httpx.Response(200, json={"code": "x", "confidence": 1.0}))

    with pytest.raises(ViewportScriptPolicyError, match="no selection"):
        _query(
            code="def extract(tree):\n    return len(tree)\n",
            selection=[],
            extraction_description="rows on screen",
        )
    assert route.call_count == 0


def test_capture_settles_then_reads_window_geometry():
    """The capture goes through the binding's settle: two identical consecutive
    page-source digests, then the window size — never a single cold read."""
    calls = []

    class _OrderedDriver:
        @property
        def page_source(self):
            calls.append("page_source")
            return _PRODUCTS_XML

        def get_window_size(self):
            calls.append("window")
            return {"width": 1080, "height": 2340}

    assert _query(_OrderedDriver()) == 1998.0
    assert calls == ["page_source", "page_source", "window"]


def test_a_cold_first_read_is_waited_out_by_the_settle(monkeypatch):
    """Immediately after launch the first tree can be empty; the settle keeps
    reading until two consecutive captures agree, so the rows come from the
    populated tree, not the cold one.

    Heal is off so the value can only have come from the settled capture: a heal
    could otherwise regenerate 1998.0 from a drifted one and hide the bug.
    """
    monkeypatch.setattr(_config, "heal", False)
    reads = iter(["<hierarchy/>", _PRODUCTS_XML, _PRODUCTS_XML])

    class _ColdDriver:
        @property
        def page_source(self):
            return next(reads)

        def get_window_size(self):
            return {"width": 1080, "height": 2340}

    assert _query(_ColdDriver()) == 1998.0


def test_capture_falls_back_to_one_read_when_settle_reads_nothing(monkeypatch):
    """A settle that produced no document (disabled budget, or a driver that
    could not answer) must not cost a second page-source read."""
    calls = []
    settled = []

    def _no_document(driver, deadline):
        settled.append(driver)
        return None

    monkeypatch.setattr("testmu_appium._action_engine._settle", _no_document)

    class _CountingDriver:
        @property
        def page_source(self):
            calls.append("page_source")
            return _PRODUCTS_XML

        def get_window_size(self):
            return {"width": 1080, "height": 2340}

    assert _query(_CountingDriver()) == 1998.0
    assert len(settled) == 1
    assert calls == ["page_source"]


def test_a_zero_settle_budget_costs_exactly_one_page_source_read(monkeypatch):
    """settle_timeout_ms=0 returns the settle at its own gate, so the capture is
    the single cold read it was before settling: a run configured with settling
    off pays no extra page-source read for the verb."""
    monkeypatch.setitem(_config._config, "settle_timeout_ms", 0)
    calls = []

    class _CountingDriver:
        @property
        def page_source(self):
            calls.append("page_source")
            return _PRODUCTS_XML

        def get_window_size(self):
            return {"width": 1080, "height": 2340}

    assert _query(_CountingDriver()) == 1998.0
    assert calls == ["page_source"]


@respx.mock
def test_a_heal_non_hit_raises_without_touching_vision(monkeypatch):
    """Fail-loud contract: after the one heal attempt misses, the helper raises
    the viewport error and never reaches for a screenshot read."""
    import testmu_appium._helpers.vision_query as _vision_module

    def _boom(*args, **kwargs):
        raise AssertionError("vision_query must not be called by textual_analyzer")

    monkeypatch.setattr(_vision_module, "vision_query", _boom)
    monkeypatch.setattr(testmu_appium, "vision_query", _boom)
    monkeypatch.setattr(_config, "smart", True)
    monkeypatch.setattr(_config, "heal", True)
    monkeypatch.setenv("TESTMU_AI_API_HOST", "https://ai.example.test/v16-server")
    route = respx.post(
        "https://ai.example.test/v16-server/api/v1/textual_analyzer/heal"
    ).mock(return_value=httpx.Response(404, json={"detail": "no code"}))

    with pytest.raises(ViewportSelectionDriftError):
        _query(
            selection=[{"where": {"resource_id": "gone-id"}, "matched": 2}],
            extraction_description="sum of product prices currently in the viewport",
        )
    assert route.call_count == 1
    assert not hasattr(_textual_analyzer_module, "vision_query")


def test_projected_rows_expose_only_the_v1_contract_fields():
    result = _query(
        code=(
            "def extract(tree):\n"
            "    row = tree.where(resource_id__startswith='product-price-')[0]\n"
            "    return ','.join(sorted(row))\n"
        ),
    )

    assert set(result.split(",")) == _CONTRACT_FIELDS
    assert "displayed" not in result
    assert "visual_name" not in result


@pytest.mark.parametrize(
    ("platform", "xml", "width", "height"),
    [
        ("android", _PRODUCTS_XML, 1080, 2340),
        ("ios", _IOS_XML, 414, 896),
    ],
)
def test_v1_contract_fields_are_produced_by_both_native_parsers(
    platform, xml, width, height,
):
    [row] = parse_tree(xml, width, height, platform=platform)[:1]

    assert _CONTRACT_FIELDS <= set(row)
    assert isinstance(row["index"], int)
    assert row["parent_index"] is None or isinstance(row["parent_index"], int)
    assert isinstance(row["depth"], int)
    assert all(isinstance(row[field], str) for field in (
        "role", "cls", "resource_id", "content_desc", "text", "name", "hint",
    ))
    assert isinstance(row["bounds"], tuple)
    assert isinstance(row["center"], tuple)
    assert all(
        row[field] is None or isinstance(row[field], bool)
        for field in ("enabled", "checked", "selected", "clickable")
    )


def test_capture_failure_is_named():
    class _BrokenDriver:
        @property
        def page_source(self):
            raise RuntimeError("session lost")

    with pytest.raises(ViewportCaptureError, match="session lost"):
        _query(_BrokenDriver())


def test_degenerate_capture_fails_before_the_script_can_return_zero():
    collapsed = """
    <hierarchy rotation="0">
      <node class="android.widget.TextView" resource-id="product-price-1"
            text="$0.00" bounds="[0,100][400,200]" />
    </hierarchy>
    """

    class _CollapsedDriver(_Driver):
        page_source = collapsed

    with pytest.raises(DegenerateViewportCaptureError, match="collapsed"):
        _query(
            _CollapsedDriver(),
            code="def extract(tree):\n    return 0\n",
            total_rows=10,
        )


def test_missing_or_zero_total_rows_skips_only_the_collapse_check():
    collapsed = """
    <hierarchy rotation="0">
      <node class="android.widget.TextView" resource-id="product-price-1"
            text="$0.00" bounds="[0,100][400,200]" />
    </hierarchy>
    """

    class _CollapsedDriver(_Driver):
        page_source = collapsed

    selection = [{
        "where": {"resource_id__startswith": "product-price-"},
        "matched": 1,
    }]
    code = (
        "def extract(tree):\n"
        "    tree.where(resource_id__startswith='product-price-')\n"
        "    return 0\n"
    )

    assert _query(
        _CollapsedDriver(), code=code, selection=selection, total_rows=0
    ) == 0
    assert _query(
        _CollapsedDriver(), code=code, selection=selection, total_rows=None,
    ) == 0
    # An entirely absent capture_baseline skips both baseline gates too.
    assert testmu_appium.textual_analyzer(_CollapsedDriver(), code=code) == 0


@respx.mock
def test_selection_drift_heals_once_with_the_fresh_rows_and_recorded_directive(monkeypatch):
    missing = """
    <hierarchy rotation="0">
      <node class="android.widget.TextView" resource-id="catalog-price-new"
            text="$999.00" bounds="[0,100][400,200]" />
    </hierarchy>
    """

    class _MissingDriver(_Driver):
        page_source = missing

    monkeypatch.setattr(_config, "smart", True)
    monkeypatch.setattr(_config, "heal", True)
    monkeypatch.setenv("TESTMU_AI_API_HOST", "https://ai.example.test/v16-server")
    monkeypatch.setitem(_config._config, "platform", "android")
    monkeypatch.setitem(_config._config, "ai_api_host", "https://ai.example.test/v16-server")
    route = respx.post(
        "https://ai.example.test/v16-server/api/v1/textual_analyzer/heal"
    ).mock(return_value=httpx.Response(200, json={
        "code": (
            "def extract(tree):\n"
                "    prices = tree.where(resource_id__startswith='catalog-price-new')\n"
            "    return sum(float(row['text'][1:]) for row in prices)\n"
        ),
        "confidence": 0.9,
        "reasoning": "price ids gained a suffix",
    }))

    with step("Read current product prices"):
        assert _query(
            _MissingDriver(),
            code="def extract(tree):\n    raise AssertionError('must not run')\n",
            total_rows=1,
            extraction_description="sum of product prices currently in the viewport",
        ) == 999.0
        healed_step = current_step()
    assert healed_step.is_autohealed is True
    assert healed_step.autoheal_source == "v16-textual-analyzer-viewport"
    assert route.call_count == 1
    request = route.calls[0].request
    assert request.headers["x-platform"] == "android"
    body = json.loads(request.content)
    assert body["previous_code"].endswith("must not run')\n")
    assert body["extraction_description"] == "sum of product prices currently in the viewport"
    assert body["failed_predicates"] == _SELECTION
    # Sent as JSON text: dom_snapshot is a string on the web leg too, and the
    # server renders it into the prompt without inspecting its shape. A live
    # 422 from the deployed server proved the list form is not accepted.
    assert isinstance(body["dom_snapshot"], str)
    assert json.loads(body["dom_snapshot"]) == json.loads(json.dumps(
        _textual_analyzer_module._project(parse_tree(missing, 1080, 2340))
    ))


@pytest.mark.parametrize(
    ("original_code", "trigger"),
    [
        (
            "def extract(tree):\n"
            "    tree.where(resource_id__startswith='product-price-')\n"
            "    return 1 / 0\n",
            "runtime",
        ),
        (
            "def extract(tree):\n"
            "    tree.where(resource_id__startswith='product-price-')\n"
            "    return None\n",
            "none",
        ),
    ],
)
@respx.mock
def test_script_raise_and_none_take_the_same_single_heal_path(
    monkeypatch, original_code, trigger,
):
    monkeypatch.setattr(_config, "smart", True)
    monkeypatch.setattr(_config, "heal", True)
    monkeypatch.setenv("TESTMU_AI_API_HOST", "https://ai.example.test/v16-server")
    route = respx.post(
        "https://ai.example.test/v16-server/api/v1/textual_analyzer/heal"
    ).mock(return_value=httpx.Response(200, json={
        "code": (
            "def extract(tree):\n"
            "    prices = tree.where(resource_id__startswith='product-price-')\n"
            "    return len(prices)\n"
        ),
        "confidence": 0.7,
        "reasoning": trigger,
    }))

    assert _query(
        code=original_code,
        extraction_description="number of visible product prices",
    ) == 2
    assert route.call_count == 1


@pytest.mark.parametrize(
    ("response", "reason"),
    [
        (httpx.Response(404, json={"detail": "no code"}), "authoritative no-match"),
        (httpx.Response(500, text="downstream unavailable"), "unavailable"),
        (httpx.Response(200, json={"code": "x", "confidence": 0.69}), "authoritative no-match"),
        (
            httpx.Response(200, json={
                "code": "def extract(tree):\n    return 1\n",
                "confidence": 0.9,
            }),
            "regenerated script unresolved",
        ),
    ],
)
@respx.mock
def test_every_non_hit_fails_without_a_recorded_value_fallback(
    monkeypatch, response, reason,
):
    missing = """
    <hierarchy rotation="0">
      <node class="android.widget.TextView" resource-id="unrelated-price"
            text="$999.00" bounds="[0,100][400,200]" />
    </hierarchy>
    """

    class _MissingDriver(_Driver):
        page_source = missing

    monkeypatch.setattr(_config, "smart", True)
    monkeypatch.setattr(_config, "heal", True)
    monkeypatch.setenv("TESTMU_AI_API_HOST", "https://ai.example.test/v16-server")
    route = respx.post(
        "https://ai.example.test/v16-server/api/v1/textual_analyzer/heal"
    ).mock(return_value=response)

    with pytest.raises(ViewportSelectionDriftError, match=reason):
        _query(
            _MissingDriver(),
            extraction_description="sum of product prices currently in the viewport",
        )
    assert route.call_count == 1


@respx.mock
def test_transport_failure_is_unavailable_after_one_request(monkeypatch):
    missing = """
    <hierarchy rotation="0">
      <node class="android.widget.TextView" resource-id="unrelated-price"
            text="$999.00" bounds="[0,100][400,200]" />
    </hierarchy>
    """

    class _MissingDriver(_Driver):
        page_source = missing

    monkeypatch.setattr(_config, "smart", True)
    monkeypatch.setattr(_config, "heal", True)
    monkeypatch.setenv("TESTMU_AI_API_HOST", "https://ai.example.test/v16-server")
    route = respx.post(
        "https://ai.example.test/v16-server/api/v1/textual_analyzer/heal"
    ).mock(side_effect=httpx.TimeoutException("timed out"))

    with pytest.raises(ViewportSelectionDriftError, match="unavailable"):
        _query(
            _MissingDriver(),
            extraction_description="sum of product prices currently in the viewport",
        )
    assert route.call_count == 1


@respx.mock
def test_heal_off_keeps_the_recorded_failure_and_never_posts(monkeypatch):
    missing = """
    <hierarchy rotation="0">
      <node class="android.widget.TextView" resource-id="unrelated-price"
            text="$999.00" bounds="[0,100][400,200]" />
    </hierarchy>
    """

    class _MissingDriver(_Driver):
        page_source = missing

    monkeypatch.setattr(_config, "smart", True)
    monkeypatch.setattr(_config, "heal", False)
    route = respx.post("https://kaneai-api.lambdatest.com/").mock(
        return_value=httpx.Response(200, json={})
    )

    with pytest.raises(ViewportSelectionDriftError, match="product-price-"):
        _query(
            _MissingDriver(),
            extraction_description="sum of product prices currently in the viewport",
        )
    assert route.call_count == 0


def test_guarding_an_empty_match_with_ValueError_is_allowed():
    """The prompts instruct the model to raise rather than let an empty match
    become a confident wrong answer, so ValueError has to be reachable.

    It was not, and every guarded extraction the model wrote was rejected —
    which pushed it to record the answer as a constant instead. Measured on a
    real device run: three finalize_code attempts, all rejected on this
    name, then a fallback that baked the value in."""
    with pytest.raises(ViewportScriptRuntimeError, match="ValueError"):
        _query(
            code=(
                "def extract(tree):\n"
                "    rows = tree.where(resource_id='no-such-id')\n"
                "    if not rows:\n"
                "        raise ValueError('no rows to total')\n"
                "    return len(rows)\n"
            ),
            selection=[],
        )


def test_no_other_exception_name_is_reachable():
    """ValueError is the single allowed name; the prompts say so because the
    policy enforces it. A model reaching for KeyError must fail loudly here
    rather than at authoring time on a device."""
    for name in ("KeyError", "RuntimeError", "AssertionError", "Exception"):
        with pytest.raises(ViewportScriptPolicyError, match=f"disallowed name '{name}'"):
            _query(
                code=(
                    "def extract(tree):\n"
                    "    rows = tree.where(resource_id='no-such-id')\n"
                    f"    raise {name}('nope')\n"
                ),
                selection=[],
            )


def test_an_extraction_must_register_a_selection():
    with pytest.raises(ViewportScriptPolicyError, match="no selection"):
        _query(code="def extract(tree):\n    return 1\n", selection=[])


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("0", 0),
        ("False", "false"),
        ("''", ""),
    ],
)
def test_zero_false_and_empty_string_are_valid_scalars(expression, expected):
    result = _query(
        code=(
            "def extract(tree):\n"
            "    tree.where(resource_id__startswith='product-price-')\n"
            f"    return {expression}\n"
        ),
    )

    assert result == expected


def test_none_result_is_a_named_viewport_miss():
    with pytest.raises(ViewportResultMissError, match="returned None"):
        _query(
            code=(
                "def extract(tree):\n"
                "    tree.where(resource_id__startswith='product-price-')\n"
                "    return None\n"
            )
        )


@pytest.mark.parametrize("expression", ["math.nan", "math.inf", "[]"])
def test_non_finite_and_non_scalar_results_are_type_errors(expression):
    with pytest.raises(ViewportResultTypeError):
        _query(
            code=(
                "def extract(tree):\n"
                "    tree.where(resource_id__startswith='product-price-')\n"
                f"    return {expression}\n"
            )
        )


def test_imports_are_rejected_by_script_policy():
    with pytest.raises(ViewportScriptPolicyError, match="imports"):
        _query(
            code=(
                "def extract(tree):\n"
                "    tree.where(resource_id__startswith='product-price-')\n"
                "    import os\n"
                "    return 1\n"
            )
        )


@pytest.mark.parametrize(
    ("builtin", "function"),
    [
        ("vars", vars),
        ("dir", dir),
        ("globals", globals),
        ("locals", locals),
        ("eval", eval),
        ("exec", exec),
        ("compile", compile),
        ("open", open),
        ("input", input),
        ("type", type),
        ("object", object),
        ("super", super),
        ("id", id),
        ("breakpoint", breakpoint),
        ("memoryview", memoryview),
        ("help", help),
        ("classmethod", classmethod),
        ("staticmethod", staticmethod),
        ("property", property),
        ("getattr", getattr),
        ("hasattr", hasattr),
        ("setattr", setattr),
        ("delattr", delattr),
    ],
)
def test_unapproved_builtins_are_rejected_even_when_the_worker_allows_them(
    monkeypatch, builtin, function,
):
    monkeypatch.setitem(_textual_analyzer_module._SAFE_BUILTINS, builtin, function)

    with pytest.raises(ViewportScriptPolicyError, match=rf"name {builtin!r}"):
        _query(
            code=(
                "def extract(tree):\n"
                "    tree.where(resource_id__startswith='product-price-')\n"
                f"    return {builtin}(tree)\n"
            )
        )


def test_policy_allows_injected_globals_and_function_local_names():
    result = _query(
        code=(
            "def extract(tree):\n"
            "    prices = tree.where(resource_id__startswith='product-price-')\n"
            "    multiplier = Decimal(json.loads('{\"value\": \"1\"}')[\"value\"])\n"
            "    amounts = [\n"
            "        Decimal(re.sub(r'\\$', '', row['text'])) * multiplier\n"
            "        for row in prices\n"
            "    ]\n"
            "    total = Decimal('0')\n"
            "    for amount in amounts:\n"
            "        total += amount\n"
            "    return float(total)\n"
        )
    )

    assert result == 1998.0


def test_comprehension_target_does_not_leak_into_function_scope():
    with pytest.raises(ViewportScriptPolicyError, match="name 'row'"):
        _query(
            code=(
                "def extract(tree):\n"
                "    prices = tree.where(resource_id__startswith='product-price-')\n"
                "    values = [row['text'] for row in prices]\n"
                "    return row\n"
            ),
        )


def test_name_bound_later_in_the_function_is_a_static_reference():
    with pytest.raises(ViewportScriptRuntimeError, match="UnboundLocalError"):
        _query(
            code=(
                "def extract(tree):\n"
                "    tree.where(resource_id__startswith='product-price-')\n"
                "    before = after\n"
                "    after = 1\n"
                "    return before\n"
            )
        )


def test_static_policy_accepts_all_supported_local_binding_forms():
    _textual_analyzer_module._validate_script(
        "def extract(tree):\n"
        "    assigned = 1\n"
        "    for loop_value in (assigned,):\n"
        "        assigned = loop_value\n"
        "    values = [comp_value for comp_value in (assigned,)]\n"
        "    with tree as context_value:\n"
        "        assigned = context_value\n"
        "    try:\n"
        "        pass\n"
        "    except () as caught:\n"
        "        assigned = caught\n"
        "    return (walrus_value := assigned)\n"
    )


@pytest.mark.parametrize("expression", [
    "open('/etc/hosts').read()",
    "driver.page_source",
])
def test_filesystem_and_driver_are_unavailable(expression):
    with pytest.raises(ViewportScriptPolicyError, match="disallowed name"):
        _query(
            code=(
                "def extract(tree):\n"
                "    tree.where(resource_id__startswith='product-price-')\n"
                f"    return {expression}\n"
            )
        )


def test_timeout_stops_an_unbounded_script(monkeypatch):
    monkeypatch.setitem(_config._config, "default_action_timeout_ms", 50)

    with pytest.raises(ViewportScriptTimeoutError, match="timed out"):
        _query(
            code=(
                "def extract(tree):\n"
                "    tree.where(resource_id__startswith='product-price-')\n"
                "    while True:\n"
                "        pass\n"
            )
        )


def test_a_sandbox_that_never_starts_says_so_rather_than_blaming_the_script(monkeypatch):
    """A silent worker was reported as "viewport extraction timed out", which
    reads as a slow script. On a device run it was the sandbox never producing
    anything — a script that raises AttributeError in 0.01s standalone consumed
    the whole budget there — and the two have nothing in common as fixes."""
    monkeypatch.setattr(_textual_analyzer_module, "_worker", _mute_worker)
    monkeypatch.setattr(_textual_analyzer_module, "_WORKER_START_TIMEOUT_S", 0.5)
    # Pin one method: with a fallback available this would silently succeed
    # via spawn, which is the recovery path the next test covers.
    monkeypatch.setattr(_textual_analyzer_module, "_FORCED_START_METHOD", "fork")

    with pytest.raises(ViewportScriptTimeoutError, match="never started"):
        _query(code="def extract(tree):\n    return len(tree.where(text='x'))\n",
               selection=[])


def test_a_started_worker_is_still_held_to_the_script_budget():
    """The start marker must not become a way to run forever."""
    with pytest.raises(ViewportScriptTimeoutError, match="timed out"):
        _query(
            code=("def extract(tree):\n"
                  "    tree.where(text='x')\n"
                  "    n = 0\n"
                  "    while True:\n"
                  "        n += 1\n"
                  "    return n\n"),
            selection=[],
        )


def test_a_dead_fork_falls_back_to_the_next_start_method(monkeypatch):
    """The runner's forked child never ran a line of Python, on every attempt,
    while the same script finished in 0.01s standalone. One dead fork must cost
    one call, not the extraction, and not every call after it."""
    tried = []

    def _fake(method, code, rows):
        tried.append(method)
        if method == "fork":
            raise _textual_analyzer_module._SandboxDidNotStart(method)
        return (1998.0, _SELECTION)

    monkeypatch.setattr(_textual_analyzer_module, "_FORCED_START_METHOD", None)
    monkeypatch.setattr(_textual_analyzer_module, "_run_script_with", _fake)

    assert _textual_analyzer_module._run_script("code", []) == (1998.0, _SELECTION)
    assert tried == ["fork", "spawn"]
    assert _textual_analyzer_module._FORCED_START_METHOD == "spawn", (
        "the dead method must not be retried on every later extraction"
    )


def test_a_frozen_build_never_falls_back_to_spawn(monkeypatch):
    """Spawn re-executes sys.executable. In a frozen runner that is the app
    binary, and without freeze_support it relaunches the app."""
    monkeypatch.setattr(_textual_analyzer_module, "_FORCED_START_METHOD", None)
    monkeypatch.setattr(_textual_analyzer_module, "_is_frozen", lambda: True)

    assert "spawn" not in _textual_analyzer_module._start_methods()
