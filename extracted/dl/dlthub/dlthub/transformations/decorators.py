from typing import Callable, Any, overload, Optional, Type

from dlt.common.typing import AnyFun, Generic, TColumnNames, TTableHintTemplate
from dlt.common.schema.typing import (
    TWriteDispositionConfig,
    TAnySchemaColumns,
    TSchemaContract,
    TTableFormat,
    TTableReferenceParam,
)
from dlt.extract.incremental import TIncrementalConfig

from dlthub.transformations.typing import (
    TTransformationFunParams,
)
from dlthub.transformations.resource import (
    make_transformation_resource,
    DltTransformationResource,
)
from dlthub.transformations.configuration import TransformationConfiguration


class TransformationFactory(DltTransformationResource, Generic[TTransformationFunParams]):
    # this class is used only for typing, do not instantiate, do not add docstring
    def __call__(  # type: ignore[override]
        self, *args: TTransformationFunParams.args, **kwargs: TTransformationFunParams.kwargs
    ) -> DltTransformationResource:
        pass


@overload
def transformation(
    func: None = ...,
    /,
    name: TTableHintTemplate[str] = None,
    table_name: TTableHintTemplate[str] = None,
    write_disposition: TTableHintTemplate[TWriteDispositionConfig] = None,
    columns: TTableHintTemplate[TAnySchemaColumns] = None,
    primary_key: TTableHintTemplate[TColumnNames] = None,
    merge_key: TTableHintTemplate[TColumnNames] = None,
    schema_contract: TTableHintTemplate[TSchemaContract] = None,
    table_format: TTableHintTemplate[TTableFormat] = None,
    references: TTableHintTemplate[TTableReferenceParam] = None,
    selected: bool = True,
    incremental: Optional[TIncrementalConfig] = None,
    spec: Type[TransformationConfiguration] = None,
    parallelized: bool = False,
    section: Optional[TTableHintTemplate[str]] = None,
) -> Callable[
    [Callable[TTransformationFunParams, Any]], TransformationFactory[TTransformationFunParams]
]: ...


@overload
def transformation(
    func: Callable[TTransformationFunParams, Any],
    /,
    name: TTableHintTemplate[str] = None,
    table_name: TTableHintTemplate[str] = None,
    write_disposition: TTableHintTemplate[TWriteDispositionConfig] = None,
    columns: TTableHintTemplate[TAnySchemaColumns] = None,
    primary_key: TTableHintTemplate[TColumnNames] = None,
    merge_key: TTableHintTemplate[TColumnNames] = None,
    schema_contract: TTableHintTemplate[TSchemaContract] = None,
    table_format: TTableHintTemplate[TTableFormat] = None,
    references: TTableHintTemplate[TTableReferenceParam] = None,
    selected: bool = True,
    incremental: Optional[TIncrementalConfig] = None,
    spec: Type[TransformationConfiguration] = None,
    parallelized: bool = False,
    section: Optional[TTableHintTemplate[str]] = None,
) -> TransformationFactory[TTransformationFunParams]: ...


def transformation(
    func: Optional[AnyFun] = None,
    /,
    name: TTableHintTemplate[str] = None,
    table_name: TTableHintTemplate[str] = None,
    write_disposition: TTableHintTemplate[TWriteDispositionConfig] = None,
    columns: TTableHintTemplate[TAnySchemaColumns] = None,
    primary_key: TTableHintTemplate[TColumnNames] = None,
    merge_key: TTableHintTemplate[TColumnNames] = None,
    schema_contract: TTableHintTemplate[TSchemaContract] = None,
    table_format: TTableHintTemplate[TTableFormat] = None,
    references: TTableHintTemplate[TTableReferenceParam] = None,
    selected: bool = True,
    incremental: Optional[TIncrementalConfig] = None,
    spec: Type[TransformationConfiguration] = None,
    parallelized: bool = False,
    section: Optional[TTableHintTemplate[str]] = None,
) -> Any:
    """
    Decorator to mark a function as a transformation. Returns a DltTransformation object.
    """

    def decorator(
        f: Callable[TTransformationFunParams, Any],
    ) -> DltTransformationResource:
        return make_transformation_resource(
            f,
            name=name,
            table_name=table_name,
            write_disposition=write_disposition,
            columns=columns,
            primary_key=primary_key,
            merge_key=merge_key,
            schema_contract=schema_contract,
            table_format=table_format,
            references=references,
            selected=selected,
            incremental=incremental,
            spec=spec,
            parallelized=parallelized,
            section=section,
        )

    if func is None:
        return decorator

    return decorator(func)
