from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.preview_inline_language import PreviewInlineLanguage

if TYPE_CHECKING:
    from ..models.preview_inline_args import PreviewInlineArgs


T = TypeVar("T", bound="PreviewInline")


@_attrs_define
class PreviewInline:
    """
    Attributes:
        content (str): The code to run
        args (PreviewInlineArgs): The arguments to pass to the script or flow
        language (PreviewInlineLanguage):
    """

    content: str
    args: "PreviewInlineArgs"
    language: PreviewInlineLanguage
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
        from ..models.preview_inline_args import PreviewInlineArgs

        d = src_dict.copy()
        content = d.pop("content")

        args = PreviewInlineArgs.from_dict(d.pop("args"))

        language = PreviewInlineLanguage(d.pop("language"))

        preview_inline = cls(
            content=content,
            args=args,
            language=language,
        )

        preview_inline.additional_properties = d
        return preview_inline

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
