import io
import logging
import pathlib
import typing
import uuid
import warnings

import numpy as np
import polars as pl

from .._auxlib._unpack_hex_bits import unpack_hex_bits
from ._impl._check_expected_columns import check_expected_columns


def _check_df(df: pl.DataFrame) -> None:
    """Validate input DataFrame for unpack_data_packed.

    Raises a ValueError if any of the required columns are missing from the
    DataFrame.
    """
    check_expected_columns(
        df,
        expected_columns=[
            "data_hex",
            "dstream_algo",
            "dstream_storage_bitoffset",
            "dstream_storage_bitwidth",
            "dstream_T_bitoffset",
            "dstream_T_bitwidth",
            "dstream_S",
        ],
    )


def _enforce_hex_aligned(df: pl.DataFrame, col: str) -> None:
    """Raise NotImplementedError if column is not hex-aligned (i.e., not a
    multiple of 4 bits)."""
    if (
        not df.lazy()
        .filter((pl.col(col) & pl.lit(0b11) != 0))
        .limit(1)
        .collect()
        .is_empty()
    ):
        raise NotImplementedError(f"{col} not hex-aligned")


def _make_empty() -> pl.DataFrame:
    """Create an empty DataFrame with the expected columns for
    unpack_data_packed, handling edge case of empty input."""
    return pl.DataFrame(
        [
            pl.Series(name="dstream_algo", values=[], dtype=pl.String),
            pl.Series(name="dstream_data_id", values=[], dtype=pl.UInt64),
            pl.Series(name="downstream_version", values=[], dtype=pl.String),
            pl.Series(name="dstream_S", values=[], dtype=pl.UInt32),
            pl.Series(name="dstream_T", values=[], dtype=pl.UInt64),
            pl.Series(name="dstream_storage_hex", values=[], dtype=pl.String),
        ],
    )


def _calculate_offsets(df: pl.DataFrame) -> pl.DataFrame:
    for col in (
        "dstream_storage_bitoffset",
        "dstream_storage_bitwidth",
        "dstream_T_bitoffset",
        "dstream_T_bitwidth",
    ):
        _enforce_hex_aligned(df, col)
        df = df.with_columns(
            **{col.replace("_bit", "_hex"): np.right_shift(pl.col(col), 2)},
        )

    for what in "dstream_storage", "dstream_T":
        hexoffset = f"{what}_hexoffset"
        hexwidth = f"{what}_hexwidth"
        out_of_bounds = (
            df.lazy()
            .filter(
                pl.col(hexoffset) + pl.col(hexwidth)
                > pl.col("data_hex").str.len_bytes(),
            )
            .collect()
        )
        if not out_of_bounds.is_empty():
            raise ValueError(
                f"{what} offset/width out of bounds, "
                f"{out_of_bounds['data_hex'].str.len_bytes().to_list()[:10]=} "
                f"{out_of_bounds[hexoffset].to_list()[:10]=} "
                f"{out_of_bounds[hexwidth].to_list()[:10]=} "
                f"{out_of_bounds[:10]=}",
            )

    return df


def _deserialize_h_matrix(h_matrix_str: str) -> np.ndarray:
    """Deserialize a parity-check (H) matrix string to a numpy array.

    The H matrix is a boolean matrix where rows are parity constraints
    and columns correspond to bit positions in the data. The input
    string should have space-separated 0/1 digits with rows delimited
    by newlines, suitable for direct parsing by ``np.loadtxt``.
    """
    try:
        h_matrix = np.loadtxt(
            io.StringIO(h_matrix_str),
            dtype=np.uint8,
            ndmin=2,
        )
    except Exception:
        logging.error(f"failed to parse H matrix: {h_matrix_str!r}")
        raise

    if (h_matrix > 1).any():
        raise ValueError(
            f"H matrix contains values other than 0 and 1: "
            f"{np.unique(h_matrix).tolist()}",
        )

    return h_matrix


