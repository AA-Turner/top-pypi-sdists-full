from marshmallow import Schema, fields
from ...utils.utils import Safe13FInteger


class Othermanager213FSchema(Schema):
    id = fields.Integer(dump_only=True)
    ACCESSION_NUMBER = fields.String(required=True)
    SEQUENCENUMBER = Safe13FInteger(required=True)
    CIK = fields.String()
    FORM13FFILENUMBER = fields.String()
    CRDNUMBER = fields.String()
    SECFILENUMBER = fields.String()
    NAME = fields.String(required=True)
