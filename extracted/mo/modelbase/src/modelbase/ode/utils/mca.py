from __future__ import annotations

__all__ = [
    "get_compound_elasticities_array",
    "get_compound_elasticities_df",
    "get_compound_elasticity",
    "get_concentration_response_coefficient",
    "get_concentration_response_coefficients_array",
    "get_concentration_response_coefficients_df",
    "get_flux_response_coefficient",
    "get_flux_response_coefficients_array",
    "get_flux_response_coefficients_df",
    "get_parameter_elasticities_array",
    "get_parameter_elasticities_df",
    "get_parameter_elasticity",
    "get_response_coefficients",
    "get_response_coefficients_array",
    "get_response_coefficients_df",
    "plot_coefficient_heatmap",
    "plot_concentration_response_coefficients",
    "plot_flux_response_coefficients",
    "plot_multiple",
]
import math
import sys
import warnings
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from typing import (
    TYPE_CHECKING,
    Any,
    Iterable,
    cast,
)

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import cm
from tqdm.auto import tqdm

from modelbase.ode.simulators import Simulator
from modelbase.typing import Array, ArrayLike, Axes, Axis
from modelbase.utils.plotting import get_norm as _get_norm
from modelbase.utils.plotting import (
    heatmap_from_dataframe as _heatmap_from_dataframe,
)

if TYPE_CHECKING:
    from matplotlib.collections import QuadMesh
    from matplotlib.figure import Figure

    from modelbase.ode.models import Model

_DISPLACEMENT = 1e-4
_DEFAULT_TOLERANCE = 1e-8


###############################################################################
# Non-steady state
###############################################################################


def get_compound_elasticity(
    model: Model,
    compound: str,
    y: dict[str, float],
    t: float = 0,
    normalized: bool = True,
    displacement: float = _DISPLACEMENT,
) -> Array:
    """Get sensitivity of all rates to a change of the concentration of a compound.

    Also called epsilon-elasticities. Not in steady state!
    """
    fcd = model.get_full_concentration_dict(y=y, t=t)
    old_concentration = fcd[compound]
    fluxes = []
    for new_concentration in (
        old_concentration * (1 + displacement),
        old_concentration * (1 - displacement),
    ):
        fcd[compound] = new_concentration
        fluxes.append(model.get_fluxes_array(y=fcd, t=t))
    elasticity_coef = (fluxes[0] - fluxes[1]) / (2 * displacement * old_concentration)
    if normalized:
        fcd[compound] = old_concentration
        flux_array = model.get_fluxes_array(y=fcd, t=t)
        elasticity_coef *= old_concentration / flux_array
    return cast(Array, np.atleast_1d(np.squeeze(elasticity_coef)))


def get_compound_elasticities_array(
    model: Model,
    compounds: list[str],
    y: dict[str, float],
    t: float = 0,
    *,
    normalized: bool = True,
    displacement: float = _DISPLACEMENT,
) -> Array:
    """Get sensitivity of all rates to a change of the concentration of multiple compounds.

    Also called epsilon-elasticities. Not in steady state!
    """
    elasticities = np.full(
        shape=(len(compounds), len(model.get_rate_names())), fill_value=np.nan
    )
    for i, compound in enumerate(compounds):
        elasticities[i] = get_compound_elasticity(
            model=model,
            compound=compound,
            y=y,
            t=t,
            normalized=normalized,
            displacement=displacement,
        )
    return elasticities


def get_compound_elasticities_df(
    model: Model,
    compounds: list[str],
    y: dict[str, float],
    t: float = 0,
    *,
    normalized: bool = True,
    displacement: float = _DISPLACEMENT,
) -> pd.DataFrame:
    """Get sensitivity of all rates to a change of the concentration of multiple compounds.

    Also called epsilon-elasticities. Not in steady state!
    """
    array = get_compound_elasticities_array(
        model=model,
        compounds=compounds,
        y=y,
        t=t,
        normalized=normalized,
        displacement=displacement,
    )
    return pd.DataFrame(data=array, index=compounds, columns=model.get_rate_names())


