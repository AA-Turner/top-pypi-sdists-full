import asyncio
from typing import Any, AsyncIterator

import wireup
from typing_extensions import Annotated
from wireup._annotations import Injected
from wireup._decorators import inject_from_container_unchecked


@wireup.injectable
class Service: ...


class ServiceScoped: ...


@wireup.injectable(lifetime="scoped")
async def s2() -> AsyncIterator[ServiceScoped]:
    yield ServiceScoped()


container = wireup.create_async_container(injectables=[Service, s2], config={"foo": "bar"})


def m(*args: Any): ...


@inject_from_container_unchecked(lambda: container.enter_scope())
def foo(s: wireup.Injected[Service], s2: Injected[ServiceScoped], bar: Annotated[str, wireup.Inject(config="foo")]):
    return s, s2, bar


print(foo.__wireup_source__)


async def main():
    print(await foo())


if __name__ == "__main__":
    asyncio.run(main())


class Thing:
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass

    def foo(self): ...


thing = Thing()

thing.__call__()
