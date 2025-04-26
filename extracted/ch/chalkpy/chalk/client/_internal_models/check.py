import dataclasses
from typing import TYPE_CHECKING, Any, Mapping, Union

from rich.text import Text

from chalk.client import ErrorCode
from chalk.client.models import ChalkError
from chalk.features.feature_field import Feature, FeatureWrapper
from chalk.utils.json import TJSON

if TYPE_CHECKING:
    import polars as pl


@dataclasses.dataclass
class ManyQueryInputsCheckerWrapper:
    inputs: Mapping[Union[str, FeatureWrapper, Feature, Any], list[Any]]


@dataclasses.dataclass(frozen=True)
class Result:
    fqn: str
    value: Union[TJSON, "pl.DataFrame"]
    cache_hit: bool
    error: Union[ChalkError, ErrorCode, None]
    pkey: TJSON = None


class Color:
    R = "\033[031m"  # RED
    G = "\033[032m"  # GREEN
    Y = "\033[033m"  # Yellow
    B = "\033[034m"  # Blue
    N = "\033[0m"  # Reset

    @staticmethod
    def render(s: str, color: str):
        return Text.from_ansi(f"{color}{s}{Color.N}")
