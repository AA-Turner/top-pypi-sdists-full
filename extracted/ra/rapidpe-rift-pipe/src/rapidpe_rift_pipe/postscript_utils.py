#!/usr/bin/env python3

__author__ = "Caitlin Rose, Vinaya Valsan"

import os
import json
import re
import glob
import logging
import math

import numpy as np
import matplotlib.pyplot as plt

from ligo.lw import utils, lsctables, ligolw
from scipy.stats import multinomial

from rapid_pe import amrlib
from rapid_pe.amrlib import VALID_TRANSFORMS_MASS
from rapid_pe.amrlib import INVERSE_TRANSFORMS_MASS
from rapid_pe.amrlib import BOUND_CHECK_MASS

from rapidpe_rift_pipe import utils as rpe_utils
import rapidpe_rift_pipe.jacobians as jacobians

logging.basicConfig(level=logging.INFO)


_default_random_state = np.random.RandomState()


class event_info:
    def __init__(self, rundir):
        self.rundir = rundir

    def load_event_info(self):
        """
        read event_info_dict.txt
        """
        with open(self.rundir + "/event_info_dict.txt") as f:
            event_info_dict = json.load(f)
        return event_info_dict

    def load_injection_info(self):
        """
        read injection_info.txt
        """
        try:
            with open(self.rundir + "/injection_info.txt") as f:
                injection_info_dict = json.load(f)
            (
                injection_info_dict["chi_eff"],
                injection_info_dict["chi_a"],
            ) = amrlib.transform_s1zs2z_chi_eff_chi_a(
                injection_info_dict["mass1"],
                injection_info_dict["mass2"],
                injection_info_dict["spin1z"],
                injection_info_dict["spin2z"],
            )
        except FileNotFoundError:
            injection_info_dict = None
        return injection_info_dict

    def get_event_params(self):
        event_info_dict = self.load_event_info()
        intrinsic_param_event = event_info_dict["intrinsic_param"]
        mass1_event = float(
            re.search('mass1=(.+?)"', intrinsic_param_event).group(1)
        )
        mass2_event = float(
            re.search('mass2=(.+?)"', intrinsic_param_event).group(1)
        )
        event_params = {}
        event_params["mass1"] = mass1_event
        event_params["mass2"] = mass2_event
        try:
            spin1z_event = float(
                re.search('spin1z=(.+?)"', intrinsic_param_event).group(1)
            )
            spin2z_event = float(
                re.search('spin2z=(.+?)"', intrinsic_param_event).group(1)
            )
            event_params["spin1z"] = spin1z_event
            event_params["spin2z"] = spin2z_event
            (
                event_params["chi_eff"],
                event_params["chi_a"],
            ) = amrlib.transform_s1zs2z_chi_eff_chi_a(
                mass1_event, mass2_event, spin1z_event, spin2z_event
            )
        except AttributeError:
            event_params["spin1z"] = None
            event_params["spin2z"] = None
            logging.info("No Spin information found in event_info_dict")
            pass
        return event_params


def get_grid_info(rundir):
    results_dir = os.path.join(rundir, "results")
    all_xml = glob.glob(
        os.path.join(results_dir, "ILE_iteration_*-MASS_SET*.xml.gz")
    )
    logging.info(f"Found {len(all_xml)} sample files")
    iterations = [
        xmlfile[
            xmlfile.find("ILE_iteration") : xmlfile.find("ILE_iteration")
            + len("ILE_iteration_0")
        ]
        for xmlfile in all_xml
    ]

    grid_levels = np.sort(np.unique(iterations))
    keys = {
        "mass1",
        "mass2",
        "spin1z",
        "spin2z",
        "chi_eff",
        "chi_a",
        "margll",
        "iteration_level",
        "filename",
    }
    data_dict = {key: [] for key in keys}
    check_spin = True
    for i, gl in enumerate(grid_levels):
        xml_files = glob.glob(
            os.path.join(results_dir, gl + "-MASS_SET*.xml.gz")
        )
        logging.info(f"Found {len(xml_files)} in grid_level {gl}")
        for xml_file in xml_files:
            xmldoc = utils.load_filename(
                xml_file, contenthandler=ligolw.LIGOLWContentHandler
            )
            new_tbl = lsctables.SnglInspiralTable.get_table(xmldoc)
            row = new_tbl[0]
            data_dict["filename"].append(os.path.basename(xml_file))
            data_dict["mass1"].append(row.mass1)
            data_dict["mass2"].append(row.mass2)
            data_dict["margll"].append(row.snr)
            data_dict["iteration_level"].append(i)
            if check_spin:
                try:
                    data_dict["spin1z"].append(row.spin1z)
                    data_dict["spin2z"].append(row.spin2z)
                    (
                        chi_eff,
                        chi_a,
                    ) = amrlib.transform_s1zs2z_chi_eff_chi_a(
                        row.mass1, row.mass2, row.spin1z, row.spin2z
                    )
                    data_dict["chi_eff"].append(chi_eff)
                    data_dict["chi_a"].append(chi_a)
                except AttributeError:
                    check_spin = False
                    logging.info(
                        "No spin information found in SnglInspiralTable"
                    )
    if data_dict["spin1z"] == []:
        del data_dict["spin1z"]
        del data_dict["spin2z"]
    data_dict = {key: np.array(data_dict[key]) for key in data_dict.keys()}
    return data_dict


