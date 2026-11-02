from sqlalchemy import Column, String, Text
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """SQLAlchemy 2.0 style declarative base class.
    This class serves as the base for all SQLAlchemy ORM models in the EnvHub system.
    """

    pass


class RockEnv(Base):
    """Base environment specification model.
    This is an abstract base class that defines the common fields for all
    environment specifications. It will not create a database table due to
    its abstract nature.
    """

    __abstract__ = True  # Declare as abstract base class, no table will be created
    env_name = Column(String(255), primary_key=True)
    description = Column(Text, default="")

    def __repr__(self):
        return f"<{self.__class__.__name__}(env_name='{self.env_name}')>"
