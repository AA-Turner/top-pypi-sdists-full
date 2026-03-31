######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.21.1+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-03-31T03:38:01.600723                                                            #
######################################################################################################

from __future__ import annotations

import typing

from .exceptions import TorchrunException as TorchrunException
from .exceptions import TorchNotInstalledException as TorchNotInstalledException
from .datastore import TorchrunDatastore as TorchrunDatastore
from .status_notifier import TaskStatusNotifier as TaskStatusNotifier
from .status_notifier import wait_for_task_completion as wait_for_task_completion
from .status_notifier import TaskFailedException as TaskFailedException
from .....exception import MetaflowException as MetaflowException

class TorchrunExecutor(object, metaclass=type):
    """
    Instances of the TorchrunExecutor class are used to run the torchrun command.
    There is one per Metaflow @step annotated with @torchrun.
    
    TorchrunExecutor takes in information about this run based on the Metaflow config,
    so users declare the infrastructure Metaflow dynamically spins up for them in one place,
    and then the TorchrunExecutor uses that information to configure the distributed parts of the torchrun command accordingly.
    
    The Torchrun decorator, which users specify in a Metaflow num_parallel task with @torchrun, attaches an instance of this class to the current object.
    Using current.torch.run() will then run the torchrun command with the appropriate arguments.
    
    This class will handle opening the subprocess, and ensuring other typical Metaflow functionality works as expected.
    """
    def __init__(self, pathspec, main_addr, main_port, num_nodes, node_index, nproc_per_node = 1, flow_datastore = None):
        ...
    def run(self, torchrun_args: typing.Union[typing.List[str], typing.Dict[str, str]] = {}, entrypoint: str = None, entrypoint_args: typing.Union[typing.List[str], typing.Dict[str, str]] = {}, nproc_per_node: int = None, push_results_dir_to_cloud: bool = False, local_output_dir: str = None, cloud_output_dir: str = None) -> typing.Optional[str]:
        ...
    ...

class TorchrunSingleNodeMultiGPU(object, metaclass=type):
    """
    A slimmed down version of TorchrunExecutor, to be exposed to Metaflow user code for single node, multi-gpu use cases.
    """
    def __init__(self):
        ...
    def run(self, torchrun_args: typing.Union[typing.List[str], typing.Dict[str, str]] = [], entrypoint: str = None, entrypoint_args: typing.Union[typing.List[str], typing.Dict[str, str]] = [], nproc_per_node: int = None) -> typing.Optional[str]:
        ...
    ...

