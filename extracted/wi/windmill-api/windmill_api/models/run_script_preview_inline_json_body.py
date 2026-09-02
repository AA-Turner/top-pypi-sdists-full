from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.run_script_preview_inline_json_body_language import RunScriptPreviewInlineJsonBodyLanguage

if TYPE_CHECKING:
    from ..models.run_script_preview_inline_json_body_args import RunScriptPreviewInlineJsonBodyArgs


T = TypeVar("T", bound="RunScriptPreviewInlineJsonBody")


@_attrs_define
class RunScriptPreviewInlineJsonBody:
    """
    Attributes:
        content (str): The code to run
        args (RunScriptPreviewInlineJsonBodyArgs): The arguments to pass to the script or flow
        language (RunScriptPreviewInlineJsonBodyLanguage):
    """

    content: str
    args: "RunScriptPreviewInlineJsonBodyArgs"
    language: RunScriptPreviewInlineJsonBodyLanguage
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        content = self.content
        args = self.args.to_dict()

        language = self.language.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "content": content,
                "args": args,
                "language": language,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.run_script_preview_inline_json_body_args import RunScriptPreviewInlineJsonBodyArgs

        d = src_dict.copy()
        content = d.pop("content")

        args = RunScriptPreviewInlineJsonBodyArgs.from_dict(d.pop("args"))

        language = RunScriptPreviewInlineJsonBodyLanguage(d.pop("language"))

        run_script_preview_inline_json_body = cls(
            content=content,
            args=args,
            language=language,
        )

        run_script_preview_inline_json_body.additional_properties = d
        return run_script_preview_inline_json_body

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
