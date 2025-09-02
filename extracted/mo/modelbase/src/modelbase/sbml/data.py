from __future__ import annotations

__all__ = [
    "AlgebraicRule",
    "AssignmentRule",
    "AtomicUnit",
    "Compartment",
    "CompositeUnit",
    "Compound",
    "Function",
    "InitialAssignment",
    "Parameter",
    "RateRule",
    "Reaction",
]

from dataclasses import dataclass


@dataclass
class AtomicUnit:
    kind: str
    exponent: int
    scale: int
    multiplier: float


@dataclass
class CompositeUnit:
    sbml_id: str
    units: list


@dataclass
class Parameter:
    sbml_id: str
    name: str
    value: float
    is_constant: bool


@dataclass
class InitialAssignment:
    sbml_id: str
    derived_parameter: str
    function_args: list[str]
    function_body: str
    sbml_math: str


@dataclass
class Compartment:
    sbml_id: str
    name: str
    dimensions: int
    size: float
    units: str
    is_constant: bool


@dataclass
class Compound:
    sbml_id: str
    name: str
    compartment: str | None
    initial_amount: float
    substance_units: str | None
    has_only_substance_units: bool
    has_boundary_condition: bool
    is_constant: bool
    is_concentration: bool


@dataclass
class Function:
    sbml_id: str
    name: str
    function_args: list[str]
    function_body: str
    sbml_math: str


@dataclass
class AlgebraicRule:
    sbml_id: str
    sbml_math: str
    parsed_args: list[str]
    derived_compound: str | None
    function_body: str
    function_args: list[str]


@dataclass
class AssignmentRule:
    sbml_id: str
    sbml_math: str
    parsed_args: list[str]
    compounds: list[str]
    derived_compound: str
    modifiers: list[str]
    parameters: list[str]
    function_body: str
    function_args: list[str]


@dataclass
class RateRule:
    sbml_id: str
    sbml_math: str
    parsed_args: list[str]
    derived_compound: str
    modifiers: list[str]
    function_args: list[str]
    function_body: str


@dataclass
class Reaction:
    sbml_id: str
    sbml_math: str
    is_reversible: bool
    modifiers: list
    parsed_args: list[str]
    parsed_reactants: dict
    parsed_products: dict
    function_body: str
    function_args: list[str]
    parameters: list
    stoichiometry: dict