def find_sigma(grid_data, param_list, sigma_factor, grid_level=None):
    """
    Find standard deviation of the gaussian at each grid point.
    Standand deviation at a given grid point is equal to sigma_factor
    multiplied by the separation between given grid point and its nearest
    neighbour grid point.
    """
    Sigma = {param: [] for param in param_list}
    for param in param_list:
        grid_param = np.array(grid_data[param])
        grid_iteration_level = grid_data["iteration_level"]
        grid_id = np.arange(len(grid_iteration_level))
        if grid_level is not None:
            grid_inds = grid_id[grid_iteration_level == grid_level]
            grid_param = np.array(grid_data[param])[grid_inds]
        for j in range(len(grid_param)):
            distance_array = np.array(
                [
                    abs(grid_param[j] - grid_param[i])
                    for i in range(len(grid_param))
                ]
            )
            distance_array = np.sort(distance_array[distance_array > 1e-5])
            distance = distance_array[0]
            Sigma[param] = np.append(
                Sigma[param], sigma_factor[param] * distance
            )

    return Sigma


def get_posterior_samples(
    grid_data,
    sigma,
    distance_coordinates_str,
    random_state=_default_random_state,
    grid_level=None,
    spin_included=False,
    nsamples_per_grid=2000,
):
    """
    Generate posterior samples for params for the given grid_level
    """
    distance_coordinates = distance_coordinates_str.split("_")
    sample_dict = {}
    Margll_sel = grid_data["margll"]
    grid_it_level = grid_data["iteration_level"]
    grid_index_list = np.arange(len(grid_it_level))
    if grid_level is not None:
        grid_inds = grid_index_list[grid_it_level == grid_level]
        Margll_sel = grid_data["margll"][grid_inds]
        for param in distance_coordinates:
            grid_data[param] = grid_data[param][grid_inds]

    margL_normed = np.exp(Margll_sel - np.max(Margll_sel), dtype=np.float128)
    # multiply by np.sqrt(2.0 * np.pi * sigma[param] ** 2.0) for each param
    # since we normalize this again, we don't need the constants
    margL_normed *= math.prod(sigma[param] for param in distance_coordinates)
    margL_normed /= np.sum(margL_normed)
    N_mn = multinomial(
        n=nsamples_per_grid * len(margL_normed),
        p=margL_normed,
        seed=random_state,
    )
    N = N_mn.rvs(1)[0]
    logging.info(f"Number of samples {N}")
    grid_id = []
    all_random_samples = {param: [] for param in distance_coordinates}
    for i in range(len(margL_normed)):
        random_samples = {param: [] for param in distance_coordinates}
        for param in distance_coordinates:
            random_samples[param] = random_state.normal(
                loc=grid_data[param][i], scale=sigma[param][i], size=N[i]
            )
            all_random_samples[param] = np.append(
                all_random_samples[param], random_samples[param]
            )
        grid_id = np.append(np.full(N[i], i), grid_id)
    param1_samples = all_random_samples[distance_coordinates[0]]
    param2_samples = all_random_samples[distance_coordinates[1]]
    if spin_included:
        param3_samples = all_random_samples[distance_coordinates[2]]
        param4_samples = all_random_samples[distance_coordinates[3]]
    if distance_coordinates_str != "mu1_mu2_q_spin2z":
        mask = BOUND_CHECK_MASS[distance_coordinates_str](
            param1_samples, param2_samples
        )

        if spin_included:
            mask &= amrlib.check_spins(param3_samples)
            mask &= amrlib.check_spins(param4_samples)
        for param in distance_coordinates:
            all_random_samples[param] = all_random_samples[param][mask]

        param1_samples = all_random_samples[distance_coordinates[0]]
        param2_samples = all_random_samples[distance_coordinates[1]]
        if spin_included:
            param3_samples = all_random_samples[distance_coordinates[2]]
            param4_samples = all_random_samples[distance_coordinates[3]]

        m1_samples, m2_samples = INVERSE_TRANSFORMS_MASS[
            VALID_TRANSFORMS_MASS[
                frozenset(distance_coordinates_str.split("_"))
            ]
        ](param1_samples, param2_samples)
        prior = jacobians.PRIOR_MAP[distance_coordinates_str](
            param1_samples, param2_samples
        )
        sample_dict["mass1"] = m1_samples
        sample_dict["mass2"] = m2_samples

        sample_dict[distance_coordinates[0]] = param1_samples
        sample_dict[distance_coordinates[1]] = param2_samples
        sample_dict["prior"] = prior
        if spin_included:
            (
                spin1z_samples,
                spin2z_samples,
            ) = amrlib.transform_chi_eff_chi_a_s1zs2z(
                m1_samples, m2_samples, param3_samples, param4_samples
            )

            sample_dict["chi_eff"] = param3_samples
            sample_dict["chi_a"] = param4_samples
            sample_dict["spin1z"] = spin1z_samples
            sample_dict["spin2z"] = spin2z_samples
    else:
        mask = amrlib.check_q(param3_samples)
        mask &= amrlib.check_spins(param4_samples)
        mu1_samples = np.array(param3_samples[mask])
        mu2_samples = np.array(param4_samples[mask])
        q_samples = np.array(param1_samples[mask])
        spin2z_samples = np.array(param2_samples[mask])

        (
            m1_samples,
            m2_samples,
            spin1z_samples,
            spin2z_samples,
        ) = amrlib.transform_mu1mu2qs2z_m1m2s1zs2z(
            mu1_samples, mu2_samples, q_samples, spin2z_samples
        )

        chi_eff_samples, chi_a_samples = amrlib.transform_s1zs2z_chi_eff_chi_a(
            m1_samples,
            m2_samples,
            spin1z_samples,
            spin2z_samples,
        )
        mu1mu2qs2z_prior = jacobians.PRIOR_MAP[distance_coordinates_str](
            mu1_samples, mu2_samples, q_samples, spin2z_samples
        )
        sample_dict["mu1"] = mu1_samples
        sample_dict["mu2"] = mu2_samples
        sample_dict["q"] = q_samples
        sample_dict["spin2z"] = spin2z_samples
        sample_dict["spin1z"] = spin1z_samples
        sample_dict["chi_eff"] = chi_eff_samples
        sample_dict["chi_a"] = chi_a_samples
        sample_dict["mass1"] = m1_samples
        sample_dict["mass2"] = m2_samples
        sample_dict["prior"] = mu1mu2qs2z_prior
    sample_dict["grid_id"] = grid_id[mask]
    return sample_dict


