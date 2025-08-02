from marshmallow import (
    Schema,
    fields,
)


class UserOrganizationResourceSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.String(required=True)
    organization_id = fields.String(required=True)
    is_deleted = fields.Boolean(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)
