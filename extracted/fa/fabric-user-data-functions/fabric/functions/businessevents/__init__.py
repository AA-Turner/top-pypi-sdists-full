# flake8: noqa: F401

from .fabric_business_events import FabricBusinessEventsClient
from .business_events_provider import BusinessEventsClientProvider
from fabric.internal.providers import ProviderFactory

# Auto-register the provider when this module is imported
ProviderFactory.register_provider(FabricBusinessEventsClient, BusinessEventsClientProvider)

__all__ = ['FabricBusinessEventsClient']