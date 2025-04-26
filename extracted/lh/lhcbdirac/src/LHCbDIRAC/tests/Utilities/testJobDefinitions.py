###############################################################################
# (c) Copyright 2019 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
"""Collection of user jobs for testing purposes"""
import os
import time
import errno

from DIRAC import rootPath
from DIRAC.DataManagementSystem.Utilities.DMSHelpers import DMSHelpers
from DIRAC.tests.Utilities.testJobDefinitions import baseToAllJobs, endOfAllJobs, find_all
from DIRAC.Core.Utilities.Proxy import executeWithUserProxy
from LHCbDIRAC.Interfaces.API.LHCbJob import LHCbJob
from LHCbDIRAC.Interfaces.API.DiracLHCb import DiracLHCb

# parameters

jobClass = LHCbJob
diracClass = DiracLHCb

try:
    tier1s = DMSHelpers().getTiers(tier=(0, 1))
except AttributeError:
    tier1s = [
        "LCG.CERN.cern",
        "LCG.CNAF.it",
        "LCG.GRIDKA.de",
        "LCG.IN2P3.fr",
        "LCG.PIC.es",
        "LCG.RAL.uk",
        "LCG.NCBJ.pl",
        "LCG.SARA.nl",
        "LCG.Beijing.cn",
    ]

# List of jobs
wdir = os.getcwd()


@executeWithUserProxy
def helloWorldTestT2s():
    job = baseToAllJobs("helloWorldTestT2s", jobClass)
    try:
        job.setInputSandbox([find_all("exe-script.py", rootPath, "DIRAC/tests/Workflow")[0]])
    except IndexError:
        try:
            job.setInputSandbox([find_all("exe-script.py", ".", "DIRAC/tests/Workflow")[0]])
        except IndexError:  # we are in Jenkins
            job.setInputSandbox([find_all("exe-script.py", os.environ["WORKSPACE"], "DIRAC/tests/Workflow")[0]])

    job.setExecutable("exe-script.py", "", "helloWorld.log")
    job.setBannedSites(tier1s)
    return endOfAllJobs(job)


@executeWithUserProxy
def helloWorldTestCERN():
    job = baseToAllJobs("helloWorld-test-CERN", jobClass)
    try:
        job.setInputSandbox([find_all("exe-script.py", rootPath, "DIRAC/tests/Workflow")[0]])
    except IndexError:
        try:
            job.setInputSandbox([find_all("exe-script.py", ".", "DIRAC/tests/Workflow")[0]])
        except IndexError:  # we are in Jenkins
            job.setInputSandbox([find_all("exe-script.py", os.environ["WORKSPACE"], "DIRAC/tests/Workflow")[0]])
    job.setExecutable("exe-script.py", "", "helloWorld.log")
    job.setDestination("LCG.CERN.cern")
    return endOfAllJobs(job)


@executeWithUserProxy
def helloWorldTestIN2P3():
    job = baseToAllJobs("helloWorld-test-IN2P3", jobClass)
    try:
        job.setInputSandbox([find_all("exe-script.py", rootPath, "DIRAC/tests/Workflow")[0]])
    except IndexError:
        try:
            job.setInputSandbox([find_all("exe-script.py", ".", "DIRAC/tests/Workflow")[0]])
        except IndexError:  # we are in Jenkins
            job.setInputSandbox([find_all("exe-script.py", os.environ["WORKSPACE"], "DIRAC/tests/Workflow")[0]])
    job.setExecutable("exe-script.py", "", "helloWorld.log")
    job.setDestination("LCG.IN2P3.fr")
    return endOfAllJobs(job)


@executeWithUserProxy
def helloWorldTestGRIDKA():
    job = baseToAllJobs("helloWorld-test-GRIDKA", jobClass)
    try:
        job.setInputSandbox([find_all("exe-script.py", rootPath, "DIRAC/tests/Workflow")[0]])
    except IndexError:
        try:
            job.setInputSandbox([find_all("exe-script.py", ".", "DIRAC/tests/Workflow")[0]])
        except IndexError:  # we are in Jenkins
            job.setInputSandbox([find_all("exe-script.py", os.environ["WORKSPACE"], "DIRAC/tests/Workflow")[0]])
    job.setExecutable("exe-script.py", "", "helloWorld.log")
    job.setDestination("LCG.GRIDKA.de")
    return endOfAllJobs(job)


