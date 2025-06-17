######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.938894                                                            #
######################################################################################################

from __future__ import annotations

import threading
import metaflow
import typing
if typing.TYPE_CHECKING:
    import threading
    import metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastructures
    import metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.card_utils.async_cards

from ...card_utils.deco_injection_mixin import CardDecoratorInjector as CardDecoratorInjector
from ...card_utils.async_cards import CardRefresher as CardRefresher
from ...card_utils.async_cards import AsyncPeriodicRefresher as AsyncPeriodicRefresher
from ...card_utils.extra_components import LineChart as LineChart
from ...card_utils.extra_components import UpadateableTable as UpadateableTable
from ...datastructures import CheckpointArtifact as CheckpointArtifact
from .lineage_card import construct_lineage_table as construct_lineage_table
from .lineage_card import create_checkpoint_card as create_checkpoint_card
from .lineage_card import null_card as null_card
from .lineage_card import format_datetime as format_datetime
from ...utils.general import unit_convert as unit_convert
from .......plugins.cards.card_modules.components import Markdown as Markdown
from .......plugins.cards.card_modules.components import Table as Table
from .......plugins.cards.card_modules.components import Artifact as Artifact
from .......plugins.cards.card_modules.components import VegaChart as VegaChart

def human_readable_date(date):
    ...

def determine_nice_value(time_range_seconds):
    """
    Function to determine the 'nice' value based on the time range in seconds.
    """
    ...

def generate_vega_timeline(data_objects):
    ...

class CheckpointListRefresher(metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.card_utils.async_cards.CardRefresher, metaclass=type):
    def __init__(self, loaded_checkpoint: typing.Optional[metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastructures.CheckpointArtifact], lineage_stack: typing.Optional[typing.List[metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastructures.CheckpointArtifact]], load_policy: str):
        ...
    def on_error(self, current_card, error_message):
        ...
    def on_startup(self, current_card):
        ...
    def first_time_render(self, current_card, data_object, force_refresh = False):
        ...
    def data_update(self, current_card, data_object):
        ...
    def on_update(self, current_card, data_object):
        ...
    def on_final(self, current_card, data_object):
        ...
    ...

class CheckpointsCollector(threading.Thread, metaclass=type):
    def __init__(self, refresher: metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.card_utils.async_cards.CardRefresher, interval = 1):
        ...
    def collect(self):
        ...
    def final_update(self):
        ...
    def run_update(self):
        ...
    def run(self):
        ...
    def stop(self):
        ...
    ...

