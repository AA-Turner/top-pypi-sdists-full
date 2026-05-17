"""Regression matrix: every provider sage exposes must surface ONLY models
that can actually respond to a real task.

The 2026-05-16 probe exposed two failure modes:

1. The cloud provider listed 8 models but only 3 had a deployed URL — the
   other 5 returned `RUNTIME_ERROR` every time a user picked them.
   Fixed by filtering `SageHostedProvider.list_models()` against
   `model_servers/model_registry.json`.

2. sage's hosted error path surfaced the error CODE ("RUNTIME_ERROR")
   instead of the human MESSAGE. Fixed by preferring `detail.message`
   over `detail.error` in `sage_hosted._raise_for_status`.

These tests pin both fixes in. Future contributors who add an undeployed
model to the cloud catalog will see this test fail.
"""

from __future__ import annotations

import json
from pathlib import Path

from sage.providers.sage_hosted import SageHostedProvider, _deployed_model_tags


REGISTRY = (
    Path(__file__).resolve().parent.parent.parent
    / "model_servers" / "model_registry.json"
)


class TestCloudCatalogMatchesDeployment:
    def test_list_models_returns_only_deployed(self) -> None:
        """Every model in `list_models()` MUST have a non-null URL in the
        registry. If we ever ship a model that's listed but not deployed,
        the user gets RUNTIME_ERROR every time they pick it."""
        provider = SageHostedProvider()
        listed_tags = {m.id.removeprefix("cloud:") for m in provider.list_models()}
        deployed = _deployed_model_tags()
        if deployed is None:
            return  # registry not packaged — fail open, nothing to verify
        # listed must be a SUBSET of deployed
        not_deployed_but_listed = listed_tags - deployed
        assert not not_deployed_but_listed, (
            f"Cloud catalog exposes models without a deployed URL: "
            f"{sorted(not_deployed_but_listed)}. Either deploy them or "
            f"remove the ModelInfo entry."
        )

    def test_deployed_tags_is_non_empty(self) -> None:
        """If the registry has zero deployed entries something is very wrong."""
        deployed = _deployed_model_tags()
        if deployed is None:
            return  # registry not packaged
        assert deployed, "model_registry.json has no deployed URLs."

    def test_registry_does_not_index_comments_as_models(self) -> None:
        """`_comment` and other underscore keys must be filtered out."""
        deployed = _deployed_model_tags()
        if deployed is None:
            return
        underscore_leaks = [t for t in deployed if t.startswith("_")]
        assert not underscore_leaks, (
            f"Registry helper indexed metadata keys as deployed models: "
            f"{underscore_leaks}"
        )


class TestErrorMessagesAreHumanReadable:
    def test_sage_hosted_prefers_message_over_code(self) -> None:
        """`detail.message` must win over `detail.error` (the taxonomy code)
        so users see actual reasons, not 'RUNTIME_ERROR'.

        This is the literal bug the probe surfaced: the backend returns
        `{"error": "RUNTIME_ERROR", "message": "Cloud model X is not
        deployed"}` and we used to show only "RUNTIME_ERROR".
        """
        import httpx
        provider = SageHostedProvider()

        class _StubResponse:
            status_code = 500
            headers: dict = {}
            is_success = False
            def read(self): pass
            def json(self):
                return {"detail": {
                    "error": "RUNTIME_ERROR",
                    "message": "Cloud model 'gemma-2-9b' is not deployed.",
                    "details": {},
                }}
            text = ""

        try:
            provider._raise_for_status(_StubResponse())
        except RuntimeError as exc:
            assert "not deployed" in str(exc), (
                f"Error string lost the human message; got: {exc}"
            )
        else:
            raise AssertionError("provider._raise_for_status should have raised")


class TestAdminAllowlist:
    """The admin allowlist gates free unlimited access. Regression test so
    future edits don't accidentally drop a name."""

    def test_known_admins_are_admin(self) -> None:
        from backend.billing import is_admin
        assert is_admin("laynefaler@gmail.com")
        assert is_admin("liamfaler@gmail.com")
        assert is_admin("LAYNEFALER@GMAIL.COM")  # case-insensitive

    def test_non_admin_is_not_admin(self) -> None:
        from backend.billing import is_admin
        assert not is_admin("randomuser@example.com")
        assert not is_admin(None)
        assert not is_admin("")