@executeWithUserProxy
def helloWorldTestARC():
    job = baseToAllJobs("helloWorld-test-ARC", jobClass)
    try:
        job.setInputSandbox([find_all("exe-script.py", rootPath, "DIRAC/tests/Workflow")[0]])
    except IndexError:
        try:
            job.setInputSandbox([find_all("exe-script.py", ".", "DIRAC/tests/Workflow")[0]])
        except IndexError:  # we are in Jenkins
            job.setInputSandbox([find_all("exe-script.py", os.environ["WORKSPACE"], "DIRAC/tests/Workflow")[0]])
    job.setExecutable("exe-script.py", "", "helloWorld.log")
    job.setDestination(["LCG.RAL.uk"])
    return endOfAllJobs(job)


@executeWithUserProxy
def helloWorldTestSSHCondor():
    job = baseToAllJobs("helloWorld-test-SSHCondor", jobClass)
    try:
        job.setInputSandbox([find_all("exe-script.py", rootPath, "DIRAC/tests/Workflow")[0]])
    except IndexError:
        try:
            job.setInputSandbox([find_all("exe-script.py", ".", "DIRAC/tests/Workflow")[0]])
        except IndexError:  # we are in Jenkins
            job.setInputSandbox([find_all("exe-script.py", os.environ["WORKSPACE"], "DIRAC/tests/Workflow")[0]])
    job.setExecutable("exe-script.py", "", "helloWorld.log")
    job.setDestination(["DIRAC.Sibir.ru"])
    return endOfAllJobs(job)


@executeWithUserProxy
def helloWorldTestARM():
    job = baseToAllJobs("helloWorld-test-ARM", jobClass)
    try:
        job.setInputSandbox([find_all("exe-script.py", rootPath, "DIRAC/tests/Workflow")[0]])
    except IndexError:
        try:
            job.setInputSandbox([find_all("exe-script.py", ".", "DIRAC/tests/Workflow")[0]])
        except IndexError:  # we are in Jenkins
            job.setInputSandbox([find_all("exe-script.py", os.environ["WORKSPACE"], "DIRAC/tests/Workflow")[0]])
    job.setExecutable("exe-script.py", "", "helloWorld.log")
    job.setDestination(["DIRAC.ARM.ch"])
    return endOfAllJobs(job)


@executeWithUserProxy
def jobWithOutput():
    timenow = time.strftime("%s")
    with open(os.path.join(wdir, timenow + "testFileUpload.txt"), "w") as f:
        f.write(timenow)
    try:
        inp1 = [find_all(timenow + "testFileUpload.txt", "LHCbDIRAC/tests/Workflow")[0]]
        inp2 = [find_all("exe-script.py", rootPath, "DIRAC/tests/Workflow")[0]]
    except IndexError:
        try:
            inp1 = [find_all(timenow + "testFileUpload.txt", "LHCbDIRAC/tests/Workflow")[0]]
            inp2 = [find_all("exe-script.py", ".", "DIRAC/tests/Workflow")[0]]
        except IndexError:  # we are in Jenkins
            inp1 = [find_all(timenow + "testFileUpload.txt", "LHCbDIRAC/tests/Workflow")[0]]
            inp2 = [find_all("exe-script.py", os.environ["WORKSPACE"], "DIRAC/tests/Workflow")[0]]

    job = baseToAllJobs("jobWithOutput", jobClass)
    job.setInputSandbox(inp1 + inp2)
    job.setExecutable("exe-script.py", "", "helloWorld.log")
    job.setOutputData([timenow + "testFileUpload.txt"])
    res = endOfAllJobs(job)
    try:
        os.remove(os.path.join(wdir, timenow + "testFileUpload.txt"))
    except OSError as e:
        return e.errno == errno.ENOENT
    return res


