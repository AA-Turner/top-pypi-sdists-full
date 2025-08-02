from marshmallow import (
    Schema,
    fields,
    validate,
)


class PubmedUserDocumentResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    pubmed_id = fields.Integer(required=True)
    user_document_id = fields.Integer(required=True)
    is_deleted = fields.Boolean(allow_none=True)
    updated_at = fields.DateTime()
