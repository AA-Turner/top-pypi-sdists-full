from benchling_api_client.v2.beta.api.custom_notations import create_custom_notation
from benchling_api_client.v2.beta.models.custom_notation import CustomNotation
from benchling_api_client.v2.beta.models.custom_notation_create import CustomNotationCreate

from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.services.v2.base_service import BaseService


class V2BetaCustomNotationService(BaseService):
    """
    V2-Beta Custom Notations.

    A customer-defined notation to model chemically-modified nucleotide sequences.

    https://benchling.com/api/v2-beta/reference#/Custom%20Notations
    """

    @api_method
    def create(self, custom_notation: CustomNotationCreate) -> CustomNotation:
        """
        Create a custom notation.

        See https://benchling.com/api/v2-beta/reference#/Custom%20Notations/createCustomNotation
        """
        response = create_custom_notation.sync_detailed(client=self.client, json_body=custom_notation)
        return model_from_detailed(response)  # type: ignore
