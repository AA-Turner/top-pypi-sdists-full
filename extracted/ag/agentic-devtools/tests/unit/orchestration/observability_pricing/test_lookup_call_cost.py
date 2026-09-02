"""Tests for observability pricing layer."""

import json
from pathlib import Path
from unittest.mock import patch

from agentic_devtools.orchestration.observability_pricing import (
    build_pricing_table,
    lookup_call_cost,
)


class TestLookupCallCost:
    """Tests for lookup_call_cost function."""

    def test_known_model_returns_cost(self) -> None:
        cost = lookup_call_cost("gpt-4o", 1000, 500)
        assert cost is not None
        assert cost > 0

    def test_exact_match_pricing(self) -> None:
        # gpt-4o: input=2.50/1M, output=10.00/1M
        cost = lookup_call_cost("gpt-4o", 1_000_000, 1_000_000)
        assert cost is not None
        assert abs(cost - 12.50) < 0.01

    def test_prefix_match_pricing(self) -> None:
        # "gpt-4o-2024-05-13" should match "gpt-4o" prefix
        cost = lookup_call_cost("gpt-4o-2024-05-13", 1000, 500)
        assert cost is not None
        assert cost > 0

    def test_unpriced_model_returns_none(self) -> None:
        cost = lookup_call_cost("totally-unknown-model", 1000, 500)
        assert cost is None

    def test_null_input_tokens_returns_none(self) -> None:
        cost = lookup_call_cost("gpt-4o", None, 500)
        assert cost is None

    def test_null_output_tokens_returns_none(self) -> None:
        cost = lookup_call_cost("gpt-4o", 1000, None)
        assert cost is None

    def test_both_null_tokens_returns_none(self) -> None:
        cost = lookup_call_cost("gpt-4o", None, None)
        assert cost is None

    def test_uses_env_pricing_override_when_no_table_passed(self, tmp_path: Path) -> None:
        pricing_file = tmp_path / "env-pricing.json"
        pricing_file.write_text(json.dumps({"env-model": {"input": 1.0, "output": 2.0}}))

        with patch.dict("os.environ", {"AGDT_LLM_PRICING_FILE": str(pricing_file)}):
            cost = lookup_call_cost("env-model", 1_000_000, 1_000_000)

        assert cost == 3.0

    def test_float_input_tokens_coerced(self) -> None:
        """Float token counts are coerced to int without crashing."""
        cost = lookup_call_cost("gpt-4o", 1000.0, 500.0)
        assert cost is not None
        assert cost > 0

    def test_string_input_tokens_coerced(self) -> None:
        """Numeric string token counts are coerced to int without crashing."""
        cost = lookup_call_cost("gpt-4o", "1000", "500")
        assert cost is not None
        assert cost > 0

    def test_bool_input_tokens_returns_none(self) -> None:
        """Bool token counts (True/False) are treated as unavailable."""
        cost = lookup_call_cost("gpt-4o", True, 500)
        assert cost is None

    def test_bool_output_tokens_returns_none(self) -> None:
        """Bool output token count is treated as unavailable."""
        cost = lookup_call_cost("gpt-4o", 1000, False)
        assert cost is None

    def test_non_numeric_string_tokens_return_none(self) -> None:
        """Non-numeric strings are treated as unavailable (no crash)."""
        cost = lookup_call_cost("gpt-4o", "not-a-number", 500)
        assert cost is None


