######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.853386                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.mf_extensions.outerbounds.plugins.card_utilities.injector
    import metaflow.decorators

from ...metaflow_current import current as current
from ...mf_extensions.outerbounds.plugins.ollama import constants as constants
from ...mf_extensions.outerbounds.plugins.ollama import exceptions as exceptions
from ...mf_extensions.outerbounds.plugins.ollama import ollama as ollama
from ...mf_extensions.outerbounds.plugins.ollama.ollama import OllamaManager as OllamaManager
from ...mf_extensions.outerbounds.plugins.ollama.ollama import OllamaRequestInterceptor as OllamaRequestInterceptor
from ...mf_extensions.outerbounds.plugins.ollama import status_card as status_card
from ...mf_extensions.outerbounds.plugins.ollama.status_card import OllamaStatusCard as OllamaStatusCard
from ...mf_extensions.outerbounds.plugins.card_utilities.injector import CardDecoratorInjector as CardDecoratorInjector

class OllamaDecorator(metaflow.decorators.StepDecorator, metaflow.mf_extensions.outerbounds.plugins.card_utilities.injector.CardDecoratorInjector, metaclass=type):
    """
    This decorator is used to run Ollama APIs as Metaflow task sidecars.
    
    User code call
    --------------
    @ollama(
        models=[...],
        ...
    )
    
    Valid backend options
    ---------------------
    - 'local': Run as a separate process on the local task machine.
    - (TODO) 'managed': Outerbounds hosts and selects compute provider.
    - (TODO) 'remote': Spin up separate instance to serve Ollama models.
    
    Valid model options
    -------------------
    Any model here https://ollama.com/search, e.g. 'llama3.2', 'llama3.3'
    
    Parameters
    ----------
    models: list[str]
        List of Ollama containers running models in sidecars.
    backend: str
        Determines where and how to run the Ollama process.
    force_pull: bool
        Whether to run `ollama pull` no matter what, or first check the remote cache in Metaflow datastore for this model key.
    cache_update_policy: str
        Cache update policy: "auto", "force", or "never".
    force_cache_update: bool
        Simple override for "force" cache update policy.
    debug: bool
        Whether to turn on verbose debugging logs.
    circuit_breaker_config: dict
        Configuration for circuit breaker protection. Keys: failure_threshold, recovery_timeout, reset_timeout.
    timeout_config: dict
        Configuration for various operation timeouts. Keys: pull, stop, health_check, install, server_startup.
    """
    def step_init(self, flow, graph, step_name, decorators, environment, flow_datastore, logger):
        ...
    def task_decorate(self, step_func, flow, graph, retry_count, max_user_code_retries, ubf_context):
        ...
    ...

