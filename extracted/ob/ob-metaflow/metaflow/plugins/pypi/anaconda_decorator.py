from .conda_decorator import CondaFlowDecorator, CondaStepDecorator


class AnacondaStepDecorator(CondaStepDecorator):
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
    extra_configs : Dict[str, str], default {}
        Additional key-value configuration passed through to the environment
        solver/builder. Merged with any ``extra_configs`` set in
        ``@anaconda_base``, with step-level values taking precedence.
    """

    name = "anaconda"
    defaults = {
        "packages": {},
        "python": None,
        "disabled": None,
        "channels": ["https://repo.anaconda.com/pkgs/main"],
        "extra_configs": {},
    }

    _flow_decorator_name = "anaconda_base"


class AnacondaFlowDecorator(CondaFlowDecorator):
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
    extra_configs : Dict[str, str], default {}
        Additional key-value configuration passed through to the environment
        solver/builder for all steps. Step-level ``@anaconda(extra_configs=...)``
        values take precedence on key conflicts.
    """

    name = "anaconda_base"
    defaults = {
        "packages": {},
        "python": None,
        "disabled": None,
        "channels": ["https://repo.anaconda.com/pkgs/main"],
        "extra_configs": {},
    }

    _step_decorator_name = "anaconda"
