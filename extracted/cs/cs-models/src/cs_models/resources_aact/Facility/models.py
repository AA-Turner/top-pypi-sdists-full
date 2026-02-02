from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
)

from ...aact_database import Base


class BriefSummaryModel(Base):
    __tablename__ = 'facilities'
    __table_args__ = (
        {'schema': 'ctgov'},
    )

    id = Column(Integer, primary_key=True)
    nct_id = Column(
        String,
        ForeignKey('ctgov.studies.nct_id'),
        nullable=False,
    )
    status = Column(String)
    name = Column(String)
    city = Column(String)
    state = Column(String)
    zip = Column(String)
    country = Column(String)

    def __repr__(self):
        return "<Facility(id='{}', nct_id='{}', status='{}', name='{}', city='{}', state='{}', zip='{}', country='{}'>"\
            .format(self.id, self.nct_id, self.status, self.name, self.city, self.state, self.zip, self.country)
