from sqlalchemy import Column, Integer, String, PrimaryKeyConstraint
from ...database import Base


class Infotable13FModel(Base):
    __tablename__ = '13finfotable'

    ACCESSION_NUMBER = Column(String(25))
    INFOTABLE_SK = Column(Integer)
    NAMEOFISSUER = Column(String(200), nullable=False)
    TITLEOFCLASS = Column(String(150), nullable=False)
    CUSIP = Column(String(9), nullable=False)
    FIGI = Column(String(12))
    VALUE = Column(Integer, nullable=False)
    SSHPRNAMT = Column(Integer, nullable=False)
    SSHPRNAMTTYPE = Column(String(10), nullable=False)
    PUTCALL = Column(String(10))
    INVESTMENTDISCRETION = Column(String(10), nullable=False)
    OTHERMANAGER = Column(String(100))
    VOTING_AUTH_SOLE = Column(Integer, nullable=False)
    VOTING_AUTH_SHARED = Column(Integer, nullable=False)
    VOTING_AUTH_NONE = Column(Integer, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('ACCESSION_NUMBER', 'INFOTABLE_SK'),
    )
