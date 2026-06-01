#
# This file is part of Invenio.
# Copyright (C) 2025 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Add index to `request_events.request_id` FK column."""

from alembic import op

# revision identifiers, used by Alembic.
revision = "1759321170"
down_revision = "a14fa442680f"
branch_labels = ()
depends_on = None


def upgrade():
    """Upgrade database."""
    op.create_index(
        op.f("ix_request_events_request_id"),
        "request_events",
        ["request_id"],
        unique=False,
    )


def downgrade():
    """Downgrade database."""
    op.drop_index(op.f("ix_request_events_request_id"), table_name="request_events")
