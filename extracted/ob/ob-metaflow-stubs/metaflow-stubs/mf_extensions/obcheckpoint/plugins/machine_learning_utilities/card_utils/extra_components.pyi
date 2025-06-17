######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:03.004026                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.cards.card_modules.components
    import metaflow.plugins.cards.card_modules.card

from ......plugins.cards.card_modules.components import VegaChart as VegaChart
from ......plugins.cards.card_modules.card import MetaflowCardComponent as MetaflowCardComponent
from ......plugins.cards.card_modules.components import Artifact as Artifact
from ......plugins.cards.card_modules.components import Table as Table
from ......plugins.cards.card_modules.card import with_default_component_id as with_default_component_id
from ......plugins.cards.card_modules.convert_to_native_type import TaskToDict as TaskToDict
from ......plugins.cards.card_modules.basic import ArtifactsComponent as ArtifactsComponent
from ......plugins.cards.card_modules.components import UserComponent as UserComponent
from ......plugins.cards.card_modules.basic import TableComponent as TableComponent
from ......plugins.cards.card_modules.basic import SectionComponent as SectionComponent
from ......plugins.cards.card_modules.renderer_tools import render_safely as render_safely
from ......metaflow_current import current as current

def update_spec_data(spec, data):
    ...

def update_data_object(data_object, data):
    ...

def line_chart_spec(title = None, x_name = 'u', y_name = 'v', xtitle = None, ytitle = None, width = 600, height = 400, with_params = True, x_axis_temporal = False):
    ...

class LineChart(metaflow.plugins.cards.card_modules.components.UserComponent, metaclass=type):
    def __init__(self, title, xtitle, ytitle, x_name, y_name, with_params = False, x_axis_temporal = False, width = None, height = None):
        ...
    def update(self, data):
        ...
    def render(self, *args, **kwargs):
        ...
    ...

class ArtifactTable(metaflow.plugins.cards.card_modules.components.Artifact, metaclass=type):
    def __init__(self, data_dict):
        ...
    def render(self, *args, **kwargs):
        ...
    ...

class UpadateableTable(metaflow.plugins.cards.card_modules.components.UserComponent, metaclass=type):
    """
    Parameters
    ----------
    data : List[List[str or MetaflowCardComponent]], optional
        List (rows) of lists (columns). Each item can be a string or a `MetaflowCardComponent`.
    headers : List[str], optional
        Optional header row for the table.
    """
    def update(self, row: typing.List[typing.Union[str, metaflow.plugins.cards.card_modules.card.MetaflowCardComponent]]):
        ...
    def __init__(self, data: typing.Optional[typing.List[typing.List[typing.Union[str, metaflow.plugins.cards.card_modules.card.MetaflowCardComponent]]]] = None, headers: typing.Optional[typing.List[str]] = None, disable_updates: bool = False):
        ...
    def render(self, *args, **kwargs):
        ...
    ...

