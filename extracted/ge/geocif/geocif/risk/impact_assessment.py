# https://iopscience.iop.org/article/10.1088/1748-9326/ab154b#erlab154bs4
import os
import ast
import multiprocessing as mp
from pathlib import Path

from tqdm import tqdm
import matplotlib.pyplot as plt

from geocif import logger as log
from geocif import geocif

plt.style.use("default")

import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)


def loop_execute(inputs):
    """

    Args:
        inputs:

    Returns:

    """
    project_name, country, crop, season, model, logger, parser, index = inputs

    logger.info("=====================================================")
    logger.info(f"\tStarting GEOCIF: {country} {crop} {season} {model}")
    logger.info("=====================================================")

    obj = geocif.Geocif(logger=logger,
                        parser=parser,
                        project_name=project_name)
    obj.read_data(country, crop, season)

    # Setup metadata and run ML code
    obj.setup(season, model)
    if obj.simulation_stages:
        obj.execute()


def gather_inputs(parser):
    """

    Args:
        parser:

    Returns:

    """
    countries = ast.literal_eval(parser.get("RISK", "countries"))

    """ Create a list of parameters over which to run the model"""
    all_inputs = []
    for country in countries:
        for crop in ast.literal_eval(parser.get(country, "crops")):
            for season in ast.literal_eval(parser.get(country, "forecast_seasons")):
                all_inputs.append([country, crop, season])

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
        cpu_count = int(mp.cpu_count() * 0.3)
        with mp.Pool(cpu_count) as pool:
            pool.map(loop_execute, inputs)
    else:
        for inputs in tqdm(inputs, desc="Executing ML models"):
            loop_execute(inputs)

    logger.info("======================================")
    logger.info("\tCompleted all model executions")
    logger.info("======================================")


def main(logger, parser):
    """

    Args:
        logger:
        parser:

    Returns:

    """
    inputs = gather_inputs(parser)
    execute_models(inputs, logger, parser)


def run(path_config_files=[Path("../config/geocif.txt")]):
    logger, parser = log.setup_logger_parser(path_config_files,
                                             name_project="risk",
                                             name_file="impact_assessment")
    main(logger, parser)


if __name__ == "__main__":
    run()
