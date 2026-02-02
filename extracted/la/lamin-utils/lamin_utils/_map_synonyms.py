from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from ._logger import logger

if TYPE_CHECKING:
    from collections.abc import Iterable

    import pandas as pd


def map_synonyms(
    df: pd.DataFrame,
    identifiers: Iterable,
    field: str,
    *,
    case_sensitive: bool = False,
    return_mapper: bool = False,
    mute: bool = False,
    synonyms_field: str = "synonyms",
    sep: str = "|",
    keep: Literal["first", "last", False] = "first",
    mute_warning: bool = False,
) -> dict[str, str] | list[str]:
    """Maps input identifiers against a field with synonym fallback.

    Implements a three-tier matching priority:
    1. Exact case-sensitive field match (preserves original casing)
    2. Case-insensitive field match (when case_sensitive=False)
    3. Synonym match (with optional case-insensitive matching)

    Args:
        df: Reference DataFrame.
        identifiers: Identifiers that will be mapped against a field.
        field: The field representing the identifiers.
        case_sensitive: Whether the mapping is case sensitive.
        return_mapper: If True, returns {input : standardized field name}.
        mute: If True, suppresses logging of mapping statistics.
        synonyms_field: The field representing the concatenated synonyms.
        sep: Separator used to split synonyms.
        keep: {'first', 'last', False}, default 'first'
            When a synonym maps to multiple standardized values, determines
            which duplicates to mark as `pandas.DataFrame.duplicated`.
            - "first": returns the first mapped standardized value
            - "last": returns the last mapped standardized value
            - False: returns all mapped standardized values
        mute_warning: If True, suppresses warnings about list values when keep=False.

    Returns:
        - If return_mapper is False: a list of mapped field values in input order.
        - If return_mapper is True: a dictionary mapping input identifiers to
          standardized field values (only includes entries that were mapped).
    """
    import pandas as pd

    identifiers = list(identifiers)
    n_input = len(identifiers)

    # Handle empty inputs
    if (
        df.shape[0] == 0
        or n_input == 0
        or synonyms_field is None
        or synonyms_field == "None"
    ):
        return {} if return_mapper else identifiers

    # Validate inputs
    if field not in df.columns:
        raise KeyError(
            f"field '{field}' is invalid! Available fields are: {list(df.columns)}"
        )
    if synonyms_field not in df.columns:
        raise KeyError(
            f"synonyms_field '{synonyms_field}' is invalid! Available fields are: {list(df.columns)}"
        )
    if field == synonyms_field:
        raise KeyError("synonyms_field must be different from field!")

    # Initialize mapping dataframe
    mapped_df = pd.DataFrame({"orig_ids": identifiers})
    mapped_df["__lookup__"] = to_str(
        mapped_df["orig_ids"], case_sensitive=case_sensitive
    )
    mapped_df["mapped"] = pd.NA

    # Step 1: Try exact case-sensitive match (highest priority)
    # This preserves original casing even when case_sensitive=False
    exact_field_values = set(df[field].dropna().drop_duplicates())
    exact_matches = mapped_df["orig_ids"].isin(exact_field_values)
    mapped_df.loc[exact_matches, "mapped"] = mapped_df.loc[exact_matches, "orig_ids"]

    # Step 2: For case-insensitive mode, try case-insensitive field matching
    if not case_sensitive:
        unmapped_mask = mapped_df["mapped"].isna()
        if unmapped_mask.any():
            # Build case-insensitive field map (keeps first occurrence)
            df_field = df[[field]].dropna(subset=[field])
            df_field["__lookup__"] = to_str(df_field[field], case_sensitive=False)
            df_field = df_field.drop_duplicates(subset=["__lookup__"], keep="first")
            field_map_lower = df_field.set_index("__lookup__")[field].to_dict()

            # Apply case-insensitive field map to unmapped entries
            mapped_df.loc[unmapped_mask, "mapped"] = mapped_df.loc[
                unmapped_mask, "__lookup__"
            ].map(field_map_lower)

    # Step 3: For still-unmapped terms, check synonyms
    unmapped_mask = mapped_df["mapped"].isna()
    if unmapped_mask.any():
        unmapped_terms = set(mapped_df.loc[unmapped_mask, "__lookup__"])

        syn_map = _build_synonym_map(
            df=df,
            synonyms_field=synonyms_field,
            field=field,
            unmapped_terms=unmapped_terms,
            case_sensitive=case_sensitive,
            keep=keep,
            sep=sep,
        )

        if syn_map:
            mapped_df.loc[unmapped_mask, "mapped"] = mapped_df.loc[
                unmapped_mask, "__lookup__"
            ].map(syn_map)

    # Log mapping statistics (only count actual changes, not exact matches)
    changed_mask = (~mapped_df["mapped"].isna()) & (
        mapped_df["mapped"] != mapped_df["orig_ids"]
    )
    n_mapped = changed_mask.sum()
    if n_mapped > 0 and not mute:
        s = "" if n_mapped == 1 else "s"
        logger.info(f"standardized {n_mapped}/{n_input} term{s}")

    # Return results
    if return_mapper:
        return _build_mapper(mapped_df, keep, mute_warning)
    else:
        return _build_result_list(mapped_df, keep, mute_warning)


