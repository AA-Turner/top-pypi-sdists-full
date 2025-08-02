import json
from marshmallow import (
    Schema,
    fields,
    validate,
)


class MeetingImportantDatesField(fields.Field):
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


class MeetingIndexingStatusField(fields.Field):
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


class MeetingResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    meeting_name = fields.String(required=True)
    start_date = fields.DateTime(required=True)
    end_date = fields.DateTime(required=True)
    title_release_date = fields.DateTime(allow_none=True)
    abstract_release_date = fields.DateTime(allow_none=True)
    from_website = fields.Boolean(allow_none=True)
    meeting_bucket_id = fields.Integer(allow_none=True)
    author_pipeline = fields.Boolean(allow_none=True)
    insights_pipeline = fields.Boolean(allow_none=True)
    important_dates = MeetingImportantDatesField(allow_none=True)
    indexing_status = MeetingIndexingStatusField(allow_none=True)
    status = fields.String(allow_none=True)
    updated_at = fields.DateTime()
