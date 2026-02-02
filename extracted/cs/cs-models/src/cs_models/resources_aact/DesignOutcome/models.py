from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
)

from ...aact_database import Base


class DesignOutcomeModel(Base):
    __tablename__ = 'design_outcomes'
    __table_args__ = (
        {'schema': 'ctgov'},
    )

    id = Column(Integer, primary_key=True)
    nct_id = Column(
        String,
        ForeignKey('ctgov.studies.nct_id'),
        nullable=False,
    )
    outcome_type = Column(String)
    measure = Column(Text)
    time_frame = Column(Text)
    population = Column(String)
    description = Column(Text)

    def __repr__(self):
        return "<DesignOutcome(id='{}', nct_id='{}', outcome_type='{}', measure='{}', time_frame='{}', population='{}', description='{}'>"\
            .format(self.id, self.nct_id, self.outcome_type, self.measure, self.time_frame, self.population, self.description)
