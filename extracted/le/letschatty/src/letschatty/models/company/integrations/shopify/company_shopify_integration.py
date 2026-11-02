from typing import List, Optional
from datetime import datetime
from zoneinfo import ZoneInfo
from pydantic import BaseModel, Field

class ShopifyWebhookSubscription(BaseModel):
    """Represents a single webhook subscription"""
    topic: str = Field(description="Webhook topic (e.g., 'products/create')")
    webhook_id: Optional[str] = Field(default=None, description="Shopify webhook ID")
    subscribed_at: datetime = Field(default_factory=lambda: datetime.now(tz=ZoneInfo("UTC")))
    is_active: bool = Field(default=True, description="Whether subscription is active")

class ShopifyIntegration(BaseModel):
    """Shopify integration for the company"""
    shopify_store_url: str = Field(default="")
    oauth_state: str = Field(default="")
    oauth_state_at: datetime = Field(default_factory=lambda: datetime.now(tz=ZoneInfo("UTC")))
    access_token: Optional[str] = Field(default=None)
    connected_at: Optional[datetime] = Field(default=None)
    scope: Optional[str] = Field(default=None)
    
    # Webhook subscriptions
    webhook_subscriptions: List[ShopifyWebhookSubscription] = Field(
        default_factory=list,
        description="List of active webhook subscriptions"
    )
    
    # Scheduled sync settings
    product_sync_enabled: bool = Field(
        default=False,
        description="Whether scheduled product sync is enabled"
    )
    product_sync_interval_hours: int = Field(
        default=24,
        description="Interval in hours for scheduled product sync"
    )
    last_product_sync_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp of last product sync"
    )
    
    @property
    def is_connected(self) -> bool:
        """Check if the integration is fully connected"""
        return bool(self.access_token and self.shopify_store_url)
    
    def get_subscribed_topics(self) -> List[str]:
        """Get list of currently subscribed webhook topics"""
        return [sub.topic for sub in self.webhook_subscriptions if sub.is_active]
    
    def reset(self) -> None:
        """Reset integration to disconnected state"""
        self.shopify_store_url = ""
        self.oauth_state = ""
        self.oauth_state_at = datetime.now(tz=ZoneInfo("UTC"))
        self.access_token = None
        self.connected_at = None
        self.scope = None
        self.webhook_subscriptions = []
        self.product_sync_enabled = False
        self.product_sync_interval_hours = 24
        self.last_product_sync_at = None