@executeWithUserProxy
def jobWithOutputAndPrepend():
    timenow = time.strftime("%s")
    with open(os.path.join(wdir, timenow + "testFileUploadNewPath.txt"), "w") as f:
        f.write(timenow)
    job = baseToAllJobs("jobWithOutputAndPrepend", jobClass)

    try:
        inp1 = [find_all(timenow + "testFileUploadNewPath.txt", "LHCbDIRAC/tests/Workflow")[0]]
        inp2 = [find_all("exe-script.py", rootPath, "DIRAC/tests/Workflow")[0]]
    except IndexError:
        try:
            inp1 = [find_all(timenow + "testFileUploadNewPath.txt", "LHCbDIRAC/tests/Workflow")[0]]
            inp2 = [find_all("exe-script.py", ".", "DIRAC/tests/Workflow")[0]]
        except IndexError:  # we are in Jenkins
            inp1 = [find_all(timenow + "testFileUploadNewPath.txt", "LHCbDIRAC/tests/Workflow")[0]]
            inp2 = [find_all("exe-script.py", os.environ["WORKSPACE"], "DIRAC/tests/Workflow")[0]]

    job.setInputSandbox(inp1 + inp2)
    job.setExecutable("exe-script.py", "", "helloWorld.log")
    job.setOutputData([timenow + "testFileUploadNewPath.txt"], filePrepend="testFilePrepend")
    res = endOfAllJobs(job)
    try:
        os.remove(os.path.join(wdir, timenow + "testFileUploadNewPath.txt"))
    except OSError as e:
        return e.errno == errno.ENOENT
    return res


@executeWithUserProxy
def jobWithOutputAndPrependWithUnderscore():
    timenow = time.strftime("%s")
    with open(os.path.join(wdir, timenow + "testFileUpload_NewPath.txt"), "w") as f:
        f.write(timenow)
    job = baseToAllJobs("jobWithOutputAndPrependWithUnderscore", jobClass)
    try:
        inp1 = [find_all(timenow + "testFileUpload_NewPath.txt", "LHCbDIRAC/tests/Workflow")[0]]
        inp2 = [find_all("exe-script.py", rootPath, "DIRAC/tests/Workflow")[0]]
    except IndexError:
        try:
            inp1 = [find_all(timenow + "testFileUpload_NewPath.txt", "LHCbDIRAC/tests/Workflow")[0]]
            inp2 = [find_all("exe-script.py", ".", "DIRAC/tests/Workflow")[0]]
        except IndexError:  # we are in Jenkins
            inp1 = [find_all(timenow + "testFileUpload_NewPath.txt", "LHCbDIRAC/tests/Workflow")[0]]
            inp2 = [find_all("exe-script.py", os.environ["WORKSPACE"], "DIRAC/tests/Workflow")[0]]

    job.setInputSandbox(inp1 + inp2)
    job.setExecutable("exe-script.py", "", "helloWorld.log")
    res = job.setOutputData([timenow + "testFileUpload_NewPath.txt"], filePrepend="testFilePrepend")
    if not res["OK"]:
        return 0
    res = endOfAllJobs(job)
    try:
        os.remove(os.path.join(wdir, timenow + "testFileUpload_NewPath.txt"))
    except OSError as e:
        return e.errno == errno.ENOENT
    return res


@executeWithUserProxy
def jobWithOutputAndReplication():
    timenow = time.strftime("%s")
    with open(os.path.join(wdir, timenow + "testFileReplication.txt"), "w") as f:
        f.write(timenow)
    job = baseToAllJobs("jobWithOutputAndReplication", jobClass)
    try:
        inp1 = [find_all(timenow + "testFileReplication.txt", "LHCbDIRAC/tests/Workflow")[0]]
        inp2 = [find_all("exe-script.py", rootPath, "DIRAC/tests/Workflow")[0]]
    except IndexError:
        try:
            inp1 = [find_all(timenow + "testFileReplication.txt", "LHCbDIRAC/tests/Workflow")[0]]
            inp2 = [find_all("exe-script.py", ".", "DIRAC/tests/Workflow")[0]]
        except IndexError:  # we are in Jenkins
            inp1 = [find_all(timenow + "testFileReplication.txt", "LHCbDIRAC/tests/Workflow")[0]]
            inp2 = [find_all("exe-script.py", os.environ["WORKSPACE"], "DIRAC/tests/Workflow")[0]]
    job.setInputSandbox(inp1 + inp2)
    job.setExecutable("exe-script.py", "", "helloWorld.log")
    job.setOutputData([timenow + "testFileReplication.txt"], replicate="True")
    res = endOfAllJobs(job)
    try:
        os.remove(os.path.join(wdir, timenow + "testFileReplication.txt"))
    except OSError as e:
        return e.errno == errno.ENOENT
    return res


