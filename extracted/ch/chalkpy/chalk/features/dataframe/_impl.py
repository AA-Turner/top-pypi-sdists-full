from __future__ import annotations

import base64
import collections.abc
import inspect
import itertools
import json
import operator
import os
import pathlib
import typing
import warnings
from datetime import date, datetime, timedelta, timezone
from typing import (
    IO,
    TYPE_CHECKING,
    Any,
    Callable,
    ClassVar,
    Dict,
    Iterable,
    List,
    Literal,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
    overload,
)

import packaging.version
import pyarrow as pa

from chalk.features._chalkop import Aggregation
from chalk.features._encoding.missing_value import MissingValueStrategy
from chalk.features._encoding.pyarrow import is_map_in_dtype_tree
from chalk.features.dataframe._filters import convert_filters_to_pl_expr, dataframe_missing_key_error, filter_data_frame
from chalk.features.dataframe._validation import validate_df_schema, validate_nulls
from chalk.features.feature_field import Feature
from chalk.features.feature_wrapper import FeatureWrapper, ensure_feature, unwrap_feature
from chalk.features.filter import Filter, get_filter_now
from chalk.features.pseudofeatures import PSEUDONAMESPACE, Distance
from chalk.features.underscore import Underscore
from chalk.features.underscore_features import parse_underscore_in_context
from chalk.utils.collections import ensure_tuple, get_unique_item
from chalk.utils.df_utils import (
    pa_array_to_pl_series,
    pa_cast,
    pa_table_to_pl_df,
    read_parquet,
    recursive_convert_map_primitive,
)
from chalk.utils.duration import Duration, parse_chalk_duration
from chalk.utils.missing_dependency import missing_dependency_exception
from chalk.utils.pydanticutil.pydantic_compat import is_pydantic_basemodel

if TYPE_CHECKING:
    import pandas as pd
    import polars as pl
    from pydantic import BaseModel

    from chalk.features.feature_set import Features
else:
    try:
        from pydantic.v1 import BaseModel
    except ImportError:
        from pydantic import BaseModel

TIntStr = TypeVar("TIntStr", int, str)
DataFrameGetOptions = TypeVar("DataFrameGetOptions", bool, Filter, Underscore, FeatureWrapper, Feature, str)


class DataFrameMeta(type):
    def __getitem__(cls, item: Any) -> Type[DataFrame]:
        from chalk.features.feature_set import Features

        # leaving untyped as we type the individual features as their object type
        # but item should really be Filter (expressions), Feature classes, or Feature instances
        cls = cast(Type[DataFrame], cls)

        item = ensure_tuple(item)

        # Disallow string annotations like DataFrame["User"].
        # Instead, the entire thing should be in quotes -- like "DataFrame[User]"
        for x in item:
            if isinstance(x, str):
                raise TypeError(
                    (
                        f'Annotation {cls.__name__}["{x}", ...] is unsupported. Instead, use a string for the entire annotation -- for example: '
                        f'"{cls.__name__}[{x}, ...]"'
                    )
                )

        # If doing multiple subscript, then keep the filters, but do not keep the individual columns
        # TODO: Validate that any new columns are a subset of the existing columns
        item = [*item, *cls.filters]

        new_filters: List[Filter] = []
        new_references_feature_set: Optional[Type[Features]] = None
        new_columns: List[Feature] = []
        pydantic_model = None
        limit = None
        for a in item:
            if isinstance(a, Underscore):
                if pydantic_model:
                    context = cls
                    is_pydantic = True
                else:
                    context = cls.references_feature_set
                    is_pydantic = False
                a = parse_underscore_in_context(exp=a, context=context, is_pydantic=is_pydantic)
            if isinstance(a, FeatureWrapper):
                a = unwrap_feature(a, raise_error=False)
            if isinstance(a, Filter):
                new_filters.append(a)
            elif isinstance(a, type) and issubclass(a, Features):
                if new_references_feature_set is not None:
                    raise ValueError(
                        f"Multiple referenced feature sets -- {new_references_feature_set} and {a} -- are not supported."
                    )
                new_references_feature_set = a
            elif isinstance(a, Feature):
                new_columns.append(a)
            elif isinstance(a, bool):
                # If we encounter a bool, that means we are evaluating the type annotation before
                # the ResolverAstParser had a chance to extract the source and rewrite the and/or/in operations
                # into expressions that return filters instead of booleans
                # This function will be called again for this annotation, so we can ignore it for now.
                pass
            elif isinstance(a, slice):
                if a.start is not None and a.start != 0:
                    raise ValueError(f"The slice expression {a} with an explicit start is not supported.")
                if a.step is not None and a.step != 1:
                    raise ValueError(f"The slice expression {a} with an explicit step is not supported")
                limit = a.stop
            elif inspect.isclass(a) and is_pydantic_basemodel(a):
                pydantic_model = a
            else:
                raise TypeError(f"Invalid type for DataFrame[{a}]: {type(a)}")

        if len(new_columns) == 0 and new_references_feature_set is None:
            # This is possible if you have something like
            # Users.transactions[after('60d')]
            # In this case, keep all existing columns
            # But if you did
            # Users.transactions[Transaction.id, after('60d')]
            # Then keep only the id column
            new_columns = list(cls.__columns__)
            new_references_feature_set = cls.__references_feature_set__

        class SubclassedDataFrame(cls):
            filters = tuple(new_filters)
            __columns__ = tuple(new_columns)
            __references_feature_set__ = new_references_feature_set
            __pydantic_model__ = pydantic_model
            __limit__ = limit

            def __eq__(self, other: object):
                if not isinstance(other, SubclassedDataFrame):
                    return NotImplemented

                    # This should probably be frozen set
                return frozenset(self.filters) == frozenset(other.filters) and frozenset(self.__columns__) == frozenset(
                    other.__columns__
                )

            def __hash__(self):
                return hash((frozenset(self.filters), frozenset(self.__columns__)))

            def __new__(cls: Type[DataFrame], *args: Any, **kwargs: Any) -> DataFrame:
                raise RuntimeError(
                    "A SubclassedDataFrame should never be instantiated. Instead, instantiate a DataFrame(...)."
                )

        return SubclassedDataFrame

    def __repr__(cls):
        cls = cast(Type[DataFrame], cls)
        elements = [str(x) for x in (*cls.filters, *cls.columns)]
        if cls.__pydantic_model__:
            return f"DataFrame[{', '.join(elements)}], model={cls.__pydantic_model__}"
        return f"DataFrame[{', '.join(elements)}]"

    @property
    def columns(cls) -> Tuple[Feature, ...]:
        # Computing the columns lazily as we need to implicitly parse the type annotation
        # to determine if a field is a has-many, and we don't want to do that on the
        # __getitem__ which could happen before forward references can be resolved
        # So, using a property on the metaclass, which acts like an attribute on the class, to
        # provide the dataframe columns
        from chalk.features.feature_field import Feature

        cls = cast(Type[DataFrame], cls)
        # Using a dict to preserve ordering
        columns: Dict[Feature, None] = {}
        for x in cls.__columns__:
            assert isinstance(x, Feature)
            if x not in columns:
                columns[x] = None
        if cls.__references_feature_set__ is not None:
            # Only include the first-level feature types
            # Do not recurse has-ones and has-many as that could create an infinite loop
            # Skipping autogenerated features because if one writes DataFrame[User],
            # then they definitely did not mean to include a feature they didn't know about
            for x in cls.__references_feature_set__.features:
                assert isinstance(x, Feature)
                if not x.is_autogenerated and not x.is_has_many and not x.is_has_one and x not in columns:
                    columns[x] = None
        return tuple(columns)

    @property
    def references_feature_set(cls):
        from chalk.features.feature_set import FeatureSetBase

        cls = cast(Type[DataFrame], cls)
        if cls.__references_feature_set__ is not None:
            return cls.__references_feature_set__
        else:
            # Determine the unique @features cls that encompasses all columns
            root_ns = get_unique_item((x.root_namespace for x in cls.__columns__), "root ns")
        return FeatureSetBase.registry[root_ns]

    @property
    def namespace(cls) -> str:
        cls = cast(Type[DataFrame], cls)
        namespaces = (x.path[0].parent.namespace if len(x.path) > 0 else x.namespace for x in cls.columns)
        # Remove the pseudo-columns
        namespaces = (x for x in namespaces if not x.startswith("__chalk__"))
        return get_unique_item(namespaces, f"dataframe {cls.__name__} column namespaces")

    def _parse_underscore(self, exp: Underscore, pydantic_model: Optional[BaseModel] = None) -> Any:
        if pydantic_model:
            context = self
            is_pydantic = True
        else:
            context = self.references_feature_set
            is_pydantic = False
        parse_underscore_in_context(exp=exp, context=context, is_pydantic=is_pydantic)


