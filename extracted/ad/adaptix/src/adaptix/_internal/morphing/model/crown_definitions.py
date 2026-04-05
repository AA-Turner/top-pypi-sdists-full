from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from ...common import VarTuple
from ...model_tools.definitions import BaseShape, DefaultFactory, DefaultValue, InputShape, OutputShape
from ...provider.located_request import LocatedRequest
from ...utils import MappingHashWrapper, SingletonMeta

T = TypeVar("T")

CrownPathElem = str | int
CrownPath = VarTuple[CrownPathElem]  # subset of struct_path.Trail


# Policies how to process extra data

class ExtraSkip(metaclass=SingletonMeta):
    """Ignore any extra data"""


class ExtraForbid(metaclass=SingletonMeta):
    """Raise error if extra data would be met"""


class ExtraCollect(metaclass=SingletonMeta):
    """Collect extra data and pass it to object"""


# --------  Base classes for crown -------- #

# Crown defines mapping of fields to structure of lists and dicts
# as well as the policy of extra data processing.
# This structure is named in honor of the crown of the tree.
#
# NoneCrown-s represents an element that does not map to any field


@dataclass(frozen=True)
class BaseDictCrown(Generic[T]):
    map: Mapping[str, T]


@dataclass(frozen=True)
class BaseListCrown(Generic[T]):
    map: Sequence[T]


@dataclass(frozen=True)
class BaseNoneCrown:
    pass


@dataclass(frozen=True)
class BaseFieldCrown:
    id: str


BranchBaseCrown = BaseDictCrown | BaseListCrown
LeafBaseCrown = BaseFieldCrown | BaseNoneCrown
BaseCrown = BranchBaseCrown | LeafBaseCrown

# --------  Input Crown -------- #

DictExtraPolicy = ExtraSkip | ExtraForbid | ExtraCollect
ListExtraPolicy = ExtraSkip | ExtraForbid


@dataclass(frozen=True)
class InpDictCrown(BaseDictCrown["InpCrown"]):
    extra_policy: DictExtraPolicy

    def __hash__(self):
        return hash(MappingHashWrapper(self.map))


@dataclass(frozen=True)
class InpListCrown(BaseListCrown["InpCrown"]):
    extra_policy: ListExtraPolicy


@dataclass(frozen=True)
class InpNoneCrown(BaseNoneCrown):
    pass


@dataclass(frozen=True)
class InpFieldCrown(BaseFieldCrown):
    pass


BranchInpCrown = InpDictCrown | InpListCrown
LeafInpCrown = InpFieldCrown | InpNoneCrown
InpCrown = BranchInpCrown | LeafInpCrown

# --------  Output Crown -------- #

# Sieve takes source object and raw field value to determine if skip field.
# True indicates to put field, False to skip.
Sieve = Callable[[Any, Any], bool]


@dataclass(frozen=True)
class OutDictCrown(BaseDictCrown["OutCrown"]):
    sieves: dict[str, Sieve]

    def _validate(self):
        wild_sieves = self.sieves.keys() - self.map.keys()
        if wild_sieves:
            raise ValueError(
                f"Sieves {wild_sieves} are attached to non-existing keys",
            )

    def __post_init__(self):
        self._validate()

    def __hash__(self):
        return hash((MappingHashWrapper(self.map), MappingHashWrapper(self.sieves)))


@dataclass(frozen=True)
class OutListCrown(BaseListCrown["OutCrown"]):
    pass


Placeholder = DefaultValue | DefaultFactory


@dataclass(frozen=True)
class OutNoneCrown(BaseNoneCrown):
    placeholder: Placeholder


@dataclass(frozen=True)
class OutFieldCrown(BaseFieldCrown):
    pass


BranchOutCrown = OutDictCrown | OutListCrown
LeafOutCrown = OutFieldCrown | OutNoneCrown
OutCrown = BranchOutCrown | LeafOutCrown

# --------  Name Layout -------- #


class ExtraKwargs(metaclass=SingletonMeta):
    pass


@dataclass(frozen=True)
class ExtraTargets:
    fields: VarTuple[str]


Saturator = Callable[[T, Mapping[str, Any]], None]
Extractor = Callable[[T], Mapping[str, Any]]


@dataclass(frozen=True)
class ExtraSaturate(Generic[T]):
    func: Saturator[T]


@dataclass(frozen=True)
class ExtraExtract(Generic[T]):
    func: Extractor[T]


InpExtraMove = None | ExtraTargets | ExtraKwargs | ExtraSaturate[T]
OutExtraMove = None | ExtraTargets | ExtraExtract[T]
BaseExtraMove = InpExtraMove | OutExtraMove


@dataclass(frozen=True)
class BaseNameLayout:
    crown: BranchBaseCrown
    extra_move: BaseExtraMove


@dataclass(frozen=True)
class BaseNameLayoutRequest(LocatedRequest[T], Generic[T]):
    shape: BaseShape


@dataclass(frozen=True)
class InputNameLayout(BaseNameLayout):
    crown: BranchInpCrown
    extra_move: InpExtraMove


@dataclass(frozen=True)
class InputNameLayoutRequest(BaseNameLayoutRequest[InputNameLayout]):
    shape: InputShape


@dataclass(frozen=True)
class OutputNameLayout(BaseNameLayout):
    crown: BranchOutCrown
    extra_move: OutExtraMove


@dataclass(frozen=True)
class OutputNameLayoutRequest(BaseNameLayoutRequest[OutputNameLayout]):
    shape: OutputShape
