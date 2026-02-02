from marshmallow import (
    Schema,
    fields,
    validate,
)


class DocMarkdownTableResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    artifact_id = fields.String(required=True)
    markdown_table = fields.Integer(required=True)
    markdown_table_description = fields.String(allow_none=True)
    has_table_description = fields.Boolean(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)
