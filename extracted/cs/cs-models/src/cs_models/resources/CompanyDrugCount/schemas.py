from marshmallow import (
    Schema,
    fields,
)


class CompanyDrugCountResourceSchema(Schema):
    id = fields.Integer(dump_only=True)
    company_id = fields.String(required=True)
    drug_count = fields.Integer(required=True)
    updated_at = fields.DateTime(dump_only=True)