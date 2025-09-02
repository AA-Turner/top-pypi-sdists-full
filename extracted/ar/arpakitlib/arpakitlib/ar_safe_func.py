# arpakit
import datetime as dt
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from arpakitlib.ar_datetime_util import now_utc_dt

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


class SafeFuncResult(BaseModel):
    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True, from_attributes=True)

    has_exception: bool = False
    func_result: Any = None
    exception: Exception | None = None
    duration: dt.timedelta | None = None
    func_name: str
    args: tuple = Field(default_factory=tuple)
    kwargs: dict = Field(default_factory=dict)

    @property
    def is_ok(self) -> bool:
        if self.has_exception:
            return False
        return True

    def simple_dict_for_json(self) -> dict[str, Any]:
        return {
            "has_exception": self.has_exception,
            "func_result": self.func_result,
            "exception": self.exception,
            "duration": self.duration,
            "duration_total_seconds": self.duration.total_seconds() if self.duration is not None else None,
            "is_ok": self.is_ok
        }


def sync_safely_run_func(*, sync_func, args: tuple | None = None, kwargs: dict | None = None) -> SafeFuncResult:
    if args is None:
        args = tuple()
    if kwargs is None:
        kwargs = {}
    func_start_dt = now_utc_dt()
    try:
        res = sync_func(*args, **kwargs)
        duration = now_utc_dt() - func_start_dt
        return SafeFuncResult(
            has_exception=False,
            func_result=res,
            duration=duration,
            func_name=sync_func.__name__,
            args=args,
            kwargs=kwargs
        )
    except Exception as exception:
        return SafeFuncResult(
            has_exception=True,
            exception=exception,
            func_name=sync_func.__name__,
            args=args,
            kwargs=kwargs
        )


def __example():
    def div(a: int, b: int) -> float:
        return a / b

    # успешный вызов
    ok_result = sync_safely_run_func(sync_func=div, args=(10, 2))
    print("OK result:", ok_result.model_dump())

    # вызов с исключением
    err_result = sync_safely_run_func(sync_func=div, args=(10, 0))
    print("ERR result:", err_result.model_dump())


if __name__ == "__main__":
    __example()