@executeWithUserProxy
def jobWithSingleInputData():
    job = baseToAllJobs("jobWithSingleInputData-shouldGoToCERN", jobClass)
    try:
        job.setInputSandbox(
            [find_all("exe-script-with-input-single-location.py", rootPath, "LHCbDIRAC/tests/Workflow")[0]]
        )
    except IndexError:
        job.setInputSandbox([find_all("exe-script-with-input-single-location.py", ".", "LHCbDIRAC/tests/Workflow")[0]])
    job.setExecutable("exe-script-with-input-single-location.py", "", "exeWithInput.log")
    # this file should be at CERN-USER only
    job.setInputData("/lhcb/user/f/fstagni/test/testInputFileSingleLocation.txt")
    job.setInputDataPolicy("download")
    res = endOfAllJobs(job)
    return res


@executeWithUserProxy
def jobWithSingleInputDataCERN():
    job = baseToAllJobs("jobWithSingleInputDataCERN-shouldSucceed", jobClass)
    try:
        job.setInputSandbox(
            [find_all("exe-script-with-input-single-location.py", rootPath, "LHCbDIRAC/tests/Workflow")[0]]
        )
    except IndexError:
        job.setInputSandbox([find_all("exe-script-with-input-single-location.py", ".", "LHCbDIRAC/tests/Workflow")[0]])
    job.setExecutable("exe-script-with-input-single-location.py", "", "exeWithInput.log")
    # this file should be at CERN-USER only
    job.setInputData("/lhcb/user/f/fstagni/test/testInputFileSingleLocation.txt")
    job.setInputDataPolicy("download")
    job.setDestination(["LCG.CERN.cern"])
    res = endOfAllJobs(job)
    return res


@executeWithUserProxy
def jobWithSingleInputDataRAL():
    job = baseToAllJobs("jobWithSingleInputDataRAL-shouldFailOptimizers", jobClass)
    try:
        job.setInputSandbox(
            [find_all("exe-script-with-input-single-location.py", rootPath, "LHCbDIRAC/tests/Workflow")[0]]
        )
    except IndexError:
        job.setInputSandbox([find_all("exe-script-with-input-single-location.py", ".", "LHCbDIRAC/tests/Workflow")[0]])
    job.setExecutable("exe-script-with-input-single-location.py", "", "exeWithInput.log")
    # this file should be at CERN-USER only
    job.setInputData("/lhcb/user/f/fstagni/test/testInputFileSingleLocation.txt")
    job.setInputDataPolicy("protocol")
    job.setDestination(["LCG.RAL.uk"])
    res = endOfAllJobs(job)
    return res


@executeWithUserProxy
def jobWithSingleInputDataIN2P3():
    job = baseToAllJobs("jobWithSingleInputDataIN2P3-shouldFailOptimizers", jobClass)
    try:
        job.setInputSandbox(
            [find_all("exe-script-with-input-single-location.py", rootPath, "LHCbDIRAC/tests/Workflow")[0]]
        )
    except IndexError:
        job.setInputSandbox([find_all("exe-script-with-input-single-location.py", ".", "LHCbDIRAC/tests/Workflow")[0]])
    job.setExecutable("exe-script-with-input-single-location.py", "", "exeWithInput.log")
    # this file should be at CERN-USER only
    job.setInputData("/lhcb/user/f/fstagni/test/testInputFileSingleLocation.txt")
    job.setInputDataPolicy("protocol")
    job.setDestination(["LCG.IN2P3.fr"])
    res = endOfAllJobs(job)
    return res


@executeWithUserProxy
def jobWithSingleInputDataNCBJ():
    job = baseToAllJobs("jobWithSingleInputDataNCBJ-shouldFailOptimizers", jobClass)
    try:
        job.setInputSandbox(
            [find_all("exe-script-with-input-single-location.py", rootPath, "LHCbDIRAC/tests/Workflow")[0]]
        )
    except IndexError:
        job.setInputSandbox([find_all("exe-script-with-input-single-location.py", ".", "LHCbDIRAC/tests/Workflow")[0]])
    job.setExecutable("exe-script-with-input-single-location.py", "", "exeWithInput.log")
    # this file should be at CERN-USER only
    job.setInputData("/lhcb/user/f/fstagni/test/testInputFileSingleLocation.txt")
    job.setInputDataPolicy("protocol")
    job.setDestination(["LCG.NCBJ.pl"])
    res = endOfAllJobs(job)
    return res


