import json
from marshmallow import (
    Schema,
    fields,
    validate,
)


class TableFigureCaptionField(fields.Field):
    """Field that stores result for the Assistant command."""

    def _serialize(self, value, attr, obj, **kwargs):
        """
        In the DB, the `result` field is a text field. We persist
        data by performing the following:

        AssistantCommandModel(
            ...
            result=json.dumps({...}),
        )

        So here we need to perform the inverse operation (i.e `json.loads(..)`)
        """
        if value is None:
            return None
        return json.loads(value)

    def _deserialize(self, value, attr, data, **kwargs):
        """
        In the DB, the `result` field is a text field. We persist
        data by performing the following:



        AssistantCommandModel(
            ***AssistantCommandResourceSchema().load({
                ...
                "result": [{"some_key": 1}, {"some_key": 2}],
            }),
        )
        """
        if value is None:
            return None
        return json.dumps(value)


class TableFigureResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    file_id = fields.Integer(required=True)
    source_type = fields.String(required=True)
    source_id = fields.Integer(required=True)
    type = fields.String(required=True)
    label = fields.String(allow_none=True)
    caption = TableFigureCaptionField(required=True, allow_none=True)
    description = fields.String(allow_none=True)
    content = fields.String(allow_none=True)
    link = fields.String(allow_none=True)
    llm_processed = fields.Boolean(allow_none=True)
    updated_at = fields.DateTime()