class TestBuildPricingTable:
    """Tests for build_pricing_table function."""

    def test_default_table_contains_gpt_models(self) -> None:
        table = build_pricing_table()
        assert table.get_price("gpt-4o") is not None
        assert table.get_price("gpt-4o-mini") is not None

    def test_state_dir_pricing_file_overrides(self, tmp_path: Path) -> None:
        obs_dir = tmp_path / "observability"
        obs_dir.mkdir()
        pricing_file = obs_dir / "pricing.json"
        pricing_file.write_text(json.dumps({"custom-model": {"input": 1.0, "output": 2.0}}))

        table = build_pricing_table(state_dir=tmp_path)
        assert table.get_price("custom-model") is not None
        # Default still available
        assert table.get_price("gpt-4o") is not None

    def test_env_var_pricing_file_overrides(self, tmp_path: Path) -> None:
        pricing_file = tmp_path / "custom-pricing.json"
        pricing_file.write_text(json.dumps({"env-model": {"input": 5.0, "output": 10.0}}))

        with patch.dict("os.environ", {"AGDT_LLM_PRICING_FILE": str(pricing_file)}):
            table = build_pricing_table()
        assert table.get_price("env-model") is not None

    def test_missing_pricing_file_uses_defaults(self, tmp_path: Path) -> None:
        table = build_pricing_table(state_dir=tmp_path)
        # No pricing.json exists, should still have defaults
        assert table.get_price("gpt-4o") is not None

    def test_invalid_json_falls_back_to_defaults(self, tmp_path: Path) -> None:
        obs_dir = tmp_path / "observability"
        obs_dir.mkdir()
        pricing_file = obs_dir / "pricing.json"
        pricing_file.write_text("not valid json {{{")

        table = build_pricing_table(state_dir=tmp_path)
        assert table.get_price("gpt-4o") is not None

    def test_partial_valid_entries_accepted(self, tmp_path: Path) -> None:
        obs_dir = tmp_path / "observability"
        obs_dir.mkdir()
        pricing_file = obs_dir / "pricing.json"
        pricing_file.write_text(
            json.dumps(
                {
                    "valid-model": {"input": 1.0, "output": 2.0},
                    "invalid-model": {"input": "not-a-number", "output": 2.0},
                    "incomplete-model": {"input": 1.0},
                }
            )
        )

        table = build_pricing_table(state_dir=tmp_path)
        assert table.get_price("valid-model") is not None
        assert table.get_price("invalid-model") is None
        assert table.get_price("incomplete-model") is None

    def test_env_var_nonexistent_file_warning(self, tmp_path: Path) -> None:
        import io
        from unittest.mock import patch as mock_patch

        captured = io.StringIO()
        with mock_patch.dict("os.environ", {"AGDT_LLM_PRICING_FILE": "/nonexistent/file.json"}):
            with mock_patch("sys.stderr", captured):
                table = build_pricing_table()
        assert "does not exist" in captured.getvalue()
        # Still has defaults
        assert table.get_price("gpt-4o") is not None

    def test_pricing_file_not_a_dict_root(self, tmp_path: Path) -> None:
        """Pricing file with non-dict root emits warning, uses defaults."""
        import io
        from unittest.mock import patch as mock_patch

        obs_dir = tmp_path / "observability"
        obs_dir.mkdir()
        pricing_file = obs_dir / "pricing.json"
        pricing_file.write_text(json.dumps(["not", "a", "dict"]))

        captured = io.StringIO()
        with mock_patch("sys.stderr", captured):
            table = build_pricing_table(state_dir=tmp_path)
        assert "not a JSON object" in captured.getvalue()
        assert table.get_price("gpt-4o") is not None

    def test_pricing_file_non_dict_entry_skipped(self, tmp_path: Path) -> None:
        """Pricing file with non-dict entry emits warning and skips it."""
        import io
        from unittest.mock import patch as mock_patch

        obs_dir = tmp_path / "observability"
        obs_dir.mkdir()
        pricing_file = obs_dir / "pricing.json"
        pricing_file.write_text(json.dumps({"bad-model": "not-a-dict", "ok-model": {"input": 1.0, "output": 2.0}}))

        captured = io.StringIO()
        with mock_patch("sys.stderr", captured):
            table = build_pricing_table(state_dir=tmp_path)
        assert "Skipping invalid" in captured.getvalue()
        assert table.get_price("ok-model") is not None

    def test_negative_input_rate_skipped(self, tmp_path: Path) -> None:
        """Pricing entry with negative input rate is skipped with a warning."""
        import io
        from unittest.mock import patch as mock_patch

        obs_dir = tmp_path / "observability"
        obs_dir.mkdir()
        pricing_file = obs_dir / "pricing.json"
        pricing_file.write_text(json.dumps({"bad-model": {"input": -1.0, "output": 2.0}}))

        captured = io.StringIO()
        with mock_patch("sys.stderr", captured):
            table = build_pricing_table(state_dir=tmp_path)
        assert "Skipping negative" in captured.getvalue()
        assert table.get_price("bad-model") is None

    def test_negative_output_rate_skipped(self, tmp_path: Path) -> None:
        """Pricing entry with negative output rate is skipped with a warning."""
        import io
        from unittest.mock import patch as mock_patch

        obs_dir = tmp_path / "observability"
        obs_dir.mkdir()
        pricing_file = obs_dir / "pricing.json"
        pricing_file.write_text(json.dumps({"bad-model": {"input": 1.0, "output": -5.0}}))

        captured = io.StringIO()
        with mock_patch("sys.stderr", captured):
            table = build_pricing_table(state_dir=tmp_path)
        assert "Skipping negative" in captured.getvalue()
        assert table.get_price("bad-model") is None

    def test_zero_rates_accepted(self, tmp_path: Path) -> None:
        """Pricing entry with zero rates is valid (free tier models)."""
        obs_dir = tmp_path / "observability"
        obs_dir.mkdir()
        pricing_file = obs_dir / "pricing.json"
        pricing_file.write_text(json.dumps({"free-model": {"input": 0.0, "output": 0.0}}))

        table = build_pricing_table(state_dir=tmp_path)
        assert table.get_price("free-model") is not None

    def test_boolean_input_rate_rejected(self, tmp_path: Path) -> None:
        """Pricing entry with boolean input rate is rejected with a warning."""
        import io
        from unittest.mock import patch as mock_patch

        obs_dir = tmp_path / "observability"
        obs_dir.mkdir()
        pricing_file = obs_dir / "pricing.json"
        # True would silently become 1.0 without the bool guard
        pricing_file.write_text(json.dumps({"bool-model": {"input": True, "output": 2.0}}))

        captured = io.StringIO()
        with mock_patch("sys.stderr", captured):
            table = build_pricing_table(state_dir=tmp_path)
        assert "boolean" in captured.getvalue()
        assert table.get_price("bool-model") is None

    def test_boolean_output_rate_rejected(self, tmp_path: Path) -> None:
        """Pricing entry with boolean output rate is rejected with a warning."""
        import io
        from unittest.mock import patch as mock_patch

        obs_dir = tmp_path / "observability"
        obs_dir.mkdir()
        pricing_file = obs_dir / "pricing.json"
        # False would silently become 0.0 without the bool guard
        pricing_file.write_text(json.dumps({"bool-model": {"input": 1.0, "output": False}}))

        captured = io.StringIO()
        with mock_patch("sys.stderr", captured):
            table = build_pricing_table(state_dir=tmp_path)
        assert "boolean" in captured.getvalue()
        assert table.get_price("bool-model") is None

    def test_boolean_rates_skipped_valid_entry_accepted(self, tmp_path: Path) -> None:
        """Boolean entry is skipped but neighbouring valid entries are still accepted."""
        import io
        from unittest.mock import patch as mock_patch

        obs_dir = tmp_path / "observability"
        obs_dir.mkdir()
        pricing_file = obs_dir / "pricing.json"
        pricing_file.write_text(
            json.dumps(
                {
                    "bool-model": {"input": True, "output": False},
                    "valid-model": {"input": 1.0, "output": 2.0},
                }
            )
        )

        captured = io.StringIO()
        with mock_patch("sys.stderr", captured):
            table = build_pricing_table(state_dir=tmp_path)
        assert "boolean" in captured.getvalue()
        assert table.get_price("bool-model") is None
        assert table.get_price("valid-model") is not None


