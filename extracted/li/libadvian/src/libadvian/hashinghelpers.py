"""Helpers to convert various mutable structures to immutable"""

from typing import Mapping, Sequence, Union, Dict, List, Any, Type
from json import JSONEncoder
import logging
import sys

FROZENDICT_DUMMY = False
try:
    from frozendict import frozendict
except ImportError:
    import warnings

    warnings.warn("Could not import frozendict, things will probably not work. install the 'http' extra feature")
    FROZENDICT_DUMMY = True

    class frozendict:  # type: ignore[no-redef] # pylint: disable=C0103,R0903
        """Dummy frozendict to avoid importerrors"""


ValidKeyTypes = Union[str, int, float]  # python actually supports just about any hashable type as key
if sys.version_info < (3, 9) or FROZENDICT_DUMMY:
    FDType = Type[frozendict]  # type: ignore[type-arg]
else:
    FDType = frozendict[ValidKeyTypes, "HandledSubTypes"]  # type: ignore[misc]
IMTypes = Union[str, bytes, int, float, bool, None, FDType]  # if you change this look at line 24 too
HandledSubTypes = Union[Mapping[ValidKeyTypes, IMTypes], Sequence[IMTypes], IMTypes]
HandledTypes = Union[Mapping[ValidKeyTypes, HandledSubTypes], Sequence[HandledSubTypes], IMTypes]
LOGGER = logging.getLogger(__name__)


class ImmobilizeError(ValueError):
    """Raised if we could not figure out what to do"""


class FrozendictEncoder(JSONEncoder):
    """Handle frozendict in JSON"""

    def default(self, o: Any) -> Any:
        if isinstance(o, frozendict):
            return dict(o)
        return super().default(o)


class ForgivingEncoder(FrozendictEncoder):
    """Set un-encodable values to None"""

    def default(self, o: Any) -> Any:
        try:
            return super().default(o)
        except TypeError as exc:
            LOGGER.warning("Encoding error {}, encoding as None".format(exc))
            return None


def immobilize(data_in: HandledTypes, none_on_fallthru: bool = False) -> Union[HandledTypes, FDType]:
    """Recurse over the input making types immutable

    if none_on_fallthru is true then this returns None for a type it does not know how to handle, otherwise
    raises ImmobilizeError"""
    if data_in is None:
        return None
    if isinstance(data_in, (str, bytes, int, float, bool, frozendict)):
        return data_in
    if isinstance(data_in, Mapping):
        new_dict: Dict[ValidKeyTypes, Union[HandledTypes, FDType]] = {}
        for key in data_in.keys():
            new_dict[key] = immobilize(data_in[key])
        return frozendict(new_dict)  # type: ignore[arg-type]  # IDK what the issue here is
    if isinstance(data_in, Sequence):
        new_list: List[Union[HandledTypes, FDType]] = []
        for value in data_in:
            new_list.append(immobilize(value))
        return tuple(new_list)  # type: ignore[arg-type]  # IDK what the issue here is
    # fail-safe for hashable types we did not enumerate
    try:
        hash(data_in)
        return data_in
    except TypeError:
        pass
    # Fall through
    if none_on_fallthru:
        return None
    raise ImmobilizeError(f"Could not figure out what to do with {repr(data_in)}")
