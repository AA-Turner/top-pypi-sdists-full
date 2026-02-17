from typing import Iterable, Optional

from benchling_api_client.v2.beta.api.worksheets import get_worksheet_review_changes
from benchling_api_client.v2.beta.models.worksheet_review_changes_by_id import WorksheetReviewChangesById

from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.helpers.serialization_helpers import none_as_unset, optional_array_query_param
from benchling_sdk.services.v2.base_service import BaseService


class V2BetaWorksheetService(BaseService):
    """
    V2-Beta Worksheets.

    Worksheets are structured documents that help you plan and describe your experiment operations in a
    consistent way.

    See also https://benchling.com/api/v2-beta/reference#/Worksheets
    """

    @api_method
    def get_worksheet_review_changes(
        self,
        worksheet_id: str,
        returning: Optional[Iterable[str]] = None,
    ) -> WorksheetReviewChangesById:
        """
        Get a worksheet's review changes given a worksheet ID.

        See also https://benchling.com/api/v2-beta/reference#/Worksheets/getWorksheetReviewChanges
        """
        response = get_worksheet_review_changes.sync_detailed(
            client=self.client,
            worksheet_id=worksheet_id,
            returning=none_as_unset(optional_array_query_param(returning)),
        )
        return model_from_detailed(response)
