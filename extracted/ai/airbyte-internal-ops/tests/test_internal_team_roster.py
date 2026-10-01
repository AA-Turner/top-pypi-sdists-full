import io
import json
import zipfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from airbyte_ops_mcp import internal_team_roster

_FIXED_NOW = datetime(2026, 5, 3, 12, tzinfo=timezone.utc)
_ROSTER_MEMBER = {"slack_id": "U123"}


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


@pytest.mark.unit
@pytest.mark.parametrize(
    "data, expected_error",
    [
        pytest.param(
            {"generated_at": _FIXED_NOW.isoformat(), "members": [_ROSTER_MEMBER]},
            None,
            id="fresh-valid-roster",
        ),
        pytest.param(
            {"generated_at": _FIXED_NOW.isoformat(), "members": []},
            "members",
            id="empty-members",
        ),
        pytest.param(
            {"members": [_ROSTER_MEMBER]},
            "generated_at",
            id="missing-generated-at",
        ),
        pytest.param(
            {"generated_at": "not-a-timestamp", "members": [_ROSTER_MEMBER]},
            "generated_at",
            id="unparseable-generated-at",
        ),
        pytest.param(
            {
                "generated_at": (_FIXED_NOW - timedelta(hours=49)).isoformat(),
                "members": [_ROSTER_MEMBER],
            },
            "too old",
            id="stale-roster",
        ),
        pytest.param([_ROSTER_MEMBER], "members", id="legacy-bare-list"),
    ],
)
def test_parse_roster_artifact(
    data: object,
    expected_error: str | None,
) -> None:
    if expected_error is None:
        assert internal_team_roster.parse_roster_artifact(data, now=_FIXED_NOW) == [
            _ROSTER_MEMBER
        ]
    else:
        with pytest.raises(RuntimeError, match=expected_error):
            internal_team_roster.parse_roster_artifact(data, now=_FIXED_NOW)


@pytest.mark.unit
def test_download_latest_artifact_selects_newest_non_expired_main_artifact(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    archive_buffer = io.BytesIO()
    members = [{"slack_id": "U123"}]
    with zipfile.ZipFile(archive_buffer, "w") as archive:
        archive.writestr(
            "roster.json",
            json.dumps(
                {
                    "generated_at": datetime.now(timezone.utc).isoformat(),
                    "members": members,
                }
            ),
        )

    artifacts = [
        {
            "expired": True,
            "created_at": "2026-05-04T00:00:00Z",
            "archive_download_url": "https://example.com/expired.zip",
            "workflow_run": {"head_branch": "main"},
        },
        {
            "expired": False,
            "created_at": "2026-05-03T00:00:00Z",
            "archive_download_url": "https://example.com/other-branch.zip",
            "workflow_run": {"head_branch": "feature"},
        },
        {
            "expired": False,
            "created_at": "2026-05-01T00:00:00Z",
            "archive_download_url": "https://example.com/older-main.zip",
            "workflow_run": {"head_branch": "main"},
        },
        {
            "expired": False,
            "created_at": "2026-05-02T00:00:00Z",
            "archive_download_url": "https://example.com/newest-main.zip",
            "workflow_run": {"head_branch": "main"},
        },
    ]
    downloaded_urls: list[str] = []

    class Response:
        def __init__(
            self,
            *,
            json_data: dict[str, object] | None = None,
            content: bytes = b"",
        ) -> None:
            self._json_data = json_data
            self.content = content

        def json(self) -> dict[str, object]:
            assert self._json_data is not None
            return self._json_data

        def raise_for_status(self) -> None:
            pass

    def fake_get(url: str, **kwargs: object) -> Response:
        downloaded_urls.append(url)
        if url.endswith("/actions/artifacts"):
            assert kwargs["params"] == {
                "name": "internal-team-roster",
                "per_page": "100",
            }
            return Response(json_data={"artifacts": artifacts})
        assert url == "https://example.com/newest-main.zip"
        return Response(content=archive_buffer.getvalue())

    monkeypatch.setattr(internal_team_roster.requests, "get", fake_get)

    assert internal_team_roster._download_latest_artifact(token="x") == members
    assert downloaded_urls[-1] == "https://example.com/newest-main.zip"


@pytest.mark.unit
def test_download_latest_artifact_requires_non_expired_main_artifact(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class Response:
        def json(self) -> dict[str, object]:
            return {
                "artifacts": [
                    {
                        "expired": True,
                        "created_at": "2026-05-04T00:00:00Z",
                        "workflow_run": {"head_branch": "main"},
                    },
                    {
                        "expired": False,
                        "created_at": "2026-05-03T00:00:00Z",
                        "workflow_run": {"head_branch": "feature"},
                    },
                ]
            }

        def raise_for_status(self) -> None:
            pass

    monkeypatch.setattr(
        internal_team_roster.requests,
        "get",
        lambda *_args, **_kwargs: Response(),
    )

    with pytest.raises(
        RuntimeError,
        match="No non-expired 'internal-team-roster' artifact from main found",
    ):
        internal_team_roster._download_latest_artifact(token="x")
