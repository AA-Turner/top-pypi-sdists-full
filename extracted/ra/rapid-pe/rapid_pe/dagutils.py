# Copyright (C) 2013, 2015  Evan Ochsner, Chris Pankow
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

"""
A collection of routines to manage Condor workflows (DAGs).
"""

import warnings
import os,ast

from pathlib import PurePath
from glue import pipeline

__author__ = "Evan Ochsner <evano@gravity.phys.uwm.edu>, Chris Pankow <pankow@gravity.phys.uwm.edu>"

# Taken from
# http://pythonadventures.wordpress.com/2011/03/13/equivalent-of-the-which-command-in-python/
def is_exe(fpath):
    return os.path.exists(fpath) and os.access(fpath, os.X_OK)

def which(program):
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file): return exe_file

    return None

def escape_quotes(s):
    """
    Escapes quotes in a string for use in a Condor submit file.

    Any quote character is simply repeated twice, removing its special meaning
    and making it behave as a literal quote character.
    """
    return s.replace('"', '""').replace("'", "''")

def format_getenv(getenv):
    """
    Produces the 'getenv' section's value for a Condor submit file, given a
    list of environment variable names.
    """
    return ", ".join(getenv)

def format_environment(environment_dict):
    """
    Produces the 'environment' section's value for a Condor submit file, given
    a dictionary of environment variable names and values.

    This uses the 'new' format (space-delimited key=value pairs with
    double-quotes enclosing the entire list), with literal quotes properly
    escaped, and with single-quotes used to surround each value in case it
    contains whitespace.
    """
    # Compute key='value' pairs, quoted properly
    pairs = (f"{k}='{escape_quotes(v)}'"
             for k, v in environment_dict.items())
    # Join the pairs into a single string
    contents = " ".join(pairs)
    # Construct the final expression
    return f'"{contents}"'


