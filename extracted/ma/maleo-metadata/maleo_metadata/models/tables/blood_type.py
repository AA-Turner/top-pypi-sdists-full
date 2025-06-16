from sqlalchemy import Column, Integer, String
from maleo_metadata.db import MaleoMetadataMetadataManager
from maleo_foundation.models.table import DataTable, AccessTable

class BloodTypesMixin:
    order = Column(name="order", type_=Integer)
    key = Column(name="key", type_=String(2), unique=True, nullable=False)
    name = Column(name="name", type_=String(2), unique=True, nullable=False)

class BloodTypesTable(
    BloodTypesMixin,
    DataTable,
    MaleoMetadataMetadataManager.Base
):
    __tablename__ = "blood_types"

class BloodTypesAccessTable(
    BloodTypesMixin,
    AccessTable,
    MaleoMetadataMetadataManager.Base
):
    __tablename__ = "blood_types_access"