class DataFrame(metaclass=DataFrameMeta):
    filters: ClassVar[Tuple[Filter, ...]] = ()
    columns: Tuple[Feature, ...]  # set via a @property on the metaclass
    __columns__: ClassVar[Tuple[Feature, ...]] = ()
    references_feature_set: Optional[Type[Features]]  # set via a @property on the metaclass
    __references_feature_set__: ClassVar[Optional[Type[Features]]] = None
    __pydantic_model__: ClassVar[Optional[Type[BaseModel]]] = None
    __limit__: int | None = None
    """The maximum number of rows to return"""

    if TYPE_CHECKING:

        def __class_getitem__(cls, cols: Any) -> Type[DataFrame]:
            ...

    def __init__(
        self,
        data: Union[
            Dict[Union[str, Feature, Any], Sequence[Any]],
            Sequence[Union[Features, Any]],
            pa.Table,
            pa.RecordBatch,
            pl.DataFrame,
            pl.LazyFrame,
            pd.DataFrame,
            Any,  # Polars supports a bunch of other formats for initialization of a DataFrame
        ] = None,
        # Setting to default_or_allow for backwards compatibility
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
        pandas_dataframe: Optional[pd.DataFrame] = None,  # For backwards compatibility
        # By default, data should match the dtype of the feature.
        # However, when doing comparisons, data will be converted to bools,
        # in which case the data types should no longer be converted.
        # This is an undocumented parameter, so it does not appear in the docstring
        convert_dtypes: bool = True,
        pydantic_model: Optional[Type[BaseModel]] = None,
        verify_validity: bool = True,
    ):
        """Construct a Chalk `DataFrame`.

        Parameters
        ----------
        data
            The data. Can be an existing `pandas.DataFrame`,
            `polars.DataFrame` or `polars.LazyFrame`,
            a sequence of feature instances, or a `dict` mapping
            a feature to a sequence of values.
        missing_value_strategy
            The strategy to use to handle missing values.

            A feature value is "missing" if it is an ellipsis (`...`),
            or it is `None` and the feature is not annotated as `Optional[...]`.

            The available strategies are:
                - `'error'`: Raise a `TypeError` if any missing values are found.
                    Do not attempt to replace missing values with the default
                    value for the feature.
                - `'default_or_error'`: If the feature has a default value, then
                    replace missing values with the default value for the feature.
                    Otherwise, raise a `TypeError`.
                - `'default_or_allow'`:  If the feature has a default value, then
                    replace missing values with the default value for the feature.
                    Otherwise, leave it as `None`. This is the default strategy.
                - `'allow'`: Allow missing values to be stored in the `DataFrame`.
                    This option may result non-nullable features being assigned
                    `None` values.

        Examples
        --------
        Row-wise construction

        >>> df = DataFrame([
        ...     User(id=1, first="Sam", last="Wu"),
        ...     User(id=2, first="Iris", last="Xi")
        ... ])

        Column-wise construction

        >>> df = DataFrame({
        ...     User.id: [1, 2],
        ...     User.first: ["Sam", "Iris"],
        ...     User.last: ["Wu", "Xi"]
        ... })

        Construction from `polars.DataFrame`

        >>> import polars
        >>> df = DataFrame(polars.DataFrame({
        ...     "user.id": [1, 2],
        ...     "user.first": ["Sam", "Iris"],
        ...     "user.last": ["Wu", "Xi"]
        ... }))
        """
        super().__init__()
        from chalk.features.feature_set import Features, FeatureSetBase

        try:
            import polars as pl
        except ImportError:
            raise missing_dependency_exception("chalkpy[runtime]")

        self._pydantic_model = pydantic_model
        self._convert_dtypes = convert_dtypes

        # Typing the keys of ``data`` as Any, as {FeatureCls.item: x} would be typed as the underlying annotation
        # of the features cls
        if pandas_dataframe is not None:
            warnings.warn(
                DeprecationWarning("ChalkDataFrameImpl(pandas_dataframe=...) has been renamed to DataFrame(data=...)")
            )
            data = pandas_dataframe
        try:
            import pandas as pd
        except ImportError:
            pass
        else:
            if isinstance(data, pd.DataFrame):
                # Convert the columns to root fqn strings
                # str(Feature) and str(FeatureWrapper) return the root fqns
                data = data.rename(columns={k: str(k) for k in data.columns})
                assert isinstance(data, pd.DataFrame)
                data.columns = data.columns.astype("string")
                data = pl.from_pandas(data)
        if isinstance(data, pa.RecordBatch):
            data = pa.Table.from_batches([data])
        if isinstance(data, pa.Table):
            data = pa_table_to_pl_df(data)
            assert isinstance(data, pl.DataFrame)
        if not isinstance(data, (pl.LazyFrame, pl.DataFrame)):
            if isinstance(data, (collections.abc.Sequence)) and not isinstance(data, str):
                # If it is a sequence, it could be a sequence of feature classes instances
                # If so, set the columns by inspecting the feature classes
                # If columns are none, then inspect the data to determine if they are feature classes
                # Otherwise, if the columns are specified, do not introspect the list construction
                features_typ = None
                new_data: dict[str, list[Any]] = {}
                for row in data:
                    if not isinstance(row, Features):
                        raise ValueError("If specifying data as a sequence, it must be a sequence of Features")
                    if features_typ is None:
                        features_typ = type(row)
                        for x in row.features:
                            assert isinstance(x, Feature)
                            assert x.attribute_name is not None
                            try:
                                feature_val = getattr(row, x.attribute_name)
                            except AttributeError:
                                continue
                            new_data[x.root_fqn] = []

                    if features_typ != type(row):
                        raise ValueError("Cannot mix different feature classes in a DataFrame")

                    # If there are multiple versions of a feature, then the `features` may
                    # include the same value more than once. In this case, we want to only
                    # push one of them into the result.
                    already_placed_fqns: set[str] = set()
                    for x in row.features:
                        assert isinstance(x, Feature)
                        assert x.attribute_name is not None
                        try:
                            feature_val = getattr(row, x.attribute_name)
                        except AttributeError:
                            if x.root_fqn in new_data:
                                raise ValueError(
                                    f"While constructing a dataframe from a list of feature classes, feature '{x.root_fqn}' was defined in some rows but not in others. Features must be defined in all provided rows or none of the provided rows."
                                )
                            continue
                        if x.root_fqn not in new_data:
                            raise ValueError(
                                f"While constructing a dataframe from a list of feature classes, feature '{x.root_fqn}' was defined in some rows but not in others. Features must be defined in all provided rows or none of the provided rows."
                            )
                        if x.root_fqn in already_placed_fqns:
                            continue
                        already_placed_fqns.add(x.root_fqn)
                        new_data[x.root_fqn].append(feature_val)
                data = new_data
            if isinstance(data, dict):
                # Convert the columns to root fqn strings
                new_data_dict: Dict[str, Union[Sequence[Any], pl.Series]] = {}
                for k, v in data.items():
                    str_k = str(k)
                    feature = Feature.from_root_fqn(str_k)
                    if feature.is_distance_pseudofeature:
                        feature = Distance
                        str_k = str(Distance)

                    if feature.is_has_one:
                        warnings.warn(
                            DeprecationWarning(
                                (
                                    f"Feature '{feature}' is a has-one feature. Its values will not be validated, "
                                    f"nor can this column be used for filtering. Support for passing has-one features "
                                    "into a Chalk DataFrame will be removed. Instead, specify each feature of the "
                                    "nested feature class as an individual column."
                                )
                            )
                        )
                    if convert_dtypes:
                        try:
                            pa_array = feature.converter.from_rich_to_pyarrow(
                                v,
                                missing_value_strategy=missing_value_strategy,
                            )
                        except (TypeError, ValueError) as e:
                            if len(v) > 0:
                                type_error = f" The first value that could not be loaded has type '{type(v[0])}'."
                            else:
                                type_error = ""

                            raise TypeError(
                                (
                                    f"The values for feature `{k}` could not be loaded into a DataFrame column "
                                    f"of type `{feature.converter.pyarrow_dtype}`.{type_error}"
                                )
                            ) from e
                        series = pa_array_to_pl_series(pa_array)
                    else:
                        series = v
                    new_data_dict[str_k] = series

                data = new_data_dict
            data = pl.DataFrame(data)
        if isinstance(data, (pl.LazyFrame, pl.DataFrame)):
            underlying = data
        else:
            raise ValueError(f"Unable to convert data of type {type(data).__name__} into a DataFrame")
        # Rename / validate that all column names are root fqns
        if self._pydantic_model is None:
            self.columns = tuple(Feature.from_root_fqn(str(c)) for c in underlying.columns)
        else:
            self.columns = ()

        # Convert columns to the correct dtype to match the fqn
        if self._pydantic_model is None and convert_dtypes:
            underlying = validate_df_schema(underlying)
            if verify_validity:
                underlying = validate_nulls(underlying, missing_value_strategy=missing_value_strategy)

        self._distance_feature_fqns = {x.root_fqn for x in self.columns if x.is_distance_pseudofeature}
        self._underlying = pl.LazyFrame()
        self._swap_underlying(underlying.lazy())

        # Remove the pseudo-features when determining the namespace
        namespaces_set = {x.root_namespace for x in self.columns if not x.root_namespace == "__chalk__"}
        if len(namespaces_set) == 1:
            self.namespace = get_unique_item(namespaces_set, "DataFrame column namespaces")
            self.references_feature_set = FeatureSetBase.registry[self.namespace]
        else:
            # Allow empty dataframes or dataframes with multiple namespaces
            self.namespace = None
            self.references_feature_set = None

    def _swap_underlying(self, underlying: pl.LazyFrame):
        """Swap the underlying lazyframe, without validation. Equivalent to DataFrame(...) for an identical LazyFrame of the same shape

        This is a private method used internally by Chalk.
        """
        import polars as pl

        rename_map = {x: Distance.fqn for x in underlying.columns if x in self._distance_feature_fqns}

        underlying = underlying.rename(rename_map)
        if len(rename_map) > 0:
            underlying = underlying.sort(pl.col(Distance.fqn))
        self._underlying = underlying

    #######################
    # Filtering / Selecting
    #######################
    @typing.overload
    def __getitem__(self, item: int) -> Features:
        ...

    @typing.overload
    def __getitem__(self, item: Union[DataFrameGetOptions, Sequence[DataFrameGetOptions]]) -> DataFrame:
        ...

    def __getitem__(self, item: Any) -> Union[Features, DataFrame]:
        """Filter the rows of a `DataFrame` or project out columns.

        You can select columns out of a `DataFrame` from
        the set of columns already present to produce a new
        `DataFrame` scoped down to those columns.

        Or, you can filter the rows of a `DataFrame` by using
        Python's built-in operations on feature columns.

        Parameters
        ----------
        item
            Filters and projections to apply to the `DataFrame`.

        Returns
        -------
        DataFrame
            A `DataFrame` with the filters and projections in `item` applied.

        Examples
        --------
        >>> df = DataFrame({
        ...     User.age: [21, 22, 23],
        ...     User.email: [...],
        ... })

        Filtering

        >>> df = df[
        ...     User.age > 21 and
        ...     User.email == "joe@chalk.ai"
        ... ]

        Projecting

        >>> df[User.name]

        Filtering & Projecting

        >>> df = df[
        ...     User.age > 21 and
        ...     User.email == "joe@chalk.ai",
        ...     User.name
        ... ]
        """

        if isinstance(item, int) and not isinstance(item, bool):
            if item >= 0:
                l = len(self)
                if item >= l:
                    raise IndexError(f"Index {item} out of range (length {l})")
                underlying = self._underlying.head(item + 1).tail(1)
            else:
                underlying = self._underlying.tail(-item).head(1)

            df = DataFrame(
                underlying,
                convert_dtypes=False,
                pydantic_model=self._pydantic_model,
            )
            return list(df.to_features())[0]

        has_bool_or_filter_value = any(
            isinstance(x, (bool, Filter, Underscore))  # pyright: ignore[reportUnnecessaryIsInstance]
            for x in ensure_tuple(item)
        )
        if has_bool_or_filter_value:
            # If we have a boolean or Filter value, then that means we need to ast-parse the caller since
            # python has already evaluated AND, OR, and IN operations into literal booleans or Filters
            # Skipping the parsing unless if we have need to for efficiency and to eliminate conflicts
            # with pytest
            from chalk.df.ast_parser import parse_dataframe_getitem

            item = parse_dataframe_getitem()

        # Resolve underscores to be within the dataframe's context
        item = tuple(
            self._parse_underscore(exp=x)
            if isinstance(x, Underscore)  # pyright: ignore[reportUnnecessaryIsInstance]
            else x
            for x in ensure_tuple(item)
        )
        assert all(not isinstance(x, Underscore) for x in item)
        if len(item) == 1:
            item = item[0]

        if any(isinstance(x, (FeatureWrapper, Feature, Filter)) for x in ensure_tuple(item)):
            return DataFrame(
                filter_data_frame(item, namespace=self.namespace, underlying=self._underlying),
                pydantic_model=self._pydantic_model,
                verify_validity=False,
            )
        elif all(isinstance(col, str) for col in ensure_tuple(item)):
            # Select the columns with `.select()` since they're by name.
            key_error_or_none = dataframe_missing_key_error(ensure_tuple(item), self._underlying.columns)
            if key_error_or_none is not None:
                raise key_error_or_none
            materialized = self._materialize()
            df = materialized.select(ensure_tuple(item))
            return DataFrame(df, pydantic_model=self._pydantic_model, verify_validity=False)

        else:
            # Otherwise, use the standard polars selection format
            # Must materialize the dataframe to use __getitem__
            materialized = self._materialize()
            df = materialized[item]
            return DataFrame(df, pydantic_model=self._pydantic_model, verify_validity=False)

    def group_by(
        self,
        group: Mapping[Union[Feature, Any], Union[Feature, Any]],
        agg: Mapping[Any, Any],
    ) -> DataFrame:
        """Aggregate the `DataFrame` by the specified columns.

        Parameters
        ----------
        group
            A mapping from the desired column name in the resulting `DataFrame`
            to the name of the column in the source `DataFrame`.
        agg
            A mapping from the desired column name in the resulting `DataFrame`
            to the aggregation operation to perform on the source `DataFrame`.

        Returns
        -------
        DataFrame
            The `DataFrame` with the specified aggregations applied.

        Examples
        --------
        >>> from chalk.features import DataFrame
        >>> df = DataFrame(
        ...     {
        ...         User.id: [1, 1, 3],
        ...         User.val: [1, 5, 10],
        ...     }
        ... ).group_by(
        ...      group={User.id: User.id}
        ...      agg={User.val: op.median(User.val)}
        ... )
        ╭─────────┬──────────╮
        │ User.id │ User.val │
        ╞═════════╪══════════╡
        │  1      │ 3        │
        ├─────────┼──────────┤
        │  3      │ 10       │
        ╰─────────┴──────────╯
        """
        import polars as pl

        from chalk.features.feature_set import FeatureSetBase

        groupby = [pl.col(str(v)).alias(str(k)) for k, v in group.items()]

        namespaces = {unwrap_feature(a).namespace for a in agg.keys()}
        namespace = namespaces.pop() if len(namespaces) == 1 else None
        timestamp_feature = None if namespace is None else FeatureSetBase.registry[namespace].__chalk_ts__

        now = datetime.now(tz=timezone.utc)
        cols = []
        operation: Aggregation
        for alias, operation in agg.items():
            alias = unwrap_feature(alias, raise_error=False)
            operation = unwrap_feature(operation, raise_error=False)
            c = operation.col
            if len(operation.filters) > 0:
                f = convert_filters_to_pl_expr(
                    operation.filters,
                    self._underlying.schema,
                    timestamp_feature,
                    now,
                )
                if f is not None:
                    c = c.filter(f)

            cols.append(operation.fn(c).alias(str(alias)))

        data = self._underlying.lazy()

        if packaging.version.parse(pl.__version__) <= packaging.version.parse("0.19.0"):
            data = data.groupby(groupby)
        else:
            data = data.group_by(groupby)

        data = data.agg(cols).collect()

        return DataFrame(
            data,
            convert_dtypes=self._convert_dtypes,
            pydantic_model=self._pydantic_model,
        )

    def histogram_list(
        self,
        nbins: int | None = None,
        bin_width: float | int | Duration | None = None,
        base: float | int | datetime | date | None = None,
        eps: float = 1e-13,
        column: Any | None = None,
        descending: bool = False,
    ) -> list[int]:
        """Compute a histogram with fixed width bins.

        Parameters
        ----------
        nbins
            If supplied, will be used to compute the binwidth.
        bin_width
            If not supplied, computed from the data (actual max and min values).
        base
            The value of the first histogram bin. Defaults to the minimum value of column.
        eps
            Allowed floating point epsilon for histogram base
        column
            The column to compute the histogram on. If not supplied, the `DataFrame`
            is assumed to contain a single column.
        descending
            If `True`, the histogram buckets will be sorted in descending order.

        Returns
        -------
        list[int]
            A list of the counts in each bin.

        Examples
        --------
        >>> DataFrame({
        ...   Taco.price: list(range(100, 200)),
        ... }).histogram_list(nbins=4, base=100)
        [25, 25, 25, 25]
        """

        if column is None:
            if len(self.columns) == 1:
                column = self.columns[0]
            else:
                raise ValueError(f"Must specify `column` if `DataFrame` has multiple columns (got {self.columns})")

        import polars as pl

        if isinstance(bin_width, str):
            bin_width = parse_chalk_duration(bin_width)

        col_str = str(column)

        col_dtype = self._underlying.schema[col_str]
        underlying = self._underlying
        if col_dtype != pl.Float64() and col_dtype != pl.Float32():
            underlying = underlying.select(pl.col(col_str).cast(pl.Float32))

        if isinstance(bin_width, timedelta):
            bin_width = bin_width.total_seconds() * 1_000_000.0

        if isinstance(base, (date, datetime)):
            epoch = datetime.fromtimestamp(0, timezone.utc)
            if isinstance(base, datetime):
                if base.tzinfo is not None:
                    epoch = epoch.replace(tzinfo=base.tzinfo)
            base = (base - epoch).total_seconds() * 1_000_000.0

        max_value: float = underlying.select(col_str).max().collect().item()
        min_value: float = underlying.select(col_str).min().collect().item()

        if base is None:
            base = min_value - eps

        if bin_width is None:
            assert nbins is not None
            bin_width = (max_value - base) / nbins

        if nbins is None:
            nbins = int((max_value - base) / bin_width)

        # A final bucket is assigned to the right of the buckets,
        # so we need to have one fewer bucket than `nbins`.
        bins = [base + x * bin_width for x in range(1, nbins)]
        return (
            self.to_polars()
            .select(col_str)
            .collect()
            .to_series()
            .hist(bins=bins)
            .sort(
                by="break_point",
                descending=descending,
            )
            .select(f"{column}_count")
            .to_series()
            .to_list()
        )

    def group_by_hopping(
        self,
        index: Union[Feature, Any],
        agg: Mapping[Any, Any],
        every: Union[str, timedelta],
        group: Mapping[Union[Feature, Any], Union[Feature, Any]] | None = None,
        period: Optional[Union[str, timedelta]] = None,
        offset: Optional[Union[str, timedelta]] = None,
        start_by: Literal[
            "window", "datapoint", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"
        ] = "window",
    ) -> DataFrame:
        """Group based on a time value (`date` or `datetime`).

        The groups are defined by a time-based window, and optionally,
        other columns in the `DataFrame`. The "width" of the window is
        defined by the `period` parameter, and the spacing between the
        windows is defined by the `every` parameter. Note that if the
        `every` parameter is smaller than the `period` parameter, then
        the windows will overlap, and a single row may be assigned to
        multiple groups.

        As an example, consider the following `DataFrame`:

        ```

        val:    a  b    c   d e     f           g h
            ─────────●─────────●─────────●─────────●───────▶
        time:        A         B         C         D
            ┌─────────┐
        1   │   a  b  │                                    1: [a, b]
            └────┬────┴────┐
        2   ◀───▶│ b    c  │                               2: [b, c]
            every└────┬────┴────┐
        3   ◀────────▶│ c   d e │                          3: [c, d, e]
              period  └────┬────┴────┐
        4                  │d e     f│                     4: [d, e, f]
                           └────┬────┴────┐
        5                       │   f     │                5: [f]
                                └────┬────┴────┐
        6                            │         │
                                     └────┬────┴────┐
        7                                 │     g h │      7: [g, h]
                                          └────┬────┴────┐
        8                                      │g h      │ 8: [g, h]
                                               └─────────┘
        ```

        In the above example, the sixth time bucket is empty, and
        will not be included in the resulting `DataFrame`.

        Parameters
        ----------
        index
            The column to use as the index for the time-based grouping.
        group
            A mapping from the desired column name in the resulting `DataFrame`
            to the name of the column in the source `DataFrame`. This parameter
            is optional, and if not specified, then the resulting `DataFrame`
            groups will be determined by the `index` parameter alone.
        agg
            A mapping from the desired column name in the resulting `DataFrame`
            to the aggregation operation to perform on the source `DataFrame`.
        every
            The spacing between the time-based windows. This parameter can be
            specified as a `str` or a `timedelta`. If specified as a `str`,
            then it must be a valid `Duration`.
        period
            The width of the time-based window. This parameter can be specified
            as a `str` or a `timedelta`. If specified as a `str`, then it must
            be a valid `Duration`. If `None` it is equal to `every`.

        Other Parameters
        ----------------
        offset
            The offset to apply to the time-based window. This parameter can be
            specified as a `str` or a `timedelta`. If specified as a `str`,
            then it must be a valid `Duration`. If `None` it is equal to negative
            `every`.
        start_by
            The strategy to determine the start of the first window by.
            - `window`: Truncate the start of the window with the ‘every’ argument.
            - `datapoint`: Start from the first encountered data point.
            - `monday | tuesday | ...`: Start from the first Monday before the first encountered data point.

        Returns
        -------
        DataFrame
            A new `DataFrame` with the specified time-based grouping applied.
            The resulting `DataFrame` will have a column for each of the keys
            in `group", "or each of the keys in `agg`, and for the `index`
            parameter.

        Examples
        --------
        >>> from chalk import DataFrame, op
        >>> df = DataFrame(
        ...     {
        ...         User.id: [1, 1, 3],
        ...         User.val: [1, 5, 10],
        ...         User.ts: [datetime(2020, 1, 1), datetime(2020, 1, 1), datetime(2020, 1, 3)],
        ...     },
        ... ).group_by_hopping(
        ...      index=User.ts,
        ...      group={User.id: User.id},
        ...      agg={User.val: op.median(User.val)},
        ...      period="1d",
        ... )
        ╭─────────┬──────────┬──────────╮
        │ User.id │ User.ts  │ User.val │
        ╞═════════╪══════════╪══════════╡
        │  1      │ 2020-1-1 │ 3        │
        ├─────────┼──────────┼──────────┤
        │  3      │ 2020-1-3 │ 10       │
        ╰─────────┴──────────┴──────────╯
        """
        import polars as pl

        from chalk.features.feature_set import FeatureSetBase

        groupby = [pl.col(str(v)).alias(str(k)) for k, v in group.items()] if group is not None else None

        namespaces = {unwrap_feature(a).namespace for a in agg.keys()}
        namespace = namespaces.pop() if len(namespaces) == 1 else None
        timestamp_feature = None if namespace is None else FeatureSetBase.registry[namespace].__chalk_ts__

        now = get_filter_now()
        cols: List[pl.Expr] = []
        operation: Aggregation
        for alias, operation in agg.items():
            c = operation.col
            if len(operation.filters) > 0:
                f = convert_filters_to_pl_expr(
                    operation.filters,
                    self._underlying.schema,
                    timestamp_feature,
                    now,
                )
                if f is not None:
                    c = c.filter(f)

            cols.append(operation.fn(c).alias(str(alias)))

        return DataFrame(
            self._underlying.lazy()
            .sort(str(index), descending=False)
            .groupby_dynamic(
                index_column=str(index),
                by=groupby,
                offset=offset,
                every=every,
                period=period,
                start_by=start_by,
            )
            .agg(cols)
            .collect(),
            convert_dtypes=self._convert_dtypes,
            pydantic_model=self._pydantic_model,
        )

    def join(
        self,
        df: DataFrame,
        on: Any | List[Any],
        how: Literal["inner", "left", "outer"] = "left",
    ) -> DataFrame:
        on = ensure_tuple(on)
        p = self._underlying.join(
            df._underlying,
            on=[str(t) for t in on],
            how=how,
        )
        return DataFrame(p)

    def vstack(self, other: DataFrame) -> DataFrame:
        """Vertically stack the `DataFrame` with another `DataFrame`
        containing the same columns. The `DataFrame` other will
        be appended to the bottom of this `DataFrame`.

        Parameters
        ----------
        other
            The other `DataFrame` to stack with this `DataFrame`.

        Returns
        -------
        DataFrame
            The `DataFrame` with the other `DataFrame` stacked on the bottom.

        Examples
        --------
        >>> from chalk.features import DataFrame
        >>> df = DataFrame([
        ...     User(id=1, first="Sam", last="Wu"),
        ...     User(id=2, first="Iris", last="Xi")
        ... ])
        >>> df.vstack(df)
        """
        return DataFrame(
            self._underlying.collect().vstack(other._underlying.collect()).lazy(),
            convert_dtypes=self._convert_dtypes,
            pydantic_model=self._pydantic_model,
        )

    def num_unique(self, column: Any = None) -> int:
        """Return the number of unique values in the specified column.

        Parameters
        ----------
        column
            The column to compute the number of unique values for.
            If `None`, then the number of unique values in the entire
            `DataFrame` is returned.

        Returns
        -------
        int
            The number of unique values in the specified column.

        Examples
        --------
        >>> from chalk.features import DataFrame
        >>> df = DataFrame([
        ...     User(id=1, first="Sam", last="Wu"),
        ...     User(id=2, first="Iris", last="Xi")
        ... ])
        >>> df.num_unique(User.id)
        2
        """

        return self._underlying.collect().n_unique(column and str(column))

    def rename(self, mapping: Mapping[Any, Any]) -> DataFrame:
        """Rename columns in the `DataFrame`.

        Parameters
        ----------
        mapping
            A mapping from the current feature for a column to the desired
            feature for the column.

        Returns
        -------
        DataFrame
            The `DataFrame` with the specified columns renamed.

        Examples
        --------
        >>> df = DataFrame([
        ...     User(id=1, first="Sam", last="Wu"),
        ...     User(id=2, first="Iris", last="Xi")
        ... ]).rename({User.last: User.family})
        """
        return DataFrame(
            self._underlying.rename(
                {unwrap_feature(k).root_fqn: unwrap_feature(v).root_fqn for k, v in mapping.items()}
            ),
            convert_dtypes=self._convert_dtypes,
            pydantic_model=self._pydantic_model,
        )

    def with_column(self, column: Any, value: Any) -> DataFrame:
        """Add a column to the `DataFrame`.

        Parameters
        ----------
        column
            The name of the column to add.
        value
            The definition of the column to add.
            This could be a constant value (e.g. `1` or `True`),
            an expression (e.g. `op.max(User.score_1, User.score_2)`),
            or a list of values (e.g. `[1, 2, 3]`).

        Examples
        --------
        >>> df = DataFrame([
        ...     User(id=1, first="Sam", last="Wu"),
        ...     User(id=2, first="Iris", last="Xi")
        ... ])
        >>> # Set the fraud score to 0 for all users
        >>> df.with_column(User.fraud_score, 0)
        >>> # Concatenation of first & last as full_name
        >>> df.with_column(
        ...     User.full_name, op.concat(User.first, User.last)
        ... )
        >>> # Alias a column name
        >>> df.with_column(
        ...     User.first_name, User.first
        ... )
        """
        return self.with_columns({column: value})

    def with_columns(self, c: Mapping[Any, Any]) -> DataFrame:
        """Add columns to the `DataFrame`.

        Parameters
        ----------
        c
            A `Mapping` from the desired name of the column
            in the `DataFrame` to the definition of the new
            column.

        Examples
        --------
        >>> df = DataFrame([
        ...     User(id=1, first="Sam", last="Wu"),
        ...     User(id=2, first="Iris", last="Xi")
        ... ])
        >>> # Set the fraud score to 0 for all users
        >>> df.with_columns({User.fraud_score: 0})
        >>> # Concatenation of first & last as full_name
        >>> df.with_columns({
        ...     User.full_name: op.concat(User.first, User.last)
        ... })
        >>> # Alias a column name
        >>> df.with_columns({
        ...     User.first_name: User.first
        ... })


        Returns
        -------
        DataFrame
            A new `DataFrame` with all the existing columns,
            plus those specified in this function.
        """
        import polars as pl

        from chalk.features.feature_set import FeatureSetBase

        new_c = {}
        for k, v in c.items():
            if isinstance(k, Underscore):
                new_k = self._parse_underscore(exp=k)
            else:
                new_k = k
            if isinstance(v, Underscore):
                new_v = self._parse_underscore(exp=v)
            else:
                new_v = v
            new_c[new_k] = new_v
        c = new_c

        assert all(not isinstance(k, Underscore) for k in c.keys())

        namespaces = {unwrap_feature(a).namespace for a in c.keys()}
        namespace = namespaces.pop() if len(namespaces) == 1 else None
        timestamp_feature = None if namespace is None else FeatureSetBase.registry[namespace].__chalk_ts__

        now = get_filter_now()
        cols: List[pl.Expr] = []
        for alias, operation in c.items():
            # if isinstance(operation, int):
            #     operation = op.count(FeatureWrapper.len_registry[operation])
            # c = pl.col(str(operation.col))
            if isinstance(operation, FeatureWrapper):
                operation = unwrap_feature(operation, raise_error=False)
            if isinstance(operation, Aggregation):
                col = operation.col
                if len(operation.filters) > 0:
                    f = convert_filters_to_pl_expr(
                        operation.filters,
                        self._underlying.schema,
                        timestamp_feature,
                        now,
                    )
                    if f is not None:
                        col = col.filter(f)

                cols.append(operation.fn(col).alias(str(alias)))
            elif isinstance(operation, Feature):
                cols.append(pl.col(str(operation)).alias(str(alias)))
            elif isinstance(operation, pl.Expr):
                cols.append(operation.alias(str(alias)))
            else:
                cols.append(pl.lit(operation).alias(str(alias)))

        agged = self._materialize().lazy().with_columns(cols).collect()

        return DataFrame(
            agged,
            convert_dtypes=self._convert_dtypes,
            pydantic_model=self._pydantic_model,
        )

    ##############
    # Classmethods
    ##############

    @classmethod
    def from_dict(
        cls,
        data: Dict[Union[str, Feature, FeatureWrapper, Any], Sequence[Any]],
    ) -> DataFrame:
        """Deprecated. Use DataFrame(...) instead."""
        warnings.warn(DeprecationWarning("DataFrame.from_dict(...) is deprecated. Instead, use DataFrame(...)"))
        df = cls(data)
        return df

    @overload
    @classmethod
    def from_list(
        cls,
        data: Sequence[Features],
        /,
    ) -> DataFrame:
        """Deprecated. Use DataFrame(...) instead."""
        ...

    @overload
    @classmethod
    def from_list(cls, *data: Features) -> DataFrame:
        """Deprecated. Use DataFrame(...) instead."""
        ...

    @classmethod
    def from_list(cls, *data: Union[Features, Sequence[Features]]) -> DataFrame:
        """Deprecated. Use DataFrame(...) instead."""
        warnings.warn(DeprecationWarning("DataFrame.from_list(...) is deprecated. Instead, use DataFrame(...)"))
        if len(data) == 1 and isinstance(data[0], collections.abc.Sequence):
            # Passed a list as the first argument
            features_seq = data[0]
        else:
            data = cast("Tuple[Features]", data)
            features_seq = data
        df = cls(features_seq)
        return df

    @classmethod
    def _get_storage_options(cls) -> Optional[Dict[str, Any]]:
        integration_creds = os.getenv("GCP_INTEGRATION_CREDENTIALS_B64")
        if integration_creds is not None:
            try:
                from google.oauth2 import service_account
            except ImportError:
                raise missing_dependency_exception("google-auth")
            token = service_account.Credentials.from_service_account_info(
                json.loads(base64.b64decode(integration_creds)),
                scopes=[
                    "https://www.googleapis.com/auth/cloud-platform",
                    "https://www.googleapis.com/auth/userinfo.email",
                ],
            )
            return {"token": token}
        else:
            return None

    @classmethod
    def read_delta(
        cls,
        table_uri: str,
        version: Optional[int] = None,
        columns: Optional[
            Dict[str, Union[str, Feature, Any]],
        ] = None,
        delta_table_options: Optional[Dict[str, Any]] = None,
        pyarrow_options: Optional[Dict[str, Any]] = None,
    ) -> DataFrame:
        try:
            import polars as pl
        except ImportError:
            raise missing_dependency_exception("chalkpy[runtime]")

        if columns is None:
            cols_to_select, _, new_columns = None, None, None
        else:
            cols_to_select, _, new_columns = cls._parse_columns(columns)

        data = pl.read_delta(
            source=table_uri,
            version=version,
            columns=cols_to_select,
            storage_options=DataFrame._get_storage_options(),
            delta_table_options=delta_table_options,
            pyarrow_options=pyarrow_options,
        )
        if new_columns is not None:
            data = data.rename({c: new_columns[i] for i, c in enumerate(data.columns)})
        return cls(data)

    @classmethod
    def read_parquet(
        cls,
        path: Union[str, pathlib.Path],
        columns: Optional[
            Union[
                Dict[str, Union[str, Feature, Any]],
                Dict[int, Union[str, Feature, Any]],
            ]
        ] = None,
        use_pyarrow: bool = False,
    ) -> DataFrame:
        if columns is None:
            cols_to_select, _, new_columns = None, None, None
        else:
            cols_to_select, _, new_columns = cls._parse_columns(columns)

        data = read_parquet(
            source=path,
            columns=cols_to_select,
            storage_options=DataFrame._get_storage_options(),
            use_pyarrow=use_pyarrow,
        )
        if new_columns is not None:
            data = data.rename({c: new_columns[i] for i, c in enumerate(data.columns)})
        return cls(data)

    @classmethod
    @overload
    def _parse_columns(
        cls,
        col_mapping: dict[int, Union[str, Feature, FeatureWrapper, Any]],
    ) -> Tuple[list[int], List[Type[pl.DataType]], List[str]]:
        ...

    @classmethod
    @overload
    def _parse_columns(
        cls,
        col_mapping: dict[str, Union[str, Feature, FeatureWrapper, Any]],
    ) -> Tuple[list[str], List[Type[pl.DataType]], List[str]]:
        ...

    @classmethod
    def _parse_columns(
        cls,
        col_mapping: dict[TIntStr, Union[str, Feature, FeatureWrapper, Any]],
    ) -> Tuple[list[TIntStr], List[Type[pl.DataType]], List[str]]:
        if not isinstance(col_mapping, dict):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise ValueError(f"Invalid column mapping. Received '{type(col_mapping).__name__}'; expected dict")
        columns = []
        dtypes = []
        new_cols: List[str] = []
        for k, v in col_mapping.items():
            columns.append(k)
            new_cols.append(str(v))
            dtypes.append(ensure_feature(v).converter.polars_dtype)
        return columns, dtypes, new_cols

    @classmethod
    def read_csv(
        cls,
        path: Union[str, pathlib.Path],
        has_header: bool = True,
        columns: Optional[
            Union[
                Dict[str, Union[str, Feature, Any]],
                Dict[int, Union[str, Feature, Any]],
            ]
        ] = None,
    ) -> DataFrame:
        """Read a .csv file as a `DataFrame`.

        Parameters
        ----------
        path
            The path to the .csv file. This may be a S3 or GCS
            storage url.
        has_header
            Whether the .csv file has a header row as the first row.
        columns
            A mapping of index to feature name.

        Returns
        -------
        DataFrame
            A `DataFrame` with the contents of the file loaded as features.

        Examples
        --------
        >>> values = DataFrame.read_csv(
        ...     "s3://...",
        ...     columns={0: MyFeatures.id, 1: MyFeatures.name},
        ...     has_header=False,
        ... )
        """
        try:
            import polars as pl
        except ImportError:
            raise missing_dependency_exception("chalkpy[runtime]")

        if columns is None:
            cols_to_select, dtypes, new_columns = None, None, None
        else:
            cols_to_select, dtypes, new_columns = cls._parse_columns(columns)

        # 'dtypes' deprecated for 'schema_overrides' in polars 0.20+, but parameter renamed without breaking
        data = pl.read_csv(
            source=path,
            has_header=has_header,
            columns=cols_to_select,
            dtypes=dtypes,  # pyright: ignore[reportCallIssue]
            new_columns=new_columns,
            storage_options=DataFrame._get_storage_options(),
        )
        return cls(data)

    @classmethod
    def read_avro(
        cls,
        path: Union[str, pathlib.Path],
    ) -> DataFrame:
        """Read a `.avro` file as a `DataFrame`.

        Parameters
        ----------
        path
            The path to the `.avro` file. This may be a S3 or GCS
            storage url.

        Returns
        -------
        DataFrame
            A `DataFrame` with the contents of the file loaded as features.

        Examples
        --------
        >>> values = DataFrame.read_avro(
        ...     "s3://...",
        ... )
        """
        try:
            import polars as pl
        except ImportError:
            raise missing_dependency_exception("chalkpy[runtime]")

        if isinstance(path, str) and path.startswith("s3://"):
            try:
                import fsspec
            except ImportError:
                raise missing_dependency_exception("fsspec")
            try:
                import s3fs
            except ImportError:
                raise missing_dependency_exception("s3fs")
            else:
                del s3fs
            try:
                import io
            except ImportError:
                raise missing_dependency_exception("io")
            with fsspec.open(path, "rb") as f:
                f = cast(IO[bytes], f)
                buffer = io.BytesIO(initial_bytes=f.read())
                data = pl.read_avro(buffer)
        else:
            data = pl.read_avro(source=path)
        return cls(data)

    def _parse_underscore(self, exp: Underscore) -> Any:
        if self._pydantic_model:
            context = self
            is_pydantic = True
        else:
            context = self.references_feature_set
            is_pydantic = False
        return parse_underscore_in_context(exp=exp, context=context, is_pydantic=is_pydantic)

    #############
    # Aggregation
    #############

    def max(self) -> DataFrame:
        """Compute the max value of each of the columns in the `DataFrame`.
        The resulting `DataFrame` will have a single row with the max value
        of each column.

        Returns
        -------
        DataFrame
            A `DataFrame` with the max value of each column.

        Examples
        --------
        >>> from chalk.features import DataFrame
        >>> df = DataFrame(
        ...     {
        ...         User.id: [1, 2, 3],
        ...         User.val: [1, 4, 10],
        ...     }
        ... ).max()
        ╭─────────┬──────────╮
        │ User.id │ User.val │
        ╞═════════╪══════════╡
        │ 3       │ 10       │
        ╰─────────┴──────────╯
        """
        return DataFrame(self._underlying.max(), convert_dtypes=False, pydantic_model=self._pydantic_model)

    def mean(self) -> DataFrame:
        """Compute the mean value of each of the columns in the `DataFrame`.
        The resulting `DataFrame` will have a single row with the mean value
        of each column.

        Returns
        -------
        DataFrame
            A `DataFrame` with the mean value of each column.

        Examples
        --------
        >>> from chalk.features import DataFrame
        >>> df = DataFrame(
        ...     {
        ...         User.id: [1, 2, 3],
        ...         User.val: [1, 4, 10],
        ...     }
        ... ).mean()
        ╭─────────┬──────────╮
        │ User.id │ User.val │
        ╞═════════╪══════════╡
        │ 2       │ 5        │
        ╰─────────┴──────────╯
        """
        return DataFrame(self._underlying.mean(), convert_dtypes=False, pydantic_model=self._pydantic_model)

    def median(self) -> DataFrame:
        """Compute the median value of each of the columns in the `DataFrame`.
        The resulting `DataFrame` will have a single row with the median value
        of each column.

        Returns
        -------
        DataFrame
            A `DataFrame` with the median value of each column.

        Examples
        --------
        >>> from chalk.features import DataFrame
        >>> df = DataFrame(
        ...     {
        ...         User.id: [1, 2, 3],
        ...         User.val: [1, 4, 10],
        ...     }
        ... ).median()
        ╭─────────┬──────────╮
        │ User.id │ User.val │
        ╞═════════╪══════════╡
        │ 2       │ 4        │
        ╰─────────┴──────────╯
        """
        return DataFrame(self._underlying.median(), convert_dtypes=False, pydantic_model=self._pydantic_model)

    def min(self) -> DataFrame:
        """Compute the min value of each of the columns in the `DataFrame`.
        The resulting `DataFrame` will have a single row with the min value
        of each column.

        Returns
        -------
        DataFrame
            A `DataFrame` with the min value of each column.

        Examples
        --------
        >>> from chalk.features import DataFrame
        >>> df = DataFrame(
        ...     {
        ...         User.id: [1, 2, 3],
        ...         User.val: [1, 4, 10],
        ...     }
        ... ).min()
        ╭─────────┬──────────╮
        │ User.id │ User.val │
        ╞═════════╪══════════╡
        │ 1       │ 1        │
        ╰─────────┴──────────╯
        """
        return DataFrame(self._underlying.min(), convert_dtypes=False, pydantic_model=self._pydantic_model)

    def std(self, ddof: int = 1) -> DataFrame:
        """Compute the standard deviation of each of the columns in the `DataFrame`.
        The resulting `DataFrame` will have a single row with the standard deviation
        of each column.

        Parameters
        ----------
        ddof
            "Delta Degrees of Freedom": the divisor used in the calculation is N - ddof,
            where N represents the number of elements. By default, ddof is 1.

        Returns
        -------
        DataFrame
            A `DataFrame` with the standard deviation of each column.

        Examples
        --------
        >>> from chalk.features import DataFrame
        >>> df = DataFrame(
        ...     {
        ...         User.id: [1, 2, 3],
        ...         User.val: [1, 4, 10],
        ...     }
        ... ).std()
        ╭─────────┬──────────╮
        │ User.id │ User.val │
        ╞═════════╪══════════╡
        │ 1       │ 4.5826   │
        ╰─────────┴──────────╯
        """
        return DataFrame(self._underlying.std(ddof), convert_dtypes=False, pydantic_model=self._pydantic_model)

    def sum(self) -> DataFrame:
        """
        Compute the sum of each of the columns in the `DataFrame`.
        The resulting `DataFrame` will have a single row with the sum
        of each column.

        Returns
        -------
        DataFrame
            A `DataFrame` with the sum of each column.
        """
        # Treat missing sums as zero
        return DataFrame(
            self._underlying.sum().fill_null(0),
            convert_dtypes=False,
            pydantic_model=self._pydantic_model,
        )

    def var(self, ddof: int = 1) -> DataFrame:
        """Compute the variance of each of the columns in the `DataFrame`.

        Parameters
        ----------
        ddof
            "Delta Degrees of Freedom": the divisor used in the calculation is N - ddof,
            where N represents the number of elements. By default, ddof is 1.

        Returns
        -------
        DataFrame
            A `DataFrame` with the variance of each column.

        """
        return DataFrame(self._underlying.var(ddof), convert_dtypes=False, pydantic_model=self._pydantic_model)

    ####################
    # Summary Operations
    ####################

    # These ops require us to materialize the dataframe.

    def _materialize(self) -> pl.DataFrame:
        materialized = self._underlying.collect()
        self._underlying = materialized.lazy()
        return materialized

    def any(self) -> bool:
        """Returns whether any the values in the `DataFrame` are truthy.
        Requires the `DataFrame` to only contain boolean values.
        """
        import polars as pl

        if len(self) == 0:
            return False
        if not all(isinstance(x, type) and issubclass(x, pl.Boolean) for x in self._underlying.dtypes):
            raise TypeError("DataFrame.any() is not defined on a dataframe that contains non-boolean columns.")
        materialized = self._materialize()
        return any(col.any() for col in materialized.get_columns())

    def all(self) -> bool:
        """Returns whether all the values in the `DataFrame` are truthy.
        Requires the `DataFrame` to only contain boolean values.
        """
        import polars as pl

        if len(self) == 0:
            return True

        if any(
            (not isinstance(x, type) or not issubclass(x, pl.Boolean))
            and x != pl.Boolean  # pyright: ignore[reportUnnecessaryComparison]
            for x in self._underlying.dtypes
        ):
            raise TypeError("DataFrame.any() is not defined on a DataFrame that contains non-boolean columns.")
        materialized = self._materialize()
        return all(col.all() for col in materialized.get_columns())

    def __len__(self) -> int:
        """Returns the number of rows in the `DataFrame`.

        Returns
        -------
        int
            The number of rows in the `DataFrame`.

        Examples
        --------
        >>> from chalk.features import DataFrame
        >>> df = DataFrame(
        ...     {
        ...         User.id: [1, 2, 3],
        ...         User.val: [1, 4, 10],
        ...     }
        ... )
        >>> len(df)
        3
        """

        materialized = self._materialize()
        return len(materialized)

    def count(self) -> int:
        """Returns the number of rows in the `DataFrame`.

        Returns
        -------
        int
            The number of rows in the `DataFrame`.

        Examples
        --------
        >>> from chalk.features import DataFrame
        >>> df = DataFrame(
        ...     {
        ...         User.id: [1, 2, 3],
        ...         User.val: [1, 4, 10],
        ...     }
        ... )
        >>> len(df)
        3
        >>> df.count()
        3
        """
        return len(self)

    @property
    def shape(self) -> tuple[int, int]:
        """The shape of the `DataFrame` as a `tuple` of `(num_rows, num_columns)`.

        Examples
        --------
        >>> DataFrame({User.id: [1, 2, 3, 4, 5]}).shape
        (5, 1)
        """
        materialized = self._materialize()
        return materialized.shape

    def item(self):
        """Get the only item from the `DataFrame`.
        This method will raise an error if the `DataFrame` contains
        more than one row or more than column.
        """
        materialized = self._materialize()
        if materialized.shape == (1, 1):
            return materialized.rows()[0][0]
        raise ValueError(
            "The dataframe contains multiple items. DataFrame.item() can only be used if the dataframe has a single element."
        )

    def sort(
        self,
        by: Union[str, Feature, Any, Iterable[Union[str, Feature, Any]]],
        *more_by: Union[str, Feature, Any],
        descending: Union[bool, Sequence[bool]] = False,
        nulls_last: bool = False,
    ) -> DataFrame:
        """Sort the `DataFrame` by the given columns.

        Parameters
        ----------
        by
            Feature(s) to sort by. Strings are parsed as feature names.
        more_by
            Additional columns to sort by, specified as positional arguments.
        descending
            Sort in descending order. When sorting by multiple columns,
            can be specified per feature by passing a sequence of booleans.
        nulls_last
            Place null values last.

        Returns
        -------
        DataFrame
            A new `DataFrame` with the rows sorted.

        Examples
        --------
        >>> df = DataFrame({
        ...     User.a: [1, 2, 3],
        ...     User.b: [3, 2, 1],
        ... })
        >>> df.sort(User.a)
              a  b
        -----------
        0     1  3
        1     2  2
        2     3  1
        """
        parsed_by = tuple(str(x) for x in itertools.chain(ensure_tuple(by), more_by))
        return DataFrame(
            self._underlying.sort(
                by=parsed_by,
                descending=descending,
                nulls_last=nulls_last,
            ),
            convert_dtypes=False,
            pydantic_model=self._pydantic_model,
        )

    def __bool__(self):
        if self.shape == (1, 1):
            # It's a dataframe of 1 item. self.any() and self.all() would return the same thing
            return self.all()
        raise ValueError("__bool__ is ambiguous on a DataFrame. Instead, use DataFrame.any() or DataFrame.all().")

    def __str__(self):
        materialized = self._materialize()
        return str(materialized)

    def __repr__(self):
        materialized = self._materialize()
        return repr(materialized)

    def __float__(self):
        return float(self.item())

    def __int__(self):
        return int(self.item())

    ############################
    # Arithmetic and Comparisons
    ############################

    # These ops require us to materialize the dataframe.

    def _perform_op(
        self,
        op: Union[str, Callable[[Any, Any], Any]],
        other: Union[DataFrame, pl.DataFrame, pd.DataFrame, Any],
        convert_dtypes: bool,
    ) -> DataFrame:
        import polars as pl

        materialized = self._materialize()
        if isinstance(other, DataFrame):
            other = other.to_polars()
        if isinstance(other, pl.LazyFrame):
            other = other.collect()
        try:
            import pandas as pd
        except ImportError:
            pass
        else:
            if isinstance(other, pd.DataFrame):
                other = pl.from_pandas(other)
        if op in ("eq", "ne", "lt", "le", "ge", "gt"):
            if isinstance(other, pl.DataFrame):
                return self._perform_comp_df(op, other, convert_dtypes=convert_dtypes)
            else:
                return DataFrame(
                    getattr(operator, op)(materialized, other),
                    convert_dtypes=convert_dtypes,
                    pydantic_model=self._pydantic_model,
                )

        assert callable(op)
        return DataFrame(
            op(materialized, other),
            convert_dtypes=convert_dtypes,
            pydantic_model=self._pydantic_model,
        )

    def _perform_comp_df(
        self,
        op: str,
        other: pl.DataFrame,
        convert_dtypes: bool,
    ) -> DataFrame:
        # There's a bug in the default polars implementation for comparisons -- see
        # https://github.com/pola-rs/polars/issues/5870
        import polars as pl

        materialized = self._materialize()
        if set(materialized.columns) != set(other.columns):
            raise ValueError(f"DataFrame columns do not match. {materialized.columns} != {other.columns}")
        # Put the columns in the same order
        other = other.select(materialized.columns)
        if materialized.shape != other.shape:
            raise ValueError("DataFrame dimensions do not match")

        suffix = "__POLARS_CMP_OTHER"
        other_renamed = other.select(pl.all().suffix(suffix))
        combined = pl.concat([materialized, other_renamed], how="horizontal")

        if op == "eq":
            expr = [
                (
                    pl.when(pl.col(n).is_null() & pl.col(f"{n}{suffix}").is_null())
                    .then(pl.lit(True))
                    .otherwise(pl.col(n) == pl.col(f"{n}{suffix}"))
                    .alias(n)
                )
                for n in materialized.columns
            ]
        elif op == "ne":
            expr = [
                (
                    pl.when(pl.col(n).is_null() & pl.col(f"{n}{suffix}").is_null())
                    .then(pl.lit(False))
                    .otherwise(pl.col(n) != pl.col(f"{n}{suffix}"))
                    .alias(n)
                )
                for n in materialized.columns
            ]
        elif op == "gt":
            expr = [pl.col(n) > pl.col(f"{n}{suffix}") for n in materialized.columns]
        elif op == "lt":
            expr = [pl.col(n) < pl.col(f"{n}{suffix}") for n in materialized.columns]
        elif op == "ge":
            expr = [
                (
                    pl.when(pl.col(n).is_null() & pl.col(f"{n}{suffix}").is_null())
                    .then(pl.lit(True))
                    .otherwise(pl.col(n) >= pl.col(f"{n}{suffix}"))
                    .alias(n)
                )
                for n in materialized.columns
            ]
        elif op == "le":
            expr = [
                (
                    pl.when(pl.col(n).is_null() & pl.col(f"{n}{suffix}").is_null())
                    .then(pl.lit(True))
                    .otherwise(pl.col(n) <= pl.col(f"{n}{suffix}"))
                    .alias(n)
                )
                for n in materialized.columns
            ]
        else:
            raise ValueError(f"got unexpected comparison operator: {op}")

        return DataFrame(combined.select(expr), convert_dtypes=convert_dtypes, pydantic_model=self._pydantic_model)

    def __eq__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: Union[DataFrame, pl.DataFrame, pl.LazyFrame, pd.DataFrame, Any]
    ):
        return self._perform_op("eq", other, convert_dtypes=False)

    def __ne__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: Union[DataFrame, pl.DataFrame, pl.LazyFrame, pd.DataFrame, Any]
    ):
        return self._perform_op("ne", other, convert_dtypes=False)

    def __gt__(self, other: Union[DataFrame, pl.DataFrame, pl.LazyFrame, pd.DataFrame, Any]):
        return self._perform_op("gt", other, convert_dtypes=False)

    def __lt__(self, other: Union[DataFrame, pl.DataFrame, pl.LazyFrame, pd.DataFrame, Any]):
        return self._perform_op("lt", other, convert_dtypes=False)

    def __ge__(self, other: Union[DataFrame, pl.DataFrame, pl.LazyFrame, pd.DataFrame, Any]):
        return self._perform_op("ge", other, convert_dtypes=False)

    def __le__(self, other: Union[DataFrame, pl.DataFrame, pl.LazyFrame, pd.DataFrame, Any]) -> DataFrame:
        return self._perform_op("le", other, convert_dtypes=False)

    def __add__(self, other: Union[DataFrame, pl.DataFrame, pl.LazyFrame, pd.DataFrame, Any]) -> DataFrame:
        return self._perform_op(operator.add, other, convert_dtypes=True)

    def __sub__(self, other: Union[DataFrame, pl.DataFrame, pl.LazyFrame, pd.DataFrame, Any]) -> DataFrame:
        return self._perform_op(operator.sub, other, convert_dtypes=True)

    def __mul__(self, other: Union[int, float]) -> DataFrame:
        return self._perform_op(operator.mul, other, convert_dtypes=True)

    def __truediv__(self, other: Union[int, float]) -> DataFrame:
        return self._perform_op(operator.truediv, other, convert_dtypes=True)

    def __floordiv__(self, other: Union[int, float]) -> DataFrame:
        return self._perform_op(operator.floordiv, other, convert_dtypes=True)

    def __mod__(self, other: Union[int, float]) -> DataFrame:
        return self._perform_op(operator.mod, other, convert_dtypes=True)

    def __pow__(self, other: Union[int, float]) -> DataFrame:
        return self._perform_op(operator.pow, other, convert_dtypes=True)

    ############
    # Conversion
    ############
    def to_polars(self, prefixed: bool = True) -> pl.LazyFrame:
        """Get the underlying `DataFrame` as a `polars.LazyFrame`.

        Parameters
        ----------
        prefixed
            Whether to prefix the column names with the feature namespace (i.e. if prefixed=True, `user.name`, if
             if prefixed=False, `name`)

        Returns
        -------
        polars.LazyFrame
            The underlying `polars.LazyFrame`.
        """
        output = self._underlying
        if not prefixed:
            alias_map = {f"{f.root_fqn}": f.name for f in self.columns}
            output = output.rename(alias_map)

        return output

    def to_pyarrow(self, prefixed: bool = True) -> pa.Table:
        """Get the underlying `DataFrame` as a `pyarrow.Table`.

        Parameters
        ----------
        prefixed
            Whether to prefix the column names with the feature namespace (i.e. if prefixed=True, `user.name`, if
             if prefixed=False, `name`)

        Returns
        -------
        pyarrow.Table
            The underlying `pyarrow.Table`. This format is the canonical
            representation of the data in Chalk.
        """
        materialized = self._materialize()
        pa_table = materialized.to_arrow()
        if self._convert_dtypes:
            pa_schema_fields: Dict[str, pa.DataType] = {}
            new_names: List[str] = []
            for col_fqn in pa_table.column_names:
                f = Feature.from_root_fqn(col_fqn)
                output_col_name = col_fqn
                if not prefixed:
                    output_col_name = f.name
                    new_names.append(output_col_name)

                if f.is_has_many:
                    # Special case for DataFrames -- restrict the struct type to only the fields that are present
                    full_dtype = f.converter.pyarrow_dtype
                    assert full_dtype is not None
                    present_field_names = [field.name for field in pa_table.schema.field(col_fqn).type.value_type]
                    new_fields = [full_dtype.value_type.field(name) for name in present_field_names]
                    pa_type = pa.large_list(pa.struct(new_fields))
                else:
                    pa_type = f.converter.pyarrow_dtype
                # For features within a has-many (user.transactions.amount), wrap them in a list[]
                for path_obj in f.path:
                    if path_obj.parent.is_has_many:
                        pa_type = pa.large_list(pa_type)
                pa_schema_fields[output_col_name] = pa_type

            if not prefixed:
                pa_table = pa_table.rename_columns(new_names)
            pa_table = pa_cast(pa_table, pa.schema(pa_schema_fields))
        return pa_table

    def to_pandas(self, string_names: bool = False, prefixed: bool = True) -> pd.DataFrame:
        """Get the underlying `DataFrame` as a `pandas.DataFrame`.

        Parameters
        ----------
        string_names
            If True, use strings for column names. If False, use `Feature` objects.

        prefixed
            Whether to prefix the column names with the feature namespace (i.e. if prefixed=True, `user.name`, if
             if prefixed=False, `name`)

        Returns
        -------
        pandas.DataFrame
            The data formatted as a `pandas.DataFrame`.
        """
        try:
            import pandas as pd
        except:
            raise missing_dependency_exception("chalkpy[pandas]")

        def types_mapper(dtype: pa.DataType):
            if dtype in (pa.utf8(), pa.large_utf8()):
                return pd.StringDtype("python")
            return None

        pd_dataframe = self._materialize().to_pandas(types_mapper=types_mapper)
        # For pandas, the columns should be the Features, not the root fqns
        # So, convert the columns to object types, and then set them to the features
        pd_dataframe.columns = pd_dataframe.columns.astype("object")

        if string_names:
            if prefixed:
                alias_map = {x.root_fqn: x.root_fqn for x in self.columns}
            else:
                alias_map = {x.root_fqn: x.name for x in self.columns}
        else:
            alias_map = {x.root_fqn: x for x in self.columns}
        pd_dataframe = pd_dataframe.rename(columns=alias_map)
        return pd_dataframe

    def to_features(self) -> Sequence[Features]:
        """Get values in the `DataFrame` as `Features` instances.

        Examples
        --------
        >>> df = DataFrame({
        ...     SpaceShip.id: [1, 2],
        ...     SpaceShip.volume: [4_000, 5_000]
        ... })
        >>> df.to_features()
        [
            SpaceShip(id=1, volume=4000),
            SpaceShip(id=2, volume=5000)
        ]
        """
        from chalk.features.feature_set import FeatureSetBase

        if self.namespace is None and self._pydantic_model is None:
            raise ValueError("This method is not supported if the DataFrame spans multiple namespaces")

        if self._pydantic_model is not None:
            # This definitely violates typing -- we should not have a PydanticModel be part of the DataFrame api
            return cast(Sequence["Features"], [self._pydantic_model(**row) for row in self.to_pyarrow().to_pylist()])

        ans: List[Features] = []
        for row in self.to_pyarrow().to_pylist():
            rooted_prefix_to_values: Dict[str, Dict[str, Any]] = {}

            for k, v in row.items():
                if k.startswith(f"{PSEUDONAMESPACE}."):
                    continue
                rooted_prefix_split = k.split(".")[:-1]
                for i in range(1, len(rooted_prefix_split) + 1):
                    rooted_prefix = ".".join(rooted_prefix_split[:i])
                    if rooted_prefix not in rooted_prefix_to_values:
                        rooted_prefix_to_values[rooted_prefix] = {}
                rooted_prefix_to_values[".".join(rooted_prefix_split)][k] = v
            # Sorting in reverse to construct the innermost features first
            sorted_sub_features = sorted(rooted_prefix_to_values.keys(), key=lambda x: len(x), reverse=True)

            for rooted_prefix in sorted_sub_features:
                values_are_lists = False
                if rooted_prefix != self.namespace:
                    rooted_prefix_feature = Feature.from_root_fqn(rooted_prefix)
                    values_are_lists = rooted_prefix_feature.is_has_many or rooted_prefix_feature.is_has_many_subfeature

                values = rooted_prefix_to_values[rooted_prefix]
                sub_kwargs: Dict[str, Any] = {}
                for k, v in values.items():
                    feature = Feature.from_root_fqn(k)
                    if is_map_in_dtype_tree(feature.converter.pyarrow_dtype):
                        v = recursive_convert_map_primitive(v, feature.converter.pyarrow_dtype)
                    if values_are_lists:
                        sub_kwargs[feature.attribute_name] = [feature.converter.from_primitive_to_rich(vv) for vv in v]
                    else:
                        sub_kwargs[feature.attribute_name] = feature.converter.from_primitive_to_rich(v)
                if rooted_prefix == self.namespace:
                    assert not values_are_lists, "Top level feature shouldn't be a has-many"
                    assert self.namespace is not None
                    features_cls = FeatureSetBase.registry[self.namespace]
                    ans.append(features_cls(**sub_kwargs))
                else:
                    rooted_prefix_split = rooted_prefix.split(".")
                    feature_cls = Feature.from_root_fqn(rooted_prefix).joined_class
                    assert feature_cls is not None
                    parent_rooted_prefix, feature_name = ".".join(rooted_prefix_split[:-1]), rooted_prefix_split[-1]
                    del feature_name  # unused
                    if values_are_lists:
                        feature_values = []
                        ks, vs = zip(*sub_kwargs.items())  # [k1, k2], [v1[...], v2[...]]
                        for row in zip(*vs):
                            feature_values.append(feature_cls(**dict(zip(ks, row))))
                        rooted_prefix_to_values[parent_rooted_prefix][rooted_prefix] = feature_values
                    else:
                        rooted_prefix_to_values[parent_rooted_prefix][rooted_prefix] = feature_cls(**sub_kwargs)
        return ans

    def slice(self, offset: int = 0, length: Optional[int] = None) -> DataFrame:
        """Slice the `DataFrame`.

        Parameters
        ----------
        offset
            The offset to start at.
        length
            The number of rows in the slice. If None (the default), include all rows from `offset`
            to the end of the `DataFrame`.

        Returns
        -------
        DataFrame
            The dataframe with the slice applied.
        """
        return DataFrame(self._underlying.slice(offset, length))


# Back-compat
DataFrameImpl = DataFrame