# FIXME: Keep in sync with arguments of integrate_likelihood_extrinsic
def write_integrate_likelihood_extrinsic_sub(tag='integrate', exe=None, log_dir=None, intr_prms=("mass1", "mass2"), ncopies=1, condor_commands=None, getenv=None, environment_dict=None, **kwargs):
    """
    Write a submit file for launching jobs to marginalize the likelihood over
    extrinsic parameters.

    Inputs:
        - 'tag' is a string to specify the base name of output files. The output
          submit file will be named tag.sub, and the jobs will write their
          output to tag-ID.out, tag-ID.err, tag.log, where 'ID' is a unique
          identifier for each instance of a job run from the sub file.
        - 'cache' is the path to a cache file which gives the location of the
          data to be analyzed.
        - 'coinc' is the path to a coincident XML file, from which masses and
          times will be drawn FIXME: remove this once it's no longer needed.
        - 'channelH1/L1/V1' is the channel name to be read for each of the
          H1, L1 and V1 detectors.
        - 'psdH1/L1/V1' is the path to an XML file specifying the PSD of
          each of the H1, L1, V1 detectors.
        - 'ncopies' is the number of runs with identical input parameters to
          submit per condor 'cluster'

    Outputs:
        - An instance of the CondorDAGJob that was generated for ILE
    """
    #If a kwarg option is defined as e.g. psd_file, convert it to psd-file because that's what the executable takes as input
    new_kwargs = {}
    for opt, param in kwargs.items():
        if isinstance(param,str) and len(param) > 1 and param[0] == "[" and param[-1] == "]":
            param = ast.literal_eval(param)
        new_kwargs[opt.replace("_","-")] = param
    kwargs = new_kwargs

    assert len(kwargs["psd-file"]) == len(kwargs["channel-name"])

    exe = exe or which("rapidpe_integrate_extrinsic_likelihood")
    ile_job = pipeline.CondorDAGJob(universe="vanilla", executable=exe)
    # This is a hack since CondorDAGJob hides the queue property
    ile_job._CondorJob__queue = ncopies

    ile_sub_name = tag +'_'+kwargs['iteration-level']+'.sub'
    ile_job.set_sub_file(ile_sub_name)

    #
    # Logging options
    #
    uniq_str = "$(macromassid)-$(cluster)-$(process)"
    ile_job.set_log_file("%s%s-%s-%s.log" % (log_dir, tag, kwargs["iteration-level"], uniq_str))
    ile_job.set_stderr_file("%s%s-%s-%s.err" % (log_dir, tag, kwargs["iteration-level"], uniq_str))
    ile_job.set_stdout_file("%s%s-%s-%s.out" % (log_dir, tag, kwargs["iteration-level"], uniq_str))

    #if kwargs.has_key("output-file") and kwargs["output-file"] is not None:
    if "output-file" in kwargs and kwargs["output-file"] is not None:
        #
        # Need to modify the output file so it's unique
        #
        ofname = PurePath(kwargs["output-file"])
        ext = "".join(PurePath(ofname).suffixes[-2:])
        ofname= kwargs["output-file"][:-len(ext)]
        ile_job.add_file_opt("output-file", "%s-%s.%s" % (ofname, uniq_str, ext))
        del kwargs["output-file"]
        #if kwargs.has_key("save-samples") and kwargs["save-samples"] == True:
        if "save-samples" in kwargs and kwargs["save-samples"] == True:
            ile_job.add_opt("save-samples", '')
            del kwargs["save-samples"]

    del kwargs["iteration-level"]
    #
    # Add normal arguments
    # FIXME: Get valid options from a module
    #
    for opt, param in kwargs.items():
        if isinstance(param, list) or isinstance(param, tuple):
            # NOTE: Hack to get around multiple instances of the same option
            for p in param:
                ile_job.add_arg("--%s %s" % (opt, str(p)))
        elif param == True or param is None:
            ile_job.add_opt(opt, '')
        # Explcitly check for False to turn it off
        elif param == False:
            continue
        else:
            ile_job.add_opt(opt, str(param))

    #
    # Macro based options
    #
    ile_job.add_var_opt("mass1")
    ile_job.add_var_opt("mass2")
    for p in intr_prms:
        ile_job.add_var_opt(p)

    if getenv is not None and len(getenv) != 0:
        ile_job.add_condor_cmd('getenv', format_getenv(getenv))
    if environment_dict is not None and len(environment_dict) != 0:
        ile_job.add_condor_cmd('environment',
                               format_environment(environment_dict))
    ile_job.add_condor_cmd('request_memory', '4096')
    ile_job.add_condor_cmd('max_retries', '5')
    warnings.warn("Requesting hard-coded disk space for ILE job")
    ile_job.add_condor_cmd('request_disk', '1 GB')
    if 'gpu' in kwargs:
        ile_job.add_condor_cmd('request_GPUs', '1')
    if condor_commands is not None:
        for cmd, value in condor_commands.items():
            ile_job.add_condor_cmd(cmd, value)
    
    
    return ile_job, ile_sub_name