def compute_evidence(
    grid_data,
    prior_boundary_dict,
    sigma,
    distance_coordinates_str,
    prior_function="uniform",
    grid_level=None,
    random_state=_default_random_state,
):
    """
    Computes total evidence and category-wise evidence
    """
    prior_function = prior_function.lower()

    m_max_bank = prior_boundary_dict["m_max_bank"]
    m_min_bank = prior_boundary_dict["m_min_bank"]
    m_max_ns = prior_boundary_dict["m_max_ns"]

    count_evidence = count_bbh = count_bns = count_nsbh = 0

    distance_coordinates = list(sigma.keys())
    Margll_sel = grid_data["margll"]
    grid_it_level = grid_data["iteration_level"]
    grid_index_list = np.arange(len(grid_it_level))

    if grid_level is not None:
        grid_inds = grid_index_list[grid_it_level == grid_level]
        Margll_sel = grid_data["margll"][grid_inds]
        for param in distance_coordinates:
            grid_data[param] = grid_data[param][grid_inds]
    MargL = np.exp(Margll_sel, dtype=np.float128)
    for i in range(len(Margll_sel)):
        count_evidence_i = count_bbh_i = count_bns_i = count_nsbh_i = 0
        Nsamples = 10000
        random_samples = {param: [] for param in distance_coordinates}
        for param in distance_coordinates:
            random_samples[param] = random_state.normal(
                loc=grid_data[param][i], scale=sigma[param][i], size=Nsamples
            )
        param1_samples = random_samples[distance_coordinates[0]]
        param2_samples = random_samples[distance_coordinates[1]]
        if distance_coordinates_str != "mu1_mu2_q_spin2z":
            mask = BOUND_CHECK_MASS[distance_coordinates_str](
                param1_samples, param2_samples
            )
            for param in distance_coordinates:
                random_samples[param] = random_samples[param][mask]

            param1_samples = random_samples[distance_coordinates[0]]
            param2_samples = random_samples[distance_coordinates[1]]

            m1_samples, m2_samples = INVERSE_TRANSFORMS_MASS[
                VALID_TRANSFORMS_MASS[
                    frozenset(distance_coordinates_str.split("_"))
                ]
            ](param1_samples, param2_samples)
            uniform_prior = jacobians.PRIOR_MAP[distance_coordinates_str](
                param1_samples, param2_samples
            )
            if prior_function == "uniform":
                prior = uniform_prior
            elif prior_function == "salpeter":
                alpha = 2.35
                prior = m1_samples ** (-alpha) * uniform_prior
        else:
            param3_samples = random_samples[distance_coordinates[2]]
            param4_samples = random_samples[distance_coordinates[3]]

            mask = amrlib.check_q(param3_samples)
            mask &= amrlib.check_spins(param4_samples)
            mu1_samples = np.array(param3_samples[mask])
            mu2_samples = np.array(param4_samples[mask])
            q_samples = np.array(param1_samples[mask])
            spin2z_samples = np.array(param2_samples[mask])

            (
                m1_samples,
                m2_samples,
                spin1z_samples,
                spin2z_samples,
            ) = amrlib.transform_mu1mu2qs2z_m1m2s1zs2z(
                mu1_samples, mu2_samples, q_samples, spin2z_samples
            )

            prior = jacobians.PRIOR_MAP[distance_coordinates_str](
                mu1_samples, mu2_samples, q_samples, spin2z_samples
            )
        mchirp_samples, q_samples = amrlib.transform_m1m2_mcq(
            m1_samples, m2_samples
        )
        selected_indices_mask = q_samples <= prior_boundary_dict["q_max_bank"]
        selected_indices_mask &= (
            m1_samples <= prior_boundary_dict["m_max_bank"]
        )
        selected_indices_mask &= (
            m1_samples >= prior_boundary_dict["m_min_bank"]
        )
        selected_indices_mask &= (
            m2_samples <= prior_boundary_dict["m_max_bank"]
        )
        selected_indices_mask &= (
            m2_samples >= prior_boundary_dict["m_min_bank"]
        )
        if prior_function == "uniform":
            full_prior = prior[selected_indices_mask] / (
                (m_max_bank - m_min_bank)
                * (m1_samples[selected_indices_mask] - m_min_bank)
            )

        elif prior_function == "salpeter":
            full_prior = (
                prior[selected_indices_mask]
                * (1 - alpha)
                / (
                    (m_max_bank ** (1 - alpha) - m_min_bank ** (1 - alpha))
                    * (m1_samples[selected_indices_mask] - m_min_bank)
                )
            )
        Fofrandoms = (
            MargL[i]
            * full_prior
            * math.prod(sigma[k][i] for k in distance_coordinates)
        )
        if not np.any(selected_indices_mask):
            continue
        try:
            random_F = random_state.uniform(
                0,
                np.amax(Fofrandoms),
                size=len(Fofrandoms),
            )
        except:
            continue
        Nsamples = len(Fofrandoms)
        area_sampled = (
            (
                np.amax(mchirp_samples[selected_indices_mask])
                - np.amin(mchirp_samples[selected_indices_mask])
            )
            * (
                np.amax(q_samples[selected_indices_mask])
                - np.amin(q_samples[selected_indices_mask])
            )
            * np.amax(Fofrandoms)
        )

        m1_samples_selected = m1_samples[selected_indices_mask]
        m2_samples_selected = m2_samples[selected_indices_mask]
        if prior_function == "uniform":
            prior_norm_bbh = 1.0 / (
                (m_max_bank - m_max_ns) * (m1_samples_selected - m_min_bank)
            )
            prior_norm_bns = 1.0 / (
                (m_max_ns - m_min_bank) * (m1_samples_selected - m_min_bank)
            )
            prior_norm_nsbh = 1.0 / (
                (m_max_bank - m_max_ns) * (m1_samples_selected - m_min_bank)
            )
            prior_norm_tot = 1.0 / (
                (m_max_bank - m_min_bank) * (m1_samples_selected - m_min_bank)
            )
        elif prior_function == "salpeter":
            prior_norm_bbh = (1.0 - alpha) / (
                (m_max_bank ** (1.0 - alpha) - m_max_ns ** (1.0 - alpha))
                * (m1_samples_selected - m_max_ns)
            )
            prior_norm_bns = (1.0 - alpha) / (
                (m_max_ns ** (1.0 - alpha) - m_min_bank ** (1.0 - alpha))
                * (m1_samples_selected - m_min_bank)
            )
            prior_norm_nsbh = np.asarray(
                (1.0 - alpha)
                / (
                    (m_max_bank ** (1.0 - alpha) - m_max_ns ** (1.0 - alpha))
                    * (m_max_ns - m_min_bank)
                )
            )
            prior_norm_nsbh = np.broadcast_to(
                prior_norm_nsbh, m1_samples_selected.shape
            )

            prior_norm_tot = (1.0 - alpha) / (
                (m_max_bank ** (1.0 - alpha) - m_min_bank ** (1.0 - alpha))
                * (m1_samples_selected - m_min_bank)
            )

        count_evidence_selected_samples = random_F <= Fofrandoms
        count_evidence_i = (
            np.count_nonzero(count_evidence_selected_samples)
            * area_sampled
            / Nsamples
        )

        m1_is_bh = m1_samples_selected > m_max_ns
        m1_is_ns = m1_samples_selected <= m_max_ns
        m2_is_ns = m2_samples_selected <= m_max_ns
        m2_is_bh = m2_samples_selected > m_max_ns

        count_bns_selected_samples = (
            count_evidence_selected_samples & m1_is_ns & m2_is_ns
        )
        count_bns_i = (
            np.sum(
                prior_norm_bns[count_bns_selected_samples]
                / prior_norm_tot[count_bns_selected_samples]
            )
            * area_sampled
            / Nsamples
        )

        count_nsbh_selected_samples = (
            count_evidence_selected_samples & m1_is_bh & m2_is_ns
        )
        count_nsbh_i = (
            np.sum(
                prior_norm_nsbh[count_nsbh_selected_samples]
                / prior_norm_tot[count_nsbh_selected_samples]
            )
            * area_sampled
            / Nsamples
        )

        count_bbh_selected_samples = (
            count_evidence_selected_samples & m1_is_bh & m2_is_bh
        )
        count_bbh_i = (
            np.sum(
                prior_norm_bbh[count_bbh_selected_samples]
                / prior_norm_tot[count_bbh_selected_samples]
            )
            * area_sampled
            / Nsamples
        )

        count_evidence += count_evidence_i
        count_bns += count_bns_i
        count_nsbh += count_nsbh_i
        count_bbh += count_bbh_i

    return {
        "evidence": count_evidence,
        "BNS": count_bns,
        "NSBH": count_nsbh,
        "BBH": count_bbh,
    }


