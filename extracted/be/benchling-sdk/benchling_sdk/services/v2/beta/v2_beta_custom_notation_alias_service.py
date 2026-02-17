from typing import Iterable

from benchling_api_client.v2.beta.api.custom_notation_aliases import bulk_create_custom_notation_aliases
from benchling_api_client.v2.beta.models.bulk_create_custom_notation_aliases_response_200 import (
    BulkCreateCustomNotationAliasesResponse_200,
)
from benchling_api_client.v2.beta.models.custom_notation_alias_bulk_create import (
    CustomNotationAliasBulkCreate,
)
from benchling_api_client.v2.beta.models.custom_notation_alias_create import CustomNotationAliasCreate

from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.services.v2.base_service import BaseService


class V2BetaCustomNotationAliasService(BaseService):
    """
    V2-Beta Custom Notation Aliases.

    A customer-defined alias for a chemical modification on a nucleotide sequence.

    https://benchling.com/api/v2-beta/reference#/Custom%20Notation%20Aliases
    """

    @api_method
    def bulk_create(
        self,
        custom_notation_aliases: Iterable[CustomNotationAliasCreate],
    ) -> BulkCreateCustomNotationAliasesResponse_200:
        """
        Bulk create aliases for a custom notation.

        See https://benchling.com/api/v2-beta/reference#/Custom%20Notation%20Aliases/bulkCreateCustomNotationAliases
        """
        json_body = CustomNotationAliasBulkCreate(list(custom_notation_aliases))
        response = bulk_create_custom_notation_aliases.sync_detailed(client=self.client, json_body=json_body)
        return model_from_detailed(response)  # type: ignore
