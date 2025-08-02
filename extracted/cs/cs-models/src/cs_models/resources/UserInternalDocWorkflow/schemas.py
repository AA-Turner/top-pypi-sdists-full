from marshmallow import (
    Schema,
    fields,
)


class UserInternalDocWorkflowResourceSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.String(required=True)
    internal_doc_workflow = fields.String(required=True)
    updated_at = fields.DateTime(dump_only=True)