def _build_synonym_map(
    df: pd.DataFrame,
    synonyms_field: str,
    field: str,
    unmapped_terms: set,
    case_sensitive: bool,
    keep: Literal["first", "last", False],
    sep: str,
) -> dict:
    """Build a synonym mapping dictionary for unmapped terms."""
    syn_series = explode_aggregated_column_to_map(
        df=df,
        agg_col=synonyms_field,
        target_col=field,
        keep=keep,
        sep=sep,
    )

    if not case_sensitive:
        # Convert synonym keys to lowercase for matching
        syn_series.index = syn_series.index.str.lower()
        # Remove duplicate synonym keys (keep first occurrence)
        syn_series = syn_series[~syn_series.index.duplicated(keep="first")]

    # Only keep synonym mappings for unmapped terms
    return {k: v for k, v in syn_series.to_dict().items() if k in unmapped_terms}


def _build_mapper(
    mapped_df: pd.DataFrame,
    keep: Literal["first", "last", False],
    mute_warning: bool,
) -> dict:
    """Build the mapper dictionary from mapped dataframe."""
    mapper_df = mapped_df[~mapped_df["mapped"].isna()].copy()
    mapper = dict(zip(mapper_df["orig_ids"], mapper_df["mapped"]))
    # Only include entries where mapping changed the value
    mapper = {k: v for k, v in mapper.items() if k != v}

    if keep is False:
        if not mute_warning:
            logger.warning(
                "returning mapper might contain lists as values when 'keep=False'"
            )
        return {
            k: v[0] if isinstance(v, list) and len(v) == 1 else v
            for k, v in mapper.items()
        }
    return mapper


def _build_result_list(
    mapped_df: pd.DataFrame,
    keep: Literal["first", "last", False],
    mute_warning: bool,
) -> list:
    """Build the result list from mapped dataframe."""
    result = mapped_df["mapped"].fillna(mapped_df["orig_ids"]).tolist()

    if keep is False:
        if not mute_warning:
            logger.warning("returning list might contain lists when 'keep=False'")
        return [v[0] if isinstance(v, list) and len(v) == 1 else v for v in result]
    return result


def to_str(
    series_values: pd.Series | pd.Index | pd.Categorical,
    case_sensitive: bool = False,
) -> pd.Series:
    """Convert Pandas Series values to strings with case sensitive option."""
    if series_values.dtype.name == "category":
        try:
            categorical = series_values.cat
        except AttributeError:
            categorical = series_values
        if "" not in categorical.categories:
            values = categorical.add_categories("")
        else:
            values = series_values
        values = values.infer_objects(copy=False).fillna("").astype(str)
    else:
        values = series_values.infer_objects(copy=False).fillna("")
    if case_sensitive is False:
        values = values.str.lower()
    return values


def not_empty_none_na(values: Iterable) -> pd.Series:
    """Return values that are not empty string, None or NA."""
    import pandas as pd

    series = (
        pd.Series(values) if not isinstance(values, (pd.Series, pd.Index)) else values
    )

    return series[pd.Series(series).infer_objects(copy=False).fillna("").astype(bool)]


def explode_aggregated_column_to_map(
    df,
    agg_col: str,
    target_col: str,
    keep: Literal["first", "last", False] = "first",
    sep: str = "|",
) -> pd.Series:
    """Explode values from an aggregated DataFrame column to map to a target column.

    Args:
        df: A DataFrame containing the agg_col and target_col.
        agg_col: The name of the aggregated column
        target_col: the name of the target column
        keep : {'first', 'last', False}, default 'first'
            Determines which duplicates to mark as `pandas.DataFrame.duplicated`
        sep: Splits all values of the agg_col by this separator.

    Returns:
        A pandas.Series indexed by the split values from the aggregated column
    """
    df = df[[target_col, agg_col]].drop_duplicates().dropna(subset=[agg_col])

    # subset to df with only non-empty strings in the agg_col
    df = df.loc[not_empty_none_na(df[agg_col]).index]

    df[agg_col] = df[agg_col].str.split(sep)
    df_explode = df.explode(agg_col)
    # remove rows with same values in agg_col and target_col
    df_explode = df_explode[df_explode[agg_col] != df_explode[target_col]]

    # group by the agg_col and return based on keep for the target_col values
    gb = df_explode.groupby(agg_col)[target_col]
    if keep == "first":
        return gb.first()
    elif keep == "last":
        return gb.last()
    elif keep is False:
        return gb.apply(list)
    else:
        raise ValueError(f"Invalid value for keep: {keep}")
