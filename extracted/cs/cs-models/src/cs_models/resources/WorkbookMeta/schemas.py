from marshmallow import (
    Schema,
    fields,
)


class WorkbookMetaResourceSchema(Schema):
    workbook_id = fields.Integer(required=True)
    version = fields.Integer(required=True)
