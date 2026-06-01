"""Tests for the Bedrock inference-profile probe used at `efterlev init`.

v0.1.0-v0.1.35 used a lexical sort over inference-profile IDs to pick the
"latest" Anthropic Opus. That sort gets `claude-opus-4-1-20250805` vs
`claude-opus-4-20250514` wrong because at position 14 the digit `2` of the
date `20250514` outranks the `1` of the version `4-1`. Result: a fresh
`efterlev init` against a Bedrock account with both Opus 4.0 and Opus 4.1
profiles enabled would pick Opus 4.0 (older) over Opus 4.1 (newer).

v0.1.36 replaces the lexical sort with a parsed (major, minor, date_int,
rev) tuple compare and adds a `us.*`-prefix filter (excluding eu/apac/global
inference profiles — the latter forfeits the US-region geographic guarantee
some FedRAMP boundary documentation depends on).

These tests:

- Pin the parser against every shape of Anthropic Bedrock ID currently in
  production (Opus 3, 4.0, 4.1, 4.7; Sonnet 3, 3.5, 3.7, 4, 4.6; Haiku 3,
  3.5, 4.5).
- Verify the ranking order on a synthetic candidate set so a future regex
  edit that breaks ordering fails the suite immediately.
- Verify the `us.*` filter excludes eu/apac/global candidates.
- Verify the family filter (opus / sonnet / haiku) returns the right family.
- A/B-verify the v0.1.36 fix against the v0.1.35 lexical-sort failure mode.
"""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

from efterlev.cli.main import (
    _parse_bedrock_anthropic_version,
    _probe_bedrock_default_model,
    _probe_bedrock_for_family,
)

# --- _parse_bedrock_anthropic_version ----------------------------------------


def test_parse_opus_4_7() -> None:
    assert _parse_bedrock_anthropic_version("us.anthropic.claude-opus-4-7-v1:0") == (4, 7, 0, 1)


def test_parse_opus_4_1_dated() -> None:
    assert _parse_bedrock_anthropic_version("us.anthropic.claude-opus-4-1-20250805-v1:0") == (
        4,
        1,
        20250805,
        1,
    )


def test_parse_opus_4_0_dated_no_minor() -> None:
    """The v0.1.0-v0.1.35 lexical-sort failure mode: Opus 4.0 with a date
    suffix. Pre-v0.1.36 regex would parse minor=20 (greedy from the date);
    v0.1.36 lookahead enforces minor must be followed by `-` or end-of-id,
    so the date is preserved and minor is correctly absent (= 0)."""
    assert _parse_bedrock_anthropic_version("us.anthropic.claude-opus-4-20250514-v1:0") == (
        4,
        0,
        20250514,
        1,
    )


def test_parse_legacy_opus_3() -> None:
    assert _parse_bedrock_anthropic_version("us.anthropic.claude-3-opus-20240229-v1:0") == (
        3,
        0,
        20240229,
        1,
    )


def test_parse_legacy_sonnet_3_5() -> None:
    assert _parse_bedrock_anthropic_version("us.anthropic.claude-3-5-sonnet-20241022-v2:0") == (
        3,
        5,
        20241022,
        2,
    )


def test_parse_legacy_sonnet_3_7() -> None:
    assert _parse_bedrock_anthropic_version("us.anthropic.claude-3-7-sonnet-20250219-v1:0") == (
        3,
        7,
        20250219,
        1,
    )


def test_parse_sonnet_4() -> None:
    assert _parse_bedrock_anthropic_version("us.anthropic.claude-sonnet-4-20250514-v1:0") == (
        4,
        0,
        20250514,
        1,
    )


def test_parse_sonnet_4_6() -> None:
    assert _parse_bedrock_anthropic_version("us.anthropic.claude-sonnet-4-6-v1:0") == (4, 6, 0, 1)


def test_parse_haiku_4_5() -> None:
    assert _parse_bedrock_anthropic_version("us.anthropic.claude-haiku-4-5-20251001-v1:0") == (
        4,
        5,
        20251001,
        1,
    )


def test_parse_legacy_haiku_3_5() -> None:
    assert _parse_bedrock_anthropic_version("us.anthropic.claude-3-5-haiku-20241022-v1:0") == (
        3,
        5,
        20241022,
        1,
    )