def plot_grid(
    grid_data,
    param1,
    param2,
    plot_dir,
    event_info=None,
    grid_level=None,
    injection_info=None,
):
    """
    plot grid alignment for param1 and param2 and a specific grid level.

    Valid grid_level = 0,1,2,3,....None

    Valid param1 and param2 = mass1, mass2, mchirp, eta, spin1z, spin2z,
                              mu1, mu2, q, tau0, tau3, mtotal

    grid_level=None plots the grid point from all grid levels


    """
    logging.info(
        f"plotting grids for {param1} and {param2} on grid_level={grid_level}"
    )
    Margll = grid_data["margll"]
    grid_iteration_level = grid_data["iteration_level"]
    grid_id = np.arange(len(grid_iteration_level))
    if grid_level is not None:
        grid_inds = grid_id[grid_iteration_level == grid_level]
        data1 = grid_data[param1][grid_inds]
        data2 = grid_data[param2][grid_inds]
        weight = Margll[grid_inds]
    else:
        data1 = grid_data[param1]
        data2 = grid_data[param2]
        weight = Margll
    plt.figure()
    plt.scatter(
        data1,
        data2,
        c=weight,
        vmin=np.min(Margll),
        vmax=np.max(Margll),
    )
    plot_xmin = np.min(grid_data[param1])
    plot_xmax = np.max(grid_data[param1])
    plot_ymin = np.min(grid_data[param2])
    plot_ymax = np.max(grid_data[param2])
    if event_info is not None:
        plt.plot(
            event_info[param1],
            event_info[param2],
            "r*",
            label="pipeline_recovered",
        )
        plot_xmin = np.min([plot_xmin, event_info[param1]])
        plot_xmax = np.max([plot_xmax, event_info[param1]])
        plot_ymin = np.min([plot_ymin, event_info[param2]])
        plot_ymax = np.max([plot_ymax, event_info[param2]])
    if injection_info is not None:
        plt.plot(
            injection_info[param1],
            injection_info[param2],
            "m+",
            label="injected",
        )
        plot_xmin = np.min([plot_xmin, injection_info[param1]])
        plot_xmax = np.max([plot_xmax, injection_info[param1]])
        plot_ymin = np.min([plot_ymin, injection_info[param2]])
        plot_ymax = np.max([plot_ymax, injection_info[param2]])

    plt.xlabel(f"{param1}_d")
    plt.ylabel(f"{param2}_d")
    x_width = plot_xmax - plot_xmin
    y_width = plot_ymax - plot_ymin
    plt.xlim(
        plot_xmin - (0.1 * x_width),
        plot_xmax + (0.1 * x_width),
    )
    plt.ylim(
        plot_ymin - (0.1 * y_width),
        plot_ymax + (0.1 * y_width),
    )
    if grid_level is not None:
        plt.title("grid_level = " + str(grid_level))
    else:
        plt.title("all grids")
    plt.colorbar(label=r"$log(L_{marg})$")
    plt.legend()
    if grid_level is not None:
        filename = (
            f"{plot_dir}/grid_{param1}"
            f"_{param2}_iteration-{str(grid_level)}.png"
        )
    else:
        filename = f"{plot_dir}/grid_{param1}_{param2}_all.png"
    plt.savefig(filename)
    return


