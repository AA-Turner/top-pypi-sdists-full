from sqlalchemy import Column, Integer, String
from maleo_metadata.db import MaleoMetadataMetadataManager
from maleo_foundation.models.table import DataTable, AccessTable

class GendersMixin:
    order = Column(name="order", type_=Integer)
    key = Column(name="key", type_=String(20), unique=True, nullable=False)
    name = Column(name="name", type_=String(20), unique=True, nullable=False)

class GendersTable(
    GendersMixin,
    DataTable,
    MaleoMetadataMetadataManager.Base
):
    __tablename__ = "genders"

class GendersAccesssTable(
    GendersMixin,
    AccessTable,
    MaleoMetadataMetadataManager.Base
):
    __tablename__ = "genders_access"