#!/usr/bin/env python3
"""
Generates posterior plots from RapidPE/RIFT results
"""

__author__ = "Vinaya Valsan"

import os
import logging
import json
import numpy as np

import requests.exceptions

import rapidpe_rift_pipe.postscript_utils as postutils

from argparse import ArgumentParser
from ligo.gracedb.rest import GraceDb
from rapidpe_rift_pipe.config import Config
from rapidpe_rift_pipe import pastro, utils
from rapid_pe import amrlib
from rapid_pe.amrlib import VALID_TRANSFORMS_MASS

print("-------------------Plotting intrinsic posteriors----------------------")

logging.basicConfig(level=logging.INFO)


optp = ArgumentParser()
optp.add_argument("input_dir", help="path to event run dir")
optp.add_argument(
    "--distance-coordinates",
    default=None,
    type=str,
    help="coordinates for intrinsic grid",
)
optp.add_argument("--output-dir", default=None, help="directory to save plots")
optp.add_argument(
    "--sigma1-factor",
    default=1.0,
    type=float,
    help="standard deviation for posterior for param1 is this factor "
    "multiplied to grid size",
)
optp.add_argument(
    "--sigma2-factor",
    default=1.0,
    type=float,
    help="standard deviation for posterior for param2 is this factor"
    "multiplied to grid size",
)
optp.add_argument(
    "--sigma3-factor",
    default=1.0,
    type=float,
    help="standard deviation for posterior for param3 is this factor"
    "multiplied to grid size",
)
optp.add_argument(
    "--sigma4-factor",
    default=1.0,
    type=float,
    help="standard deviation for posterior for param4 is this factor"
    "multiplied to grid size",
)
optp.add_argument(
    "--seed",
    default=None,
    type=int,
    help="seed used for sampling in posterior and pastro calculation",
)
opts = optp.parse_args()
random_state = np.random.RandomState(opts.seed)

input_dir = opts.input_dir

results_dir = os.path.join(input_dir, "results")


config = Config.load(os.path.join(input_dir, "Config.ini"))

distance_coordinates_str = opts.distance_coordinates

distance_coordinates = distance_coordinates_str.split("_")
sigma_str = f'sigma1_{str(opts.sigma1_factor).replace(".","p")}'
sigma_str += f'-sigma2_{str(opts.sigma2_factor).replace(".","p")}'
if len(distance_coordinates) >= 3:
    sigma_str += f'-sigma3_{str(opts.sigma3_factor).replace(".","p")}'
elif len(distance_coordinates) == 4:
    sigma_str += f'-sigma4_{str(opts.sigma4_factor).replace(".","p")}'

print(f"Sigma values: {sigma_str}")
if opts.output_dir:
    output_dir = opts.output_dir
else:
    output_dir = input_dir

summary_plots_dir = os.path.join(output_dir, "summary")
os.system(f"mkdir -p {summary_plots_dir}")

f_lower = 40

# Get injection/search point
event_info = postutils.event_info(input_dir)
event_info_dict = event_info.load_event_info()
event_param_dict = event_info.get_event_params()
mass1_event = event_param_dict["mass1"]
mass2_event = event_param_dict["mass2"]
spin1z_event = event_param_dict["spin1z"]
spin2z_event = event_param_dict["spin2z"]

injection_info = event_info.load_injection_info()

sigma_factor = {}
grid_param_list = distance_coordinates

grid_in_4dimensions = spin1z_event is not None
if grid_in_4dimensions:
    if distance_coordinates_str != "mu1_mu2_q_spin2z":
        grid_param_list += ["chi_eff", "chi_a"]
sigma_factor = {}
sigma_factor[grid_param_list[0]] = opts.sigma1_factor
sigma_factor[grid_param_list[1]] = opts.sigma2_factor
if grid_in_4dimensions:
    sigma_factor[grid_param_list[2]] = opts.sigma3_factor
    sigma_factor[grid_param_list[3]] = opts.sigma4_factor

