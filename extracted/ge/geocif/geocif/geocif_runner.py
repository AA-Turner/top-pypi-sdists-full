"""ML Pipeline Runner.

Trains crop yield forecasting models via LOOCV for each
(country, crop, season, model) combination defined in config.

Usage::

    from geocif import geocif_runner
    geocif_runner.run(cfg_geocif)
"""

import os
import ast
import multiprocessing as mp
from pathlib import Path

from tqdm.rich import tqdm
import matplotlib.pyplot as plt

from geocif import logger as log
from geocif import utils as ut
from geocif import progress
from .ml import output, threads as ml_threads
from geocif import geocif

plt.style.use("default")


def _loop_execute(logger, parser, project_name, country, crop, season, model, index):
    """Execute ML pipeline for a single country/crop/season/model combination."""
    obj = geocif.Geocif(logger=logger, parser=parser, project_name=project_name)
    obj.read_data(country, crop, season)

    if not hasattr(obj, 'df_inputs') or obj.df_inputs is None:
        return

    # Store config file in database, only execute this for
    # the first iteration of the loop
    if index == 0:
        output.config_to_db(obj.db_path, obj.parser, obj.today)

    # Setup metadata and run ML code
    obj.setup(season, model)
    if obj.simulation_stages:
        obj.execute()


def _loop_execute_pooled(logger, parser, project_name, countries, crop, season, model, index):
    """Execute ML pipeline with pooled data from multiple countries."""
    obj = geocif.Geocif(logger=logger, parser=parser, project_name=project_name)
    obj.read_data_pooled(countries, crop, season)

    if not hasattr(obj, 'df_inputs') or obj.df_inputs is None:
        return

    if index == 0:
        output.config_to_db(obj.db_path, obj.parser, obj.today)

    obj.setup_pooled(countries, season, model)
    if obj.simulation_stages:
        obj.execute()


def loop_execute(inputs):
    """Unpack inputs and run single-country ML pipeline."""
    project_name, country, crop, season, model, logger, parser, index = inputs

    logger.info("=====================================================")
    logger.info(f"\tStarting GEOCIF: {country} {crop} {season} {model}")
    logger.info("=====================================================")

    if progress.in_worker():
        with progress.StatusTimer(index, f"{country} {crop} {season} {model}"):
            _loop_execute(logger, parser, project_name, country, crop, season, model, index)
    else:
        _loop_execute(logger, parser, project_name, country, crop, season, model, index)


def loop_execute_pooled(inputs):
    """Unpack inputs and run pooled multi-country ML pipeline."""
    project_name, countries, crop, season, model, logger, parser, index = inputs

    logger.info("=====================================================")
    logger.info(f"\tStarting GEOCIF (pooled): {countries} {crop} {season} {model}")
    logger.info("=====================================================")

    if progress.in_worker():
        label = f"pooled[{','.join(countries)}] {crop} {season} {model}"
        with progress.StatusTimer(index, label):
            _loop_execute_pooled(logger, parser, project_name, countries, crop, season, model, index)
    else:
        _loop_execute_pooled(logger, parser, project_name, countries, crop, season, model, index)


def gather_inputs(parser):
    """Build list of [project_name, country, crop, season, model] tuples."""
    project_name = parser.get("DEFAULT", "project_name")
    countries = ast.literal_eval(parser.get("DEFAULT", "countries"))

    all_inputs = []
    for country in countries:
        for crop in ast.literal_eval(parser.get(country, "crops")):
            for season in ast.literal_eval(parser.get(country, "forecast_seasons")):
                for model in ast.literal_eval(parser.get(country, "models")):
                    all_inputs.append([project_name, country, crop, season, model])

    return all_inputs


def gather_pooled_inputs(parser):
    """Group inputs by (crop, season, model) for cross-country pooling.

    Returns list of [project_name, [country1, ...], crop, season, model].
    """
    project_name = parser.get("DEFAULT", "project_name")
    countries = ast.literal_eval(parser.get("DEFAULT", "countries"))

    groups = {}
    for country in countries:
        for crop in ast.literal_eval(parser.get(country, "crops")):
            for season in ast.literal_eval(parser.get(country, "forecast_seasons")):
                for model in ast.literal_eval(parser.get(country, "models")):
                    groups.setdefault((crop, season, model), []).append(country)

    return [[project_name, clist, crop, season, model]
            for (crop, season, model), clist in groups.items()]


