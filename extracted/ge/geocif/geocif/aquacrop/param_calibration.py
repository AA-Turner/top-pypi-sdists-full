"""
param_calibration.py — PyGMO PSO calibration of AquaCrop internal crop
parameters against HarvestStat observed yields.

Mirrors the EPIC reference pattern at
``D:/Users/ritvik/projects/crop_models/kenya_maize/geoepic/core/calibration.py``:
- PygmoProblem holds the fitness evaluator + bounds + sample subset.
- Problem_Wrapper drives the outer PSO evolution loop with tqdm + best
  fitness history + optional SALib sensitivity analysis.

Adaptation: AquaCrop is a Python-object model. We don't edit .DAT files;
we mutate ``aquacrop.Crop`` attributes per cell via the existing
``CellTask.crop_param_overrides`` field, then run cells through the
existing ``grid_simulator.run_grid`` using the per-country Pool already
held by ``aquacrop_runner``.

Key design notes:
- Cells are subsampled ONCE per problem (production-weighted, stratified
  by admin). Every PSO candidate is scored on the same cells → no
  sampling noise contaminating the optimization signal.
- ``fitness(x)`` returns a scalar MAE in t/ha, country-aggregated across
  training years. PSO minimizes.
- ``save_fitted_json`` / ``load_fitted_json`` provide cheap caching:
  production runs after a successful calibration skip the entire
  optimization phase.
"""

from __future__ import annotations

import json
import logging
import os
from dataclasses import replace
from datetime import date as _date
from pathlib import Path
from time import perf_counter
from typing import Optional

import numpy as np
import pandas as pd

from .grid_simulator import CellTask
from .param_spec import AquaCropParamSpec

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------
# Subsample helper
# ----------------------------------------------------------------------

