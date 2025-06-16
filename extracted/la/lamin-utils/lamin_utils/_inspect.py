from __future__ import annotations

from typing import TYPE_CHECKING

from ._colors import colors
from ._logger import logger
from ._map_synonyms import map_synonyms, to_str

if TYPE_CHECKING:
    from collections.abc import Iterable

    import numpy as np
    import pandas as pd


class InspectResult:
    """Result of inspect.

    An InspectResult object of calls such as :meth:`~lamindb.models.CanCurate.inspect`.
    """

    def __init__(
        self,
        validated_df: pd.DataFrame,
        validated: list[str],
        nonvalidated: list[str],
        frac_validated: float,
        n_empty: int,
        n_unique: int,
    ) -> None:
        self._df = validated_df
        self._validated = validated
        self._non_validated = nonvalidated
        self._frac_validated = frac_validated
        self._n_empty = n_empty
        self._n_unique = n_unique
        self._synonyms_mapper: dict = {}

    @property
    def df(self) -> pd.DataFrame:
        """A DataFrame indexed by values with a boolean `__validated__` column."""
        return self._df

    @property
    def validated(self) -> list[str]:
        """List of successfully :meth:`~lamindb.models.CanCurate.validate` validated items."""
        return self._validated

    @property
    def non_validated(self) -> list[str]:
        """List of unsuccessfully :meth:`~lamindb.models.CanCurate.validate` items.

        This list can be used to remove any non-validated values such as
        genes that do not map against the specified source.
        """
        return self._non_validated

    @property
    def frac_validated(self) -> float:
        """Fraction of items that were validated."""
        return self._frac_validated

    @property
    def n_empty(self) -> int:
        """Number of empty items."""
        return self._n_empty

    @property
    def n_unique(self) -> int:
        """Number of unique items."""
        return self._n_unique

    @property
    def synonyms_mapper(self) -> dict:
        """Synonyms mapper dictionary.

        Such a dictionary maps the actual values to their synonyms
        which can be used to rename values accordingly.

        Examples:
            >>> markers = pd.DataFrame(index=["KI67","CCR7"])
            >>> synonyms_mapper = bt.CellMarker.standardize(markers.index, return_mapper=True)

            {'KI67': 'Ki67', 'CCR7': 'Ccr7'}
        """
        return self._synonyms_mapper

    def __getitem__(self, key) -> list[str]:
        """Bracket access to the inspect result."""
        if key == "validated":
            return self.validated
        elif key == "non_validated":
            return self.non_validated
        # backward compatibility below
        elif key == "mapped":
            return self.validated
        elif key == "not_mapped":
            return self.non_validated
        else:
            raise KeyError("invalid key")


def validate(
    identifiers: Iterable,
    field_values: Iterable,
    *,
    case_sensitive: bool = True,
    mute: bool = False,
    field: str | None = None,
    **kwargs,
) -> np.ndarray:
    """Check if elements in an iterable are present in a list of values.

    This function validates whether each element in `identifiers` is present in `field_values`.
    It returns a boolean numpy array indicating which elements are valid (True) or invalid (False).

    Args:
        identifiers: The iterable containing elements to be validated.
        field_values: The iterable containing valid values to check against.
        case_sensitive: If True, the comparison is case-sensitive.
        mute: If True, suppresses logging output
        field: Name of the field being validated, used in logging.
        **kwargs: Additional keyword arguments.
            logging: If provided as a boolean, overrides the 'mute' parameter.

    Returns:
        A boolean numpy array where True indicates a valid element and False an invalid one.

    Notes:
        - The function converts both `identifiers` and `field_values` to strings before comparison.
    """
    if isinstance(kwargs.get("logging"), bool):
        mute = not kwargs.get("logging")
    import pandas as pd

    _check_type_compatibility(identifiers, field_values)

    identifiers = list(identifiers)
    identifiers_idx = pd.Index(identifiers)
    identifiers_idx = to_str(identifiers_idx, case_sensitive=case_sensitive)

    field_values = to_str(field_values, case_sensitive=case_sensitive)

    # annotated what complies with the default ID
    matches = identifiers_idx.isin(field_values)
    if not mute:
        if len(identifiers) == 0:
            logger.warning("input has zero length")
        else:
            _validate_logging(
                _validate_stats(identifiers=identifiers, matches=matches), field=field
            )
    return matches


def _check_type_compatibility(identifiers: Iterable, field_values: Iterable) -> None:
    """Checks whether the identifiers and field_values have the same high level (numeric vs str/categorical) data type.

    Raises:
        TypeError: If the high level data types do not match.
    """
    import math

    import numpy as np
    import pandas as pd

    # Only look at the first element because we assume that the dtype is consistent for efficiency
    id_sample, value_sample = (
        next(iter(identifiers), None),
        next(iter(field_values), None),
    )

    def _is_nan(value) -> bool:
        if isinstance(value, (float, np.floating)):
            return math.isnan(value) or np.isnan(value)
        return False

    def _get_type_category(value):
        if isinstance(value, (int, float, complex, np.number)):
            return "numeric"
        elif isinstance(value, (str, np.str_, pd.Categorical)):
            return "str/categorical"
        return "unknown"

    # Real world data may have Nones and nan values. We can pass over them.
    if (
        id_sample is not None
        and value_sample is not None
        and not _is_nan(id_sample)
        and not _is_nan(value_sample)
    ):
        id_type, value_type = (
            _get_type_category(id_sample),
            _get_type_category(value_sample),
        )

        if id_type != value_type:
            raise TypeError(
                f"Type mismatch: identifiers are '{id_type}' but field_values are '{value_type}'."
            )


