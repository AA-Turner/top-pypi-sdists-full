import logging

from picsellia.sdk.campaign.abstract_assignment import AbstractAssignment

logger = logging.getLogger("picsellia")


class AnnotationCampaignAssignment(AbstractAssignment):
    _base_path = "/api/campaigns/annotation/assignments"
