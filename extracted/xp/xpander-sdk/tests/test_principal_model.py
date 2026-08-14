"""Typed caller principal rides the task input; mirror of dev_utils models/principal.py."""
import pytest
from pydantic import ValidationError

from xpander_sdk.models.principal import Principal, PrincipalKind
from xpander_sdk.modules.tasks.models.task import AgentExecutionInput


def test_kinds_roundtrip() -> None:
    """Every kind survives a dump/validate cycle."""
    for kind in PrincipalKind:
        p = Principal(kind=kind, id="abc-123")
        assert Principal.model_validate(p.model_dump()).kind == kind


def test_id_rejects_colon_and_whitespace() -> None:
    """':' is the vault-key delimiter; whitespace is never a canonical id."""
    for bad in ("a:b", "a b", " ", ""):
        with pytest.raises(ValidationError):
            Principal(kind=PrincipalKind.user, id=bad)


def test_input_carries_and_serializes_principal() -> None:
    """A set principal rides the wire dict; an unset one keeps the legacy shape."""
    inp = AgentExecutionInput(text="hi", principal=Principal(kind=PrincipalKind.api_key, id="client-1"))
    dumped = inp.to_request_dict()
    assert dumped["principal"] == {"kind": "api_key", "id": "client-1", "email": None, "display_name": None}
    assert "principal" not in AgentExecutionInput(text="hi").to_request_dict()
