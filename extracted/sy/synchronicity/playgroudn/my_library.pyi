import typing
import typing_extensions

class __foo_spec(typing_extensions.Protocol):
    def __call__(self) -> typing.Generator[int, None, None]:
        ...

    def aio(self) -> typing.AsyncGenerator[int, None]:
        ...

foo: __foo_spec
