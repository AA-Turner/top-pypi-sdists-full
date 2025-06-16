from sqlalchemy import Column, Integer, UUID, String, Enum
from uuid import uuid4
from maleo_foundation.enums import BaseEnums
from maleo_metadata.db import MaleoMetadataMetadataManager
from maleo_foundation.models.table import DataTable, AccessTable

class ServicesMixin:
    order = Column(name="order", type_=Integer)
    type = Column(
        name="type",
        type_=Enum(BaseEnums.ServiceType, name="service_type"),
        nullable=False
    )
    category = Column(
        name="category",
        type_=Enum(BaseEnums.ServiceCategory, name="service_category"),
        nullable=False
    )
    key = Column(name="key", type_=String(20), unique=True, nullable=False)
    name = Column(name="name", type_=String(20), unique=True, nullable=False)
    secret = Column(name="secret", type_=UUID, default=uuid4, unique=True, nullable=False)

class ServicesTable(
    ServicesMixin,
    DataTable,
    MaleoMetadataMetadataManager.Base
):
    __tablename__ = "services"

class ServicesAccessTable(
    ServicesMixin,
    AccessTable,
    MaleoMetadataMetadataManager.Base
):
    __tablename__ = "services_access"