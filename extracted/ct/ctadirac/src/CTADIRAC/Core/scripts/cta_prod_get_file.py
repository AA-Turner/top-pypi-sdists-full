#!/usr/bin/env python

__RCSID__ = "$Id$"

# generic imports
import os
import signal
from multiprocessing import Pool

# DIRAC imports
import DIRAC
from DIRAC import gLogger
from DIRAC.Core.Base.Script import Script
from DIRAC.DataManagementSystem.Client.DataManager import DataManager

from CTADIRAC.Core.Utilities.tool_box import read_inputs_from_file

Script.setUsageMessage(
    """
Download a list of files or a single file with N parallel process
Usage:
   cta-prod-get-file [options] <lfn> --NbProcess=8
   cta-prod-get-file [options] <ascii file with a list of lfns> --NbProcess=8
"""
)

config = dict(
    n_processes=8,
    skip_existing=False,
)


def set_n_processes(n):
    config["n_processes"] = int(n)


def set_skip(_):
    config["skip_existing"] = True


Script.registerSwitch(
    "n:", "NbProcess=", "number of parallel download processes", set_n_processes
)
Script.registerSwitch("k", "skip-existing", "skip files already downloaded", set_skip)
switches, args = Script.parseCommandLine(ignoreErrors=True)

DIRAC.initialize()

TEMPDIR = ".incomplete"

gLogger.setLevel("NOTICE")


def sigint_handler(signum, frame):
    """
    Raise KeyboardInterrupt on SIGINT (CTRL + C)
    This should be the default, but apparently Dirac changes it.
    """
    raise KeyboardInterrupt()


def getfile(lfn):
    try:
        voName = lfn.split("/")[1]
        if voName not in ["ctao", "vo.cta.in2p3.fr"]:
            message = f"Wrong lfn: path must start with vo name (ctao or vo.cta.in2p3.fr):\n{lfn}"
            gLogger.error(message)
            return

        name = os.path.basename(lfn)
        if config["skip_existing"] and os.path.isfile(name):
            gLogger.notice("Skipping already downloaded file", lfn)
            return

        dm = DataManager(vo=voName)
        gLogger.notice("Start downloading file", lfn)
        res = dm.getFile(lfn, destinationDir=TEMPDIR)

        if not res["OK"]:
            message = res["Message"]
            gLogger.error(f"Error downloading file {lfn}:\n{message}")
            return
        elif res["Value"]["Failed"]:
            message = res["Value"]["Failed"][lfn]
            gLogger.error(f"Error downloading file {lfn}:\n{message}")
            return

        gLogger.info(f"Successfully downloaded file {lfn}")
        os.rename(os.path.join(".incomplete", name), name)

    except Exception as e:
        gLogger.error(f"Unexpected error while downloading {lfn}: {e}")
        # Don't raise; just log so worker doesn't crash


@Script()
def main():
    if len(args) == 1:
        infile = args[0]
    else:
        Script.showHelp()

    # put files currently downloading in a subdirectory
    # to know which files have already finished
    if not os.path.exists(TEMPDIR):
        os.makedirs(TEMPDIR)

    if os.path.isfile(infile):
        infileList = read_inputs_from_file(infile)
    else:
        infileList = [infile]
    # see https://stackoverflow.com/a/35134329/3838691
    # ignore sigint before creating the pool,
    # so child processes inherit the setting, we will terminate them
    # if the master process catches sigint
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    p = Pool(config["n_processes"])
    # add the original handler back
    signal.signal(signal.SIGINT, sigint_handler)

    try:
        future = p.map_async(getfile, infileList)

        while not future.ready():
            future.wait(5)
    except (SystemExit, KeyboardInterrupt):
        gLogger.fatal("Received SIGINT, waiting for subprocesses to terminate")
        p.close()
        p.terminate()
    finally:
        p.close()
        p.join()
        if len(os.listdir(TEMPDIR)) == 0:
            os.rmdir(TEMPDIR)


if __name__ == "__main__":
    main()
