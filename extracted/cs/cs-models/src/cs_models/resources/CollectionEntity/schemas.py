from marshmallow import (
    Schema,
    fields,
    validate,
)


class CollectionEntityResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    collection_id = fields.Integer(required=True)
    entity_type = fields.String(required=True)
    entity_id = fields.String(required=True)
    entity_name = fields.String(required=True)
    is_deleted = fields.Boolean(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)