def test_parse_unknown_id_returns_none() -> None:
    assert _parse_bedrock_anthropic_version("us.anthropic.cohere-command-r-v1:0") is None
    assert _parse_bedrock_anthropic_version("us.amazon.titan-text-v1:0") is None
    assert _parse_bedrock_anthropic_version("garbage") is None


# --- ranking sanity ----------------------------------------------------------


def test_opus_4_7_ranks_above_opus_4_1() -> None:
    """Major.minor wins over date alone: Opus 4.7 (no date) beats Opus 4.1 (Aug 2025)."""
    assert _parse_bedrock_anthropic_version(
        "us.anthropic.claude-opus-4-7-v1:0"
    ) > _parse_bedrock_anthropic_version("us.anthropic.claude-opus-4-1-20250805-v1:0")


def test_opus_4_1_ranks_above_opus_4_0() -> None:
    """The v0.1.36 bug-fix lock: Opus 4.1 (Aug 2025) MUST beat Opus 4.0 (May
    2025) despite the lexical sort getting this wrong."""
    assert _parse_bedrock_anthropic_version(
        "us.anthropic.claude-opus-4-1-20250805-v1:0"
    ) > _parse_bedrock_anthropic_version("us.anthropic.claude-opus-4-20250514-v1:0")


def test_opus_4_anything_ranks_above_opus_3() -> None:
    """Even the oldest Opus 4 beats every Opus 3."""
    assert _parse_bedrock_anthropic_version(
        "us.anthropic.claude-opus-4-20250514-v1:0"
    ) > _parse_bedrock_anthropic_version("us.anthropic.claude-3-opus-20240229-v1:0")


def test_sonnet_4_6_ranks_above_sonnet_3_7() -> None:
    assert _parse_bedrock_anthropic_version(
        "us.anthropic.claude-sonnet-4-6-v1:0"
    ) > _parse_bedrock_anthropic_version("us.anthropic.claude-3-7-sonnet-20250219-v1:0")


def test_haiku_4_5_ranks_above_haiku_3_5() -> None:
    assert _parse_bedrock_anthropic_version(
        "us.anthropic.claude-haiku-4-5-20251001-v1:0"
    ) > _parse_bedrock_anthropic_version("us.anthropic.claude-3-5-haiku-20241022-v1:0")


# --- _probe_bedrock_for_family (with mocked boto) ----------------------------


def _profile_to_underlying_id(pid: str) -> str:
    """Strip the `us.` / `eu.` / etc. prefix to get the underlying foundation
    model ID a profile points at. e.g. `us.anthropic.claude-opus-4-7-v1:0`
    -> `anthropic.claude-opus-4-7-v1:0`. Realistic enough for tests; the
    real boto response carries this in `models[].modelArn`.
    """
    if pid.startswith(("us.", "eu.", "apac.", "global.")):
        return pid.split(".", 1)[1]
    return pid


def _mock_bedrock_response(profile_ids: list[str]) -> dict[str, Any]:
    """Build a fake `list_inference_profiles` response shaped like boto's."""
    return {
        "inferenceProfileSummaries": [
            {
                "inferenceProfileId": pid,
                "inferenceProfileName": pid,
                "models": [
                    {
                        "modelArn": (
                            f"arn:aws:bedrock:::foundation-model/{_profile_to_underlying_id(pid)}"
                        )
                    }
                ],
            }
            for pid in profile_ids
        ]
    }


def _mock_foundation_models_response(
    models: list[tuple[str, str]] | list[tuple[str, str, list[str]]] | None = None,
) -> dict[str, Any]:
    """Build a fake `list_foundation_models` response.

    Each entry is either a 2-tuple `(model_id, lifecycle_status)` for
    pre-v0.1.40 test compatibility (defaults `inferenceTypesSupported`
    to `["ON_DEMAND"]`, since that's what historical tests assumed) or
    a 3-tuple `(model_id, lifecycle_status, inference_types)` for
    v0.1.40+ tests that exercise the on-demand requirement explicitly.
    """
    summaries: list[dict[str, Any]] = []
    for entry in models or []:
        if len(entry) == 2:
            mid, status = entry
            inference_types: list[str] = ["ON_DEMAND"]
        else:
            mid, status, inference_types = entry
        summaries.append(
            {
                "modelId": mid,
                "modelLifecycle": {"status": status},
                "inferenceTypesSupported": inference_types,
            }
        )
    return {"modelSummaries": summaries}