class TestResolvePricingOverrides:
    """Tests for _resolve_pricing_overrides function."""

    def test_returns_empty_when_no_overrides(self, tmp_path: Path) -> None:
        from agentic_devtools.orchestration.observability_pricing import (
            _resolve_pricing_overrides,
        )

        result = _resolve_pricing_overrides(state_dir=tmp_path)
        assert result == {}

    def test_returns_state_dir_overrides(self, tmp_path: Path) -> None:
        from agentic_devtools.orchestration.observability_pricing import (
            _resolve_pricing_overrides,
        )

        obs_dir = tmp_path / "observability"
        obs_dir.mkdir()
        pricing_file = obs_dir / "pricing.json"
        pricing_file.write_text(json.dumps({"custom": {"input": 1.0, "output": 2.0}}))

        result = _resolve_pricing_overrides(state_dir=tmp_path)
        assert "custom" in result

    def test_returns_env_var_overrides(self, tmp_path: Path) -> None:
        from agentic_devtools.orchestration.observability_pricing import (
            _resolve_pricing_overrides,
        )

        pricing_file = tmp_path / "env-pricing.json"
        pricing_file.write_text(json.dumps({"env-model": {"input": 3.0, "output": 4.0}}))

        with patch.dict("os.environ", {"AGDT_LLM_PRICING_FILE": str(pricing_file)}):
            result = _resolve_pricing_overrides()
        assert "env-model" in result

    def test_returns_empty_when_no_state_dir(self) -> None:
        from agentic_devtools.orchestration.observability_pricing import (
            _resolve_pricing_overrides,
        )

        with patch.dict("os.environ", {}, clear=True):
            result = _resolve_pricing_overrides(state_dir=None)
        assert result == {}

    def test_env_var_nonexistent_file_returns_empty(self) -> None:
        from agentic_devtools.orchestration.observability_pricing import (
            _resolve_pricing_overrides,
        )

        with patch.dict("os.environ", {"AGDT_LLM_PRICING_FILE": "/nonexistent/file.json"}):
            result = _resolve_pricing_overrides()
        assert result == {}
