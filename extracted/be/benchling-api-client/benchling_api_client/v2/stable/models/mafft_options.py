from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.mafft_options_adjust_direction import MafftOptionsAdjustDirection
from ..models.mafft_options_strategy import MafftOptionsStrategy
from ..types import UNSET, Unset

T = TypeVar("T", bound="MafftOptions")


@attr.s(auto_attribs=True, repr=False)
class MafftOptions:
    """ Options to pass to the MAFFT algorithm, only applicable for MAFFT. """

    _adjust_direction: Union[Unset, MafftOptionsAdjustDirection] = MafftOptionsAdjustDirection.FAST
    _gap_extension_penalty: Union[Unset, float] = 0.0
    _gap_open_penalty: Union[Unset, float] = 1.53
    _max_iterations: Union[Unset, int] = 0
    _retree: Union[Unset, int] = 2
    _strategy: Union[Unset, MafftOptionsStrategy] = MafftOptionsStrategy.AUTO
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("adjust_direction={}".format(repr(self._adjust_direction)))
        fields.append("gap_extension_penalty={}".format(repr(self._gap_extension_penalty)))
        fields.append("gap_open_penalty={}".format(repr(self._gap_open_penalty)))
        fields.append("max_iterations={}".format(repr(self._max_iterations)))
        fields.append("retree={}".format(repr(self._retree)))
        fields.append("strategy={}".format(repr(self._strategy)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "MafftOptions({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        adjust_direction: Union[Unset, int] = UNSET
        if not isinstance(self._adjust_direction, Unset):
            adjust_direction = self._adjust_direction.value

        gap_extension_penalty = self._gap_extension_penalty
        gap_open_penalty = self._gap_open_penalty
        max_iterations = self._max_iterations
        retree = self._retree
        strategy: Union[Unset, int] = UNSET
        if not isinstance(self._strategy, Unset):
            strategy = self._strategy.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if adjust_direction is not UNSET:
            field_dict["adjustDirection"] = adjust_direction
        if gap_extension_penalty is not UNSET:
            field_dict["gapExtensionPenalty"] = gap_extension_penalty
        if gap_open_penalty is not UNSET:
            field_dict["gapOpenPenalty"] = gap_open_penalty
        if max_iterations is not UNSET:
            field_dict["maxIterations"] = max_iterations
        if retree is not UNSET:
            field_dict["retree"] = retree
        if strategy is not UNSET:
            field_dict["strategy"] = strategy

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_adjust_direction() -> Union[Unset, MafftOptionsAdjustDirection]:
            adjust_direction = UNSET
            _adjust_direction = d.pop("adjustDirection")
            if _adjust_direction is not None and _adjust_direction is not UNSET:
                try:
                    adjust_direction = MafftOptionsAdjustDirection(_adjust_direction)
                except ValueError:
                    adjust_direction = MafftOptionsAdjustDirection.of_unknown(_adjust_direction)

            return adjust_direction

        try:
            adjust_direction = get_adjust_direction()
        except KeyError:
            if strict:
                raise
            adjust_direction = cast(Union[Unset, MafftOptionsAdjustDirection], UNSET)

        def get_gap_extension_penalty() -> Union[Unset, float]:
            gap_extension_penalty = d.pop("gapExtensionPenalty")
            return gap_extension_penalty

        try:
            gap_extension_penalty = get_gap_extension_penalty()
        except KeyError:
            if strict:
                raise
            gap_extension_penalty = cast(Union[Unset, float], UNSET)

        def get_gap_open_penalty() -> Union[Unset, float]:
            gap_open_penalty = d.pop("gapOpenPenalty")
            return gap_open_penalty

        try:
            gap_open_penalty = get_gap_open_penalty()
        except KeyError:
            if strict:
                raise
            gap_open_penalty = cast(Union[Unset, float], UNSET)

        def get_max_iterations() -> Union[Unset, int]:
            max_iterations = d.pop("maxIterations")
            return max_iterations

        try:
            max_iterations = get_max_iterations()
        except KeyError:
            if strict:
                raise
            max_iterations = cast(Union[Unset, int], UNSET)

        def get_retree() -> Union[Unset, int]:
            retree = d.pop("retree")
            return retree

        try:
            retree = get_retree()
        except KeyError:
            if strict:
                raise
            retree = cast(Union[Unset, int], UNSET)

        def get_strategy() -> Union[Unset, MafftOptionsStrategy]:
            strategy = UNSET
            _strategy = d.pop("strategy")
            if _strategy is not None and _strategy is not UNSET:
                try:
                    strategy = MafftOptionsStrategy(_strategy)
                except ValueError:
                    strategy = MafftOptionsStrategy.of_unknown(_strategy)

            return strategy

        try:
            strategy = get_strategy()
        except KeyError:
            if strict:
                raise
            strategy = cast(Union[Unset, MafftOptionsStrategy], UNSET)

        mafft_options = cls(
            adjust_direction=adjust_direction,
            gap_extension_penalty=gap_extension_penalty,
            gap_open_penalty=gap_open_penalty,
            max_iterations=max_iterations,
            retree=retree,
            strategy=strategy,
        )

        mafft_options.additional_properties = d
        return mafft_options

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

    def get(self, key, default=None) -> Optional[Any]:
        return self.additional_properties.get(key, default)

    @property
    def adjust_direction(self) -> MafftOptionsAdjustDirection:
        """Adjust direction:
        * `fast`: Enabled, quickly.
        * `accurate`: Enabled, accurately (slow).
        * `disabled`: Disabled, fastest.
        """
        if isinstance(self._adjust_direction, Unset):
            raise NotPresentError(self, "adjust_direction")
        return self._adjust_direction

    @adjust_direction.setter
    def adjust_direction(self, value: MafftOptionsAdjustDirection) -> None:
        self._adjust_direction = value

    @adjust_direction.deleter
    def adjust_direction(self) -> None:
        self._adjust_direction = UNSET

    @property
    def gap_extension_penalty(self) -> float:
        """ Gap extension penalty. """
        if isinstance(self._gap_extension_penalty, Unset):
            raise NotPresentError(self, "gap_extension_penalty")
        return self._gap_extension_penalty

    @gap_extension_penalty.setter
    def gap_extension_penalty(self, value: float) -> None:
        self._gap_extension_penalty = value

    @gap_extension_penalty.deleter
    def gap_extension_penalty(self) -> None:
        self._gap_extension_penalty = UNSET

    @property
    def gap_open_penalty(self) -> float:
        """ Gap open penalty. """
        if isinstance(self._gap_open_penalty, Unset):
            raise NotPresentError(self, "gap_open_penalty")
        return self._gap_open_penalty

    @gap_open_penalty.setter
    def gap_open_penalty(self, value: float) -> None:
        self._gap_open_penalty = value

    @gap_open_penalty.deleter
    def gap_open_penalty(self) -> None:
        self._gap_open_penalty = UNSET

    @property
    def max_iterations(self) -> int:
        """ Max refinement iterations. Not applicable for auto strategy, as it will be selected automatically. """
        if isinstance(self._max_iterations, Unset):
            raise NotPresentError(self, "max_iterations")
        return self._max_iterations

    @max_iterations.setter
    def max_iterations(self, value: int) -> None:
        self._max_iterations = value

    @max_iterations.deleter
    def max_iterations(self) -> None:
        self._max_iterations = UNSET

    @property
    def retree(self) -> int:
        """ Tree rebuilding. Only used for 6-mer strategy. """
        if isinstance(self._retree, Unset):
            raise NotPresentError(self, "retree")
        return self._retree

    @retree.setter
    def retree(self, value: int) -> None:
        self._retree = value

    @retree.deleter
    def retree(self) -> None:
        self._retree = UNSET

    @property
    def strategy(self) -> MafftOptionsStrategy:
        """MAFFT Strategy:
        * `auto`: Pick a strategy automatically based on the count and size of inputs.
        * `sixmer`: Use 6-mer distance for constructing the guide tree.
        * `localpair`: Compute local pairwise alignments using Smith-Waterman for constructing the guide tree and iterative refinement.
        * `globalpair`: Compute global pairwise alignments using Needleman-Wunsch for constructing the guide tree and iterative refinement.
        """
        if isinstance(self._strategy, Unset):
            raise NotPresentError(self, "strategy")
        return self._strategy

    @strategy.setter
    def strategy(self, value: MafftOptionsStrategy) -> None:
        self._strategy = value

    @strategy.deleter
    def strategy(self) -> None:
        self._strategy = UNSET
