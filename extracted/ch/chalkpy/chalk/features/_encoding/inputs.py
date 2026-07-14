import collections
import collections.abc
import dataclasses
import warnings
from typing import Any, Dict, Iterator, List, Mapping, Optional, Sequence, Tuple, Union, cast

import pyarrow as pa

from chalk.client.models import FeatureReference
from chalk.features import Features, FeatureWrapper, TPrimitive, ensure_feature, unwrap_feature
from chalk.features._encoding.json import FeatureEncodingOptions, unstructure_primitive_to_json
from chalk.features.feature_field import Feature, FeatureNotFoundException
from chalk.utils.json import TJSON


@dataclasses.dataclass
class InputEncodeOptions:
    encode_structs_as_objects: bool
    """c.f. encode_structs_as_objects in chalk.features._encoding.json.FeatureEncodingOptions"""

    json_encode: bool
    """
    If `True`, encode feature values into JSON. Specifically, structs/datetimes/bytes/etc. are encoded
    into a JSON-compatible format.
    If `False`, encode features values into a 'primitive' type (TPrimitive) but don't apply json encoding.
    This is needed for the HTTP client which sends feature data in JSON requests. However, the GRPC
    client transmits Arrow data which supports a richer set of types.
    """


HTTP_ENCODE_OPTIONS = InputEncodeOptions(json_encode=True, encode_structs_as_objects=False)
GRPC_ENCODE_OPTIONS = InputEncodeOptions(json_encode=False, encode_structs_as_objects=True)

InputSchemaHint = Mapping[FeatureReference, Union[FeatureReference, Sequence[FeatureReference]]]
"""
Specifies the expected type of an input column to hint the type when it cannot be inferred
from the value of the column.

For example, the schema of a has_many input can be specified to have a consistent value
even when the provided input is an empty collection of rows, e.g.
```
# Specify the columns as a sequence
input_schema_hint = { User.transactions: [Transaction.id, Transaction.amount] }
# Specify the columns as a projection of the has-many itself
input_schema_hint = { User.transactions: User.transactions[Transaction.id, Transaction.amount] }
# Specify with strings
input_schema_hint = { "user.transactions": ["transaction.id", "transaction.amount"] }
```
"""


def resolve_input_schema_hint(input_schema_hint: InputSchemaHint) -> Dict[str, Feature]:
    """
    Canonicalizes a user-provided `InputSchemaHint` into a mapping of projected features.

    For input `{User.txns: [Txn.id, Txn.amount]}`, resolves to a mapping of
    `{"user.txns": User.txns: [Txn.id, Txn.amount]}`.

    Support string inputs and recursive column projections.

    Without a hint for a column, empty collections like `[]` will typically be inferred to have
    a type like `list<null>` or fall back to a generic "all scalar columns in namespace".

    This ensures that the inferred schema is consistent across queries, allowing query plans
    to be re-used across queries which only differ in the number of items in input.
    """
    resolved: Dict[str, Feature] = {}
    for feature_ref, hint_value in input_schema_hint.items():
        feature = ensure_feature(feature_ref)
        if not feature.is_has_many:
            raise TypeError(
                f"input_schema_hint entry '{feature.root_fqn}' is not a has-many feature; "
                + "schema hints may only be provided for has-many inputs"
            )
        if feature.joined_class is None:
            raise ValueError(f"A has_many feature `{feature.root_fqn}` must have an associated joined class")
        foreign_namespace = feature.joined_class.namespace
        if isinstance(hint_value, collections.abc.Sequence) and not isinstance(hint_value, str):
            column_refs: Sequence[Any] = hint_value
        else:
            # A single reference to a projection of the has-many itself, e.g.
            # `{User.transactions: User.transactions[Transaction.id, Transaction.amount]}`.
            projection = ensure_feature(hint_value)
            if projection.root_fqn != feature.root_fqn:
                raise TypeError(
                    f"input_schema_hint value for '{feature.root_fqn}' references '{projection.root_fqn}'; "
                    + f"expected either a projection of '{feature.root_fqn}' itself or a sequence of its columns"
                )
            column_refs = _hint_columns(projection)
        column_features: List[Feature] = []
        for column_ref in column_refs:
            column = ensure_feature(column_ref)
            if column.namespace != foreign_namespace:
                raise TypeError(
                    f"input_schema_hint column '{column.root_fqn}' for has-many '{feature.root_fqn}' "
                    + f"must be a feature of its foreign namespace '{foreign_namespace}'"
                )
            column_features.append(column)
        resolved[feature.root_fqn] = unwrap_feature(FeatureWrapper(feature)[tuple(column_features)])
    return resolved