def _init_ml_worker(parallel_mode, total, threads):
    """
    Pool worker startup: pin the thread budget BEFORE any model is built,
    then hand off to the normal progress-bar initializer.
    """
    ml_threads.apply_worker_limits(threads)
    progress.set_worker_mode(parallel_mode, total)


def order_inputs_model_major(inputs, model_index=4):
    """Reorder fold tasks so the model varies slowest.

    gather_inputs nests model innermost, so a year's tasks for every model
    sit next to each other and the pool dispatches them at the same moment.
    That defeats the feature-selection cache (geocif/ml/fs_cache.py): the
    selection is model-independent, but concurrent same-fold tasks all miss
    and all recompute it.

    Grouping by model instead — every year for model A, then every year for
    model B — means model B's folds start once model A has already cached
    their selections. Sorting is stable and models keep their configured
    order, so only dispatch order changes; imap_unordered already makes
    completion order arbitrary.

    Args:
        inputs: list of [project_name, country(s), crop, season, model] items
        model_index: position of the model name within each item

    Returns:
        The reordered list, or the input unchanged if it has an unexpected
        shape (ordering is an optimisation, never a correctness requirement).
    """
    try:
        model_order = []
        for item in inputs:
            model = item[model_index]
            if not isinstance(model, str):
                return list(inputs)
            if model not in model_order:
                model_order.append(model)

        rank = {model: i for i, model in enumerate(model_order)}
        return sorted(inputs, key=lambda item: rank[item[model_index]])
    except (IndexError, KeyError, TypeError):
        return list(inputs)


def ensure_statistics_files(inputs, logger, parser):
    """Pre-create statistics files for all unique (country, crop) pairs.

    Must run before the parallel pool so that workers only ever read
    existing, fully-written files — avoids the race where one worker
    is mid-write while another tries to read the same file.
    """
    project_name = parser.get("DEFAULT", "project_name")
    seen = set()
    for item in inputs:
        country_field, crop = item[1], item[2]
        # Pooled inputs (gather_pooled_inputs) put a list of countries at
        # item[1]; per-country inputs put a single country string.  Stats
        # files are still per-country, so flatten either case to a list.
        countries_iter = country_field if isinstance(country_field, (list, tuple)) else [country_field]

        for country in countries_iter:
            key = (country, crop)
            if key in seen:
                continue
            seen.add(key)

            obj = geocif.Geocif(logger=logger, parser=parser, project_name=project_name)
            file_path = obj._get_statistics_file_path(country, crop)

            if (
                not file_path.exists()
                or obj.update_input_file
                or obj._statistics_file_stale(country, crop, file_path)
            ):
                logger.info(f"Pre-creating statistics file: {country} {crop}")
                try:
                    obj._create_statistics_file(country, crop, file_path)
                except FileNotFoundError as e:
                    logger.warning(f"Skipping {country} {crop}: {e}")


