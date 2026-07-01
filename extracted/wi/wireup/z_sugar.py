from dataclasses import dataclass
from typing import Annotated

import wireup
from wireup._annotations import Inject, injectable


class Config:
    def __class_getitem__(cls, params):
        typ, key = params
        return Annotated[typ, Inject(config=key)]


class Qualified:
    def __class_getitem__(cls, params):
        typ, qualifier = params
        return Annotated[typ, Inject(qualifier=qualifier)]


@injectable
@dataclass
class DB:
    host: Config[str, "db.host"]


container = wireup.create_sync_container(injectables=[DB], config={"db.host": "localhost"})

print(container.get(DB))