def _patch_boto(
    profile_ids: list[str],
    foundation_models: list[tuple[str, str]] | list[tuple[str, str, list[str]]] | None = None,
    invokable: set[str] | None = None,
) -> Any:
    """Build a context manager that patches boto3.Session().client to return
    a stub with `list_inference_profiles`, `list_foundation_models`, AND
    `converse` (the v0.1.41 test-call closure).

    `foundation_models`: empty default preserves pre-v0.1.39 test
        behavior. 2-tuples expand to ON_DEMAND-supported entries;
        3-tuples let tests pin `inferenceTypesSupported`.
    `invokable`: set of model IDs whose `converse` ping should succeed.
        None defaults to "every model invokable" — preserves pre-v0.1.41
        test behavior so existing v0.1.39/v0.1.40 tests don't need to
        update. Pass an explicit set to exercise EOL/invalid-ID
        scenarios where some candidates fail at Converse time.
    """
    bedrock_client = MagicMock()
    bedrock_client.list_inference_profiles.return_value = _mock_bedrock_response(profile_ids)
    bedrock_client.list_foundation_models.return_value = _mock_foundation_models_response(
        foundation_models
    )

    runtime_client = MagicMock()

    def _fake_converse(**kwargs: Any) -> dict[str, Any]:
        # boto's converse takes `modelId` (camelCase) — accept via kwargs
        # to keep the boto signature without ruff's N803 complaint about
        # camelCase parameter names in our helper.
        model_id = kwargs.get("modelId", "")
        if invokable is not None and model_id not in invokable:
            # Mimic the AWS errors a real EOL / invalid ID would produce.
            # The probe only cares that an exception fires; the message
            # is for diagnostic value if a future test inspects it.
            raise Exception(f"ResourceNotFoundException for {model_id}")
        return {"output": {"message": {"content": [{"text": "hi"}]}}}

    runtime_client.converse.side_effect = _fake_converse

    def _client_factory(service_name: str, **_kwargs: Any) -> MagicMock:
        if service_name == "bedrock-runtime":
            return runtime_client
        return bedrock_client

    fake_session = MagicMock()
    fake_session.client.side_effect = _client_factory
    return patch("boto3.Session", return_value=fake_session)


def test_probe_picks_latest_opus_v0_1_36_failure_mode() -> None:
    """Lock the v0.1.36 bug-fix end-to-end: an account with both Opus 4.0
    and Opus 4.1 enabled must pick Opus 4.1, not Opus 4.0.

    Pre-v0.1.36 lexical sort picks `us.anthropic.claude-opus-4-20250514-v1:0`
    (Opus 4.0) because lexically `4-2…` outranks `4-1…`. v0.1.36 parses the
    version tuple correctly and picks Opus 4.1.
    """
    with _patch_boto(
        [
            "us.anthropic.claude-opus-4-20250514-v1:0",
            "us.anthropic.claude-opus-4-1-20250805-v1:0",
            "us.anthropic.claude-3-opus-20240229-v1:0",
        ]
    ):
        result = _probe_bedrock_for_family("us-east-1", "opus")
    assert result == "us.anthropic.claude-opus-4-1-20250805-v1:0"


def test_probe_picks_opus_4_7_when_available() -> None:
    """Account with Opus 4.7 (latest) + 4.1 + 4.0: must pick 4.7."""
    with _patch_boto(
        [
            "us.anthropic.claude-opus-4-1-20250805-v1:0",
            "us.anthropic.claude-opus-4-20250514-v1:0",
            "us.anthropic.claude-opus-4-7-v1:0",
        ]
    ):
        result = _probe_bedrock_for_family("us-east-1", "opus")
    assert result == "us.anthropic.claude-opus-4-7-v1:0"


def test_probe_excludes_eu_apac_global_profiles() -> None:
    """Even if eu/apac/global have a newer profile, US must win.

    FedRAMP boundary policy: data shouldn't egress outside the US
    authorization boundary; `global.*` forfeits the US-region geographic
    guarantee. We err toward conservatism and skip non-US profiles.
    """
    with _patch_boto(
        [
            "global.anthropic.claude-opus-4-7-v1:0",  # newer, but global
            "eu.anthropic.claude-opus-4-7-v1:0",  # newer, but EU
            "apac.anthropic.claude-opus-4-7-v1:0",  # newer, but APAC
            "us.anthropic.claude-opus-4-1-20250805-v1:0",  # older but US — wins
        ]
    ):
        result = _probe_bedrock_for_family("us-east-1", "opus")
    assert result == "us.anthropic.claude-opus-4-1-20250805-v1:0"


