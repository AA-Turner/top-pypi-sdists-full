from marshmallow import Schema, fields
from ...utils.utils import Safe13FDate


class Submission13FSchema(Schema):
    ACCESSION_NUMBER = fields.String(required=True)
    FILING_DATE = Safe13FDate(required=True)
    SUBMISSIONTYPE = fields.String(required=True)
    CIK = fields.String(required=True)
    PERIODOFREPORT = Safe13FDate(required=True)
