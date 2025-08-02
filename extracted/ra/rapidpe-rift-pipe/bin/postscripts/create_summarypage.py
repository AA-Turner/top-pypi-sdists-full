#!/usr/bin/env python3

"""
Creates summary page from RapidPE/RIFT results
"""

__author__ = "Vinaya Valsan"

import os

import numpy as np

from glob import glob
from argparse import ArgumentParser
from urllib.parse import urlparse

import rapidpe_rift_pipe.postscript_utils as postutils

from rapidpe_rift_pipe.config import Config
from rapidpe_rift_pipe.profiling import write_css_file
from rapidpe_rift_pipe.utils import print_output

optp = ArgumentParser()
optp.add_argument("input_dir", help="path to event run dir")
optp.add_argument("--web-dir", default=None, help="path to web dir")
optp.add_argument("--output-dir", default=None, help="directory to save plots")
opts = optp.parse_args()
print("-----------Creating summary page--------------")
input_dir = opts.input_dir

if opts.web_dir:
    output_dir = opts.web_dir
else:
    output_dir = os.path.join(
        os.getenv("HOME"),
        f'public_html/RapidPE/{input_dir[input_dir.rfind("output/") + 7 :]}',
    )
os.makedirs(output_dir, exist_ok=True)
write_css_file(output_dir, "stylesheet.css")

if opts.output_dir:
    run_dir = opts.output_dir
else:
    run_dir = input_dir
summary_plot_dir = os.path.join(run_dir, "summary")

os.system(f"cp {summary_plot_dir}/* {output_dir}/")
print(f"Summary page will be saved in {output_dir}")
index_html_file = os.path.join(output_dir, "summarypage.html")

html_file = open(index_html_file, "w")


print_output(
    html_file,
    """
<html>
<head>
<link rel="stylesheet" href="stylesheet.css">
<script src="https://www.kryogenix.org/code/browser/sorttable/sorttable.js"></script>
</head>
""",
)

print_output(html_file, "<body>")
print_output(html_file, f"<h2>rundir = {run_dir}</h2>")

event_info = postutils.event_info(input_dir)

event_info_dict = event_info.load_event_info()

print_output(html_file, "<h1> Event Info  </h1>")
print_output(
    html_file,
    f"""
snr = {event_info_dict["snr"]} <br>
approximant = {event_info_dict["approximant"]} <br>
pipeline_recovered_param = {event_info_dict["intrinsic_param"]} <br>
event_time = {event_info_dict["event_time"]} <br>
""",
)
config = Config.load(os.path.join(input_dir, "Config.ini"))
is_event = config.event.mode in {"sid", "gid"}
if is_event:
    gracedb_url = urlparse(config.gracedb_url)
    if config.event.mode == "sid":
        event_id = config.event.superevent_id
        event_path = f"/superevents/{event_id}/view/"
    else:
        event_id = config.event.gracedb_id
        event_path = f"/events/{event_id}/view/"
    event_url = gracedb_url._replace(path=event_path).geturl()
    print_output(
        html_file, f'GraceDB url : <a href="{event_url}">{event_id}</a> <br>'
    )

filelist = glob(output_dir + "/grid*png")
print_output(html_file, "<h1> Grid Plots </h1>")
distance_coordinate = config.distance_coordinates
all_grid_fname = os.path.join(
    output_dir, f"grid_{distance_coordinate}_all.png"
)
print_output(html_file, f'<img src="{os.path.basename(all_grid_fname)}">')
distance_coordinate_filelist = glob(
    f"{output_dir}/grid_{distance_coordinate}_iteration-*.png"
)
for fname_full in sorted(distance_coordinate_filelist):
    fname = os.path.basename(fname_full)
    print_output(html_file, f'<img src="{fname}">')
remaining_filelist = (
    set(filelist) - set([all_grid_fname]) - set(distance_coordinate_filelist)
)
for fname_full in sorted(remaining_filelist):
    fname = os.path.basename(fname_full)
    print_output(html_file, f'<img src="{fname}">')

print_output(html_file, "<h1> Posterior Plots </h1>")


filelist = glob(output_dir + "/posterior*.png")
for fname_full in sorted(filelist):
    fname = os.path.basename(fname_full)
    print_output(html_file, f'<img src="{fname}">')

filelist = glob(output_dir + "/p_astro*png")
if filelist != []:
    print_output(html_file, "<h1> Pastro </h1>")
    for fname_full in sorted(filelist):
        fname = os.path.basename(fname_full)
        print_output(html_file, f"<br>{fname}")
        print_output(html_file, f'<img src="{fname}">')

filelist = glob(output_dir + "/skymap*png")
if len(filelist) != 0:
    print_output(html_file, "<h1> Skymaps </h1>")
    for fname_full in sorted(filelist):
        fname = os.path.basename(fname_full)
        print_output(html_file, f"<br>{fname}")
        print_output(html_file, f'<img src="{fname}">')


if config.cProfile:
    print_output(html_file, """<h1> Timing </h1> """)

    if os.path.exists(f"{summary_plot_dir}/cprofile.html"):
        filelist = np.sort(glob(output_dir + "/cprofile*hist*png"))
        for fname_full in sorted(filelist):
            fname = os.path.basename(fname_full)
            print_output(html_file, f'<img src="{fname}">')

    # Total job time:
    condor_submit_time = int(event_info_dict["condor_submit_time"])
    job_timing_file = os.path.join(input_dir, "job_timing.txt")
    iteration_completion_time = []
    with open(job_timing_file) as f:
        lines = f.readlines()
        for line_id, line in enumerate(lines):
            line_split = line.split(" ")
            level_complete_time = float(line_split[1])
            iteration_completion_time.append(level_complete_time)
            if line_id == 0:
                print_output(
                    html_file,
                    f'<br> <font size="+2"> iteration level {line_split[0]} took '
                    f"{level_complete_time-condor_submit_time} s </font>",
                )
            else:
                print_output(
                    html_file,
                    f'<br> <font size="+2"> iteration level {line_split[0]} took '
                    f"{level_complete_time-iteration_completion_time[line_id-1]} s </font>",
                )

    if os.path.exists(f"{summary_plot_dir}/cprofile.html"):
        print_output(
            html_file,
            "<br><a href='cprofile.html'>Detailed cProfile info for a single ILE job</a>",
        )
    print_output(html_file, "<h1> Config.ini </h1>")

with open(os.path.join(input_dir, "Config.ini")) as config_f:
    for line in config_f:
        if line[0] != "#" and len(line.strip()) > 0:
            if line[0] == "[":
                print_output(html_file, f"<br> <b> {line} </b>")
            else:
                print_output(html_file, f"<br> {line}")


print_output(html_file, "</body></html>")

html_file.close()
