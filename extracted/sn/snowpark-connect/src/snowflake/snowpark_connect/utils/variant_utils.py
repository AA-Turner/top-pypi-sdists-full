#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#
from collections import defaultdict

import snowflake.snowpark.functions as snowpark_fn
import snowflake.snowpark.types as snowpark_type
from snowflake import snowpark
from snowflake.snowpark import Session


def _contains_array_type(typ: snowpark_type.DataType) -> bool:
    """Check if a data type is or contains an ArrayType."""
    if isinstance(typ, snowpark_type.ArrayType):
        return True
    if isinstance(typ, snowpark_type.StructType):
        return any(_contains_array_type(field.datatype) for field in typ.fields)
    if isinstance(typ, snowpark_type.MapType):
        return _contains_array_type(typ.key_type) or _contains_array_type(
            typ.value_type
        )
    return False


# This is a temporary fix for issue in snowpark. Remove once SNOW-3071683 will be resolved
def to_variant_preserving_nulls(
    col: snowpark.Column, typ: snowpark.types.DataType
) -> snowpark.Column:
    """Cast a column to VariantType, preserving null elements inside arrays.

    When casting an array to VARIANT, SQL NULL elements become SQL NULLs (absent values)
    rather than JSON nulls.  This function transforms null elements within arrays to
    PARSE_JSON('null') so they are preserved as JSON null values in the resulting VARIANT.

    Uses the same analyzer-based recursive pattern as ``_coerce_to_type`` in
    ``map_unresolved_function.py``: the function calls itself with a placeholder
    column, serialises the resulting expression tree to SQL via the analyzer,
    then injects that SQL into a TRANSFORM (for arrays) or REDUCE (for maps)
    lambda.  This naturally handles arbitrary nesting depth without manual
    variable-name bookkeeping.

    Handles:
    - ArrayType (including nested arrays like ArrayType(ArrayType(StringType)))
    - StructType containing arrays
    - MapType whose values contain arrays (casts MAP→OBJECT first so
      OBJECT_KEYS works)
    For types that don't contain arrays, a simple cast to VariantType is used.
    """
    if isinstance(typ, snowpark_type.ArrayType):
        # Recursively build the expression for the element type using a
        # placeholder column "x", then serialize to SQL for the TRANSFORM lambda.
        analyzer = Session.get_active_session()._analyzer
        fn_sql = analyzer.analyze(
            to_variant_preserving_nulls(
                snowpark_fn.col("x"), typ.element_type
            )._expression,
            defaultdict(),
        )

        transformed = snowpark_fn.call_function(
            "transform",
            col,
            snowpark_fn.sql_expr(f"x -> IFNULL({fn_sql}, PARSE_JSON('null'))"),
        )
        return snowpark_fn.cast(transformed, snowpark_type.VariantType())
    elif isinstance(typ, snowpark_type.StructType) and _contains_array_type(typ):
        # For structs containing arrays, handle each field recursively and
        # rebuild via OBJECT_CONSTRUCT.
        construct_args = []
        for field in typ.fields:
            field_col = col[field.name]
            construct_args.append(snowpark_fn.lit(field.name))
            if _contains_array_type(field.datatype):
                construct_args.append(
                    to_variant_preserving_nulls(field_col, field.datatype)
                )
            else:
                construct_args.append(
                    snowpark_fn.cast(field_col, snowpark_type.VariantType())
                )
        return snowpark_fn.cast(
            snowpark_fn.object_construct_keep_null(*construct_args),
            snowpark_type.VariantType(),
        )
    elif isinstance(typ, snowpark_type.MapType) and _contains_array_type(typ):
        # OBJECT_KEYS does not accept MAP type directly, so cast to OBJECT
        # first via TO_OBJECT.
        obj_col = snowpark_fn.call_function("to_object", col)

        # Recursively build the value-coercion expression using a placeholder
        # column "v", then serialize to SQL.
        analyzer = Session.get_active_session()._analyzer
        fn_sql = analyzer.analyze(
            to_variant_preserving_nulls(
                snowpark_fn.col("v"), typ.value_type
            )._expression,
            defaultdict(),
        )

        # Replace placeholder "V" with a reference to the original map value
        # via the state array:  state[1] = original object, k = current key.
        fn_sql_with_value = fn_sql.replace('"V"', "strip_null_value(GET(state[1], k))")

        # REDUCE lambda: (state, k) -> [updated_result_object, original_object]
        lambda_expr = (
            f"(state, k) -> ARRAY_CONSTRUCT("
            f"object_insert(state[0], k, ({fn_sql_with_value})::variant, true), "
            f"state[1])"
        )

        reduce_result = snowpark_fn.call_function(
            "reduce",
            snowpark_fn.call_function("object_keys", obj_col),
            snowpark_fn.array_construct(
                snowpark_fn.object_construct(),  # state[0]: empty result object
                obj_col,  # state[1]: original map as OBJECT
            ),
            snowpark_fn.sql_expr(lambda_expr),
        )
        # Extract the result object (state[0]) from the final state
        return snowpark_fn.get(reduce_result, snowpark_fn.lit(0))
    else:
        return snowpark_fn.cast(col, snowpark_type.VariantType())