def test_probe_filters_by_family() -> None:
    """A `family="sonnet"` probe ignores Opus + Haiku profiles."""
    with _patch_boto(
        [
            "us.anthropic.claude-opus-4-7-v1:0",
            "us.anthropic.claude-sonnet-4-6-v1:0",
            "us.anthropic.claude-haiku-4-5-20251001-v1:0",
        ]
    ):
        sonnet = _probe_bedrock_for_family("us-east-1", "sonnet")
        haiku = _probe_bedrock_for_family("us-east-1", "haiku")
        opus = _probe_bedrock_for_family("us-east-1", "opus")
    assert sonnet == "us.anthropic.claude-sonnet-4-6-v1:0"
    assert haiku == "us.anthropic.claude-haiku-4-5-20251001-v1:0"
    assert opus == "us.anthropic.claude-opus-4-7-v1:0"


def test_probe_returns_none_on_no_us_anthropic_profile() -> None:
    """Account with only non-US or non-Anthropic profiles: probe returns None
    so caller falls back to the hardcoded default."""
    with _patch_boto(
        [
            "global.anthropic.claude-opus-4-7-v1:0",
            "us.amazon.titan-text-v1:0",
        ]
    ):
        result = _probe_bedrock_for_family("us-east-1", "opus")
    assert result is None


def test_probe_returns_none_on_invalid_family() -> None:
    """Unknown families return None without calling boto."""
    assert _probe_bedrock_for_family("us-east-1", "haiku-junior") is None
    assert _probe_bedrock_for_family("us-east-1", "") is None


def test_probe_returns_none_on_no_region() -> None:
    """Region required to construct the bedrock client."""
    assert _probe_bedrock_for_family(None, "opus") is None
    assert _probe_bedrock_for_family("", "opus") is None


def test_default_model_wrapper_returns_opus() -> None:
    """`_probe_bedrock_default_model` is a thin wrapper that asks for Opus."""
    with _patch_boto(
        [
            "us.anthropic.claude-opus-4-7-v1:0",
            "us.anthropic.claude-sonnet-4-6-v1:0",
        ]
    ):
        result = _probe_bedrock_default_model("us-east-1")
    assert result == "us.anthropic.claude-opus-4-7-v1:0"


# --- v0.1.39: lifecycle-aware probe ---------------------------------------


def test_v0_1_39_skips_legacy_backed_inference_profile() -> None:
    """Surfaced by v0.1.38 deep-test re-validation in a real account: the
    only `us.*` Opus profile pointed at the foundation model
    `anthropic.claude-opus-4-20250514-v1:0` whose lifecycle is LEGACY,
    so init succeeded but the gap call died with AccessDenied. v0.1.39
    skips profiles whose underlying foundation model is LEGACY.

    Lock: with one LEGACY-backed profile and one ACTIVE-backed profile,
    pick the ACTIVE-backed one even if the LEGACY profile has the higher
    parsed version.
    """
    with _patch_boto(
        profile_ids=[
            "us.anthropic.claude-opus-4-20250514-v1:0",  # LEGACY-backed
            "us.anthropic.claude-3-opus-20240229-v1:0",  # ACTIVE-backed
        ],
        foundation_models=[
            ("anthropic.claude-opus-4-20250514-v1:0", "LEGACY"),
            ("anthropic.claude-3-opus-20240229-v1:0", "ACTIVE"),
        ],
    ):
        result = _probe_bedrock_for_family("us-east-1", "opus")
    # LEGACY-backed profile skipped despite having a higher parsed version
    # than Claude 3 Opus.
    assert result == "us.anthropic.claude-3-opus-20240229-v1:0"


