#
# Copyright (C) 2025 CERN.
#
# Invenio-Requests is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Create request files table."""

import sqlalchemy as sa
import sqlalchemy_utils
from alembic import op
from sqlalchemy.dialects import mysql, postgresql

# revision identifiers, used by Alembic.
revision = "1763728177"
down_revision = "1759321170"
branch_labels = ()
depends_on = "8ae99b034410"


def upgrade():
    """Upgrade database."""
    op.create_table(
        "request_files",
        sa.Column("id", sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
        sa.Column(
            "json",
            sa.JSON()
            .with_variant(sqlalchemy_utils.types.json.JSONType(), "mysql")
            .with_variant(
                postgresql.JSONB(none_as_null=True, astext_type=sa.Text()), "postgresql"
            )
            .with_variant(sqlalchemy_utils.types.json.JSONType(), "sqlite"),
            nullable=True,
        ),
        sa.Column("version_id", sa.Integer(), nullable=False),
        sa.Column(
            "created",
            sa.DateTime().with_variant(mysql.DATETIME(fsp=6), "mysql"),
            nullable=False,
        ),
        sa.Column(
            "updated",
            sa.DateTime().with_variant(mysql.DATETIME(fsp=6), "mysql"),
            nullable=False,
        ),
        sa.Column(
            "key",
            sa.Text().with_variant(mysql.VARCHAR(length=255), "mysql"),
            nullable=False,
        ),
        sa.Column("record_id", sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
        sa.Column(
            "object_version_id", sqlalchemy_utils.types.uuid.UUIDType(), nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["object_version_id"],
            ["files_object.version_id"],
            name=op.f("fk_request_files_object_version_id_files_object"),
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["record_id"],
            ["request_metadata.id"],
            name=op.f("fk_request_files_record_id_request_metadata"),
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_request_files")),
    )
    op.create_index(
        op.f("ix_request_files_object_version_id"),
        "request_files",
        ["object_version_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_request_files_record_id"), "request_files", ["record_id"], unique=False
    )
    op.create_index(
        "uidx_request_files_record_id_key",
        "request_files",
        ["record_id", "key"],
        unique=True,
    )
    op.add_column(
        "request_metadata",
        sa.Column("bucket_id", sqlalchemy_utils.types.uuid.UUIDType(), nullable=True),
    )
    op.create_index(
        op.f("ix_request_metadata_bucket_id"),
        "request_metadata",
        ["bucket_id"],
        unique=False,
    )
    op.create_foreign_key(
        op.f("fk_request_metadata_bucket_id_files_bucket"),
        "request_metadata",
        "files_bucket",
        ["bucket_id"],
        ["id"],
        ondelete="RESTRICT",
    )


def downgrade():
    """Downgrade database."""
    op.drop_index(op.f("ix_request_metadata_bucket_id"), table_name="request_metadata")
    op.drop_constraint(
        op.f("fk_request_metadata_bucket_id_files_bucket"),
        "request_metadata",
        type_="foreignkey",
    )
    op.drop_column("request_metadata", "bucket_id")
    op.drop_index("uidx_request_files_record_id_key", table_name="request_files")
    op.drop_index(op.f("ix_request_files_record_id"), table_name="request_files")
    op.drop_index(
        op.f("ix_request_files_object_version_id"), table_name="request_files"
    )
    op.drop_table("request_files")
