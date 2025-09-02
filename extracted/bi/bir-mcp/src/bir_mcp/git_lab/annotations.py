import inspect
from typing import Annotated

import pydantic

ProjectPathOrUrlType = Annotated[
    str,
    pydantic.Field(
        description=inspect.cleandoc("""
            Either the filesystem-like path to a GitLab project with variable depth, for example:
            "organization/project_name" or "organization/namespace/subgroup/project_name",
            or a full url to a GitLab project in the format:
            "https://{gitlab_domain}/{project_path}/[.git]".
        """)
    ),
]
BranchType = Annotated[
    str,
    pydantic.Field(description="The branch name to fetch files from."),
]
MergeRequestIidType = Annotated[
    int,
    pydantic.Field(
        description=inspect.cleandoc("""
                The internal id of a GitLab merge request, can be extracted from a merge request url
                if it ends in the following suffix: "/-/merge_requests/{merge_request_iid}".
            """)
    ),
]
