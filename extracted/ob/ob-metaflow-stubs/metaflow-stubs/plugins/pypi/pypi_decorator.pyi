######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.17.1.0+obcheckpoint(0.2.4);ob(v1)                                                    #
# Generated on 2025-08-21T23:31:59.757385                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.decorators


class PyPIStepDecorator(metaflow.decorators.StepDecorator, metaclass=type):
    """
    Specifies the PyPI packages for the step.
    
    Information in this decorator will augment any
    attributes set in the `@pyi_base` flow-level decorator. Hence,
    you can use `@pypi_base` to set packages required by all
    steps and use `@pypi` to specify step-specific overrides.
    
    Parameters
    ----------
    packages : Dict[str, str], default: {}
        Packages to use for this step. The key is the name of the package
        and the value is the version to use.
    python : str, optional, default: None
        Version of Python to use, e.g. '3.7.4'. A default value of None implies
        that the version used will correspond to the version of the Python interpreter used to start the run.
    """
    def __init__(self, attributes = None, statically_defined = False, inserted_by = None):
        ...
    def step_init(self, flow, graph, step, decos, environment, flow_datastore, logger):
        ...
    def is_attribute_user_defined(self, name):
        ...
    ...

class PyPIFlowDecorator(metaflow.decorators.FlowDecorator, metaclass=type):
    """
    Specifies the PyPI packages for all steps of the flow.
    
    Use `@pypi_base` to set common packages required by all
    steps and use `@pypi` to specify step-specific overrides.
    Parameters
    ----------
    packages : Dict[str, str], default: {}
        Packages to use for this flow. The key is the name of the package
        and the value is the version to use.
    python : str, optional, default: None
        Version of Python to use, e.g. '3.7.4'. A default value of None implies
        that the version used will correspond to the version of the Python interpreter used to start the run.
    """
    def __init__(self, attributes = None, statically_defined = False, inserted_by = None):
        ...
    def flow_init(self, flow, graph, environment, flow_datastore, metadata, logger, echo, options):
        ...
    ...

