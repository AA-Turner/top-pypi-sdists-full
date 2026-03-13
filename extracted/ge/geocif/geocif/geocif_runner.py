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
    """

    Args:
        logger:
        parser:
        project_name:
        country:
        crop:
        season:
        model:
        index:

    Returns:

    """
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


def loop_execute(inputs):
    """

    Args:
        inputs:

    Returns:

    """
    enable_pycallgraph = False
    project_name, country, crop, season, model, logger, parser, index = inputs

    logger.info("=====================================================")
    logger.info(f"\tStarting GEOCIF: {country} {crop} {season} {model}")
    logger.info("=====================================================")

    if enable_pycallgraph:
        import warnings
        warnings.simplefilter(action="ignore", category=FutureWarning)

        from pycallgraph2 import Config, PyCallGraph, GlobbingFilter
        from pycallgraph2.output import GraphvizOutput

        graphviz = GraphvizOutput()
        graphviz.output_file = "geocif_visualization.png"
        plt.rcParams["figure.dpi"] = 600
        config = Config(max_depth=5)
        config.trace_filter = GlobbingFilter(
            exclude=[
                "pycallgraph.*",
            ]
        )

        with PyCallGraph(output=graphviz, config=config):
            _loop_execute(
                logger, parser, project_name, country, crop, season, model, index
            )
    else:
        _loop_execute(logger, parser, project_name, country, crop, season, model, index)


def gather_inputs(parser):
    """

    Args:
        parser:

    Returns:

    """
    project_name = parser.get("DEFAULT", "project_name")
    countries = ast.literal_eval(parser.get("DEFAULT", "countries"))

    """ Create a list of parameters over which to run the model"""
    all_inputs = []
    for country in countries:
        for crop in ast.literal_eval(parser.get(country, "crops")):
            for season in ast.literal_eval(parser.get(country, "forecast_seasons")):
                for model in ast.literal_eval(parser.get(country, "models")):
                    all_inputs.append([project_name, country, crop, season, model])

    return all_inputs


def execute_models(inputs, logger, parser):
    """
    Executes the model either in parallel or serially based on configuration.

    Args:
        inputs (list): The input data for model execution.
        logger (logging.Logger): Logger for tracking execution details
        parser (configparser.ConfigParser): Configuration file parser

    Returns:

    """
    if parser.has_option("DEFAULT", "do_parallel_ml"):
        do_parallel = parser.getboolean("DEFAULT", "do_parallel_ml")
    else:
        do_parallel = False

    # Add logger and parser to each element in inputs
    inputs = [item + [logger, parser, idx] for idx, item in enumerate(inputs)]

    if do_parallel:
        fraction_cpus = parser.getfloat("DEFAULT", "fraction_cpus")
        cpu_count = int(mp.cpu_count() * fraction_cpus)

        with mp.Pool(cpu_count) as pool:
            pool.map(loop_execute, inputs)
    else:
        pbar = tqdm(inputs, desc="Executing ML models")
        for inputs in pbar:
            country, crop, season = inputs[1], inputs[2], inputs[3]
            pbar.set_description(f"{country} {crop} {season}")
            loop_execute(inputs)

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
    for _, country, crop, season, model in inputs:
        info = country_details.setdefault(country, {"crops": set(), "seasons": set(), "models": set()})
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
    first_model = inputs[0][4] if inputs else None
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
    """

    Args:
        logger:
        parser:

    Returns:

    """
    from geocif.data import ensure_metadata
    ensure_metadata(parser)

    inputs = gather_inputs(parser)

    params = _build_summary_params(parser, inputs)
    ut.display_run_summary("GeoCIF ML Runner", params, wait=20)

    execute_models(inputs, logger, parser)


def run(path_config_files=[Path("../config/geocif.txt")]):
    logger, parser = log.setup_logger_parser(path_config_files)
    main(logger, parser)


if __name__ == "__main__":
    run()
