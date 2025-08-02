"""
Generates and submits HTCondor jobs for rapidPE and RIFT
"""

__author__ = "Caitlin Rose, Daniel Wysocki, Sinead Walsh, Soichiro Morisaki, Vinaya Valsan"

import sys
import os
import json
import logging

import time
import glob
import h5py
import shutil
import numpy as np
import lal
import requests.exceptions
import urllib.parse

from rapid_pe import lalsimutils
from argparse import ArgumentParser
from ligo.gracedb.rest import GraceDb, HTTPError
from rapidpe_rift_pipe.modules import (
    check_switch_m1m2s1s2,
    convert_injections_txt_to_objects,
    construct_event_time_string,
    convert_list_string_to_dict,
    correct_list_string_formatting_if_list_string,
    transform_s1zs2z_chi,
)
from rapidpe_rift_pipe.search_bias_bounds import parse_search_bias_bounds
from rapid_pe import amrlib


import gwpy.timeseries
from ligo.lw import ligolw
from ligo.lw import lsctables
from ligo.lw import utils as ligolw_utils
from rapidpe_rift_pipe.config import Config
from sklearn.neighbors import BallTree


@lsctables.use_in
class LIGOLWContentHandler(ligolw.LIGOLWContentHandler):
    pass


# Exit statuses
_NO_TRIGGER_EXIT_CODE = 100

_allowed_pipelines = ["gstlal", "spiir", "MBTA", "pycbc"]

# Default channels from: https://wiki.ligo.org/LSC/JRPComm/ObsRun3
# TODO: Add K1 and offline channel names from:
#       https://wiki.ligo.org/LSC/JRPComm/ObsRun4
# TODO: Do this more programmatically.  Data isn't in GraceDB, but maybe is
#       accessible from GWDataFind?
_run_mode_to_channels = {
    "online": {
        "H1": "GDS-CALIB_STRAIN_CLEAN",
        "L1": "GDS-CALIB_STRAIN_CLEAN",
        "V1": "Hrec_hoft_16384Hz",
    },
    "o2replay": {
        "H1": "GDS-CALIB_STRAIN_O2Replay",
        "L1": "GDS-CALIB_STRAIN_O2Replay",
        "V1": "Hrec_hoft_16384Hz_O2Replay",
    },
    "o3replay": {
        "H1": "GDS-CALIB_STRAIN_INJ1_O3Replay",
        "L1": "GDS-CALIB_STRAIN_INJ1_O3Replay",
        "V1": "Hrec_hoft_16384Hz_INJ1_O3Replay",
    },
    "o4llpic": {
        "H1": "GDS-CALIB_STRAIN_CLEAN_INJ1_O4Replay",
        "L1": "GDS-CALIB_STRAIN_CLEAN_INJ1_O4Replay",
        "V1": "Hrec_hoft_16384Hz_INJ1_O4Replay",
    },
}

shm_basedir = "/dev/shm/kafka/"

_run_mode_to_shm_dir = {}
_run_mode_to_shm_dir["online"] = {
    ifo: os.path.join(shm_basedir, ifo)
    for ifo in ["H1", "L1", "V1"]
}
_run_mode_to_shm_dir["o3replay"] = {
    ifo: os.path.join(shm_basedir, f"{ifo}_O3ReplayMDC")
    for ifo in ["H1", "L1", "V1"]
}
_run_mode_to_shm_dir["o4llpic"] = {
    ifo: os.path.join(shm_basedir, f"{ifo}_O4LLPIC")
    for ifo in ["H1", "L1", "V1"]
}


def make_parser():
    parser = ArgumentParser()

    parser.add_argument(
        "config",
        help="Configuration file.",
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output.",
    )

    return parser


def main():
    cli_parser = make_parser()
    cli_args = cli_parser.parse_args()

    if cli_args.verbose:
        logging_level = logging.DEBUG
    else:
        logging_level = logging.INFO

    logging.basicConfig(level=logging_level)

    logging.info(os.uname())

    cfgname = os.path.abspath(cli_args.config)
    config = Config.load(cfgname)

    # Validate environment variables
    if len(config.getenv) == 0 and len(config.environment) == 0:
        logging.warning(
            "No environment variables being passed to HTCondor.  "
            "You may want to set `getenv' and/or `environment' in the General "
            "config section."
        )

    # TODO: make this a configuration option
    init_directory = os.getcwd()
    output_parent_directory = config.output_parent_directory
    use_skymap = config.use_skymap
    use_event_spin = config.use_event_spin
    email_address_for_job_complete_notice = (
        config.email_address_for_job_complete_notice
    )
    intrinsic_param_to_search = config.intrinsic_param_to_search
    # TODO: handle verbosity levels with `logging` module
#    verbose = True

    is_event = config.event.mode in {"sid", "gid"}

    if not is_event:
        # Start injections workflow
        injections = None
        read_inj_index = 0
        if config.event.injections_file.endswith(".txt"):
            injections = convert_injections_txt_to_objects(
                config.event.injections_file
            )
            read_inj_index = 1
        else:
            xmldoc = ligolw_utils.load_filename(
                config.event.injections_file,
                verbose=True, contenthandler=LIGOLWContentHandler,
            )
            injections = lsctables.SimInspiralTable.get_table(xmldoc)

        inj_index = 0
        n_submitted = 0
        params_all = {}
        n_events = len(injections)
    else:
        n_events = 1

    for event_index in range(n_events):
        #os.chdir(init_directory)
        if is_event:
            fmin_template = float(
                config.integrate_likelihood_cmds_dict["fmin-template"]
            )

            # lvalert submission script workflow
            client = GraceDb(config.gracedb_url)
            event = None
            # TODO: check whether we should be getting the submitter name
