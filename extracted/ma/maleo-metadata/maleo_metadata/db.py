from sqlalchemy.orm import declarative_base
from maleo_foundation.models.table import BaseTable
from maleo_foundation.managers.db import MetadataManager

class MaleoMetadataMetadataManager(MetadataManager):
    Base = declarative_base(cls=BaseTable)