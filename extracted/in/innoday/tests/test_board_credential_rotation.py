"""Tests for the PATCH .../boards/{board_id}/credential rotation endpoint."""

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from fastapi import HTTPException

from src.domain.board import BoardRegistration, BoardType


@pytest.fixture
def board_registration(db_session, org, project):
    b = BoardRegistration(
        id=str(uuid4()),
        organization_id=org.id,
        project_id=project.id,
        board_name="Test Board",
        board_type=BoardType.JIRA,
        board_url="https://example.atlassian.net",
        board_external_id="1",
    )
    db_session.add(b)
    db_session.commit()
    db_session.refresh(b)
    return b


@pytest.mark.asyncio
async def test_rotates_credential_after_validating_new_token(
    db_session, org, board_registration
):
    from src.routers.boards import update_board_credential

    current_user = MagicMock()
    current_user.id = "test-user"

    with (
        patch("src.routers.boards.require_org_role"),
        patch(
            "src.routers.boards.validate_board_access", new=AsyncMock(return_value=True)
        ),
        patch("src.routers.boards.set_board_credential") as mock_set_cred,
    ):
        result = await update_board_credential(
            organization_id=org.id,
            board_id=board_registration.id,
            token="new-email@example.com:new-api-token",
            session=db_session,
            current_user=current_user,
        )

    mock_set_cred.assert_called_once_with(
        db_session,
        board_registration.id,
        org.id,
        BoardType.JIRA,
        {"email": "new-email@example.com", "api_token": "new-api-token"},
    )
    assert result.board_id == board_registration.id
    assert result.board_type == BoardType.JIRA


@pytest.mark.asyncio
async def test_rejects_invalid_token_without_persisting(
    db_session, org, board_registration
):
    from src.routers.boards import update_board_credential

    current_user = MagicMock()
    current_user.id = "test-user"

    with (
        patch("src.routers.boards.require_org_role"),
        patch(
            "src.routers.boards.validate_board_access",
            new=AsyncMock(return_value=False),
        ),
        patch("src.routers.boards.set_board_credential") as mock_set_cred,
    ):
        with pytest.raises(HTTPException) as exc_info:
            await update_board_credential(
                organization_id=org.id,
                board_id=board_registration.id,
                token="bad-token",
                session=db_session,
                current_user=current_user,
            )

    assert exc_info.value.status_code == 403
    mock_set_cred.assert_not_called()


@pytest.mark.asyncio
async def test_404_for_unknown_board(db_session, org):
    from src.routers.boards import update_board_credential

    current_user = MagicMock()
    current_user.id = "test-user"

    with pytest.raises(HTTPException) as exc_info:
        await update_board_credential(
            organization_id=org.id,
            board_id="does-not-exist",
            token="whatever:token",
            session=db_session,
            current_user=current_user,
        )

    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_does_not_reject_when_board_already_registered(
    db_session, org, board_registration
):
    """Unlike register_board (409 on an existing board), rotating the
    credential for an already-registered board is exactly the point."""
    from src.routers.boards import update_board_credential

    current_user = MagicMock()
    current_user.id = "test-user"

    with (
        patch("src.routers.boards.require_org_role"),
        patch(
            "src.routers.boards.validate_board_access", new=AsyncMock(return_value=True)
        ),
        patch("src.routers.boards.set_board_credential"),
    ):
        result = await update_board_credential(
            organization_id=org.id,
            board_id=board_registration.id,
            token="rotated@example.com:rotated-token",
            session=db_session,
            current_user=current_user,
        )

    assert result.board_id == board_registration.id
