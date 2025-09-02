from __future__ import annotations

__all__ = [
    "_LinearLabelSimulate",
]

import copy
from typing import (
    TYPE_CHECKING,
    Any,
    Iterable,
    cast,
)

from typing_extensions import Self

from modelbase.ode.models import LinearLabelModel as _LinearLabelModel
from modelbase.typing import Array, ArrayLike, Axis
from modelbase.utils.plotting import plot, plot_grid

from . import _BaseSimulator

if TYPE_CHECKING:
    from matplotlib.figure import Figure

    from modelbase.ode.integrators import (
        AbstractIntegrator as _AbstractIntegrator,
    )


class _LinearLabelSimulate(_BaseSimulator[_LinearLabelModel]):

    """Simulator for LinearLabelModels."""

    def __init__(
        self,
        model: _LinearLabelModel,
        integrator: type[_AbstractIntegrator],
        y0: ArrayLike | None = None,
        time: list[Array] | None = None,
        results: list[Array] | None = None,
    ) -> None:
        self.y0: ArrayLike | None  # For some reasons mypy has problems finding this
        super().__init__(
            model=model,
            integrator=integrator,
            y0=y0,
            time=time,
            results=results,
        )

    def _test_run(self) -> None:
        if self.y0 is None:
            msg = "y0 must not be None"
            raise ValueError(msg)
        self.model.get_fluxes_dict(
            y=self.y0,
            v_ss=self.model._v_ss,
            external_label=self.model._external_label,
        )
        self.model.get_right_hand_side(
            y_labels=self.y0,
            y_ss=self.model._y_ss,
            v_ss=self.model._v_ss,
            external_label=self.model._external_label,
            t=0,
        )

    def copy(self) -> _LinearLabelSimulate:
        """Return a deepcopy of this class."""
        new = copy.deepcopy(self)
        if new.results is not None:
            new._initialise_integrator(y0=new.results[-1])
        elif new.y0 is not None:
            new.initialise(
                label_y0=new.y0,
                y_ss=new.model._y_ss,
                v_ss=new.model._v_ss,
                external_label=new.model._external_label,
                test_run=False,
            )
        return new

    def initialise(
        self,
        label_y0: ArrayLike | dict[str, float],
        y_ss: dict[str, float],
        v_ss: dict[str, float],
        external_label: float = 1.0,
        test_run: bool = True,
    ) -> Self:
        self.model._y_ss = y_ss
        self.model._v_ss = v_ss
        self.model._external_label = external_label
        if self.results is not None:
            self.clear_results()
        if isinstance(label_y0, dict):
            self.y0 = [label_y0[compound] for compound in self.model.get_compounds()]
        else:
            self.y0 = list(label_y0)
        self._initialise_integrator(y0=self.y0)

        if test_run:
            self._test_run()
        return self

    def get_label_position(self, compound: str, position: int) -> Array | None:
        """Get relative concentration of a single isotopomer.

        Examples
        --------
        >>> get_label_position(compound="GAP", position=2)

        """
        res = self.get_results_dict(concatenated=True)
        if res is None:
            return None
        return res[self.model.isotopomers[compound][position]]

    def get_label_distribution(self, compound: str) -> Array | None:
        """Get relative concentrations of all compound isotopomers.

        Examples
        --------
        >>> get_label_position(compound="GAP")

        """
        compounds = self.model.isotopomers[compound]
        res = self.get_results_df(concatenated=True)
        if res is None:
            return None
        return cast(Array, res.loc[:, compounds].values)

    def _make_legend_labels(
        self, prefix: str, compound: str, initial_index: int
    ) -> list[str]:
        return [
            f"{prefix}{i}"
            for i in range(
                initial_index, len(self.model.isotopomers[compound]) + initial_index
            )
        ]

    def plot_label_distribution(
        self,
        compound: str,
        relative: bool = True,
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
        legend_prefix: str = "Pos ",
        initial_index: int = 0,
    ) -> tuple[Figure, Axis]:
        """Plot label distribution of a compound."""
        if ylabel is None and relative:
            ylabel = "Relative concentration"
        x = self.get_time()
        y = self.get_label_distribution(compound=compound)
        legend = self._make_legend_labels(legend_prefix, compound, initial_index)
        if title is None:
            title = compound
        return plot(
            plot_args=(x, y),
            legend=legend,
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

    def plot_label_distribution_grid(
        self,
        compounds: list[str],
        relative: bool = True,
        ncols: int | None = None,
        sharex: bool = True,
        sharey: bool = True,
        xlabels: str | list[str] | None = None,
        ylabels: str | list[str] | None = None,
        plot_titles: list[str] | None = None,
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
        legend_prefix: str = "Pos ",
        initial_index: int = 0,
    ) -> tuple[Figure | None, Array | None]:
        """Plot label distributions of multiple compounds on a grid."""
        time = self.get_time()
        plot_groups = [
            (time, self.get_label_distribution(compound=compound))
            for compound in compounds
        ]
        legend_groups = [
            self._make_legend_labels(legend_prefix, compound, initial_index)
            for compound in compounds
        ]
        if ylabels is None and relative:
            ylabels = "Relative concentration"
        if plot_titles is None:
            plot_titles = compounds
        return plot_grid(
            plot_groups=plot_groups,  # type: ignore
            legend_groups=legend_groups,
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

    def plot_all_label_distributions(
        self,
        relative: bool = True,
        ncols: int | None = None,
        sharex: bool = True,
        sharey: bool = True,
        xlabels: str | list[str] | None = None,
        ylabels: str | list[str] | None = None,
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
        legend_prefix: str = "Pos ",
        initial_index: int = 0,
    ) -> tuple[Figure | None, Array | None]:
        """Plot label distributions of all compounds on a grid."""
        time = self.get_time()
        compounds = self.model.isotopomers
        plot_groups = [
            (time, self.get_label_distribution(compound=compound))
            for compound in compounds
        ]
        legend_groups = [
            self._make_legend_labels(legend_prefix, compound, initial_index)
            for compound in compounds
        ]
        if ylabels is None and relative:
            ylabels = "Relative concentration"
        if plot_titles is None:
            plot_titles = compounds

        return plot_grid(
            plot_groups=plot_groups,  # type: ignore
            legend_groups=legend_groups,
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
