from typing import reveal_type

import wireup


class Db: ...


inst = wireup.instance(Db(), as_type=str)

reveal_type(inst)
container = wireup.create_sync_container(injectables=[])