def _apply_data_parity0(df: pl.DataFrame) -> pl.DataFrame:
    """Apply downstream_data_parity0_rule to compute parity syndrome.

    If 'downstream_data_parity0_rule' column is present, computes the
    parity check result for each row's data_hex against its H matrix
    and stores the result in 'downstream_data_parity0_result'.

    Groups by unique H matrix strings to deserialize each only once,
    then performs vectorized bulk computation across all rows sharing
    the same H matrix.
    """
    df_len = df.lazy().select(pl.len()).collect().item()
    parity_result = np.zeros(df_len, dtype=int)

    logging.info(" - filtering non-empty parity rules...")
    indexed = (
        df.lazy()
        .with_row_index("_downstream_parity_idx")
        .filter(
            pl.col("downstream_data_parity0_rule").is_not_null()
            & (
                pl.col("downstream_data_parity0_rule")
                .cast(pl.String)
                .str.len_bytes()
                > 0
            ),
        )
    )
    indexed_len = indexed.select(pl.len()).collect().item()
    logging.info(
        f" - {indexed_len} of {df_len} row(s) have parity rules...",
    )
    unique_rules = (
        indexed.select("downstream_data_parity0_rule")
        .unique()
        .collect()
        .to_series()
        .to_list()
    )
    for h_matrix_str in unique_rules:
        group = indexed.filter(
            pl.col("downstream_data_parity0_rule") == h_matrix_str,
        )
        num_rows = group.select(pl.len()).collect().item()
        indices = (
            group.select("_downstream_parity_idx").collect().to_numpy().ravel()
        )

        logging.info(f" - deserializing H matrix for {num_rows} row(s)...")
        h_matrix = _deserialize_h_matrix(str(h_matrix_str))
        logging.info(f" - H matrix has {h_matrix.shape[0]} parity rule(s)...")

        logging.info(f" - concatenating data_hex for {num_rows} row(s)...")
        concat_hex = (
            group.select(pl.col("data_hex").str.join("")).collect().item()
        )
        hex_len = (
            group.select(pl.col("data_hex").str.len_bytes().first())
            .collect()
            .item()
        )
        logging.info(" - converting hex to bits...")
        all_bits = unpack_hex_bits(concat_hex)

        bits_per_row = hex_len * 4
        data_matrix = all_bits.reshape(num_rows, bits_per_row)

        if h_matrix.shape[1] != bits_per_row:
            raise ValueError(
                f"H matrix column count {h_matrix.shape[1]} does not "
                f"match data_hex bit length {bits_per_row}, "
                f"H matrix: {h_matrix_str!r}",
            )

        logging.info(f" - computing syndromes for {num_rows} row(s)...")
        syndromes = (data_matrix @ h_matrix.T) % 2
        row_violations = np.sum(syndromes, axis=1)
        total_violations = int(np.sum(row_violations))
        logging.info(
            f" - data parity0: {total_violations} rule violation(s) "
            f"across {h_matrix.shape[0]} rule(s) occurring in "
            f"{int(np.count_nonzero(row_violations))} "
            f"row(s)",
        )
        parity_result[indices] = row_violations

    return df.with_columns(
        downstream_data_parity0_result=pl.Series(
            parity_result,
            dtype=pl.UInt32,
        ),
    ).drop("downstream_data_parity0_rule")


def _extract_from_data_hex(df: pl.DataFrame) -> pl.DataFrame:
    return (
        df.lazy()
        .with_columns(
            dstream_storage_hex=pl.col("data_hex").str.slice(
                pl.col("dstream_storage_hexoffset"),
                length=pl.col("dstream_storage_hexwidth"),
            ),
            dstream_T=pl.col("data_hex")
            .str.slice(
                pl.col("dstream_T_hexoffset"),
                length=pl.col("dstream_T_hexwidth"),
            )
            .str.to_integer(base=16),
        )
        .drop(
            [
                "data_hex",
                "dstream_storage_hexoffset",
                "dstream_storage_hexwidth",
                "dstream_T_hexoffset",
                "dstream_T_hexwidth",
                "dstream_storage_bitoffset",
                "dstream_storage_bitwidth",
                "dstream_T_bitoffset",
                "dstream_T_bitwidth",
            ],
        )
        .collect()
    )


