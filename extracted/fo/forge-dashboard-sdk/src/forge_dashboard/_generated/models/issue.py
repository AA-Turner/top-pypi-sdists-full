from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.forge import Forge
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.label import Label
  from ..models.linked_pull_request import LinkedPullRequest





T = TypeVar("T", bound="Issue")



@_attrs_define
class Issue:
    """ 
        Attributes:
            forge (Forge):
            repo (str):
            number (int):
            title (str):
            url (str): The real issue URL on its own forge.
            linked_pull_requests (list[LinkedPullRequest]): The open pull requests that will close the issue when they
                merge,
                the other side of a pull request's `closesIssues`, ordered by
                repository and number. Always present, and empty when there are
                none. The server joins the pull requests it already holds, so it
                costs the forge no request. It counts every open pull request the
                user could see, including a draft and one they hid, but not one in
                a repository whose pull requests they ignore. A pull request that
                merged or closed is gone from the list on the next refresh.
            mentioned_by_pull_requests (list[LinkedPullRequest]): The open pull requests that mention the issue without
                closing it,
                the other side of a pull request's `mentionsIssues`, ordered by
                repository and number and with the same entry as
                `linkedPullRequests`. A pull request that closes the issue is only
                in `linkedPullRequests`. Always present, and empty when there are
                none. The pull requests counted are the same as in `linkedPullRequests`.
            housekeeping (bool): True for an issue a bot keeps open and rewrites, Renovate's
                "Dependency Dashboard", which is not work for a person. The
                server decides, so every client lists and counts the same
                issues. It stays in `issues`, and `openIssueCount` leaves it out,
                unless the user's `hideDependencyDashboard` setting is on: then
                the server leaves it out of `issues` as well.
            author (str):
            author_avatar_url (str): The forge's own avatar URL for whoever filed the issue, passed through unchanged and
                never proxied. Empty when the forge supplies none, such as a deleted account.
            author_url (str): The author's profile page on the forge, built by the server from the forge's own web address.
                Empty when there is nothing to link to, such as a deleted account.
            labels (list[Label]):
            created_at (datetime.datetime):
            updated_at (datetime.datetime):
     """

    forge: Forge
    repo: str
    number: int
    title: str
    url: str
    linked_pull_requests: list[LinkedPullRequest]
    mentioned_by_pull_requests: list[LinkedPullRequest]
    housekeeping: bool
    author: str
    author_avatar_url: str
    author_url: str
    labels: list[Label]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.label import Label # noqa: PLC0415
        from ..models.linked_pull_request import LinkedPullRequest # noqa: PLC0415
        forge = self.forge.value

        repo = self.repo

        number = self.number

        title = self.title

        url = self.url

        linked_pull_requests = []
        for linked_pull_requests_item_data in self.linked_pull_requests:
            linked_pull_requests_item = linked_pull_requests_item_data.to_dict()
            linked_pull_requests.append(linked_pull_requests_item)



        mentioned_by_pull_requests = []
        for mentioned_by_pull_requests_item_data in self.mentioned_by_pull_requests:
            mentioned_by_pull_requests_item = mentioned_by_pull_requests_item_data.to_dict()
            mentioned_by_pull_requests.append(mentioned_by_pull_requests_item)



        housekeeping = self.housekeeping

        author = self.author

        author_avatar_url = self.author_avatar_url

        author_url = self.author_url

        labels = []
        for labels_item_data in self.labels:
            labels_item = labels_item_data.to_dict()
            labels.append(labels_item)



        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "forge": forge,
            "repo": repo,
            "number": number,
            "title": title,
            "url": url,
            "linkedPullRequests": linked_pull_requests,
            "mentionedByPullRequests": mentioned_by_pull_requests,
            "housekeeping": housekeeping,
            "author": author,
            "authorAvatarUrl": author_avatar_url,
            "authorUrl": author_url,
            "labels": labels,
            "createdAt": created_at,
            "updatedAt": updated_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.label import Label # noqa: PLC0415
        from ..models.linked_pull_request import LinkedPullRequest # noqa: PLC0415
        d = dict(src_dict)
        forge = Forge(d.pop("forge"))




        repo = d.pop("repo")

        number = d.pop("number")

        title = d.pop("title")

        url = d.pop("url")

        linked_pull_requests = []
        _linked_pull_requests = d.pop("linkedPullRequests")
        for linked_pull_requests_item_data in (_linked_pull_requests):
            linked_pull_requests_item = LinkedPullRequest.from_dict(linked_pull_requests_item_data)



            linked_pull_requests.append(linked_pull_requests_item)


        mentioned_by_pull_requests = []
        _mentioned_by_pull_requests = d.pop("mentionedByPullRequests")
        for mentioned_by_pull_requests_item_data in (_mentioned_by_pull_requests):
            mentioned_by_pull_requests_item = LinkedPullRequest.from_dict(mentioned_by_pull_requests_item_data)



            mentioned_by_pull_requests.append(mentioned_by_pull_requests_item)


        housekeeping = d.pop("housekeeping")

        author = d.pop("author")

        author_avatar_url = d.pop("authorAvatarUrl")

        author_url = d.pop("authorUrl")

        labels = []
        _labels = d.pop("labels")
        for labels_item_data in (_labels):
            labels_item = Label.from_dict(labels_item_data)



            labels.append(labels_item)


        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))




        issue = cls(
            forge=forge,
            repo=repo,
            number=number,
            title=title,
            url=url,
            linked_pull_requests=linked_pull_requests,
            mentioned_by_pull_requests=mentioned_by_pull_requests,
            housekeeping=housekeeping,
            author=author,
            author_avatar_url=author_avatar_url,
            author_url=author_url,
            labels=labels,
            created_at=created_at,
            updated_at=updated_at,
        )


        issue.additional_properties = d
        return issue

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