def write_result_coalescence_sub(tag='coalesce', exe=None, log_dir=None, output_dir="./", use_default_cache=True, getenv=None, environment_dict=None):
    """
    Write a submit file for launching jobs to coalesce ILE output
    """

    exe = exe or which("ligolw_sqlite")
    sql_job = pipeline.CondorDAGJob(universe="vanilla", executable=exe)

    sql_sub_name = tag + '.sub'
    sql_job.set_sub_file(sql_sub_name)

    #
    # Logging options
    #
    uniq_str = "$(cluster)-$(process)"
    sql_job.set_log_file("%s%s-%s.log" % (log_dir, tag, uniq_str))
    sql_job.set_stderr_file("%s%s-%s.err" % (log_dir, tag, uniq_str))
    sql_job.set_stdout_file("%s%s-%s.out" % (log_dir, tag, uniq_str))

    if use_default_cache:
        sql_job.add_opt("input-cache", "ILE_$(macromassid).cache")
    else:
        sql_job.add_arg("$(macrofiles)")
    #sql_job.add_arg("*$(macromassid)*.xml.gz")
    sql_job.add_opt("database", "ILE_$(macromassid).sqlite")
    #if os.environ.has_key("TMPDIR"):
        #tmpdir = os.environ["TMPDIR"]
    #else:
        #print >>sys.stderr, "WARNING, TMPDIR environment variable not set. Will default to /tmp/, but this could be dangerous."
        #tmpdir = "/tmp/"
    tmpdir = "/dev/shm/"
    sql_job.add_opt("tmp-space", tmpdir)
    sql_job.add_opt("verbose", '')

    if getenv is not None and len(getenv) != 0:
        sql_job.add_condor_cmd('getenv', format_getenv(getenv))
    if environment_dict is not None and len(environment_dict) != 0:
        sql_job.add_condor_cmd('environment',
                               format_environment(environment_dict))

    sql_job.add_condor_cmd('request_memory', '1024')
    warnings.warn("Requesting hard-coded disk space for SQL job")
    sql_job.add_condor_cmd('request_disk', '1 GB')

    return sql_job, sql_sub_name

def write_posterior_plot_sub(tag='plot_post', exe=None, log_dir=None, output_dir="./", getenv=None, environment_dict=None):
    """
    Write a submit file for launching jobs to coalesce ILE output
    """

    exe = exe or which("plot_like_contours")
    plot_job = pipeline.CondorDAGJob(universe="vanilla", executable=exe)

    plot_sub_name = tag + '.sub'
    plot_job.set_sub_file(plot_sub_name)

    #
    # Logging options
    #
    uniq_str = "$(cluster)-$(process)"
    plot_job.set_log_file("%s%s-%s.log" % (log_dir, tag, uniq_str))
    plot_job.set_stderr_file("%s%s-%s.err" % (log_dir, tag, uniq_str))
    plot_job.set_stdout_file("%s%s-%s.out" % (log_dir, tag, uniq_str))

    plot_job.add_opt("show-points", '')
    plot_job.add_opt("dimension1", "mchirp")
    plot_job.add_opt("dimension2", "eta")
    plot_job.add_opt("input-cache", "ILE_all.cache")
    plot_job.add_opt("log-evidence", '')

    if getenv is not None and len(getenv) != 0:
        plot_job.add_condor_cmd('getenv', format_getenv(getenv))
    if environment_dict is not None and len(environment_dict) != 0:
        plot_job.add_condor_cmd('environment',
                               format_environment(environment_dict))

    plot_job.add_condor_cmd('request_memory', '1024')
    warnings.warn("Requesting hard-coded disk space for plot job")
    plot_job.add_condor_cmd('request_disk', '1 GB')

    return plot_job, plot_sub_name

def write_tri_plot_sub(tag='plot_tri', injection_file=None, exe=None, log_dir=None, output_dir="./", getenv=None, environment_dict=None):
    """
    Write a submit file for launching jobs to coalesce ILE output
    """

    exe = exe or which("make_triplot")
    plot_job = pipeline.CondorDAGJob(universe="vanilla", executable=exe)

    plot_sub_name = tag + '.sub'
    plot_job.set_sub_file(plot_sub_name)

    #
    # Logging options
    #
    uniq_str = "$(cluster)-$(process)"
    plot_job.set_log_file("%s%s-%s.log" % (log_dir, tag, uniq_str))
    plot_job.set_stderr_file("%s%s-%s.err" % (log_dir, tag, uniq_str))
    plot_job.set_stdout_file("%s%s-%s.out" % (log_dir, tag, uniq_str))

    plot_job.add_opt("output", "ILE_triplot_$(macromassid).png")
    if injection_file is not None:
        plot_job.add_opt("injection", injection_file)
    plot_job.add_arg("ILE_$(macromassid).sqlite")

    if getenv is not None and len(getenv) != 0:
        plot_job.add_condor_cmd('getenv', format_getenv(getenv))
    if environment_dict is not None and len(environment_dict) != 0:
        plot_job.add_condor_cmd('environment',
                               format_environment(environment_dict))

    #plot_job.add_condor_cmd('request_memory', '2048')
    warnings.warn("Requesting hard-coded disk space for plot job")
    plot_job.add_condor_cmd('request_disk', '1 GB')

    return plot_job, plot_sub_name