def test_v0_1_39_falls_back_to_active_foundation_model() -> None:
    """v0.1.39 fix for the user's actual account state at
    re-validation time: only `us.*` Opus profiles available are
    Claude 3 Opus (ACTIVE) and the legacy Opus 4 (LEGACY-backed).
    Foundation models include the active 4-1/4-5/4-6/4-7 family.
    Probe must fall back to direct foundation-model invocation on the
    highest-version ACTIVE foundation model — `anthropic.claude-opus-4-7`.
    """
    with _patch_boto(
        profile_ids=[
            "us.anthropic.claude-opus-4-20250514-v1:0",
            "us.anthropic.claude-3-opus-20240229-v1:0",
        ],
        foundation_models=[
            ("anthropic.claude-opus-4-20250514-v1:0", "LEGACY"),
            ("anthropic.claude-opus-4-1-20250805-v1:0", "ACTIVE"),
            ("anthropic.claude-opus-4-5-20251101-v1:0", "ACTIVE"),
            ("anthropic.claude-opus-4-6-v1", "ACTIVE"),
            ("anthropic.claude-opus-4-7", "ACTIVE"),
            ("anthropic.claude-3-opus-20240229-v1:0", "ACTIVE"),
        ],
    ):
        result = _probe_bedrock_for_family("us-east-1", "opus")
    assert result == "anthropic.claude-opus-4-7"


def test_v0_1_39_prefers_profile_over_equal_version_foundation_model() -> None:
    """When a cross-region inference profile and a direct foundation model
    are both available at the same version, the profile wins. Cross-region
    routing has better availability characteristics than direct invocation,
    so it's the right default. Lock the tiebreak.
    """
    with _patch_boto(
        profile_ids=["us.anthropic.claude-opus-4-7-v1:0"],
        foundation_models=[
            ("anthropic.claude-opus-4-7-v1:0", "ACTIVE"),
            ("anthropic.claude-opus-4-7", "ACTIVE"),
        ],
    ):
        result = _probe_bedrock_for_family("us-east-1", "opus")
    assert result == "us.anthropic.claude-opus-4-7-v1:0"


def test_v0_1_39_returns_none_when_only_legacy_candidates() -> None:
    """If the only available candidates (profiles + foundation models)
    are all LEGACY, return None. Caller falls back to the hardcoded
    DEFAULT_BEDROCK_MODEL — better than handing the user an auto-pick
    that's guaranteed to fail.
    """
    with _patch_boto(
        profile_ids=["us.anthropic.claude-opus-4-20250514-v1:0"],
        foundation_models=[
            ("anthropic.claude-opus-4-20250514-v1:0", "LEGACY"),
        ],
    ):
        result = _probe_bedrock_for_family("us-east-1", "opus")
    assert result is None


def test_v0_1_39_continues_when_list_foundation_models_denied() -> None:
    """If `bedrock:ListFoundationModels` permission is denied but
    `ListInferenceProfiles` works, degrade gracefully — probe profiles
    without lifecycle filtering. Better than returning None and forcing
    the user to set --llm-model manually.
    """
    fake_client = MagicMock()
    fake_client.list_inference_profiles.return_value = _mock_bedrock_response(
        ["us.anthropic.claude-opus-4-7-v1:0"]
    )
    fake_client.list_foundation_models.side_effect = Exception("AccessDenied")
    fake_session = MagicMock()
    fake_session.client.return_value = fake_client
    with patch("boto3.Session", return_value=fake_session):
        result = _probe_bedrock_for_family("us-east-1", "opus")
    assert result == "us.anthropic.claude-opus-4-7-v1:0"


def test_v0_1_39_foundation_model_fallback_filters_by_family() -> None:
    """Foundation-model fallback respects the `family` filter so a
    `family='sonnet'` probe doesn't accidentally return an Opus
    foundation model.
    """
    with _patch_boto(
        profile_ids=[],  # no profiles at all
        foundation_models=[
            ("anthropic.claude-opus-4-7", "ACTIVE"),
            ("anthropic.claude-sonnet-4-6", "ACTIVE"),
            ("anthropic.claude-haiku-4-5", "ACTIVE"),
        ],
    ):
        opus = _probe_bedrock_for_family("us-east-1", "opus")
        sonnet = _probe_bedrock_for_family("us-east-1", "sonnet")
        haiku = _probe_bedrock_for_family("us-east-1", "haiku")
    assert opus == "anthropic.claude-opus-4-7"
    assert sonnet == "anthropic.claude-sonnet-4-6"
    assert haiku == "anthropic.claude-haiku-4-5"


# --- v0.1.40: foundation-model on-demand-callability filter --------------


