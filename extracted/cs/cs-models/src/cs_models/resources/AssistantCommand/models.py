import enum
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, Text, Boolean
from sqlalchemy.orm import relationship

from ...database import Base


class AssistantCommandTypeEnum(enum.Enum):
    SEARCH = "SEARCH"
    FINAL_ANSWER = "FINAL_ANSWER"
    INTERMEDIATE_ANSWER = "INTERMEDIATE_ANSWER"
    ANSWER = "ANSWER"
    RELEVANCY = "RELEVANCY"
    EXTRACT = "EXTRACT"
    SUMMARIZE = "SUMMARIZE"
    QUESTION_AND_ANSWER = "QUESTION_AND_ANSWER"
    TABLE_GENERATION = "TABLE_GENERATION"
    CHART_GENERATION = "CHART_GENERATION"
    DRUG_LIST = "DRUG_LIST"
    DEAL_LIST = "DEAL_LIST"
    LIST = "LIST"
    SMART_GRID = "SMART_GRID"
    DYNAMIC_TABLE = "DYNAMIC_TABLE"
    FOLLOW_UP_QUESTIONS = "FOLLOW_UP_QUESTIONS"


class AssistantCommandStatusEnum(enum.Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    FAILED = "FAILED"
    SUCCESSFUL = "SUCCESSFUL"


class AssistantCommandModel(Base):
    __tablename__ = "assistant_commands"

    id = Column(Integer, primary_key=True)
    user_query_id = Column(
        Integer,
        ForeignKey("assistant_user_queries.id"),
        nullable=False,
    )
    step_number = Column(Integer, nullable=False)
    type = Column("type", Enum(AssistantCommandTypeEnum))
    status = Column("status", Enum(AssistantCommandStatusEnum))
    label = Column(Text, nullable=False)
    result = Column(Text)
    llm_result = Column(Text)
    error = Column(Text, nullable=True)
    internal_doc = Column(Boolean, nullable=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.utcnow())
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )

    # These are ORM fields. Don't need to be added in the corresponding migration.
    # https://docs.sqlalchemy.org/en/14/orm/tutorial.html#building-a-relationship
    user_query = relationship(
        "AssistantUserQueryModel",
        back_populates="commands",
    )

    def higher_neighbors(self):
        return [x.higher_node for x in self.lower_edges]

    def lower_neighbors(self):
        return [x.lower_node for x in self.higher_edges]