#            submitter = ""
            packet = ""
            lvalert = False
            if config.event.mode == 'sid':
                retry_times = [1]*2 + [5]*2 + [30]*2
                tried_events = set()
                gracedb_id = None
                for retry_time in retry_times:
                    is_failed = False
                    try:
                        sevent = client.superevent(config.event.superevent_id).json()
                    except HTTPError as e:
                        logging.exception(f'Failed while requesting superevent {config.event.superevent_id}')
                        is_failed = True
                    except requests.exceptions.JSONDecodeError as e:
                        logging.exception(f'Failed while parsing superevent {config.event.superevent_id}')
                        is_failed = True
                    if not is_failed:
                        preferred_event_id = sevent['preferred_event']
                        preferred_search_ok = sevent['preferred_event_data']['search']=='AllSky'
                        preferred_group_ok = sevent['preferred_event_data']['group']=='CBC'
                        preferred_pipeline_ok = sevent['preferred_event_data']['pipeline'] in _allowed_pipelines
                        if preferred_search_ok and preferred_group_ok and preferred_pipeline_ok:
                            gracedb_id = preferred_event_id
                            logging.info(f"Using preferred_event: {gracedb_id} from {sevent['preferred_event_data']['pipeline']}")
                            break
                        else:
                            gw_events = sevent["gw_events"]
                            new_gw_events = set(gw_events) - tried_events
                            current_event_snr = 0.0
                            for event_name in new_gw_events:
                                try:
                                    event = client.event(event_name).json()
                                except HTTPError as e:
                                    logging.exception(f"Failed while requesting gevent {event_name}")
                                    tried_events.add(event_name)
                                    continue
                                except requests.exceptions.JSONDecodeError as e:
                                    logging.exception(f'Failed while parsing gevent {event_name}')
                                    tried_events.add(event_name)
                                    continue
                                try:
                                    search_ok = event['search'] == "AllSky"
                                    group_ok = event['group']=='CBC'
                                    pipeline_ok = event['pipeline'] in _allowed_pipelines
                                    if search_ok and group_ok and pipeline_ok:
                                        event_snr = event['extra_attributes']['CoincInspiral']['snr']
                                        if event_snr>current_event_snr:
                                            gracedb_id = event_name
                                            current_event_snr = event_snr
                                            logging.info(f'Updating selected event: {event_name}')
                                    else:
                                        logging.info(f'Skipping {event_name}')
                                    tried_events.add(event_name)
                                except KeyError:
                                    logging.exception(f'missing key in {event_name}')
                                    continue
                            if gracedb_id is not None:
                                logging.info(f"Using highest snr trigger from {event['pipeline']}: {gracedb_id}")
                                break
                    if gracedb_id is None:
                        logging.info("No AllSky CBC event found, retrying in %s seconds", retry_time)
                        time.sleep(retry_time)
                if gracedb_id is None:
                    logging.error("No AllSky CBC event found after %s seconds", sum(retry_times))
                    sys.exit(_NO_TRIGGER_EXIT_CODE)
            elif config.event.mode == 'gid':
                gracedb_id = config.event.gracedb_id
            else:
                raise RuntimeError(f'Unknown mode {config.event.mode}')

            event = client.event(gracedb_id).json()
            insp_type = event["extra_attributes"]
            pipeline = event["pipeline"]

            # Ensure m1 >= m2 in SingleInspiral
            for insp in insp_type["SingleInspiral"]:
                if insp["mass2"] > insp["mass1"]:
                    logging.warning(
                        "Template mass2 > mass1 for IFO %s.  Re-ordering.",
                        insp["ifo"],
                    )
                    insp["mass1"], insp["mass2"] = insp["mass2"], insp["mass1"]

            print("event info", event)

            # Take the information from the first detector.
            # Template parameters are required to be the same across templates
            # for gstlal.
            coinc = insp_type["CoincInspiral"]

            # Gather event info in format needed for following scripts.
            params = insp_type["SingleInspiral"][0]
            event_info = {}
            event_info["gracedb_id"] = gracedb_id
            event_info["event_time"] = construct_event_time_string(
                params["end_time"], params["end_time_ns"],
            )
            event_info["snr"] = coinc["snr"]
            event_info["likelihood"] = event["likelihood"]


        else:
            inj = injections[event_index]
            event_info = {}
            # TODO: double check this is still used
            if read_inj_index:
                # Note: this is only true for the inj files I generated with
                # generate_injections.
                # Here the index is set to the index in the original injections
                # file.
                inj_index = inj.alpha6
            event_info = config.common_event_info.copy()
            # If the cache file input includes the expression $INJINDEX$ it
            # will be replaced by the inj index
            if config.use_skymap:
                if "$INJINDEX$" in event_info["skymap_file"]:
                    event_info["skymap_file"] = (
                        event_info["skymap_file"].replace(
                            "$INJINDEX$", str(int(inj_index))
                        )
                    )
                if not os.path.isfile(event_info["skymap_file"]):
                    sys.exit(
                        "ERROR: you've requested use_skymap but the skymap"
                        "file you've specified doesn't exist: "
                        + event_info["skymap_file"]
                    )
            if "$INJINDEX$" in event_info["cache_file"]:
                event_info["cache_file"] = (
                    event_info["cache_file"].replace(
                        "$INJINDEX$", str(int(inj_index))
                    )
                )
            if not os.path.isfile(event_info["cache_file"]):
                sys.exit(
                    "ERROR: cache file doesn't exist: "
                    + event_info["cache_file"]
                )
            event_info["output_event_ID"] = f"inj_{inj_index}"
            output_event_directory = event_info["output_event_ID"]
            output_dir = os.path.abspath(
                    os.path.join(
                        config.output_parent_directory, 
                        output_event_directory,
                        ),
                    )
            event_all_iterations_fname = os.path.join(
                output_dir, "event_all_iterations.dag",
            )
            if not os.path.isdir(output_dir):
                os.makedirs(output_dir, exist_ok=True)
            elif os.path.isfile(event_all_iterations_fname):
                # Skip this inejction if it has already been submitted
                continue

            event_info["output_event_ID"] = f"inj_{inj_index}"
            event_info[
                "event_time"] = construct_event_time_string(
                inj.geocent_end_time, inj.geocent_end_time_ns,
            )
            event_info["snr"] = inj.snr
            params = check_switch_m1m2s1s2({
                "mass1": inj.mass1,
                "mass2": inj.mass2,
                "spin1z": inj.spin1z,
                "spin2z": inj.spin2z,
            })
            params_all[inj_index] = params
            # Save all the true injected values for
            # pp plots or other tests later
            injection_param_list = [
                f"mass1={params['mass1']}",
                f"mass2={params['mass2']}",
                f"spin1z={params['spin1z']}",
                f"spin2z={params['spin2z']}",
                f"longitude={inj.longitude}",
                f"latitude={inj.latitude}",
                f"distance={inj.distance}",
                f"inclination={inj.inclination}",
                f"phase={inj.phi0}",
                f"polarization={inj.psi0}",
            ]
            event_info[
                "injection_param"] = f"[{','.join(injection_param_list)}]"
        intrinsic_param_list = [
            f"{ip}={params[ip]}"
            for ip in intrinsic_param_to_search
        ]
        event_info[
            "intrinsic_param"] = f"[{','.join(intrinsic_param_list)}]"
        event_info[
            "wrapper_script_start_time"] = time.time()
        # TODO: Clean up this comment, too much detail specific to the time
        # it was written.
        # Determine which approximant should be used based on the total mass
        # the threshold is from the gstlal O2 template bank threshold:
        # https://arxiv.org/pdf/1812.05121.pdf
        # NRHybridSurrogate up to q=8, should work with everything.
        # Review finishing now. Ask Seb?
        # At very high mass, waveform generator will fail. No inspiral phase at
        # very high mass. Waveform generator requires you to start at inspiral
        # phase.
        integrate_likelihood_cmds_dict = config.integrate_likelihood_cmds_dict
        if is_event:
            if use_event_spin:
                event_info["event_spin"] = {'spin1z':params['spin1z'],'spin2z':params['spin2z']}
            if 'approximant' in integrate_likelihood_cmds_dict:
                event_info["approximant"] = integrate_likelihood_cmds_dict['approximant']
            else:
                event_params_mchirp,_ = amrlib.transform_m1m2_mcq(float(params["mass1"]),float(params["mass2"]))
                if event_params_mchirp> 2.6:
                    event_info["approximant"] = "SEOBNRv4_ROM"  # v4 vs v4_ROM
                else:
                    if use_event_spin or "spin1z" in intrinsic_param_to_search:
                        # SpinTaylorT4 is the fastest for spinning searches.
                        event_info["approximant"] = "SpinTaylorT4"
                    else:
                        # TaylorT2 is the fastest in general.
                        event_info["approximant"] = "TaylorT2"

            output_dir = os.path.abspath(config.output_parent_directory)
            if not os.path.isdir(output_dir):
                os.makedirs(output_dir, exist_ok=True)

            if packet != "":
                packet_fname = os.path.join(output_dir, "lvalert_packet.txt")
                with open(packet_fname, "w") as packet_file:
                    print(packet, file=packet_file)

        else:
            if use_event_spin:
                event_info["event_spin"] = {'spin1z':params['spin1z'],'spin2z':params['spin2z']}
            if 'approximant' in integrate_likelihood_cmds_dict:
                event_info["approximant"] = integrate_likelihood_cmds_dict['approximant']
            else:
                event_params_mchirp,_ = amrlib.transform_m1m2_mcq(float(params["mass1"]),float(params["mass2"]))
                if event_params_mchirp>2.6:
                    # Note: pp-plots injections used SEOBNRv4, NOT SEOBNRv4_ROM
                    event_info["approximant"] = "SEOBNRv4"
                else:
                    if use_event_spin or "spin1z" in intrinsic_param_to_search:
                        # SpinTaylorT4 is the fastest for spinning searches.
                        event_info["approximant"] = "SpinTaylorT4"
                    else:
                        # all approximants checked with BNS
                        event_info["approximant"] = "TaylorF2"
        event_info["output_dir"] = output_dir
        if is_event:
            coinc_xml_filename = os.path.join(output_dir, "coinc.xml")
            # The PSD file name is set here, but it's written later because
            # sometimes it takes a while for the file to upload
            psd_filename = os.path.join(output_dir, "psd.xml.gz")
            skymap_filename = os.path.join(output_dir, "bayestar.fits")

            # If not pulling the channel names from GraceDB, get the dict
            # mapping IFO -> channel name
            if config.event.run_mode != "gracedb":
                ifo_to_channel = _run_mode_to_channels[config.event.run_mode]

            # Now, based on the event_time, find the frame files you want.
            channel_str = "["
            psd_file_str = "["
            num_ifos = 0
            ifo_list = []
            for insp in insp_type["SingleInspiral"]:
                ifo = insp["ifo"]
                ifo_list.append(ifo)
                logging.info("IFO: %s", ifo)

                if config.event.run_mode == "gracedb":
                    # Get the channel name from GraceDB
                    channel = insp["channel"]
                else:
                    try:
                        # Get the channel name based on the hard-coded value
                        # for the IFO.
                        channel = ifo_to_channel[ifo]
                    except KeyError:
                        # No hard coded value found.  This might happen if a
                        # new IFO (e.g., K1) is added without us hard-coding
                        # it.
                        logging.warning(
                            "Could not find channel name for IFO `%s' in run "
                            "mode `%s'.  Skipping `%s'",
                            ifo, config.event.run_mode, ifo,
                        )
                        continue

                logging.info("Channel: %s", channel)

                channel_str += f"{ifo}={channel},"
                psd_file_str += f"{ifo}={psd_filename},"

                # Copied from Richards code
                # https://git.ligo.org/richard-oshaughnessy/research-projects-RIT/blob/temp-RIT-Tides-port_master-GPUIntegration/MonteCarloMarginalizeCode/Code/helper_LDG_Events.py
                # Estimate signal duration
                t_event = insp["end_time"]
                P = lalsimutils.ChooseWaveformParams()
                P.m1 = insp["mass1"]*lal.MSUN_SI
                P.m2 = insp["mass2"]*lal.MSUN_SI
                P.fmin = fmin_template
                P.tref = t_event
                logging.debug("P: %s, %s, %s", P.m1, P.m2, P.fmin)

                expected_duration = lalsimutils.estimateWaveformDuration(P)
                coinc_minimum_duration = coinc['minimum_duration']
                t_duration = (
                    expected_duration if coinc_minimum_duration is None
                    else max(coinc_minimum_duration, expected_duration)
                )

                logging.info(
                    "DONE Estimate duration: %s, %s, %s",
                    t_duration,
                    coinc["minimum_duration"],
                    lalsimutils.estimateWaveformDuration(P)
                )
                # Buffer for inverse spectrum truncation.

                t_before_cache = 200
                t_after_cache = 14
                t_mr_buffer = 10
                t_duration_buffer = 50
                data_start_time = int(t_event - t_before_cache)
                data_end_time = int(t_event + t_after_cache)

                event_info['data_start_time'] = int(t_event - t_duration_buffer)
                event_info['data_end_time'] = int(t_event + t_mr_buffer)

                cache_fname = cache_data(
                    config,
                    ifo=ifo, channel=channel,
                    start_time=data_start_time, end_time=data_end_time,
                )
                # TODO: Use `cache_fname` when creating Condor submit files to
                #       pass the data without relying on NFS.
                num_ifos += 1

            if num_ifos == 0:
                logging.error("Failed to load data from any IFOs.")

            # path2cache always assumes data is in output_dir, so that path
            # needs to be removed before passing output to data.cache
            text_for_sed_removal = "localhost{}\/file:\\/".format(
                init_directory.replace('/', '\\/')
            )
            if shutil.which('lal_path2cache') is not None:
                path2cache = 'lal_path2cache'
            else:
                path2cache = 'lalapps_path2cache'
            data_cache_file_path = os.path.join(output_dir,'data.cache')
            os.system(
                f"cat {output_dir}/*_raw.cache "
                f"| {path2cache} "
                f"| sed 's/{text_for_sed_removal}//g' > {data_cache_file_path}"
            )

            # Check if the data.cache file is empty
            if os.stat(data_cache_file_path).st_size == 0:
                if lvalert and email_address_for_job_complete_notice != "":
                    email_cmd = (
                        f"Failed Lvalert, no data at trigger time "
                        f"{gracedb_id} | mail -s {output_parent_directory} "
                        f"          {email_address_for_job_complete_notice}"
                    )
                    # TODO: Instead of system call, should use Python's
                    # standard email modules
                    os.system(email_cmd)

                sys.exit(
                    "ERROR: There is no data at the time when this triggered, "
                    "how can that happen?"
                )
            # Put together cache file
            event_info["cache_file"] = data_cache_file_path
            event_info["psd_file"] = psd_file_str[:-1] + "]"
            event_info["channel_name"] = channel_str[:-1] + "]"
            event_info["coinc_xml_file"] = coinc_xml_filename

            mdc_event_injection_file = config.event.mdc_event_injection_file
            is_mdc = "INJ" in event_info["channel_name"] and mdc_event_injection_file is not None
            if is_mdc:
                mdc_time_offset = int(config.event.mdc_time_offset)
                mdc_xml_doc = ligolw_utils.load_filename(
                        mdc_event_injection_file,
                        contenthandler=ligolw.LIGOLWContentHandler,
                        )
                mdc_sim_inspiral_tbl = lsctables.SimInspiralTable.get_table(mdc_xml_doc)
                list_of_keys = ["gpstime","mass1","mass2","spin1z","spin2z","distance","latitude","longitude"]
                mdc_data_dict = {k: [] for k in list_of_keys}
                for row in mdc_sim_inspiral_tbl:
                    for key in list_of_keys:
                        if key== 'gpstime':
                           mdc_data_dict[key].append(row.geocent_end_time + 1e-9 * row.geocent_end_time_ns)
                        else:
                            mdc_data_dict[key].append(getattr(row,key))
                time_diff_from_injections = np.absolute(np.array(mdc_data_dict['gpstime'])-float(event_info['event_time'])+mdc_time_offset)
                nearest_inj_index = np.argmin(time_diff_from_injections)
                mdc_injection_info = {k:0 for k in list_of_keys}
                nearest_injection_found = False
                if time_diff_from_injections[nearest_inj_index] <=1.0:
                    logging.info('Mapping trigger to an injection')
                    nearest_injection_found = True
                    for k in list_of_keys:
                        if k == 'gpstime':
                            mdc_injection_info[k] = mdc_data_dict[k][nearest_inj_index]+mdc_time_offset
                        else:
                            mdc_injection_info[k] = mdc_data_dict[k][nearest_inj_index]
                    logging.info(f'Nearby injection info: {mdc_injection_info}')

        from . import create_submit_dag_one_event
        if config.submit_only_at_exact_signal_position:
            # Only submit one integrate job at the exact signal position
            event_info_list_strings_reformatted = {
                key : correct_list_string_formatting_if_list_string(val)
                for key, val in event_info.items()
            }
            create_submit_dag_one_event.main(
                config, event_info_list_strings_reformatted,
            )
        else:
            # Create the initial grid for this event
            intrinsic_param = convert_list_string_to_dict(
                event_info["intrinsic_param"]
            )
            exe = config.exe_grid_refine

            intrinsic_grid_name_base = os.path.join(output_dir,"intrinsic_grid")
            initial_grid_xml = intrinsic_grid_name_base+"_iteration_0.xml.gz"
            initial_grid_hdf = intrinsic_grid_name_base+"_all_iterations.hdf"
            # now fill in the rest
            cmd = (
                f"{exe} --verbose --no-exact-match --setup "
                f"{initial_grid_hdf} --output-xml-file-name {initial_grid_xml}"
            )
            if config.distance_coordinates != "":
                cmd += " -d "+config.distance_coordinates

            # Add the event trigger parameters, the inital grid will include
            # all points in the overlap bank with overlap < the -T value
            for param, val in intrinsic_param.items():
                print(param, val)
                cmd += " -i "+param+"="+str(val)
            cmd += config.initial_grid_only_cli_args
            if use_event_spin:
                cmd += f" --pin-param spin1z={params['spin1z']} --pin-param spin2z={params['spin2z']}"

            # Apply the parameter limits from
            # the 'initial_region' config option.
            if config.initial_grid_setup.mode == "initial_region":
                for (
                    param,
                    vals,
                ) in config.initial_grid_setup.initial_region.items():
                    if len(vals) != 2:
                        raise ValueError(
                            f"Expected 2 values for parameter {param} in "
                            f"'initial_region', got {len(vals)} instead."
                        )

                    val_lo, val_hi = vals
                    cmd += f" -I {param}={val_lo},{val_hi}"
            elif config.initial_grid_setup.mode == "search_bias_bounds":
                logging.info(
                    f"Constructing initial grid from search bias bounds, "
                    f"according to the config file: "
                    f"{config.initial_grid_setup.search_bias_bounds_spec}"
                )

                shutil.copy(
                    config.initial_grid_setup.search_bias_bounds_spec,
                    os.path.join(output_dir, "search_bias_bounds.json")
                )

                search_bias_bounds_spec_file = (
                    open(config.initial_grid_setup.search_bias_bounds_spec, "r")
                )
                with search_bias_bounds_spec_file:
                    search_bias_bounds_spec = json.load(
                        search_bias_bounds_spec_file
                    )

                m1_rec = params["mass1"]
                m2_rec = params["mass2"]

                recovered = {
                    "snr": event_info["snr"],
                    "mchirp": lalsimutils.mchirp(m1_rec, m2_rec),
                    "mtotal": m1_rec + m2_rec,
                    "q": m2_rec / m1_rec,
                }

                limits = parse_search_bias_bounds(recovered,
                                                  search_bias_bounds_spec)

                for param, (val_lo, val_hi) in limits.items():
                    cmd += f" -I {param}={val_lo},{val_hi}"

            elif config.initial_grid_setup.mode == "overlap_bank":
                # The overlap files are split by Mchirp, it takes time to check all
                # files and see which one contains our signal. Here, we check the
                m1 = float(intrinsic_param["mass1"])
                m2 = float(intrinsic_param["mass2"])
                s1 = s2 = 0
                if "spin1z" in intrinsic_param:
                    s1 = float(intrinsic_param["spin1z"])
                    s2 = float(intrinsic_param["spin2z"])

                chi_eff_event = transform_s1zs2z_chi(m1, m2, s1, s2)
                Mchirp_event = ((m1*m2)**(3/5.0))/((m1 + m2)**(1/5.0))
                eta_event = ((m1*m2)/((m1+m2)**2.))
                print("Event mchirp", Mchirp_event, eta_event)

                # Reducing list of files to those in mchirp range
                olap_filenames = glob.glob(config.initial_grid_setup.overlap_bank)
                count_files = 0
                # strings_to_include = "{"
                min_dist = -1
                min_dist_filename = ""

                # TODO: Note that if we provide one file, it's always used, but if
                #       we provide multiple, there's a possibility no file contains
                #       the template, and we error out.  So providing `A.hdf` might
                #       work, but providing `A.hdf` and `B.hdf` triggers an error.
                #       This seems like bad behavior and should be addressed.
                if len(olap_filenames) == 0:
                    sys.exit("ERROR: no overlap files found")
                elif len(olap_filenames) == 1:
                    count_files = 1
                    cmd += f" --use-overlap {olap_filenames[0]}"
                else:
                    for hdf_filename in olap_filenames:
                        with h5py.File(hdf_filename, "r") as h5file:
                            wfrm_fam = next(iter(h5file.keys()))
                            mdata = h5file[wfrm_fam]
                            m1, m2 = mdata["mass1"][:], mdata["mass2"][:]
                            ntemplates = len(mdata["overlaps"])
                            m1, m2 = (
                                mdata["mass1"][:ntemplates],
                                mdata["mass2"][:ntemplates]
                            )
                            Mchirps = ((m1*m2)**(3/5.0))/((m1+m2)**(1/5.0))
                            if min(Mchirps) <= Mchirp_event <= max(Mchirps):
                                print(hdf_filename)
                                s1, s2 = (
                                    mdata["spin1z"][:ntemplates],
                                    mdata["spin2z"][:ntemplates]
                                )
                                etas = ((m1*m2)/((m1+m2)**2.))
                                chi_effs = transform_s1zs2z_chi(m1, m2, s1, s2)
                                # FIXME: even if youre not searching over spin, you
                                #        want to find the file with the closest
                                #        template assuming spin=0 implement above
                                #        here at same time as code
                                list_for_tree = np.asarray([Mchirps, etas]).T
                                pt = np.asarray([Mchirp_event, eta_event])
                                if "spin1z" in intrinsic_param:
                                    list_for_tree = np.asarray(
                                        [Mchirps, etas, chi_effs]
                                    ).T
                                    pt = np.asarray([
                                        Mchirp_event,
                                        eta_event,
                                        chi_eff_event
                                    ])

                                tree = BallTree(list_for_tree)
                                dist, m_idx = tree.query(np.atleast_2d(pt), k=1)
                                if dist < min_dist or min_dist_filename == "":
                                    min_dist = dist
                                    min_dist_filename = hdf_filename

                                count_files += 1
                                cmd += f" --use-overlap {hdf_filename}"
                    if count_files == 0:
                        sys.exit("ERROR: No overlap files found")

            elif config.initial_grid_setup.mode == "svd_bounds":
                # Get the trigger's masses
                m1_trigger = float(intrinsic_param["mass1"])
                m2_trigger = float(intrinsic_param["mass2"])
                mtot_trigger = m1_trigger + m2_trigger
                eta_trigger = m1_trigger*m2_trigger * mtot_trigger**-2.0
                mchirp_trigger = eta_trigger**0.6 * mtot_trigger

                trigger_vals = {
                    "mass1": m1_trigger,
                    "mass2": m2_trigger,
                    "mtot": mtot_trigger,
                    "mchirp": mchirp_trigger,
                    "eta": eta_trigger,
                }

                # Load the fixed boundary values for the SVD bins
                with open(config.initial_grid_setup.svd_bounds_file, "r") as f:
                    svd_bounds = json.load(f)

                # Download the SVD bin information from this specific event.
                trigger_history = (
                    client.files(gracedb_id, 'trigger_history.json').json()
                )

                # Get list of SNRs associated with each SVD bin
                # NOTE: We handle multiple file formats for now, but can settle
                #       on whichever one is kept in O4.
                if "svdbin" in trigger_history:
                    svd_bin_labels = trigger_history["svdbin"]
                    svd_bin_snrs = trigger_history["snr"]
                else:
                    svd_bin_labels = list(trigger_history.keys())
                    svd_bin_snrs = [
                        trigger_history[label]["snr"]
                        for label in svd_bin_labels
                    ]

                # Convert to arrays
                svd_bin_labels = np.asarray(svd_bin_labels)
                svd_bin_snrs = np.asarray(svd_bin_snrs)

                # Sort the labels from lowest to highest SNR
                svd_bin_argsort = np.argsort(svd_bin_snrs)
                svd_bin_labels_sorted = svd_bin_labels[svd_bin_argsort]

                # Open file specifying multiple methods to choose SVD depth
                with open(config.initial_grid_setup.svd_depth_json, "r") as f:
                    svd_depth_spec = json.load(f)

                # Make a copy of SVD depth JSON file in run directory
                shutil.copy(
                    config.initial_grid_setup.svd_depth_json,
                    os.path.join(output_dir, "svd_depth_spec.json"),
                )

                # Decide which method to use to select the SVD bins
                found_region = False
                for region_spec in svd_depth_spec:
                    # If the bounds for this region contain the trigger, use it
                    if all(lo <= trigger_vals[param] < hi
                           for param, (lo, hi)
                           in region_spec["bounds"].items()):
                        fudge_factors = region_spec["fudge_factors"]
                        svd_depth = region_spec["svd_depth"]

                        found_region = True
                        break

                if not found_region:
                    raise RuntimeError(
                        "svd_depth_json in [InitialGridSetup] did not include "
                        "a region with bounds that contain the trigger "
                        f"parameters: {trigger_vals}"
                    )


                # Get the highest SNR bin labels
                # TODO: Add other options for how to select from this list.
                svd_bin_labels_keep = (
                    svd_bin_labels_sorted[-svd_depth:]
                )

                # Get the information associated with each bin we're going to
                # keep
                svd_bounds_keep = [
                    svd_bounds["bins"][label]
                    for label in svd_bin_labels_keep
                ]

                # Get the parameter ranges associated with the selected SVD bins
                mins = {
                    param : min(
                        bounds[f"min_{param}"] for bounds in svd_bounds_keep
                    )
                    for param in config.initial_grid_setup.svd_bin_params
                }
                maxs = {
                    param : max(
                        bounds[f"max_{param}"] for bounds in svd_bounds_keep
                    )
                    for param in config.initial_grid_setup.svd_bin_params
                }

                # Adjust the limits by adding/subtracting a fraction of the
                # original range
                for param in config.initial_grid_setup.svd_bin_params:
                    init_range = maxs[param] - mins[param]
                    padding = 0.5 * init_range * fudge_factors[param]
                    mins[param] -= padding
                    maxs[param] += padding

                for param in config.initial_grid_setup.svd_bin_params:
                    cmd += f" -I {param}={mins[param]},{maxs[param]}"

            else:
                raise ValueError(
                    f"Unknown initial grid setup mode: "
                    f"'{config.initial_grid_setup.mode}'"
                )

            logging.info(cmd)
            exit_status = os.system(cmd)
            if exit_status != 0:
                logging.error(cmd)
                sys.exit("ERROR: non zero exit status"+str(exit_status))

            print(
                f"[initial_grid_xml={initial_grid_xml},"
                f"initial_grid_hdf={initial_grid_hdf}]"
            )

        intrinsic_grid_name_base = os.path.join(output_dir,"intrinsic_grid")
        event_info["initial_grid_xml"] = (
            f"{intrinsic_grid_name_base}_iteration_0.xml.gz"
        )
        event_info["initial_grid_hdf"] = (
            f"{intrinsic_grid_name_base}_all_iterations.hdf"
        )

        if is_event:
            with open(coinc_xml_filename,'wb') as coincfileobj:
                logging.info(
                        f"Downloading coinc.xml from {gracedb_id} ...")
                r = client.files(gracedb_id, 'coinc.xml')
                logging.info("coinc.xml has been successfully downloaded.")
                logging.info(r.headers)
                for line in r:
                    coincfileobj.write(line)
            # Get the psd file and write locally
            # This is done after the intrinsic grid generation because
            # sometimes the file takes time to upload.

            with open(psd_filename, 'wb') as psdfileobj:
                try:
                    logging.info(
                        f"Downloading psd.xml.gz from {gracedb_id} ...")
                    r = client.files(gracedb_id, 'psd.xml.gz')
                    logging.info(
                        "psd.xml.gz has been successfully downloaded.")
                    logging.info(r.headers)
                    for line in r:
                        psdfileobj.write(line)

                except HTTPError:
                    logging.info(
                        "psd.xml.gz was not successfully downloaded. "
                        "Using coinc.xml instead ...")
                    shutil.copyfile(coinc_xml_filename, psd_filename)
            event_info['pipeline'] = event['pipeline']
            if event['pipeline'] == 'pycbc':
                ## correct for f0 offset
                shutil.copyfile(psd_filename,os.path.join(
                    output_dir, "shifted_psd.xml.gz"))
                corrected_psd_dict = {}
                psd_f0_list = []
                for ifo in ifo_list:
                    shifted_psd_data_obj = lalsimutils.get_psd_series_from_xmldoc(
                            psd_filename,ifo
                    )
                    shifted_psd_data = shifted_psd_data_obj.data.data
                    f0 = shifted_psd_data_obj.f0
                    psd_f0_list.append(f0)
                    deltaF = shifted_psd_data_obj.deltaF

                    n_to_add =  int(f0/deltaF)
                    f_array = np.arange(
                            (n_to_add+len(shifted_psd_data))*deltaF,step=deltaF
                    )
                    psd_to_add =  list(np.ones(n_to_add)*shifted_psd_data[0])
                    psd_corrected = np.zeros(len(f_array))
                    psd_corrected[:n_to_add] = psd_to_add
                    psd_corrected[n_to_add:] = shifted_psd_data
                    epoch = lal.LIGOTimeGPS(shifted_psd_data_obj.epoch)
                    psd_corrected_obj = lal.CreateREAL8FrequencySeries(
                            name=ifo, epoch=epoch, f0=0.0, deltaF=deltaF, 
                            sampleUnits="s", length=len(f_array)
                    )
                    psd_corrected_obj.data.data=psd_corrected
                    corrected_psd_dict[ifo] =  psd_corrected_obj
                psd_corrected_xmldoc = lal.series.make_psd_xmldoc(corrected_psd_dict)
                psd_corrected_xmldoc.childNodes[0].attributes._attrs  = {"Name": "psd"}
                ligolw_utils.write_filename(psd_corrected_xmldoc, psd_filename, compress="gz")
                event_info["psd_f0"] = max(psd_f0_list)
            if use_skymap:
                with open(skymap_filename, 'wb') as skymapfileobj:
                    if config.event.superevent_id:
                        r = client.files(
                            config.event.superevent_id, 'bayestar.fits.gz'
                        )
                    else:
                        r = client.files(
                            gracedb_id, 'bayestar.multiorder.fits'
                        )
                    for line in r:
                        skymapfileobj.write(line)

                event_info["skymap_file"] = skymap_filename
            if is_mdc and nearest_injection_found:
                with open(os.path.join(output_dir, "injection_info.txt"),'w') as injectionobj:
                    json.dump(mdc_injection_info, injectionobj)


        # Run create_submit_dag
        event_info_list_strings_reformatted = {
            key : correct_list_string_formatting_if_list_string(val)
            for key, val in event_info.items()
        }
        create_submit_dag_one_event.main(
            config, event_info_list_strings_reformatted,
        )
        if email_address_for_job_complete_notice != "":
            email_cmd = (
                f"echo 'Sent for dag submission {json.dumps(event_info)}' "
                f"| mail -s 'rapidPE:{output_parent_directory}' "
                f"          {email_address_for_job_complete_notice}"
            )
            os.system(email_cmd)
        if not is_event:
            logging.info("Events submitted %s", inj_index)
            n_submitted += 1
            if n_submitted % 10 != 0:
                logging.warning("Waiting for 3 seconds!!!!")
                time.sleep(3)
            if not read_inj_index:
                inj_index += 1



