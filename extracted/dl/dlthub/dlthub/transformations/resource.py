from functools import wraps
from typing import Callable, Any, Optional, Type, Iterator, List
import sqlglot

import dlt
from dlt.common.configuration.inject import get_fun_last_config, get_fun_spec
from dlt.dataset import Dataset, Relation
from dlt.common.typing import TDataItems, TTableHintTemplate
from dlt.common import logger, json
from dlt.common.typing import TDataItem
from dlt.common.schema.typing import TTableSchema
from dlt.common.exceptions import MissingDependencyException
from dlt.common.schema.typing import (
    TAnySchemaColumns,
    TWriteDispositionConfig,
    TColumnNames,
    TSchemaContract,
    TTableFormat,
    TTableReferenceParam,
)
from dlt.common.utils import get_callable_name, simple_repr, without_none

from dlt.extract import DltResource
from dlt.extract.incremental import TIncrementalConfig
from dlt.extract.exceptions import CurrentSourceNotAvailable
from dlt.extract.pipe_iterator import DataItemWithMeta
from dlt.extract.hints import DLT_HINTS_METADATA_KEY, make_hints

from dlthub.transformations.typing import TTransformationFunParams
from dlthub.transformations.exceptions import (
    TransformationException,
    IncompatibleDatasetsException,
    TransformationTypeMismatch,
    UnboundDatasetArgument,
)
from dlthub.transformations.configuration import TransformationConfiguration
from dlthub.common.license.decorators import (
    require_license,
)

try:
    from dlt.helpers.ibis import Expr as IbisExpr
except (ImportError, MissingDependencyException):
    IbisExpr = None

try:
    from dlt.common.libs.pyarrow import pyarrow
except (ImportError, MissingDependencyException):
    pyarrow = None


class DltTransformationResource(DltResource):
    def __init__(self, *args: Any, **kwds: Any) -> None:
        super().__init__(*args, **kwds)

    @property
    def has_dynamic_table_name(self) -> bool:
        return True

    @property
    def has_other_dynamic_hints(self) -> bool:
        return True

    def compute_table_schema(self, item: TDataItem = None, meta: Any = None) -> TTableSchema:
        # if we detect any hints on the item directly, merge them with the existing hints
        schema: TTableSchema = {}
        original_hints = self._hints
        if isinstance(item, dlt.Relation):
            schema = item.schema

        # extract resource hints from arrow metadata if available
        if (
            pyarrow
            and isinstance(item, (pyarrow.Table, pyarrow.RecordBatch))
            and item.schema
            and item.schema.metadata
        ):
            _h = item.schema.metadata.get(DLT_HINTS_METADATA_KEY.encode("utf-8"))
            if _h:
                schema = json.loads(_h.decode("utf-8"))

        if schema:
            # TODO: helper function that does this properly
            # convert schema to hints
            hints = make_hints(columns=schema["columns"])

            # NOTE: by merging in the original hints again,
            # we ensure that the item hints are the lowest priority
            self.merge_hints(hints)
            self.merge_hints(original_hints)

        return super().compute_table_schema(item, meta)

    @property
    def relation(self) -> Relation:
        """Returns the first Relation yielded by this resource. Requires all arguments to the
        transformation function to be bound, including Dataset instances.
        """
        if not self.args_bound:
            raise UnboundDatasetArgument(self.name)
        # evaluate resource to retrieve relation
        iter_ = self.__iter__()
        try:
            rel = iter_.__next__()
            if not isinstance(rel, Relation):
                raise TransformationTypeMismatch(
                    self.name, f"Expected Relation to be yielded, not {type(rel).__name__}"
                )
            return rel
        except StopIteration:
            raise
        finally:
            iter_.close()

    def __repr__(self) -> str:
        kwargs = {
            "name": self.name,
            #  "section": self.section,  should this be explicitly passed?
            "table_name": self._hints.get("table_name"),
            "primary_key": self._hints.get("primary_key"),
            "merge_key": self._hints.get("merge_key"),
            "columns": "{...}" if self._hints.get("columns") else None,
            "parent_table_name": self._hints.get("parent_table_name"),
            "references": "{...}" if self._hints.get("references") else None,
            "nested_hints": "{...}" if self._hints.get("nested_hints") else None,
            "max_table_nesting": self._hints.get("max_table_nesting"),
            "write_disposition": self._hints.get("write_disposition"),
            "table_format": self._hints.get("table_format"),
            "file_format": self._hints.get("file_format"),
            "schema_contract": "{...}" if self._hints.get("schema_contract") else None,
            "incremental": self.incremental,
            "validator": self.validator,
        }
        return simple_repr("@dlt.transformation", **without_none(kwargs))


