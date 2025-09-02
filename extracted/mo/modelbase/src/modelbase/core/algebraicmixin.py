from __future__ import annotations

__all__ = [
    "AlgebraicModule",
    "Module",
]

import copy
import warnings
from dataclasses import dataclass, field
from queue import Empty, SimpleQueue
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Iterable,
    Iterator,
)

import numpy as np
from typing_extensions import Self

from .basemodel import BaseModel
from .compoundmixin import CompoundMixin
from .parametermixin import ParameterMixin
from .utils import (
    _sort_dependencies_multiple,
    check_function_arity,
    get_formatted_function_source_code,
    patch_lambda_function_name,
    warning_on_one_line,
)

if TYPE_CHECKING:
    import libsbml

    from modelbase.typing import Array

warnings.formatwarning = warning_on_one_line  # type: ignore


@dataclass
class Module:
    """Meta-info container for an algebraic module."""

    common_name: str | None = None
    notes: dict = field(default_factory=dict)
    database_links: dict = field(default_factory=dict)


@dataclass
class AlgebraicCache:
    module_order: list[str]


class AlgebraicModule:
    """Container for algebraic modules"""

    def __init__(
        self,
        name: str,
        function: Callable[..., float] | Callable[..., Iterable[float]],
        derived_compounds: list[str],
        compounds: list[str],
        modifiers: list[str],
        parameters: list[str],
        dynamic_variables: list[str],
        args: list[str],
    ) -> None:
        self.name = name
        self.function = function
        self.compounds = compounds
        self.derived_compounds = derived_compounds
        self.modifiers = modifiers
        self.parameters = parameters
        self.dynamic_variables = dynamic_variables
        self.args = args

    def check_consistency(self) -> None:
        """Check whether all arguments exists and the arity matches"""
        self._check_dynamic_variables()
        self._check_module_args()

        if not check_function_arity(function=self.function, arity=len(self.args)):
            warnings.warn(f"Function arity does not match args of {self.name}")

    def _check_dynamic_variables(self) -> None:
        difference = set(self.dynamic_variables).difference(
            self.compounds + self.modifiers
        )
        if difference:
            warnings.warn(
                f"Supplied args {difference} for module {self.name} that aren't in compounds or modifiers"
            )

    def _check_module_args(self) -> None:
        difference = set(self.args).difference(self.dynamic_variables + self.parameters)
        if difference:
            warnings.warn(
                f"Supplied args {difference} for module {self.name} that aren't in compounds, modifiers or parameters"
            )

    def __repr__(self) -> str:
        return repr(self.__dict__)

    def __str__(self) -> str:
        return f"{self.function.__name__}({', '.join(self.args)}) -> {self.derived_compounds}"

    def keys(self) -> list[str]:
        """Get all valid keys of the algebraic module"""
        return [
            "function",
            "compounds",
            "derived_compounds",
            "modifiers",
            "parameters",
            "dynamic_variables",
            "args",
        ]

    def __getitem__(self, key: str) -> Any:
        return self.__dict__[key]

    def __iter__(self) -> Iterator:
        yield "function", self.function
        yield "compounds", self.compounds
        yield "derived_compounds", self.derived_compounds
        yield "modifiers", self.modifiers
        yield "parameters", self.parameters
        yield "dynamic_variables", self.dynamic_variables
        yield "args", self.args

    def copy(self) -> AlgebraicModule:
        """Create a copy of the module"""
        return copy.deepcopy(self)


@dataclass
class Readout:
    function: Callable[..., float]
    args: list[str]


