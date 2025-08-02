from marshmallow import (
    Schema,
    fields,
    validate,
    pre_load,
    ValidationError,
)


class InterventionDataResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    source_type = fields.String()
    date = fields.DateTime(allow_none=True)
    news_id = fields.Integer(allow_none=True)
    pubmed_id = fields.Integer(allow_none=True)
    company_filing_id = fields.Integer(allow_none=True)
    fda_label_id = fields.Integer(allow_none=True)
    info = fields.String(allow_none=True)
    updated_at = fields.DateTime()

    @pre_load
    def check_resource_info(self, in_data, **kwargs):
        if self._get_number_of_source_fields(in_data) != 1:
            raise ValidationError('Provide only one source info')
        return in_data

    def _get_number_of_source_fields(self, in_data, **kwargs):
        result = 0
        if 'news_id' in in_data:
            if in_data['news_id'] is not None:
                result += 1
        if 'pubmed_id' in in_data:
            if in_data['pubmed_id'] is not None:
                result += 1
        if 'company_filing_id' in in_data:
            if in_data['company_filing_id'] is not None:
                result += 1
        if 'fda_label_id' in in_data:
            if in_data['fda_label_id'] is not None:
                result += 1
        return result
