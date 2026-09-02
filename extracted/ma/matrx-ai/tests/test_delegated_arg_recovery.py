"""Regression coverage for schema-proven client-tool argument recovery."""

from matrx_ai.tools._dispatch_util import recover_action_type_alias

USER_PARAMETERS = {
    "type": {"type": "string", "enum": ["confirm", "choice", "notify"]},
    "message": {"type": "string"},
    "level": {"type": "string"},
}


def test_recovers_production_user_action_notify_shape() -> None:
    assert recover_action_type_alias(
        {
            "action": "notify",
            "level": "success",
            "message": "Cerebras + Groq sync complete.",
        },
        USER_PARAMETERS,
    ) == {
        "type": "notify",
        "level": "success",
        "message": "Cerebras + Groq sync complete.",
    }


def test_refuses_unknown_ambiguous_or_canonical_shapes() -> None:
    assert recover_action_type_alias({"action": "delete", "message": "no"}, USER_PARAMETERS) is None
    assert (
        recover_action_type_alias(
            {"type": "notify", "action": "confirm", "message": "ok"},
            USER_PARAMETERS,
        )
        is None
    )
    assert (
        recover_action_type_alias(
            {"action": "notify", "message": "real action"},
            {**USER_PARAMETERS, "action": {"type": "string"}},
        )
        is None
    )
    assert (
        recover_action_type_alias(
            {"questions": [{"type": "confirm", "question": "OK?"}], "action": "notify"},
            USER_PARAMETERS,
        )
        is None
    )
