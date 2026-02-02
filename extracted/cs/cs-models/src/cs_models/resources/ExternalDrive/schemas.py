from marshmallow import (
    Schema,
    fields,
)


class ExternalDriveResourceSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.String(required=True)
    org_id = fields.String(allow_none=True)
    webhook_id = fields.String(required=True)
    provider = fields.String(required=True)
    additional_info = fields.String(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)