def _perform_validations(
    df: pl.DataFrame,
    col_name: str,
) -> pl.DataFrame:
    validator_strs = (
        df.lazy()
        .select(pl.col(col_name))
        .unique()
        .collect()
        .to_series()
        .drop_nulls()
        .replace("", None)
        .drop_nulls()
        .to_list()
    )
    for validator in validator_strs:
        validation_expr = eval(validator, {"pl": pl})
        group = df.lazy().filter(pl.col(col_name) == validator)
        if not group.select(validation_expr.all()).collect().item():
            err_msg = f"{col_name} `{validator}` failed"
            logging.error(err_msg)
            failed_rows = group.filter(~validation_expr).collect()
            logging.error(failed_rows.glimpse(return_type="str"))
            for dump_path in (
                pathlib.Path.home()
                / f"downstream_validation_fail_{uuid.uuid4()}.pqt",
                f"/tmp/downstream_validation_fail_{uuid.uuid4()}.pqt",  # nosec B108
            ):
                try:
                    failed_rows.write_parquet(dump_path)
                    logging.error(f"failing rows dumped to {dump_path}")
                    break
                except Exception as e:
                    logging.error(
                        f"failed to dump rows to {dump_path}: {e}",
                    )
            raise ValueError(err_msg)

    df = df.drop(col_name)
    logging.info(f" - {len(validator_strs)} validation(s) passed!")

    return df


def _apply_filters(
    df: pl.DataFrame,
    col_name: str,
) -> pl.DataFrame:
    num_before = df.lazy().select(pl.len()).collect().item()
    filter_strs = (
        df.lazy()
        .select(pl.col(col_name))
        .unique()
        .collect()
        .to_series()
        .drop_nulls()
        .replace("", None)
        .drop_nulls()
        .to_list()
    )
    combined_expr = pl.lit(True)
    for filter_expr_str in filter_strs:
        combined_expr = (
            pl.when(pl.col(col_name) == filter_expr_str)
            .then(eval(filter_expr_str, {"pl": pl}))
            .otherwise(combined_expr)
        )

    df = df.lazy().filter(combined_expr).collect().drop(col_name)
    num_after = len(df)
    num_filtered = num_before - num_after
    logging.info(
        f" - {len(filter_strs)} filter(s) applied, "
        f"{num_filtered} dropped and {num_after} kept "
        f"from {num_before} rows",
    )

    return df


def _drop_excluded_rows(df: pl.DataFrame) -> pl.DataFrame:
    has_dropped_validations = (
        "downstream_validate_exploded" in df.lazy().collect_schema().names()
        and df.lazy()
        .select(
            (
                (pl.col("downstream_validate_exploded").str.len_bytes() > 0)
                & pl.col("downstream_exclude_unpacked")
            ).any()
        )
        .collect()
        .item()
    )
    if has_dropped_validations:
        warnings.warn(
            "row(s) with both `downstream_validate_exploded` "
            "and `downstream_exclude_unpacked` detected,"
            "but these rows will be dropped before validation",
        )

    kept = pl.col("downstream_exclude_unpacked").not_().fill_null(True)
    num_before = df.lazy().select(pl.len()).collect().item()
    df = df.filter(kept).drop("downstream_exclude_unpacked")
    num_after = len(df)
    num_dropped = num_before - num_after
    logging.info(
        f" - {num_dropped} dropped and {num_after} kept "
        f"from {num_before} rows!",
    )
    return df


def _finalize_result_schema(
    df: pl.DataFrame, result_schema: str
) -> pl.DataFrame:
    try:
        df = {
            "coerce": lambda df: df.cast(
                {
                    "dstream_data_id": pl.UInt64,
                    "dstream_S": pl.UInt32,
                    "dstream_T": pl.UInt64,
                    "dstream_storage_hex": pl.String,
                },
            ),
            "relax": lambda df: df,
            "shrink": lambda df: df.select(pl.all().shrink_dtype()),
        }[result_schema](df)
    except KeyError:
        raise ValueError(f"Invalid arg {result_schema} for result_schema")
    return df


