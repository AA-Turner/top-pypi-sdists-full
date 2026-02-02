from marshmallow import Schema, fields


class PipelineDrugPortfolioSchema(Schema):
    id = fields.Int(dump_only=True)
    session_id = fields.Int(required=True)
    page_id = fields.Int(required=True)
    company_sec_id = fields.Int(allow_none=True)
    company_ous_id = fields.Int(allow_none=True)
    drug_name = fields.Str(required=True)
    drug_name_normalized = fields.Str(allow_none=True)
    synonyms = fields.Raw(allow_none=True)  # JSON array
    modality = fields.Str(allow_none=True)
    targets = fields.Raw(allow_none=True)  # JSON array
    mechanism_of_action = fields.Str(allow_none=True)
    indications = fields.Raw(required=True)  # JSON array
    additional_info = fields.Raw(allow_none=True)  # JSON object
    extraction_method = fields.Str(required=True)
    extraction_confidence = fields.Float(allow_none=True)
    raw_extraction_text = fields.Str(allow_none=True)
    is_verified = fields.Bool(allow_none=True)
    is_duplicate = fields.Bool(allow_none=True)
    needs_review = fields.Bool(allow_none=True)
    review_notes = fields.Str(allow_none=True)
    extracted_at = fields.DateTime(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class PipelineDrugPortfolioResourceSchema(PipelineDrugPortfolioSchema):
    pass
