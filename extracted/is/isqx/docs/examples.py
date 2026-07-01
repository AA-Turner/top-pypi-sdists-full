# mypy: ignore-errors
# %%
# --8<-- [start:tsfc_example]
import isqx
import isqx.usc as usc

tsfc_converter = isqx.convert(
    usc.LB / (isqx.HOUR * usc.LBF), isqx.KG / (isqx.S * isqx.N), exact=True
)
print(f"1 lb/(h·lbf) = {tsfc_converter.scale} g/(s·kN)")
# --8<-- [end:tsfc_example]
# %%
"""
# --8<-- [start:tsfc_output]
1 lb/(h·lbf) = 50/1765197 g/(s·kN)
# --8<-- [end:tsfc_output]
"""
# %%
# --8<-- [start:verbose_fmt_example]
print(isqx.SPECIFIC_HEAT_CAPACITY(usc.BTU_IT * usc.LB**-1 * usc.R**-1))
# --8<-- [end:verbose_fmt_example]
# %%
"""
# --8<-- [start:verbose_fmt_output]
(btu_it · pound⁻¹ · rankine⁻¹)['specific_heat_capacity']
- btu_it = 1055.05585262 · joule
  - joule = newton · meter
    - newton = kilogram · meter · second⁻²
- pound = 0.45359237 · kilogram
- rankine = 5/9 · kelvin
# --8<-- [end:verbose_fmt_output]
"""
# %%
# --8<-- [start:tagged_error_example]
import isqx.aerospace as aero

try:
    isqx.convert(
        aero.PRESSURE_ALTITUDE(isqx.M), aero.GEOMETRIC_ALTITUDE(isqx.M)
    )
except isqx.DimensionMismatchError as e:
    print(e)
# --8<-- [end:tagged_error_example]
# %%
"""
# --8<-- [start:tagged_error_output]
cannot convert from `meter['altitude', relative to `'mean_sea_level'`, 'pressure']` to `meter['altitude', relative to `'mean_sea_level'`, 'geometric']`.
= help: expected compatible dimensions, but found:
dimension of origin: `L['altitude', relative to `'mean_sea_level'`, 'pressure']`
dimension of target: `L['altitude', relative to `'mean_sea_level'`, 'geometric']`
# --8<-- [end:tagged_error_output]
"""
# %%
# --8<-- [start:decorator_def]
import typing as t
from dataclasses import dataclass

from typing_extensions import ParamSpec

T = t.TypeVar("T")
P = ParamSpec("P")


@t.overload
def sphinx_doc(
    *, formatter: t.Union[isqx.Formatter, str]
) -> t.Callable[[T], T]: ...


@t.overload
def sphinx_doc(obj: T, /) -> T: ...


def sphinx_doc(
    obj: t.Optional[T] = None,
    /,
    *,
    formatter: t.Union[isqx.Formatter, str] = isqx.BasicFormatter(
        verbose=False
    ),
):
    def wrapper(obj_: T) -> T:
        doc = obj_.__doc__ or ""
        if doc.startswith(obj_.__qualname__ + "("):
            doc = ""

        hints = t.get_type_hints(obj_, include_extras=True)
        params_doc = []
        for name, hint in hints.items():
            if t.get_origin(hint) is not t.Annotated:
                continue
            # assuming the first metadata item is the isqx unit expression
            unit_expr = t.get_args(hint)[1]
            unit_str = isqx.fmt(unit_expr, formatter=formatter)
            directive = ":returns:" if name == "return" else f":param {name}:"
            params_doc.append(f"{directive} `{unit_str}`")

        if doc and params_doc:
            doc += "\n\n" + "\n".join(params_doc)
        elif params_doc:
            doc = "\n".join(params_doc)

        obj_.__doc__ = doc.strip()
        return obj_

    if obj is None:
        return wrapper
    return wrapper(obj)


# --8<-- [end:decorator_def]
# %%
# --8<-- [start:breguet_example]
_T = t.TypeVar("_T")

MPerSCruiseTas = t.Annotated[_T, aero.TRUE_AIRSPEED["cruise"](isqx.M_PERS)]
LOverD = t.Annotated[_T, isqx.ratio(isqx.LIFT(isqx.N), isqx.DRAG(isqx.N))]
SIsp = t.Annotated[_T, isqx.TIME["specific_impulse"](isqx.S)]
WiOverWf = t.Annotated[
    _T, isqx.ratio(aero.TAKEOFF_MASS(isqx.KG), aero.LANDING_MASS(isqx.KG))
]
Range = t.Annotated[_T, isqx.DISTANCE(isqx.M)]


@sphinx_doc
def breguet_range(
    v: MPerSCruiseTas,
    l_over_d: LOverD,
    isp: SIsp,
    wi_over_wf: WiOverWf,
    *,
    xp,  # library that implements the array api
) -> Range:
    """Calculates the Breguet range of an aircraft."""
    return v * l_over_d * isp * xp.log(wi_over_wf)


print(breguet_range.__doc__)
# --8<-- [end:breguet_example]
# %%
"""
# --8<-- [start:breguet_output]
Calculates the Breguet range of an aircraft.

:param v: `(meter · second⁻¹)['airspeed', 'true', 'cruise']`
:param l_over_d: `ratio[`newton[_Tensor(rank=1), 'lift']` to `newton[_Tensor(rank=1), 'drag']`]`
:param isp: `second['specific_impulse']`
:param wi_over_wf: `ratio[`kilogram['aircraft', 'takeoff']` to `kilogram['aircraft', 'landing']`]`
:returns: `meter['distance']`
# --8<-- [end:breguet_output]
"""


# %%
# --8<-- [start:dataclass_example]
@sphinx_doc
@dataclass
class AircraftParams:
    """Aircraft performance parameters."""

    l_over_d: LOverD
    specific_impulse: SIsp


print(AircraftParams.__doc__)
# --8<-- [end:dataclass_example]
"""
# --8<-- [start:dataclass_output]
Aircraft performance parameters.

:param l_over_d: `ratio[`newton[_Tensor(rank=1), 'lift']` to `newton[_Tensor(rank=1), 'drag']`]`
:param specific_impulse: `second['specific_impulse']`
# --8<-- [end:dataclass_output]
"""
# %%
