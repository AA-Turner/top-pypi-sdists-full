"""Helper module that contains a set of useful simple and generic functions

JB, September 2018
"""

__RCSID__ = "$Id$"

import copy
import datetime
import os
import re

import DIRAC
from DIRAC.Core.Utilities.ReturnValues import returnSingleResult
from DIRAC.Resources.Catalog.FileCatalogClient import FileCatalogClient

# Jobs status dictionnary
BASE_STATUS_DIR = {
    "Received": 0,
    "Matched": 0,
    "Waiting": 0,
    "Running": 0,
    "Failed": 0,
    "Stalled": 0,
    "Rescheduled": 0,
    "Checking": 0,
    "Done": 0,
    "Completing": 0,
    "Completed": 0,
    "Killed": 0,
    "Total": 0,
}

# Data level meta data id
DATA_LEVEL_METADATA_ID = {
    "MC0": -3,
    "R0": -2,
    "R1": -1,
    "DL0": 0,
    "DL1": 1,
    "DL2": 2,
    "DL3": 3,
    "DL4": 4,
    "DL5": 5,
}


def highlight(string):
    """highlight a string in a terminal display"""
    return f"\x1b[31;1m{string}\x1b[0m"


def read_inputs_from_file(file_path):
    """Read inputs from an ASCII files
    Used for list of LFN or list of datasets
    Expects just one LFN/dataset per line
    """
    content = open(file_path).readlines()
    input_file_list = []
    for line in content:
        infile = line.strip()
        if line != "\n":
            input_file_list.append(infile)
    return input_file_list


def extract_run_number_from_logs_tgz(filename):
    match = re.search(r"_(\d+)\.logs\.tgz$", filename)
    return int(match.group(1)) if match else -1


def extract_run_number_from_chimp_mars(filename):
    match = re.search(r"run(\d+)___cta", filename)
    return int(match.group(1)) if match else -1


def extract_run_number_from_corsika_sim_telarray(filename):
    if filename.endswith(".corsika.zst"):
        match = re.search(r"run(\d+)_", os.path.basename(filename))
    elif "tid" in filename:
        match = re.search(r"tid(\d+)", os.path.basename(filename))
    elif filename.endswith(".log"):
        match = re.search(r"run(\d+)\.log$", os.path.basename(filename))
    elif filename.endswith(".corsika.log.gz"):
        match = re.search(r"run(\d+)", os.path.basename(filename))
    else:
        match = re.search(r"run(\d+)___cta", filename)
    return int(match.group(1)) if match else -1


def extract_run_number_from_simpipe(filename):
    match = re.search(r"_run(\d+)_", os.path.basename(filename))

    return int(match.group(1)) if match else -1


def extract_run_number_from_evndisplay(filename):
    if "tid" in filename:
        match = re.search(r"tid(\d+)", os.path.basename(filename))
    elif filename.endswith(("DL1.root", "DL2.root", "DL1.tar.gz", "DL2.tar.gz")):
        match = re.search(r"run(\d+)___cta", filename)
    else:
        match = re.search(r"(\d+)-", filename)
    return int(match.group(1)) if match else -1


def extract_run_number_from_image_extractor(filename):
    match = re.search(r"srun(\d+)-", filename)
    return int(match.group(1)) if match else -1


def extract_run_number_from_dl1_data_handler(filename):
    match = re.search(r"runs(\d+)-", filename)
    return int(match.group(1)) if match else -1


def extract_run_number_from_ctapipe(filename):
    match = re.search(r"run(\d+)___cta", filename)
    return int(match.group(1)) if match else -1


