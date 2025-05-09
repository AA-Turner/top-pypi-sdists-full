"""DO NOT EDIT THIS FILE!

This file is automatically @generated by githubkit using the follow command:

bash ./scripts/run-codegen.sh

See https://github.com/github/rest-api-description for more information.
"""

from __future__ import annotations

from datetime import datetime
from typing import Union

from pydantic import Field

from githubkit.compat import GitHubModel, model_rebuild
from githubkit.typing import Missing
from githubkit.utils import UNSET


class CodespaceExportDetails(GitHubModel):
    """Fetches information about an export of a codespace.

    An export of a codespace. Also, latest export details for a codespace can be
    fetched with id = latest
    """

    state: Missing[Union[str, None]] = Field(
        default=UNSET, description="State of the latest export"
    )
    completed_at: Missing[Union[datetime, None]] = Field(
        default=UNSET, description="Completion time of the last export operation"
    )
    branch: Missing[Union[str, None]] = Field(
        default=UNSET, description="Name of the exported branch"
    )
    sha: Missing[Union[str, None]] = Field(
        default=UNSET, description="Git commit SHA of the exported branch"
    )
    id: Missing[str] = Field(default=UNSET, description="Id for the export details")
    export_url: Missing[str] = Field(
        default=UNSET, description="Url for fetching export details"
    )
    html_url: Missing[Union[str, None]] = Field(
        default=UNSET, description="Web url for the exported branch"
    )


model_rebuild(CodespaceExportDetails)

__all__ = ("CodespaceExportDetails",)
