from __future__ import annotations

__all__ = [
    "_BaseRateSimulator",
    "_BaseSimulator",
]

import copy
import json
import pickle
import sys
import warnings
from abc import ABC, abstractmethod
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Generic,
    Iterable,
    List,
    cast,
    overload,
)

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tqdm.auto import tqdm
from typing_extensions import Literal, Self

from modelbase.typing import Array, ArrayLike, Axes, Axis, Figure
from modelbase.utils.plotting import (
    _get_plot_kwargs,
    _style_subplot,
    plot,
    plot_grid,
)

from . import BASE_MODEL_TYPE, RATE_MODEL_TYPE

if TYPE_CHECKING:
    from modelbase.ode.integrators import AbstractIntegrator


class _BaseSimulator(Generic[BASE_MODEL_TYPE], ABC):
    def __init__(
        self,
        model: BASE_MODEL_TYPE,
        integrator: type[AbstractIntegrator],
        y0: ArrayLike | None = None,
        time: list[Array] | None = None,
        results: list[Array] | None = None,
    ) -> None:
        self.model = model
        self._integrator = integrator
        self.integrator: AbstractIntegrator | None = None

        # For restoring purposes
        self.y0 = y0
        self.time = time
        self.results = results

    def __reduce__(self) -> Any:
        """Pickle this class."""
        return (
            self.__class__,
            (
                self.model,
                self._integrator,
            ),
            (
                ("y0", self.y0),
                ("time", self.time),
                ("results", self.results),
            ),
        )

    def clear_results(self) -> None:
        """Clear simulation results."""
        self.time = None
        self.results = None
        if self.integrator is not None:
            self.integrator.reset()

    def _initialise_integrator(self, *, y0: ArrayLike) -> None:
        """Initialise the integrator.

        Required for assimulo, as it needs y0 to initialise
        """
        self.integrator = self._integrator(rhs=self.model._get_rhs, y0=y0)

    def get_integrator_params(self) -> dict[str, Any] | None:
        if self.integrator is None:
            return None
        return self.integrator.get_integrator_kwargs()

    @abstractmethod
    def copy(self) -> Any:
        """Create a copy."""

    def _normalise_split_array(
        self,
        *,
        split_array: list[Array],
        normalise: float | ArrayLike,
    ) -> list[Array]:
        if isinstance(normalise, (int, float)):
            return [i / normalise for i in split_array]
        if len(normalise) == len(split_array):
            return [
                i / np.reshape(j, (len(i), 1)) for i, j in zip(split_array, normalise)
            ]

        results = []
        start = 0
        end = 0
        for i in split_array:
            end += len(i)
            results.append(i / np.reshape(normalise[start:end], (len(i), 1)))
            start += end
        return results

    @abstractmethod
    def _test_run(self) -> None:
        """Perform a test step of the simulation in Python to get proper error handling."""

    def _save_simulation_results(
        self, *, time: Array, results: Array, skipfirst: bool
    ) -> None:
        if self.time is None or self.results is None:
            self.time = [time]
            self.results = [results]
        elif skipfirst:
            self.time.append(time[1:])
            self.results.append(results[1:, :])
        else:
            self.time.append(time)
            self.results.append(results)

    @overload
    def get_time(self, concatenated: Literal[False]) -> None | list[Array]:  # type: ignore
        # The type error here comes from List[Array] and Array overlapping
        # Can safely be ignore
        ...

    @overload
    def get_time(self, concatenated: Literal[True]) -> None | Array:
        ...

    @overload
    def get_time(self, concatenated: bool = True) -> None | Array:
        ...

    def get_time(self, concatenated: bool = True) -> None | Array | list[Array]:
        """Get simulation time.

        Returns
        -------
        time : numpy.array

        """
        if self.time is None:
            return None
        if concatenated:
            return np.concatenate(self.time, axis=0)  # type: ignore
        return self.time.copy()

    def simulate(
        self,
        t_end: float | None = None,
        steps: int | None = None,
        time_points: ArrayLike | None = None,
        **integrator_kwargs: dict[str, Any],
    ) -> tuple[Array | None, Array | None]:
        """Simulate the model."""
        if self.integrator is None:
            msg = "Initialise the simulator first."
            raise AttributeError(msg)

        if steps is not None and time_points is not None:
            warnings.warn(
                """
            You can either specify the steps or the time return points.
            I will use the time return points"""
            )
            if t_end is None:
                t_end = time_points[-1]
            time, results = self.integrator._simulate(
                t_end=t_end,
                time_points=time_points,
                **integrator_kwargs,  # type: ignore
            )
        elif time_points is not None:
            time, results = self.integrator._simulate(
                t_end=time_points[-1],
                time_points=time_points,
                **integrator_kwargs,  # type: ignore
            )
        elif steps is not None:
            if t_end is None:
                msg = "t_end must no be None"
                raise ValueError(msg)
            time, results = self.integrator._simulate(
                t_end=t_end,
                steps=steps,
                **integrator_kwargs,  # type: ignore
            )
        else:
            time, results = self.integrator._simulate(
                t_end=t_end,
                **integrator_kwargs,  # type: ignore
            )

        if time is None or results is None:
            return None, None
        time_array = np.array(time)
        results_array = np.array(results)
        self._save_simulation_results(
            time=time_array, results=results_array, skipfirst=True
        )
        return time_array, results_array

    def simulate_and(
        self,
        t_end: float | None = None,
        steps: int | None = None,
        time_points: ArrayLike | None = None,
        **integrator_kwargs: dict[str, Any],
    ) -> Self:
        self.simulate(
            t_end=t_end,
            steps=steps,
            time_points=time_points,
            **integrator_kwargs,
        )
        return self

    def simulate_to_steady_state(
        self,
        tolerance: float = 1e-6,
        simulation_kwargs: dict[str, Any] | None = None,
        rel_norm: bool = False,
        **integrator_kwargs: dict[str, Any],
    ) -> tuple[Array | None, Array | None]:
        """Simulate the model."""
        if self.integrator is None:
            msg = "Initialise the simulator first."
            raise AttributeError(msg)
        if simulation_kwargs is None:
            simulation_kwargs = {}
        time, results = self.integrator._simulate_to_steady_state(
            tolerance=tolerance,
            simulation_kwargs=simulation_kwargs,
            integrator_kwargs=integrator_kwargs,
            rel_norm=rel_norm,
        )
        if time is None or results is None:
            return None, None
        time_array = np.array([time])
        results_array = np.array([results])
        self._save_simulation_results(
            time=time_array, results=results_array, skipfirst=False
        )
        return time_array, results_array

    def simulate_to_steady_state_and(
        self,
        tolerance: float = 1e-6,
        simulation_kwargs: dict[str, Any] | None = None,
        rel_norm: bool = False,
        **integrator_kwargs: dict[str, Any],
    ) -> Self:
        self.simulate_to_steady_state(
            tolerance=tolerance,
            simulation_kwargs=simulation_kwargs,
            rel_norm=rel_norm,
            **integrator_kwargs,
        )
        return self

    @overload
    def get_results_array(  # type: ignore
        self,
        *,
        normalise: float | ArrayLike | None = None,
        concatenated: Literal[False],
    ) -> None | list[Array]:
        ...

    @overload
    def get_results_array(
        self,
        *,
        normalise: float | ArrayLike | None = None,
        concatenated: bool = True,
    ) -> None | Array:
        ...

    def get_results_array(
        self,
        *,
        normalise: float | ArrayLike | None = None,
        concatenated: bool = True,
    ) -> None | Array | list[Array]:
        """Get simulation results."""
        if self.results is None:
            return None

        results = self.results.copy()
        if normalise is not None:
            results = self._normalise_split_array(
                split_array=results, normalise=normalise
            )
        if concatenated:
            return np.concatenate(results, axis=0)  # type: ignore
        return results

    @overload
    def get_results_dict(  # type: ignore
        self,
        *,
        normalise: float | ArrayLike | None = None,
        concatenated: Literal[False],
    ) -> None | list[dict[str, Array]]:
        ...

    @overload
    def get_results_dict(
        self,
        *,
        normalise: float | ArrayLike | None = None,
        concatenated: Literal[True],
    ) -> None | dict[str, Array]:
        ...

    @overload
    def get_results_dict(
        self,
        *,
        normalise: float | ArrayLike | None = None,
        concatenated: bool = True,
    ) -> None | dict[str, Array]:
        ...

    def get_results_dict(
        self,
        *,
        normalise: float | ArrayLike | None = None,
        concatenated: bool = True,
    ) -> None | dict[str, Array] | list[dict[str, Array]]:
        """Get simulation results."""
        if concatenated:
            results = self.get_results_array(normalise=normalise, concatenated=True)
            if results is None:
                return None
            return dict(zip(self.model.get_compounds(), results.T))
        else:
            results_ = self.get_results_array(normalise=normalise, concatenated=False)
            if results_ is None:
                return None
            return [dict(zip(self.model.get_compounds(), i.T)) for i in results_]

    @overload
    def get_results_df(  # type: ignore
        self,
        *,
        normalise: float | ArrayLike | None = None,
        concatenated: Literal[False],
    ) -> None | list[pd.DataFrame]:
        ...

    @overload
    def get_results_df(
        self,
        *,
        normalise: float | ArrayLike | None = None,
        concatenated: Literal[True],
    ) -> None | pd.DataFrame:
        ...

    @overload
    def get_results_df(
        self,
        *,
        normalise: float | ArrayLike | None = None,
        concatenated: bool = True,
    ) -> None | pd.DataFrame:
        ...

    def get_results_df(
        self,
        *,
        normalise: float | ArrayLike | None = None,
        concatenated: bool = True,
    ) -> None | pd.DataFrame | list[pd.DataFrame]:
        """Get simulation results."""
        results = self.get_results_array(normalise=normalise, concatenated=concatenated)
        time = self.get_time(concatenated=concatenated)
        if results is None or time is None:
            return None
        if concatenated:
            return pd.DataFrame(
                data=results,
                index=self.get_time(),
                columns=self.model.get_compounds(),
            )
        return [
            pd.DataFrame(
                data=result,
                index=t,
                columns=self.model.get_compounds(),
            )
            for t, result in zip(time, results)
        ]

    def get_new_y0(self) -> dict[str, float] | None:
        if (res := self.get_results_df()) is None:
            return None
        return dict(res.iloc[-1])

    def store_results_to_file(self, filename: str, filetype: str = "json") -> None:
        """Store the simulation results into a json or pickle file.

        Parameters
        ----------
        filename
            The name of the pickle file
        filetype
            Output file type. Json or pickle.

        """
        if self.time is None or self.results is None:
            msg = "Cannot save results, since none are stored in the simulator"
            raise ValueError(
                msg
            )

        res = cast(
            Dict[str, Array], self.get_results_dict(concatenated=True)
        )  # cast is just typing annotation
        time = cast(
            Array, self.get_time(concatenated=True)
        )  # cast is just typing annotation
        res["time"] = time

        res = {k: v.tolist() for k, v in res.items()}
        if filetype == "json":
            if not filename.endswith(".json"):
                filename += ".json"
            with open(filename, "w") as f:
                json.dump(obj=res, fp=f)
        elif filetype == "pickle":
            if not filename.endswith(".p"):
                filename += ".p"
            with open(filename, "wb") as f:  # type: ignore
                pickle.dump(obj=res, file=f)  # type: ignore
        else:
            msg = "Can only save to json or pickle"
            raise ValueError(msg)

    def load_results_from_file(self, filename: str, filetype: str = "json") -> None:
        """Load simulation results from a json or pickle file.

        Parameters
        ----------
        filename
            The name of the pickle file
        filetype
            Input file type. Json or pickle.

        """
        if filetype == "json":
            with open(filename) as f:
                res: dict[str, Array] = json.load(fp=f)
        elif filetype == "pickle":
            with open(filename, "rb") as f:  # type: ignore
                res = pickle.load(file=f)  # type: ignore
        else:
            msg = "Can only save to json or pickle"
            raise ValueError(msg)
        res = {k: np.array(v) for k, v in res.items()}
        self.time = [res.pop("time")]
        cpds = np.array([v for k, v in res.items()]).reshape(
            (len(self.time[0]), len(self.model.get_compounds()))
        )
        self.results = [cpds]


