from datetime import datetime
from typing import Any

from sqlalchemy import JSON, Column, String
from sqlalchemy.dialects import postgresql

from rock.envhub.database.base import RockEnv


class RockDockerEnv(RockEnv):
    """Docker environment specification model.
    This class defines the database schema for Docker environment specifications.
    It extends the base RockEnv class with Docker-specific fields.
    """

    __tablename__ = "RockDockerEnvs"
    image = Column(String(512), nullable=False)
    owner = Column(String(255), default="")
    create_at = Column(String(64), default=lambda: datetime.now().isoformat())
    update_at = Column(
        String(64), default=lambda: datetime.now().isoformat(), onupdate=lambda: datetime.now().isoformat()
    )
    # PostgreSQL-specific adaptation, other databases use default JSON
    tags = Column(JSON().with_variant(postgresql.JSONB(), "postgresql"), default=list)
    extra_spec = Column(JSON, nullable=True)

    def __repr__(self):
        return f"<DockerEnv(env_name='{self.env_name}', image='{self.image}')>"

    def to_dict(self) -> dict[str, Any]:
        """Convert the Docker environment specification to a dictionary.
        Returns:
            A dictionary representation of the Docker environment specification
            containing all relevant fields.
        """
        return {
            "env_name": self.env_name,
            "image": self.image,
            "owner": self.owner,
            "create_at": self.create_at,
            "update_at": self.update_at,
            "description": self.description,
            "tags": self.tags,
            "extra_spec": self.extra_spec,
        }
