from __future__ import annotations

from unittest.mock import patch

import pytest
from airbyte.exceptions import PyAirbyteInputError
from airbyte_cloud_cli import workspaces


def test_list_workspaces_requires_organization_id_when_missing() -> None:
    with patch.object(
        workspaces.api_util, "list_workspaces_in_organization"
    ) as list_workspaces, pytest.raises(
        PyAirbyteInputError,
        match=(
            r"Organization ID is required; provide `--organization-id`, "
            r"`AIRBYTE_ORGANIZATION_ID`, "
            r"or `AIRBYTE_CLOUD_ORGANIZATION_ID`."
        ),
    ):
        workspaces.list_()

    list_workspaces.assert_not_called()


def test_list_workspaces_requires_organization_id() -> None:
    with patch.object(
        workspaces.api_util, "list_workspaces_in_organization"
    ) as list_workspaces:
        list_workspaces.return_value = []
        workspaces.list_(organization_id="org-123")

    list_workspaces.assert_called_once()
    assert list_workspaces.call_args.kwargs["organization_id"] == "org-123"
