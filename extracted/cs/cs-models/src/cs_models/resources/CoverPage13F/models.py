from sqlalchemy import Column, Integer, String, Date

from ...database import Base


class Coverpage13FModel(Base):
    __tablename__ = '13fcoverpage'

    ACCESSION_NUMBER = Column(String(25), primary_key=True)
    REPORTCALENDARORQUARTER = Column(Date, nullable=False)
    ISAMENDMENT = Column(String(1))
    AMENDMENTNO = Column(Integer)
    AMENDMENTTYPE = Column(String(20))
    CONFDENIEDEXPIRED = Column(String(1))
    DATEDENIEDEXPIRED = Column(Date)
    DATEREPORTED = Column(Date)
    REASONFORNONCONFIDENTIALITY = Column(String(40))
    FILINGMANAGER_NAME = Column(String(150), nullable=False)
    FILINGMANAGER_STREET1 = Column(String(40))
    FILINGMANAGER_STREET2 = Column(String(40))
    FILINGMANAGER_CITY = Column(String(30))
    FILINGMANAGER_STATEORCOUNTRY = Column(String(2))
    FILINGMANAGER_ZIPCODE = Column(String(10))
    REPORTTYPE = Column(String(30), nullable=False)
    FORM13FFILENUMBER = Column(String(17))
    CRDNUMBER = Column(String(9))
    SECFILENUMBER = Column(String(17))
    PROVIDEINFOFORINSTRUCTION5 = Column(String(1), nullable=False)
    ADDITIONALINFORMATION = Column(String(4000))