def input_schema_hint_to_projection_strings(input_schema_hint: InputSchemaHint) -> Dict[str, str]:
    """
    Serialize an input schema hint for the HTTP JSON payload, mapping each hinted input column
    to a projection string like `{"user.txns": "user.txns[txn.id,txn.amount]"}`.
    Only feature names are sent, the server has the authoritative datatype for each feature.
    Old Chalk servers that predate this field ignore it.
    """
    resolved = resolve_input_schema_hint(input_schema_hint)
    return {fqn: _projection_string(feature) for fqn, feature in resolved.items()}


def _projection_string(feature: Feature) -> str:
    if not feature.is_has_many:
        return feature.root_fqn
    columns = ",".join(_projection_string(column) for column in _hint_columns(feature))
    return f"{feature.root_fqn}[{columns}]"


def _hint_columns(feature: Feature) -> Sequence[Feature]:
    dataframe_typ = feature.typ.as_dataframe()
    assert dataframe_typ is not None, f"has-many feature '{feature.root_fqn}' must have a DataFrame annotation"
    return dataframe_typ.columns


def _validate_rows_against_hint(rows: Sequence[Mapping[str, Any]], columns: Sequence[Feature], has_many_fqn: str):
    """Raise if any row carries a column absent from the hinted projection.

    pyarrow silently drops dict keys that are not struct fields, which would let a caller bug
    (or a hint that drifted from the call site) silently discard data; missing hinted columns are
    fine and are null-filled by arrow.
    """
    allowed = {column.root_fqn: column for column in columns}
    for row in rows:
        for key, value in row.items():
            if key not in allowed:
                raise TypeError(
                    f"Input for has-many feature '{has_many_fqn}' contains column '{key}', which is not in "
                    + f"its input_schema_hint columns {sorted(allowed)}"
                )
            column = allowed[key]
            # Only a has-many column contains rows to recurse into; a scalar column may share the
            # same list-of-struct arrow shape (e.g. `List[SomeDataclass]`) but is opaque here.
            if column.is_has_many and isinstance(value, list):
                _validate_rows_against_hint(
                    [nested_row for nested_row in value if isinstance(nested_row, Mapping)],
                    _hint_columns(column),
                    has_many_fqn=column.root_fqn,
                )


def _recursive_unstructure_primitive_to_json(val: TPrimitive) -> TJSON:
    if isinstance(val, dict):
        return {cast(str, k): _recursive_unstructure_primitive_to_json(v) for k, v in val.items()}
    elif isinstance(val, (list, tuple)):
        return [_recursive_unstructure_primitive_to_json(x) for x in val]
    else:
        return unstructure_primitive_to_json(val)


def validate_iterable_values_in_mapping(inputs: Mapping[str, Sequence[Any]], method_name: Optional[str] = None):
    """
    If a method expects inputs of the form Mapping[str, Sequence[Any]], this function will confirm that the values are in fact sequences.
    In particular, because strings are considered sequences, an input `{"user.name": "Raphael"}` will typecheck but then be converted into a list of
    seven users "R", "a", ...

    Parameters
    ----------
    inputs
        Mapping from feature FQN to a sequence of values.
    method_name
        Optional method name used to improve warning messages.
    """
    try:
        import polars as pl
    except ImportError:
        pl = None

    if not isinstance(inputs, collections.abc.Mapping):  # pyright: ignore[reportUnnecessaryIsInstance]
        # Skip this logic for DataFrames, tables, etc.
        return
    for k, vv in inputs.items():
        if isinstance(vv, pa.Array):
            continue
        if pl is not None and isinstance(vv, pl.Series):
            continue

        function_text = "This function"
        if method_name is not None:
            function_text = f"The function {method_name}"

        if not isinstance(vv, collections.abc.Sequence):  # pyright: ignore[reportUnnecessaryIsInstance]
            message = f"""{function_text} accepts a mapping of string keys to Sequence's of values. For key '{k}', got a value of type {type(vv)!r} which is not a Sequence"""
        elif isinstance(vv, str):
            message = f"""{function_text} accepts a mapping of string keys to Sequence's of values. Key '{k}' has a string value which is likely an error. Did you mean to pass in a list of strings instead?"""
        else:
            continue
        warnings.warn(message)
        return


