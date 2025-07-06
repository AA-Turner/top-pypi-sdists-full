"""
Dynamic nonlinear period-by-period simulator
"""


#[

from __future__ import annotations

import numpy as _np
import scipy as _sp

from .. import equations as _equations
from .. import wrongdoings as _wrongdoings
from .. import frames as _frames
from ..simultaneous import main as _simultaneous
from ..plans.simulation_plans import SimulationPlan
from ..dataslates.main import Dataslate
from ..fords import terminators as _terminators

from . import _evaluators as _evaluators
from ..stacked_time import simulators as _stacked_time_simulators

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from numbers import Real
    from typing import Callable, Any, Literal
    from ..dates import Period
    from ..frames import Frame
    from ..incidences.main import Token

#]


METHOD_NAME = "period_by_period"


def create_frames(
    model_v: Simultaneous,
    dataslate_v: Dataslate,
    plan: SimulationPlan | None,
    **kwargs,
) -> tuple[Frame, ...]:
    """
    """
    #[
    base_break_points = _frames.create_empty_base_break_points(dataslate_v, )
    base_break_points[:] = True
    base_end = dataslate_v.base_periods[-1]
    return _frames.split_into_frames_by_breakpoints(
        base_break_points, dataslate_v,
        get_simulation_end=lambda start, end: end,
    )
    #]


def simulate_initial_guess(
    *args,
    initial_guess: Literal["first_order", "data"] = "data",
    **kwargs,
) -> None:
    """
    """
    return _stacked_time_simulators.simulate_initial_guess(
        *args,
        initial_guess=initial_guess,
        **kwargs,
    )


def simulate_frame(
    model_v: Simultaneous,
    frame_ds: Dataslate,
    *,
    frame: Frame,
    **kwargs,
) -> dict[str, Any]:
    """
    """
    is_first_frame = frame_ds.base_columns[0] == frame.first
    return _stacked_time_simulators.simulate_frame(
        model_v,
        frame_ds,
        frame=frame,
        **kwargs,
        terminal="data",
        _precatch_missing=_precatch_missing_first_frame if is_first_frame else _precatch_missing,
    )


def _setup_current_period(
    plan: SimulationPlan | None,
    create_evaluator: Callable,
    current_wrt_qids: tuple[int, ...],
    current_period: Period,
    name_to_qid: dict[str, int],
    /,
) -> tuple[tuple[int, ...], PeriodEvaluator]:
    """
    """
    current_wrt_qids = tuple(current_wrt_qids)
    if plan:
        names_exogenized = plan.get_exogenized_unanticipated_in_period(current_period, )
        names_endogenized = plan.get_endogenized_unanticipated_in_period(current_period, )
        if len(names_exogenized) != len(names_endogenized):
            raise _wrongdoings.IrisPieCritical(
                f"Number of exogenized quantities {len(names_exogenized)}"
                f" does not match number of endogenized quantities {len(names_endogenized)}"
                f" in period {current_period}"
            )
        qids_exogenized = tuple(name_to_qid[name] for name in names_exogenized)
        qids_endogenized = tuple(name_to_qid[name] for name in names_endogenized)
        current_wrt_qids = tuple(sorted(set(current_wrt_qids).difference(qids_exogenized).union(qids_endogenized)))
    current_evaluator = create_evaluator(current_wrt_qids, )
    return current_wrt_qids, current_evaluator


def _initial_guess_previous_period(
    data: _np.ndarray,
    wrt_qids: tuple[int, ...],
    t: int,
) -> _np.ndarray:
    """
    """
    source_t = t - 1 if t > 0 else 0
    return data[wrt_qids, source_t]


def _initial_guess_data(
    data: _np.ndarray,
    wrt_qids: tuple[int, ...],
    t: int,
) -> _np.ndarray:
    """
    """
    return data[wrt_qids, t]


def _catch_missing(
    data: _np.ndarray,
    t: int,
    /,
    frame_ds: Dataslate,
    qid_to_name: dict[int, str],
    fallback_value: Real,
    when_missing_stream: _wrongdoings.Stream,
) -> None:
    """
    """
    missing = _np.isnan(data[:, t])
    if not missing.any():
        return
    #
    data[missing, t] = fallback_value
    #
    current_period = frame_ds.periods[t]
    shift = 0
    for qid in _np.flatnonzero(missing):
        when_missing_stream.add(
            f"{qid_to_name[qid]}[{current_period+shift}]"
            f" when simulating {current_period}"
        )


def _catch_fail(
    when_fails_stream,
    root_final: _sp.optimize.OptimizeResult,
    period: Period,
) -> None:
    """
    """
    when_fails_stream.add(
        f"Simulation failed in {period} with message: {root_final.message}"
    )


def _create_custom_header(
    vid: str,
    t: int,
    current_period: int,
) -> str:
    """
    """
    return f"[Variant {vid}][Period {current_period}]"


def _get_wrt_qids(
    model_v,
    name_to_qid: dict[str, int],
    /,
) -> tuple[int, ...]:
    """
    """
    plannable = model_v.get_simulation_plannable()
    wrt_names \
        = tuple(plannable.can_be_exogenized_unanticipated) \
        + tuple(plannable.can_be_exogenized_anticipated)
    wrt_qids = sorted(
        name_to_qid[name]
        for name in set(wrt_names)
    )
    return wrt_qids


_INITIAL_GUESS = {
    "previous_period": _initial_guess_previous_period,
    "data": _initial_guess_data,
}


_DEFAULT_SOLVER_SETTINGS = {
    "method": "hybr",
    "tol": 1e-12,
    "options": {"xtol": 1e-12, },
}


def _precatch_missing(
    data: _np.ndarray,
    wrt_spots: Iterable[Token],
) -> None:
    """
    In the second and subsequent periods, always copy the previous period's
    values for endogenous quantities
    """
    for qid, column in wrt_spots:
        if column == 0:
            continue
        data[qid, column] = data[qid, column-1]


def _precatch_missing_first_frame(
    data: _np.ndarray,
    wrt_spots: Iterable[Token],
) -> None:
    """
    In the first period, copy the previous period's values for endogenous
    quantities only if they are NaN
    """
    for qid, column in wrt_spots:
        if column == 0 or not _np.isnan(data[qid, column]):
            continue
        data[qid, column] = data[qid, column-1]