def write_1dpos_plot_sub(tag='1d_post_plot', exe=None, log_dir=None, output_dir="./", getenv=None, environment_dict=None):
    """
    Write a submit file for plotting 1d posterior cumulants.
    """

    exe = exe or which("postprocess_1d_cumulative")
    plot_job = pipeline.CondorDAGJob(universe="vanilla", executable=exe)

    plot_sub_name = tag + '.sub'
    plot_job.set_sub_file(plot_sub_name)

    #
    # Logging options
    #
    uniq_str = "$(cluster)-$(process)"
    plot_job.set_log_file("%s%s-%s.log" % (log_dir, tag, uniq_str))
    plot_job.set_stderr_file("%s%s-%s.err" % (log_dir, tag, uniq_str))
    plot_job.set_stdout_file("%s%s-%s.out" % (log_dir, tag, uniq_str))

    plot_job.add_opt("save-sampler-file", "ILE_$(macromassid).sqlite")
    plot_job.add_opt("disable-triplot", '')
    plot_job.add_opt("disable-1d-density", '')

    if getenv is not None and len(getenv) != 0:
        plot_job.add_condor_cmd('getenv', format_getenv(getenv))
    if environment_dict is not None and len(environment_dict) != 0:
        plot_job.add_condor_cmd('environment',
                               format_environment(environment_dict))

    plot_job.add_condor_cmd('request_memory', '2048')
    warnings.warn("Requesting hard-coded disk space for plot job")
    plot_job.add_condor_cmd('request_disk', '1 GB')

    return plot_job, plot_sub_name

def write_bayes_pe_postproc_sub(tag='bayespe_post_plot', exe=None, log_dir=None, web_dir="./", inj_xml=None, getenv=None, environment_dict=None):
    """
    Write a submit file for postprocessing output and pushing it through cbcBayesPostProc.py
    """

    exe = exe or which("cbcBayesPostProc.py")
    plot_job = pipeline.CondorDAGJob(universe="vanilla", executable=exe)

    plot_sub_name = tag + '.sub'
    plot_job.set_sub_file(plot_sub_name)

    #
    # Logging options
    #
    uniq_str = "$(cluster)-$(process)"
    plot_job.set_log_file("%s%s-%s.log" % (log_dir, tag, uniq_str))
    plot_job.set_stderr_file("%s%s-%s.err" % (log_dir, tag, uniq_str))
    plot_job.set_stdout_file("%s%s-%s.out" % (log_dir, tag, uniq_str))

    #
    # Injection options
    #
    plot_job.add_opt("outpath", web_dir)
    if inj_xml:
        plot_job.add_opt("inj", inj_xml)
        # FIXME: Since we put individual sim entries into their own XML, this is
        # always zero. We might need to tweak this if we use a bigger one
        plot_job.add_opt("eventnum", 0)

    # Calculate evidence (just to compare)
    plot_job.add_opt("dievidence", '')

    plot_job.add_opt("header", "header.txt")
    plot_job.add_opt("data", "tmp")

    if getenv is not None and len(getenv) != 0:
        plot_job.add_condor_cmd('getenv', format_getenv(getenv))
    if environment_dict is not None and len(environment_dict) != 0:
        plot_job.add_condor_cmd('environment',
                               format_environment(environment_dict))

    plot_job.add_condor_cmd('request_memory', '1024')
    warnings.warn("Requesting hard-coded disk space for plot job")
    plot_job.add_condor_cmd('request_disk', '1 GB')

    return plot_job, plot_sub_name