def recursive_encode_bulk_inputs(
    inputs: Mapping[str, Sequence[Any]],
    options: InputEncodeOptions,
    input_schema_hint: Optional[InputSchemaHint] = None,
) -> Tuple[Dict[str, Union[List[TJSON], pa.Array]], List[str]]:
    all_warnings: List[str] = []
    validate_iterable_values_in_mapping(inputs)
    if input_schema_hint and options.json_encode:
        # JSON-encoded values (datetimes as strings, ...) cannot be converted by arrow to the
        # hinted types, and the JSON wire format has no place to carry a schema yet.
        raise ValueError("input_schema_hint is currently only supported by the GRPC client")
    resolved_hint = resolve_input_schema_hint(input_schema_hint) if input_schema_hint else {}
    encoded_inputs: Dict[str, Union[List[TJSON], pa.Array]] = collections.defaultdict(list)
    for wrapped_feature, vv in inputs.items():
        try:
            feature = ensure_feature(wrapped_feature)
        except FeatureNotFoundException:
            fqn = str(wrapped_feature)
            all_warnings.append(
                f"Input '{fqn}' not recognized. Recursively JSON encoding '{fqn}' and requesting anyways"
            )
            if options.json_encode:
                encoded_inputs[str(fqn)] = [_recursive_unstructure_primitive_to_json(v) for v in vv]
            else:
                encoded_inputs[str(fqn)] = list(iter(vv))
            continue

        if feature.is_has_many:
            for v in vv:
                if not isinstance(v, list):
                    raise TypeError(f"has-many feature '{feature.fqn}' must be a list, but got {type(v).__name__}")

                has_many_result: List[Dict[str, TJSON]] = []
                assert feature.joined_class is not None
                foreign_namespace = feature.joined_class.namespace
                for item in v:
                    # The value can be either a feature instance or a dict
                    if isinstance(item, Features):
                        item = dict(item.items())
                    if not isinstance(item, dict):
                        raise TypeError(
                            (
                                f"Has-many feature '{feature.root_fqn}' must be a list of dictionaries or feature set instances, "
                                f"but got a list of `{type(item).__name__}`"
                            )
                        )
                    # Prepend the namespace onto the dict keys, if it's not already there
                    item = {
                        k if str(k).startswith(f"{foreign_namespace}.") else f"{foreign_namespace}.{str(k)}": sub_v
                        for (k, sub_v) in item.items()
                    }
                    result, inner_warnings = recursive_encode_inputs(item, options=options)
                    all_warnings.extend(inner_warnings)
                    has_many_result.append(result)

                encoded_inputs[feature.root_fqn].append(has_many_result)

            hint_feature = resolved_hint.get(feature.root_fqn)
            if hint_feature is not None:
                column_rows = encoded_inputs[feature.root_fqn]
                assert isinstance(column_rows, list)
                for rows in column_rows:
                    _validate_rows_against_hint(
                        cast(List[Dict[str, TJSON]], rows), _hint_columns(hint_feature), feature.root_fqn
                    )
                # An explicitly-typed array pins the wire schema regardless of the row data, so
                # e.g. all-empty inputs don't degenerate to list<null>.
                encoded_inputs[feature.root_fqn] = pa.array(column_rows, type=hint_feature.converter.pyarrow_dtype)
        elif feature.is_has_one:
            assert feature.joined_class is not None
            foreign_namespace = feature.joined_class.namespace
            for v in vv:
                # The value can be either a feature instance or a dict
                if isinstance(v, Features):
                    v = dict(v.items())
                if not isinstance(v, dict):
                    raise TypeError(
                        (
                            f"Has-one feature '{feature.root_fqn}' must be a list of dictionaries or feature set instances, "
                            f"but got a list of `{type(v).__name__}`"
                        )
                    )
                # Prepend the namespace onto the dict keys, if needed
                v = {
                    k if str(k).startswith(f"{foreign_namespace}.") else f"{foreign_namespace}.{str(k)}": sub_v
                    for (k, sub_v) in v.items()
                }
                has_one_values, inner_warnings = recursive_encode_inputs(v, options=options)
                all_warnings.extend(inner_warnings)
                # Flatten the has-one inputs onto the encoded inputs dict -- similar to how input
                # features
                root_parts = feature.root_fqn.split(".")
                for k, encoded_v in has_one_values.items():
                    # Chop off the namespace from the nested features, as the
                    # namespace is implied by the has-one feature
                    root_fqn = ".".join((*root_parts, *k.split(".")[1:]))
                    encoded_inputs[root_fqn].append(encoded_v)
        elif isinstance(vv, pa.Array):
            if options.json_encode:
                assert not isinstance(vv, (int, str, Sequence))
                raise ValueError(
                    f"The feature '{wrapped_feature}' contains an invalid value. Pyarrow arrays are only supported by the GRPC Chalk client. Cannot send a pyarrow array containing elements {vv.type} over the HTTP Chalk Client."
                )
            encoded_inputs[feature.root_fqn] = vv
        else:
            for v in vv:
                if feature.primary:
                    if not isinstance(v, (int, str)):
                        raise TypeError(
                            f"Input '{v}' for primary feature {feature.root_fqn} must be of type int or str"
                        )
                if options.json_encode:
                    if isinstance(v, pa.Scalar):
                        assert not isinstance(v, (int, str))
                        raise ValueError(
                            f"The feature '{wrapped_feature}' contains an invalid value. Pyarrow arrays are only supported by the GRPC Chalk client. Cannot send a pyarrow array containing elements {v.type} over the HTTP Chalk Client."
                        )
                    converted_value = feature.converter.from_rich_to_json(
                        v,
                        # Allowing missing values because the server could be on a different version of the code that has a default
                        missing_value_strategy="allow",
                        # (pyarrow.RecordBatch.from_pydict expects dict's for struct data, as opposed to an array.)
                        options=FeatureEncodingOptions(encode_structs_as_objects=options.encode_structs_as_objects),
                    )
                else:
                    if isinstance(v, pa.Scalar):
                        converted_value = v
                    else:
                        converted_value = feature.converter.from_rich_to_primitive(
                            v,
                            # Allowing missing values because the server could be on a different version of the code that has a default
                            missing_value_strategy="allow",
                        )

                encoded_inputs[feature.root_fqn].append(converted_value)
    return encoded_inputs, all_warnings


