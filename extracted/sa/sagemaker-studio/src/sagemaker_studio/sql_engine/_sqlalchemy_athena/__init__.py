"""Registration for the SDK-owned SQLAlchemy dialect for Amazon Athena."""

from sqlalchemy.dialects import registry

__all__ = ["register_dialect"]


def register_dialect() -> None:
    module = "sagemaker_studio.sql_engine._sqlalchemy_athena.dialect"
    registry.register("awsathena", module, "AthenaDialect")
    registry.register("awsathena.rest", module, "AthenaDialect")


register_dialect()
