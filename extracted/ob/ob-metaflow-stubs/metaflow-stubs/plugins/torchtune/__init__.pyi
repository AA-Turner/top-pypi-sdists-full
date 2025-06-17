######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.855274                                                            #
######################################################################################################

from __future__ import annotations

import typing

from ...metaflow_current import current as current

class TorchTune(object, metaclass=type):
    def __init__(self, use_multi_node_config: bool = False):
        """
        Initialize the Tune launcher.
        
        :param use_multi_node_config: If True, attempt to build a distributed configuration
                                      from current.torch.torchrun_args.
        """
        ...
    def run(self, recipe: str, config_dict: typing.Dict, additional_cli_options: typing.Optional[typing.List[str]] = None):
        """
        Launch the torchtune job via its CLI.
        
        :param recipe: The path to the recipe (or name of the recipe) to run.
        :param config_dict: Optional dictionary that will be dumped to a YAML file and passed via --config.
        :param additional_cli_options: Optional list of additional CLI options.
        :raises: subprocess.CalledProcessError if the subprocess returns a nonzero exit code.
        """
        ...
    ...

def enqueue_output(file, queue):
    ...

def read_popen_pipes(p):
    ...

