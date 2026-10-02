from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.course_account_create_nested_request import CourseAccountCreateNestedRequest


T = TypeVar("T", bound="CourseAccountsBulkCreateRequest")


@_attrs_define
class CourseAccountsBulkCreateRequest:
    """
    Attributes:
        course_accounts (list['CourseAccountCreateNestedRequest']):
        project (UUID):
    """

    course_accounts: list["CourseAccountCreateNestedRequest"]
    project: UUID
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        course_accounts = []
        for course_accounts_item_data in self.course_accounts:
            course_accounts_item = course_accounts_item_data.to_dict()
            course_accounts.append(course_accounts_item)

        project = str(self.project)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "course_accounts": course_accounts,
                "project": project,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.course_account_create_nested_request import CourseAccountCreateNestedRequest

        d = dict(src_dict)
        course_accounts = []
        _course_accounts = d.pop("course_accounts")
        for course_accounts_item_data in _course_accounts:
            course_accounts_item = CourseAccountCreateNestedRequest.from_dict(course_accounts_item_data)

            course_accounts.append(course_accounts_item)

        project = UUID(d.pop("project"))

        course_accounts_bulk_create_request = cls(
            course_accounts=course_accounts,
            project=project,
        )

        course_accounts_bulk_create_request.additional_properties = d
        return course_accounts_bulk_create_request

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