@executeWithUserProxy
def jobWithSingleInputDataSARA():
    job = baseToAllJobs("jobWithSingleInputDataSARA-shouldFailOptimizers", jobClass)
    try:
        job.setInputSandbox(
            [find_all("exe-script-with-input-single-location.py", rootPath, "LHCbDIRAC/tests/Workflow")[0]]
        )
    except IndexError:
        job.setInputSandbox([find_all("exe-script-with-input-single-location.py", ".", "LHCbDIRAC/tests/Workflow")[0]])
    job.setExecutable("exe-script-with-input-single-location.py", "", "exeWithInput.log")
    # this file should be at CERN-USER only
    job.setInputData("/lhcb/user/f/fstagni/test/testInputFileSingleLocation.txt")
    job.setInputDataPolicy("protocol")
    job.setDestination(["LCG.SARA.nl"])
    res = endOfAllJobs(job)
    return res


@executeWithUserProxy
def jobWithSingleInputDataPIC():
    job = baseToAllJobs("jobWithSingleInputDataPIC-shouldFailOptimizers", jobClass)
    try:
        job.setInputSandbox(
            [find_all("exe-script-with-input-single-location.py", rootPath, "LHCbDIRAC/tests/Workflow")[0]]
        )
    except IndexError:
        job.setInputSandbox([find_all("exe-script-with-input-single-location.py", ".", "LHCbDIRAC/tests/Workflow")[0]])
    job.setExecutable("exe-script-with-input-single-location.py", "", "exeWithInput.log")
    # this file should be at CERN-USER only
    job.setInputData("/lhcb/user/f/fstagni/test/testInputFileSingleLocation.txt")
    job.setInputDataPolicy("protocol")
    job.setDestination(["LCG.PIC.es"])
    res = endOfAllJobs(job)
    return res


@executeWithUserProxy
def jobWithInputDataAndAncestor():
    job = baseToAllJobs("jobWithInputDataAndAncestor", jobClass)
    try:
        job.setInputSandbox(
            [find_all("exe-script-with-input-and-ancestor.py", rootPath, "LHCbDIRAC/tests/Workflow")[0]]
        )
    except IndexError:
        job.setInputSandbox([find_all("exe-script-with-input-and-ancestor.py", ".", "LHCbDIRAC/tests/Workflow")[0]])
    job.setExecutable("exe-script-with-input-and-ancestor.py", "", "exeWithInput.log")
    # WARNING: Collision10!!
    job.setInputData("/lhcb/data/2010/SDST/00008375/0005/00008375_00053941_1.sdst")  # this file should be at SARA-RDST
    # the ancestor should be /lhcb/data/2010/RAW/FULL/LHCb/COLLISION10/81616/081616_0000000213.raw (CERN and SARA)
    job.setAncestorDepth(1)  # pylint: disable=no-member
    job.setInputDataPolicy("download")
    res = endOfAllJobs(job)
    return res


def parametricJobInputDataLHCb():
    """Creates a parametric job with 3 subjobs which are simple hello world jobs, but with input data"""

    J = baseToAllJobs("parametricJobInput")
    try:
        J.setInputSandbox([find_all("exe-script.py", rootPath, "DIRAC/tests/Workflow")[0]])
    except IndexError:
        try:
            J.setInputSandbox([find_all("exe-script.py", ".", "DIRAC/tests/Workflow")[0]])
        except IndexError:  # we are in Jenkins
            J.setInputSandbox([find_all("exe-script.py", os.environ["WORKSPACE"], "DIRAC/tests/Workflow")[0]])
    J.setParameterSequence("args", ["one", "two", "three"])
    J.setParameterSequence("iargs", [1, 2, 3])
    J.setParameterSequence(
        "InputData",
        [
            "/lhcb/user/f/fstagni/2022_12/2138/2138252/1671456075testFileUpload.txt",
            "/lhcb/user/f/fstagni/2022_12/2138/2138505/1671629479testFileUpload.txt",
            "/lhcb/user/f/fstagni/2023_01/2138/2138533/1673343116testFileUpload.txt",
        ],
    )
    J.setParameterSequence("runNumber", [123, 456, 789])
    J.setInputDataPolicy("download")
    J.setExecutable("exe-script.py", arguments=": testing %(args)s %(iargs)s", logFile="helloWorld_%n.log")
    return endOfAllJobs(J)
