from typing import NewType, Protocol, reveal_type

import wireup

container = wireup.create_sync_container()


class A: ...


class B(Protocol): ...


C = NewType("C", str)


reveal_type(container.get(A))
reveal_type(container.get(A | None))
reveal_type(container.get(C))
reveal_type(container.get(C | None))
