from marshmallow import (
    Schema,
    fields,
    validate,
    pre_load,
    ValidationError,
)


class MergerResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    announcement_date = fields.DateTime(required=True)
    news_id = fields.Integer(required=True)
    target_sec_id = fields.Integer(allow_none=True)
    target_ous_id = fields.Integer(allow_none=True)
    acquirer_sec_id = fields.Integer(allow_none=True)
    acquirer_ous_id = fields.Integer(allow_none=True)
    currency = fields.String(allow_none=True)
    deal_value = fields.Decimal(allow_none=True)
    offer_price = fields.String(allow_none=True)
    dma_file_id = fields.Integer(allow_none=True)
    updated_at = fields.DateTime()

    @pre_load
    def check_target_acquirer_ids(self, in_data, **kwargs):
        if self._get_number_of_target_company_fields(in_data) != 1:
            raise ValidationError('Provide either company_sec_id or '
                                  'company_ous_id for target, not both')
        if self._get_number_of_acquirer_company_fields(in_data) != 1:
            raise ValidationError('Provide either company_sec_id or '
                                  'company_ous_id for acquirer, not both')
        return in_data

    def _get_number_of_target_company_fields(self, in_data, **kwargs):
        result = 0
        if 'target_sec_id' in in_data:
            if in_data['target_sec_id'] is not None:
                result += 1
        if 'target_ous_id' in in_data:
            if in_data['target_ous_id'] is not None:
                result += 1
        return result

    def _get_number_of_acquirer_company_fields(self, in_data, **kwargs):
        result = 0
        if 'acquirer_sec_id' in in_data:
            if in_data['acquirer_sec_id'] is not None:
                result += 1
        if 'acquirer_ous_id' in in_data:
            if in_data['acquirer_ous_id'] is not None:
                result += 1
        return result
