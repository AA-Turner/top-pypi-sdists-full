######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.928019                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

from ...exception import CommandException as CommandException
from ...exception import MetaflowException as MetaflowException

class KubernetesException(metaflow.exception.MetaflowException, metaclass=type):
    ...

def parse_cli_options(flow_name, run_id, user, my_runs, echo):
    ...

def qos_requests_and_limits(qos: str, cpu: int, memory: int, storage: int):
    """
    return resource requests and limits for the kubernetes pod based on the given QoS Class
    """
    ...

def validate_kube_labels(labels: typing.Optional[typing.Dict[str, typing.Optional[str]]]) -> bool:
    """
    Validate label values.
    
    This validates the kubernetes label values.  It does not validate the keys.
    Ideally, keys should be static and also the validation rules for keys are
    more complex than those for values.  For full validation rules, see:
    
    https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#syntax-and-character-set
    """
    ...

def parse_kube_keyvalue_list(items: typing.List[str], requires_both: bool = True):
    ...