def make_transformation_resource(
    func: Callable[TTransformationFunParams, Any],
    name: TTableHintTemplate[str],
    table_name: TTableHintTemplate[str],
    write_disposition: TTableHintTemplate[TWriteDispositionConfig],
    columns: TTableHintTemplate[TAnySchemaColumns],
    primary_key: TTableHintTemplate[TColumnNames],
    merge_key: TTableHintTemplate[TColumnNames],
    schema_contract: TTableHintTemplate[TSchemaContract],
    table_format: TTableHintTemplate[TTableFormat],
    references: TTableHintTemplate[TTableReferenceParam],
    selected: bool,
    incremental: Optional[TIncrementalConfig],
    spec: Type[TransformationConfiguration],
    parallelized: bool,
    section: Optional[TTableHintTemplate[str]],
) -> DltTransformationResource:
    resource_name = name if name and not callable(name) else get_callable_name(func)

    if spec and not issubclass(spec, TransformationConfiguration):
        raise TransformationException(
            resource_name,
            "Please derive transformation spec from `TransformationConfiguration`",
        )

    @require_license("dlthub.transformation")
    @wraps(func)
    def transformation_function(*args: Any, **kwargs: Any) -> Iterator[TDataItems]:
        # Collect all datasets from args and kwargs
        all_arg_values = list(args) + list(kwargs.values())
        datasets: List[Dataset] = [arg for arg in all_arg_values if isinstance(arg, Dataset)]

        if len(datasets) == 0:
            raise IncompatibleDatasetsException(
                resource_name,
                "No datasets found in transformation function arguments. Please supply"
                " all used datasets via transformation function arguments.",
            )

        # resolve config
        config: TransformationConfiguration = (
            get_fun_last_config(func) or get_fun_spec(func)()  # type: ignore[assignment]
        )

        # get output dataset if available
        # TODO: decouple transformations from Pipeline implementation
        from dlt.pipeline.exceptions import PipelineConfigMissing

        try:
            schema_name = dlt.current.source().name
            current_pipeline = dlt.current.pipeline()
            current_pipeline.destination_client()  # raises if destination not configured
            output_dataset = current_pipeline.dataset(schema=schema_name)
        except (PipelineConfigMissing, CurrentSourceNotAvailable):
            output_dataset = None

        # determine materialization strategy
        if output_dataset:
            should_materialize = not datasets[0].is_same_physical_destination(output_dataset)
        else:
            logger.info(
                "Cannot reach destination or transformation run outside of pipeline, defaulting to"
                " model extraction for transformation %s",
                resource_name,
            )
            should_materialize = False
        should_materialize = should_materialize or config.always_materialize

        def _process_item(item: TDataItems) -> Iterator[TDataItems]:
            # catch the cases where we get a relation from the transformation function
            if isinstance(item, dlt.Relation):
                relation = item
            # we see if the string is a valid sql query, if so we need a dataset
            elif isinstance(item, str):
                try:
                    sqlglot.parse_one(item)
                    relation = datasets[0](item)
                except sqlglot.errors.ParseError as e:
                    raise TransformationException(
                        resource_name,
                        "Invalid SQL query in transformation function. Please supply a valid SQL"
                        " query via transform function arguments.",
                    ) from e
            elif IbisExpr and isinstance(item, IbisExpr):
                relation = datasets[0](item)
            else:
                # no transformation, just yield this item
                yield item
                return

            if not should_materialize:
                yield relation
            else:
                from dlt.common.libs.pyarrow import add_arrow_metadata

                serialized_hints = json.dumps(relation.schema)
                for chunk in relation.iter_arrow(chunk_size=config.buffer_max_items):
                    yield add_arrow_metadata(chunk, {DLT_HINTS_METADATA_KEY: serialized_hints})

        # support both generator and function
        gen_or_item = func(*args, **kwargs)
        iterable_items = gen_or_item if isinstance(gen_or_item, Iterator) else [gen_or_item]

        for item in iterable_items:
            # unwrap if needed
            meta = None
            if isinstance(item, DataItemWithMeta):
                meta = item.meta
                item = item.data

            for processed_item in _process_item(item):
                yield (DataItemWithMeta(meta, processed_item) if meta else processed_item)

    return dlt.resource(  # type: ignore[return-value]
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
        spec=spec,
        parallelized=parallelized,
        section=section,
        incremental=incremental,
        _impl_cls=DltTransformationResource,
        _base_spec=TransformationConfiguration,
    )(transformation_function)