class _BaseRateSimulator(Generic[RATE_MODEL_TYPE], _BaseSimulator[RATE_MODEL_TYPE]):  # type: ignore
    def __init__(
        self,
        model: RATE_MODEL_TYPE,
        integrator: type[AbstractIntegrator],
        y0: ArrayLike | None = None,
        time: list[Array] | None = None,
        results: list[Array] | None = None,
        parameters: list[dict[str, float]] | None = None,
    ) -> None:
        _BaseSimulator.__init__(
            self, model=model, integrator=integrator, y0=y0, time=time, results=results
        )
        self.full_results: list[Array] | None = None
        self.fluxes: list[Array] | None = None
        self.simulation_parameters = parameters

    def __reduce__(self) -> Any:
        """Pickle this class."""
        return (
            self.__class__,
            (
                self.model,
                self._integrator,
            ),
            (
                ("y0", self.y0),
                ("time", self.time),
                ("results", self.results),
                ("parameters", self.simulation_parameters),
            ),
        )

    def copy(self) -> Any:
        """Return a deepcopy of this class."""
        new = copy.deepcopy(self)
        if self.simulation_parameters is not None:
            new.simulation_parameters = self.simulation_parameters.copy()
        if self.fluxes is not None:
            new.fluxes = self.fluxes.copy()
        if self.full_results is not None:
            new.full_results = self.full_results.copy()
        if new.results is not None:
            new._initialise_integrator(y0=new.results[-1])
        elif new.y0 is not None:
            new.initialise(y0=new.y0, test_run=False)
        return new

    def clear_results(self) -> None:
        """Clear simulation results."""
        super().clear_results()
        self.full_results = None
        self.fluxes = None
        self.simulation_parameters = None

    def _test_run(self) -> None:
        """Test run of a single integration step to get proper error handling."""
        if not self.model.rates:
            msg = "Please set at least one rate for the integration"
            raise AttributeError(msg)

        if self.y0 is not None:
            y = self.model.get_full_concentration_dict(y=self.y0, t=0)
            self.model.get_fluxes_dict(y=y, t=0)
            self.model.get_right_hand_side(y=y, t=0)

    def initialise(
        self,
        y0: ArrayLike | dict[str, float],
        test_run: bool = True,
    ) -> Self:
        """Initialise the integrator."""
        if self.results is not None:
            self.clear_results()
        if isinstance(y0, dict):
            self.y0 = [y0[compound] for compound in self.model.get_compounds()]
        else:
            self.y0 = list(y0)
        self._initialise_integrator(y0=self.y0)

        if test_run:
            self._test_run()
        return self

    def update_parameter(
        self,
        parameter_name: str,
        parameter_value: float,
    ) -> Self:
        """Update a model parameter."""
        self.model.update_parameter(
            parameter_name=parameter_name,
            parameter_value=parameter_value,
        )
        return self

    def scale_parameter(
        self,
        parameter_name: str,
        factor: float,
        verbose: bool = False,
    ) -> Self:
        """Scale a model parameter."""
        self.model.scale_parameter(
            parameter_name=parameter_name,
            factor=factor,
            verbose=verbose,
        )
        return self

    def update_parameters(self, parameters: dict[str, float]) -> Self:
        """Update model parameters."""
        self.model.update_parameters(parameters=parameters)
        return self

    def _save_simulation_results(
        self, *, time: Array, results: Array, skipfirst: bool
    ) -> None:
        super()._save_simulation_results(time=time, results=results, skipfirst=skipfirst)
        if self.simulation_parameters is None:
            self.simulation_parameters = []
        self.simulation_parameters.append(self.model.get_parameters())

    def simulate(
        self,
        t_end: float | None = None,
        steps: int | None = None,
        time_points: ArrayLike | None = None,
        **integrator_kwargs: dict[str, Any],
    ) -> tuple[Array | None, Array | None]:
        """Simulate the model.

        You can either supply only a terminal time point, or additionally also the
        number of steps or exact time points for which values should be returned.

        Parameters
        ----------
        t_end
            Last point of the integration
        steps
            Number of integration time steps to be returned
        time_points
            Explicit time points which shall be returned
        integrator_kwargs : dict
            Integrator options

        """
        time, results = super().simulate(
            t_end=t_end,
            steps=steps,
            time_points=time_points,
            **integrator_kwargs,
        )
        self.full_results = None
        self.fluxes = None
        return time, results

    def simulate_to_steady_state(
        self,
        tolerance: float = 1e-8,
        simulation_kwargs: dict[str, Any] | None = None,
        rel_norm: bool = False,
        **integrator_kwargs: dict[str, Any],
    ) -> tuple[Array | None, Array | None]:
        """Simulate the model to steady state."""
        time, results = super().simulate_to_steady_state(
            tolerance=tolerance,
            simulation_kwargs=simulation_kwargs,
            rel_norm=rel_norm,
            **integrator_kwargs,
        )
        self.full_results = None
        self.fluxes = None
        return time, results

    def _calculate_fluxes(self) -> None:
        time = self.time
        results = self.results
        pars = self.simulation_parameters
        if time is None or results is None or pars is None:
            return

        fluxes = []
        for t, y, p in zip(time, results, pars):
            self.update_parameters(parameters=p)
            fluxes_array = self.model.get_fluxes_array(y=y, t=t)
            fluxes.append(fluxes_array)
        self.fluxes = fluxes

    @overload
    def get_fluxes_array(  # type: ignore
        self,
        *,
        normalise: float | ArrayLike | None = None,
        concatenated: Literal[False],
    ) -> list[Array] | None:
        ...

    @overload
    def get_fluxes_array(
        self,
        *,
        normalise: float | ArrayLike | None = None,
        concatenated: Literal[True],
    ) -> Array | None:
        ...

    @overload
    def get_fluxes_array(
        self,
        *,
        normalise: float | ArrayLike | None = None,
        concatenated: bool = True,
    ) -> Array | None:
        ...

    def get_fluxes_array(
        self,
        *,
        normalise: float | ArrayLike | None = None,
        concatenated: bool = True,
    ) -> Array | list[Array] | None:
        """Get the model fluxes for the simulation."""
        if self.time is None or self.results is None:
            return None
        if self.fluxes is None:
            self._calculate_fluxes()
        # Cast is ok
        fluxes = cast(List[Array], self.fluxes)
        if normalise is not None:
            fluxes = self._normalise_split_array(split_array=fluxes, normalise=normalise)
        if concatenated:
            return np.concatenate(fluxes, axis=0)  # type: ignore
        return fluxes

    @overload
    def get_fluxes_dict(  # type: ignore
        self,
        *,
        normalise: float | ArrayLike | None = None,
        concatenated: Literal[False],
    ) -> list[dict[str, Array]] | None:
        ...

    @overload
    def get_fluxes_dict(
        self,
        *,
        normalise: float | ArrayLike | None = None,
        concatenated: Literal[True],
    ) -> dict[str, Array] | None:
        ...

    @overload
    def get_fluxes_dict(
        self,
        *,
        normalise: float | ArrayLike | None = None,
        concatenated: bool = True,
    ) -> dict[str, Array] | None:
        ...

    def get_fluxes_dict(
        self,
        *,
        normalise: float | ArrayLike | None = None,
        concatenated: bool = True,
    ) -> dict[str, Array] | list[dict[str, Array]] | None:
        """Get the model fluxes for the simulation."""
        fluxes = self.get_fluxes_array(normalise=normalise, concatenated=concatenated)
        if fluxes is None:
            return None
        if concatenated:
            return dict(zip(self.model.rates, cast(Array, fluxes).T))
        return [dict(zip(self.model.rates, i.T)) for i in fluxes]

    @overload
    def get_fluxes_df(
        self,
        *,
        normalise: float | ArrayLike | None = None,
        concatenated: Literal[False],
    ) -> list[pd.DataFrame] | None:
        ...

    @overload
    def get_fluxes_df(
        self,
        *,
        normalise: float | ArrayLike | None = None,
        concatenated: Literal[True],
    ) -> pd.DataFrame | None:
        ...

    @overload
    def get_fluxes_df(
        self,
        *,
        normalise: float | ArrayLike | None = None,
        concatenated: bool = True,
    ) -> pd.DataFrame | None:
        ...

    def get_fluxes_df(
        self,
        *,
        normalise: float | ArrayLike | None = None,
        concatenated: bool = True,
    ) -> pd.DataFrame | list[pd.DataFrame] | None:
        """Get the model fluxes for the simulation."""
        fluxes = self.get_fluxes_array(normalise=normalise, concatenated=concatenated)
        time = self.get_time(concatenated=concatenated)
        if fluxes is None or time is None:
            return None
        if concatenated:
            return pd.DataFrame(
                data=fluxes,
                index=time,
                columns=self.model.get_rate_names(),
            )
        return [
            pd.DataFrame(
                data=flux,
                index=t,
                columns=self.model.get_rate_names(),
            )
            for t, flux in zip(time, fluxes)
        ]

    def get_results_and_fluxes_df(
        self,
    ) -> tuple[pd.DataFrame | None, pd.DataFrame | None]:
        return self.get_results_df(), self.get_fluxes_df()

    def get_full_results_and_fluxes_df(
        self,
        include_readouts: bool = True,
    ) -> tuple[pd.DataFrame | None, pd.DataFrame | None]:
        return (
            self.get_full_results_df(include_readouts=include_readouts),
            self.get_fluxes_df(),
        )

    def _calculate_full_results(self, include_readouts: bool) -> None:
        full_results = []
        for t, y, p in zip(self.time, self.results, self.simulation_parameters):  # type: ignore
            self.update_parameters(parameters=p)
            results = self.model.get_full_concentration_dict(
                y=y,
                t=t,
                include_readouts=include_readouts,
            )
            del results["time"]
            full_results.append(np.reshape(list(results.values()), (len(results), len(t))).T)  # type: ignore
        self.full_results = full_results

    @overload
    def get_full_results_array(  # type: ignore
        self,
        *,
        normalise: float | ArrayLike | None = None,
        concatenated: Literal[False],
        include_readouts: bool = True,
    ) -> list[Array] | None:
        ...

    @overload
    def get_full_results_array(
        self,
        *,
        normalise: float | ArrayLike | None = None,
        concatenated: Literal[True],
        include_readouts: bool = True,
    ) -> Array | None:
        ...

    @overload
    def get_full_results_array(
        self,
        *,
        normalise: float | ArrayLike | None = None,
        concatenated: bool = True,
        include_readouts: bool = True,
    ) -> Array | None:
        ...

    def get_full_results_array(
        self,
        *,
        normalise: float | ArrayLike | None = None,
        concatenated: bool = True,
        include_readouts: bool = True,
    ) -> Array | list[Array] | None:
        """Get simulation results and derived compounds.

        Returns
        -------
        results : numpy.array

        """
        if self.results is None or self.time is None:
            return None
        if self.full_results is None:
            self._calculate_full_results(include_readouts)
        # Cast is ok
        full_results = cast(List[Array], self.full_results).copy()
        if normalise is not None:
            full_results = self._normalise_split_array(
                split_array=full_results,
                normalise=normalise,
            )
        if concatenated:
            return np.concatenate(full_results, axis=0)  # type: ignore
        return full_results

    @overload
    def get_full_results_dict(  # type: ignore
        self,
        *,
        normalise: float | ArrayLike | None = None,
        concatenated: Literal[False],
        include_readouts: bool = True,
    ) -> list[dict[str, Array]] | None:
        ...

    @overload
    def get_full_results_dict(
        self,
        *,
        normalise: float | ArrayLike | None = None,
        concatenated: Literal[True],
        include_readouts: bool = True,
    ) -> dict[str, Array] | None:
        ...

    @overload
    def get_full_results_dict(
        self,
        *,
        normalise: float | ArrayLike | None = None,
        concatenated: bool = True,
        include_readouts: bool = True,
    ) -> dict[str, Array] | None:
        ...

    def get_full_results_dict(
        self,
        *,
        normalise: float | ArrayLike | None = None,
        concatenated: bool = True,
        include_readouts: bool = True,
    ) -> dict[str, Array] | list[dict[str, Array]] | None:
        """Get simulation results and derived compounds."""
        full_results = self.get_full_results_array(
            normalise=normalise,
            concatenated=concatenated,
            include_readouts=include_readouts,
        )
        if full_results is None:
            return None
        all_compounds = self.model.get_all_compounds()
        if concatenated:
            return dict(zip(all_compounds, cast(Array, full_results).T))
        return [dict(zip(all_compounds, i.T)) for i in full_results]

    @overload
    def get_full_results_df(
        self,
        *,
        normalise: float | ArrayLike | None = None,
        concatenated: Literal[False],
        include_readouts: bool = True,
    ) -> list[pd.DataFrame] | None:
        ...

    @overload
    def get_full_results_df(
        self,
        *,
        normalise: float | ArrayLike | None = None,
        concatenated: Literal[True],
        include_readouts: bool = True,
    ) -> pd.DataFrame | None:
        ...

    @overload
    def get_full_results_df(
        self,
        *,
        normalise: float | ArrayLike | None = None,
        concatenated: bool = True,
        include_readouts: bool = True,
    ) -> pd.DataFrame | None:
        ...

    def get_full_results_df(
        self,
        *,
        normalise: float | ArrayLike | None = None,
        concatenated: bool = True,
        include_readouts: bool = True,
    ) -> pd.DataFrame | list[pd.DataFrame] | None:
        """Get simulation results and derived compounds."""
        full_results = self.get_full_results_array(
            normalise=normalise,
            concatenated=concatenated,
            include_readouts=include_readouts,
        )
        time = self.get_time(concatenated=concatenated)
        if full_results is None or time is None:
            return None
        all_compounds = self.model.get_all_compounds() + list(
            self.model.get_readout_names()
        )

        if concatenated:
            return pd.DataFrame(data=full_results, index=time, columns=all_compounds)
        return [
            pd.DataFrame(data=res, index=t, columns=all_compounds)
            for t, res in zip(time, full_results)
        ]

    @overload
    def get_variable(  # type: ignore
        self,
        variable: str,
        *,
        normalise: float | ArrayLike | None = None,
        concatenated: Literal[False],
    ) -> list[Array] | None:
        ...

    @overload
    def get_variable(
        self,
        variable: str,
        *,
        normalise: float | ArrayLike | None = None,
        concatenated: Literal[True],
    ) -> Array | None:
        ...

    @overload
    def get_variable(
        self,
        variable: str,
        *,
        normalise: float | ArrayLike | None = None,
        concatenated: bool = True,
    ) -> Array | None:
        ...

    def get_variable(
        self,
        variable: str,
        *,
        normalise: float | ArrayLike | None = None,
        concatenated: bool = True,
    ) -> Array | list[Array] | None:
        """Get simulation results for a specific variable.

        Returns
        -------
        results : numpy.array

        """
        full_results_dict = self.get_full_results_dict(
            normalise=normalise, concatenated=concatenated
        )
        if full_results_dict is None:
            return None
        if concatenated:
            return cast(Dict[str, Array], full_results_dict)[variable]
        return [i[variable] for i in cast(List[Dict[str, Array]], full_results_dict)]

    @overload
    def get_variables(  # type: ignore
        self,
        variables: list[str],
        *,
        normalise: float | ArrayLike | None = None,
        concatenated: Literal[False],
    ) -> list[Array]:
        ...

    @overload
    def get_variables(
        self,
        variables: list[str],
        *,
        normalise: float | ArrayLike | None = None,
        concatenated: Literal[True],
    ) -> Array:
        ...

    @overload
    def get_variables(
        self,
        variables: list[str],
        *,
        normalise: float | ArrayLike | None = None,
        concatenated: bool = True,
    ) -> Array:
        ...

    def get_variables(
        self,
        variables: list[str],
        *,
        normalise: float | ArrayLike | None = None,
        concatenated: bool = True,
    ) -> Array | list[Array]:
        """Get simulation results for a specific variable."""
        full_results_df = self.get_full_results_df(
            normalise=normalise, concatenated=concatenated
        )
        if concatenated:
            full_results_df = cast(pd.DataFrame, full_results_df)
            return full_results_df.loc[:, variables].values  # type: ignore
        full_results_df = cast(List[pd.DataFrame], full_results_df)
        return [i.loc[:, variables].values for i in full_results_df]

    def get_right_hand_side(
        self,
        *,
        annotate_names: bool = True,
    ) -> pd.DataFrame:
        rhs = pd.DataFrame()
        for t, y, p in zip(self.time, self.results, self.simulation_parameters):  # type: ignore
            self.update_parameters(p)
            _rhs = [
                self.model.get_right_hand_side(y=yi, t=ti, annotate_names=annotate_names)
                for ti, yi in zip(t, y)
            ]
            rhs = pd.concat((rhs, pd.DataFrame(_rhs, index=t)))
        return rhs

    @staticmethod
    def _parameter_scan_worker(
        parameter_value: float,
        *,
        parameter_name: str,
        model: RATE_MODEL_TYPE,
        Sim: type[_BaseRateSimulator],
        integrator: type[AbstractIntegrator],
        tolerance: float,
        y0: list[float],
        integrator_kwargs: dict[str, Any],
        include_fluxes: bool,
        rel_norm: bool,
    ) -> tuple[float, dict[str, float], dict[str, float]]:
        m = model.copy()
        s = Sim(model=m, integrator=integrator)
        s.initialise(y0=y0, test_run=False)
        s.update_parameter(parameter_name=parameter_name, parameter_value=parameter_value)
        t, y = s.simulate_to_steady_state(
            tolerance=tolerance, rel_norm=rel_norm, **integrator_kwargs
        )
        if t is None or y is None:
            concentrations = dict(
                zip(
                    m.get_all_compounds(),  # type: ignore
                    np.full(len(m.get_all_compounds()), np.nan),  # type: ignore
                ),
            )
            fluxes = dict(
                zip(
                    m.get_rate_names(),  # type: ignore
                    np.full(len(m.get_rate_names()), np.nan),  # type: ignore
                ),
            )
            return parameter_value, concentrations, fluxes
        if include_fluxes:
            fluxes = dict(s.get_fluxes_df(concatenated=True).iloc[-1])  # type: ignore
        else:
            fluxes = {}
        concentrations = dict(s.get_full_results_df(concatenated=True).iloc[-1])  # type: ignore
        return parameter_value, concentrations, fluxes  # type: ignore

    def parameter_scan(
        self,
        parameter_name: str,
        parameter_values: ArrayLike,
        tolerance: float = 1e-8,
        multiprocessing: bool = True,
        max_workers: int | None = None,
        disable_tqdm: bool = False,
        rel_norm: bool = False,
        **integrator_kwargs: dict[str, Any],
    ) -> pd.DataFrame:
        """Scan the model steady state changes caused by a change to a parameter."""
        return self.parameter_scan_with_fluxes(
            parameter_name=parameter_name,
            parameter_values=parameter_values,
            tolerance=tolerance,
            multiprocessing=multiprocessing,
            max_workers=max_workers,
            disable_tqdm=disable_tqdm,
            rel_norm=rel_norm,
            **integrator_kwargs,
        )[0]

    def parameter_scan_with_fluxes(
        self,
        parameter_name: str,
        parameter_values: ArrayLike,
        tolerance: float = 1e-8,
        multiprocessing: bool = True,
        disable_tqdm: bool = False,
        max_workers: int | None = None,
        rel_norm: bool = False,
        **integrator_kwargs: dict[str, Any],
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Scan the model steady state changes caused by a change to a parameter."""
        if sys.platform in ["win32", "cygwin"]:
            warnings.warn(
                """
                Windows does not behave well with multiple processes.
                Falling back to threading routine."""
            )
        worker = partial(
            self._parameter_scan_worker,
            parameter_name=parameter_name,
            model=self.model,
            Sim=self.__class__,
            integrator=self._integrator,
            tolerance=tolerance,
            y0=self.y0,
            integrator_kwargs=integrator_kwargs,
            include_fluxes=True,
            rel_norm=rel_norm,
        )

        results: Iterable[tuple[float, dict[str, Array], dict[str, Array]]]
        if sys.platform in ["win32", "cygwin"] or not multiprocessing:
            results = tqdm(
                map(worker, parameter_values),
                total=len(parameter_values),
                desc=parameter_name,
                disable=disable_tqdm,
            )
        else:
            with ProcessPoolExecutor(max_workers=max_workers) as pe:
                results = tqdm(pe.map(worker, parameter_values))
        concentrations = {}
        fluxes = {}
        for i, conc, flux in results:
            concentrations[i] = conc
            fluxes[i] = flux
        return (
            pd.DataFrame(concentrations).T,
            pd.DataFrame(fluxes).T,
        )

    def parameter_scan_2d(
        self,
        p1: tuple[str, ArrayLike],
        p2: tuple[str, ArrayLike],
        tolerance: float = 1e-8,
        disable_tqdm: bool = False,
        multiprocessing: bool = True,
        max_workers: int | None = None,
        rel_norm: bool = False,
        **integrator_kwargs: dict[str, Any],
    ) -> dict[float, pd.DataFrame]:
        cs = {}
        parameter_name1, parameter_values1 = p1
        parameter_name2, parameter_values2 = p2
        original_pars = self.model.get_parameters().copy()
        for value in tqdm(
            parameter_values2, total=len(parameter_values2), desc=parameter_name2
        ):
            self.update_parameter(parameter_name2, value)
            cs[value] = self.parameter_scan(
                parameter_name1,
                parameter_values1,
                tolerance=tolerance,
                disable_tqdm=disable_tqdm,
                multiprocessing=multiprocessing,
                max_workers=max_workers,
                rel_norm=rel_norm,
                **integrator_kwargs,
            )
        self.update_parameters(original_pars)
        return cs

    def parameter_scan_2d_with_fluxes(
        self,
        p1: tuple[str, ArrayLike],
        p2: tuple[str, ArrayLike],
        tolerance: float = 1e-8,
        disable_tqdm: bool = False,
        multiprocessing: bool = True,
        max_workers: int | None = None,
        rel_norm: bool = False,
        **integrator_kwargs: dict[str, Any],
    ) -> tuple[dict[float, pd.DataFrame], dict[float, pd.DataFrame]]:
        cs = {}
        vs = {}
        parameter_name1, parameter_values1 = p1
        parameter_name2, parameter_values2 = p2
        original_pars = self.model.get_parameters().copy()
        for value in tqdm(
            parameter_values2, total=len(parameter_values2), desc=parameter_name2
        ):
            self.update_parameter(parameter_name2, value)
            c, v = self.parameter_scan_with_fluxes(
                parameter_name1,
                parameter_values1,
                tolerance=tolerance,
                multiprocessing=multiprocessing,
                disable_tqdm=disable_tqdm,
                max_workers=max_workers,
                rel_norm=rel_norm,
                **integrator_kwargs,  # type: ignore
            )
            cs[value] = c
            vs[value] = v
        self.update_parameters(original_pars)
        return cs, vs

    def plot_log(
        self,
        xlabel: str | None = None,
        ylabel: str | None = None,
        title: str | None = None,
        normalise: float | ArrayLike | None = None,
        grid: bool = True,
        tight_layout: bool = True,
        ax: Axis | None = None,
        figure_kwargs: dict[str, Any] | None = None,
        subplot_kwargs: dict[str, Any] | None = None,
        plot_kwargs: dict[str, Any] | None = None,
        grid_kwargs: dict[str, Any] | None = None,
        legend_kwargs: dict[str, Any] | None = None,
        tick_kwargs: dict[str, Any] | None = None,
        label_kwargs: dict[str, Any] | None = None,
        title_kwargs: dict[str, Any] | None = None,
    ) -> tuple[Figure | None, Axis | None]:
        compounds = self.model.get_compounds()
        y = cast(
            pd.DataFrame,
            self.get_full_results_df(normalise=normalise, concatenated=True),
        )
        if y is None:
            return None, None
        fig, ax = plot(
            plot_args=(y.loc[:, compounds],),
            legend=compounds,
            xlabel=xlabel,
            ylabel=ylabel,
            title=title,
            grid=grid,
            tight_layout=tight_layout,
            ax=ax,
            figure_kwargs=figure_kwargs,
            subplot_kwargs=subplot_kwargs,
            plot_kwargs=plot_kwargs,
            grid_kwargs=grid_kwargs,
            legend_kwargs=legend_kwargs,
            tick_kwargs=tick_kwargs,
            label_kwargs=label_kwargs,
            title_kwargs=title_kwargs,
        )
        ax.set_xscale("log")
        ax.set_yscale("log")
        return fig, ax

    def plot_semilog(
        self,
        log_axis: str = "y",
        xlabel: str | None = None,
        ylabel: str | None = None,
        title: str | None = None,
        normalise: float | ArrayLike | None = None,
        grid: bool = True,
        tight_layout: bool = True,
        ax: Axis | None = None,
        figure_kwargs: dict[str, Any] | None = None,
        subplot_kwargs: dict[str, Any] | None = None,
        plot_kwargs: dict[str, Any] | None = None,
        grid_kwargs: dict[str, Any] | None = None,
        legend_kwargs: dict[str, Any] | None = None,
        tick_kwargs: dict[str, Any] | None = None,
        label_kwargs: dict[str, Any] | None = None,
        title_kwargs: dict[str, Any] | None = None,
    ) -> tuple[Figure | None, Axis | None]:
        compounds = self.model.get_compounds()
        y = cast(
            pd.DataFrame,
            self.get_full_results_df(normalise=normalise, concatenated=True),
        )
        if y is None:
            return None, None
        fig, ax = plot(
            plot_args=(y.loc[:, compounds],),
            legend=compounds,
            xlabel=xlabel,
            ylabel=ylabel,
            title=title,
            grid=grid,
            tight_layout=tight_layout,
            ax=ax,
            figure_kwargs=figure_kwargs,
            subplot_kwargs=subplot_kwargs,
            plot_kwargs=plot_kwargs,
            grid_kwargs=grid_kwargs,
            legend_kwargs=legend_kwargs,
            tick_kwargs=tick_kwargs,
            label_kwargs=label_kwargs,
            title_kwargs=title_kwargs,
        )
        if log_axis == "y":
            ax.set_yscale("log")
        elif log_axis == "x":
            ax.set_xscale("log")
        else:
            msg = "log_axis must be either x or y"
            raise ValueError(msg)
        return fig, ax

    def plot_derived(
        self,
        xlabel: str | None = None,
        ylabel: str | None = None,
        title: str | None = None,
        normalise: float | ArrayLike | None = None,
        grid: bool = True,
        tight_layout: bool = True,
        ax: Axis | None = None,
        figure_kwargs: dict[str, Any] | None = None,
        subplot_kwargs: dict[str, Any] | None = None,
        plot_kwargs: dict[str, Any] | None = None,
        grid_kwargs: dict[str, Any] | None = None,
        legend_kwargs: dict[str, Any] | None = None,
        tick_kwargs: dict[str, Any] | None = None,
        label_kwargs: dict[str, Any] | None = None,
        title_kwargs: dict[str, Any] | None = None,
    ) -> tuple[Figure | None, Axis | None]:
        compounds = self.model.get_derived_compounds()
        y = cast(
            pd.DataFrame,
            self.get_full_results_df(normalise=normalise, concatenated=True),
        )
        if y is None:
            return None, None
        return plot(
            plot_args=(y.loc[:, compounds],),
            legend=compounds,
            xlabel=xlabel,
            ylabel=ylabel,
            title=title,
            grid=grid,
            tight_layout=tight_layout,
            ax=ax,
            figure_kwargs=figure_kwargs,
            subplot_kwargs=subplot_kwargs,
            plot_kwargs=plot_kwargs,
            grid_kwargs=grid_kwargs,
            legend_kwargs=legend_kwargs,
            tick_kwargs=tick_kwargs,
            label_kwargs=label_kwargs,
            title_kwargs=title_kwargs,
        )

    def plot_all(
        self,
        xlabel: str | None = None,
        ylabel: str | None = None,
        title: str | None = None,
        normalise: float | ArrayLike | None = None,
        grid: bool = True,
        tight_layout: bool = True,
        ax: Axis | None = None,
        figure_kwargs: dict[str, Any] | None = None,
        subplot_kwargs: dict[str, Any] | None = None,
        plot_kwargs: dict[str, Any] | None = None,
        grid_kwargs: dict[str, Any] | None = None,
        legend_kwargs: dict[str, Any] | None = None,
        tick_kwargs: dict[str, Any] | None = None,
        label_kwargs: dict[str, Any] | None = None,
        title_kwargs: dict[str, Any] | None = None,
    ) -> tuple[Figure | None, Axis | None]:
        compounds = self.model.get_all_compounds()
        y = cast(
            pd.DataFrame,
            self.get_full_results_df(normalise=normalise, concatenated=True),
        )
        if y is None:
            return None, None
        return plot(
            plot_args=(y.loc[:, compounds],),
            legend=compounds,
            xlabel=xlabel,
            ylabel=ylabel,
            title=title,
            grid=grid,
            tight_layout=tight_layout,
            ax=ax,
            figure_kwargs=figure_kwargs,
            subplot_kwargs=subplot_kwargs,
            plot_kwargs=plot_kwargs,
            grid_kwargs=grid_kwargs,
            legend_kwargs=legend_kwargs,
            tick_kwargs=tick_kwargs,
            label_kwargs=label_kwargs,
            title_kwargs=title_kwargs,
        )

    def plot_selection(
        self,
        compounds: list[str],
        xlabel: str | None = None,
        ylabel: str | None = None,
        title: str | None = None,
        normalise: float | ArrayLike | None = None,
        grid: bool = True,
        tight_layout: bool = True,
        ax: Axis | None = None,
        figure_kwargs: dict[str, Any] | None = None,
        subplot_kwargs: dict[str, Any] | None = None,
        plot_kwargs: dict[str, Any] | None = None,
        grid_kwargs: dict[str, Any] | None = None,
        legend_kwargs: dict[str, Any] | None = None,
        tick_kwargs: dict[str, Any] | None = None,
        label_kwargs: dict[str, Any] | None = None,
        title_kwargs: dict[str, Any] | None = None,
    ) -> tuple[Figure | None, Axis | None]:
        y = cast(
            pd.DataFrame,
            self.get_full_results_df(normalise=normalise, concatenated=True),
        )
        if y is None:
            return None, None
        return plot(
            plot_args=(y.loc[:, compounds],),
            legend=compounds,
            xlabel=xlabel,
            ylabel=ylabel,
            title=title,
            grid=grid,
            tight_layout=tight_layout,
            ax=ax,
            figure_kwargs=figure_kwargs,
            subplot_kwargs=subplot_kwargs,
            plot_kwargs=plot_kwargs,
            grid_kwargs=grid_kwargs,
            legend_kwargs=legend_kwargs,
            tick_kwargs=tick_kwargs,
            label_kwargs=label_kwargs,
            title_kwargs=title_kwargs,
        )

    def plot_grid(
        self,
        compound_groups: list[list[str]],
        ncols: int | None = None,
        sharex: bool = True,
        sharey: bool = True,
        xlabels: str | Iterable[str] | None = None,
        ylabels: str | Iterable[str] | None = None,
        normalise: float | ArrayLike | None = None,
        plot_titles: Iterable[str] | None = None,
        figure_title: str | None = None,
        grid: bool = True,
        tight_layout: bool = True,
        figure_kwargs: dict[str, Any] | None = None,
        subplot_kwargs: dict[str, Any] | None = None,
        plot_kwargs: dict[str, Any] | None = None,
        grid_kwargs: dict[str, Any] | None = None,
        legend_kwargs: dict[str, Any] | None = None,
        tick_kwargs: dict[str, Any] | None = None,
        label_kwargs: dict[str, Any] | None = None,
        title_kwargs: dict[str, Any] | None = None,
    ) -> tuple[Figure | None, Axes | None]:
        """Plot simulation results of the compound groups as a grid.

        Examples
        --------
        >>> plot_grid([["x1", "x2"], ["x3", "x4]])

        """
        y = cast(
            pd.DataFrame,
            self.get_full_results_df(normalise=normalise, concatenated=True),
        )
        if y is None:
            return None, None
        plot_groups = [(y.loc[:, compounds],) for compounds in compound_groups]
        return plot_grid(
            plot_groups=plot_groups,  # type: ignore
            legend_groups=compound_groups,
            ncols=ncols,
            sharex=sharex,
            sharey=sharey,
            xlabels=xlabels,
            ylabels=ylabels,
            figure_title=figure_title,
            plot_titles=plot_titles,
            grid=grid,
            tight_layout=tight_layout,
            figure_kwargs=figure_kwargs,
            subplot_kwargs=subplot_kwargs,
            plot_kwargs=plot_kwargs,
            grid_kwargs=grid_kwargs,
            legend_kwargs=legend_kwargs,
            tick_kwargs=tick_kwargs,
            label_kwargs=label_kwargs,
            title_kwargs=title_kwargs,
        )

    def plot_derivatives(
        self,
        compounds: list[str],
        xlabel: str | None = None,
        ylabel: str | None = None,
        title: str | None = None,
        grid: bool = True,
        tight_layout: bool = True,
        ax: Axis | None = None,
        figure_kwargs: dict[str, Any] | None = None,
        subplot_kwargs: dict[str, Any] | None = None,
        plot_kwargs: dict[str, Any] | None = None,
        grid_kwargs: dict[str, Any] | None = None,
        legend_kwargs: dict[str, Any] | None = None,
        tick_kwargs: dict[str, Any] | None = None,
        label_kwargs: dict[str, Any] | None = None,
        title_kwargs: dict[str, Any] | None = None,
    ) -> tuple[Figure | None, Axis | None]:
        rhs = self.get_right_hand_side(annotate_names=False)
        if len(rhs) == 0:
            return None, None

        return plot(
            plot_args=(rhs.loc[:, compounds],),
            legend=compounds,
            xlabel=xlabel,
            ylabel=ylabel,
            title=title,
            grid=grid,
            tight_layout=tight_layout,
            ax=ax,
            figure_kwargs=figure_kwargs,
            subplot_kwargs=subplot_kwargs,
            plot_kwargs=plot_kwargs,
            grid_kwargs=grid_kwargs,
            legend_kwargs=legend_kwargs,
            tick_kwargs=tick_kwargs,
            label_kwargs=label_kwargs,
            title_kwargs=title_kwargs,
        )

    def plot_against_variable(
        self,
        variable: str,
        xlabel: str | None = None,
        ylabel: str | None = None,
        title: str | None = None,
        grid: bool = True,
        tight_layout: bool = True,
        ax: Axis | None = None,
        figure_kwargs: dict[str, Any] | None = None,
        subplot_kwargs: dict[str, Any] | None = None,
        plot_kwargs: dict[str, Any] | None = None,
        grid_kwargs: dict[str, Any] | None = None,
        legend_kwargs: dict[str, Any] | None = None,
        tick_kwargs: dict[str, Any] | None = None,
        label_kwargs: dict[str, Any] | None = None,
        title_kwargs: dict[str, Any] | None = None,
    ) -> tuple[Figure | None, Axis | None]:
        if xlabel is None:
            xlabel = variable
        results = cast(pd.DataFrame, self.get_full_results_df(concatenated=True))
        if results is None:
            return None, None
        compounds = cast(List[str], self.model.get_compounds())
        x = results.loc[:, variable].values  # type: ignore
        y = results.loc[:, compounds].values
        return plot(
            plot_args=(x, y),
            legend=compounds,
            xlabel=xlabel,
            ylabel=ylabel,
            title=title,
            grid=grid,
            tight_layout=tight_layout,
            ax=ax,
            figure_kwargs=figure_kwargs,
            subplot_kwargs=subplot_kwargs,
            plot_kwargs=plot_kwargs,
            grid_kwargs=grid_kwargs,
            legend_kwargs=legend_kwargs,
            tick_kwargs=tick_kwargs,
            label_kwargs=label_kwargs,
            title_kwargs=title_kwargs,
        )

    def plot_derived_against_variable(
        self,
        variable: str,
        xlabel: str | None = None,
        ylabel: str | None = None,
        title: str | None = None,
        grid: bool = True,
        tight_layout: bool = True,
        ax: Axis | None = None,
        figure_kwargs: dict[str, Any] | None = None,
        subplot_kwargs: dict[str, Any] | None = None,
        plot_kwargs: dict[str, Any] | None = None,
        grid_kwargs: dict[str, Any] | None = None,
        legend_kwargs: dict[str, Any] | None = None,
        tick_kwargs: dict[str, Any] | None = None,
        label_kwargs: dict[str, Any] | None = None,
        title_kwargs: dict[str, Any] | None = None,
    ) -> tuple[Figure | None, Axis | None]:
        if xlabel is None:
            xlabel = variable
        results = cast(pd.DataFrame, self.get_full_results_df(concatenated=True))
        if results is None:
            return None, None
        compounds = cast(List[str], self.model.get_derived_compounds())
        x = results.loc[:, variable].values  # type: ignore
        y = results.loc[:, compounds].values
        return plot(
            plot_args=(x, y),
            legend=compounds,
            xlabel=xlabel,
            ylabel=ylabel,
            title=title,
            grid=grid,
            tight_layout=tight_layout,
            ax=ax,
            figure_kwargs=figure_kwargs,
            subplot_kwargs=subplot_kwargs,
            plot_kwargs=plot_kwargs,
            grid_kwargs=grid_kwargs,
            legend_kwargs=legend_kwargs,
            tick_kwargs=tick_kwargs,
            label_kwargs=label_kwargs,
            title_kwargs=title_kwargs,
        )

    def plot_all_against_variable(
        self,
        variable: str,
        xlabel: str | None = None,
        ylabel: str | None = None,
        title: str | None = None,
        grid: bool = True,
        tight_layout: bool = True,
        ax: Axis | None = None,
        figure_kwargs: dict[str, Any] | None = None,
        subplot_kwargs: dict[str, Any] | None = None,
        plot_kwargs: dict[str, Any] | None = None,
        grid_kwargs: dict[str, Any] | None = None,
        legend_kwargs: dict[str, Any] | None = None,
        tick_kwargs: dict[str, Any] | None = None,
        label_kwargs: dict[str, Any] | None = None,
        title_kwargs: dict[str, Any] | None = None,
    ) -> tuple[Figure | None, Axis | None]:
        if xlabel is None:
            xlabel = variable
        results = cast(pd.DataFrame, self.get_full_results_df(concatenated=True))
        if results is None:
            return None, None
        compounds = cast(List[str], self.model.get_all_compounds())
        x = results.loc[:, variable].values  # type: ignore
        y = results.loc[:, compounds].values
        return plot(
            plot_args=(x, y),
            legend=compounds,
            xlabel=xlabel,
            ylabel=ylabel,
            title=title,
            grid=grid,
            tight_layout=tight_layout,
            ax=ax,
            figure_kwargs=figure_kwargs,
            subplot_kwargs=subplot_kwargs,
            plot_kwargs=plot_kwargs,
            grid_kwargs=grid_kwargs,
            legend_kwargs=legend_kwargs,
            tick_kwargs=tick_kwargs,
            label_kwargs=label_kwargs,
            title_kwargs=title_kwargs,
        )

    def plot_selection_against_variable(
        self,
        compounds: Iterable[str],
        variable: str,
        xlabel: str | None = None,
        ylabel: str | None = None,
        title: str | None = None,
        grid: bool = True,
        tight_layout: bool = True,
        ax: Axis | None = None,
        figure_kwargs: dict[str, Any] | None = None,
        subplot_kwargs: dict[str, Any] | None = None,
        plot_kwargs: dict[str, Any] | None = None,
        grid_kwargs: dict[str, Any] | None = None,
        legend_kwargs: dict[str, Any] | None = None,
        tick_kwargs: dict[str, Any] | None = None,
        label_kwargs: dict[str, Any] | None = None,
        title_kwargs: dict[str, Any] | None = None,
    ) -> tuple[Figure | None, Axis | None]:
        if xlabel is None:
            xlabel = variable
        results = cast(pd.DataFrame, self.get_full_results_df(concatenated=True))
        if results is None:
            return None, None
        x = results.loc[:, variable].values  # type: ignore
        y = results.loc[:, compounds].values  # type: ignore
        return plot(
            plot_args=(x, y),
            legend=compounds,
            xlabel=xlabel,
            ylabel=ylabel,
            title=title,
            grid=grid,
            tight_layout=tight_layout,
            ax=ax,
            figure_kwargs=figure_kwargs,
            subplot_kwargs=subplot_kwargs,
            plot_kwargs=plot_kwargs,
            grid_kwargs=grid_kwargs,
            legend_kwargs=legend_kwargs,
            tick_kwargs=tick_kwargs,
            label_kwargs=label_kwargs,
            title_kwargs=title_kwargs,
        )

    def plot_fluxes(
        self,
        xlabel: str | None = None,
        ylabel: str | None = None,
        title: str | None = None,
        normalise: float | ArrayLike | None = None,
        grid: bool = True,
        tight_layout: bool = True,
        ax: Axis | None = None,
        figure_kwargs: dict[str, Any] | None = None,
        subplot_kwargs: dict[str, Any] | None = None,
        plot_kwargs: dict[str, Any] | None = None,
        grid_kwargs: dict[str, Any] | None = None,
        legend_kwargs: dict[str, Any] | None = None,
        tick_kwargs: dict[str, Any] | None = None,
        label_kwargs: dict[str, Any] | None = None,
        title_kwargs: dict[str, Any] | None = None,
    ) -> tuple[Figure | None, Axis | None]:
        rate_names = cast(List[str], self.model.get_rate_names())
        y = self.get_fluxes_df(normalise=normalise, concatenated=True)
        if y is None:
            return None, None
        y = cast(pd.DataFrame, y)
        return plot(
            plot_args=(y.loc[:, rate_names],),
            legend=rate_names,
            xlabel=xlabel,
            ylabel=ylabel,
            title=title,
            grid=grid,
            tight_layout=tight_layout,
            ax=ax,
            figure_kwargs=figure_kwargs,
            subplot_kwargs=subplot_kwargs,
            plot_kwargs=plot_kwargs,
            grid_kwargs=grid_kwargs,
            legend_kwargs=legend_kwargs,
            tick_kwargs=tick_kwargs,
            label_kwargs=label_kwargs,
            title_kwargs=title_kwargs,
        )

    def plot_flux_selection(
        self,
        rate_names: list[str],
        xlabel: str | None = None,
        ylabel: str | None = None,
        title: str | None = None,
        normalise: float | ArrayLike | None = None,
        grid: bool = True,
        tight_layout: bool = True,
        ax: Axis | None = None,
        figure_kwargs: dict[str, Any] | None = None,
        subplot_kwargs: dict[str, Any] | None = None,
        plot_kwargs: dict[str, Any] | None = None,
        grid_kwargs: dict[str, Any] | None = None,
        legend_kwargs: dict[str, Any] | None = None,
        tick_kwargs: dict[str, Any] | None = None,
        label_kwargs: dict[str, Any] | None = None,
        title_kwargs: dict[str, Any] | None = None,
    ) -> tuple[Figure | None, Axis | None]:
        y = self.get_fluxes_df(normalise=normalise, concatenated=True)
        if y is None:
            return None, None
        y = cast(pd.DataFrame, y)
        return plot(
            plot_args=(y.loc[:, rate_names],),
            legend=rate_names,
            xlabel=xlabel,
            ylabel=ylabel,
            title=title,
            grid=grid,
            tight_layout=tight_layout,
            ax=ax,
            figure_kwargs=figure_kwargs,
            subplot_kwargs=subplot_kwargs,
            plot_kwargs=plot_kwargs,
            grid_kwargs=grid_kwargs,
            legend_kwargs=legend_kwargs,
            tick_kwargs=tick_kwargs,
            label_kwargs=label_kwargs,
            title_kwargs=title_kwargs,
        )

    def plot_fluxes_grid(
        self,
        rate_groups: list[list[str]],
        ncols: int | None = None,
        sharex: bool = True,
        sharey: bool = True,
        xlabels: list[str] | None = None,
        ylabels: list[str] | None = None,
        normalise: float | ArrayLike | None = None,
        plot_titles: Iterable[str] | None = None,
        figure_title: str | None = None,
        grid: bool = True,
        tight_layout: bool = True,
        figure_kwargs: dict[str, Any] | None = None,
        subplot_kwargs: dict[str, Any] | None = None,
        plot_kwargs: dict[str, Any] | None = None,
        grid_kwargs: dict[str, Any] | None = None,
        legend_kwargs: dict[str, Any] | None = None,
        tick_kwargs: dict[str, Any] | None = None,
        label_kwargs: dict[str, Any] | None = None,
        title_kwargs: dict[str, Any] | None = None,
    ) -> tuple[Figure | None, Array | None]:
        """Plot simulation results of the compound groups as a grid.

        Examples
        --------
        >>> plot_fluxes_grid([["v1", "v2"], ["v3", "v4]])

        """
        fluxes = self.get_fluxes_df(normalise=normalise, concatenated=True)
        if fluxes is None:
            return None, None
        fluxes = cast(pd.DataFrame, fluxes)
        plot_groups = [(cast(Array, fluxes.loc[:, group]),) for group in rate_groups]
        return plot_grid(
            plot_groups=plot_groups,  # type: ignore
            legend_groups=rate_groups,
            ncols=ncols,
            sharex=sharex,
            sharey=sharey,
            xlabels=xlabels,
            ylabels=ylabels,
            figure_title=figure_title,
            plot_titles=plot_titles,
            grid=grid,
            tight_layout=tight_layout,
            figure_kwargs=figure_kwargs,
            subplot_kwargs=subplot_kwargs,
            plot_kwargs=plot_kwargs,
            grid_kwargs=grid_kwargs,
            legend_kwargs=legend_kwargs,
            tick_kwargs=tick_kwargs,
            label_kwargs=label_kwargs,
            title_kwargs=title_kwargs,
        )

    def plot_fluxes_against_variable(
        self,
        variable: str,
        xlabel: str | None = None,
        ylabel: str | None = None,
        title: str | None = None,
        grid: bool = True,
        tight_layout: bool = True,
        ax: Axis | None = None,
        figure_kwargs: dict[str, Any] | None = None,
        subplot_kwargs: dict[str, Any] | None = None,
        plot_kwargs: dict[str, Any] | None = None,
        grid_kwargs: dict[str, Any] | None = None,
        legend_kwargs: dict[str, Any] | None = None,
        tick_kwargs: dict[str, Any] | None = None,
        label_kwargs: dict[str, Any] | None = None,
        title_kwargs: dict[str, Any] | None = None,
    ) -> tuple[Figure | None, Axis | None]:
        if xlabel is None:
            xlabel = variable
        rate_names = cast(List[str], self.model.get_rate_names())
        x = self.get_variable(variable=variable)
        y = self.get_fluxes_df(concatenated=True)
        if x is None or y is None:
            return None, None
        y = cast(pd.DataFrame, y).loc[:, rate_names].values
        return plot(
            plot_args=(x, y),
            legend=rate_names,
            xlabel=xlabel,
            ylabel=ylabel,
            title=title,
            grid=grid,
            tight_layout=tight_layout,
            ax=ax,
            figure_kwargs=figure_kwargs,
            subplot_kwargs=subplot_kwargs,
            plot_kwargs=plot_kwargs,
            grid_kwargs=grid_kwargs,
            legend_kwargs=legend_kwargs,
            tick_kwargs=tick_kwargs,
            label_kwargs=label_kwargs,
            title_kwargs=title_kwargs,
        )

    def plot_flux_selection_against_variable(
        self,
        rate_names: list[str],
        variable: str,
        xlabel: str | None = None,
        ylabel: str | None = None,
        title: str | None = None,
        grid: bool = True,
        tight_layout: bool = True,
        ax: Axis | None = None,
        figure_kwargs: dict[str, Any] | None = None,
        subplot_kwargs: dict[str, Any] | None = None,
        plot_kwargs: dict[str, Any] | None = None,
        grid_kwargs: dict[str, Any] | None = None,
        legend_kwargs: dict[str, Any] | None = None,
        tick_kwargs: dict[str, Any] | None = None,
        label_kwargs: dict[str, Any] | None = None,
        title_kwargs: dict[str, Any] | None = None,
    ) -> tuple[Figure | None, Axis | None]:
        if xlabel is None:
            xlabel = variable
        x = self.get_variable(variable=variable)
        y = self.get_fluxes_df(concatenated=True)
        if x is None or y is None:
            return None, None
        y = cast(pd.DataFrame, y).loc[:, rate_names].values
        return plot(
            plot_args=(x, y),
            legend=rate_names,
            xlabel=xlabel,
            ylabel=ylabel,
            title=title,
            grid=grid,
            tight_layout=tight_layout,
            ax=ax,
            figure_kwargs=figure_kwargs,
            subplot_kwargs=subplot_kwargs,
            plot_kwargs=plot_kwargs,
            grid_kwargs=grid_kwargs,
            legend_kwargs=legend_kwargs,
            tick_kwargs=tick_kwargs,
            label_kwargs=label_kwargs,
            title_kwargs=title_kwargs,
        )

    def plot_phase_plane(
        self,
        cpd1: str,
        cpd2: str,
        xlabel: str | None = None,
        ylabel: str | None = None,
        title: str | None = None,
        grid: bool = True,
        tight_layout: bool = True,
        ax: Axis | None = None,
        figure_kwargs: dict[str, Any] | None = None,
        subplot_kwargs: dict[str, Any] | None = None,
        plot_kwargs: dict[str, Any] | None = None,
        grid_kwargs: dict[str, Any] | None = None,
        legend_kwargs: dict[str, Any] | None = None,
        tick_kwargs: dict[str, Any] | None = None,
        label_kwargs: dict[str, Any] | None = None,
        title_kwargs: dict[str, Any] | None = None,
    ) -> tuple[Figure | None, Axis | None]:
        if xlabel is None:
            xlabel = cpd1
        if ylabel is None:
            ylabel = cpd2
        x = self.get_variable(variable=cpd1)
        y = self.get_variable(variable=cpd2)
        if x is None or y is None:
            return None, None
        return plot(
            plot_args=(x, y),
            legend=None,
            xlabel=xlabel,
            ylabel=ylabel,
            title=title,
            grid=grid,
            tight_layout=tight_layout,
            ax=ax,
            figure_kwargs=figure_kwargs,
            subplot_kwargs=subplot_kwargs,
            plot_kwargs=plot_kwargs,
            grid_kwargs=grid_kwargs,
            legend_kwargs=legend_kwargs,
            tick_kwargs=tick_kwargs,
            label_kwargs=label_kwargs,
            title_kwargs=title_kwargs,
        )

    def plot_phase_space(
        self,
        cpd1: str,
        cpd2: str,
        cpd3: str,
        xlabel: str | None = None,
        ylabel: str | None = None,
        zlabel: str | None = None,
        title: str | None = None,
        grid: bool = True,
        tight_layout: bool = True,
        ax: Axis | None = None,
        figure_kwargs: dict[str, Any] | None = None,
        subplot_kwargs: dict[str, Any] | None = None,
        plot_kwargs: dict[str, Any] | None = None,
        grid_kwargs: dict[str, Any] | None = None,
        legend_kwargs: dict[str, Any] | None = None,
        tick_kwargs: dict[str, Any] | None = None,
        label_kwargs: dict[str, Any] | None = None,
        title_kwargs: dict[str, Any] | None = None,
    ) -> tuple[Figure | None, Axis | None]:
        kwargs = _get_plot_kwargs(
            figure_kwargs=figure_kwargs,
            subplot_kwargs=subplot_kwargs,
            plot_kwargs=plot_kwargs,
            grid_kwargs=grid_kwargs,
            tick_kwargs=tick_kwargs,
            label_kwargs=label_kwargs,
            title_kwargs=title_kwargs,
            legend_kwargs=legend_kwargs,
        )
        kwargs["subplot"].update({"projection": "3d"})

        x = self.get_variable(variable=cpd1)
        y = self.get_variable(variable=cpd2)
        z = self.get_variable(variable=cpd3)

        if x is None or y is None or z is None:
            return None, None

        xlabel = cpd1 if xlabel is None else xlabel
        ylabel = cpd2 if ylabel is None else ylabel
        zlabel = cpd3 if zlabel is None else zlabel

        if ax is None:
            fig, ax = plt.subplots(1, 1, subplot_kw=kwargs["subplot"], **kwargs["figure"])
        else:
            fig = ax.get_figure()

        ax.plot(x, y, z, **kwargs["plot"])
        _style_subplot(
            ax=ax,
            xlabel=xlabel,
            ylabel=ylabel,
            zlabel=zlabel,
            title=title,
            grid=grid,
            kwargs=kwargs,
        )
        if tight_layout:
            fig.tight_layout()
        return fig, ax

    def plot_trajectories(
        self,
        cpd1: str,
        cpd2: str,
        cpd1_bounds: tuple[float, float],
        cpd2_bounds: tuple[float, float],
        n: int,
        y0: dict[str, float],
        t0: float = 0,
        xlabel: str | None = None,
        ylabel: str | None = None,
        title: str | None = None,
        grid: bool = True,
        tight_layout: bool = True,
        ax: Axis | None = None,
        figure_kwargs: dict[str, Any] | None = None,
        subplot_kwargs: dict[str, Any] | None = None,
        plot_kwargs: dict[str, Any] | None = None,
        grid_kwargs: dict[str, Any] | None = None,
        legend_kwargs: dict[str, Any] | None = None,
        tick_kwargs: dict[str, Any] | None = None,
        label_kwargs: dict[str, Any] | None = None,
        title_kwargs: dict[str, Any] | None = None,
    ) -> tuple[Figure | None, Axis | None]:
        xlabel = cpd1 if xlabel is None else xlabel
        ylabel = cpd2 if ylabel is None else ylabel

        kwargs = _get_plot_kwargs(
            figure_kwargs=figure_kwargs,
            subplot_kwargs=subplot_kwargs,
            plot_kwargs=plot_kwargs,
            grid_kwargs=grid_kwargs,
            tick_kwargs=tick_kwargs,
            label_kwargs=label_kwargs,
            title_kwargs=title_kwargs,
            legend_kwargs=legend_kwargs,
        )

        x = np.linspace(*cpd1_bounds, n)
        y = np.linspace(*cpd2_bounds, n)
        u = np.zeros((n, n))
        v = np.zeros((n, n))

        fcd = self.model.get_full_concentration_dict(y=y0, t=t0)
        for i, s1 in enumerate(x):
            for j, s2 in enumerate(y):
                # Update y0 to new values
                fcd.update({cpd1: s1, cpd2: s2})
                rhs = self.model.get_right_hand_side(y=fcd, t=t0)
                u[i, j] = rhs[f"d{cpd1}dt"]
                v[i, j] = rhs[f"d{cpd2}dt"]

        if ax is None:
            fig, ax = plt.subplots(1, 1, subplot_kw=kwargs["subplot"], **kwargs["figure"])
        else:
            fig = ax.get_figure()
        ax.quiver(x, y, u.T, v.T)
        _style_subplot(
            ax=ax,
            xlabel=xlabel,
            ylabel=ylabel,
            title=title,
            grid=grid,
            kwargs=kwargs,
        )
        if tight_layout:
            fig.tight_layout()
        return fig, ax

    def plot_3d_trajectories(
        self,
        cpd1: str,
        cpd2: str,
        cpd3: str,
        cpd1_bounds: tuple[float, float],
        cpd2_bounds: tuple[float, float],
        cpd3_bounds: tuple[float, float],
        n: int,
        y0: dict[str, float],
        t0: float = 0,
        xlabel: str | None = None,
        ylabel: str | None = None,
        zlabel: str | None = None,
        title: str | None = None,
        grid: bool = True,
        tight_layout: bool = True,
        ax: Axis | None = None,
        figure_kwargs: dict[str, Any] | None = None,
        subplot_kwargs: dict[str, Any] | None = None,
        plot_kwargs: dict[str, Any] | None = None,
        grid_kwargs: dict[str, Any] | None = None,
        legend_kwargs: dict[str, Any] | None = None,
        tick_kwargs: dict[str, Any] | None = None,
        label_kwargs: dict[str, Any] | None = None,
        title_kwargs: dict[str, Any] | None = None,
    ) -> tuple[Figure | None, Axis | None]:
        kwargs = _get_plot_kwargs(
            figure_kwargs=figure_kwargs,
            subplot_kwargs=subplot_kwargs,
            plot_kwargs=plot_kwargs,
            grid_kwargs=grid_kwargs,
            tick_kwargs=tick_kwargs,
            label_kwargs=label_kwargs,
            title_kwargs=title_kwargs,
            legend_kwargs=legend_kwargs,
        )
        kwargs["subplot"].update({"projection": "3d"})

        x = np.linspace(*cpd1_bounds, n)
        y = np.linspace(*cpd2_bounds, n)
        z = np.linspace(*cpd3_bounds, n)
        u = np.zeros((n, n, n))
        v = np.zeros((n, n, n))
        w = np.zeros((n, n, n))

        fcd = self.model.get_full_concentration_dict(y=y0, t=t0)
        for i, s1 in enumerate(x):
            for j, s2 in enumerate(y):
                for k, s3 in enumerate(y):
                    fcd.update({cpd1: s1, cpd2: s2, cpd3: s3})
                    rhs = self.model.get_right_hand_side(y=fcd, t=t0)
                    u[i, j, k] = rhs[f"d{cpd1}dt"]
                    v[i, j, k] = rhs[f"d{cpd2}dt"]
                    w[i, j, k] = rhs[f"d{cpd3}dt"]

        if ax is None:
            fig, ax = plt.subplots(1, 1, subplot_kw=kwargs["subplot"], **kwargs["figure"])
        else:
            fig = ax.get_figure()
        X, Y, Z = np.meshgrid(x, y, z)
        ax.quiver(
            X,
            Y,
            Z,
            np.transpose(u, [1, 0, 2]),
            np.transpose(v, [1, 0, 2]),
            np.transpose(w, [1, 0, 2]),
            length=0.05,
            normalize=True,
            alpha=0.5,
        )
        xlabel = cpd1 if xlabel is None else xlabel
        ylabel = cpd2 if ylabel is None else ylabel
        zlabel = cpd3 if zlabel is None else zlabel
        _style_subplot(
            ax=ax,
            xlabel=xlabel,
            ylabel=ylabel,
            zlabel=zlabel,
            title=title,
            grid=grid,
            kwargs=kwargs,
        )
        if tight_layout:
            fig.tight_layout()
        return fig, ax

    # def plot_production_and_consumption(
    #     self, cpd: str
    # ) -> tuple[Optional[Figure], Optional[tuple[Axis, Axis]]]:
    #     if (fluxes := self.get_fluxes_df()) is None:
    #         return None, None

    #     fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), sharey=True)
    #     for k, v in self.model.stoichiometries_by_compounds[cpd].items():
    #         if v < 0:
    #             ax = ax2
    #         else:
    #             ax = ax1
    #         (fluxes[k] * abs(v)).plot(ax=ax, label=k)

    #     fig.suptitle(cpd)
    #     ax1.set_title("Production")
    #     ax2.set_title("Consumption")
    #     ax1.legend(loc="upper left")
    #     ax2.legend(loc="upper left")

    #     return fig, (ax1, ax2)
