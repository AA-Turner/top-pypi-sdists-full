from typing import Union, List

from requests_toolbelt.sessions import BaseUrlSession

from pipebio.models.attachment_type import AttachmentType
from pipebio.util import Util


class Attachments:
    _url: str
    _session: BaseUrlSession

    def __init__(self, session: BaseUrlSession):
        self._url = 'entities'
        self._session = session

    def create(self, entity_id: str, attachment_type: AttachmentType, data: Union[dict, List]):
        """Create a new attachment on an entity.

        Args:
            entity_id: Id of the entity to attach to.
            attachment_type: The kind of attachment to create.
            data: The attachment payload.

        Returns:
            The created attachment object.

        .. API reference (generated - do not edit) ::

        **POST** ``/entities/{entityId}/attachments``

        Create

        Create a new entity attachment

        API parameters:
            * ``entityId`` (path) -- Id of the entity to attach to.
            * ``allowDeletedEntity`` (query) -- If true, allow referencing an entity that has been soft-deleted.

        API request body:
            * ``type`` -- Type of attachment to create.
            * ``data`` -- Attachment payload (shape depends on the attachment type).
            * ``name`` (optional) -- Optional display name for the attachment.

        .. end API reference ::
        """
        print(f'Creating attachment: entity_id={entity_id},kind={attachment_type.value}')
        url = f'{self._url}/{entity_id}/attachments'
        json = {
            "data": data,
            "type": attachment_type.value,
        }
        response = self._session.post(url, json=json)
        Util.raise_detailed_error(response)
        print('Created attachment: response', response.status_code)
        return response.json()

    def upsert_single(self, entity_id: str, attachment_type: AttachmentType, data: Union[dict, List], version: int = 1,
                      ignore_version=True):
        """
        Create or update if exists.

        .. API reference (generated - do not edit) ::

        **PUT** ``/entities/{entityId}/attachments``

        Update

        Update an attachment.

        API parameters:
            * ``entityId`` (path) -- Id of the entity whose attachment is being upserted.
            * ``allowDeletedEntity`` (query) -- If true, allow referencing an entity that has been soft-deleted.

        API request body:
            * ``data`` -- Attachment payload (shape depends on the attachment type).
            * ``version`` (optional) -- Expected current version, used for optimistic concurrency.
            * ``ignoreVersion`` (optional) -- If true, skip the optimistic-concurrency version check.
            * ``type`` -- Type of attachment to upsert.
            * ``name`` (optional) -- Optional display name for the attachment.

        .. end API reference ::
        """
        print(f'Upserting attachment: entity_id={entity_id},type={attachment_type.value},version={version},ignore_version={ignore_version}')
        url = f'{self._url}/{entity_id}/attachments'
        json = {
            "data": data,
            "version": version,
            "type": attachment_type.value,
            "ignoreVersion": ignore_version,
        }
        response = self._session.put(url, json=json)
        Util.raise_detailed_error(response)
        print('Upserted attachment: response', response.status_code)

    def upsert_multi(self, attachment_id: str, data: Union[dict, List], version: int):
        """
        Create or update if exists.

        .. API reference (generated - do not edit) ::

        **PUT** ``/attachments/{attachmentId}``

        Update

        Update an attachment.

        API parameters:
            * ``attachmentId`` (path) -- Id of the attachment to upsert.

        API request body:
            * ``attachment`` -- Attachment object to create or update.

        .. end API reference ::
        """
        print(f'Upserting multi attachment: attachment_id={attachment_id}')
        url = f'attachments/{attachment_id}'
        json = {
            "attachment": {
                "data": data,
                "version": version,
                "id": attachment_id,
            }
        }
        response = self._session.put(url, json=json)
        Util.raise_detailed_error(response)
        print('Upserted attachment: response', response.status_code)

    def get(self, entity_id: str, attachment_type: AttachmentType):
        """Fetch an entity's attachment of a given type.

        Args:
            entity_id: Id of the entity that owns the attachment.
            attachment_type: The kind of attachment to fetch.

        Returns:
            The attachment object.

        .. API reference (generated - do not edit) ::

        **GET** ``/entities/{entityId}/attachments/{type}``

        Get

        Get a single attachment by type.

        API parameters:
            * ``type`` (path) -- Attachment type to fetch.
            * ``entityId`` (path) -- Id of the entity that owns the attachment.
            * ``allowDeletedEntity`` (query) -- If true, allow referencing an entity that has been soft-deleted.

        .. end API reference ::
        """
        url = f'{self._url}/{entity_id}/attachments/{attachment_type.value}'
        response = self._session.get(url)
        Util.raise_detailed_error(response)
        return response.json()