def ensure_db_tables(inputs, logger, parser):
    """Pre-create SQLite tables for all unique (country, crop) pairs.

    Must run before the parallel pool so that workers only INSERT/UPDATE
    into existing tables — avoids concurrent CREATE TABLE races in pangres.
    """
    import sqlite3

    project_name = parser.get("DEFAULT", "project_name")
    obj = geocif.Geocif(logger=logger, parser=parser, project_name=project_name)
    db_path = obj.db_path
    target = obj.target

    # Schema mirrors _build_results_dataframe + _add_* methods in Geocif.
    # All columns are determined by config, not by model output.
    columns = [
        ('"Index"', "TEXT NOT NULL PRIMARY KEY"),
        ('"Experiment_ID"', "TEXT"),
        ('"Experiment Name"', "TEXT"),
        ('"Date"', "TEXT"),
        ('"Time"', "TEXT"),
        ('"Country"', "TEXT"),
        ('"Crop"', "TEXT"),
        ('"Cluster Strategy"', "TEXT"),
        ('"Frequency"', "TEXT"),
        ('"Selected Features"', "JSON"),
        ('"Best Hyperparameters"', "JSON"),
        ('"Stage_ID"', "TEXT"),
        ('"Stage Range"', "TEXT"),
        ('"Stage Name"', "TEXT"),
        # Calendar-order human-readable label (Tier 2a — added 0.4.788).
        # MUST be in the pre-create schema because the DataFrame written
        # by _build_results_dataframe includes it; without this column the
        # INSERT fails with "table has no column named Stage Window
        # Display" and every row is dropped (empty DB — cf. 0.4.788 regression).
        ('"Stage Window Display"', "TEXT"),
        ('"Starting Stage"', "BIGINT"),
        ('"Ending Stage"', "BIGINT"),
        ('"Model"', "TEXT"),
        ('"Region_ID"', "TEXT"),
        ('"Region"', "TEXT"),
        ('"Season"', "BIGINT"),
        ('"Harvest Year"', "TEXT"),
        ('"Area (ha)"', "FLOAT"),
        (f'"Observed {target}"', "FLOAT"),
        (f'"Predicted {target}"', "FLOAT"),
        ('"APE"', "FLOAT"),
        (f'"Median {target}"', "FLOAT"),
        (f'"Median {target} (2018-2022)"', "FLOAT"),
        (f'"Median {target} (2013-2017)"', "FLOAT"),
        ('"alpha"', "FLOAT"),
        ('"lower CI"', "FLOAT"),
        ('"upper CI"', "FLOAT"),
        ('"Analogous Year"', "FLOAT"),
        ('"Analogous Year Yield"', "FLOAT"),
        ('"Detrended Model Type"', "FLOAT"),
        ('"Detrended Model"', "FLOAT"),
        ('"Last Observed Year"', "BIGINT"),
        (f'"Last Observed {target}"', "FLOAT"),
    ]
    col_defs = ", ".join(f"{name} {typ}" for name, typ in columns)

    seen = set()
    table_names = []
    for item in inputs:
        country, crop = item[1], item[2]
        table_name = f"pooled_{crop}" if isinstance(country, list) else f"{country}_{crop}"
        if table_name not in seen:
            seen.add(table_name)
            table_names.append(table_name)

    con = sqlite3.connect(str(db_path), timeout=120)
    con.execute("PRAGMA journal_mode=WAL")
    con.execute("PRAGMA busy_timeout=120000")
    for table_name in table_names:
        con.execute(f'CREATE TABLE IF NOT EXISTS "{table_name}" ({col_defs})')
        logger.info(f"Ensured DB table: {table_name}")
    con.commit()
    con.close()


def execute_models(inputs, logger, parser, loop_fn=None, desc=None):
    """
    Executes the model either in parallel or serially based on configuration.

    Args:
        inputs (list): The input data for model execution.
        logger (logging.Logger): Logger for tracking execution details
        parser (configparser.ConfigParser): Configuration file parser
        loop_fn (callable): Function to call per input. Defaults to loop_execute.
        desc (str): Progress bar description. Defaults to "Executing ML models".
    """
    if loop_fn is None:
        loop_fn = loop_execute

    desc = desc or "Executing ML models"
    do_parallel = parser.getboolean("DEFAULT", "do_parallel_ml", fallback=False)

    if do_parallel:
        ensure_statistics_files(inputs, logger, parser)
        ensure_db_tables(inputs, logger, parser)

    # Stagger same-fold models so the feature-selection cache can actually
    # be hit instead of every model racing to compute the same selection.
    if do_parallel and parser.getboolean("ML", "cache_feature_selection", fallback=True):
        reordered = order_inputs_model_major(inputs)
        if reordered != inputs:
            logger.info(
                "Dispatching fold tasks model-major so the feature-selection "
                "cache is shared across models"
            )
        inputs = reordered

    # Add logger and parser to each element in inputs
    inputs = [item + [logger, parser, idx] for idx, item in enumerate(inputs)]

    if do_parallel:
        fraction_cpus = parser.getfloat("DEFAULT", "fraction_cpus")
        cpu_count = int(mp.cpu_count() * fraction_cpus)

        # Without this every worker's model grabs all cores: 19 workers x 131
        # threads measured load 940 on a 128-core node and starved the other
        # jobs sharing it. Override with [ML] threads_per_worker.
        threads_per_worker = ml_threads.resolve_threads_per_worker(
            cpu_count, mp.cpu_count(), parser=parser
        )
        if threads_per_worker:
            logger.info(
                f"Limiting each of the {cpu_count} worker(s) to "
                f"{threads_per_worker} thread(s) of {mp.cpu_count()} cores "
                f"({cpu_count * threads_per_worker} total) so models do not "
                f"oversubscribe the node"
            )
        else:
            logger.info(
                f"Thread limiting disabled — each of the {cpu_count} worker(s) "
                f"may use all {mp.cpu_count()} cores"
            )

        with mp.Pool(
            cpu_count,
            initializer=_init_ml_worker,
            initargs=(True, len(inputs), threads_per_worker),
        ) as pool:
            for _ in tqdm(
                pool.imap_unordered(loop_fn, inputs),
                total=len(inputs),
                desc=desc,
            ):
                pass
    else:
        pbar = tqdm(inputs, desc=desc)
        for item in pbar:
            crop, season = item[2], item[3]
            label = item[1] if isinstance(item[1], str) else "pooled"
            pbar.set_description(f"{desc} | {label} {crop} {season}")
            loop_fn(item)

    logger.info("======================================")
    logger.info("\tCompleted all model executions")
    logger.info("======================================")


