from sqlalchemy import Column, Integer, String, Date
from ...database import Base


class Othermanager213FModel(Base):
    __tablename__ = '13fothermanager2'

    id = Column(Integer, primary_key=True)
    ACCESSION_NUMBER = Column(String(25), index=True)
    SEQUENCENUMBER = Column(Integer, nullable=False)
    CIK = Column(String(10))
    FORM13FFILENUMBER = Column(String(17))
    CRDNUMBER = Column(String(9))
    SECFILENUMBER = Column(String(17))
    NAME = Column(String(150), nullable=False)
