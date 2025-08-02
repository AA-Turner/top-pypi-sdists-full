#!/usr/bin/env python3

"""
Creates cprofile summary page from RapidPE/RIFT results
"""

__author__ = "Vinaya Valsan"

import os
import shutil
import pstats

import numpy as np
import matplotlib.pyplot as plt

from glob import glob
from argparse import ArgumentParser
from rapidpe_rift_pipe.profiling import get_stats_profile
from rapidpe_rift_pipe.utils import print_output

optp = ArgumentParser()
optp.add_argument("input_dir", help="path to event run dir")
optp.add_argument("--web-dir", default=None, help="path to web dir")
optp.add_argument("--output-dir", default=None, help="directory to save plots")
opts = optp.parse_args()

input_dir = opts.input_dir

if opts.output_dir:
    run_dir = opts.output_dir
else:
    run_dir = input_dir
summary_plot_dir = os.path.join(run_dir, "summary")

cprofile_html_file = open(os.path.join(summary_plot_dir, "cprofile.html"), "w")
print_output(
    cprofile_html_file,
    """
<html>
<head>
<link rel="stylesheet" href="stylesheet.css">
<script src="https://www.kryogenix.org/code/browser/sorttable/sorttable.js"></script>
</head>
""",
)
table_thread = """
<thead>
        <tr>
          <th class="num">
            <button>
              ncalls
              <span aria-hidden="true"></span>
            </button>
          </th>
          <th class="num">
            <button>
              cumtime
              <span aria-hidden="true"></span>
            </button>
          </th>
          <th class="num">
            <button>
              percall cumtime
              <span aria-hidden="true"></span>
            </button>
          </th>
          <th>
            <button>
              line number
              <span aria-hidden="true"></span>
            </button>
          </th>
          <th>
              file name
          </th>
          <th>
              function name
          </th>
        </tr>
      </thead>
"""

print_output(cprofile_html_file, "<body>")

file_list = glob(f"{run_dir}/logs/cprofile_*.out")

File_name = []
ILE_SCRIPT_RUNTIME = []
Iter_level = []
PRECOMPUTE_TIME = []
LIKELIHOOD_EVALUATION_TIME = []
PRESET_TIME = []
ANALYZE_EVENT = []

for n, ff in enumerate(file_list):
    try:
        file_name = ff.split("/")[-1]
        ps = pstats.Stats(ff)
        ps.strip_dirs()
        timestamped_stats_profiles = []
        iter_level = ff[ff.find("ILE_iteration") + len("ILE_iteration_") : -4]
        stats_profile = get_stats_profile(ps)
        all_func_profiles = stats_profile.func_profiles
        all_keys = list(all_func_profiles.keys())
        precompute_time = all_func_profiles[
            "PrecomputeLikelihoodTerms"
        ].cumtime

        # all_line_numbers = [all_func_profiles[k].line_number for k in all_keys]
        # analyze_event_line = all_func_profiles['analyze_event'].line_number
        # ind_lines_before_analyze_event = np.where(np.array(all_line_numbers)<analyze_event_line)[0]
        # pre_func = np.array(all_keys)[ind_lines_before_analyze_event]
        # preset_time = sum([all_func_profiles[k].tottime for k in pre_func])
        # PRESET_TIME.append(preset_time)
        likelihood_evaluation_time = all_func_profiles[
            "likelihood_function"
        ].cumtime

        analyze_event = all_func_profiles["analyze_event"].cumtime

        ile_script_runtime = stats_profile.total_tt
        if n == 0:
            shutil.copyfile(ff, os.path.join(summary_plot_dir, file_name))
            print_output(
                cprofile_html_file, f"<details><summary>{file_name}</summary>"
            )

            print_output(cprofile_html_file, '<table class="sortable">')
            print_output(
                cprofile_html_file,
                f"""<caption>
                Download cprofile stats file <a href='./{file_name}' download>here</a>
                </caption>""",
            )
            print_output(cprofile_html_file, table_thread)

            print_output(cprofile_html_file, "<tbody>")
            for func_key in all_keys:
                print_output(
                    cprofile_html_file,
                    f"""<tr>
                <td>{all_func_profiles[func_key].ncalls}</td>
                <td>{all_func_profiles[func_key].cumtime}</td>
                <td>{all_func_profiles[func_key].percall_cumtime}</td>
                <td>{all_func_profiles[func_key].line_number}</td>
                <td>{all_func_profiles[func_key].file_name}</td>
                <td>{all_func_profiles[func_key].func_name}</td>
                </tr>""",
                )
            print_output(cprofile_html_file, "</tbody></table></details>")
    except KeyError:
        continue
    File_name.append(file_name)
    Iter_level.append(iter_level)
    ILE_SCRIPT_RUNTIME.append(ile_script_runtime)
    PRECOMPUTE_TIME.append(precompute_time)
    LIKELIHOOD_EVALUATION_TIME.append(likelihood_evaluation_time)
    ANALYZE_EVENT.append(analyze_event)

if File_name != []:
    save_data = np.column_stack(
        [
            File_name,
            Iter_level,
            ILE_SCRIPT_RUNTIME,
            PRECOMPUTE_TIME,
            LIKELIHOOD_EVALUATION_TIME,
            ANALYZE_EVENT,
        ]
    )
    np.savetxt(
        f"{summary_plot_dir}/cprofile_summary.txt",
        save_data,
        header="FILENAME ITER_LEVEL ILE_SCRIPT_RUNTIME PRECOMPUTE_TIME LIKELIHOOD_EVALUATION_TIME ANALYZE_EVENT",
        fmt="%s",
    )

    unique_iter_levels = np.unique(Iter_level)

    plt.figure()
    plt.hist(PRECOMPUTE_TIME, bins=int(len(PRECOMPUTE_TIME) / 5))
    plt.xlabel("PRECOMPUTE_TIME(s)")
    plt.savefig(summary_plot_dir + "/cprofile_PRECOMPUTE_TIME_hist.png")

    plt.figure()
    plt.hist(ILE_SCRIPT_RUNTIME, bins=int(len(PRECOMPUTE_TIME) / 5))
    plt.xlabel("ILE_SCRIPT_RUNTIME(s)")
    plt.savefig(summary_plot_dir + "/cprofile_ILE_SCRIPT_RUNTIME_hist.png")

    plt.figure()
    plt.hist(ANALYZE_EVENT, bins=int(len(PRECOMPUTE_TIME) / 5))
    plt.xlabel("ANALYZE_EVENT(s)")
    plt.savefig(summary_plot_dir + "/cprofile_ANALYZE_EVENT_hist.png")

    plt.figure()
    plt.hist(
        np.array(ILE_SCRIPT_RUNTIME) - np.array(ANALYZE_EVENT),
        bins=int(len(PRECOMPUTE_TIME) / 5),
    )
    plt.xlabel("ILE_SCRIPT_RUNTIME-ANALYZE_EVENT (s)")
    plt.savefig(summary_plot_dir + "/cprofile_PRESET_TIME_hist.png")


print_output(cprofile_html_file, "</body></html>")
