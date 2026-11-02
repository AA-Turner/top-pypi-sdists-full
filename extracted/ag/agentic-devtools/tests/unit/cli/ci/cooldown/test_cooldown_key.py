"""Tests for cooldown_key()."""

from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.cooldown import cooldown_key


class TestCooldownKey:
    """cooldown_key() derives safe provider/identity keys from configuration."""

    def test_uses_safe_default_and_configured_identity(self) -> None:
        with patch.dict("os.environ", {}, clear=True):
            assert cooldown_key() == "github:GH_TOKEN"

        with patch.dict("os.environ", {"AI_PR_LOOP_CREDENTIAL_IDENTITY": "safe.id"}, clear=True):
            assert cooldown_key() == "github:safe.id"

        with patch.dict("os.environ", {"AI_PR_LOOP_CREDENTIAL_IDENTITY": "bad/key", "GH_TOKEN": "x"}, clear=True):
            assert cooldown_key() == "github:GH_TOKEN"
        with patch.dict("os.environ", {"AI_PR_LOOP_CREDENTIAL_IDENTITY": "bad:identity", "GH_TOKEN": "x"}, clear=True):
            assert cooldown_key() == "github:GH_TOKEN"

    @pytest.mark.parametrize(
        "kwargs",
        [
            {"credential_identity": "bad/key"},
            {"provider": "bad/key"},
            {"credential_identity": "bad:identity"},
            {"provider": "bad:provider"},
        ],
    )
    def test_rejects_invalid_inputs(self, kwargs) -> None:
        with pytest.raises(ValueError, match="safe logical identifier"):
            cooldown_key(**kwargs)

    def test_accepts_max_length_components(self) -> None:
        provider = "p" * 128
        identity = "i" * 128
        assert cooldown_key(identity, provider=provider) == f"{provider}:{identity}"
