from pathlib import Path

import pytest

from airbyte_ops_mcp import internal_team_roster


@pytest.mark.unit
@pytest.mark.parametrize(
    "resolution",
    [
        pytest.param("checkout", id="checkout_csv"),
        pytest.param("api", id="contents_api"),
        pytest.param("empty", id="no_mapping"),
    ],
)
def test_load_github_to_airbyte_io_email_resolution_ladder(
    resolution: str,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    if resolution == "checkout":
        csv_path = tmp_path / "data/github_to_airbyte_io_email.csv"
        csv_path.parent.mkdir()
        csv_path.write_text(
            "github_handle,slack_email\ncheckout-user,checkout@airbyte.io\n"
        )
        monkeypatch.setattr(internal_team_roster, "_REPO_ROOT_CANDIDATES", (tmp_path,))
    else:
        monkeypatch.setattr(internal_team_roster, "_REPO_ROOT_CANDIDATES", ())

    if resolution == "api":

        class Response:
            status_code = 200
            text = "github_handle,slack_email\napi-user,api@airbyte.io\n"

        monkeypatch.setattr(
            internal_team_roster.requests,
            "get",
            lambda *_args, **_kwargs: Response(),
        )

    github_token = "token" if resolution == "api" else None
    expected = {
        "checkout": {"checkout-user": "checkout@airbyte.io"},
        "api": {"api-user": "api@airbyte.io"},
        "empty": {},
    }[resolution]
    assert (
        internal_team_roster._load_github_to_airbyte_io_email(github_token) == expected
    )
