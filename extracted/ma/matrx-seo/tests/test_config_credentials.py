from types import SimpleNamespace

import pytest
from matrx_orm.secrets_battery import SecretNotFoundError
from matrx_orm.secrets_battery import service as battery_service

from matrx_seo.config import battery_credential_resolver
from matrx_seo.contracts import CollectionRequest, SeoCapability


def _request() -> CollectionRequest:
    return CollectionRequest(
        organization_id="org-credential-scope",
        created_by="user-credential-scope",
        capability=SeoCapability.RAW_PROVIDER,
        operation="provider.raw",
        target_ref="credential-test",
        observation_period="2026-07-22",
        credential_keys=("PROVIDER_API_KEY",),
    )


@pytest.mark.asyncio
async def test_battery_resolver_prefers_personal_secret(monkeypatch: pytest.MonkeyPatch) -> None:
    async def personal_secret(user_id: str, key: str, **_kwargs: object) -> SimpleNamespace:
        assert (user_id, key) == ("user-credential-scope", "PROVIDER_API_KEY")
        return SimpleNamespace(is_active=True, value="personal-test-value")

    async def organization_secret(*_args: object, **_kwargs: object) -> SimpleNamespace:
        pytest.fail("organization lookup must not run when a personal secret exists")

    monkeypatch.setattr(battery_service, "get_user_secret", personal_secret)
    monkeypatch.setattr(battery_service, "get_org_secret", organization_secret)

    credential = await battery_credential_resolver(_request(), "provider")

    assert credential.values == {"PROVIDER_API_KEY": "personal-test-value"}


@pytest.mark.asyncio
async def test_battery_resolver_falls_back_to_organization_secret(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def missing_personal(*_args: object, **_kwargs: object) -> None:
        return None

    async def organization_secret(
        organization_id: str,
        key: str,
        **kwargs: object,
    ) -> SimpleNamespace:
        assert (organization_id, key) == ("org-credential-scope", "PROVIDER_API_KEY")
        assert kwargs["user_id"] == "user-credential-scope"
        assert kwargs["is_org_admin"] is False
        return SimpleNamespace(is_active=True, value="organization-test-value")

    monkeypatch.setattr(battery_service, "get_user_secret", missing_personal)
    monkeypatch.setattr(battery_service, "get_org_secret", organization_secret)

    credential = await battery_credential_resolver(_request(), "provider")

    assert credential.values == {"PROVIDER_API_KEY": "organization-test-value"}


@pytest.mark.asyncio
async def test_battery_resolver_names_both_scopes_when_secret_is_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def missing(*_args: object, **_kwargs: object) -> None:
        return None

    monkeypatch.setattr(battery_service, "get_user_secret", missing)
    monkeypatch.setattr(battery_service, "get_org_secret", missing)

    with pytest.raises(SecretNotFoundError) as error:
        await battery_credential_resolver(_request(), "provider")

    message = str(error.value)
    assert "user user-credential-scope" in message
    assert "org org-credential-scope" in message