def get_parameter_elasticity(
    model: Model,
    parameter: str,
    y: dict[str, float],
    t: float = 0,
    *,
    normalized: bool = True,
    displacement: float = _DISPLACEMENT,
) -> Array:
    """Get sensitivity of all rates to a change of a parameter value.

    Also called pi-elasticities. Not in steady state!
    """
    model_copy: Model = model.copy()
    old_value = model_copy.get_parameter(parameter_name=parameter)
    fluxes = []
    for new_value in [old_value * (1 + displacement), old_value * (1 - displacement)]:
        model_copy.update_parameter(parameter_name=parameter, parameter_value=new_value)
        fluxes.append(model_copy.get_fluxes_array(y=y, t=t))
    elasticity_coef = (fluxes[0] - fluxes[1]) / (2 * displacement * old_value)
    if normalized:
        model_copy.update_parameter(parameter_name=parameter, parameter_value=old_value)
        fluxes_array = model_copy.get_fluxes_array(y=y, t=t)
        elasticity_coef *= old_value / fluxes_array
    return cast(Array, np.atleast_1d(np.squeeze(elasticity_coef)))


def get_parameter_elasticities_array(
    model: Model,
    parameters: list[str],
    y: dict[str, float],
    t: float = 0,
    *,
    normalized: bool = True,
    displacement: float = _DISPLACEMENT,
) -> Array:
    """Get sensitivity of all rates to a change of multiple parameter values.

    Also called pi-elasticities. Not in steady state!
    """
    elasticities = np.full(
        shape=(len(parameters), len(model.get_rate_names())), fill_value=np.nan
    )
    for i, parameter in enumerate(parameters):
        elasticities[i] = get_parameter_elasticity(
            model=model,
            parameter=parameter,
            y=y,
            t=t,
            normalized=normalized,
            displacement=displacement,
        )
    return elasticities


def get_parameter_elasticities_df(
    model: Model,
    parameters: list[str],
    y: dict[str, float],
    t: float = 0,
    *,
    normalized: bool = True,
    displacement: float = _DISPLACEMENT,
) -> pd.DataFrame:
    """Get sensitivity of all rates to a change of multiple parameter values.

    Also called pi-elasticities. Not in steady state!
    """
    matrix = get_parameter_elasticities_array(
        model=model,
        parameters=parameters,
        y=y,
        t=t,
        normalized=normalized,
        displacement=displacement,
    )
    return pd.DataFrame(matrix, index=parameters, columns=model.get_rate_names())


###############################################################################
# Steady state
###############################################################################


def _find_steady_state(
    *,
    model: Model,
    y0: ArrayLike | dict[str, float],
    tolerance: float,
    simulation_kwargs: dict[str, Any] | None,
    rel_norm: bool = False,
    **integrator_kwargs: dict[str, Any],
) -> tuple[Array | None, Array | None]:
    """Simulate the system to steadt state."""
    s = Simulator(model=model)
    s.initialise(y0=y0, test_run=False)
    t, y = s.simulate_to_steady_state(
        tolerance=tolerance,
        simulation_kwargs=simulation_kwargs,
        rel_norm=rel_norm,
        **integrator_kwargs,
    )
    return t, y


