from marshmallow import Schema, fields
from ...utils.utils import Safe13FDate, Safe13FInteger


class Coverpage13FSchema(Schema):
    ACCESSION_NUMBER = fields.String(required=True)
    REPORTCALENDARORQUARTER = Safe13FDate(required=True)
    ISAMENDMENT = fields.String()
    AMENDMENTNO = Safe13FInteger(allow_none=True)
    AMENDMENTTYPE = fields.String()
    CONFDENIEDEXPIRED = fields.String()
    DATEDENIEDEXPIRED = Safe13FDate(allow_none=True)
    DATEREPORTED = Safe13FDate(allow_none=True)
    REASONFORNONCONFIDENTIALITY = fields.String()
    FILINGMANAGER_NAME = fields.String(required=True)
    FILINGMANAGER_STREET1 = fields.String()
    FILINGMANAGER_STREET2 = fields.String()
    FILINGMANAGER_CITY = fields.String()
    FILINGMANAGER_STATEORCOUNTRY = fields.String()
    FILINGMANAGER_ZIPCODE = fields.String()
    REPORTTYPE = fields.String(required=True)
    FORM13FFILENUMBER = fields.String()
    CRDNUMBER = fields.String()
    SECFILENUMBER = fields.String()
    PROVIDEINFOFORINSTRUCTION5 = fields.String(required=True)
    ADDITIONALINFORMATION = fields.String()