def cache_data(config, *, ifo, channel, start_time, end_time):
    output_dir = os.path.abspath(config.output_parent_directory)
    raw_cache_file_path = os.path.join(output_dir, f"{ifo[0]}_raw.cache")

    data_type = config.event.frame_data_types[ifo]

    channel = f"{ifo}:{channel}"
    if config.event.query_shm:
        try:
            shm_dir = _run_mode_to_shm_dir[config.event.run_mode]
            data = get_data_shm(shm_dir=shm_dir[ifo],
                                ifo=ifo,
                                channel=channel, data_type=data_type,
                                start_time=start_time, end_time=end_time)

        except FileNotFoundError:
            logging.info(
                "Shared-memory data unavailable for %s between %s and %s",
                ifo, start_time, end_time,
            )

            data = get_data_gwpy(channel=channel, data_type=data_type,
                                 start_time=start_time, end_time=end_time)
    else:
        data = get_data_gwpy(channel=channel, data_type=data_type,
                             start_time=start_time, end_time=end_time)

    if data is None:
        logging.error("Failed to fetch data for IFO %s", ifo)
        return

    actual_start = data.times[0].value
    actual_duration = data.duration.value

    # NOTE: Copied this from Bilby, seems a little wonky.
    #       Converts float to int, but only if it's equivalent.
    if int(actual_duration) == actual_duration:
        actual_duration = int(actual_duration)

    output_gwf_path = os.path.join(
        output_dir,
        f"{ifo[0]}-{data_type}-{actual_start}-{actual_duration}.gwf"
    )
    data.write(output_gwf_path)
    logging.info("Wrote %s data to %s", ifo, output_gwf_path)

    with open(raw_cache_file_path, "w") as cache_file:
        print(urllib.parse.urljoin("file://localhost", output_gwf_path), file=cache_file)

    return raw_cache_file_path


