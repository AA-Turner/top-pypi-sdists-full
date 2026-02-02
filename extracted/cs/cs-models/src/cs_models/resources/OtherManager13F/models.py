from sqlalchemy import Column, Integer, String, PrimaryKeyConstraint
from ...database import Base


class Othermanager13FModel(Base):
    __tablename__ = '13fothermanager'

    ACCESSION_NUMBER = Column(String(25))
    OTHERMANAGER_SK = Column(Integer)
    CIK = Column(String(10))
    FORM13FFILENUMBER = Column(String(17))
    CRDNUMBER = Column(String(9))
    SECFILENUMBER = Column(String(17))
    NAME = Column(String(150), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('ACCESSION_NUMBER', 'OTHERMANAGER_SK'),
    )