def test_v0_1_40_skips_foundation_model_without_on_demand_inference_type() -> None:
    """Surfaced by the v0.1.39 deep-test re-validation S2 finding: the
    probe correctly skipped the LEGACY-backed `us.*` profile and fell
    back to `anthropic.claude-opus-4-7` — but the gap call died with
    `ValidationException: Invocation of model ID anthropic.claude-opus-4-7
    with on-demand throughput isn't supported`. AWS's contract is that
    `lifecycle=ACTIVE` does NOT imply directly invokable; newer Opus
    foundation models are inference-profile-only and the documented
    signal is `inferenceTypesSupported: ['INFERENCE_PROFILE']` (no
    `ON_DEMAND`). v0.1.40 filters foundation-model fallback candidates
    on this signal.

    Lock: an ACTIVE foundation model whose inferenceTypesSupported lacks
    ON_DEMAND must be rejected even though lifecycle says it's current.
    """
    with _patch_boto(
        profile_ids=[],  # no usable profiles at all
        foundation_models=[
            # 4-7 is the newest but inference-profile-only. Reject it.
            ("anthropic.claude-opus-4-7", "ACTIVE", ["INFERENCE_PROFILE"]),
            # 4-1 is ON_DEMAND-callable. Pick this one.
            (
                "anthropic.claude-opus-4-1-20250805-v1:0",
                "ACTIVE",
                ["ON_DEMAND", "INFERENCE_PROFILE"],
            ),
        ],
    ):
        result = _probe_bedrock_for_family("us-east-1", "opus")
    assert result == "anthropic.claude-opus-4-1-20250805-v1:0"


def test_v0_1_40_returns_none_when_only_inference_profile_only_models_exist() -> None:
    """Reproduces the user's actual v0.1.39 deep-test re-validation
    account state: no usable cross-region profiles (only LEGACY-backed
    plus Claude 3 Opus), all newer Opus 4.x foundation models are
    inference-profile-only. Correct behavior is `None` — caller surfaces
    the actionable error rather than writing a doomed model into config.
    """
    with _patch_boto(
        profile_ids=[
            "us.anthropic.claude-opus-4-20250514-v1:0",  # LEGACY-backed
        ],
        foundation_models=[
            ("anthropic.claude-opus-4-20250514-v1:0", "LEGACY", ["ON_DEMAND"]),
            # Newer 4.x — all inference-profile-only.
            ("anthropic.claude-opus-4-1-20250805-v1:0", "ACTIVE", ["INFERENCE_PROFILE"]),
            ("anthropic.claude-opus-4-5-20251101-v1:0", "ACTIVE", ["INFERENCE_PROFILE"]),
            ("anthropic.claude-opus-4-6-v1", "ACTIVE", ["INFERENCE_PROFILE"]),
            ("anthropic.claude-opus-4-7", "ACTIVE", ["INFERENCE_PROFILE"]),
        ],
    ):
        result = _probe_bedrock_for_family("us-east-1", "opus")
    assert result is None


def test_v0_1_40_treats_missing_inference_types_field_as_no_on_demand() -> None:
    """Defensive: if AWS omits the `inferenceTypesSupported` field
    entirely (older API responses, edge cases), be conservative and
    treat as not-on-demand. Better to skip than to pick something that
    might fail at agent runtime.
    """
    fake_client = MagicMock()
    fake_client.list_inference_profiles.return_value = {"inferenceProfileSummaries": []}
    fake_client.list_foundation_models.return_value = {
        "modelSummaries": [
            # No inferenceTypesSupported field at all.
            {
                "modelId": "anthropic.claude-opus-4-7",
                "modelLifecycle": {"status": "ACTIVE"},
            },
        ]
    }
    fake_session = MagicMock()
    fake_session.client.return_value = fake_client
    with patch("boto3.Session", return_value=fake_session):
        result = _probe_bedrock_for_family("us-east-1", "opus")
    assert result is None


def test_v0_1_40_inference_profile_kept_even_when_underlying_lacks_on_demand() -> None:
    """The on-demand filter applies to the FOUNDATION-MODEL FALLBACK path,
    not to inference profiles. A profile is by definition the right way
    to invoke its underlying model regardless of the model's own
    inference-types-supported listing — that's the whole point of
    inference profiles. Lock that the v0.1.40 filter doesn't accidentally
    reject profiles whose underlying model is inference-profile-only.
    """
    with _patch_boto(
        profile_ids=["us.anthropic.claude-opus-4-7-v1:0"],
        foundation_models=[
            # Underlying model is inference-profile-only — but the profile
            # is the right invocation path for it, so keep the profile.
            ("anthropic.claude-opus-4-7-v1:0", "ACTIVE", ["INFERENCE_PROFILE"]),
        ],
    ):
        result = _probe_bedrock_for_family("us-east-1", "opus")
    assert result == "us.anthropic.claude-opus-4-7-v1:0"


