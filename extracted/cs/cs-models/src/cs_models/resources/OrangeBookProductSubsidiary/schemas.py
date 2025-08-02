from marshmallow import (
    Schema,
    fields,
    validate,
)


class OrangeBookProductSubsidiaryResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    orange_book_product_id = fields.Integer(required=True)
    subsidiary_id = fields.Integer(required=True)
    updated_at = fields.DateTime()
