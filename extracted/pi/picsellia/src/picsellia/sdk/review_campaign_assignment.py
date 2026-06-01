import logging

from picsellia.sdk.campaign.abstract_assignment import AbstractAssignment

logger = logging.getLogger("picsellia")


class ReviewCampaignAssignment(AbstractAssignment):
    _base_path = "/api/campaigns/review/assignments"
