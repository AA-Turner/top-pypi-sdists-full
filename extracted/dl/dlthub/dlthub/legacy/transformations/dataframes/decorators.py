from typing import Callable, Literal, Union, Any, Generator, List, TYPE_CHECKING

from dataclasses import dataclass
from functools import wraps

if TYPE_CHECKING:
    from duckdb import DuckDBPyConnection
else:
    DuckDBPyConnection = Any


TTransformationMaterialization = Literal["table", "view", "sql"]
TTransformationWriteDisposition = Literal["replace", "append"]


@dataclass
class TransformationUtils:
    make_qualified_input_table_name: Callable[[str], str]
    make_qualified_output_table_name: Callable[[str], str]
    existing_input_tables: Callable[[], List[str]]
    existing_output_tables: Callable[[], List[str]]


TTransformationFunc = Callable[
    [DuckDBPyConnection, TransformationUtils], Union[None, str, Generator[Any, None, None]]
]

TTransformationGroupFunc = Callable[[], List[TTransformationFunc]]


def transformation(
    table_name: str,
    materialization: TTransformationMaterialization = "table",
    write_disposition: TTransformationWriteDisposition = "replace",
) -> Callable[[TTransformationFunc], TTransformationFunc]:
    def decorator(func: TTransformationFunc) -> TTransformationFunc:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Union[None, str, Generator[Any, None, None]]:
            return func(*args, **kwargs)

        # save the arguments to the function
        wrapper.__transformation_args__ = {  # type: ignore
            "table_name": table_name,
            "materialization": materialization,
            "write_disposition": write_disposition,
        }

        return wrapper

    return decorator


def transformation_group(
    name: str,
) -> Callable[[TTransformationGroupFunc], TTransformationGroupFunc]:
    def decorator(func: TTransformationGroupFunc) -> TTransformationGroupFunc:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> List[TTransformationFunc]:
            return func(*args, **kwargs)

        func.__transformation_group_args__ = {  # type: ignore
            "name": name,
        }
        return wrapper

    return decorator