def recursive_encode_inputs(
    inputs: Mapping[str, Any], options: InputEncodeOptions = HTTP_ENCODE_OPTIONS
) -> Tuple[Dict[str, Union[TJSON, pa.Scalar]], List[str]]:
    bulk_result, warnings = recursive_encode_bulk_inputs({k: [v] for k, v in inputs.items()}, options=options)
    return {k: next(iter(v)) for (k, v) in bulk_result.items()}, warnings


def _flatten_feature_instance(
    instance: Features, prefix: str, root_namespace: str, strip_namespace: bool
) -> Iterator[Tuple[str, Any]]:
    """Recursively flatten a feature instance, yielding (key, value) pairs."""
    for fqn, value in instance.items():
        if strip_namespace:
            # Strip the namespace from the fqn to get the relative key
            relative_key = fqn.removeprefix(f"{instance.__chalk_namespace__}.")
            full_key = f"{prefix}.{relative_key}" if prefix else relative_key
        else:
            full_key = fqn

        if isinstance(value, Features):
            # Recursively flatten nested has-one features
            yield from _flatten_feature_instance(value, full_key, root_namespace, strip_namespace)
        else:
            yield full_key, value


def features_to_columnar(instances: Sequence[Features], strip_namespace: bool = True) -> Dict[str, List[Any]]:
    """
    Convert a list of feature instances (row-oriented) to a columnar dict.

    Handles nested has-one relationships by flattening them with dotted keys.

    Parameters
    ----------
    instances
        A list of feature class instances, e.g. [User(id=1, name="Alice"), User(id=2, name="Bob")]
    strip_namespace
        If `True`, strip the root namespace from the keys. e.g. "user.name" becomes "name".
        If `False`, keep the full FQN as keys.

    Returns
    -------
    Dict[str, List[Any]]
        A dict mapping feature names to lists of values, e.g. {"id": [1, 2], "name": ["Alice", "Bob"]}
    """
    if not instances:
        return {}

    result: Dict[str, List[Any]] = collections.defaultdict(list)
    root_namespace = instances[0].__chalk_namespace__

    for instance in instances:
        for key, value in _flatten_feature_instance(instance, "", root_namespace, strip_namespace):
            result[key].append(value)

    return dict(result)
