"""The main class for modeling. Provides model construction and inspection tools."""

from __future__ import annotations

from dataclasses import dataclass

__all__ = [
    "DerivedStoichiometry",
    "Model",
]

import copy
import itertools as it
import subprocess
import warnings
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    cast,
)

import libsbml
import numpy as np
import pandas as pd
from typing_extensions import Self

from modelbase.core import (
    AlgebraicMixin,
    BaseModel,
    CompoundMixin,
    ParameterMixin,
    RateMixin,
    Readout,
    StoichiometricMixin,
)
from modelbase.core.utils import convert_id_to_sbml

from . import _AbstractRateModel

if TYPE_CHECKING:
    from modelbase.typing import Array, ArrayLike

    from . import LabelModel, LinearLabelModel


@dataclass
class DerivedStoichiometry:
    function: Callable[..., float]
    args: list[str]


class Model(_AbstractRateModel, BaseModel):
    """The main class for modeling. Provides model construction and inspection tools."""

    def __init__(
        self,
        parameters: dict[str, float] | None = None,
        compounds: list[str] | None = None,
        algebraic_modules: dict | None = None,
        rate_stoichiometries: dict | None = None,
        rates: dict | None = None,
        functions: dict | None = None,
        meta_info: dict | None = None,
    ) -> None:
        BaseModel.__init__(self, meta_info=meta_info)
        CompoundMixin.__init__(self, compounds=compounds)
        ParameterMixin.__init__(self, parameters=parameters)
        AlgebraicMixin.__init__(self, algebraic_modules=algebraic_modules)
        StoichiometricMixin.__init__(self, rate_stoichiometries=rate_stoichiometries)
        RateMixin.__init__(self, rates=rates, functions=functions)
        self.meta_info["model"].sbo = "SBO:0000062"  # continuous framework
        self.derived_stoichiometries: dict[str, dict[str, DerivedStoichiometry]] = {}

    def __enter__(self) -> Model:
        """Enter the context manager.

        Returns
        -------
            Deepcopy of the model object

        """
        self._copy = self.copy()
        return self.copy()

    def copy(self) -> Model:
        """Create a deepcopy of the model.

        Returns
        -------
        model
            Deepcopy of the model object

        """
        return copy.deepcopy(self)  # type: ignore

    def __str__(self) -> str:
        """Give a string representation.

        Returns
        -------
        representation : str

        """
        return (
            "Model:"
            + f"\n    {len(self.get_compounds())} Compounds"
            + f"\n    {len(self.get_stoichiometries())} Reactions"
        )

    def _element_difference(
        self, other: Model, attribute: str
    ) -> list[str] | dict[str, list[str]] | None:
        self_collection = getattr(self, attribute)
        other_collection = getattr(other, attribute)
        difference = sorted(set(other_collection).difference(self_collection))
        if not difference:
            return None
        if attribute == "compounds":
            return difference
        return {k: other_collection[k] for k in difference}

    def _element_intersection(
        self, other: Model, attribute: str
    ) -> list[str] | dict[str, list[str]] | None:
        self_collection = getattr(self, attribute)
        other_collection = getattr(other, attribute)
        intersection: list[str] = sorted(
            set(self_collection).intersection(other_collection)
        )
        if not intersection:
            return None
        if attribute == "compounds":
            return intersection
        return {k: other_collection[k] for k in intersection}

    def __add__(self, other: Model) -> Model:
        return self.copy().__iadd__(other)

    def __iadd__(self, other: Model) -> Model:
        self.add(compounds=self._element_difference(other, "compounds"))  # type: ignore

        for k, v in other.get_parameters().items():
            if k not in other.derived_parameters:
                self.add_and_update_parameter(k, v)

        for k, dpar in other.derived_parameters.items():
            if k in self.derived_parameters:
                self.update_derived_parameter(k, dpar["function"], dpar["parameters"])
            else:
                self.add_derived_parameter(
                    k, function=dpar["function"], parameters=dpar["parameters"]
                )

        for name in other._algebraic_module_order:
            module = other.algebraic_modules[name]
            if name in self.algebraic_modules:
                self.update_algebraic_module(name, **dict(module))
            else:
                self.add_algebraic_module(name, **dict(module))

        for rate_name, cpd_dict in other.derived_stoichiometries.items():
            for cpd_name, der_stoich in cpd_dict.items():
                self._add_derived_stoichiometry(
                    rate_name=rate_name,
                    cpd_name=cpd_name,
                    derived_stoichiometry=der_stoich,
                )

        for attribute in [
            "rates",
            "stoichiometries",
            "functions",
            "readouts",
        ]:
            self.add(**{attribute: self._element_difference(other, attribute)})  # type: ignore
            self.update(**{attribute: self._element_intersection(other, attribute)})  # type: ignore
        return self

    def __sub__(self, other: Model) -> Model:
        m: Model = self.copy()
        for attribute in [
            "compounds",
            "parameters",
            "algebraic_modules",
            "rates",
            "stoichiometries",
            "functions",
            "derived_stoichiometries",
            "readouts",
        ]:
            m.remove(**{attribute: self._element_intersection(other, attribute)})  # type: ignore
        return m

    def __isub__(self, other: Model) -> Model:
        return self.copy().__sub__(other)

    def _collect_used_parameters(self) -> set[str]:
        used_parameters = set()
        for par in self.derived_parameters.values():
            used_parameters.update(par["parameters"])
        for module in self.algebraic_modules.values():
            used_parameters.update(module.parameters)
        for rate in self.rates.values():
            used_parameters.update(rate.parameters)
        for cpd_dict in self.derived_stoichiometries.values():
            for der_stoich in cpd_dict.values():
                used_parameters.update(der_stoich.args)
        return used_parameters

    def add(
        self,
        compounds: list[str] | None = None,
        parameters: dict[str, float] | None = None,
        algebraic_modules: dict[str, dict] | None = None,
        rates: dict[str, dict] | None = None,
        stoichiometries: dict[str, dict] | None = None,
        functions: dict[str, Callable] | None = None,
        readouts: dict[str, Readout] | None = None,
    ) -> Self:
        if compounds is not None:
            self.add_compounds(compounds)
        if parameters is not None:
            self.add_parameters(parameters)
        if algebraic_modules is not None:
            self.add_algebraic_modules(algebraic_modules)
        if rates is not None:
            self.add_rates(rates)
        if stoichiometries is not None:
            self.add_stoichiometries(stoichiometries)
        if functions is not None:
            self.add_functions(functions)
        if readouts is not None:
            for name, readout in readouts.items():
                self.add_readout(name, readout.function, readout.args)
        return self

    def update(
        self,
        parameters: dict[str, float] | None = None,
        algebraic_modules: dict[str, dict] | None = None,
        rates: dict[str, dict] | None = None,
        stoichiometries: dict[str, dict] | None = None,
        functions: dict[str, Callable] | None = None,
        readouts: dict[str, Readout] | None = None,
    ) -> Self:
        if parameters is not None:
            self.update_parameters(parameters)
        if algebraic_modules is not None:
            self.update_algebraic_modules(algebraic_modules)
        if rates is not None:
            self.update_rates(rates)
        if stoichiometries is not None:
            self.update_stoichiometries(stoichiometries)
        if functions is not None:
            self.update_functions(functions)
        if readouts is not None:
            for name, readout in readouts.items():
                self.add_readout(name, readout.function, readout.args)
        return self

    def remove(
        self,
        compounds: list[str] | None = None,
        parameters: list[str] | None = None,
        algebraic_modules: list[str] | None = None,
        rates: list[str] | None = None,
        stoichiometries: list[str] | None = None,
        functions: list[str] | None = None,
        derived_stoichiometries: list[str] | None = None,
    ) -> Self:
        if compounds is not None:
            self.remove_compounds(compounds)
        if parameters is not None:
            self.remove_parameters(parameters)
        if algebraic_modules is not None:
            self.remove_algebraic_modules(algebraic_modules)
        if rates is not None:
            self.remove_rates(rates)
        if stoichiometries is not None:
            self.remove_rate_stoichiometries(stoichiometries)
        if functions is not None:
            self.remove_functions(functions)
        if derived_stoichiometries is not None:
            self._remove_derived_stoichiometries(derived_stoichiometries)
        return self

    ##########################################################################
    # Reactions
    ##########################################################################

    def _add_derived_stoichiometry(
        self, rate_name: str, cpd_name: str, derived_stoichiometry: DerivedStoichiometry
    ) -> None:
        self.derived_stoichiometries.setdefault(rate_name, {})[cpd_name] = (
            derived_stoichiometry
        )
        self._update_derived_stoichiometries()

    def _update_derived_stoichiometries(self) -> None:
        parameters = self.get_all_parameters()
        for rate_name, d in self.derived_stoichiometries.items():
            for cpd_name, stoichiometry in d.items():
                new_stoichiometry = stoichiometry.function(
                    *(parameters[i] for i in stoichiometry.args)
                )

                self.stoichiometries.setdefault(rate_name, {}).update(
                    {cpd_name: new_stoichiometry}
                )
                self.stoichiometries_by_compounds.setdefault(cpd_name, {}).update(
                    {rate_name: new_stoichiometry}
                )

    def _remove_derived_stoichiometry(self, rate_name: str) -> None:
        self.derived_stoichiometries.pop(rate_name, None)

    def _remove_derived_stoichiometries(self, rate_names: list[str]) -> None:
        for rate_name in rate_names:
            self._remove_derived_stoichiometry(rate_name)

    def update_parameter(
        self,
        parameter_name: str,
        parameter_value: float,
        **meta_info: dict[str, Any],
    ) -> Self:
        super().update_parameter(parameter_name, parameter_value, **meta_info)
        self._update_derived_stoichiometries()
        return self

    def update_parameters(
        self,
        parameters: dict[str, float],
        meta_info: dict[str, Any] | None = None,
    ) -> Self:
        super().update_parameters(parameters, meta_info)
        self._update_derived_stoichiometries()
        return self

    def add_reaction(
        self,
        rate_name: str,
        function: Callable[..., float],
        stoichiometry: dict[str, float],
        modifiers: list[str] | None = None,
        parameters: list[str] | None = None,
        dynamic_variables: list[str] | None = None,
        args: list[str] | None = None,
        reversible: bool = False,
        check_consistency: bool = True,
        derived_stoichiometry: dict[str, DerivedStoichiometry] | None = None,
        **meta_info: dict[str, Any],
    ) -> Self:
        """Add a reaction to the model.

        Shortcut for add_rate and add stoichiometry functions.

        See Also
        --------
        add_rate
        add_stoichiometry

        Examples
        --------
        >>> add_reaction(
        >>>     rate_name="v1",
        >>>     function=mass_action,
        >>>     stoichiometry={"X": -1, "Y": 1},
        >>>     parameters=["k2"],
        >>> )

        >>> add_reaction(
        >>>     rate_name="v1",
        >>>     function=reversible_mass_action,
        >>>     stoichiometry={"X": -1, "Y": 1},
        >>>     parameters=["k1_fwd", "k1_bwd"],
        >>>     reversible=True,
        >>> )

        """
        self.add_stoichiometry(rate_name=rate_name, stoichiometry=stoichiometry)

        if derived_stoichiometry is not None:
            for cpd_name, der in derived_stoichiometry.items():
                self._add_derived_stoichiometry(rate_name, cpd_name, der)

        # Use now updated stoichiometry
        stoichiometry = self.stoichiometries[rate_name]
        substrates = [k for k, v in stoichiometry.items() if v < 0]
        products = [k for k, v in stoichiometry.items() if v > 0]

        self.add_rate(
            rate_name=rate_name,
            function=function,
            substrates=substrates,
            products=products,
            dynamic_variables=dynamic_variables,
            modifiers=modifiers,
            parameters=parameters,
            reversible=reversible,
            args=args,
            check_consistency=check_consistency,
            **meta_info,
        )
        return self

    def add_reaction_from_args(
        self,
        rate_name: str,
        function: Callable[..., float],
        stoichiometry: dict[str, float],
        args: list[str],
        reversible: bool | None = None,
        derived_stoichiometry: dict[str, DerivedStoichiometry] | None = None,
        check_consistency: bool = True,
        **meta_info: dict[str, Any],
    ) -> Self:
        self.add_stoichiometry(rate_name=rate_name, stoichiometry=stoichiometry)

        if derived_stoichiometry is not None:
            for cpd_name, der in derived_stoichiometry.items():
                self._add_derived_stoichiometry(rate_name, cpd_name, der)

        # Use now updated stoichiometry
        stoichiometry = self.stoichiometries[rate_name]

        modifiers = []
        parameters = []
        dynamic_variables = []

        par_names = self.get_all_parameter_names()
        for i in args:
            if i in par_names:
                parameters.append(i)
            elif i not in stoichiometry:
                modifiers.append(i)
                dynamic_variables.append(i)
            else:
                dynamic_variables.append(i)
        substrates = [k for k, v in stoichiometry.items() if v < 0]
        products = [k for k, v in stoichiometry.items() if v > 0]

        if reversible is None:
            if any(i in dynamic_variables for i in products):
                reversible = True
            else:
                reversible = False

        self.add_rate(
            rate_name=rate_name,
            function=function,
            substrates=substrates,
            products=products,
            modifiers=modifiers,
            parameters=parameters,
            dynamic_variables=dynamic_variables,
            args=args,
            reversible=reversible,
            check_consistency=check_consistency,
            **meta_info,
        )
        return self

    def update_reaction(
        self,
        rate_name: str,
        function: Callable[..., float] | None = None,
        stoichiometry: dict[str, float] | None = None,
        modifiers: list[str] | None = None,
        parameters: list[str] | None = None,
        dynamic_variables: list[str] | None = None,
        args: list[str] | None = None,
        reversible: bool | None = None,
        check_consistency: bool = True,
        derived_stoichiometry: dict[str, DerivedStoichiometry] | None = None,
        **meta_info: dict[str, Any],
    ) -> Self:
        """Update an existing reaction.

        See Also
        --------
        add_reaction
        update_rate
        update_stoichiometry

        """
        if derived_stoichiometry is not None:
            for cpd_name, der in derived_stoichiometry.items():
                self._add_derived_stoichiometry(rate_name, cpd_name, der)

        if stoichiometry is not None:
            self.update_stoichiometry(rate_name=rate_name, stoichiometry=stoichiometry)

        if stoichiometry is not None:
            stoichiometry = self.stoichiometries[rate_name]
            substrates = [k for k, v in stoichiometry.items() if v < 0]
            products = [k for k, v in stoichiometry.items() if v > 0]
        else:
            substrates = None  # type: ignore
            products = None  # type: ignore
        self.update_rate(
            rate_name=rate_name,
            function=function,
            substrates=substrates,
            products=products,
            modifiers=modifiers,
            parameters=parameters,
            reversible=reversible,
            dynamic_variables=dynamic_variables,
            args=args,
            check_consistency=check_consistency,
            **meta_info,
        )
        return self

    def update_stoichiometry_of_cpd(
        self, rate_name: str, compound: str, value: float
    ) -> Model:
        self.update_stoichiometry(
            rate_name=rate_name,
            stoichiometry=self.stoichiometries[rate_name] | {compound: value},
        )
        return self

    def scale_stoichiometry_of_cpd(
        self, rate_name: str, compound: str, scale: float
    ) -> Model:
        return self.update_stoichiometry_of_cpd(
            rate_name=rate_name,
            compound=compound,
            value=self.stoichiometries[rate_name][compound] * scale,
        )

    def update_reactions(self, reactions: dict) -> Self:
        for rate_name, reaction in reactions.items():
            self.update_reaction(rate_name, **reaction)
        return self

    def update_reaction_from_args(
        self,
        rate_name: str,
        function: Callable[..., float] | None = None,
        stoichiometry: dict[str, float] | None = None,
        args: list[str] | None = None,
        reversible: bool | None = None,
        check_consistency: bool = True,
        derived_stoichiometry: dict[str, DerivedStoichiometry] | None = None,
        **meta_info: dict[str, Any],
    ) -> Self:
        if stoichiometry is not None:
            self.update_stoichiometry(rate_name=rate_name, stoichiometry=stoichiometry)

        if derived_stoichiometry is not None:
            for cpd_name, der in derived_stoichiometry.items():
                self._add_derived_stoichiometry(rate_name, cpd_name, der)

        # Now properly updated
        stoichiometry = self.stoichiometries[rate_name]

        if function is None:
            function = self.rates[rate_name].function

        if args is not None:
            modifiers = []
            parameters = []
            dynamic_variables = []

            par_names = self.get_all_parameter_names()
            for i in args:
                if i in par_names:
                    parameters.append(i)
                elif i not in stoichiometry:
                    modifiers.append(i)
                    dynamic_variables.append(i)
                else:
                    dynamic_variables.append(i)
            substrates = [k for k, v in stoichiometry.items() if v < 0]
            products = [k for k, v in stoichiometry.items() if v > 0]
            if reversible is None:
                if any(i in dynamic_variables for i in products):
                    reversible = True
                else:
                    reversible = False
        else:
            substrates = self.rates[rate_name].substrates
            products = self.rates[rate_name].products
            modifiers = self.rates[rate_name].modifiers
            parameters = self.rates[rate_name].parameters
            dynamic_variables = self.rates[rate_name].dynamic_variables
            args = self.rates[rate_name].args

        self.update_rate(
            rate_name=rate_name,
            function=function,
            substrates=substrates,
            products=products,
            modifiers=modifiers,
            parameters=parameters,
            reversible=reversible,
            dynamic_variables=dynamic_variables,
            args=args,
            check_consistency=check_consistency,
            **meta_info,
        )
        return self

    def add_reaction_from_ratelaw(
        self,
        rate_name: str,
        ratelaw: Any,
        **meta_info: dict[str, Any],
    ) -> Self:
        """Add a reaction from a ratelaw.

        Parameters
        ----------
        rate_name
        ratelaw
            Ratelaw instance
        meta_info

        Examples
        --------
        >>> add_reaction_from_ratelaw(
                rate_name="v1",
                ratelaw=ReversibleMassAction(
                    substrates=["X"],
                    products=["Y"],
                    k_fwd="k1p",
                    k_bwd="k1m"
                ),
            )

        """
        default_meta_info = {"sbml_function": ratelaw.get_sbml_function_string()}
        default_meta_info.update(meta_info)

        self.add_rate(
            rate_name=rate_name,
            function=ratelaw.get_rate_function(),
            substrates=ratelaw.substrates,
            products=ratelaw.products,
            modifiers=ratelaw.modifiers,
            parameters=ratelaw.parameters,
            reversible=ratelaw.reversible,
            **default_meta_info,
        )
        self.add_stoichiometry(rate_name=rate_name, stoichiometry=ratelaw.stoichiometry)
        return self

    def remove_reaction(self, rate_name: str) -> Self:
        """Remove a reaction from the model.

        Parameters
        ----------
        rate_name : str

        """
        self.remove_rate(rate_name=rate_name)
        self.remove_rate_stoichiometry(rate_name=rate_name)
        self._remove_derived_stoichiometry(rate_name=rate_name)
        return self

    def remove_reactions(self, rate_names: list[str]) -> Self:
        """Remove multiple reactions from the model.

        Parameters
        ----------
        names : iterable(str)

        """
        for rate_name in rate_names:
            self.remove_reaction(rate_name=rate_name)
        return self

    ##########################################################################
    # Conversion functions
    ##########################################################################

    def make_parameter_dynamic(self, name: str) -> Self:
        if name in self.derived_parameters:
            self.remove_derived_parameter(parameter_name=name)
        else:
            self.remove_parameter(parameter_name=name)
        self.add_compound(name)

        # Change all modifiers / parameters etc. accordingly
        for rate_name, rate in self.rates.items():
            if name in rate.args:
                self.update_reaction_from_args(rate_name=rate_name, args=rate.args)
        return self

    def make_compound_static(self, name: str, parameter_value: float) -> Self:
        self.remove_compound(name)
        self.add_parameter(parameter_name=name, parameter_value=parameter_value)

        # Change all modifiers / parameters etc. accordingly
        for rate_name, rate in self.rates.items():
            if name in rate.args:
                self.update_reaction_from_args(rate_name=rate_name, args=rate.args)
        return self

    ##########################################################################
    # Simulation functions
    ##########################################################################

    def get_full_concentration_dict(
        self,
        y: dict[str, float] | dict[str, Array] | ArrayLike | Array,
        t: float | ArrayLike | Array = 0.0,
        include_readouts: bool = False,
    ) -> dict[str, Array]:
        """Calculate the derived variables (at time(s) t).

        Examples
        --------
        >>> get_full_concentration_dict(y=[0, 0])
        >>> get_full_concentration_dict(y={"X": 0, "Y": 0})

        """
        if isinstance(t, (int, float)):
            t = [t]
        t = np.array(t)
        if isinstance(y, dict):
            y = {k: np.ones(len(t)) * v for k, v in y.items()}
        else:
            y = dict(zip(self.get_compounds(), (np.ones((len(t), 1)) * y).T))

        fcd = {
            k: np.ones(len(t)) * v
            for k, v in self._get_fcd(
                t=t,
                y=y,  # type: ignore
            ).items()
        }
        if include_readouts:
            args = self.parameters | y
            for name, readout in self.readouts.items():
                fcd[name] = np.ones(len(t)) * readout.function(
                    *(args[i] for i in readout.args)
                )
        return fcd  # type: ignore

    def get_derived_variables(self, y: dict[str, float]) -> pd.Series:
        s = (
            pd.DataFrame(self.get_full_concentration_dict(y))
            .iloc[0]
            .drop(["time", *self.compounds])
        )
        s.name = "derived_variables"
        return s

    def get_fluxes_dict(
        self,
        y: dict[str, float]
        | dict[str, ArrayLike]
        | dict[str, Array]
        | Array
        | ArrayLike,
        t: float | ArrayLike | Array = 0.0,
    ) -> dict[str, Array]:
        """Calculate the fluxes at time point(s) t."""
        fcd = self.get_full_concentration_dict(y=y, t=t)  # type: ignore
        ones = np.ones(len(fcd["time"]))
        if len(fcd["time"]) == 1:
            return {k: ones * v for k, v in self._get_fluxes(fcd=fcd).items()}  # type: ignore
        return {k: ones * v for k, v in self._get_fluxes_array(fcd=fcd).items()}  # type: ignore

    # This can't get keyword-only arguments, as the integrators are calling it with
    # positional arguments
    def _get_rhs(self, t: float | ArrayLike | Array, y: list[Array]) -> Array:
        """Calculate the right hand side of the ODE system.

        This is the more performant version of get_right_hand_side()
        and thus returns only an array instead of a dictionary.

        Watch out that this function swaps t and y!
        """
        y = dict(zip(self.get_compounds(), np.array(y).reshape(-1, 1)))  # type: ignore
        fcd = self._get_fcd(t=t, y=y)  # type: ignore
        fluxes = self._get_fluxes(fcd=fcd)  # type: ignore
        compounds_local = self.get_compounds()
        dxdt = dict(zip(compounds_local, it.repeat(0.0)))
        for k, stoc in self.stoichiometries_by_compounds.items():
            for flux, n in stoc.items():
                dxdt[k] += n * fluxes[flux]
        return np.array([dxdt[i] for i in compounds_local], dtype="float")

    ##########################################################################
    # Model conversion functions
    ##########################################################################

    def to_labelmodel(
        self, labelcompounds: dict[str, int], labelmaps: dict[str, list[int]]
    ) -> LabelModel:
        """Create a LabelModel from this model.

        Examples
        --------
        >>> m = Model()
        >>> m.add_reaction(
                rate_name="TPI",
                function=reversible_mass_action_1_1,
                stoichiometry={"GAP": -1, "DHAP": 1},
                parameters=["kf_TPI", "kr_TPI"],
                reversible=True,
            )
        >>> labelcompounds = {"GAP": 3, "DHAP": 3}
        >>> labelmaps = {"TPI": [2, 1, 0]}
        >>> m.to_labelmodel(labelcompounds=labelcompounds, labelmaps=labelmaps)

        """
        from modelbase.ode import LabelModel

        lm = LabelModel()
        lm.add_parameters(self.get_parameters())
        for compound in self.get_compounds():
            if compound in labelcompounds:
                lm.add_label_compound(
                    compound=compound, num_labels=labelcompounds[compound]
                )
            else:
                lm.add_compound(compound=compound)

        for module_name, module in self.algebraic_modules.items():
            lm.add_algebraic_module(
                module_name=module_name,
                function=module["function"],
                compounds=module["compounds"],
                derived_compounds=module["derived_compounds"],
                modifiers=module["modifiers"],
                parameters=module["parameters"],
            )

        for rate_name, rate in self.rates.items():
            if rate_name not in labelmaps:
                lm.add_reaction(
                    rate_name=rate_name,
                    function=rate["function"],
                    stoichiometry=self.stoichiometries[rate_name],
                    modifiers=rate["modifiers"],
                    parameters=rate["parameters"],
                    reversible=rate["reversible"],
                )
            else:
                lm.add_labelmap_reaction(
                    rate_name=rate_name,
                    function=rate["function"],
                    stoichiometry=cast(Dict[str, int], self.stoichiometries[rate_name]),
                    labelmap=labelmaps[rate_name],
                    modifiers=rate["modifiers"],
                    parameters=rate["parameters"],
                    reversible=rate["reversible"],
                )
        return lm

    def to_linear_labelmodel(
        self,
        labelcompounds: dict[str, int],
        labelmaps: dict[str, list[int]],
        show_warnings: bool = True,
    ) -> LinearLabelModel:
        """Create a LinearLabelModel from this model.

        Watch out that for a linear label model reversible reactions have to be split
        into a forward and backward part.

        Examples
        --------
        >>> m = Model()
        >>> m.add_reaction(
        >>>     rate_name="TPI_fwd",
        >>>     function=_mass_action_1_1,
        >>>     stoichiometry={"GAP": -1, "DHAP": 1},
        >>>     parameters=["kf_TPI"],
        >>> )
        >>> m.add_reaction(
        >>>     rate_name="TPI_bwd",
        >>>     function=mass_action_1_1,
        >>>     stoichiometry={"DHAP": -1, "GAP": 1},
        >>>     parameters=["kr_TPI"],
        >>> )
        >>> labelcompounds = {"GAP": 3, "DHAP": 3}
        >>> labelmaps = {"TPI_fwd": [2, 1, 0], 'TPI_bwd': [2, 1, 0]}
        >>> m.to_linear_labelmodel(labelcompounds=labelcompounds, labelmaps=labelmaps)

        """
        from modelbase.ode import LinearLabelModel

        lm = LinearLabelModel(_warn=show_warnings)
        for compound in self.get_compounds():
            if compound in labelcompounds:
                lm.add_compound(compound=compound, num_labels=labelcompounds[compound])

        for rate_name, rate in self.rates.items():
            if rate_name in labelmaps:
                if rate["reversible"] and show_warnings:
                    warnings.warn(
                        f"Reaction {rate_name} is annotated as reversible. "
                        "Did you remember to split it into a forward and backward part?"
                    )
                lm.add_reaction(
                    rate_name=rate_name,
                    stoichiometry={
                        k: v
                        for k, v in cast(
                            Dict[str, int], self.stoichiometries[rate_name]
                        ).items()
                        if k in labelcompounds
                    },
                    labelmap=labelmaps[rate_name],
                )
            elif show_warnings:
                warnings.warn(f"Skipping reaction {rate_name} as no labelmap is given")
        return lm

    ##########################################################################
    # Source code functions
    ##########################################################################

    def generate_model_source_code(
        self, linted: bool = True, include_meta_info: bool = False
    ) -> str:
        """Generate source code of the model.

        Parameters
        ----------
        linted
            Whether the source code should be formatted via black.
            Usually it only makes sense to turn this off if there is an error somewhere.
        include_meta_info
            Whether to include meta info of the model components

        """
        parameters, par_fns, derived_pars = self._generate_parameters_source_code(
            include_meta_info=include_meta_info
        )
        compounds = self._generate_compounds_source_code(
            include_meta_info=include_meta_info
        )
        functions = self._generate_function_source_code()
        module_functions, modules = self._generate_algebraic_modules_source_code(
            include_meta_info=include_meta_info
        )
        rate_functions, rates = self._generate_rates_source_code(
            include_meta_info=include_meta_info
        )
        stoichiometries = self._generate_stoichiometries_source_code()

        to_export = [
            "import math",
            "import numpy as np",
            "from modelbase.ode import Model, Simulator",
        ]
        for i in (
            functions,
            module_functions,
            rate_functions,
            par_fns,
        ):
            if i:
                to_export.append(i)
        to_export.append("m = Model()")
        for i in (
            parameters,
            derived_pars,
            compounds,
            modules,
            rates,
            stoichiometries,
        ):
            if i:
                to_export.append(i)

        model_string = "\n".join(to_export)
        if linted:
            blacked_string = subprocess.run(
                ["black", "-c", model_string], stdout=subprocess.PIPE, check=True
            )
            return blacked_string.stdout.decode("utf-8")
        return model_string

    ##########################################################################
    # SBML functions
    ##########################################################################

    def _create_sbml_reactions(self, *, sbml_model: libsbml.Model) -> None:
        """Create the reactions for the sbml model."""
        for rate_id, stoichiometry in self.stoichiometries.items():
            rate = self.meta_info["rates"][rate_id]
            rxn = sbml_model.createReaction()
            rxn.setId(convert_id_to_sbml(id_=rate_id, prefix="RXN"))
            name = rate.common_name
            if name:
                rxn.setName(name)
            rxn.setFast(False)
            rxn.setReversible(self.rates[rate_id]["reversible"])

            for compound_id, factor in stoichiometry.items():
                if factor < 0:
                    sref = rxn.createReactant()
                else:
                    sref = rxn.createProduct()
                sref.setSpecies(convert_id_to_sbml(id_=compound_id, prefix="CPD"))
                sref.setStoichiometry(abs(factor))
                sref.setConstant(False)

            for compound in self.rates[rate_id]["modifiers"]:
                sref = rxn.createModifier()
                sref.setSpecies(convert_id_to_sbml(id_=compound, prefix="CPD"))

            function = rate.sbml_function
            if function is not None:
                kinetic_law = rxn.createKineticLaw()
                kinetic_law.setMath(libsbml.parseL3Formula(function))

    def _model_to_sbml(self) -> libsbml.SBMLDocument:
        """Export model to sbml."""
        doc = self._create_sbml_document()
        sbml_model = self._create_sbml_model(doc=doc)
        self._create_sbml_units(sbml_model=sbml_model)
        self._create_sbml_compartments(sbml_model=sbml_model)
        self._create_sbml_compounds(sbml_model=sbml_model)
        if bool(self.algebraic_modules):
            self._create_sbml_algebraic_modules(_sbml_model=sbml_model)
        self._create_sbml_reactions(sbml_model=sbml_model)
        return doc
