from sqlalchemy import Column, Integer, String, Date
from ...database import Base


class Submission13FModel(Base):
    __tablename__ = '13fsubmission'

    ACCESSION_NUMBER = Column(String(25), primary_key=True)
    FILING_DATE = Column(Date, nullable=False)
    SUBMISSIONTYPE = Column(String(10), nullable=False)
    CIK = Column(String(10), nullable=False)
    PERIODOFREPORT = Column(Date, nullable=False)
