######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.923105                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.decorators

from ...metaflow_current import current as current
from ...user_configs.config_options import ConfigInput as ConfigInput
from ...user_configs.config_parameters import dump_config_values as dump_config_values
from .component_serializer import CardComponentCollector as CardComponentCollector
from .component_serializer import get_card_class as get_card_class
from .card_creator import CardCreator as CardCreator

TYPE_CHECK_REGEX: str

ASYNC_TIMEOUT: int

def warning_message(message, logger = None, ts = False):
    ...

class CardDecorator(metaflow.decorators.StepDecorator, metaclass=type):
    """
    Creates a human-readable report, a Metaflow Card, after this step completes.
    
    Note that you may add multiple `@card` decorators in a step with different parameters.
    
    Parameters
    ----------
    type : str, default 'default'
        Card type.
    id : str, optional, default None
        If multiple cards are present, use this id to identify this card.
    options : Dict[str, Any], default {}
        Options passed to the card. The contents depend on the card type.
    timeout : int, default 45
        Interrupt reporting if it takes more than this many seconds.
    
    MF Add To Current
    -----------------
    card -> metaflow.plugins.cards.component_serializer.CardComponentCollector
        The `@card` decorator makes the cards available through the `current.card`
        object. If multiple `@card` decorators are present, you can add an `ID` to
        distinguish between them using `@card(id=ID)` as the decorator. You will then
        be able to access that specific card using `current.card[ID].
    
        Methods available are `append` and `extend`
    
        @@ Returns
        -------
        CardComponentCollector
            The or one of the cards attached to this step.
    """
    def __init__(self, *args, **kwargs):
        ...
    def step_init(self, flow, graph, step_name, decorators, environment, flow_datastore, logger):
        ...
    def task_pre_step(self, step_name, task_datastore, metadata, run_id, task_id, flow, graph, retry_count, max_user_code_retries, ubf_context, inputs):
        ...
    def task_finished(self, step_name, flow, graph, is_task_ok, retry_count, max_user_code_retries):
        ...
    def task_exception(self, exception, step_name, flow, graph, retry_count, max_user_code_retries):
        ...
    ...

