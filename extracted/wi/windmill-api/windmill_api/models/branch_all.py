from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.branch_all_type import BranchAllType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.branch_all_branches_item import BranchAllBranchesItem
    from ..models.branch_all_parallelism_type_0 import BranchAllParallelismType0
    from ..models.branch_all_parallelism_type_1 import BranchAllParallelismType1
    from ..models.branch_all_parallelism_type_2 import BranchAllParallelismType2


T = TypeVar("T", bound="BranchAll")


@_attrs_define
class BranchAll:
    """Parallel branching where all branches execute simultaneously. Unlike BranchOne, all branches run regardless of
    conditions. Useful for executing independent tasks concurrently

        Attributes:
            branches (List['BranchAllBranchesItem']): Array of branches that all execute (either in parallel or
                sequentially)
            type (BranchAllType):
            parallel (Union[Unset, bool]): If true, all branches execute concurrently. If false, they execute sequentially
            parallelism (Union['BranchAllParallelismType0', 'BranchAllParallelismType1', 'BranchAllParallelismType2',
                Unset]): Maps input parameters for a step. Can be a static value or a JavaScript expression that references
                previous results or flow inputs
    """

    branches: List["BranchAllBranchesItem"]
    type: BranchAllType
    parallel: Union[Unset, bool] = UNSET
    parallelism: Union[
        "BranchAllParallelismType0", "BranchAllParallelismType1", "BranchAllParallelismType2", Unset
    ] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.branch_all_parallelism_type_0 import BranchAllParallelismType0
        from ..models.branch_all_parallelism_type_1 import BranchAllParallelismType1

        branches = []
        for branches_item_data in self.branches:
            branches_item = branches_item_data.to_dict()

            branches.append(branches_item)

        type = self.type.value

        parallel = self.parallel
        parallelism: Union[Dict[str, Any], Unset]
        if isinstance(self.parallelism, Unset):
            parallelism = UNSET

        elif isinstance(self.parallelism, BranchAllParallelismType0):
            parallelism = UNSET
            if not isinstance(self.parallelism, Unset):
                parallelism = self.parallelism.to_dict()

        elif isinstance(self.parallelism, BranchAllParallelismType1):
            parallelism = UNSET
            if not isinstance(self.parallelism, Unset):
                parallelism = self.parallelism.to_dict()

        else:
            parallelism = UNSET
            if not isinstance(self.parallelism, Unset):
                parallelism = self.parallelism.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "branches": branches,
                "type": type,
            }
        )
        if parallel is not UNSET:
            field_dict["parallel"] = parallel
        if parallelism is not UNSET:
            field_dict["parallelism"] = parallelism

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.branch_all_branches_item import BranchAllBranchesItem
        from ..models.branch_all_parallelism_type_0 import BranchAllParallelismType0
        from ..models.branch_all_parallelism_type_1 import BranchAllParallelismType1
        from ..models.branch_all_parallelism_type_2 import BranchAllParallelismType2

        d = src_dict.copy()
        branches = []
        _branches = d.pop("branches")
        for branches_item_data in _branches:
            branches_item = BranchAllBranchesItem.from_dict(branches_item_data)

            branches.append(branches_item)

        type = BranchAllType(d.pop("type"))

        parallel = d.pop("parallel", UNSET)

        def _parse_parallelism(
            data: object,
        ) -> Union["BranchAllParallelismType0", "BranchAllParallelismType1", "BranchAllParallelismType2", Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _parallelism_type_0 = data
                parallelism_type_0: Union[Unset, BranchAllParallelismType0]
                if isinstance(_parallelism_type_0, Unset):
                    parallelism_type_0 = UNSET
                else:
                    parallelism_type_0 = BranchAllParallelismType0.from_dict(_parallelism_type_0)

                return parallelism_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _parallelism_type_1 = data
                parallelism_type_1: Union[Unset, BranchAllParallelismType1]
                if isinstance(_parallelism_type_1, Unset):
                    parallelism_type_1 = UNSET
                else:
                    parallelism_type_1 = BranchAllParallelismType1.from_dict(_parallelism_type_1)

                return parallelism_type_1
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            _parallelism_type_2 = data
            parallelism_type_2: Union[Unset, BranchAllParallelismType2]
            if isinstance(_parallelism_type_2, Unset):
                parallelism_type_2 = UNSET
            else:
                parallelism_type_2 = BranchAllParallelismType2.from_dict(_parallelism_type_2)

            return parallelism_type_2

        parallelism = _parse_parallelism(d.pop("parallelism", UNSET))

        branch_all = cls(
            branches=branches,
            type=type,
            parallel=parallel,
            parallelism=parallelism,
        )

        branch_all.additional_properties = d
        return branch_all

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
