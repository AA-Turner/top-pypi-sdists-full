import os
import ast
import multiprocessing as mp
from pathlib import Path

from tqdm import tqdm
import matplotlib.pyplot as plt

from geocif import logger as log
from geocif import utils as ut
from .ml import output
from geocif import geocif

plt.style.use("default")

# Show usage info on import
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

_console = Console()
_table = Table(show_header=False, box=None, padding=(0, 1))
_table.add_column(style="bold cyan", no_wrap=True)
_table.add_column()
_table.add_row("Usage", "from geocif import geocif_runner; geocif_runner.run(cfg)")
_table.add_row("cfg", "\\[geobase.txt, countries.txt, crops.txt, geocif.txt]")
_console.print(Panel(_table, title="[bold bright_white]GeoCIF ML Runner[/]", border_style="bright_blue", padding=(1, 2)))


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

    _loop_execute(logger, parser, project_name, country, crop, season, model, index)


def loop_execute_pooled(inputs):
    """Unpack inputs and run pooled multi-country ML pipeline."""
    project_name, countries, crop, season, model, logger, parser, index = inputs

    logger.info("=====================================================")
    logger.info(f"\tStarting GEOCIF (pooled): {countries} {crop} {season} {model}")
    logger.info("=====================================================")

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


def execute_models(inputs, logger, parser, loop_fn=None):
    """
    Executes the model either in parallel or serially based on configuration.

    Args:
        inputs (list): The input data for model execution.
        logger (logging.Logger): Logger for tracking execution details
        parser (configparser.ConfigParser): Configuration file parser
        loop_fn (callable): Function to call per input. Defaults to loop_execute.
    """
    if loop_fn is None:
        loop_fn = loop_execute

    do_parallel = parser.getboolean("DEFAULT", "do_parallel_ml", fallback=False)

    # Add logger and parser to each element in inputs
    inputs = [item + [logger, parser, idx] for idx, item in enumerate(inputs)]

    if do_parallel:
        fraction_cpus = parser.getfloat("DEFAULT", "fraction_cpus")
        cpu_count = int(mp.cpu_count() * fraction_cpus)

        with mp.Pool(cpu_count) as pool:
            pool.map(loop_fn, inputs)
    else:
        pbar = tqdm(inputs, desc="Executing ML models")
        for item in pbar:
            crop, season = item[2], item[3]
            label = item[1] if isinstance(item[1], str) else "pooled"
            pbar.set_description(f"{label} {crop} {season}")
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

    params = [("Countries", countries)]
    for country, info in country_details.items():
        params.append((f"  {country} crops", sorted(info["crops"])))
        params.append((f"  {country} seasons", sorted(info["seasons"])))
        params.append((f"  {country} models", sorted(info["models"])))

    # Global settings
    for key in ["db", "method"]:
        if parser.has_option("DEFAULT", key):
            params.append((key, parser.get("DEFAULT", key)))

    # ML settings (safe reads with fallbacks)
    for key, section in [
        ("feature_selection", "ML"),
        ("cluster_strategy", "ML"),
        ("model_type", "ML"),
        ("check_yield_trend", "ML"),
        ("use_single_time_period_as_feature", "ML"),
        ("lag_yield_as_feature", "ML"),
        ("use_spatial_neighbors", "ML"),
    ]:
        if parser.has_option(section, key):
            params.append((key, parser.get(section, key)))

    # Per-model use_ceis (show from first model)
    first_model = inputs[0][4] if inputs else None  # index 4 = model name
    if first_model and parser.has_option(first_model, "use_ceis"):
        params.append(("use_ceis", parser.get(first_model, "use_ceis")))

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

    if pool_countries:
        inputs = gather_pooled_inputs(parser)
        params = _build_summary_params(parser, inputs)
        ut.display_run_summary("GeoCIF ML Runner (Pooled)", params, wait=20)
        execute_models(inputs, logger, parser, loop_fn=loop_execute_pooled)
    else:
        inputs = gather_inputs(parser)
        params = _build_summary_params(parser, inputs)
        ut.display_run_summary("GeoCIF ML Runner", params, wait=20)
        execute_models(inputs, logger, parser)


def run(path_config_files=[Path("../config/geocif.txt")]):
    logger, parser = log.setup_logger_parser(path_config_files)
    main(logger, parser)


if __name__ == "__main__":
    run()
