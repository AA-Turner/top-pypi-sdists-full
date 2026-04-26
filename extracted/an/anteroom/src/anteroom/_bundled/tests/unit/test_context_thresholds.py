"""Tests for model-aware context threshold derivation."""

from __future__ import annotations

from anteroom.services.context_thresholds import ContextThresholdConfig, derive_context_thresholds


def test_default_128k_window_preserves_legacy_thresholds() -> None:
    thresholds = derive_context_thresholds(ContextThresholdConfig())

    assert thresholds.model_context_window == 128_000
    assert thresholds.reserved_output_tokens == 4_096
    assert thresholds.effective_context_window == 123_904
    assert thresholds.context_warn_tokens == 80_000
    assert thresholds.summary_trigger_token_count == 90_000
    assert thresholds.context_auto_compact_tokens == 100_000


def test_small_window_uses_model_aware_floor_instead_of_legacy_absolute_defaults() -> None:
    thresholds = derive_context_thresholds(ContextThresholdConfig(model_context_window=32_000))

    assert thresholds.effective_context_window == 27_904
    assert thresholds.context_warn_tokens == 17_440
    assert thresholds.summary_trigger_token_count == 19_532
    assert thresholds.context_auto_compact_tokens == 21_765


def test_large_window_scales_up_from_default_thresholds() -> None:
    thresholds = derive_context_thresholds(ContextThresholdConfig(model_context_window=200_000))

    assert thresholds.effective_context_window == 195_904
    assert thresholds.context_warn_tokens == 152_000
    assert thresholds.summary_trigger_token_count == 162_000
    assert thresholds.context_auto_compact_tokens == 172_000


def test_reserved_output_is_clamped_to_leave_a_minimum_effective_window() -> None:
    thresholds = derive_context_thresholds(
        ContextThresholdConfig(model_context_window=8_000, reserved_output_tokens=20_000)
    )

    assert thresholds.reserved_output_tokens == 7_000
    assert thresholds.effective_context_window == 1_000
    assert thresholds.context_warn_tokens == 1_000
    assert thresholds.context_auto_compact_tokens == 1_000
    assert thresholds.summary_trigger_token_count == 5_000


def test_explicit_legacy_thresholds_take_precedence() -> None:
    thresholds = derive_context_thresholds(
        ContextThresholdConfig(
            model_context_window=32_000,
            explicit_warn_tokens=8_000,
            explicit_auto_compact_tokens=9_000,
            explicit_summary_trigger_token_count=10_000,
        )
    )

    assert thresholds.context_warn_tokens == 8_000
    assert thresholds.context_auto_compact_tokens == 9_000
    assert thresholds.summary_trigger_token_count == 10_000


def test_buffers_are_configurable() -> None:
    thresholds = derive_context_thresholds(
        ContextThresholdConfig(
            model_context_window=128_000,
            reserved_output_tokens=8_000,
            warn_buffer_tokens=20_000,
            summary_trigger_buffer_tokens=15_000,
            auto_compact_buffer_tokens=10_000,
        )
    )

    assert thresholds.effective_context_window == 120_000
    assert thresholds.context_warn_tokens == 100_000
    assert thresholds.summary_trigger_token_count == 105_000
    assert thresholds.context_auto_compact_tokens == 110_000
