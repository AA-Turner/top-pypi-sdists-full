from functools import wraps
from typing import Callable, Any, Dict, Optional, Set, Type, Iterator, List, cast
import sqlglot

import dlt
from dlt.common.configuration.inject import get_fun_last_config, get_fun_spec
from dlt.common.destination.reference import describe_dataset_location
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

from dlthub.transformations.typing import TTransformationFunParams, TTransformationDataLocation
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


def _collect_relation_tables(relation: Relation, tables_by_dataset: Dict[str, Set[str]]) -> None:
    """Accumulates the tables read by `relation`, grouped by the dataset each belongs to."""
    schema_map = relation._all_schemas()
    # the relation reads its own dataset unqualified. joins qualify the foreign ones
    primary_dataset = relation._dataset.dataset_name
    expression = relation.sqlglot_expression
    cte_names = {cte.alias_or_name for cte in expression.find_all(sqlglot.exp.CTE)}
    for table in expression.find_all(sqlglot.exp.Table):
        # a CTE is referenced as an unqualified table, so a qualified name of the same spelling is
        # still a real table
        if not table.db and table.name in cte_names:
            continue
        dataset_name = table.db or primary_dataset
        schemas = schema_map.get(dataset_name)
        # keep only tables of a dataset the relation reads, and names one of its schemas knows
        if not schemas or not any(table.name in schema.tables for schema in schemas):
            continue
        tables_by_dataset.setdefault(dataset_name, set()).add(table.name)


def _describe_inputs(
    tables_by_dataset: Dict[str, Set[str]],
    datasets_by_name: Dict[str, Dataset],
    resource_name: str,
    is_materialized: bool,
) -> List[TTransformationDataLocation]:
    """Describes every dataset that was read as one input data location."""
    locations: List[TTransformationDataLocation] = []
    for dataset_name, tables in tables_by_dataset.items():
        dataset = datasets_by_name.get(dataset_name)
        if dataset is None:
            # without the dataset instance there is no client config to describe the location with
            logger.debug(
                "Skipping input lineage for dataset %s of transformation %s: not passed as an"
                " argument",
                dataset_name,
                resource_name,
            )
            continue
        # only the schemas holding the tables that were read, in the dataset's own order so the
        # default schema stays first as it names the dataset
        if tables:
            schemas = [
                schema
                for schema in dataset.schemas
                if any(table in schema.tables for table in tables)
            ]
        else:
            # no table to attribute, so every schema of the dataset describes the location
            schemas = list(dataset.schemas)
        client = dataset.destination_client
        location = cast(
            TTransformationDataLocation,
            describe_dataset_location(
                client.config,
                client.capabilities,
                schemas,
                resource_name,
                sorted(tables),
                dataset.sql_client.dataset_name,
            ),
        )
        location["is_materialized"] = is_materialized
        locations.append(location)
    return locations


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

        if not output_dataset:
            logger.info(
                "Cannot access the destination, or the transformation runs outside a pipeline."
                " dlt uses a model job for transformation %s",
                resource_name,
            )

        def _materializes(relation: Relation) -> bool:
            """Tells if dlt must run `relation` here, and not send it as a model job."""

            if config.always_materialize or not output_dataset:
                return config.always_materialize
            return not output_dataset.destination_client.config.can_write_from(
                relation._dataset.destination_client.config
            )

        # a transformation takes all its datasets as arguments. an index by name lets lineage
        # attach the destination of each source
        datasets_by_name = {ds.dataset_name: ds for ds in datasets}

        try:
            current_resource = dlt.current.resource()
        except CurrentSourceNotAvailable:
            current_resource = None

        tables_by_dataset: Dict[str, Set[str]] = {}
        tables_unknown = False
        """Set once the transformation yields a raw item. dlt then attributes no table"""

        def _record_inputs(is_materialized: bool) -> None:
            """Records every dataset that the transformation read as an input data location."""
            if current_resource is None:
                return
            try:
                # a raw item names no tables, so dlt attributes nothing to any dataset
                tables = (
                    {ds_name: set() for ds_name in datasets_by_name}
                    if tables_unknown
                    else tables_by_dataset
                )
                for idx, location in enumerate(
                    _describe_inputs(tables, datasets_by_name, resource_name, is_materialized)
                ):
                    current_resource.add_input(location, replace=idx == 0)
            except Exception as ex:
                logger.warning(
                    "Could not compute lineage for transformation %s: %s", resource_name, ex
                )

        def _process_item(item: TDataItems) -> Iterator[TDataItems]:
            # a list is a batch of items in dlt, for example several models. process each element
            if isinstance(item, list):
                for element in item:
                    yield from _process_item(element)
                return
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
                nonlocal tables_unknown
                # a raw item does not name the tables it read, so table lineage of the whole
                # transformation becomes unknown. the datasets are still known, they arrive as
                # arguments
                if not tables_unknown:
                    tables_unknown = True
                    _record_inputs(True)
                # no transformation, just yield this item
                yield item
                return

            should_materialize = _materializes(relation)

            # record the datasets read as input data locations in the trace (best-effort).
            # tables accumulate across yielded models, so the whole set is re-recorded
            _collect_relation_tables(relation, tables_by_dataset)
            _record_inputs(should_materialize)

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
