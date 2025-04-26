from typing import List, Optional

from benchling_api_client.v2.beta.api.analyses import get_analysis, update_analysis
from benchling_api_client.v2.beta.models.analysis import Analysis
from benchling_api_client.v2.beta.models.analysis_update import AnalysisUpdate

from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.helpers.serialization_helpers import none_as_unset, optional_array_query_param
from benchling_sdk.services.v2.base_service import BaseService


class V2BetaAnalysisService(BaseService):
    """
    V2-Beta Analyses.

    Analyses allow experimental data to be viewed, analyzed, and visualized.

    https://benchling.com/api/v2-beta/reference#/Analyses
    """

    @api_method
    def get_by_id(self, analysis_id: str, returning: Optional[List[str]] = None) -> Analysis:
        """
        Get an analysis.

        See https://benchling.com/api/v2-beta/reference#/Analyses/getAnalysis
        """
        response = get_analysis.sync_detailed(
            client=self.client,
            analysis_id=analysis_id,
            returning=none_as_unset(optional_array_query_param(returning)),
        )
        return model_from_detailed(response)

    @api_method
    def update(self, analysis_id: str, update: AnalysisUpdate) -> Analysis:
        """
        Update an analysis.

        See https://benchling.com/api/v2-beta/reference#/Analyses/updateAnalysis
        """
        response = update_analysis.sync_detailed(
            client=self.client, analysis_id=analysis_id, json_body=update
        )
        return model_from_detailed(response)
