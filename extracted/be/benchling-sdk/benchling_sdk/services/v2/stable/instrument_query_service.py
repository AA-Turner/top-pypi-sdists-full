from benchling_api_client.v2.stable.api.instrument_queries import get_instrument_query

from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.models import InstrumentQuery
from benchling_sdk.services.v2.base_service import BaseService


class InstrumentQueryService(BaseService):
    """
    Instrument Queries.

    Instrument Queries are used to query the instrument service.

    See https://benchling.com/api/reference#/Instrument%20Queries
    """

    @api_method
    def get_by_id(self, instrument_query_id: str) -> InstrumentQuery:
        """
        Get an instrument query.

        See https://benchling.com/api/reference#/Instrument%20Queries/getInstrumentQuery
        """
        response = get_instrument_query.sync_detailed(
            client=self.client, instrument_query_id=instrument_query_id
        )
        return model_from_detailed(response)