# --- v0.1.41: test-call closure ------------------------------------------


def test_v0_1_41_skips_eol_profile_caught_only_by_test_call() -> None:
    """Surfaced by the v0.1.40 deep-test re-validation S2 finding: an
    inference profile pointing at a foundation model AWS has EOL'd is
    no longer in `list_foundation_models` BUT the cross-region profile
    lingers as `status=ACTIVE`. Pre-v0.1.41 we kept these profiles
    (defensive "unknown lifecycle = keep"), then the agent gap call
    died with `ResourceNotFoundException: This model version has
    reached the end of its life`. The test-call closure is the only
    way to catch this — AWS only surfaces EOL at Converse time.

    Lock: with one EOL-but-listed profile and one currently-invokable
    profile, return the invokable one — even if the EOL-listed one
    has the higher parsed version.
    """
    with _patch_boto(
        profile_ids=[
            "us.anthropic.claude-opus-4-7-v1:0",  # higher version, but EOL
            "us.anthropic.claude-3-opus-20240229-v1:0",  # lower, but invokable
        ],
        # Neither model in foundation list — exact reproduction of the
        # user's account state for Claude 3 Opus on 2026-05-08.
        foundation_models=[],
        invokable={"us.anthropic.claude-3-opus-20240229-v1:0"},
    ):
        result = _probe_bedrock_for_family("us-east-1", "opus")
    assert result == "us.anthropic.claude-3-opus-20240229-v1:0"


def test_v0_1_41_returns_none_when_no_candidate_test_call_succeeds() -> None:
    """If every candidate fails the test-call (account is in a state
    where nothing Anthropic Opus is actually invokable), return None.
    Caller surfaces the actionable error from the v0.1.40 init path.
    """
    with _patch_boto(
        profile_ids=[
            "us.anthropic.claude-opus-4-7-v1:0",
            "us.anthropic.claude-3-opus-20240229-v1:0",
        ],
        invokable=set(),  # nothing succeeds
    ):
        result = _probe_bedrock_for_family("us-east-1", "opus")
    assert result is None


def test_v0_1_41_test_call_walks_candidates_in_version_order() -> None:
    """The test-call must walk candidates in the same version-priority
    order the pre-v0.1.41 sort produced. If 4-7 fails but 4-1 succeeds,
    we get 4-1 — not Claude 3 Opus, even though Claude 3 Opus's profile
    might also work.
    """
    with _patch_boto(
        profile_ids=[
            "us.anthropic.claude-opus-4-7-v1:0",  # highest, EOL
            "us.anthropic.claude-opus-4-1-20250805-v1:0",  # next, invokable
            "us.anthropic.claude-3-opus-20240229-v1:0",  # lowest, also invokable
        ],
        invokable={
            "us.anthropic.claude-opus-4-1-20250805-v1:0",
            "us.anthropic.claude-3-opus-20240229-v1:0",
        },
    ):
        result = _probe_bedrock_for_family("us-east-1", "opus")
    # 4-7 failed, but 4-1 is next in version-priority order and succeeds.
    assert result == "us.anthropic.claude-opus-4-1-20250805-v1:0"


def test_v0_1_41_falls_back_to_first_candidate_when_runtime_client_construction_fails() -> None:
    """If the bedrock-runtime client itself can't be constructed (e.g.,
    a credentials edge case in some environments), degrade gracefully
    to the v0.1.40 behavior — return the highest-version candidate
    untested. Better than total failure; the agent call will surface
    any actual problem.
    """
    bedrock_client = MagicMock()
    bedrock_client.list_inference_profiles.return_value = _mock_bedrock_response(
        ["us.anthropic.claude-opus-4-7-v1:0"]
    )
    bedrock_client.list_foundation_models.return_value = _mock_foundation_models_response([])

    def _client_factory(service_name: str, **_kwargs: Any) -> Any:
        if service_name == "bedrock-runtime":
            raise Exception("simulated runtime-client construction failure")
        return bedrock_client

    fake_session = MagicMock()
    fake_session.client.side_effect = _client_factory
    with patch("boto3.Session", return_value=fake_session):
        result = _probe_bedrock_for_family("us-east-1", "opus")
    assert result == "us.anthropic.claude-opus-4-7-v1:0"