def plot_posterior(
    sample_dict,
    param,
    plot_dir,
    event_info=None,
    grid_level=None,
    injection_info=None,
):
    """
    Plotting and saving posterior distribution
    """
    logging.info(f"plotting posterior for {param} at grid_level={grid_level}")
    samples = sample_dict[param]

    prior = sample_dict["prior"]
    prior /= np.sum(prior)
    fig, ax = plt.subplots()

    lo, hi = np.percentile(samples, [0.1, 99.9])
    if event_info is not None:
        ax.axvline(
            x=event_info[param], color="red", label="pipeline_recovered"
        )
        lo = min(lo, event_info[param])
        hi = max(hi, event_info[param])
    if injection_info is not None:
        ax.axvline(x=injection_info[param], color="magenta", label="injected")
        lo = min(lo, injection_info[param])
        hi = max(hi, injection_info[param])
    lo = lo - (hi - lo) * 0.01
    hi = hi + (hi - lo) * 0.01
    bins = np.linspace(lo, hi, 50)
    ax.hist(
        samples,
        bins=bins,
        weights=prior,
        histtype="step",
        density=True,
        color="g",
    )
    ax.set_xlabel(f"{param}_d")
    ax.set_ylabel("posterior")
    ax.legend()
    ax.yaxis.set_ticks([])
    ax.set_xlim(lo, hi)
    if grid_level is not None:
        plt.title("grid_level = " + str(grid_level))
        filename = (
            f"{plot_dir}/posterior_detframe"
            f"{param}_iteration-{str(grid_level)}.png"
        )
    else:
        plt.title("all grids")
        filename = f"{plot_dir}/posterior_detframe_{param}_all.png"
    plt.savefig(filename)
    return


