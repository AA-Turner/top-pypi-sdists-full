import abc
from pydantic import StrictStr
from typing import TYPE_CHECKING, List

from istari_digital_client.legacy.v2.models.access_relationship import AccessRelationship
from istari_digital_client.legacy.v2.models.access_subject_type import AccessSubjectType
from istari_digital_client.legacy.v2.models.access_relation import AccessRelation
from istari_digital_client.legacy.v2.models.access_resource_type import AccessResourceType
from istari_digital_client.legacy.v2.models.update_access_relationship import (
    UpdateAccessRelationship,
)
from istari_digital_client.legacy.log_utils import log_method

if TYPE_CHECKING:
    from istari_digital_client.legacy.v2.api.v2_api import V2Api


class Shareable(abc.ABC):
    def _require_client(self) -> "V2Api":
        """
        Ensure that a client is available on this instance.

        :raises ValueError: If the ``client`` attribute is not set.
        """
        client = getattr(self, "client", None)
        if client is None:
            raise ValueError(
                f"`client` is not set for instance of {self.__class__.__name__}"
            )
        return client

    @property
    def _resource_id(self) -> StrictStr:
        """
        Return the ID of the current resource.

        This assumes the instance has an ``id`` attribute.
        :raises ValueError: If ``id`` is not present.
        """
        resource_id = getattr(self, "id", None)

        if resource_id is None:
            raise ValueError("id is not set")

        return resource_id

    @property
    def _resource_type(self) -> AccessResourceType:
        """
        Resolve the resource type based on the class name.

        :raises ValueError: If the class name does not match a valid AccessResourceType.
        """
        class_name = self.__class__.__name__

        try:
            return AccessResourceType(class_name.lower())
        except ValueError as e:
            raise ValueError(
                f"Invalid resource type for {class_name}. "
                f"Ensure the class name is a valid AccessResourceType."
            ) from e

    @log_method
    def create_access(
        self,
        subject_type: AccessSubjectType,
        subject_id: str,
        relation: AccessRelation,
    ) -> AccessRelationship:
        """
        Create a new access relationship for a subject by ID.

        :param subject_type: The type of subject being granted access (e.g., user, group).
        :param subject_id: The ID of the subject.
        :param relation: The access relation to grant (e.g., reader, writer).
        :raises ValueError: If the client is not set.
        """
        client = self._require_client()

        access_relationship = AccessRelationship(
            subject_type=subject_type,
            subject_id=subject_id,
            relation=relation,
            resource_type=self._resource_type,
            resource_id=self._resource_id,
        )

        return client.create_access(
            access_relationship=access_relationship,
        )

    @log_method
    def create_access_by_email(
        self,
        subject_type: AccessSubjectType,
        subject_email: StrictStr,
        relation: AccessRelation,
    ) -> AccessRelationship:
        """
        Create a new access relationship for a subject by email.

        Useful for inviting users across tenants when their ID is not yet known.

        :param subject_type: The type of subject being granted access.
        :param subject_email: The email address of the subject.
        :param relation: The access relation to grant.
        :raises ValueError: If the client is not set.
        """
        client = self._require_client()

        return client.create_access_by_email_for_other_tenants(
            subject_type=subject_type,
            email=subject_email,
            resource_type=self._resource_type,
            resource_id=self._resource_id,
            access_relationship=relation,
        )

    @log_method
    def update_access(
        self,
        subject_type: AccessSubjectType,
        subject_id: StrictStr,
        relation: AccessRelation,
    ) -> AccessRelationship:
        """
        Update an existing access relationship for a subject.

        :param subject_type: The type of subject whose access is being updated.
        :param subject_id: The ID of the subject.
        :param relation: The new access relation to assign.
        :raises ValueError: If the client is not set.
        """
        client = self._require_client()

        update_access_relationship = UpdateAccessRelationship(
            relation=relation,
        )

        return client.update_access(
            subject_type=subject_type,
            subject_id=subject_id,
            resource_type=self._resource_type,
            resource_id=self._resource_id,
            update_access_relationship=update_access_relationship,
        )

    @log_method
    def remove_access(
        self,
        subject_type: AccessSubjectType,
        subject_id: StrictStr,
    ) -> None:
        """
        Remove an existing access relationship.

        :param subject_type: The type of subject whose access is being revoked.
        :param subject_id: The ID of the subject.
        :raises ValueError: If the client is not set.
        """
        client = self._require_client()

        client.remove_access(
            subject_type=subject_type,
            subject_id=subject_id,
            resource_type=self._resource_type,
            resource_id=self._resource_id,
        )

    @log_method
    def list_access(self) -> List[AccessRelationship]:
        """
        List all access relationships for this resource.

        :raises ValueError: If the client is not set.
        """
        client = self._require_client()

        return client.list_access(
            resource_type=self._resource_type,
            resource_id=self._resource_id,
        )
