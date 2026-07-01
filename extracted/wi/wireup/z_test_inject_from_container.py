import wireup
from wireup._annotations import Injected, injectable


@injectable
class Foo: ...


container = wireup.create_async_container(injectables=[Foo])


@wireup.inject_from_container(container)
async def main(foo: Injected[Foo]):
    pass


print(main.__wireup_generated_code__)
