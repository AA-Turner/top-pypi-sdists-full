###############################################################################
# (c) Copyright 2021 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
"""Table/object defintions used in the AnalysisProductionsDB"""
from sqlalchemy import (
    ForeignKeyConstraint,
    Integer,
    Column,
    String,
    JSON,
    DateTime,
    func,
    ForeignKey,
    Float,
    UniqueConstraint,
)
from sqlalchemy.orm import declarative_base, relationship, validates
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import expression
from sqlalchemy.types import TypeEngine

Base = declarative_base()
Base.__table_args__ = {
    "mysql_engine": "InnoDB",
    "mysql_charset": "utf8",
}


class utcnow_add_days(expression.FunctionElement):
    """Sqlalchemy function to return a date now() plus 'days_to_add' days.

    Used to set default datetime as NOW() plus some number of days.

    """

    type: TypeEngine = DateTime()
    inherit_cache: bool = True

    def __init__(self, *args, days_to_add, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if not isinstance(days_to_add, int):
            raise TypeError(f"days_to_add must be an int, got {type(days_to_add)}")
        self._days_to_add = days_to_add


@compiles(utcnow_add_days, "mysql")
def mysql_utcnow_add_days(element, compiler, **kw) -> str:
    """Sqlalchemy function for mysql rendering of utcnow_add_days.

    Part of utcnow_add_days.
    """
    return f"DATE_ADD( UTC_TIMESTAMP, INTERVAL {element._days_to_add} DAY)"


@compiles(utcnow_add_days, "sqlite")
def sqlite_utcnow_add_days(element, compiler, **kw) -> str:
    """Sqlalchemy function for sqlite rendering of utcnow_add_days.

    Part of utcnow_add_days.
    """
    return f"DATE(DATETIME('now'), '+{element._days_to_add} days')"


class Request(Base):
    __tablename__ = "ap_requests"

    VALID_STATES = [
        "waiting",
        "active",
        "replicating",
        "ready",
    ]
    request_id = Column(Integer, primary_key=True)
    filetype = Column(String(64), primary_key=True)
    state = Column(String(16), nullable=False, default="waiting")
    progress = Column(Float, nullable=True)
    last_state_update = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),  # pylint: disable=not-callable
        onupdate=func.now(),  # pylint: disable=not-callable
    )

    name = Column(String(256), nullable=False)
    version = Column(String(64), nullable=False)
    auto_tags = relationship("AutoTag", back_populates="request", lazy="selectin")
    # TODO: Use the mutable extension and validate this object better?
    extra_info = Column(JSON(), nullable=False, default=lambda: {"transformations": []})

    @validates("name")
    def convert_lower(self, key, value):
        return value.lower()

    def toDict(self):
        result = {
            "name": self.name,
            "version": self.version,
            "request_id": self.request_id,
            "filetype": self.filetype,
            "state": self.state,
            "last_state_update": self.last_state_update,
            "transformations": self.extra_info["transformations"],
        }
        if self.progress is not None:
            result["progress"] = self.progress
        if "jira_task" in self.extra_info:
            result["jira_task"] = self.extra_info["jira_task"]
        if "merge_request" in self.extra_info:
            result["merge_request"] = self.extra_info["merge_request"]
        return result


class AnalysisSample(Request):
    __tablename__ = "ap_analysis_samples"

    sample_id = Column(Integer, primary_key=True)
    wg = Column(String(16), nullable=False)
    analysis = Column(String(256), nullable=False)
    request_id = Column(Integer, nullable=False)
    filetype = Column(String(64), nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(["request_id", "filetype"], ["ap_requests.request_id", "ap_requests.filetype"]),
    )

    owners = relationship("User", back_populates="sample", lazy="selectin")
    tags = relationship("Tag", back_populates="sample", lazy="selectin")
    publications = relationship("Publication", back_populates="sample", lazy="selectin")

    # Allow this table to be temporally versioned
    validity_start = Column(
        DateTime(timezone=False), nullable=False, server_default=func.now()  # pylint: disable=not-callable
    )
    validity_end = Column(DateTime(timezone=False), nullable=True)

    housekeeping_interaction_due = Column(DateTime(timezone=False), server_default=utcnow_add_days(days_to_add=90))

    @validates("wg", "analysis")
    def convert_lower(self, key, value):
        return value.lower()

    def toDict(self):
        result = Request.toDict(self)
        result.update(
            {
                "wg": self.wg,
                "analysis": self.analysis,
                "sample_id": self.sample_id,
                # TODO: Remove
                "owners": [],
                "validity_start": self.validity_start,
                "validity_end": self.validity_end,
                "housekeeping_interaction_due": self.housekeeping_interaction_due,
                "publications": self.publications or [],
            }
        )
        return result


class User(Base):
    __tablename__ = "ap_users"

    id = Column(Integer, primary_key=True)
    username = Column(String(256), nullable=False)
    sample_id = Column(Integer, ForeignKey("ap_analysis_samples.sample_id"), nullable=False)
    sample = relationship("AnalysisSample", back_populates="owners", lazy="selectin")

    # Allow this table to be temporally versioned
    validity_start = Column(
        DateTime(timezone=False), nullable=False, server_default=func.now()  # pylint: disable=not-callable
    )
    validity_end = Column(DateTime(timezone=False), nullable=True)

    @validates("username")
    def convert_lower(self, key, value):
        return value.lower()


class AnalysisOwner(Base):
    __tablename__ = "ap_analyis_owners"

    wg = Column(String(16), primary_key=True)
    analysis = Column(String(256), primary_key=True)
    username = Column(String(256), primary_key=True)

    @validates("username", "wg", "analysis")
    def convert_lower(self, key, value):
        return value.lower()


class Publication(Base):
    __tablename__ = "ap_publications"

    id = Column(Integer, primary_key=True)
    number = Column(String(64), nullable=False)
    sample_id = Column(Integer, ForeignKey("ap_analysis_samples.sample_id"), nullable=False)
    sample = relationship("AnalysisSample", back_populates="publications", lazy="selectin")

    __table_args__ = (UniqueConstraint("number", "sample_id", name="_pubnumber_sample_id_no_duplicates"),)

    @validates("number")
    def convert_upper(self, key, value):
        return value.upper()


class Tag(Base):
    __tablename__ = "ap_tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    value = Column(String(64), nullable=False)
    sample_id = Column(Integer, ForeignKey("ap_analysis_samples.sample_id"), nullable=False)
    sample = relationship("AnalysisSample", back_populates="tags", lazy="joined")

    # Allow this table to be temporally versioned
    validity_start = Column(
        DateTime(timezone=False), nullable=False, server_default=func.now()  # pylint: disable=not-callable
    )
    validity_end = Column(DateTime(timezone=False), nullable=True)

    @validates("name", "value")
    def convert_lower(self, key, value):
        return value.lower()


class AutoTag(Base):
    __tablename__ = "ap_auto_tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    value = Column(String(64), nullable=False)
    # composite foreign keys
    request_id = Column(Integer, nullable=False)
    filetype = Column(String(64), nullable=False)
    request = relationship("Request", back_populates="auto_tags", lazy="joined", enable_typechecks=False)

    __table_args__ = (
        ForeignKeyConstraint(["request_id", "filetype"], ["ap_requests.request_id", "ap_requests.filetype"]),
    )

    @validates("name", "value")
    def convert_lower(self, key, value):
        return value.lower()
