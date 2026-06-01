#
# This file is part of Invenio.
# Copyright (C) 2025 CERN.
# Copyright (C) 2026 Graz University of Technology.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Alter datetime columns to utc aware datetime columns."""

from invenio_db.utils import (
    update_table_columns_column_type_to_datetime,
    update_table_columns_column_type_to_utc_datetime,
)

# revision identifiers, used by Alembic.
revision = "74b23178bfbe"
down_revision = "1763728177"
branch_labels = ()
depends_on = None


def upgrade():
    """Upgrade database."""
    for table_name in ["request_metadata", "request_events"]:
        update_table_columns_column_type_to_utc_datetime(table_name, "created")
        update_table_columns_column_type_to_utc_datetime(table_name, "updated")
    update_table_columns_column_type_to_utc_datetime("request_metadata", "expires_at")


def downgrade():
    """Downgrade database."""
    for table_name in ["request_metadata", "request_events"]:
        update_table_columns_column_type_to_datetime(table_name, "created")
        update_table_columns_column_type_to_datetime(table_name, "updated")
    update_table_columns_column_type_to_datetime("request_metadata", "expires_at")
