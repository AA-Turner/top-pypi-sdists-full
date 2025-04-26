from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="NucleotideAlignmentBaseClustaloOptions")


@attr.s(auto_attribs=True, repr=False)
class NucleotideAlignmentBaseClustaloOptions:
    """ Options to pass to the ClustalO algorithm, only applicable for ClustalO. """

    _max_guidetree_iterations: Union[Unset, int] = -1
    _max_hmm_iterations: Union[Unset, int] = -1
    _mbed_guide_tree: Union[Unset, bool] = True
    _mbed_iteration: Union[Unset, bool] = True
    _num_combined_iterations: Union[Unset, int] = 0
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("max_guidetree_iterations={}".format(repr(self._max_guidetree_iterations)))
        fields.append("max_hmm_iterations={}".format(repr(self._max_hmm_iterations)))
        fields.append("mbed_guide_tree={}".format(repr(self._mbed_guide_tree)))
        fields.append("mbed_iteration={}".format(repr(self._mbed_iteration)))
        fields.append("num_combined_iterations={}".format(repr(self._num_combined_iterations)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "NucleotideAlignmentBaseClustaloOptions({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        max_guidetree_iterations = self._max_guidetree_iterations
        max_hmm_iterations = self._max_hmm_iterations
        mbed_guide_tree = self._mbed_guide_tree
        mbed_iteration = self._mbed_iteration
        num_combined_iterations = self._num_combined_iterations

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if max_guidetree_iterations is not UNSET:
            field_dict["maxGuidetreeIterations"] = max_guidetree_iterations
        if max_hmm_iterations is not UNSET:
            field_dict["maxHmmIterations"] = max_hmm_iterations
        if mbed_guide_tree is not UNSET:
            field_dict["mbedGuideTree"] = mbed_guide_tree
        if mbed_iteration is not UNSET:
            field_dict["mbedIteration"] = mbed_iteration
        if num_combined_iterations is not UNSET:
            field_dict["numCombinedIterations"] = num_combined_iterations

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_max_guidetree_iterations() -> Union[Unset, int]:
            max_guidetree_iterations = d.pop("maxGuidetreeIterations")
            return max_guidetree_iterations

        try:
            max_guidetree_iterations = get_max_guidetree_iterations()
        except KeyError:
            if strict:
                raise
            max_guidetree_iterations = cast(Union[Unset, int], UNSET)

        def get_max_hmm_iterations() -> Union[Unset, int]:
            max_hmm_iterations = d.pop("maxHmmIterations")
            return max_hmm_iterations

        try:
            max_hmm_iterations = get_max_hmm_iterations()
        except KeyError:
            if strict:
                raise
            max_hmm_iterations = cast(Union[Unset, int], UNSET)

        def get_mbed_guide_tree() -> Union[Unset, bool]:
            mbed_guide_tree = d.pop("mbedGuideTree")
            return mbed_guide_tree

        try:
            mbed_guide_tree = get_mbed_guide_tree()
        except KeyError:
            if strict:
                raise
            mbed_guide_tree = cast(Union[Unset, bool], UNSET)

        def get_mbed_iteration() -> Union[Unset, bool]:
            mbed_iteration = d.pop("mbedIteration")
            return mbed_iteration

        try:
            mbed_iteration = get_mbed_iteration()
        except KeyError:
            if strict:
                raise
            mbed_iteration = cast(Union[Unset, bool], UNSET)

        def get_num_combined_iterations() -> Union[Unset, int]:
            num_combined_iterations = d.pop("numCombinedIterations")
            return num_combined_iterations

        try:
            num_combined_iterations = get_num_combined_iterations()
        except KeyError:
            if strict:
                raise
            num_combined_iterations = cast(Union[Unset, int], UNSET)

        nucleotide_alignment_base_clustalo_options = cls(
            max_guidetree_iterations=max_guidetree_iterations,
            max_hmm_iterations=max_hmm_iterations,
            mbed_guide_tree=mbed_guide_tree,
            mbed_iteration=mbed_iteration,
            num_combined_iterations=num_combined_iterations,
        )

        nucleotide_alignment_base_clustalo_options.additional_properties = d
        return nucleotide_alignment_base_clustalo_options

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
    def max_guidetree_iterations(self) -> int:
        """ Max guide tree iterations within combined iterations. Use -1 for no max (all iterations will include guide tree iterations). """
        if isinstance(self._max_guidetree_iterations, Unset):
            raise NotPresentError(self, "max_guidetree_iterations")
        return self._max_guidetree_iterations

    @max_guidetree_iterations.setter
    def max_guidetree_iterations(self, value: int) -> None:
        self._max_guidetree_iterations = value

    @max_guidetree_iterations.deleter
    def max_guidetree_iterations(self) -> None:
        self._max_guidetree_iterations = UNSET

    @property
    def max_hmm_iterations(self) -> int:
        """ Max HMM iterations within combined iterations. Use -1 for no max (all iterations will include HMM iterations). """
        if isinstance(self._max_hmm_iterations, Unset):
            raise NotPresentError(self, "max_hmm_iterations")
        return self._max_hmm_iterations

    @max_hmm_iterations.setter
    def max_hmm_iterations(self, value: int) -> None:
        self._max_hmm_iterations = value

    @max_hmm_iterations.deleter
    def max_hmm_iterations(self) -> None:
        self._max_hmm_iterations = UNSET

    @property
    def mbed_guide_tree(self) -> bool:
        """ Whether mBed-like clustering guide tree should be used (faster to use it). """
        if isinstance(self._mbed_guide_tree, Unset):
            raise NotPresentError(self, "mbed_guide_tree")
        return self._mbed_guide_tree

    @mbed_guide_tree.setter
    def mbed_guide_tree(self, value: bool) -> None:
        self._mbed_guide_tree = value

    @mbed_guide_tree.deleter
    def mbed_guide_tree(self) -> None:
        self._mbed_guide_tree = UNSET

    @property
    def mbed_iteration(self) -> bool:
        """ Whether mBed-like clustering iteration should be used (faster to use it). """
        if isinstance(self._mbed_iteration, Unset):
            raise NotPresentError(self, "mbed_iteration")
        return self._mbed_iteration

    @mbed_iteration.setter
    def mbed_iteration(self, value: bool) -> None:
        self._mbed_iteration = value

    @mbed_iteration.deleter
    def mbed_iteration(self) -> None:
        self._mbed_iteration = UNSET

    @property
    def num_combined_iterations(self) -> int:
        """ Number of (combined guide-tree/HMM) iterations. """
        if isinstance(self._num_combined_iterations, Unset):
            raise NotPresentError(self, "num_combined_iterations")
        return self._num_combined_iterations

    @num_combined_iterations.setter
    def num_combined_iterations(self, value: int) -> None:
        self._num_combined_iterations = value

    @num_combined_iterations.deleter
    def num_combined_iterations(self) -> None:
        self._num_combined_iterations = UNSET