def get_response_coefficients(
    model: Model,
    parameter: str,
    y: dict[str, float] | Array | list,
    *,
    normalized: bool = True,
    displacement: float = _DISPLACEMENT,
    tolerance: float = _DEFAULT_TOLERANCE,
    simulation_kwargs: dict[str, Any] | None = None,
    rel_norm: bool = False,
    **integrator_kwargs: dict[str, Any],
) -> tuple[Array | None, Array | None]:
    """Get response of the steady state concentrations and fluxes to a change of the given parameter."""
    model_copy: Model = model.copy()
    old_value = model_copy.get_parameter(parameter_name=parameter)
    if normalized:
        t_ss, y_ss = _find_steady_state(
            model=model_copy,
            y0=y,
            tolerance=tolerance,
            simulation_kwargs=simulation_kwargs,
            rel_norm=rel_norm,
            **integrator_kwargs,
        )
        if t_ss is None or y_ss is None:
            return None, None
        fluxes_array_norm = model_copy.get_fluxes_array(y=y_ss, t=t_ss)
        fcd = model_copy.get_full_concentration_dict(y_ss)
        del fcd["time"]
        y_ss_norm = old_value / np.fromiter(fcd.values(), dtype="float")
        fluxes_array_norm = old_value / fluxes_array_norm

    ss: list[Array] = []
    fluxes: list[Array] = []
    for new_value in [
        old_value * (1 + displacement),
        old_value * (1 - displacement),
    ]:
        model_copy.update_parameter(parameter_name=parameter, parameter_value=new_value)
        t_ss, y_ss = _find_steady_state(
            model=model_copy,
            y0=y,
            tolerance=tolerance,
            simulation_kwargs=simulation_kwargs,
            rel_norm=rel_norm,
            **integrator_kwargs,
        )
        if t_ss is None or y_ss is None:
            return None, None
        fcd = model_copy.get_full_concentration_dict(y_ss)
        del fcd["time"]
        ss.append(np.fromiter(fcd.values(), dtype="float"))
        fluxes.append(model_copy.get_fluxes_array(y=y_ss, t=t_ss))

    conc_resp_coef: Array = (ss[0] - ss[1]) / (2 * displacement * old_value)
    flux_resp_coef: Array = (fluxes[0] - fluxes[1]) / (2 * displacement * old_value)

    if normalized:
        conc_resp_coef *= y_ss_norm  # type: ignore
        flux_resp_coef *= fluxes_array_norm  # type: ignore
    return np.atleast_1d(np.squeeze(conc_resp_coef)), np.atleast_1d(
        np.squeeze(flux_resp_coef)
    )


def get_response_coefficients_array(
    model: Model,
    parameters: list[str],
    y: dict[str, float],
    *,
    normalized: bool = True,
    displacement: float = _DISPLACEMENT,
    tolerance: float = _DEFAULT_TOLERANCE,
    disable_tqdm: bool = False,
    multiprocessing: bool = True,
    max_workers: int | None = None,
    rel_norm: bool = False,
    simulation_kwargs: dict[str, Any] | None = None,
    **integrator_kwargs: dict[str, Any],
) -> tuple[Array, Array]:
    """Get response of the steady state concentrations and fluxes to a change of the given parameter."""
    if sys.platform in ["win32", "cygwin"] and multiprocessing:
        warnings.warn(
            """
                Windows does not behave well with multiple processes.
                Falling back to threading routine."""
        )

    crcs = np.full(
        shape=(len(parameters), len(model.get_all_compounds())), fill_value=np.nan
    )
    frcs = np.full(
        shape=(len(parameters), len(model.get_rate_names())), fill_value=np.nan
    )
    _get_response_coefficients = partial(
        get_response_coefficients,
        model,
        y=y,
        normalized=normalized,
        displacement=displacement,
        tolerance=tolerance,
        simulation_kwargs=simulation_kwargs,
        rel_norm=rel_norm,
        **integrator_kwargs,
    )

    rcs: Iterable[tuple[Array | None, Array | None]]
    if sys.platform in ["win32", "cygwin"] or not multiprocessing:
        rcs = tqdm(
            map(_get_response_coefficients, parameters),
            disable=disable_tqdm,
            total=len(parameters),
        )
    else:
        with ProcessPoolExecutor(max_workers=max_workers) as pe:
            rcs = tqdm(
                pe.map(_get_response_coefficients, parameters),
                disable=disable_tqdm,
                total=len(parameters),
            )

    for i, (crc, frc) in enumerate(rcs):
        crcs[i] = crc
        frcs[i] = frc
    return crcs, frcs


