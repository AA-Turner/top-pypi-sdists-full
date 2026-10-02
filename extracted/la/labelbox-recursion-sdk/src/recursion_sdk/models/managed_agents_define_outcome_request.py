from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_outcome_rubric_ref import ManagedAgentsOutcomeRubricRef





T = TypeVar("T", bound="ManagedAgentsDefineOutcomeRequest")



@_attrs_define
class ManagedAgentsDefineOutcomeRequest:
    """ A definition of done for a session -- the task plus the rubric it is graded against. Accepted both when starting a
    session and when adding an outcome to a running one. Exactly one of rubric and rubric_ref is required.

        Example:
            {'description': 'Export the product catalog to /out/catalog.csv', 'rubric': '- /out/catalog.csv exists\\n- The
                CSV has a header row with sku, name, and price columns\\n- Every price value is a number'}

        Attributes:
            description (str): The objective the agent works toward, and the statement of it the grader is given. It opens
                the session when the start request carries no message.
            grader_model_ref_id (str | Unset): Model reference for the grader. Defaults to the session's model.
            max_iterations (int | Unset): Ceiling on grader passes before the outcome ends as max_iterations_reached. Omit
                it, or send 0, to revise until the grader is satisfied, which is the default. Set a number only to cap a rubric
                you are not sure can be met.
            rubric (str | Unset): Markdown the grader scores the work against. Criteria must be independently checkable:
                'the CSV has a numeric price column' can be verified, 'the data looks good' cannot. Send this or rubric_ref.
            rubric_ref (ManagedAgentsOutcomeRubricRef | Unset): A file whose text is an outcome's rubric. Example:
                {'file_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'type': 'file'}.
     """

    description: str
    grader_model_ref_id: str | Unset = UNSET
    max_iterations: int | Unset = UNSET
    rubric: str | Unset = UNSET
    rubric_ref: ManagedAgentsOutcomeRubricRef | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_outcome_rubric_ref import ManagedAgentsOutcomeRubricRef # noqa: PLC0415
        description = self.description

        grader_model_ref_id = self.grader_model_ref_id

        max_iterations = self.max_iterations

        rubric = self.rubric

        rubric_ref: dict[str, Any] | Unset = UNSET
        if not isinstance(self.rubric_ref, Unset):
            rubric_ref = self.rubric_ref.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "description": description,
        })
        if grader_model_ref_id is not UNSET:
            field_dict["grader_model_ref_id"] = grader_model_ref_id
        if max_iterations is not UNSET:
            field_dict["max_iterations"] = max_iterations
        if rubric is not UNSET:
            field_dict["rubric"] = rubric
        if rubric_ref is not UNSET:
            field_dict["rubric_ref"] = rubric_ref

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_outcome_rubric_ref import ManagedAgentsOutcomeRubricRef # noqa: PLC0415
        d = dict(src_dict)
        description = d.pop("description")

        grader_model_ref_id = d.pop("grader_model_ref_id", UNSET)

        max_iterations = d.pop("max_iterations", UNSET)

        rubric = d.pop("rubric", UNSET)

        _rubric_ref = d.pop("rubric_ref", UNSET)
        rubric_ref: ManagedAgentsOutcomeRubricRef | Unset
        if isinstance(_rubric_ref,  Unset):
            rubric_ref = UNSET
        else:
            rubric_ref = ManagedAgentsOutcomeRubricRef.from_dict(_rubric_ref)




        managed_agents_define_outcome_request = cls(
            description=description,
            grader_model_ref_id=grader_model_ref_id,
            max_iterations=max_iterations,
            rubric=rubric,
            rubric_ref=rubric_ref,
        )


        managed_agents_define_outcome_request.additional_properties = d
        return managed_agents_define_outcome_request

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
