from pydantic import Field
from typing import List, Optional
from datetime import datetime
from enum import StrEnum
from letschatty.models.base_models.chatty_asset_model import CompanyAssetModel
from letschatty.models.utils.types.identifier import StrObjectId
from .scheduled_communication import LaunchScheduledCommunication
from .subscription import LaunchSubscription, LaunchSubscriptionStatus
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode


class LaunchStatus(StrEnum):
    """Status of the launch"""
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Launch(CompanyAssetModel):
    """
    Launch asset model.
    Represents a product launch event with communications and subscriptions.
    """
    # Basic info
    name: str = Field(description="Name of the launch")
    product_name: str = Field(description="Name of the product being launched")
    product_description: str = Field(description="Description of the product being launched")
    launch_datetime: datetime = Field(description="Date and time of the launch")
    access_link: str = Field(description="Base link for the launch event")
    status: LaunchStatus = Field(default=LaunchStatus.DRAFT, description="Current status of the launch")

    # Data Collection & Pre-qualification
    form_fields: List[StrObjectId] = Field(
        default_factory=list,
        description="FormField IDs required before subscription"
    )
    acceptance_criteria: str = Field(
        default="",
        description="Instructions for AI to determine when to subscribe the user"
    )
    enable_tracking: bool = Field(
        default=False,
        description="If True, generate personal trackable links for each subscriber"
    )

    # Communications
    welcome_kit: Optional[LaunchScheduledCommunication] = Field(
        default=None,
        description="Communication sent immediately upon subscription (delta_minutes=0)"
    )
    pre_launch_communications: List[LaunchScheduledCommunication] = Field(
        default_factory=list,
        description="Communications scheduled before the launch"
    )
    post_launch_attended_communications: List[LaunchScheduledCommunication] = Field(
        default_factory=list,
        description="Communications for attendees after the launch"
    )
    post_launch_missed_communications: List[LaunchScheduledCommunication] = Field(
        default_factory=list,
        description="Communications for those who missed the launch"
    )

    # Subscriptions (embedded)
    subscriptions: List[LaunchSubscription] = Field(
        default_factory=list,
        description="List of chat subscriptions to this launch"
    )

    # AI Configuration
    chat_examples: List[StrObjectId] = Field(
        default_factory=list,
        description="Chat examples for AI message adaptation"
    )
    contexts: List[StrObjectId] = Field(
        default_factory=list,
        description="Specific contexts for the launch"
    )

    @property
    def all_communications(self) -> List[LaunchScheduledCommunication]:
        """Get all communications including welcome kit"""
        comms = []
        if self.welcome_kit:
            comms.append(self.welcome_kit)
        comms.extend(self.pre_launch_communications)
        comms.extend(self.post_launch_attended_communications)
        comms.extend(self.post_launch_missed_communications)
        return comms

    def get_subscription_by_chat_id(self, chat_id: StrObjectId) -> Optional[LaunchSubscription]:
        """Find a subscription by chat ID"""
        for sub in self.subscriptions:
            if str(sub.chat_id) == str(chat_id):
                return sub
        return None

    def is_chat_subscribed(self, chat_id: StrObjectId) -> bool:
        """Check if a chat is subscribed to this launch"""
        sub = self.get_subscription_by_chat_id(chat_id)
        return sub is not None and sub.status in [
            LaunchSubscriptionStatus.SUBSCRIBED,
            LaunchSubscriptionStatus.ATTENDED
        ]

    def get_access_link_for_subscriber(self, chat_id: StrObjectId) -> str:
        """
        Returns the personal trackable link for a subscriber if tracking is enabled,
        otherwise returns the general access_link.
        """
        if self.enable_tracking:
            subscription = self.get_subscription_by_chat_id(chat_id)
            if subscription and subscription.personal_access_link:
                return subscription.personal_access_link
        return self.access_link

    def generate_personal_link(self, chat_id: StrObjectId) -> str:
        """
        Generates a unique trackable link for a given chat_id.
        Adds a 'subscriber' query parameter to the base access_link.
        """
        parsed_url = urlparse(self.access_link)
        query_params = parse_qs(parsed_url.query)
        query_params['subscriber'] = [str(chat_id)]
        new_query = urlencode(query_params, doseq=True)
        return urlunparse(parsed_url._replace(query=new_query))

