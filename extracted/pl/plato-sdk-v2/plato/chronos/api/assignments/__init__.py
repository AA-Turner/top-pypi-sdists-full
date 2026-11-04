"""API endpoints."""

from . import (
    auto_create_assignments,
    batch_create_assignments,
    claim_assignment_api_assignments__assignment_id__claim_post,
    create_assignment_api_assignments_post,
    get_assignment_analytics,
    get_assignment_api_assignments__assignment_id__get,
    list_assignment_types,
    list_assignments_api_assignments_get,
    preview_assignments,
    stream_preview_assignments,
    submit_assignment_api_assignments__assignment_id__submit_post,
    unassign_assignment,
    update_assignment_api_assignments__assignment_id__patch,
)

__all__ = [
    "auto_create_assignments",
    "batch_create_assignments",
    "claim_assignment_api_assignments__assignment_id__claim_post",
    "create_assignment_api_assignments_post",
    "get_assignment_analytics",
    "get_assignment_api_assignments__assignment_id__get",
    "list_assignment_types",
    "list_assignments_api_assignments_get",
    "preview_assignments",
    "stream_preview_assignments",
    "submit_assignment_api_assignments__assignment_id__submit_post",
    "unassign_assignment",
    "update_assignment_api_assignments__assignment_id__patch",
]
