######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.37.2+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-08-28T18:11:58.458798                                                            #
######################################################################################################

from __future__ import annotations

import typing
import metaflow
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

def validate_kube_labels(labels: typing.Union[typing.Dict[str, typing.Union[str, None]], None]) -> bool:
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

