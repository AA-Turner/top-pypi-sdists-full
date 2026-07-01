from dataclasses import dataclass
from typing import Annotated

import wireup
from wireup import Inject, injectable


@dataclass
class DbClient:
    dsn: str


@dataclass
class DbRepository:
    client: DbClient


def make_db_bundle(*, dsn: str, qualifier: str | None = None) -> list[object]:
    @injectable(qualifier=qualifier)
    def db_client_factory() -> DbClient:
        return DbClient(dsn=dsn)

    @injectable(qualifier=qualifier)
    def db_repo_factory(
        client: Annotated[DbClient, Inject(qualifier=qualifier)],
    ) -> DbRepository:
        return DbRepository(client=client)

    return [db_client_factory, db_repo_factory]


primary = make_db_bundle(dsn="postgresql://primary-db")
analytics = make_db_bundle(
    dsn="postgresql://analytics-db",
    qualifier="analytics",
)

container = wireup.create_sync_container(
    injectables=[*primary, *analytics],
)


print(container.get(DbClient))
