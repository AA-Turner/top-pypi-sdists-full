from sqlalchemy import Column, Integer, UUID, TIMESTAMP, Enum, func
from sqlalchemy.orm import declared_attr
from uuid import uuid4
from maleo_foundation.enums import BaseEnums
from maleo_foundation.utils.formatter.case import CaseFormatter

class BaseTable:
    __abstract__ = True

    @declared_attr
    def __tablename__(cls) -> str:
        return CaseFormatter.to_snake_case(cls.__name__)

class DataMixin:
    #* Timestamps
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    deleted_at = Column(TIMESTAMP(timezone=True))
    restored_at = Column(TIMESTAMP(timezone=True))
    deactivated_at = Column(TIMESTAMP(timezone=True))
    activated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    #* Statuses
    status = Column(
        Enum(BaseEnums.StatusType, name="statustype"),
        default=BaseEnums.StatusType.ACTIVE,
        nullable=False
    )

class DataIdentifiers:
    #* Identifiers
    id = Column(Integer, primary_key=True)
    uuid = Column(UUID, default=uuid4, unique=True, nullable=False)

class DataTable(
    DataMixin,
    DataIdentifiers
): pass

class AccessIdentifiers:
    #* Identifiers
    access_id = Column(Integer, primary_key=True)
    access_uuid = Column(UUID, default=uuid4, unique=True, nullable=False)
    accessed_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    accessed_by = Column(Integer, default=0, nullable=False)

class AccessMixin:
    id = Column(Integer)
    uuid = Column(UUID)

class AccessTable(
    DataMixin,
    AccessMixin,
    AccessIdentifiers
): pass