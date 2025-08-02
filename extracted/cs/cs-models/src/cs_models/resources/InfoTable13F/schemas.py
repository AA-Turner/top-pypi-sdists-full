from marshmallow import Schema, fields
from ...utils.utils import Safe13FInteger


class Infotable13FSchema(Schema):
    ACCESSION_NUMBER = fields.String(required=True)
    INFOTABLE_SK = Safe13FInteger(required=True)
    NAMEOFISSUER = fields.String(required=True)
    TITLEOFCLASS = fields.String(required=True)
    CUSIP = fields.String(required=True)
    FIGI = fields.String()
    VALUE = Safe13FInteger(required=True)
    SSHPRNAMT = Safe13FInteger(required=True)
    SSHPRNAMTTYPE = fields.String(required=True)
    PUTCALL = fields.String()
    INVESTMENTDISCRETION = fields.String(required=True)
    OTHERMANAGER = fields.String()
    VOTING_AUTH_SOLE = Safe13FInteger(required=True)
    VOTING_AUTH_SHARED = Safe13FInteger(required=True)
    VOTING_AUTH_NONE = Safe13FInteger(required=True)