def unpack_data_packed(
    df: pl.DataFrame,
    *,
    result_schema: typing.Literal["coerce", "relax", "shrink"] = "coerce",
) -> pl.DataFrame:
    """Unpack data with dstream buffer and counter serialized into a single
    hexadecimal data field.

    Parameters
    ----------
    df : pl.DataFrame
        The input DataFrame containing packed data with required columns, one
        row per dstream buffer.

        Required schema:

        - 'data_hex' : pl.String
            - Raw binary data, with serialized dstream buffer and counter.
            - Represented as a hexadecimal string.
        - 'dstream_algo' : pl.Categorical
            - Name of downstream curation algorithm used.
            - e.g., 'dstream.steady_algo'
        - 'dstream_storage_bitoffset' : pl.UInt64
            - Position of dstream buffer field in 'data_hex'.
        - 'dstream_storage_bitwidth' : pl.UInt64
            - Size of dstream buffer field in 'data_hex'.
        - 'dstream_T_bitoffset' : pl.UInt64
            - Position of dstream counter field in 'data_hex'.
        - 'dstream_T_bitwidth' : pl.UInt64
            - Size of dstream counter field in 'data_hex'.
        - 'dstream_S' : pl.UInt32
            - Capacity of dstream buffer, in number of data items.

        Optional schema:

        - 'downstream_data_parity0_rule' : pl.String or pl.Categorical
            - Boolean parity-check matrix (H) for validating the binary
              representation of 'data_hex', serialized as a string.
            - Rows of H correspond to independent parity constraints;
              columns correspond to bit positions in 'data_hex'.
            - The string uses space-separated 0/1 digits with rows
              delimited by newlines, parsed directly by ``np.loadtxt``
              into a uint8 matrix.
            - Example: for 4-bit data_hex, ``"1 1 1 1\n1 0 1 0"``
              defines a 2x4 H matrix ``[[1,1,1,1],[1,0,1,0]]``.
            - If present, 'downstream_data_parity0_result' will be
              computed as the syndrome H @ data (mod 2).
            - Parity is computed before packed filters and validations,
              so ``"pl.col('downstream_data_parity0_result') == 0"``
              can be used as a 'downstream_filter_packed' to drop rows
              failing the parity check, or as a
              'downstream_validate_packed' to assert all rows pass.
        - 'downstream_exclude_exploded' : pl.Boolean
            - Should row be dropped after exploding unpacked data?
        - 'downstream_exclude_unpacked' : pl.Boolean
            - Should row be dropped after unpacking packed data?
        - 'downstream_filter_exploded' : pl.String, polars expression
            - Polars expression to filter exploded data; non-matching rows
            are dropped. Applied after validation.
        - 'downstream_filter_packed' : pl.String, polars expression
            - Polars expression to filter packed data; non-matching rows
            are dropped. Applied after validation.
        - 'downstream_filter_unpacked' : pl.String, polars expression
            - Polars expression to filter unpacked data; non-matching rows
            are dropped. Applied after validation.
        - 'dstream_T_dilation' : pl.UInt32
            - Dilation factor applied to T counter, if any; supports scenario
            where data items are ingested every `dstream_T_dilation`th counter
            step (default 1).
        - 'downstream_validate_exploded' : pl.String, polars expression
            - Polars expression to validate exploded data.
        - 'downstream_validate_packed' : pl.String, polars expression
            - Polars expression to validate packed data.
        - 'downstream_validate_unpacked' : pl.String, polars expression
            - Polars expression to validate unpacked data.
        - 'downstream_version' : pl.Categorical
            - Version of downstream library used to curate data items.

    result_schema : Literal['coerce', 'relax', 'shrink'], default 'coerce'
        How should dtypes in the output DataFrame be handled?

        - 'coerce' : cast all columns to output schema.
        - 'relax' : keep all columns as-is.
        - 'shrink' : cast columns to smallest possible types.

    Returns
    -------
    pl.DataFrame
        Processed DataFrame with unpacked and decoded data fields, one row per
        dstream buffer

        Output schema:
            - 'dstream_algo' : pl.Categorical
                - Name of downstream curation algorithm used.
                - e.g., 'dstream.steady_algo'
            - 'dstream_data_id' : pl.UInt64
                - Row index identifier for dstream buffer.
            - 'dstream_S' : pl.UInt32
                - Capacity of dstream buffer, in number of data items.
            - 'dstream_T' : pl.UInt64
                - Logical time elapsed (number of elapsed data items in stream).
            - 'dstream_T_dilation' : pl.UInt32
                - Dilation factor applied to T counter; if none, then 1.
            - 'dstream_T_raw' : pl.UInt64
                - Raw packed time counter value, before un-dilation.
            - 'dstream_storage_hex' : pl.String
                - Raw dstream buffer binary data, containing packed data items.
                - Represented as a hexadecimal string.

        If 'downstream_data_parity0_rule' was provided:

            - 'downstream_data_parity0_result' : pl.UInt32
                - Number of parity rule rows violated.
                - Zero indicates data passes the parity check.

        User-defined columns and 'downstream_version' will be forwarded from
        the input DataFrame.

    Raises
    ------
    NotImplementedError
        If any of the bit offset or bit width columns are not hex-aligned
        (i.e., not multiples of 4 bits).
    ValueError
        If any of the required columns are missing from the input DataFrame.


    See Also
    --------
    downstream.dataframe.explode_lookup_unpacked :
        Explodes unpacked buffers into individual constituent data items.
    """
    logging.info("begin explode_lookup_unpacked")
    logging.info(" - prepping data...")

    _check_df(df)
    if df.lazy().limit(1).collect().is_empty():
        return _make_empty()

    logging.info(" - casting data_hex and dstream_algo...")
    df = df.cast({"data_hex": pl.String, "dstream_algo": pl.Categorical})

    logging.info(" - collecting schema names...")
    schema_names = df.lazy().collect_schema().names()

    if "dstream_T_dilation" in schema_names:
        logging.info(" - found dstream_T_dilation...")
    else:
        logging.info(" - defaulting dstream_T_dilation...")
        df = df.with_columns(dstream_T_dilation=pl.lit(1).cast(pl.UInt32))

    if "downstream_data_parity0_rule" in schema_names:
        logging.info(" - computing downstream_data_parity0_result...")
        df = _apply_data_parity0(df)
    else:
        logging.info(" - downstream_data_parity0_rule not found in df")

    if "downstream_validate_packed" in df:
        logging.info(" - evaluating `downstream_validate_packed` exprs...")
        df = _perform_validations(df, "downstream_validate_packed")

    if "downstream_filter_packed" in df:
        logging.info(" - applying `downstream_filter_packed` exprs...")
        df = _apply_filters(df, "downstream_filter_packed")

    logging.info(" - calculating offsets...")
    df = _calculate_offsets(df)

    if "dstream_data_id" not in df.lazy().collect_schema().names():
        df = df.with_row_index("dstream_data_id")

    logging.info(" - extracting T and storage_hex from data_hex...")
    df = _extract_from_data_hex(df)

    logging.info(" - un-dilating T...")
    df = df.with_columns(
        dstream_T_raw=pl.col("dstream_T"),
    ).with_columns(
        dstream_T=pl.col("dstream_T") // pl.col("dstream_T_dilation"),
    )

    if "downstream_validate_unpacked" in df:
        logging.info(" - evaluating `downstream_validate_unpacked` exprs...")
        df = _perform_validations(df, "downstream_validate_unpacked")

    if "downstream_filter_unpacked" in df:
        logging.info(" - applying `downstream_filter_unpacked` exprs...")
        df = _apply_filters(df, "downstream_filter_unpacked")

    if "downstream_exclude_unpacked" in df:
        logging.info(" - dropping excluded rows...")
        df = _drop_excluded_rows(df)

    logging.info(" - finalizing result schema...")
    df = _finalize_result_schema(df, result_schema)

    logging.info("unpack_data_packed complete")
    return df