def plot_2d_posterior_with_grid(
    sample_dict,
    grid_data,
    distance_coordinates_str,
    plot_dir,
    grid_level=None,
    event_info=None,
    injection_info=None,
):
    """
    Plotting and saving 2d posterior distribution
    """
    distance_coordinates = distance_coordinates_str.split("_")
    param1_name = distance_coordinates[0]
    param2_name = distance_coordinates[1]
    grid_iteration_level = grid_data["iteration_level"]
    grid_id = np.arange(len(grid_iteration_level))
    if grid_level is not None:
        grid_inds = grid_id[grid_iteration_level == grid_level]
        data1 = grid_data[param1_name][grid_inds]
        data2 = grid_data[param2_name][grid_inds]
        weight = grid_data["margll"][grid_inds]
    else:
        data1 = grid_data[param1_name]
        data2 = grid_data[param2_name]
        weight = grid_data["margll"]
    all_weights = grid_data["margll"]
    plt.figure()
    plt.scatter(
        data1,
        data2,
        c=weight,
        vmin=np.min(all_weights),
        vmax=np.max(all_weights),
    )
    if event_info is not None:
        plt.plot(
            event_info[param1_name],
            event_info[param2_name],
            "r*",
            label="pipeline_recovered",
        )
    if injection_info is not None:
        plt.plot(
            injection_info[param1_name],
            injection_info[param2_name],
            "m+",
            label="injected",
        )

    plt.xlabel(f"{param1_name}_d")
    plt.ylabel(f"{param2_name}_d")
    plt.colorbar(label=r"$ln(L_{marg})$")
    plt.legend()

    samples1 = sample_dict[param1_name]
    samples2 = sample_dict[param2_name]
    prior = sample_dict["prior"]
    plt.hist2d(samples1, samples2, bins=50, weights=prior, density=True)
    if grid_level is not None:
        plt.title("grid_level = ", str(grid_level))
        filename = (
            f"{plot_dir}/{param1_name}_{param2_name}"
            f" _iteration-{str(grid_level)}.png"
        )
    else:
        plt.title("all grids")
        filename = f"{plot_dir}/{param1_name}_{param2_name}_all.png"
    plt.savefig(filename)
    return