def _build_summary_params(parser, inputs):
    """Build parameter list for the run summary display."""
    countries = ast.literal_eval(parser.get("DEFAULT", "countries"))
    if parser.has_option("DEFAULT", "do_parallel_ml"):
        do_parallel = parser.getboolean("DEFAULT", "do_parallel_ml")
    else:
        do_parallel = False

    # Collect unique crops, seasons, models per country
    country_details = {}
    for item in inputs:
        _, country_or_list, crop, season, model = item[:5]
        # In pooled mode, country_or_list is a list of countries
        if isinstance(country_or_list, list):
            for c in country_or_list:
                info = country_details.setdefault(c, {"crops": set(), "seasons": set(), "models": set()})
                info["crops"].add(crop)
                info["seasons"].add(str(season))
                info["models"].add(model)
        else:
            info = country_details.setdefault(country_or_list, {"crops": set(), "seasons": set(), "models": set()})
            info["crops"].add(crop)
            info["seasons"].add(str(season))
            info["models"].add(model)

    # Resolve yield file per country
    default_yield = "hvstat_africa_data_v1.0.csv"
    if parser.has_option("DEFAULT", "production_statistics_file"):
        default_yield = parser.get("DEFAULT", "production_statistics_file")

    dir_output = Path(parser.get("PATHS", "dir_output"))
    dir_inputs = Path(parser.get("PATHS", "dir_inputs", fallback=parser.get("PATHS", "dir_input", fallback="")))
    params = [
        ("Input dir", str(dir_inputs)),
        ("Output dir", str(dir_output)),
        ("Countries", countries),
    ]
    for country, info in country_details.items():
        params.append((f"  {country} crops", sorted(info["crops"])))
        params.append((f"  {country} seasons", sorted(info["seasons"])))
        params.append((f"  {country} models", sorted(info["models"])))
        ck = country.lower().replace(" ", "_")
        yf = parser.get(ck, "production_statistics_file") if parser.has_option(ck, "production_statistics_file") else default_yield
        params.append((f"  {country} yield file", yf))

    # Global settings
    for key in ["db", "method"]:
        if parser.has_option("DEFAULT", key):
            params.append((key, parser.get("DEFAULT", key)))

    # ML settings (safe reads with fallbacks)
    for key, section in [
        ("feature_selection", "ML"),
        ("cluster_strategy", "ML"),
        ("model_type", "ML"),
        ("run_time_steps", "ML"),
        ("check_yield_trend", "ML"),
        ("use_single_time_period_as_feature", "ML"),
        ("lag_yield_as_feature", "ML"),
        ("use_spatial_neighbors", "ML"),
    ]:
        if parser.has_option(section, key):
            params.append((key, parser.get(section, key)))

    # Per-model use_cids (show from first model)
    first_model = inputs[0][4] if inputs else None  # index 4 = model name
    if first_model and parser.has_option(first_model, "use_cids"):
        params.append(("use_cids", parser.get(first_model, "use_cids")))

    params.append(("Parallel", str(do_parallel)))
    if do_parallel:
        fraction_cpus = parser.getfloat("DEFAULT", "fraction_cpus")
        cpu_count = int(mp.cpu_count() * fraction_cpus)
        params.append(("CPUs", str(cpu_count)))
    params.append(("Total combinations", str(len(inputs))))

    return params


