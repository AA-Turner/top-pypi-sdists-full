from sqlalchemy import Column, Integer, String
from maleo_metadata.db import MaleoMetadataMetadataManager
from maleo_foundation.models.table import DataTable, AccessTable

class OrganizationTypesMixin:
    order = Column(name="order", type_=Integer)
    key = Column(name="key", type_=String(20), unique=True, nullable=False)
    name = Column(name="name", type_=String(20), unique=True, nullable=False)

class OrganizationTypesTable(
    OrganizationTypesMixin,
    DataTable,
    MaleoMetadataMetadataManager.Base
):
    __tablename__ = "organization_types"

class OrganizationTypesAccessTable(
    OrganizationTypesMixin,
    AccessTable,
    MaleoMetadataMetadataManager.Base
):
    __tablename__ = "organization_types_access"