class AlgebraicMixin(ParameterMixin, CompoundMixin, BaseModel):
    """Mixin for algebraic modules.

    This adds the capability to calculate concentrations of derived
    compounds that are calculated before the rate functions are calculated.
    """

    def __init__(
        self, algebraic_modules: dict[str, dict[str, Any]] | None = None
    ) -> None:
        self.algebraic_modules: dict[str, AlgebraicModule] = {}
        self.readouts: dict[str, Readout] = {}
        if algebraic_modules is not None:
            self.add_algebraic_modules(algebraic_modules=algebraic_modules)
        self._algebraic_cache: AlgebraicCache | None = None

    def _make_algebraic_cache(self) -> AlgebraicCache:
        self._algebraic_cache = AlgebraicCache(
            module_order=_sort_dependencies_multiple(
                available=set(self.get_all_parameter_names())
                ^ set(self.get_compounds())
                ^ {"time"},
                elements=[
                    (k, v.derived_compounds, set(v.args))
                    for k, v in self.algebraic_modules.items()
                ],
            )
        )
        return self._algebraic_cache

    @property
    def _algebraic_module_order(self) -> list[str]:
        cache = (
            self._make_algebraic_cache()
            if self._algebraic_cache is None
            else self._algebraic_cache
        )

        return cache.module_order

    ##########################################################################
    # Derived compound functions
    ##########################################################################

    def get_derived_compounds(self) -> list[str]:
        """Return names of compounds derived from algebraic modules."""
        derived_compounds = []
        for name in self._algebraic_module_order:
            derived_compounds.extend(self.algebraic_modules[name].derived_compounds)
        return derived_compounds

    @property
    def derived_compounds(self) -> list[str]:
        """Return names of compounds derived from algebraic modules

        Used to be an attribute of the model, so this is kept to ensure backwards compatability
        """
        return self.get_derived_compounds()

    def _get_all_compounds(self) -> list[str]:
        return list(self.get_compounds() + self.get_derived_compounds())

    def get_all_compounds(self) -> list[str]:
        """Return names of compounds and derived compounds (in that order)."""
        return self._get_all_compounds()

    ##########################################################################
    # Algebraic Modules
    ##########################################################################

    def _check_module_consistency(
        self, module: AlgebraicModule, check_ids: bool = True
    ) -> None:
        if check_ids:
            self._check_and_insert_ids(module.derived_compounds, context=module.name)
        module.check_consistency()

    def add_algebraic_module(
        self,
        module_name: str,
        function: Callable[..., float] | Callable[..., Iterable[float]],
        compounds: list[str] | None = None,
        derived_compounds: list[str] | None = None,
        modifiers: list[str] | None = None,
        parameters: list[str] | None = None,
        dynamic_variables: list[str] | None = None,
        args: list[str] | None = None,
        check_consistency: bool = True,
        **meta_info: dict[str, Any],
    ) -> Self:
        """Add an algebraic module to the model.

        CAUTION: The Python function of the module has to return an iterable.
        The Python function will get the function arguments in the following order:
        [**compounds, **modifiers, **parameters]

        Warns:
        -----
        UserWarning
            If algebraic module is already in the model.

        Examples:
        --------
        def rapid_equilibrium(substrate, k_eq)-> None:
            x = substrate / (1 + k_eq)
            y = substrate * k_eq / (1 + k_eq)
            return x, y

        add_algebraic_module(
            module_name="fast_eq",
            function=rapid_equilibrium,
            compounds=["A"],
            derived_compounds=["X", "Y"],
            parameters=["K"],
        )

        """
        self._algebraic_cache = None

        if module_name in self.algebraic_modules:
            self.remove_algebraic_module(module_name=module_name)
            warnings.warn(f"Overwriting algebraic module {module_name}")

        patch_lambda_function_name(function=function, name=module_name)

        if compounds is None:
            compounds = []
        if derived_compounds is None:
            derived_compounds = []
        if modifiers is None:
            modifiers = []
        if parameters is None:
            parameters = []
        if dynamic_variables is None:
            dynamic_variables = compounds + modifiers
        if args is None:
            args = dynamic_variables + parameters

        module = AlgebraicModule(
            name=module_name,
            function=function,
            compounds=compounds,
            derived_compounds=derived_compounds,
            modifiers=modifiers,
            parameters=parameters,
            dynamic_variables=dynamic_variables,
            args=args,
        )
        self.algebraic_modules[module_name] = module

        self.meta_info.setdefault("modules", {}).setdefault(
            module_name,
            Module(**meta_info),  # type: ignore
        )

        if check_consistency:
            self._check_module_consistency(module)

        return self

    def add_algebraic_module_from_args(
        self,
        module_name: str,
        function: Callable[..., float] | Callable[..., Iterable[float]],
        derived_compounds: list[str],
        args: list[str],
        check_consistency: bool = True,
        **meta_info: dict[str, Any],
    ) -> Self:
        compounds = []
        modifiers = []
        parameters = []

        param_names = self.get_all_parameter_names()
        for i in args:
            if i in param_names:
                parameters.append(i)
            elif i in self.compounds:
                compounds.append(i)
            else:
                modifiers.append(i)

        self.add_algebraic_module(
            module_name=module_name,
            function=function,
            compounds=compounds,
            derived_compounds=derived_compounds,
            modifiers=modifiers,
            parameters=parameters,
            dynamic_variables=None,
            args=args,
            check_consistency=check_consistency,
            **meta_info,
        )
        return self

    def add_derived_compound(
        self,
        name: str,
        function: Callable[..., float],
        args: list[str],
        check_consistency: bool = True,
    ) -> Self:
        """Shortcut function for adding algebraic module that only contains a single derived compound"""
        self.add_algebraic_module_from_args(
            module_name=name,
            function=function,
            derived_compounds=[name],
            args=args,
            check_consistency=check_consistency,
        )
        return self

    def add_algebraic_modules(
        self, algebraic_modules: dict, meta_info: dict | None = None
    ) -> Self:
        """Add multiple algebraic modules to the model.

        See Also
        --------
        add_algebraic_module

        """
        meta_info = {} if meta_info is None else meta_info
        for module_name, module in algebraic_modules.items():
            info = meta_info.get(module_name, {})
            self.add_algebraic_module(module_name=module_name, **module, **info)
        return self

    def update_algebraic_module(
        self,
        module_name: str,
        function: Callable[..., float] | Callable[..., Iterable[float]] | None = None,
        compounds: list[str] | None = None,
        derived_compounds: list[str] | None = None,
        modifiers: list[str] | None = None,
        parameters: list[str] | None = None,
        dynamic_variables: list[str] | None = None,
        args: list[str] | None = None,
        check_consistency: bool = True,
        **meta_info: dict[str, Any],
    ) -> Self:
        """Update an existing reaction."""
        self._algebraic_cache = None

        module = self.algebraic_modules[module_name]
        args_have_changed = False
        derived_have_changed = False

        if function is not None:
            patch_lambda_function_name(function=function, name=module_name)
            module.function = function

        if compounds is not None:
            module.compounds = compounds
            args_have_changed = True
        else:
            compounds = module.compounds

        if derived_compounds is not None:
            self._remove_ids(module.derived_compounds)
            module.derived_compounds = derived_compounds
            derived_have_changed = True

        if modifiers is not None:
            module.modifiers = modifiers
            args_have_changed = True
        else:
            modifiers = module.modifiers

        if parameters is not None:
            module.parameters = parameters
            args_have_changed = True
        else:
            parameters = module.parameters

        if dynamic_variables is not None:
            args_have_changed = True
            module.dynamic_variables = dynamic_variables
        elif args_have_changed:
            dynamic_variables = compounds + modifiers
            module.dynamic_variables = dynamic_variables
        else:
            dynamic_variables = module.dynamic_variables

        if args is not None:
            dynamic_variables = [i for i in args if i in module.dynamic_variables]
            module.dynamic_variables = dynamic_variables
            module.args = args
        elif args_have_changed:
            args = dynamic_variables + parameters
            module.args = args
        else:
            args = module.args

        if check_consistency:
            self._check_module_consistency(module, check_ids=derived_have_changed)

        self.update_meta_info("modules", meta_info)
        return self

    def update_algebraic_module_from_args(
        self,
        module_name: str,
        function: Callable[..., float] | Callable[..., Iterable[float]] | None = None,
        derived_compounds: list[str] | None = None,
        args: list[str] | None = None,
        check_consistency: bool = True,
        **meta_info: dict[str, Any],
    ) -> Self:
        if args is None:
            compounds = self.algebraic_modules[module_name].compounds
            modifiers = self.algebraic_modules[module_name].modifiers
            parameters = self.algebraic_modules[module_name].parameters
        else:
            compounds = []
            modifiers = []
            parameters = []

            param_names = self.get_all_parameter_names()

            for i in args:
                if i in param_names:
                    parameters.append(i)
                elif i in self.compounds:
                    compounds.append(i)
                else:
                    modifiers.append(i)
        self.update_algebraic_module(
            module_name=module_name,
            function=function,
            compounds=compounds,
            derived_compounds=derived_compounds,
            modifiers=modifiers,
            parameters=parameters,
            dynamic_variables=None,
            args=args,
            check_consistency=check_consistency,
            **meta_info,
        )
        return self

    def update_algebraic_modules(
        self, modules: dict, meta_info: dict | None = None
    ) -> Self:
        """Update multiple algebraic modules

        See Also
        --------
        update_algebraic_module

        """
        meta_info = {} if meta_info is None else meta_info
        for name, module in modules.items():
            info = meta_info.get(name, {})
            self.update_algebraic_module(name, **module, **info)
        return self

    def update_module_meta_info(self, module: str, meta_info: dict) -> Self:
        """Update meta info of an algebraic module.

        Parameters
        ----------
        module : str
            Name of the algebraic module
        meta_info : dict
            Meta info of the algebraic module. Allowed keys are
            {common_name, notes, database_links}

        """
        self.update_meta_info(component="modules", meta_info={module: meta_info})
        return self

    def remove_algebraic_module(self, module_name: str) -> Self:
        """Remove an algebraic module.

        Parameters
        ----------
        module_name : str
            Name of the algebraic module

        """
        self._algebraic_cache = None

        module = self.algebraic_modules.pop(module_name)
        self._remove_ids(module.derived_compounds)

        return self

    def remove_algebraic_modules(self, module_names: list[str]) -> Self:
        """Remove multiple algebraic modules.

        Parameters
        ----------
        module_names : iterable(str)
            Names of the algebraic modules

        """
        for module_name in module_names:
            self.remove_algebraic_module(module_name=module_name)
        return self

    def get_algebraic_module(self, module_name: str) -> AlgebraicModule:
        """Return the algebraic module"""
        return self.algebraic_modules[module_name]

    def get_algebraic_module_function(
        self, module_name: str
    ) -> Callable[..., float] | Callable[..., Iterable[float]]:
        """Return the function of the algebraic module"""
        return self.algebraic_modules[module_name].function

    def get_algebraic_module_compounds(self, module_name: str) -> list[str]:
        """Return the compounds of the algebraic module"""
        return list(self.algebraic_modules[module_name].compounds)

    def get_algebraic_module_derived_compounds(self, module_name: str) -> list[str]:
        """Return the derived compounds of the algebraic module"""
        return list(self.algebraic_modules[module_name].derived_compounds)

    def get_algebraic_module_modifiers(self, module_name: str) -> list[str]:
        """Return the modifiers of the algebraic module"""
        return list(self.algebraic_modules[module_name].modifiers)

    def get_algebraic_module_parameters(self, module_name: str) -> list[str]:
        """Return the parameters of the algebraic module"""
        return list(self.algebraic_modules[module_name].parameters)

    def get_algebraic_module_args(self, module_name: str) -> list[str]:
        """Return the arguments of the algebraic module function"""
        return list(self.algebraic_modules[module_name].args)

    ##########################################################################
    # Readouts
    # Similar to algebraic modules, just not always calculated
    ##########################################################################

    def add_readout(
        self, name: str, function: Callable[..., float], args: list[str]
    ) -> Self:
        self.readouts[name] = Readout(function, args)
        return self

    ##########################################################################
    # Simulation functions
    ##########################################################################

    def _get_fcd(
        self,
        *,
        t: Array,
        y: dict[str, Array],
    ) -> dict[str, Array]:
        """Calculate the derived variables of all algebraic modules.

        fdc = full_concentration_dict

        The derived compounds are sorted by the algebraic modules and their internal
        derived_modules attribute.
        """
        y["time"] = t
        args = self.parameters | y
        for name in self._algebraic_module_order:
            module = self.algebraic_modules[name]
            try:
                derived_values = module.function(*(args[arg] for arg in module.args))
            except KeyError as e:
                msg = f"Could not find argument {e} for module {name}"
                raise KeyError(msg) from e
            derived_compounds = dict(
                zip(
                    module.derived_compounds,
                    np.array(derived_values).reshape(
                        (len(module.derived_compounds), -1)
                    ),
                )
            )
            y.update(derived_compounds)
            args.update(derived_compounds)
        return y

    ##########################################################################
    # Source code functions
    ##########################################################################

    def _generate_algebraic_modules_source_code(
        self, *, include_meta_info: bool = True
    ) -> tuple[str, str]:
        """Generate modelbase source code for algebraic modules.

        This is mainly used for the generate_model_source_code function.

        Parameters
        ----------
        include_meta_info : bool
            Whether to include meta info in the source code.

        Returns
        -------
        algebraic_module_source_code : str
            Code generating the Python functions of the algebraic modules
        algebraic_module_modelbase_code : str
            Code generating the modelbase objects

        See Also
        --------
        generate_model_source_code

        """
        module_functions = set()
        modules = []
        for name, module in self.algebraic_modules.items():
            function = module.function
            compounds = module.compounds
            derived_compounds = module.derived_compounds
            modifiers = module.modifiers
            parameters = module.parameters
            args = module.args

            function_code = get_formatted_function_source_code(
                function_name=name, function=function, function_type="module"
            )
            module_functions.add(function_code)
            module_definition = (
                "m.add_algebraic_module(\n"
                f"    module_name={name!r},\n"
                f"    function={function.__name__},\n"
                f"    compounds={compounds},\n"
                f"    derived_compounds={derived_compounds},\n"
                f"    modifiers={modifiers},\n"
                f"    parameters={parameters},\n"
                f"    args={args},\n"
            )
            if include_meta_info:
                meta_info = self._get_nonzero_meta_info(component="modules")
                try:
                    info = meta_info[name]
                    module_definition += f"**{info}"
                except KeyError:
                    pass
            module_definition += ")"
            modules.append(module_definition)
        return "\n".join(sorted(module_functions)), "\n".join(modules)

    ##########################################################################
    # SBML functions
    ##########################################################################

    def _create_sbml_algebraic_modules(self, *, _sbml_model: libsbml.Model) -> None:
        """Convert the algebraic modules their sbml equivalent.

        Notes
        -----
        The closest we can get in SBML are assignment rules of the form x = f(V), see
        http://sbml.org/Software/libSBML/docs/python-api/classlibsbml_1_1_assignment_rule.html

        Thus we have to split algebraic modules that contain multiple derived compounds
        into multiple assignment rules.

        But apparently they do not support parameters, so for now I am skipping
        this.

        """
        warnings.warn("SBML does support algebraic modules, skipping.")
