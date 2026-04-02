"""Shared ESI provider for Eve Universe."""

from esi.clients import EsiClientProvider

from . import __version__

esi = EsiClientProvider(app_info_text=f"django-eveuniverse v{__version__}")
