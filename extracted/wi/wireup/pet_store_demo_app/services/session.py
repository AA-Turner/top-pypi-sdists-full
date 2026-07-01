from __future__ import annotations

from typing_extensions import Annotated

from wireup import Inject, injectable


@injectable(lifetime="scoped")
class SQLAlchemySession:
    def __init__(
        self,
        database_url: Annotated[str, Inject(config="infra.database.url")],
        schema: Annotated[str, Inject(config="infra.database.schema")],
    ) -> None:
        self.database_url = database_url
        self.schema = schema

    def describe(self) -> dict[str, str]:
        return {
            "database_url": self.database_url,
            "schema": self.schema,
            "transaction_state": "open",
        }
