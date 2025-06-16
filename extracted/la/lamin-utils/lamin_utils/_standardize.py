from __future__ import annotations

from itertools import chain
from typing import TYPE_CHECKING, Any, Literal

from ._logger import logger
from ._map_synonyms import map_synonyms

if TYPE_CHECKING:
    from collections.abc import Iterable


def standardize(
    df: Any,
    identifiers: Iterable,
    field: str,
    *,
    return_field: str = None,
    case_sensitive: bool = False,
    return_mapper: bool = False,
    mute: bool = False,
    synonyms_field: str = "synonyms",
    sep: str = "|",
    keep: Literal["first", "last", False] = "first",
) -> dict[str, str] | list[str]:
    """Standardizes input identifiers against a concatenated synonyms column.

    Will also standardize casing.

    Args:
        df: Reference DataFrame.
        identifiers: Identifiers that will be mapped against a field.
        field: The field representing the identifiers.
        return_field: The field to return. Defaults to field.
        case_sensitive: Whether the mapping is case sensitive.
        return_mapper: If True, returns {input synonyms : standardized field name}.
        mute: If True, suppresses logging.
        synonyms_field: The field representing the concatenated synonyms.
        sep: Which separator is used to separate synonyms.
        keep: {'first', 'last', False}, default 'first'
            When a synonym maps to multiple standardized values, determines
            which duplicates to mark as `pandas.DataFrame.duplicated`.
            - "first": returns the first mapped standardized value
            - "last": returns the last mapped standardized value
            - False: returns all mapped standardized value

    Returns:
        - If return_mapper is False: a list of mapped field values.
        - If return_mapper is True: a dictionary of mapped values with mappable
            identifiers as keys and values mapped to field as values.
    """
    if df.shape[0] == 0 or len(identifiers) == 0:  # type: ignore
        if return_mapper:
            return {}
        else:
            return identifiers  # type: ignore

    # default return_field to field if not specified
    return_field = field if return_field is None else return_field

    # map synonyms
    result = map_synonyms(
        df=df,
        identifiers=identifiers,
        field=field,
        return_mapper=return_mapper,
        case_sensitive=case_sensitive,
        mute=mute,
        synonyms_field=synonyms_field,
        sep=sep,
        keep=keep,
    )

    if return_field == field:
        return result

    # convert identifiers to return_field
    # always get the full list of values (identifiers)
    if return_mapper:
        values = map_synonyms(
            df=df,
            identifiers=identifiers,
            field=field,
            return_mapper=False,
            case_sensitive=case_sensitive,
            mute=True,
            synonyms_field=synonyms_field,
            sep=sep,
            keep=keep,
            mute_warning=True,
        )
    else:
        values = result

    # no values can be converted
    if len(values) == 0:
        if not mute:
            logger.warning(
                f"no values can be converted from {field} to {return_field}!"
            )
        return values
    if keep is False:
        # flatten list of lists
        values = list(
            chain(*[item if isinstance(item, list) else [item] for item in values])
        )
    else:
        # deal with duplications here
        df = df.drop_duplicates(subset=[field], keep=keep)

    values_df = df[df[field].isin(values)]
    mapper = values_df[[field, return_field]].set_index(field)[return_field]
    if keep is False:
        mapper = (
            mapper.groupby(field)
            .agg(lambda x: list(x) if len(x) > 1 else x.iloc[0])
            .to_dict()
        )

    if return_mapper:
        # deals with the case where the mapper is a list
        return_dict: dict = {}
        for k, v in result.items():  # type: ignore
            if isinstance(v, list):
                return_dict[k] = []
                for x in v:
                    if mapper.get(x) is None:
                        continue
                    if isinstance(mapper.get(x), list):
                        return_dict[k].extend(mapper.get(x))
                    else:
                        return_dict[k].append(mapper.get(x))
            else:
                if mapper.get(v) is not None:
                    return_dict[k] = mapper.get(v)
        # add non-synonyms converted values
        return_dict.update(
            {
                k: v
                for k, v in mapper.items()
                if k
                not in set(
                    chain(*[v if isinstance(v, list) else [v] for v in result.values()])  # type: ignore
                )
            }
        )
        return return_dict
    else:
        return [mapper.get(v, v) for v in values]