def stratified_production_subsample(
    cells_df: pd.DataFrame,
    n_total: int = 150,
    density_multiplier: float = 1.0,
    min_cells_per_admin: int = 1,
    max_cells_per_admin: int = 0,
    min_crop_fraction: float = 0.05,
    strategy: str = "production_weighted",
    seed: int = 42,
) -> pd.DataFrame:
    """Pick a fixed, production-weighted, admin-stratified subset of cells.

    ``cells_df`` must have columns: ``admin_id``, ``crop_fraction``,
    ``cell_area_km2`` (plus any other columns the caller carries — they
    survive intact).

    See the plan at ``replicated-sniffing-candle.md`` for rationale.
    All knobs are surfaced as ``[AQUACROP_CALIBRATION]`` config keys.
    """
    cells_df = cells_df[cells_df["crop_fraction"] >= min_crop_fraction].copy()
    if cells_df.empty:
        return cells_df
    n_total = int(round(n_total * density_multiplier))
    if n_total <= 0:                                   # 0 = use full grid
        return cells_df

    if strategy == "cell_fraction":                    # flat across admins
        return cells_df.sample(
            n=min(n_total, len(cells_df)),
            weights=cells_df["crop_fraction"], random_state=seed,
        ).reset_index(drop=True)

    # Per-admin allocation
    if strategy == "uniform_per_admin":
        n_admins = cells_df["admin_id"].nunique()
        n_per_admin = {
            a: max(1, n_total // n_admins)
            for a in cells_df["admin_id"].unique()
        }
    else:  # production_weighted (default)
        admin_area = (
            cells_df["crop_fraction"] * cells_df["cell_area_km2"]
        ).groupby(cells_df["admin_id"]).sum()
        total_area = admin_area.sum()
        if total_area <= 0:                            # fallback
            return cells_df.sample(
                n=min(n_total, len(cells_df)),
                weights=cells_df["crop_fraction"], random_state=seed,
            ).reset_index(drop=True)
        raw = admin_area / total_area * n_total
        n_per_admin = raw.round().astype(int).to_dict()

    cap = max_cells_per_admin if max_cells_per_admin > 0 else 10**9
    n_per_admin = {
        a: min(cap, max(min_cells_per_admin, n))
        for a, n in n_per_admin.items()
    }

    out = []
    for admin_id, g in cells_df.groupby("admin_id"):
        n_i = min(n_per_admin.get(admin_id, 0), len(g))
        if n_i <= 0:
            continue
        out.append(g.sample(
            n=n_i, weights=g["crop_fraction"].clip(lower=0),
            random_state=seed,
        ))
    if not out:
        return cells_df.head(0)
    return pd.concat(out, ignore_index=True)


# ----------------------------------------------------------------------
# PyGMO problem
# ----------------------------------------------------------------------

class AquaCropPygmoProblem:
    """Fitness evaluator for PyGMO over AquaCrop crop parameters.

    Args:
        specs: list of AquaCropParamSpec (one per crop being co-calibrated).
            For Tier 1 this is a single-element list (one crop per
            calibration run).
        base_tasks_by_year: dict[year -> list[CellTask]]. The CellTasks
            are pre-built for the calibration cell subsample × the
            training years; their ``crop_param_overrides`` field will be
            overwritten per fitness eval.
        observed: pd.DataFrame indexed by (admin_id, year) with column
            'observed_yield' (tn/ha). The MAE is computed against this.
        run_grid_fn: callable(tasks, pool=...) → iterable of CellResult.
            Injected so we can use the existing ``grid_simulator.run_grid``
            with the per-country Pool the caller already holds.
        pool: optional multiprocessing.Pool. Forwarded to run_grid_fn.
        cell_to_admin: dict[(row, col) -> admin_id]. Used to aggregate
            per-cell yields into per-(admin, year) means.

    The PyGMO contract requires:
      - fitness(x) returns a list/tuple of objectives (we return [scalar])
      - get_bounds() returns (lower_bounds_array, upper_bounds_array)
      - get_name() / get_extra_info() optional but useful in logs
    """

    def __init__(
        self,
        specs: list[AquaCropParamSpec],
        base_tasks_by_year: dict[int, list[CellTask]],
        observed: pd.DataFrame,
        run_grid_fn,
        pool=None,
        cell_to_admin: Optional[dict] = None,
    ):
        if not specs:
            raise ValueError("AquaCropPygmoProblem requires at least one spec")
        self.specs = specs
        self.base_tasks_by_year = base_tasks_by_year
        self.observed = observed
        self.run_grid_fn = run_grid_fn
        self.pool = pool
        self.cell_to_admin = cell_to_admin or {}

        # Split point indices so we can slice x back across specs.
        self.lens = np.cumsum([len(s.params) for s in specs])

        # Cache bounds as plain numpy arrays (PyGMO wants this shape).
        cons = []
        for s in specs:
            cons.extend(s.constraints())
        self._bounds = np.asarray(cons, dtype=float)

        # Stash the best fitness so far for nicer log lines.
        self._eval_count = 0

    # PyGMO protocol -----------------------------------------------------

    def fitness(self, x):
        x = np.asarray(x, dtype=float)
        split = np.split(x, self.lens[:-1])
        for spec, vals in zip(self.specs, split):
            spec.edit(vals)

        # For each training year, replace crop_param_overrides on every
        # task with the current spec's overrides. Assumes single-crop
        # calibration for Tier 1; multi-crop would need a per-task lookup
        # by crop_aquacrop_name.
        overrides_by_crop = {s.crop_name: s.overrides_dict() for s in self.specs}

        sims: list[tuple[int, int, int, float]] = []  # (year, row, col, yield)
        for year, base_tasks in self.base_tasks_by_year.items():
            tasks = [
                replace(
                    t,
                    crop_param_overrides=overrides_by_crop.get(t.crop_aquacrop_name),
                )
                for t in base_tasks
            ]
            for res in self.run_grid_fn(tasks, pool=self.pool):
                if res.success and np.isfinite(res.yield_tha):
                    sims.append((year, res.row, res.col, res.yield_tha))

        if not sims:
            self._eval_count += 1
            return [999.0]

        sim_df = pd.DataFrame(sims, columns=["year", "row", "col", "yield"])
        sim_df["admin_id"] = sim_df.apply(
            lambda r: self.cell_to_admin.get((int(r.row), int(r.col))), axis=1,
        )
        sim_df = sim_df.dropna(subset=["admin_id"])
        if sim_df.empty:
            self._eval_count += 1
            return [999.0]

        # Per-(admin, year) simulated mean → MAE against observed.
        sim_agg = sim_df.groupby(["admin_id", "year"])["yield"].mean()
        sim_agg.name = "simulated"
        joined = self.observed.join(sim_agg, how="inner")
        if joined.empty:
            self._eval_count += 1
            return [999.0]
        mae = float((joined["simulated"] - joined["observed_yield"]).abs().mean())
        self._eval_count += 1
        if self._eval_count % 8 == 0:
            logger.debug(
                f"PSO eval #{self._eval_count} → MAE={mae:.4f} t/ha "
                f"(n={len(joined)} admin-years)"
            )
        return [mae]

    def get_bounds(self):
        return self._bounds[:, 0], self._bounds[:, 1]

    def get_name(self):
        return "AquaCropPygmoProblem"

    def get_extra_info(self):
        names = []
        for s in self.specs:
            names.extend(s.var_names())
        return f"vars={names}"

    # Convenience --------------------------------------------------------

    @property
    def var_names(self) -> list[str]:
        names = []
        for s in self.specs:
            names.extend(s.var_names())
        return names


# ----------------------------------------------------------------------
# Calibrator (PSO driver)
# ----------------------------------------------------------------------

class AquaCropCalibrator:
    """Wraps an AquaCropPygmoProblem with a PyGMO algorithm + outer loop.

    Mirrors EPIC's Problem_Wrapper.optimize. Keeps fitness_history for
    convergence plots.
    """

    def __init__(self, problem: AquaCropPygmoProblem):
        try:
            import pygmo as pg  # noqa: F401
        except ImportError as exc:  # pragma: no cover
            raise ImportError(
                "pygmo is required for AquaCrop parameter calibration. "
                "Install with `pip install pygmo` (or `uv add pygmo`). "
                "On Windows, pygmo is best installed from conda-forge."
            ) from exc

        self._pg = pg
        self.problem = problem
        self.pg_problem = pg.problem(problem)
        self.pg_algorithm = None
        self.population = None
        self.fitness_history: list[float] = []

    def init(self, algorithm_cls=None, **algo_kwargs):
        """Set up the PyGMO algorithm. Defaults to ``pg.pso_gen``."""
        pg = self._pg
        if algorithm_cls is None:
            algorithm_cls = pg.pso_gen
        # gen=1 inside the wrapped algo; the outer loop calls evolve() per gen.
        self.pg_algorithm = pg.algorithm(algorithm_cls(gen=1, **algo_kwargs))

    def optimize(self, population_size: int, generations: int):
        """Run population_size × generations fitness evaluations."""
        if self.pg_algorithm is None:
            raise RuntimeError("Call .init() before .optimize()")

        try:
            from geocif.progress import pbar as _pbar
        except ImportError:
            from tqdm import tqdm as _pbar

        logger.info(
            f"PSO start: {self.pg_algorithm.get_name()} × {generations} gens "
            f"(pop={population_size}, vars={len(self.problem.var_names)})"
        )

        t0 = perf_counter()
        self.population = self._pg.population(self.pg_problem, size=population_size)
        logger.info(
            f"Initial population built in {perf_counter() - t0:.1f}s "
            f"(best={float(self.population.champion_f[0]):.4f})"
        )

        bar = _pbar(total=generations, desc="PSO", leave=False)
        for g in range(generations):
            self.population = self.pg_algorithm.evolve(self.population)
            f = float(self.population.champion_f[0])
            self.fitness_history.append(f)
            bar.set_postfix({"best": f"{f:.4g}"})
            bar.update(1)
        bar.close()

        logger.info(
            f"PSO done: best fitness {float(self.population.champion_f[0]):.4f} t/ha "
            f"after {generations} gens ({(perf_counter() - t0) / 60.0:.1f} min)"
        )
        return self.population

    @property
    def best_x(self) -> np.ndarray:
        if self.population is None:
            raise RuntimeError("optimize() not yet called")
        return np.asarray(self.population.champion_x, dtype=float)

    @property
    def best_fitness(self) -> float:
        if self.population is None:
            raise RuntimeError("optimize() not yet called")
        return float(self.population.champion_f[0])

    def apply_best(self):
        """Apply the champion solution to all specs (so .overrides_dict() works)."""
        x = self.best_x
        split = np.split(x, self.problem.lens[:-1])
        for spec, vals in zip(self.problem.specs, split):
            spec.edit(vals)

    # Sensitivity --------------------------------------------------------

    def sensitivity_analysis(self, base_samples: int, method: str = "morris"):
        """Run a Sobol / eFAST / Morris sensitivity study using SALib.

        Mirror of EPIC Problem_Wrapper.sensitivity_analysis. Useful before
        committing to a full PSO run: confirms which params actually
        influence the MAE. Drop low-influence ones from self.specs to
        shrink the search space.
        """
        try:
            from SALib import ProblemSpec
        except ImportError as exc:  # pragma: no cover
            raise ImportError(
                "SALib is required for sensitivity analysis. "
                "Install with `pip install SALib`."
            ) from exc

        lo, hi = self.problem.get_bounds()
        bounds = [[float(lo[i]), float(hi[i])] for i in range(len(lo))]
        sp = ProblemSpec({
            "num_vars": len(bounds),
            "names": self.problem.var_names,
            "bounds": bounds,
            "outputs": ["MAE"],
        })

        if method == "sobol":
            sp.sample_sobol(base_samples)
        elif method == "efast":
            sp.sample_fast(base_samples)
        elif method == "morris":
            sp.sample_morris(base_samples)
        else:
            raise ValueError(f"Unsupported sensitivity method: {method!r}")

        try:
            from geocif.progress import pbar as _pbar
        except ImportError:
            from tqdm import tqdm as _pbar

        def _evaluate(samples):
            out = []
            for s in _pbar(samples, desc=f"SALib/{method}", leave=False):
                fit = self.problem.fitness(s)
                out.append(float(fit[0]))
            return np.array(out)

        sp.evaluate(_evaluate)
        if method == "sobol":
            return sp.analyze_sobol(print_to_console=True)
        elif method == "efast":
            return sp.analyze_fast(print_to_console=True)
        else:
            return sp.analyze_morris(print_to_console=True)


# ----------------------------------------------------------------------
# JSON persistence
# ----------------------------------------------------------------------

def fitted_params_path(dir_output: Path, country: str, crop: str) -> Path:
    """Canonical JSON path for one (country, crop) calibration result."""
    country_slug = country.lower().replace(" ", "_")
    crop_slug = crop.lower().replace(" ", "_")
    return (
        Path(dir_output) / "geocif" / "aquacrop" / "calibrated_params"
        / f"{country_slug}_{crop_slug}.json"
    )


def save_fitted_json(
    path: Path,
    specs: list[AquaCropParamSpec],
    best_fitness: float,
    metadata: Optional[dict] = None,
) -> None:
    """Persist the fitted overrides for cheap reuse across production runs."""
    os.makedirs(path.parent, exist_ok=True)
    payload = {
        "best_fitness_mae_t_per_ha": float(best_fitness),
        "metadata": metadata or {},
        "crops": [
            {
                "crop_name": s.crop_name,
                "params": s.params,
                "bounds": {p: list(s.bounds[p]) for p in s.params},
                "fitted_values": s.overrides_dict(),
            }
            for s in specs
        ],
    }
    with open(path, "w") as fh:
        json.dump(payload, fh, indent=2)
    logger.info(f"Saved calibrated params → {path}")


def load_fitted_overrides(path: Path) -> Optional[dict[str, dict[str, float]]]:
    """Load fitted overrides as ``{crop_name: {param: value}}``.

    Returns None if the file doesn't exist; raises on parse errors so a
    corrupted cache surfaces immediately rather than silently triggering
    a multi-hour refit.
    """
    if not path.is_file():
        return None
    with open(path) as fh:
        payload = json.load(fh)
    out: dict[str, dict[str, float]] = {}
    for crop_entry in payload.get("crops", []):
        name = crop_entry["crop_name"]
        out[name] = {
            p: float(v)
            for p, v in (crop_entry.get("fitted_values") or {}).items()
        }
    logger.info(
        f"Loaded fitted overrides from {path} "
        f"(best MAE={payload.get('best_fitness_mae_t_per_ha', float('nan')):.4f})"
    )
    return out