def save_m1m2_weighted_samples(sample_dict, save_dir):
    """
    saving weighted posterior samples for intrinsic paramters
    in detector frame in h5 format"
    """
    logging.info(
        "saving weighted posterior samples for intrinsic"
        "paramters in detector frame"
    )
    filename = os.path.join(save_dir, "intrinsic_weighted_samples_detframe.h5")
    keys = ["mass1", "mass2", "grid_id", "prior"]
    if "spin1z" in sample_dict:
        keys += ["spin1z", "spin2z"]
    rpe_utils.save_dict_in_hdf(sample_dict, filename, keys_to_save=keys)


def save_m1m2_posterior_samples(
    sample_dict, save_dir, n=10000, random_state=_default_random_state
):
    """
    saving poserior samples for intrinsic paramters
    in detector frame in h5 format
    """
    logging.info(
        "saving poserior samples for intrinsic paramters in detector frame"
    )
    filename = os.path.join(
        save_dir, "intrinsic_posterior_samples_detframe.h5"
    )
    keys = ["mass1", "mass2"]
    if "spin1z" in sample_dict:
        keys += ["spin1z", "spin2z"]
    p = sample_dict["prior"]
    p /= np.sum(p)
    indices = random_state.choice(
        len(sample_dict["mass1"]), size=n, replace=True, p=p
    )
    resampled_dict = {k: sample_dict[k][indices] for k in keys}
    rpe_utils.save_dict_in_hdf(
        resampled_dict,
        filename,
        keys_to_save=keys,
        group_name="posterior_samples",
    )