# Read results xml files
grid_data_dict = postutils.get_grid_info(input_dir)
if distance_coordinates_str == "mu1_mu2_q_spin2z":
    (
        event_param_dict[grid_param_list[0]],
        event_param_dict[grid_param_list[1]],
        event_param_dict[grid_param_list[2]],
        event_param_dict[grid_param_list[3]],
    ) = amrlib.transform_m1m2s1zs2z_mu1mu2qs2z(
        mass1_event, mass2_event, spin1z_event, spin2z_event
    )
    (
        grid_data_dict[grid_param_list[0]],
        grid_data_dict[grid_param_list[1]],
        grid_data_dict[grid_param_list[2]],
        grid_data_dict[grid_param_list[3]],
    ) = amrlib.transform_m1m2s1zs2z_mu1mu2qs2z(
        grid_data_dict["mass1"],
        grid_data_dict["mass2"],
        grid_data_dict["spin1z"],
        grid_data_dict["spin2z"],
    )
    if injection_info is not None:
        (
            injection_info[grid_param_list[0]],
            injection_info[grid_param_list[1]],
            injection_info[grid_param_list[2]],
            injection_info[grid_param_list[3]],
        ) = amrlib.transform_m1m2s1zs2z_mu1mu2qs2z(
            injection_info["mass1"],
            injection_info["mass2"],
            injection_info["spin1z"],
            injection_info["spin2z"],
        )
else:
    (
        event_param_dict[grid_param_list[0]],
        event_param_dict[grid_param_list[1]],
    ) = VALID_TRANSFORMS_MASS[frozenset(distance_coordinates_str.split("_"))](
        mass1_event, mass2_event
    )
    (
        grid_data_dict[grid_param_list[0]],
        grid_data_dict[grid_param_list[1]],
    ) = VALID_TRANSFORMS_MASS[frozenset(distance_coordinates_str.split("_"))](
        grid_data_dict["mass1"],
        grid_data_dict["mass2"],
    )
    if injection_info is not None:
        (
            injection_info[grid_param_list[0]],
            injection_info[grid_param_list[1]],
        ) = VALID_TRANSFORMS_MASS[
            frozenset(distance_coordinates_str.split("_"))
        ](
            injection_info["mass1"], injection_info["mass2"]
        )
logging.info(f"grid_data: {grid_data_dict}")

utils.save_dict_in_hdf(
    grid_data_dict, os.path.join(summary_plots_dir, "grid_info.h5")
)

use_grid_level = None
sigma_dict = postutils.find_sigma(
    grid_data_dict, grid_param_list, sigma_factor, grid_level=use_grid_level
)
finite_indices = np.isfinite(grid_data_dict["margll"])


class ConditionFailedError(Exception):
    pass


length_of_inf_points = len(grid_data_dict["margll"]) - finite_indices.sum()
if length_of_inf_points != 0:
    raise ConditionFailedError(
        f"margl=inf for {length_of_inf_points} grid points"
    )

for key in grid_data_dict.keys():
    grid_data_dict[key] = grid_data_dict[key][finite_indices]

for key in sigma_dict.keys():
    sigma_dict[key] = sigma_dict[key][finite_indices]

grid_levels = np.unique(grid_data_dict["iteration_level"])

if config.pastro.mode == "enabled":
    starting_gracedb_id = event_info_dict["gracedb_id"]
    client = GraceDb(config.gracedb_url)
    starting_gevent = client.event(starting_gracedb_id).json()
    superevent_id = starting_gevent["superevent"]
    superevent = client.superevent(superevent_id).json()
    preferred_pipeline = superevent["preferred_event_data"]["pipeline"]
    logging.info(f'Using p_terr from {superevent["preferred_event"]}')
    preferred_pipeline = preferred_pipeline.lower()

    channel_names = event_info_dict["channel_name"]

    if "INJ" in channel_names:
        rate_dict = config.pastro.category_rates_inj
    else:
        rate_dict = config.pastro.category_rates
    prior_boundary_dict = config.pastro.prior_boundary
    evidence = postutils.compute_evidence(
        grid_data_dict,
        prior_boundary_dict,
        sigma_dict,
        prior_function="salpeter",
        distance_coordinates_str=distance_coordinates_str,
        random_state=random_state,
    )
    try:
        pastro_file = client.files(
            superevent_id, f"{preferred_pipeline}.p_astro.json"
        )
        p_terr = json.load(pastro_file)["Terrestrial"]
        source_prob_dict = pastro.compute_source_prob(
            rate_dict=rate_dict, evidence_dict=evidence
        )
        # NOTE: We are truncating the 128-bit float to 64-bit at the last
        # possible moment to be conservative, but we should revisit this
        # and truncate earlier.
        for key in source_prob_dict:
            source_prob_dict[key] = source_prob_dict[key].astype(np.float64)

        pastro_dict = pastro.pastro(src_prob=source_prob_dict, p_terr=p_terr)
        pastro.plot_pastro(pastro_dict, summary_plots_dir)
        utils.save_as_json(
            pastro_dict, os.path.join(summary_plots_dir, "p_astro.json")
        )
        utils.save_as_json(
            source_prob_dict, os.path.join(summary_plots_dir, "src_prob.json")
        )

    except requests.exceptions.HTTPError:
        logging.exception(
            f"No {preferred_pipeline}.p_astro.json found for {superevent_id}"
        )
    except Exception:
        logging.exception("Pastro calculation failed.")

    # NOTE: We are truncating the 128-bit float to 64-bit at the last
    # possible moment to be conservative, but we should revisit this
    # and truncate earlier.
    for key in evidence:
        evidence[key] = evidence[key].astype(np.float64)
    utils.save_as_json(
        evidence, os.path.join(summary_plots_dir, "evidence.json")
    )

