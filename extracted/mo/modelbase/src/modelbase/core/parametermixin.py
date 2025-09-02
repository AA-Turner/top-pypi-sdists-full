from __future__ import annotations

__all__ = [
    "Parameter",
    "ParameterMixin",
]

import json
import pickle
import warnings
from dataclasses import dataclass, field
from queue import Empty, SimpleQueue
from typing import TYPE_CHECKING, Any, Callable, Iterable

from typing_extensions import Literal, Self  # 3.7 compatability

from .basemodel import BaseModel
from .utils import (
    _sort_dependencies,
    convert_id_to_sbml,
    get_formatted_function_source_code,
    warning_on_one_line,
)

if TYPE_CHECKING:
    import libsbml

warnings.formatwarning = warning_on_one_line  # type: ignore


@dataclass
class Parameter:
    """Meta-info container for parameters."""

    unit: str | None = None
    annotation: str | None = None
    database_links: dict = field(default_factory=dict)
    notes: dict = field(default_factory=dict)


@dataclass
class DerivedParameter:
    function: Callable
    parameters: list[str]

    def __getitem__(self, key: str) -> Any:
        return self.__dict__[key]


@dataclass
class ParameterCache:
    derived_parameter_order: list[str]


class ParameterMixin(BaseModel):
    """Adding parameter functions."""

    def __init__(self, parameters: dict[str, float] | None = None) -> None:
        self.derived_parameters: dict[str, DerivedParameter] = {}
        self._parameters: dict[str, float] = {}
        self._parameter_cache: ParameterCache | None = None

        # Bookkeeping
        self._derived_from_parameters: set[str] = set()

        if parameters is not None:
            self.add_parameters(parameters=parameters)
        self.initialization_parameters = self._parameters.copy()

    def _make_parameter_cache(self) -> ParameterCache:
        self._parameter_cache = ParameterCache(
            derived_parameter_order=_sort_dependencies(
                available=set(self._parameters),
                elements=[
                    (k, set(v.parameters)) for k, v in self.derived_parameters.items()
                ],
            )
        )
        return self._parameter_cache

    @property
    def _derived_parameter_order(self) -> list[str]:
        cache = (
            self._make_parameter_cache()
            if self._parameter_cache is None
            else self._parameter_cache
        )

        return cache.derived_parameter_order

    @property
    def parameters(self) -> dict[str, float]:
        return self.get_all_parameters()

    ##########################################################################
    # Meta info
    ##########################################################################

    def _add_parameter_meta_info(self, parameter: str, meta_info: dict) -> None:
        self.meta_info.setdefault("parameters", {}).setdefault(
            parameter,
            Parameter(**meta_info),  # type: ignore
        )

    def update_parameter_meta_info(self, parameter: str, meta_info: dict) -> Self:
        """Update meta info of a parameter.

        Parameters
        ----------
        meta_info
            Meta info of the parameter. Allowed keys are
            {unit, database_links, notes}

        """
        self.update_meta_info(component="parameters", meta_info={parameter: meta_info})
        return self

    ##########################################################################
    # Parameter functions
    ##########################################################################

    def add_parameter(
        self,
        parameter_name: str,
        parameter_value: float,
        **meta_info: dict[str, Any],
    ) -> Self:
        """Add a new parameter to the model.

        Parameters
        ----------
        meta_info
            Meta info of the parameter. Allowed keys are
            {unit, database_links, notes}

        """
        self._check_and_insert_ids([parameter_name], context="add_parameter")
        self._add_parameter_meta_info(parameter_name, meta_info)

        self._parameters[parameter_name] = parameter_value
        return self

    def add_parameters(
        self,
        parameters: dict[str, float],
        meta_info: dict[str, Any] | None = None,
    ) -> Self:
        """Add multiple parameters to the model"""
        self._parameter_cache = None
        meta_info = {} if meta_info is None else meta_info
        for parameter_name, parameter_value in parameters.items():
            info = meta_info.get(parameter_name, {})
            self.add_parameter(
                parameter_name=parameter_name,
                parameter_value=parameter_value,
                **info,
            )
        return self

    def update_parameter(
        self,
        parameter_name: str,
        parameter_value: float,
        **meta_info: dict[str, Any],
    ) -> Self:
        """Update an existing model parameter.

        Warns:
        -----
        UserWarning
            If parameter is not in the model

        """
        self._parameter_cache = None
        if parameter_name not in self._parameters:
            if parameter_name in self._derived_from_parameters:
                msg = f"{parameter_name} is a derived parameter"
                raise ValueError(msg)
            warnings.warn(f"Key {parameter_name} is not in the model. Adding.")
        self.update_parameter_meta_info(parameter_name, meta_info)
        self._parameters[parameter_name] = parameter_value
        return self

    def scale_parameter(
        self,
        parameter_name: str,
        factor: float,
        verbose: bool = False,
    ) -> Self:
        self.update_parameter(parameter_name, self._parameters[parameter_name] * factor)
        if verbose:
            print(
                f"Updating parameter {parameter_name} to {self.parameters[parameter_name]:.2e}"
            )
        return self

    def update_parameters(
        self,
        parameters: dict[str, float],
        meta_info: dict[str, dict[str, Any]] | None = None,
    ) -> Self:
        """Update multiple existing model parameters.

        See Also
        --------
        update_parameter

        """
        meta_info = {} if meta_info is None else meta_info
        for parameter_name, parameter_value in parameters.items():
            info = meta_info.get(parameter_name, {})
            self.update_parameter(
                parameter_name=parameter_name,
                parameter_value=parameter_value,
                **info,
            )
        return self

    def add_and_update_parameter(
        self,
        parameter_name: str,
        parameter_value: float,
        **meta_info: dict[str, Any],
    ) -> Self:
        """Add a new or update an existing parameter."""
        if parameter_name not in self._ids:
            self.add_parameter(parameter_name, parameter_value, **meta_info)
        else:
            self.update_parameter(parameter_name, parameter_value, **meta_info)
        return self

    def add_and_update_parameters(
        self,
        parameters: dict[str, float],
        meta_info: dict[str, dict[str, Any]] | None = None,
    ) -> Self:
        """Add new and update existing model parameters.

        See Also
        --------
        add_and_update_parameter

        """
        meta_info = {} if meta_info is None else meta_info
        for parameter_name, parameter_value in parameters.items():
            info = meta_info.get(parameter_name, {})
            self.add_and_update_parameter(
                parameter_name=parameter_name,
                parameter_value=parameter_value,
                **info,
            )
        return self

    def remove_parameter(self, parameter_name: str) -> Self:
        """Remove a parameter from the model."""
        self._parameter_cache = None

        del self._parameters[parameter_name]
        if parameter_name in self.meta_info:
            del self.meta_info["parameters"][parameter_name]
        self._remove_ids([parameter_name])
        return self

    def remove_parameters(self, parameter_names: Iterable[str]) -> Self:
        """Remove multiple parameters from the model.

        See Also
        --------
        remove_parameter

        """
        for parameter_name in parameter_names:
            self.remove_parameter(parameter_name=parameter_name)
        return self

    def add_derived_parameter(
        self,
        parameter_name: str,
        function: Callable,
        parameters: list[str],
        **meta_info: dict[str, Any],
    ) -> Self:
        """Add a derived parameter.

        Derived parameters are calculated from other model parameters and dynamically updated
        on any changes.
        """

        self._parameter_cache = None
        self.derived_parameters[parameter_name] = DerivedParameter(
            function=function,
            parameters=parameters,
        )
        for parameter in parameters:
            self._derived_from_parameters.add(parameter)
        self._check_and_insert_ids([parameter_name], context="add_derived_parameter")

        return self

    def update_derived_parameter(
        self,
        parameter_name: str,
        function: Callable | None,
        parameters: list[str] | None,
        **meta_info: dict[str, Any],
    ) -> Self:
        self._parameter_cache = None

        old = self.derived_parameters[parameter_name]
        if function is None:
            function = old.function
        if parameters is None:
            parameters = old.parameters

        self.derived_parameters[parameter_name].function = function
        self.derived_parameters[parameter_name].parameters = parameters
        self.update_parameter_meta_info(parameter_name, meta_info)
        return self

    def remove_derived_parameter(self, parameter_name: str) -> Self:
        """Remove a derived parameter from the model."""
        self._parameter_cache = None

        old_parameter = self.derived_parameters.pop(parameter_name)
        derived_from = old_parameter["parameters"]
        for i in derived_from:
            if all(i not in j["parameters"] for j in self.derived_parameters.values()):
                self._derived_from_parameters.remove(i)
        self._remove_ids([parameter_name])
        return self

    def store_parameters_to_file(
        self,
        filename: str,
        filetype: Literal["json", "pickle"] = "json",
    ) -> None:
        """Store the parameters into a json or pickle file."""
        if filetype == "json":
            if not filename.endswith(".json"):
                filename += ".json"
            with open(filename, "w") as f:
                json.dump(self._parameters, f)
        elif filetype == "pickle":
            if not filename.endswith(".p"):
                filename += ".p"
            with open(filename, "wb") as f:  # type: ignore
                pickle.dump(self._parameters, f)  # type: ignore
        else:
            msg = "Can only save to json or pickle"
            raise ValueError(msg)

    def load_parameters_from_file(
        self,
        filename: str,
        filetype: Literal["json", "pickle"] = "json",
    ) -> None:
        """Load parameters from a json or pickle file."""
        if filetype == "json":
            with open(filename) as f:
                self.add_and_update_parameters(parameters=json.load(f))
        elif filetype == "pickle":
            with open(filename, "rb") as f:  # type: ignore
                self.add_and_update_parameters(parameters=pickle.load(f))  # type: ignore
        else:
            msg = "Can only load from json or pickle"
            raise ValueError(msg)

    def restore_initialization_parameters(self) -> Self:
        """Restore parameters to initialization parameters."""
        self._parameters = self.initialization_parameters.copy()
        return self

    def get_parameter(self, parameter_name: str) -> float:
        """Return the value of a single parameter."""
        if parameter_name in self.derived_parameters:
            msg = (
                f"Parameter {parameter_name} is a derived parameter. "
                "Use `.parameters[parameter_name]` "
                "or `get_derived_parameter_value(parameter_name)`"
            )
            raise ValueError(msg)
        return self._parameters[parameter_name]

    def get_derived_parameter(self, parameter_name: str) -> DerivedParameter:
        return self.derived_parameters[parameter_name]

    def get_derived_parameter_value(self, parameter_name: str) -> float:
        if parameter_name in self._parameters:
            msg = (
                f"Parameter {parameter_name} is a normal parameter. "
                "Use `.parameters[parameter_name]` "
                "or `.get_parameter(parameter_name)`"
            )
            raise ValueError(msg)

        return self.parameters[parameter_name]

    def get_parameters(self) -> dict[str, float]:
        """Return all parameters."""
        return dict(self._parameters)

    def get_all_parameters(self) -> dict[str, float]:
        all_params = self._parameters.copy()

        for parameter_name in self._derived_parameter_order:
            derived_parameter = self.derived_parameters[parameter_name]
            all_params[parameter_name] = derived_parameter.function(
                *(all_params[i] for i in derived_parameter.parameters)
            )

        return all_params

    def get_parameter_names(self) -> list[str]:
        """Return names of all parameters"""
        return list(self._parameters)

    def get_all_parameter_names(self) -> set[str]:
        """Return names of all parameters"""
        return set(self._parameters) | set(self.derived_parameters)

    ##########################################################################
    # Source code functions
    ##########################################################################
    def _generate_constant_parameters_source_code(
        self, *, include_meta_info: bool = True
    ) -> str:
        """Generate modelbase source code for parameters.

        This is mainly used for the generate_model_source_code function.

        Parameters
        ----------
        include_meta_info : bool
            Whether to include the parameter meta info

        Returns
        -------
        parameter_modelbase_code : str
            Source code generating the modelbase parameters

        """
        parameters = repr(dict(self._parameters.items()))
        # derived_pars =
        if include_meta_info:
            meta_info = self._get_nonzero_meta_info(component="parameters")
            if bool(meta_info):
                return (
                    f"m.add_parameters(parameters={parameters}, meta_info={meta_info})"
                )
        return f"m.add_parameters(parameters={parameters})"

    def _generate_derived_parameters_source_code(self) -> tuple[str, str]:
        """Generate modelbase source code for parameters.

        This is mainly used for the generate_model_source_code function.

        Parameters
        ----------
        include_meta_info : bool
            Whether to include the parameter meta info

        Returns
        -------
        parameter_modelbase_code : str
            Source code generating the modelbase parameters

        """
        fns: set[str] = set()
        pars: list[str] = []
        for name, module in self.derived_parameters.items():
            function = module["function"]
            parameters = module["parameters"]

            function_code = get_formatted_function_source_code(
                function_name=name, function=function, function_type="module"
            )
            fns.add(function_code)
            pars.append(
                "m.add_derived_parameter(\n"
                f"    parameter_name={name!r},\n"
                f"    function={function.__name__},\n"
                f"    parameters={parameters},\n"
                ")"
            )
        return "\n".join(sorted(fns)), "\n".join(pars)

    def _generate_parameters_source_code(
        self, *, include_meta_info: bool = True
    ) -> tuple[str, str, str]:
        return (
            self._generate_constant_parameters_source_code(
                include_meta_info=include_meta_info
            ),
            *self._generate_derived_parameters_source_code(),
        )

    ##########################################################################
    # SBML functions
    ##########################################################################

    def _create_sbml_parameters(self, *, sbml_model: libsbml.Model) -> None:
        """Create the parameters for the sbml model.

        Parameters
        ----------
        sbml_model : libsbml.Model

        """
        for parameter_id, value in self._parameters.items():
            parameter = self.meta_info["parameters"][parameter_id]
            k = sbml_model.createParameter()
            k.setId(convert_id_to_sbml(id_=parameter_id, prefix="PAR"))
            k.setConstant(True)
            k.setValue(float(value))
            unit = parameter.unit
            if unit is not None:
                k.setUnits(unit)
