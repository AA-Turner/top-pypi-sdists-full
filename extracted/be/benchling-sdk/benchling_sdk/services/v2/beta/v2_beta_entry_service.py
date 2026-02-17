from typing import Iterable, Optional

from benchling_api_client.v2.beta.api.entries import get_entry, get_template_entry, update_entry
from benchling_api_client.v2.beta.models.entry import Entry
from benchling_api_client.v2.beta.models.entry_template import EntryTemplate
from benchling_api_client.v2.beta.models.entry_update import EntryUpdate

from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.helpers.serialization_helpers import none_as_unset, optional_array_query_param
from benchling_sdk.services.v2.base_service import BaseService


class V2BetaEntryService(BaseService):
    """
    V2-Beta Entries.

    Entries are rich text documents that allow you to capture all of your experimental data in one place.

    https://benchling.com/api/v2-beta/reference#/Entries
    """

    @api_method
    def get_by_id(self, entry_id: str) -> Entry:
        """
        Get an entry.

        See https://benchling.com/api/v2-beta/reference#/Entries/getEntry
        """
        response = get_entry.sync_detailed(client=self.client, entry_id=entry_id)
        return model_from_detailed(response)

    @api_method
    def update_entry(
        self, entry_id: str, entry: EntryUpdate, returning: Optional[Iterable[str]] = None
    ) -> Entry:
        """
        Update a notebook entry's metadata.

        See https://benchling.com/api/v2-beta/reference#/Entries/updateEntry
        """
        returning_string = optional_array_query_param(returning)
        response = update_entry.sync_detailed(
            client=self.client, entry_id=entry_id, json_body=entry, returning=none_as_unset(returning_string)
        )
        return model_from_detailed(response)

    @api_method
    def get_entry_template_by_id(self, entry_template_id: str) -> EntryTemplate:
        """
        Get a notebook template entry by ID.

        See https://benchling.com/api/v2-beta/reference#/Entries/getTemplateEntry
        """
        response = get_template_entry.sync_detailed(client=self.client, entry_template_id=entry_template_id)
        return model_from_detailed(response)
