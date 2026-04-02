import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.reviewer_affiliation import ReviewerAffiliation
    from ..models.reviewer_expertise import ReviewerExpertise
    from ..models.reviewer_profile_profile_completeness import ReviewerProfileProfileCompleteness
    from ..models.reviewer_publication import ReviewerPublication
    from ..models.reviewer_stats import ReviewerStats


T = TypeVar("T", bound="ReviewerProfile")


@_attrs_define
class ReviewerProfile:
    """
    Attributes:
        url (str):
        uuid (UUID):
        user (str):
        user_uuid (UUID):
        user_full_name (str):
        user_email (str):
        orcid_connected (bool): Check if ORCID is connected (has access token).
        orcid_last_sync (Union[None, datetime.datetime]):
        affiliations (list['ReviewerAffiliation']):
        expertise_set (list['ReviewerExpertise']):
        publications (list['ReviewerPublication']):
        stats (ReviewerStats):
        profile_completeness (ReviewerProfileProfileCompleteness): Calculate profile completeness percentage and missing
            fields.
        is_published (bool): Whether profile is discoverable by call managers
        published_at (Union[None, datetime.datetime]): When the profile was published
        created (datetime.datetime):
        modified (datetime.datetime):
        orcid_id (Union[None, Unset, str]): ORCID identifier (format: 0000-0000-0000-0000)
        biography (Union[Unset, str]): Professional biography / summary
        alternative_names (Union[Unset, Any]): List of name variants used in publications
        available_for_reviews (Union[Unset, bool]): Whether reviewer is currently accepting review requests
    """

    url: str
    uuid: UUID
    user: str
    user_uuid: UUID
    user_full_name: str
    user_email: str
    orcid_connected: bool
    orcid_last_sync: Union[None, datetime.datetime]
    affiliations: list["ReviewerAffiliation"]
    expertise_set: list["ReviewerExpertise"]
    publications: list["ReviewerPublication"]
    stats: "ReviewerStats"
    profile_completeness: "ReviewerProfileProfileCompleteness"
    is_published: bool
    published_at: Union[None, datetime.datetime]
    created: datetime.datetime
    modified: datetime.datetime
    orcid_id: Union[None, Unset, str] = UNSET
    biography: Union[Unset, str] = UNSET
    alternative_names: Union[Unset, Any] = UNSET
    available_for_reviews: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        user = self.user

        user_uuid = str(self.user_uuid)

        user_full_name = self.user_full_name

        user_email = self.user_email

        orcid_connected = self.orcid_connected

        orcid_last_sync: Union[None, str]
        if isinstance(self.orcid_last_sync, datetime.datetime):
            orcid_last_sync = self.orcid_last_sync.isoformat()
        else:
            orcid_last_sync = self.orcid_last_sync

        affiliations = []
        for affiliations_item_data in self.affiliations:
            affiliations_item = affiliations_item_data.to_dict()
            affiliations.append(affiliations_item)

        expertise_set = []
        for expertise_set_item_data in self.expertise_set:
            expertise_set_item = expertise_set_item_data.to_dict()
            expertise_set.append(expertise_set_item)

        publications = []
        for publications_item_data in self.publications:
            publications_item = publications_item_data.to_dict()
            publications.append(publications_item)

        stats = self.stats.to_dict()

        profile_completeness = self.profile_completeness.to_dict()

        is_published = self.is_published

        published_at: Union[None, str]
        if isinstance(self.published_at, datetime.datetime):
            published_at = self.published_at.isoformat()
        else:
            published_at = self.published_at

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        orcid_id: Union[None, Unset, str]
        if isinstance(self.orcid_id, Unset):
            orcid_id = UNSET
        else:
            orcid_id = self.orcid_id

        biography = self.biography

        alternative_names = self.alternative_names

        available_for_reviews = self.available_for_reviews

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "user": user,
                "user_uuid": user_uuid,
                "user_full_name": user_full_name,
                "user_email": user_email,
                "orcid_connected": orcid_connected,
                "orcid_last_sync": orcid_last_sync,
                "affiliations": affiliations,
                "expertise_set": expertise_set,
                "publications": publications,
                "stats": stats,
                "profile_completeness": profile_completeness,
                "is_published": is_published,
                "published_at": published_at,
                "created": created,
                "modified": modified,
            }
        )
        if orcid_id is not UNSET:
            field_dict["orcid_id"] = orcid_id
        if biography is not UNSET:
            field_dict["biography"] = biography
        if alternative_names is not UNSET:
            field_dict["alternative_names"] = alternative_names
        if available_for_reviews is not UNSET:
            field_dict["available_for_reviews"] = available_for_reviews

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.reviewer_affiliation import ReviewerAffiliation
        from ..models.reviewer_expertise import ReviewerExpertise
        from ..models.reviewer_profile_profile_completeness import ReviewerProfileProfileCompleteness
        from ..models.reviewer_publication import ReviewerPublication
        from ..models.reviewer_stats import ReviewerStats

        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        user = d.pop("user")

        user_uuid = UUID(d.pop("user_uuid"))

        user_full_name = d.pop("user_full_name")

        user_email = d.pop("user_email")

        orcid_connected = d.pop("orcid_connected")

        def _parse_orcid_last_sync(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                orcid_last_sync_type_0 = isoparse(data)

                return orcid_last_sync_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        orcid_last_sync = _parse_orcid_last_sync(d.pop("orcid_last_sync"))

        affiliations = []
        _affiliations = d.pop("affiliations")
        for affiliations_item_data in _affiliations:
            affiliations_item = ReviewerAffiliation.from_dict(affiliations_item_data)

            affiliations.append(affiliations_item)

        expertise_set = []
        _expertise_set = d.pop("expertise_set")
        for expertise_set_item_data in _expertise_set:
            expertise_set_item = ReviewerExpertise.from_dict(expertise_set_item_data)

            expertise_set.append(expertise_set_item)

        publications = []
        _publications = d.pop("publications")
        for publications_item_data in _publications:
            publications_item = ReviewerPublication.from_dict(publications_item_data)

            publications.append(publications_item)

        stats = ReviewerStats.from_dict(d.pop("stats"))

        profile_completeness = ReviewerProfileProfileCompleteness.from_dict(d.pop("profile_completeness"))

        is_published = d.pop("is_published")

        def _parse_published_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                published_at_type_0 = isoparse(data)

                return published_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        published_at = _parse_published_at(d.pop("published_at"))

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        def _parse_orcid_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        orcid_id = _parse_orcid_id(d.pop("orcid_id", UNSET))

        biography = d.pop("biography", UNSET)

        alternative_names = d.pop("alternative_names", UNSET)

        available_for_reviews = d.pop("available_for_reviews", UNSET)

        reviewer_profile = cls(
            url=url,
            uuid=uuid,
            user=user,
            user_uuid=user_uuid,
            user_full_name=user_full_name,
            user_email=user_email,
            orcid_connected=orcid_connected,
            orcid_last_sync=orcid_last_sync,
            affiliations=affiliations,
            expertise_set=expertise_set,
            publications=publications,
            stats=stats,
            profile_completeness=profile_completeness,
            is_published=is_published,
            published_at=published_at,
            created=created,
            modified=modified,
            orcid_id=orcid_id,
            biography=biography,
            alternative_names=alternative_names,
            available_for_reviews=available_for_reviews,
        )

        reviewer_profile.additional_properties = d
        return reviewer_profile

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
