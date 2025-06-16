from sqlalchemy import Column, Integer, String
from maleo_metadata.db import MaleoMetadataMetadataManager
from maleo_foundation.models.table import DataTable, AccessTable

class UserTypesMixin:
    order = Column(name="order", type_=Integer)
    key = Column(name="key", type_=String(20), unique=True, nullable=False)
    name = Column(name="name", type_=String(20), unique=True, nullable=False)

class UserTypesTable(
    UserTypesMixin,
    DataTable,
    MaleoMetadataMetadataManager.Base
):
    __tablename__ = "user_types"

class UserTypesAccessTable(
    UserTypesMixin,
    AccessTable,
    MaleoMetadataMetadataManager.Base
):
    __tablename__ = "user_types_access"