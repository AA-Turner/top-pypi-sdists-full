import wireup
from wireup._annotations import Injected, injectable


@injectable(lifetime="scoped")
class Foo: ...


container = wireup.create_sync_container(injectables=[Foo])


@wireup.inject_from_container(container)
def main(foo: Injected[Foo]):
    pass


print(main.__wireup_generated_code__)


with container.override({Foo: 1}):
    print(container.get(Foo))