def main(logger, parser):
    """Run the GeoCIF ML pipeline."""
    from geocif.data import ensure_metadata
    ensure_metadata(parser)

    pool_countries = parser.getboolean("ML", "pool_countries", fallback=False)
    check_yield_trend = parser.getboolean("ML", "check_yield_trend", fallback=True)

    if pool_countries and not check_yield_trend:
        logger.error(
            "pool_countries=True requires check_yield_trend=True. "
            "Pooling without detrending mixes raw yield scales across countries, "
            "producing unreliable models. Enable detrending or disable pooling."
        )
        return

    if pool_countries:
        inputs = gather_pooled_inputs(parser)
        loop_fn = loop_execute_pooled
        summary_title = "GeoCIF ML Runner (Pooled)"
    else:
        inputs = gather_inputs(parser)
        loop_fn = None
        summary_title = "GeoCIF ML Runner"

    params = _build_summary_params(parser, inputs)
    ut.display_run_summary(summary_title, params, wait=20)

    run_time_steps = parser.get("ML", "run_time_steps", fallback="latest")

    # Check use_cids for forecast type presence
    try:
        _use_cids = ast.literal_eval(parser.get("DEFAULT", "use_cids", fallback="['all']"))
    except (ValueError, SyntaxError):
        _use_cids = ["all"]
    _has_forecast = (
        "all" in _use_cids
        or any(c in ("FLDAS", "S2S") for c in _use_cids)
    )
    _forecast_only = (
        "all" not in _use_cids
        and all(c in ("FLDAS", "S2S") for c in _use_cids)
    )

    if run_time_steps == "auto":
        if _forecast_only:
            parser.set("ML", "run_time_steps", "pre_season")
            logger.info("Auto mode (forecast-only): single pass pre-season + in-season")
            execute_models(inputs, logger, parser, loop_fn=loop_fn,
                           desc="Forecast models (pre+in-season)")
        elif _has_forecast:
            parser.set("ML", "run_time_steps", "pre_season")
            logger.info("Auto mode — Pass 1: Pre-season (FLDAS/S2S leads only)")
            execute_models(inputs, logger, parser, loop_fn=loop_fn,
                           desc="Pre-season models")

            parser.set("ML", "run_time_steps", "all")
            logger.info("Auto mode — Pass 2: In-season (all time steps)")
            execute_models(inputs, logger, parser, loop_fn=loop_fn,
                           desc="In-season models")
        else:
            parser.set("ML", "run_time_steps", "all")
            logger.info("Auto mode — No forecast CIDs, in-season only")
            execute_models(inputs, logger, parser, loop_fn=loop_fn,
                           desc="In-season models")

        parser.set("ML", "run_time_steps", "auto")
    else:
        execute_models(inputs, logger, parser, loop_fn=loop_fn)

    # Upload outputs to HuggingFace Hub if configured
    push_to_hf = parser.getboolean("ML", "push_to_hf", fallback=False)
    if push_to_hf:
        from geocif.hf_sync import upload_to_hf
        upload_to_hf(parser)


def run(path_config_files=[Path("../config/geocif.txt")]):
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    console = Console()
    table = Table(show_header=False, box=None, padding=(0, 1))
    table.add_column(style="bold cyan", no_wrap=True)
    table.add_column()
    table.add_row("Usage", "from geocif import geocif_runner; geocif_runner.run(cfg)")
    table.add_row("cfg", "[geobase.txt, countries.txt, crops.txt, geocif.txt]")
    console.print(Panel(table, title="[bold bright_white]GeoCIF ML Runner[/]",
                        border_style="bright_blue", padding=(1, 2)))
    logger, parser = log.setup_logger_parser(path_config_files)
    main(logger, parser)


if __name__ == "__main__":
    run()
