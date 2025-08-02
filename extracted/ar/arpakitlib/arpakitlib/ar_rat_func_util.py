from typing import Any

from pydantic import BaseModel, ConfigDict

from arpakitlib.ar_type_util import NotSet, is_set, is_not_set


class RatFuncRes(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    func_res: Any = NotSet
    func_exception: Exception | None = None

    def raise_for_func_exception(self):
        if self.func_exception is not None:
            raise self.func_exception

    @property
    def has_exception(self) -> bool:
        if self.func_exception is not None:
            return True
        return False

    @property
    def is_func_res_set(self) -> bool:
        return is_set(self.func_res)

    @property
    def is_func_res_not_set(self) -> bool:
        return is_not_set(self.func_res)


def rat_sync_func(
        *,
        sync_func: Any,
        sync_func_args: tuple[Any, ...] | None = None,
        sync_func_kwargs: dict[str, Any] | None = None,
) -> RatFuncRes:
    sync_func_args = sync_func_args or ()
    sync_func_kwargs = sync_func_kwargs or {}
    rat_func_res = RatFuncRes()
    try:
        rat_func_res.func_res = sync_func(*sync_func_args, **sync_func_kwargs)
    except Exception as exception:
        rat_func_res.func_exception = exception
    return rat_func_res


async def rat_async_func(
        *,
        async_func: Any,
        async_func_args: tuple[Any, ...] | None = None,
        async_func_kwargs: dict[str, Any] | None = None,
) -> RatFuncRes:
    async_func_args = async_func_args or ()
    async_func_kwargs = async_func_kwargs or {}
    rat_func_res = RatFuncRes()
    try:
        rat_func_res.func_res = await async_func(*async_func_args, **async_func_kwargs)
    except Exception as exception:
        rat_func_res.func_exception = exception
    return rat_func_res


def __example():
    def go():
        return "go"

    a = rat_sync_func(sync_func=go)
    print(a.has_exception)
    print(a)
    print(a.is_func_res_set)
    print(a.is_func_res_not_set)


if __name__ == '__main__':
    __example()
