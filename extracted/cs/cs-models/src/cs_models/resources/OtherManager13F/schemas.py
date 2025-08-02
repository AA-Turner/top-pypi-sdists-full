from marshmallow import Schema, fields
from ...utils.utils import Safe13FInteger


class Othermanager13FSchema(Schema):
    ACCESSION_NUMBER = fields.String(required=True)
    OTHERMANAGER_SK = Safe13FInteger(required=True)
    CIK = fields.String()
    FORM13FFILENUMBER = fields.String()
    CRDNUMBER = fields.String()
    SECFILENUMBER = fields.String()
    NAME = fields.String(required=True)
