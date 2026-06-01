import logging
from uuid import UUID

from picsellia.colors import Colors
from picsellia.sdk.campaign.abstract_step import AbstractCampaignStep
from picsellia.sdk.connection import Connection
from picsellia.sdk.dao import Dao

logger = logging.getLogger("picsellia")


class ReviewCampaignStep(AbstractCampaignStep):
    _base_path = "/api/campaigns/review/steps"

    def __init__(self, connexion: Connection, data: dict, campaign_id: UUID):
        Dao.__init__(self, connexion, data)
        self._campaign_id = campaign_id

    def __str__(self):
        return f"{Colors.GREEN}Review Campaign Step{Colors.ENDC} for campaign {self.campaign_id} (id: {self.id})"

    @property
    def campaign_id(self) -> UUID:
        """UUID of the (ReviewCampaign) of this step"""
        return self._campaign_id
