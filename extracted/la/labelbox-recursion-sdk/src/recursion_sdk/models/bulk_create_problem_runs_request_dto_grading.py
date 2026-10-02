from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="BulkCreateProblemRunsRequestDtoGrading")



@_attrs_define
class BulkCreateProblemRunsRequestDtoGrading:
    """ Per-request grader override for a bulk problem-run submission. The grading config itself is read from the locked
    problem version server-side.

        Attributes:
            model_name (None | str | Unset): Grader model override for this submission. Null permits a model-less run-config
                grader; omission leaves model selection to the resolved grader binding.
            image_id (None | str | Unset): Grader container-image override for this submission. Null permits an image-less
                run-config grader; omission leaves image selection to the resolved grader binding.
     """

    model_name: None | str | Unset = UNSET
    image_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        model_name: None | str | Unset
        if isinstance(self.model_name, Unset):
            model_name = UNSET
        else:
            model_name = self.model_name

        image_id: None | str | Unset
        if isinstance(self.image_id, Unset):
            image_id = UNSET
        else:
            image_id = self.image_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if model_name is not UNSET:
            field_dict["modelName"] = model_name
        if image_id is not UNSET:
            field_dict["imageId"] = image_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        def _parse_model_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        model_name = _parse_model_name(d.pop("modelName", UNSET))


        def _parse_image_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        image_id = _parse_image_id(d.pop("imageId", UNSET))


        bulk_create_problem_runs_request_dto_grading = cls(
            model_name=model_name,
            image_id=image_id,
        )


        bulk_create_problem_runs_request_dto_grading.additional_properties = d
        return bulk_create_problem_runs_request_dto_grading

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
