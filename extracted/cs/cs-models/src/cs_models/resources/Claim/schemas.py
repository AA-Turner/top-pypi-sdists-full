from marshmallow import (
    Schema,
    fields,
    validate,
    pre_load,
    ValidationError,
)


class ClaimResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    patent_id = fields.Integer(allow_none=True)
    patent_application_id = fields.Integer(allow_none=True)
    claim_number = fields.Integer(required=True)
    claim_text = fields.String(required=True, validate=not_blank)
    updated_at = fields.DateTime(dump_only=True)

    @pre_load
    def check_patent_patent_application_ids(self, in_data, **kwargs):
        if self._get_number_of_patent_id_fields(in_data) > 1:
            raise ValidationError('Provide either patent_id or '
                                  'patent_application_id, not both')
        return in_data

    def _get_number_of_patent_id_fields(self, in_data, **kwargs):
        result = 0
        if 'patent_id' in in_data:
            if in_data['patent_id'] is not None:
                result += 1
        if 'patent_application_id' in in_data:
            if in_data['patent_application_id'] is not None:
                result += 1
        return result


class ClaimQueryParamsSchema(Schema):
    id = fields.Integer()
    patent_id = fields.Integer()
    patent_application_id = fields.Integer()
    claim_number = fields.Integer()


class ClaimPatchSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')
    claim_text = fields.String(validate=not_blank)