def _unique_rm_empty(idx: pd.Index):
    idx = idx.unique()
    return idx[(idx != "") & (~idx.isnull())]


def _validate_stats(identifiers: Iterable, matches: np.ndarray):
    import pandas as pd

    df_val = pd.DataFrame(data={"__validated__": matches}, index=identifiers)
    val = _unique_rm_empty(df_val.index[df_val["__validated__"]]).tolist()
    nonval = _unique_rm_empty(df_val.index[~df_val["__validated__"]]).tolist()

    n_unique = len(val) + len(nonval)
    if n_unique == 0:
        return InspectResult(
            validated_df=df_val,
            validated=val,
            nonvalidated=nonval,
            frac_validated=0,
            n_empty=0,
            n_unique=0,
        )
    n_empty = df_val.shape[0] - n_unique
    frac_nonval = round(len(nonval) / n_unique * 100, 1)
    frac_val = 100 - frac_nonval

    return InspectResult(
        validated_df=df_val,
        validated=val,
        nonvalidated=nonval,
        frac_validated=frac_val,
        n_empty=n_empty,
        n_unique=n_unique,
    )


def _validate_logging(result: InspectResult, field: str | None = None) -> None:
    """Logging of the validated result to stdout."""
    field_msg = ""
    if field is not None:
        field_msg = f" for {colors.italic(field)}"
    empty_warn_msg = ""
    if result.n_empty > 0:
        unique_s = "" if result.n_unique == 1 else "s"
        empty_s = " is" if result.n_empty == 1 else "s are"
        empty_warn_msg = (
            f"received {result.n_unique} unique term{unique_s},"
            f" {result.n_empty} empty/duplicated term{empty_s} ignored"
        )
    s = "" if len(result.validated) == 1 else "s"
    are = "is" if len(result.validated) == 1 else "are"
    success_msg = ""
    if len(result.validated) > 0:
        success_msg = (
            f"{colors.green(f'{len(result.validated)} unique term{s}')} ({result.frac_validated:.2f}%)"
            f" {are} validated{field_msg}"
        )
    if result.frac_validated < 100:
        s = "" if len(result.non_validated) == 1 else "s"
        are = "is" if len(result.non_validated) == 1 else "are"
        print_values = ", ".join([f"'{i}'" for i in result.non_validated[:10]])
        if len(result.non_validated) > 10:
            print_values += ", ..."
        warn_msg = (
            f"{colors.yellow(f'{len(result.non_validated)} unique term{s}')} ({(100 - result.frac_validated):.2f}%)"
            f" {are} not validated{field_msg}: {colors.yellow(print_values)}"
        )
        if len(empty_warn_msg) > 0:
            logger.warning(empty_warn_msg)
        if len(success_msg) > 0:
            logger.success(success_msg)
        logger.warning(warn_msg)
    else:
        logger.success(success_msg)


def inspect(
    df: pd.DataFrame,
    identifiers: Iterable,
    field: str,
    *,
    mute: bool = False,
    **kwargs,
) -> InspectResult:
    """Inspect if a list of identifiers are mappable to the entity reference.

    Args:
        df: DataFrame containing the field.
        identifiers: Identifiers that will be checked against the field.
        field: The BiontyField of the ontology to compare against.
                Examples are 'ontology_id' to map against the source ID
                or 'name' to map against the ontologies field names.
        return_df: Whether to return a Pandas DataFrame.

    Returns:
        InspectResult object.
    """
    # backward compat
    if isinstance(kwargs.get("logging"), bool):
        mute = not kwargs.get("logging")
    import pandas as pd

    identifiers = list(identifiers)
    uniq_identifiers = _unique_rm_empty(pd.Index(identifiers)).tolist()
    # empty DataFrame or input
    if df.shape[0] == 0 or len(uniq_identifiers) == 0:
        result = _validate_stats(
            identifiers=identifiers,
            matches=[False] * len(identifiers),  # type:ignore
        )
        if not mute:
            _validate_logging(result=result, field=field)
        if kwargs.get("return_df") is True:
            return result.df
        else:
            return result

    # check if index is compliant with exact matches
    matches = validate(
        identifiers=identifiers, field_values=df[field], case_sensitive=True, mute=True
    )
    # matches if case sensitive is turned off
    noncs_matches = validate(
        identifiers=identifiers, field_values=df[field], case_sensitive=False, mute=True
    )

    msg_casing = "inconsistent casing/" if noncs_matches.sum() > matches.sum() else ""

    result = _validate_stats(identifiers=identifiers, matches=matches)

    # backward compat
    info_msg = ""
    if kwargs.get("inspect_synonyms") is not False:
        try:
            synonyms_mapper = map_synonyms(
                df=df,
                identifiers=result.non_validated,
                field=field,
                return_mapper=True,
                case_sensitive=False,
                mute=True,
            )
            if len(synonyms_mapper) > 0:
                print_values = ", ".join(
                    list(synonyms_mapper.keys())[:10]  # type:ignore
                )
                if len(synonyms_mapper) > 10:
                    print_values += ", ..."
                s = "" if len(synonyms_mapper) == 1 else "s"
                labels = colors.yellow(
                    f"{len(synonyms_mapper)} unique terms with {msg_casing}synonym{s}"
                )
                info_msg = f"detected {labels}: {colors.yellow(print_values)}"
                result._synonyms_mapper = synonyms_mapper

        except Exception:  # noqa: S110
            pass
    if not mute:
        _validate_logging(result=result, field=field)
        if len(info_msg) > 0:
            logger.print(f"   {info_msg}")
            logger.print(f"→  standardize terms via {colors.italic('.standardize()')}")

    # backward compat
    if kwargs.get("return_df") is True:
        return result.df

    return result