def get_response_coefficients_df(
    model: Model,
    parameters: list[str],
    y: dict[str, float],
    *,
    normalized: bool = True,
    displacement: float = _DISPLACEMENT,
    tolerance: float = _DEFAULT_TOLERANCE,
    disable_tqdm: bool = False,
    multiprocessing: bool = True,
    max_workers: int | None = None,
    rel_norm: bool = False,
    simulation_kwargs: dict[str, Any] | None = None,
    **integrator_kwargs: dict[str, Any],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Get response of the steady state concentrations and fluxes to a change of the given parameter."""
    crcs, frcs = get_response_coefficients_array(
        model=model,
        parameters=parameters,
        y=y,
        normalized=normalized,
        displacement=displacement,
        tolerance=tolerance,
        simulation_kwargs=simulation_kwargs,
        disable_tqdm=disable_tqdm,
        multiprocessing=multiprocessing,
        max_workers=max_workers,
        rel_norm=rel_norm,
        **integrator_kwargs,
    )
    crcs_df = pd.DataFrame(
        data=crcs,
        index=parameters,
        columns=model.get_all_compounds(),
    )
    frcs_df = pd.DataFrame(
        data=frcs,
        index=parameters,
        columns=model.get_rate_names(),
    )
    return crcs_df, frcs_df


def get_concentration_response_coefficient(
    model: Model,
    parameter: str,
    y: dict[str, float],
    *,
    normalized: bool = True,
    displacement: float = _DISPLACEMENT,
    tolerance: float = _DEFAULT_TOLERANCE,
    simulation_kwargs: dict[str, Any] | None = None,
    rel_norm: bool = False,
    **integrator_kwargs: dict[str, Any],
) -> Array | None:
    """Get response of the steady state concentrations to a change of the given parameter."""
    return get_response_coefficients(
        model=model,
        parameter=parameter,
        y=y,
        normalized=normalized,
        displacement=displacement,
        tolerance=tolerance,
        simulation_kwargs=simulation_kwargs,
        rel_norm=rel_norm,
        **integrator_kwargs,
    )[0]


def get_concentration_response_coefficients_array(
    model: Model,
    parameters: list[str],
    y: dict[str, float],
    *,
    normalized: bool = True,
    displacement: float = _DISPLACEMENT,
    tolerance: float = _DEFAULT_TOLERANCE,
    disable_tqdm: bool = False,
    multiprocessing: bool = True,
    max_workers: int | None = None,
    rel_norm: bool = False,
    simulation_kwargs: dict[str, Any] | None = None,
    **integrator_kwargs: dict[str, Any],
) -> Array:
    """Get response of the steady state concentrations to a change of the given parameters."""
    return get_response_coefficients_array(
        model=model,
        parameters=parameters,
        y=y,
        normalized=normalized,
        displacement=displacement,
        tolerance=tolerance,
        multiprocessing=multiprocessing,
        max_workers=max_workers,
        simulation_kwargs=simulation_kwargs,
        disable_tqdm=disable_tqdm,
        rel_norm=rel_norm,
        **integrator_kwargs,
    )[0]


def get_concentration_response_coefficients_df(
    model: Model,
    parameters: list[str],
    y: dict[str, float],
    *,
    disable_tqdm: bool = False,
    normalized: bool = True,
    displacement: float = _DISPLACEMENT,
    tolerance: float = _DEFAULT_TOLERANCE,
    multiprocessing: bool = True,
    max_workers: int | None = None,
    rel_norm: bool = False,
    simulation_kwargs: dict[str, Any] | None = None,
    **integrator_kwargs: dict[str, Any],
) -> pd.DataFrame:
    """Get response of the steady state concentrations to a change of the given parameters"""
    return get_response_coefficients_df(
        model=model,
        parameters=parameters,
        y=y,
        normalized=normalized,
        displacement=displacement,
        tolerance=tolerance,
        multiprocessing=multiprocessing,
        max_workers=max_workers,
        simulation_kwargs=simulation_kwargs,
        disable_tqdm=disable_tqdm,
        rel_norm=rel_norm,
        **integrator_kwargs,
    )[0]


def get_flux_response_coefficient(
    model: Model,
    parameter: str,
    y: dict[str, float],
    *,
    normalized: bool = True,
    displacement: float = _DISPLACEMENT,
    tolerance: float = _DEFAULT_TOLERANCE,
    simulation_kwargs: dict[str, Any] | None = None,
    rel_norm: bool = False,
    **integrator_kwargs: dict[str, Any],
) -> Array | None:
    """Get response of the steady state fluxes to a change of the given parameter."""
    return get_response_coefficients(
        model=model,
        parameter=parameter,
        y=y,
        normalized=normalized,
        displacement=displacement,
        tolerance=tolerance,
        simulation_kwargs=simulation_kwargs,
        rel_norm=rel_norm,
        **integrator_kwargs,
    )[1]


def get_flux_response_coefficients_array(
    model: Model,
    parameters: list[str],
    y: dict[str, float],
    *,
    normalized: bool = True,
    displacement: float = _DISPLACEMENT,
    tolerance: float = _DEFAULT_TOLERANCE,
    disable_tqdm: bool = False,
    multiprocessing: bool = True,
    max_workers: int | None = None,
    rel_norm: bool = False,
    simulation_kwargs: dict[str, Any] | None = None,
    **integrator_kwargs: dict[str, Any],
) -> Array:
    """Get response of the steady state fluxes to a change of the given parameters."""
    return get_response_coefficients_array(
        model=model,
        parameters=parameters,
        y=y,
        normalized=normalized,
        displacement=displacement,
        tolerance=tolerance,
        multiprocessing=multiprocessing,
        max_workers=max_workers,
        simulation_kwargs=simulation_kwargs,
        disable_tqdm=disable_tqdm,
        rel_norm=rel_norm,
        **integrator_kwargs,
    )[1]


def get_flux_response_coefficients_df(
    model: Model,
    parameters: list[str],
    y: dict[str, float],
    *,
    normalized: bool = True,
    displacement: float = _DISPLACEMENT,
    tolerance: float = _DEFAULT_TOLERANCE,
    disable_tqdm: bool = False,
    multiprocessing: bool = True,
    max_workers: int | None = None,
    rel_norm: bool = False,
    simulation_kwargs: dict[str, Any] | None = None,
    **integrator_kwargs: dict[str, Any],
) -> pd.DataFrame:
    """Get response of the steady state fluxes to a change of the given parameters."""
    return get_response_coefficients_df(
        model=model,
        parameters=parameters,
        y=y,
        normalized=normalized,
        displacement=displacement,
        tolerance=tolerance,
        multiprocessing=multiprocessing,
        max_workers=max_workers,
        simulation_kwargs=simulation_kwargs,
        disable_tqdm=disable_tqdm,
        rel_norm=rel_norm,
        **integrator_kwargs,
    )[1]


def plot_coefficient_heatmap(
    df: pd.DataFrame,
    *,
    title: str,
    cmap: str = "RdBu_r",
    rows: list[str] | None = None,
    columns: list[str] | None = None,
    vmax: float | None = None,
    vmin: float | None = None,
    norm: plt.Normalize | None = None,  # type: ignore
    annotate: bool = True,
    colorbar: bool = True,
    xlabel: str | None = None,
    ylabel: str | None = None,
    ax: Axis | None = None,
    cax: Axis | None = None,
) -> tuple[Figure, Axis, QuadMesh]:
    """Plot the DataFrame of a response coefficient as a heatmap.

    Use the rows and columns arguments to only plot a subset of the data.
    """
    df = df.T.round(2)
    if rows is None:
        rows = df.index  # type: ignore
    if columns is None:
        columns = df.columns  # type: ignore
    fig, ax, hm = _heatmap_from_dataframe(
        df=df.loc[rows, columns],  # type: ignore
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
        annotate=annotate,
        colorbar=colorbar,
        cmap=cmap,
        norm=norm,
        vmax=vmax,
        vmin=vmin,
        ax=ax,
        cax=cax,
    )
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    return fig, ax, hm


def plot_multiple(
    dfs: list[pd.DataFrame],
    *,
    titles: list[str],
    cmap: str = "RdBu_r",
    annotate: bool = True,
    colorbar: bool = True,
    neutral_midpoint: bool = True,
    figsize: tuple[int, int] | None = None,
) -> tuple[Figure, Axes]:
    """Plot multiple heatmaps of the response coefficient DataFrames.

    See Also
    --------
    plot_coefficient_heatmap

    """
    vmin = min(i.values.min() for i in dfs)
    vmax = max(i.values.max() for i in dfs)
    if neutral_midpoint:
        total = max((abs(vmin), vmax))
        vmin = -total
        vmax = total

    n_cols = 2
    n_rows = math.ceil(len(dfs) / n_cols)

    norm = _get_norm(vmin=vmin, vmax=vmax)

    if figsize is None:
        figsize = (n_cols * 4, n_rows * 4)

    fig, axs = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=figsize, squeeze=False)
    axs = cast(Axes, axs)
    for ax, df, title in zip(axs.ravel(), dfs, titles):
        plot_coefficient_heatmap(
            df=df,
            title=title,
            cmap=cmap,
            annotate=annotate,
            colorbar=False,
            norm=norm,
            ax=ax,
        )

    # Add a colorbar+
    if colorbar:
        cb = fig.colorbar(
            cm.ScalarMappable(norm=norm, cmap=cmap),
            ax=axs.ravel()[-1],
        )
        cb.outline.set_linewidth(0)  # type: ignore
    fig.tight_layout()
    return fig, axs


def plot_concentration_response_coefficients(
    model: Model,
    parameters: list[str],
    y: dict[str, float],
    *,
    normalized: bool = True,
    displacement: float = _DISPLACEMENT,
    tolerance: float = _DEFAULT_TOLERANCE,
    disable_tqdm: bool = False,
    rel_norm: bool = False,
    simulation_kwargs: dict[str, Any] | None = None,
    cmap: str = "RdBu_r",
    rows: list[str] | None = None,
    columns: list[str] | None = None,
    vmax: float | None = None,
    vmin: float | None = None,
    annotate: bool = True,
    colorbar: bool = True,
    xlabel: str | None = None,
    ylabel: str | None = None,
    ax: Axis | None = None,
    cax: Axis | None = None,
    **integrator_kwargs: dict[str, Any],
) -> tuple[Figure, Axis, QuadMesh]:
    """Calculate and plot response of the steady state concentration to a change of the given parameters.

    See Also
    --------
    get_concentration_response_coefficients_df
    plot_coefficient_heatmap

    """
    df = get_concentration_response_coefficients_df(
        model=model,
        parameters=parameters,
        y=y,
        normalized=normalized,
        displacement=displacement,
        tolerance=tolerance,
        simulation_kwargs=simulation_kwargs,
        disable_tqdm=disable_tqdm,
        rel_norm=rel_norm,
        **integrator_kwargs,  # type: ignore
    )
    return plot_coefficient_heatmap(
        df=df,
        title="Concentration Response Coefficients",
        rows=rows,
        columns=columns,
        xlabel=xlabel,
        ylabel=ylabel,
        annotate=annotate,
        colorbar=colorbar,
        cmap=cmap,
        vmax=vmax,
        vmin=vmin,
        ax=ax,
        cax=cax,
    )


def plot_flux_response_coefficients(
    model: Model,
    parameters: list[str],
    y: dict[str, float],
    *,
    normalized: bool = True,
    displacement: float = _DISPLACEMENT,
    tolerance: float = _DEFAULT_TOLERANCE,
    disable_tqdm: bool = False,
    rel_norm: bool = False,
    simulation_kwargs: dict[str, Any] | None = None,
    cmap: str = "RdBu_r",
    rows: list[str] | None = None,
    columns: list[str] | None = None,
    vmax: float | None = None,
    vmin: float | None = None,
    annotate: bool = True,
    colorbar: bool = True,
    xlabel: str | None = None,
    ylabel: str | None = None,
    ax: Axis | None = None,
    cax: Axis | None = None,
    **integrator_kwargs: dict[str, Any],
) -> tuple[Figure, Axis, QuadMesh]:
    """Calculate and plot response of the steady state fluxes to a change of the given parameters.

    See Also
    --------
    get_flux_response_coefficients_df
    plot_coefficient_heatmap

    """
    df = get_flux_response_coefficients_df(
        model=model,
        parameters=parameters,
        y=y,
        normalized=normalized,
        displacement=displacement,
        tolerance=tolerance,
        simulation_kwargs=simulation_kwargs,
        disable_tqdm=disable_tqdm,
        rel_norm=rel_norm,
        **integrator_kwargs,  # type: ignore
    )
    return plot_coefficient_heatmap(
        df=df,
        title="Flux Response Coefficients",
        rows=rows,
        columns=columns,
        xlabel=xlabel,
        ylabel=ylabel,
        annotate=annotate,
        colorbar=colorbar,
        cmap=cmap,
        vmax=vmax,
        vmin=vmin,
        ax=ax,
        cax=cax,
    )
