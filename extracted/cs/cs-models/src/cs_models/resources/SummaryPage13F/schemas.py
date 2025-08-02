from marshmallow import Schema, fields


class Summarypage13FSchema(Schema):
    ACCESSION_NUMBER = fields.String(required=True)
    OTHERINCLUDEDMANAGERSCOUNT = fields.Integer()
    TABLEENTRYTOTAL = fields.Integer()
    TABLEVALUETOTAL = fields.Integer()
    ISCONFIDENTIALOMITTED = fields.String()
