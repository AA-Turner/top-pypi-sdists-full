from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.eval_run_payload_response_200_run import EvalRunPayloadResponse200Run


T = TypeVar("T", bound="EvalRunPayloadResponse200")


@_attrs_define
class EvalRunPayloadResponse200:
    """
    Attributes:
        run (EvalRunPayloadResponse200Run): The case, the answer, and every tool call the agent made.
        rendered (str): The same run as a judge agent is shown it.
    """

    run: "EvalRunPayloadResponse200Run"
    rendered: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        run = self.run.to_dict()

        rendered = self.rendered

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "run": run,
                "rendered": rendered,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.eval_run_payload_response_200_run import EvalRunPayloadResponse200Run

        d = src_dict.copy()
        run = EvalRunPayloadResponse200Run.from_dict(d.pop("run"))

        rendered = d.pop("rendered")

        eval_run_payload_response_200 = cls(
            run=run,
            rendered=rendered,
        )

        eval_run_payload_response_200.additional_properties = d
        return eval_run_payload_response_200

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
