######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.884490                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.mf_extensions.outerbounds.plugins.card_utilities.async_cards

from .....plugins.cards.card_modules.components import Markdown as Markdown
from .....plugins.cards.card_modules.components import Table as Table
from .....plugins.cards.card_modules.components import VegaChart as VegaChart
from .....metaflow_current import current as current
from ..card_utilities.async_cards import CardRefresher as CardRefresher

class OllamaStatusCard(metaflow.mf_extensions.outerbounds.plugins.card_utilities.async_cards.CardRefresher, metaclass=type):
    """
    Real-time status card for Ollama system monitoring.
    Shows circuit breaker state, server health, model status, and recent events.
    """
    def __init__(self, refresh_interval = 10):
        ...
    def update_status(self, category, data):
        """
        Thread-safe method to update status data
        """
        ...
    def add_event(self, event_type, message, timestamp = None):
        """
        Add an event to the timeline
        """
        ...
    def get_circuit_breaker_emoji(self, state):
        """
        Get status emoji for circuit breaker state
        """
        ...
    def get_uptime_string(self, start_time):
        """
        Calculate uptime string
        """
        ...
    def on_startup(self, current_card):
        """
        Initialize the card when monitoring starts
        """
        ...
    def render_card_fresh(self, current_card, data):
        """
        Render the complete card with all status information
        """
        ...
    def on_error(self, current_card, error_message):
        """
        Handle errors in card rendering
        """
        ...
    def on_update(self, current_card, data_object):
        """
        Update the card with new data
        """
        ...
    def sqlite_fetch_func(self, conn):
        """
        Required by CardRefresher (which needs a refactor), but we use in-memory data instead
        """
        ...
    ...

