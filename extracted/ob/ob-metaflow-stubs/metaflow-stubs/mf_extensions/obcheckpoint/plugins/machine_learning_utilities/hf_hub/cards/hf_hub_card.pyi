######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.34.1+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-06-18T13:29:50.560456                                                            #
######################################################################################################

from __future__ import annotations

import threading
import typing
import metaflow
if typing.TYPE_CHECKING:
    import metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.card_utils.async_cards
    import threading

from ...card_utils.async_cards import CardRefresher as CardRefresher
from ...card_utils.extra_components import UpadateableTable as UpadateableTable
from ...utils.general import unit_convert as unit_convert
from .......plugins.cards.card_modules.components import Markdown as Markdown
from .......plugins.cards.card_modules.components import Table as Table
from .......plugins.cards.card_modules.components import Artifact as Artifact

def format_datetime(iso_str):
    ...

class HuggingfaceHubListRefresher(metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.card_utils.async_cards.CardRefresher, metaclass=type):
    """
    Card refresher for Hugging Face Hub models
    """
    def __init__(self, loaded_models_data: typing.Dict[str, typing.Dict], cache_scope: str):
        ...
    def on_error(self, current_card, error_message):
        ...
    def on_startup(self, current_card):
        """
        Initialize the card on startup
        """
        ...
    def first_time_render(self, current_card, data_object, force_refresh = False):
        """
        Render the card for the first time with runtime data
        """
        ...
    def data_update(self, current_card, data_object):
        """
        Update the card with new runtime data
        """
        ...
    def on_update(self, current_card, data_object):
        """
        Handle card updates
        """
        ...
    def on_final(self, current_card, data_object):
        """
        Handle final card update
        """
        ...
    ...

class HuggingfaceHubCollector(threading.Thread, metaclass=type):
    """
    Thread to collect Hugging Face Hub model tracking data
    """
    def __init__(self, refresher: metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.card_utils.async_cards.CardRefresher, interval = 1):
        ...
    def collect(self):
        """
        Collect runtime model tracking data
        """
        ...
    def final_update(self):
        """
        Perform final update before thread exits
        """
        ...
    def run_update(self):
        """
        Perform periodic update
        """
        ...
    def run(self):
        """
        Main thread loop
        """
        ...
    def stop(self):
        """
        Stop the collector thread
        """
        ...
    ...