def get_data_shm(*, shm_dir, ifo, channel, data_type, start_time, end_time):
    segments = []
    for time in range(start_time, end_time):
        gwf_path = os.path.join(shm_dir,
                                f"{ifo[0]}-{data_type}-{time}-1.gwf")

        logging.info("Attempting to load data from %s", gwf_path)

        segments.append(
            gwpy.timeseries.TimeSeries.read(gwf_path, channel=channel)
        )

    return gwpy.timeseries.TimeSeriesList(*segments).join()


gwpy_retry_times = [30]*2 + [60]*2
def get_data_gwpy(*, channel, data_type, start_time, end_time):
    for retry_time in gwpy_retry_times:
        try:
            logging.info(
                "Attempting to fetch %s from %s to %s with GWpy discovery",
                channel, start_time, end_time,
            )
            return gwpy.timeseries.TimeSeries.get(
                channel=channel, frametype=data_type,
                start=start_time, end=end_time,
            )
        except RuntimeError:
            logging.exception(
                "Failed to discover data with GWpy, retrying in %s sec",
                retry_time,
            )
            time.sleep(retry_time)

    logging.error(
        "Failed to discover data with GWpy after %s attempts in %s sec",
        len(gwpy_retry_times), sum(gwpy_retry_times),
    )


if __name__ == '__main__':
    main()
