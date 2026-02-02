from marshmallow import (
    Schema,
    fields,
)


class AssigneeResourceSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.String(required=True)
    user_name = fields.String(required=True)
    updated_at = fields.DateTime(dump_only=True)