try:
    sample_dict = postutils.get_posterior_samples(
        grid_data_dict,
        sigma_dict,
        grid_level=use_grid_level,
        spin_included=grid_in_4dimensions,
        distance_coordinates_str=distance_coordinates_str,
        random_state=random_state,
    )

    posterior_plot_axis = distance_coordinates + ["mass1", "mass2"]
    if grid_in_4dimensions:
        posterior_plot_axis += ["spin1z", "spin2z", "chi_eff", "chi_a"]

    for param in posterior_plot_axis:
        postutils.plot_posterior(
            sample_dict,
            param,
            plot_dir=summary_plots_dir,
            event_info=event_param_dict,
            injection_info=injection_info,
        )

    postutils.save_m1m2_posterior_samples(
        sample_dict,
        summary_plots_dir,
        random_state=random_state,
    )
    postutils.save_m1m2_weighted_samples(
        sample_dict,
        summary_plots_dir,
    )

except ValueError:
    logging.exception("Failed to generate posterior samples")


for i, gl in enumerate(grid_levels):
    postutils.plot_grid(
        grid_data_dict,
        "mass1",
        "mass2",
        summary_plots_dir,
        grid_level=i,
        event_info=event_param_dict,
        injection_info=injection_info,
    )
    postutils.plot_grid(
        grid_data_dict,
        distance_coordinates[0],
        distance_coordinates[1],
        summary_plots_dir,
        grid_level=i,
        event_info=event_param_dict,
        injection_info=injection_info,
    )

    if grid_in_4dimensions:
        postutils.plot_grid(
            grid_data_dict,
            "spin1z",
            "spin2z",
            summary_plots_dir,
            grid_level=i,
            event_info=event_param_dict,
            injection_info=injection_info,
        )

    if distance_coordinates_str == "mu1_mu2_q_s2q":
        postutils.plot_grid(
            grid_data_dict,
            "mu1",
            "mu2",
            summary_plots_dir,
            grid_level=i,
            event_info=event_param_dict,
            injection_info=injection_info,
        )
        postutils.plot_grid(
            grid_data_dict,
            "q",
            "spin1z",
            summary_plots_dir,
            grid_level=i,
            event_info=event_param_dict,
            injection_info=injection_info,
        )
        postutils.plot_grid(
            grid_data_dict,
            "q",
            "spin2z",
            summary_plots_dir,
            grid_level=i,
            event_info=event_param_dict,
            injection_info=injection_info,
        )


postutils.plot_grid(
    grid_data_dict,
    "mass1",
    "mass2",
    summary_plots_dir,
    event_info=event_param_dict,
    injection_info=injection_info,
)
postutils.plot_grid(
    grid_data_dict,
    distance_coordinates[0],
    distance_coordinates[1],
    summary_plots_dir,
    event_info=event_param_dict,
    injection_info=injection_info,
)

if grid_in_4dimensions:
    postutils.plot_grid(
        grid_data_dict,
        "spin1z",
        "spin2z",
        summary_plots_dir,
        event_info=event_param_dict,
        injection_info=injection_info,
    )

if distance_coordinates_str == "mu1_mu2_q_s2q":
    postutils.plot_grid(
        grid_data_dict,
        "mu1",
        "mu2",
        summary_plots_dir,
        event_info=event_param_dict,
        injection_info=injection_info,
    )
    postutils.plot_grid(
        grid_data_dict,
        "q",
        "spin1z",
        summary_plots_dir,
        event_info=event_param_dict,
        injection_info=injection_info,
    )
    postutils.plot_grid(
        grid_data_dict,
        "q",
        "spin2z",
        summary_plots_dir,
        event_info=event_param_dict,
        injection_info=injection_info,
    )

print(f"All plots saved in {output_dir}")
