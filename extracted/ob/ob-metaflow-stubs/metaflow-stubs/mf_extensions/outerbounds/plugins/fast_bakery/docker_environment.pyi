######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.21.1+obcheckpoint(0.2.4);ob(v1)                                                   #
# Generated on 2025-07-11T23:29:18.564092                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception
    import metaflow.metaflow_environment

from .....exception import MetaflowException as MetaflowException
from .....metaflow_config import get_pinned_conda_libs as get_pinned_conda_libs
from .....plugins.aws.batch.batch_decorator import BatchDecorator as BatchDecorator
from .....plugins.kubernetes.kubernetes_decorator import KubernetesDecorator as KubernetesDecorator
from .....plugins.pypi.conda_decorator import CondaStepDecorator as CondaStepDecorator
from .....plugins.pypi.conda_environment import CondaEnvironment as CondaEnvironment
from .....plugins.pypi.pypi_decorator import PyPIStepDecorator as PyPIStepDecorator
from .fast_bakery import FastBakery as FastBakery
from .fast_bakery import FastBakeryApiResponse as FastBakeryApiResponse
from .fast_bakery import FastBakeryException as FastBakeryException

FAST_BAKERY_URL: None

BAKERY_METAFILE: str

def cache_request(cache_file):
    ...

class DockerEnvironmentException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, msg):
        ...
    ...

class DockerEnvironment(metaflow.metaflow_environment.MetaflowEnvironment, metaclass=type):
    def __init__(self, flow):
        ...
    def set_local_root(self, local_root):
        ...
    def decospecs(self):
        ...
    def validate_environment(self, logger, datastore_type):
        ...
    def init_environment(self, echo):
        ...
    def executable(self, step_name, default = None):
        ...
    def interpreter(self, step_name):
        ...
    def is_disabled(self, step):
        ...
    def pylint_config(self):
        ...
    def get_package_commands(self, codepackage_url, datastore_type):
        ...
    def bootstrap_commands(self, step_name, datastore_type):
        ...
    ...

def get_fastbakery_metafile_path(local_root, flow_name):
    ...

