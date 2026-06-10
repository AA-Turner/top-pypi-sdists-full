######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.33.1+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-06-09T20:21:00.289020                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.pypi.conda_decorator

from .conda_decorator import CondaFlowDecorator as CondaFlowDecorator
from .conda_decorator import CondaStepDecorator as CondaStepDecorator

class AnacondaStepDecorator(metaflow.plugins.pypi.conda_decorator.CondaStepDecorator, metaclass=type):
    """
    Specifies the Anaconda environment for the step.
    
    Identical to ``@conda`` but defaults to the ``anaconda`` channel
    instead of the globally configured channel (typically ``conda-forge``).
    
    Information in this decorator will augment any
    attributes set in the ``@anaconda_base`` flow-level decorator. Hence,
    you can use ``@anaconda_base`` to set packages required by all
    steps and use ``@anaconda`` to specify step-specific overrides.
    
    Parameters
    ----------
    packages : Dict[str, str], default {}
        Packages to use for this step. The key is the name of the package
        and the value is the version to use.
    python : str, optional, default None
        Version of Python to use, e.g. '3.7.4'. A default value of None implies
        that the version used will correspond to the version of the Python interpreter used to start the run.
    disabled : bool, default False
        If set to True, disables @anaconda.
    channels : List[str], default ["https://repo.anaconda.com/pkgs/main"]
        Conda channels to use for package resolution.
    """
    ...

class AnacondaFlowDecorator(metaflow.plugins.pypi.conda_decorator.CondaFlowDecorator, metaclass=type):
    """
    Specifies the Anaconda environment for all steps of the flow.
    
    Identical to ``@conda_base`` but defaults to the ``anaconda`` channel
    instead of the globally configured channel (typically ``conda-forge``).
    
    Use ``@anaconda_base`` to set common libraries required by all
    steps and use ``@anaconda`` to specify step-specific additions.
    
    Parameters
    ----------
    packages : Dict[str, str], default {}
        Packages to use for this flow. The key is the name of the package
        and the value is the version to use.
    python : str, optional, default None
        Version of Python to use, e.g. '3.7.4'. A default value of None implies
        that the version used will correspond to the version of the Python interpreter used to start the run.
    disabled : bool, default False
        If set to True, disables Anaconda.
    channels : List[str], default ["anaconda"]
        Conda channels to use for package resolution.
    """
    ...

