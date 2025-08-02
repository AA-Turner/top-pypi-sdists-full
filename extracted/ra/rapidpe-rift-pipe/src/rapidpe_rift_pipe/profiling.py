#!/usr/bin/env python3

import os
import shutil

import importlib.resources

from pstats import f8
from dataclasses import dataclass
from typing import Dict


@dataclass
class FunctionProfile:
    ncalls: int
    tottime: float
    percall_tottime: float
    cumtime: float
    percall_cumtime: float
    file_name: str
    line_number: int
    func_name: str


@dataclass
class StatsProfile:
    """Class for keeping track of an item in inventory."""

    total_tt: float
    func_profiles: Dict[str, FunctionProfile]


def get_stats_profile(stats):
    """This method returns an instance of StatsProfile,
    which contains a mapping of function names to instances
    of FunctionProfile. Each FunctionProfile instance holds
    information related to the function's profile such as how
    long the function took to run, how many times it was called, etc...
    """
    func_list = (
        stats.fcn_list[:] if stats.fcn_list else list(stats.stats.keys())
    )
    if not func_list:
        return StatsProfile(0, {})

    total_tt = float(f8(stats.total_tt))
    func_profiles = {}
    stats_profile = StatsProfile(total_tt, func_profiles)

    for func in func_list:
        cc, nc, tt, ct, callers = stats.stats[func]
        file_name, line_number, func_name = func
        ncalls = str(nc) if nc == cc else (str(nc) + "/" + str(cc))
        tottime = float(f8(tt))
        percall_tottime = -1 if nc == 0 else float(f8(tt / nc))
        cumtime = float(f8(ct))
        percall_cumtime = -1 if cc == 0 else float(f8(ct / cc))
        func_profile = FunctionProfile(
            ncalls,
            tottime,  # time spent in this function alone
            percall_tottime,
            cumtime,  # time spent in the function plus all functions that this function called,
            percall_cumtime,
            file_name,
            line_number,
            func_name,
        )
        func_profiles[func_name] = func_profile

    return stats_profile


def write_css_file(public_html_dir, static_css_file):
    '''
    Copy a css file to the  public html dir
    '''
    with importlib.resources.path('rapidpe_rift_pipe.static', static_css_file) as  p:
       css_path = p
    shutil.copy(css_path, os.path.join(public_html_dir, static_css_file))
