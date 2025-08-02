from sqlalchemy import Column, Integer, String, Date
from ...database import Base


class Signature13FModel(Base):
    __tablename__ = '13fsignature'

    ACCESSION_NUMBER = Column(String(25), primary_key=True)
    NAME = Column(String(150), nullable=False)
    TITLE = Column(String(60), nullable=False)
    PHONE = Column(String(20))
    SIGNATURE = Column(String(150), nullable=False)
    CITY = Column(String(30), nullable=False)
    STATEORCOUNTRY = Column(String(2), nullable=False)
    SIGNATUREDATE = Column(Date, nullable=False)
