# mypy: disable-error-code="assignment"
#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of oarepo-runtime (see http://github.com/oarepo/oarepo-runtime).
#
# oarepo-runtime is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Everyone permissions."""

from __future__ import annotations

from invenio_records_permissions import RecordPermissionPolicy
from invenio_records_permissions.generators import AnyUser, Generator, SystemProcess


class EveryonePermissionPolicy(RecordPermissionPolicy):
    """Record policy for read-only repository."""

    can_search: tuple[Generator, ...] = (SystemProcess(), AnyUser())
    can_read: tuple[Generator, ...] = (SystemProcess(), AnyUser())
    can_create: tuple[Generator, ...] = (SystemProcess(), AnyUser())
    can_update: tuple[Generator, ...] = (SystemProcess(), AnyUser())
    can_delete: tuple[Generator, ...] = (SystemProcess(), AnyUser())
    can_manage: tuple[Generator, ...] = (SystemProcess(), AnyUser())

    can_create_files: tuple[Generator, ...] = (SystemProcess(), AnyUser())
    can_set_content_files: tuple[Generator, ...] = (SystemProcess(), AnyUser())
    can_get_content_files: tuple[Generator, ...] = (SystemProcess(), AnyUser())
    can_commit_files: tuple[Generator, ...] = (SystemProcess(), AnyUser())
    can_read_files: tuple[Generator, ...] = (SystemProcess(), AnyUser())
    can_update_files: tuple[Generator, ...] = (SystemProcess(), AnyUser())
    can_delete_files: tuple[Generator, ...] = (SystemProcess(), AnyUser())
    can_list_files: tuple[Generator, ...] = (SystemProcess(), AnyUser())
    can_manage_files: tuple[Generator, ...] = (SystemProcess(), AnyUser())

    can_edit: tuple[Generator, ...] = (SystemProcess(), AnyUser())
    can_new_version: tuple[Generator, ...] = (SystemProcess(), AnyUser())
    can_search_drafts: tuple[Generator, ...] = (SystemProcess(), AnyUser())
    can_read_draft: tuple[Generator, ...] = (SystemProcess(), AnyUser())
    can_search_versions: tuple[Generator, ...] = (SystemProcess(), AnyUser())
    can_update_draft: tuple[Generator, ...] = (SystemProcess(), AnyUser())
    can_delete_draft: tuple[Generator, ...] = (SystemProcess(), AnyUser())
    can_publish: tuple[Generator, ...] = (SystemProcess(), AnyUser())
    can_draft_create_files: tuple[Generator, ...] = (SystemProcess(), AnyUser())
    can_draft_set_content_files: tuple[Generator, ...] = (SystemProcess(), AnyUser())
    can_draft_get_content_files: tuple[Generator, ...] = (SystemProcess(), AnyUser())
    can_draft_commit_files: tuple[Generator, ...] = (SystemProcess(), AnyUser())
    can_draft_read_files: tuple[Generator, ...] = (SystemProcess(), AnyUser())
    can_draft_update_files: tuple[Generator, ...] = (SystemProcess(), AnyUser())
    can_draft_delete_files: tuple[Generator, ...] = (SystemProcess(), AnyUser())

    can_add_community: tuple[Generator, ...] = (SystemProcess(), AnyUser())
    can_remove_community: tuple[Generator, ...] = (SystemProcess(), AnyUser())

    can_read_deleted: tuple[Generator, ...] = (SystemProcess(), AnyUser())
    can_manage_record_access: tuple[Generator, ...] = (SystemProcess(), AnyUser())
    can_lift_embargo: tuple[Generator, ...] = (SystemProcess(), AnyUser())

    can_draft_media_create_files: tuple[Generator, ...] = (SystemProcess(), AnyUser())
    can_draft_media_read_files: tuple[Generator, ...] = (SystemProcess(), AnyUser())
    can_draft_media_set_content_files: tuple[Generator, ...] = (
        SystemProcess(),
        AnyUser(),
    )
    can_draft_media_get_content_files: tuple[Generator, ...] = (
        SystemProcess(),
        AnyUser(),
    )
    can_draft_media_commit_files: tuple[Generator, ...] = (SystemProcess(), AnyUser())
    can_draft_media_update_files: tuple[Generator, ...] = (SystemProcess(), AnyUser())
    can_draft_media_delete_files: tuple[Generator, ...] = (SystemProcess(), AnyUser())

    can_media_read_files: tuple[Generator, ...] = (SystemProcess(), AnyUser())
    can_media_get_content_files: tuple[Generator, ...] = (SystemProcess(), AnyUser())
    can_media_create_files: tuple[Generator, ...] = (SystemProcess(), AnyUser())
    can_media_set_content_files: tuple[Generator, ...] = (SystemProcess(), AnyUser())
    can_media_commit_files: tuple[Generator, ...] = (SystemProcess(), AnyUser())
    can_media_update_files: tuple[Generator, ...] = (SystemProcess(), AnyUser())
    can_media_delete_files: tuple[Generator, ...] = (SystemProcess(), AnyUser())
