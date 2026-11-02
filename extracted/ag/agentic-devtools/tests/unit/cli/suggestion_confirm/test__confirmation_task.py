import pytest

from agentic_devtools.cli.suggestion_confirm import _confirmation_task


@pytest.mark.parametrize(
    ("result", "expected"),
    [
        ({"success": True}, 0),
        ({"success": False, "status": "failed"}, 1),
        ({"success": False, "status": "partial_success"}, 1),
    ],
)
def test_returns_exit_code_from_confirmation_success(
    monkeypatch: pytest.MonkeyPatch, result: dict[str, object], expected: int
) -> None:
    monkeypatch.setattr(
        "agentic_devtools.cli.suggestion_confirm.confirm_suggestion_addressed",
        lambda _request=None: result,
    )

    assert _confirmation_task(request={"provider": "github"}) == expected