def run_number_from_filename(filename, package):
    """Try to get a run number from the file name

    return:
        run_number : int - the run number
    """
    if filename.endswith(".logs.tgz"):
        return extract_run_number_from_logs_tgz(filename)

    package_extractors = {
        "chimp": extract_run_number_from_chimp_mars,
        "mars": extract_run_number_from_chimp_mars,
        "corsika_simhessarray": extract_run_number_from_corsika_sim_telarray,
        "corsika_simtelarray": extract_run_number_from_corsika_sim_telarray,
        "simpipe": extract_run_number_from_simpipe,
        "evndisplay_dl1": extract_run_number_from_evndisplay,
        "evndisplay_dl2": extract_run_number_from_evndisplay,
        "image_extractor": extract_run_number_from_image_extractor,
        "dl1_data_handler": extract_run_number_from_dl1_data_handler,
        "ctapipe_dl1": extract_run_number_from_ctapipe,
        "ctapipe_dl2": extract_run_number_from_ctapipe,
    }

    if package in package_extractors:
        return package_extractors[package](filename)

    return -1


def check_dataset_query(dataset_name):
    """print dfind command for a given dataset"""
    md_dict = get_dataset_MQ(dataset_name)
    return debug_query(md_dict)


def debug_query(MDdict):
    """just unwrap a meta data dictionnary into a dfind command"""
    msg = "dfind /vo.cta.in2p3.fr/MC/"
    for key, val in MDdict.items():
        try:
            val = val.values()[0]
        except BaseException:
            pass
        msg += f" {key}={val}"
    return msg


def get_dataset_MQ(dataset_name):
    """Return the Meta Query associated with a given dataset"""
    fc = FileCatalogClient()
    result = returnSingleResult(fc.getDatasetParameters(dataset_name))
    if not result["OK"]:
        DIRAC.gLogger.error("Failed to retrieved dataset:", result["Message"])
        DIRAC.exit(-1)
    else:
        DIRAC.gLogger.info("Successfully retrieved dataset: ", dataset_name)
    return result["Value"]["MetaQuery"]


def get_job_list(owner, job_group, n_hours):
    """get a list of jobs for a selection"""
    from DIRAC.Interfaces.API.Dirac import Dirac

    dirac = Dirac()

    now = datetime.datetime.now()
    onehour = datetime.timedelta(hours=1)
    results = dirac.selectJobs(
        jobGroup=job_group, owner=owner, date=now - n_hours * onehour
    )
    if "Value" not in results:
        DIRAC.gLogger.error(
            'No job found for group "%s" and owner "%s" in the past %s hours'
            % (job_group, owner, n_hours)
        )
        DIRAC.exit(-1)

    # Found some jobs, print information)
    jobs_list = results["Value"]
    return jobs_list


def parse_jobs_list(jobs_list):
    """parse a jobs list by first getting the status of all jobs"""
    from DIRAC.Interfaces.API.Dirac import Dirac

    dirac = Dirac()
    # status of all jobs
    status = dirac.getJobStatus(jobs_list)
    # parse it
    sites_dict = {}
    status_dict = copy.copy(BASE_STATUS_DIR)
    for job in jobs_list:
        site = status["Value"][int(job)]["Site"]
        majstatus = status["Value"][int(job)]["Status"]
        if majstatus not in status_dict.keys():
            DIRAC.gLogger.notice(f"Add {majstatus} to BASE_STATUS_DIR")
            DIRAC.sys.exit(1)
        status_dict[majstatus] += 1
        status_dict["Total"] += 1
        if site not in sites_dict.keys():
            if site.find(".") == -1:
                site = "    None"  # note that blank spaces are needed
            sites_dict[site] = copy.copy(BASE_STATUS_DIR)
            sites_dict[site][majstatus] = 1
            sites_dict[site]["Total"] = 1
        else:
            sites_dict[site]["Total"] += 1
            if majstatus not in sites_dict[site].keys():
                sites_dict[site][majstatus] = 1
            else:
                sites_dict[site][majstatus] += 1
    return status_dict, sites_dict


def get_os_and_cpu_info():
    """get OS and instructions supported by current cpu"""
    import platform
    import re
    import subprocess

    platform = platform.platform()
    cpuinfo = subprocess.check_output("cat /proc/cpuinfo", shell=True, text=True)
    model_name = subprocess.check_output(
        'grep -m 1 "model name" /proc/cpuinfo', shell=True, text=True
    ).strip()
    for inst in ["avx512", "avx2", "avx", "sse4"]:
        if re.search(inst, cpuinfo) is not None:
            break
    return (platform, model_name, inst)
