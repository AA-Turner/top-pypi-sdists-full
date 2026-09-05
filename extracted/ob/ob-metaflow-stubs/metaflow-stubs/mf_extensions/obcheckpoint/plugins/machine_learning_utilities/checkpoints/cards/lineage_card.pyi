######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.37.3+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-09-04T19:03:46.161939                                                            #
######################################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.cards.card_modules.card

from .......plugins.cards.card_modules.components import Table as Table
from .......plugins.cards.card_modules.components import Markdown as Markdown
from .......plugins.cards.card_modules.card import MetaflowCardComponent as MetaflowCardComponent
from .......plugins.cards.card_modules.components import Artifact as Artifact
from .......plugins.cards.card_modules.basic import DagComponent as DagComponent
from .......plugins.cards.card_modules.basic import SectionComponent as SectionComponent

TYPE_CHECKING: bool

def format_datetime(iso_str):
    ...

def null_card(load_policy):
    ...

def construct_lineage_table(lineage):
    ...

def create_checkpoint_card(loaded_checkpoint: "Checkpoint", checkpoint_lineage: typing.List["Checkpoint"], load_policy: str) -> typing.List[metaflow.plugins.cards.card_modules.card.MetaflowCardComponent]:
    ...

