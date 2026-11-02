from agentic_devtools.adapters.suggestion_confirm import SuggestionConfirmationResult


def test_as_dict_serializes_tuple_diagnostics_as_list() -> None:
    result = SuggestionConfirmationResult(
        success=False,
        provider="github",
        status="partial_success",
        reply_id="reply-id",
        diagnostics=("first", "second"),
    )

    assert result.as_dict() == {
        "success": False,
        "provider": "github",
        "status": "partial_success",
        "reply_id": "reply-id",
        "diagnostics": ["first", "second"],
    }
