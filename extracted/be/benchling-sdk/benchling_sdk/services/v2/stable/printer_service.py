from typing import List, Optional

from benchling_api_client.v2.stable.api.printers import list_printers

from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.helpers.serialization_helpers import none_as_unset
from benchling_sdk.models import Printer
from benchling_sdk.services.v2.base_service import BaseService


class PrinterService(BaseService):
    """
    Printers.

    List printers.

    See https://benchling.com/api/reference#/Printers
    """

    @api_method
    def get_list(self, registry_id: str, name: Optional[str] = None) -> List[Printer]:
        """
        List printers.

        See https://benchling.com/api/reference#/Printers/listPrinters

        :param registry_id: ID of the registry to list printers from.
        :param name: The name of the printer.
        :return: A list of printers
        :rtype: List[Printer]
        """
        response = list_printers.sync_detailed(
            client=self.client, registry_id=registry_id, name=none_as_unset(name)
        )
        results = model_from_detailed(response)
        return results.label_printers
