###############################################################################
# (c) Copyright 2022 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
"""The HistogramMergingAgent finds MC transformations that are finished with
testing and merges their HIST files for SimDQ monitoring.

An overview of the procedure:
1. take all MCSimulation/MCFastSimulation/MCReconstruction transformations that
have finished testing but are not yet archived,
2. deduce the output LFNs for the merged histograms from each transformation,
3. if the output LFN does not already exist then merge the files,
4. upload and register the new merged files,
5. generate and commit new metadata to the SimProdDB repository.
"""
import hashlib
import re
import shlex
import subprocess
import tempfile
from copy import copy
from datetime import datetime
from functools import lru_cache
from pathlib import Path

import DIRAC
import git
import yaml
from DIRAC import S_OK
from DIRAC.ConfigurationSystem.Client.ConfigurationData import gConfigurationData
from DIRAC.ConfigurationSystem.Client.Helpers.Operations import Operations
from DIRAC.Core.Base.AgentModule import AgentModule
from DIRAC.Core.Utilities.File import generateGuid
from DIRAC.Core.Utilities.ReturnValues import returnValueOrRaise
from DIRAC.Core.Utilities.TimeUtilities import timeThis
from DIRAC.DataManagementSystem.Client.DataManager import DataManager

from LHCbDIRAC.BookkeepingSystem.Client.BookkeepingClient import BookkeepingClient
from LHCbDIRAC.Core.Utilities.BookkeepingJobInfo import BookkeepingJobInfo
from LHCbDIRAC.Core.Utilities.XMLTreeParser import XMLNode, XMLTreeParser
from LHCbDIRAC.ProductionManagementSystem.Client.ProductionRequestClient import ProductionRequestClient
from LHCbDIRAC.TransformationSystem.Client.TransformationClient import TransformationClient

AGENT_NAME = "ProductionManagement/HistogramMergingAgent"

gStandAlone = False  # Do not perform queries to the Bookkeeping/Transformation/ProductionManagement Systems
gLocalWorkDir = False  # Use the CWD for writing files, in case am_getWorkDirectory resolves to a read-only location
gDoRealMerging = True  # Run the `hadd` command to produce actual ROOT files
gDoRealUpdate = True  # OK to upload files, write to Bookkeeping and commit & push to the git repo
gUseGitRepo = True  # OK to check-out and manipulate the SimDQ metadata git repository

REQ_KEYS = {
    # Extra information that Monet can display to the shifter
    # See LHCbDIRAC.ProductionManagementSystem.DB.ProductionRequestDB for full list
    "RequestID",
    "RequestName",
    "RequestWG",
    "SimCondition",
    "SimCondDetail",
    "ProPath",
    "Extra",
    "RetentionRate",
    "FastSimulationType",
}

TFM_KEYS = {
    # Extra information that Monet can display to the shifter
    # See LHCbDIRAC.TransformationSystem.DB.TransformationDB and DIRAC.TransformationSystem.DB.TransformationDB for full list
    "TransformationID",
    "Type",
}


class HistogramMergingAgent(AgentModule):
    """HistogramMergingAgent"""

    def __init__(self, *args, **kwargs):
        """c'tor."""
        super().__init__(*args, **kwargs)
        # Clients
        self.bk_client = None
        self.rp_client = None
        self.tf_client = None
        self.dm_client = None
        self.xml_parser = None
        # Local directories
        self.merge_dir = None
        self.simdq_dir = None
        # Remote targets
        self.simdq_repo = None
        self.hist_se = None
        # Configuration
        self.git_author = git.Actor(
            self.am_getOption("GitAuthorName", "LHCbDIRAC"),
            self.am_getOption("GitAuthorEmail", "lhcb-production-manager@cern.ch"),
        )
        self.ssh_key = self.am_getOption("GitSSHKeyFile", "")
        self.n_cpus = 1  # Passed to `hadd -j`
        if gDoRealUpdate:
            self.simdq_url = "ssh://git@gitlab.cern.ch:7999/lhcb-simulation/simdqdata.git"
        else:
            self.simdq_url = "https://gitlab.cern.ch/lhcb-simulation/simdqdata.git"
        self.simdq_url = self.am_getOption("SimDQRepoURL", self.simdq_url)
        self.simdq_branch = self.am_getOption("SimDQRepoBranch", "main")
        self.lbconda_env_name = self.am_getOption("HistMergeCondaEnv", "default")
        self.allowed_types = self.am_getOption(
            "ProductionTypes", ["MCSimulation", "MCFastSimulation", "MCReconstruction"]
        )
        self.allowed_statuses = self.am_getOption("ProductionStatuses", ["Active", "Idle", "Completed"])
        self.lbconda_env_version = None

    def initialize(self):
        """Set up the clients and merging directory."""
        # Local directories
        if gLocalWorkDir:
            # Useful if am_getWorkDirectory resolves to a read-only file system (e.g. CVMFS)
            work_dir = "."
        else:
            work_dir = self.am_getWorkDirectory()
        self.merge_dir = Path(work_dir) / "MergeHistograms"
        self.simdq_dir = Path(work_dir) / "SimProdDB"
        # Make sure that the directories exist
        for path in [self.merge_dir, self.simdq_dir]:
            path.mkdir(parents=True, exist_ok=True)
        # Remote targets
        self.hist_se = Operations().getValue("Productions/HistogramSE", "CERN-HIST-EOS")

        return S_OK()

    def beginExecution(self):
        """Get latest version of conda env"""
        self.bk_client = BookkeepingClient()
        self.rp_client = ProductionRequestClient()
        self.tf_client = TransformationClient()
        self.xml_parser = XMLTreeParser()
        self.dm_client = DataManager()

        self.lbconda_env_version = self._latest_lbconda_env_version

        return S_OK()

    def execute(self):
        """Main method"""
        # Don't use the server certificate otherwise the DFC wont let us write
        gConfigurationData.setOptionInCFG("/DIRAC/Security/UseServerCertificate", "false")

        transformations = self._fetch_transformations()
        if not transformations:
            # Nothing to do!
            return S_OK()

        if gDoRealUpdate and not Path(self.ssh_key).is_file():
            raise RuntimeError(f"GitSSHKeyFile={self.ssh_key} is not a valid file path")
        self.simdq_repo = self._checkout_metadata()

        request_ids = list({int(t["TransformationFamily"]) for t in transformations})
        requests = self._query_requests(request_ids)

        # Perform the merging and write the metadata files
        for transform in transformations:
            request_id = int(transform["TransformationFamily"])
            request = requests[request_id]
            # Loop over step-filetype combinations
            new_files = []
            for key in transform["HistogramMerging"]:
                new_files += [self._handle_transformation(transform, request, key)]

            # Commit meteadata files to the SimDQ repo
            if gUseGitRepo:
                commit_message = f"add metadata for {len(new_files)} new productions"
                self._commit_and_push_metadata(new_files, commit_message)

        return S_OK()

    # Properties ###############################################################

    @property
    def _latest_lbconda_env_version(self) -> str:
        cmd = ["lb-conda", "--list", self.lbconda_env_name]
        ret = subprocess.run(cmd, check=True, capture_output=True, text=True)
        latest_version = ret.stdout.strip().split("\n")[-1]
        return latest_version

    @property
    @lru_cache
    def _available_hist_filetypes(self) -> list[str]:
        if gStandAlone:
            return [f"{app.upper()}HIST" for app in ["Gauss", "Boole", "Brunel", "Moore", "DaVinci"]]
        all_filetypes = returnValueOrRaise(self.bk_client.getAvailableFileTypes())["Records"]
        hist_filetypes = [filetype for filetype, _ in all_filetypes if filetype.endswith("HIST")]
        return hist_filetypes

    # Main method for obtaining transformations to process #####################

    def _fetch_transformations(self) -> list[dict]:
        """Get recent unprocessed transformations that have histogram files to merge"""
        # Get recent transformations and their additional parameters
        recent_transformations = self._query_recent_transformations()
        for transform in recent_transformations:
            workflow = self._parse_workflow_xml(transform.pop("Body"))
            transform.update({"Parameters": self._get_transformation_parameters(workflow)})
            transform.update({"Steps": self._get_transformation_steps(workflow)})

        # Get histogram file LFNs and corresponding PFNs
        all_transform_ids = [int(t["TransformationID"]) for t in recent_transformations]
        all_lfns = self._query_input_lfns(all_transform_ids)
        if len(all_lfns) == 0:
            return []
        all_pfns = self._query_pfns(all_lfns)
        input_lfn_dict = self._group_lfns_by_prod_and_type(all_lfns)
        input_pfn_dict = {
            transform_id: {filetype: [all_pfns[lfn] for lfn in filetype_dict[filetype]] for filetype in filetype_dict}
            for transform_id, filetype_dict in input_lfn_dict.items()
        }

        # Deduce the corresponding output LFNs for merged hist files
        output_lfn_dict = {
            transform_id: {
                filetype: self._format_output_lfn(
                    [t for t in recent_transformations if int(t["TransformationID"]) == transform_id][0],
                    filetype,
                )
                for filetype in filetype_dict
            }
            for transform_id, filetype_dict in input_lfn_dict.items()
        }
        all_output_lfns = [lfn for filetype_dict in output_lfn_dict.values() for lfn in filetype_dict.values()]
        output_lfn_status = self._query_lfns_exist(all_output_lfns)

        # Update transformation dicts with info about histogram merging
        for transform in recent_transformations:
            if (transform_id := int(transform["TransformationID"])) in input_lfn_dict:
                merge_info = {
                    filetype: {
                        "InputLFNs": input_lfn_dict[transform_id][filetype],
                        "InputPFNs": input_pfn_dict[transform_id][filetype],
                        "OutputLFN": output_lfn_dict[transform_id][filetype],
                    }
                    for filetype in input_lfn_dict[transform_id]
                    if len(input_pfn_dict[transform_id][filetype]) > 0  # There are actually some PFNs to merge
                    and output_lfn_dict[transform_id][filetype]
                    in output_lfn_status["Failed"]  # Output LFN doesn't exist already
                }
                if len(merge_info) > 0:
                    transform.update({"HistogramMerging": merge_info})

        filtered_transformations = filter(lambda t: "HistogramMerging" in t, recent_transformations)

        return list(filtered_transformations)

    # Main method for processing a single transformation #######################

    def _handle_transformation(
        self,
        transform: dict,
        request: dict,
        file_key: str,
    ) -> Path:
        """Perform the merging, upload the file, write metadata to Bookkeeping and SimDQ repo"""

        merge_info = transform["HistogramMerging"][file_key]

        # Deduce filename of merged histogram file
        output_lfn = merge_info["OutputLFN"]
        output_fn = self.merge_dir / output_lfn.rsplit("/", maxsplit=1)[-1]

        # Merge the histogram files locally
        start = datetime.utcnow()
        self._write_merged_hist_file(merge_info["InputPFNs"], output_fn)
        end = datetime.utcnow()

        # Get some metadata about the merged histogram file
        output_md5 = hashlib.md5(output_fn.read_bytes()).hexdigest()
        output_guid = generateGuid(output_md5, "MD5")
        job_info = self._format_bk_job_info(
            transform,
            file_key,
            start,
            end,
            output_fn.stat().st_size,
            output_md5,
            output_guid,
        )

        # Upload the merged histogram file and register in Bookkeeping
        self._upload_and_register(output_lfn, output_fn, job_info, output_guid)
        output_pfn = self._query_pfns([output_lfn], dummy=not gDoRealMerging)[output_lfn]
        # Delete the local merged histogram file
        output_fn.unlink()

        # Generate the metadata YAML file to be read by Monet
        metadata = {"LFN": output_lfn, "PFN": output_pfn, "refLFN": output_lfn, "refPFN": output_pfn}
        metadata = self._format_metadata(transform, request, metadata)
        metadata_dir = self.simdq_dir / str(request["RequestID"]).rjust(8, "0") / transform["Parameters"]["eventType"]
        secondary_app_name = self._get_application_name(transform, file_key, secondary=True)
        step_index = file_key.split("-")[0]
        metadata_fn = f"{step_index}-{secondary_app_name.upper()}HIST.yml"
        self._write_metadata_file(metadata_dir, metadata_fn, metadata)

        # Return the path to the metadata YAML file so it can be committed
        return metadata_dir / metadata_fn

    # Methods that perform queries with the clients ############################

    def _query_recent_transformations(self) -> list[dict]:
        """Get transformations that have finished testing but are not yet archived"""
        if gStandAlone:
            return []
        query = {
            "Type": self.allowed_types,
            "Status": self.allowed_statuses,
        }
        transformations = returnValueOrRaise(self.tf_client.getTransformations(query))
        self.log.info(f"Found {len(transformations)} recent transformations with status {self.allowed_statuses}")
        return transformations

    def _query_requests(self, request_ids: list[int]) -> dict[int, dict]:
        if gStandAlone:
            # Rather than empty list, return dicts with expected keys but blank values
            return {req_id: {key: "" for key in REQ_KEYS} for req_id in request_ids}
        requests = returnValueOrRaise(self.rp_client.getProductionRequest(request_ids))
        self.log.info(f"Found {len(requests)} requests")
        return requests

    def _query_input_lfns(self, transform_ids: list[int]) -> list[str]:
        if gStandAlone:
            return []
        query = {
            "Production": transform_ids,
            "FileType": self._available_hist_filetypes,
            "Visibility": "Y",
            "ReplicaFlag": "Yes",
        }
        ret = returnValueOrRaise(self.bk_client.getFilesWithMetadata(query))
        lfn_records = [dict(zip(ret["ParameterNames"], record)) for record in ret["Records"]]
        all_lfns = [x["FileName"] for x in lfn_records]
        self.log.info(f"Found {len(all_lfns)} LFNs from {len(transform_ids)} transformations")
        return all_lfns

    def _query_pfns(self, lfns: list[str], *, dummy: bool = False) -> dict[str, str]:
        if dummy or gStandAlone:
            # Assume the LFNs are at CERN
            return {lfn: "root://eoslhcb.cern.ch//eos/lhcb/grid/prod" + lfn for lfn in lfns}
        replicas = returnValueOrRaise(self.dm_client.getReplicas(lfns, diskOnly=True, getUrl=True, protocol="root"))
        if replicas["Failed"]:
            raise NotImplementedError(replicas)
        all_pfns = {lfn: list(pfns.values())[0] for lfn, pfns in replicas["Successful"].items()}
        self.log.info(f"Found {len(all_pfns)} PFNs from {len(lfns)} LFNs")
        return all_pfns

    def _query_lfns_exist(self, lfns: list[str], *, expected: str = "Failed") -> dict:
        if gStandAlone:
            return {expected: lfns}
        result = returnValueOrRaise(self.bk_client.getFileMetadata(lfns))
        msg = ", ".join([f"{state}: {len(result[state])} LFNs" for state in result])
        self.log.info(msg)
        return result

    # Methods that transform existing data #####################################

    @staticmethod
    def _group_lfns_by_prod_and_type(lfns: list[str]) -> dict[int, dict[str, list[str]]]:
        """Group a list of LFNs by their transform ID and step+filetype, as nested dicts, e.g.:

        .. code-block:: python

            {
                1234: {"1-GAUSSHIST" : ["/lhcb/MC/2011/GAUSSHIST/...", ...]},
                1235: {"1-BOOLEHIST" : ["/lhcb/MC/2011/BOOLEHIST/...", ...]},
            }

        :param lfns: Flat list of LFNs to sort
        :returns: Nested dicts where the outer key is transform ID, and the
                  inner key is <step>_<filetype>, and the inner values are lists
                  of LFNs
        """
        lfn_regex = "/".join(
            [
                r"/lhcb/MC/(?P<data_type>[\w\.\-]+)",
                r"(?P<filetype>[A-Z]+HIST)",
                r"(?P<transform_id>\d{8})",
                r"\d{4}",
                r"(?P<application>\w+)\_\d{8}\_\d{8}\_(?P<step>\d+)\.Hist\.root",
            ]
        )
        pattern = re.compile(lfn_regex)
        sorted_lfns = {}
        for lfn in lfns:
            if (match := re.match(pattern, lfn)) is None:
                raise NotImplementedError(f"{lfn=} does not match pattern {lfn_regex}")
            # Pull out the strings used as/in dict keys
            parent_transform = int(match.group("transform_id"))
            filetype = match.group("filetype")
            step_index = match.group("step")
            key = "-".join([step_index, filetype])
            # Append the LFN to the right nested dict
            if parent_transform not in sorted_lfns:
                sorted_lfns[parent_transform] = {key: []}
            if key not in sorted_lfns[parent_transform]:
                sorted_lfns[parent_transform][key] = []
            sorted_lfns[parent_transform][key] += [lfn]
        return sorted_lfns

    def _parse_workflow_xml(self, xml: str) -> XMLNode:
        workflow = self.xml_parser.parseString(xml)[0]
        if workflow.name != "Workflow":
            raise NotImplementedError(f"Expected an XML Workflow node, found {workflow}")
        return workflow

    def _get_transformation_parameters(self, workflow: XMLNode) -> dict:
        """Extract the <Parameter> XML tags from the transform Body, convert to a dict"""
        parameters = {child.attributes["name"]: child.children[0].value for child in workflow.childrens("Parameter")}
        return parameters

    def _get_transformation_steps(self, workflow: XMLNode) -> dict[str, dict]:
        """Extract the <Parameter> XML tags from each <StepInstance> in the
        transform Body, convert to dict where the keys are the values of the
        <name> tags, and the values are dicts of the <Parameter> tags
        """
        step_instances = workflow.childrens("StepInstance")
        steps = {
            step.childrens("name")[0].value: {
                child.attributes["name"]: child.children[0].value for child in step.childrens("Parameter")
            }
            for step in step_instances
        }
        return steps

    @staticmethod
    def _is_dict_string(string: str) -> bool:
        """Deduce whether a string encodes a python dict as YAML/JSON"""
        if not isinstance(string, str):
            return False
        try:
            return isinstance(yaml.safe_load(string), dict)
        except yaml.parser.ParserError:
            return False

    def _parse_dict_strings(self, data: dict) -> dict:
        """Convert "string dicts" to actual dicts"""
        return {key: yaml.safe_load(value) if self._is_dict_string(value) else value for key, value in data.items()}

    def _format_metadata(self, transform: dict, request: dict, extra: dict) -> dict:
        """Content of the metadata YAML file to for SimDQ"""
        req_dict = {key: request[key] for key in REQ_KEYS}
        req_dict = self._parse_dict_strings(req_dict)

        tfm_dict = {key: transform[key] for key in TFM_KEYS}
        tfm_dict = self._parse_dict_strings(tfm_dict)

        metadata = copy(req_dict)
        metadata.update(tfm_dict)
        metadata.update(extra)

        return metadata

    @staticmethod
    def _get_application_name(transform: dict, file_key: str, *, secondary: bool = False) -> str:
        """Deduce the application name with the correct capitalisation"""
        step_index, filetype = file_key.split("-")
        matching_steps = list(
            filter(
                lambda step_name: str(step_name).upper() == f"{filetype.removesuffix('HIST')}_{step_index}",
                transform["Steps"].keys(),
            )
        )
        assert len(matching_steps) == 1
        app_key = matching_steps[0]
        step = transform["Steps"][app_key]
        if secondary and step["optionsFormat"]:
            return step["optionsFormat"]
        return step["applicationName"]

    def _format_output_lfn(self, transform: dict, file_key: str, merge_id: int = 0) -> str:
        step_index, filetype = file_key.split("-")
        transform_id = int(transform["TransformationID"])
        parameters = transform["Parameters"]
        app = self._get_application_name(transform, file_key)
        output_lfn = "/".join(
            [
                "/lhcb",
                parameters["configName"],
                parameters["configVersion"],
                f"{filetype}MERGED",
                f"{transform_id:08d}",
                "0" * 4,
                f"{app}_{transform_id:08d}_{merge_id}_{step_index}.Hist.root",
            ]
        )
        return output_lfn

    def _format_bk_job_info(
        self,
        transform: dict,
        file_key: str,
        start: datetime,
        end: datetime,
        output_filesize: int,
        output_md5: str,
        output_guid: str,
    ) -> BookkeepingJobInfo:
        transform_id = int(transform["TransformationID"])
        parameters = transform["Parameters"]
        merge_info = transform["HistogramMerging"][file_key]
        input_lfns = merge_info["InputLFNs"]
        output_lfn = merge_info["OutputLFN"]
        filetype = file_key.rsplit("-", maxsplit=1)[-1]
        fn_time = start.strftime("%Y%m%d%H%M%S")
        job_info = BookkeepingJobInfo(
            ConfigName=parameters["configName"],
            ConfigVersion=parameters["configVersion"],
            Date=end.strftime("%Y-%m-%d"),
            Time=end.strftime("%H:%M:%S"),
        )
        if simulation_condition := parameters.get("BKCondition"):
            job_info.simulation_condition = simulation_condition
        job_info.typed_parameters = BookkeepingJobInfo.TypedParameters(
            CPUTIME=f"{(end - start).total_seconds():.0f}",
            ExecTime=f"{(end - start).total_seconds() * self.n_cpus:.0f}",
            NumberOfProcessors=f"{self.n_cpus}",
            Production=f"{transform_id}",
            Name=f"{transform_id:08d}_{fn_time}_1",
            JobStart=start.strftime("%Y-%m-%d %H:%M"),
            JobEnd=end.strftime("%Y-%m-%d %H:%M"),
            Location=DIRAC.siteName(),
            ProgramName=f"lb-conda {self.lbconda_env_name}",
            ProgramVersion=self.lbconda_env_version,
            StepID="1",
            NumberOfEvents=f"{len(input_lfns)}",
        )
        job_info.input_files = input_lfns
        job_info.output_files = [
            BookkeepingJobInfo.OutputFile(
                Name=output_lfn,
                TypeName=f"{filetype}MERGED",
                TypeVersion="1",
                EventTypeId=parameters["eventType"],
                EventStat=f"{len(input_lfns)}",
                FileSize=str(output_filesize),
                CreationDate=end.strftime("%Y-%m-%d %H:%M:%S"),
                MD5Sum=output_md5,
                Guid=output_guid,
            ),
        ]
        return job_info

    # Methods that write and commit files ######################################

    @staticmethod
    def _write_metadata_file(metadata_dir: Path, metadata_fn: str, metadata: dict):
        metadata_dir.mkdir(parents=True, exist_ok=True)
        with open(metadata_dir / metadata_fn, "w", encoding="utf-8") as metadata_file:
            yaml.dump(metadata, metadata_file)

    @timeThis
    def _write_merged_hist_file(self, input_pfns: list[str], output_fn: str) -> subprocess.CompletedProcess:
        with tempfile.NamedTemporaryFile(mode="wt") as tmpfile:
            tmpfile.write("\n".join(input_pfns))
            tmpfile.flush()
            lbconda_env = f"{self.lbconda_env_name}/{self.lbconda_env_version}"
            if gDoRealMerging:
                cmd = [
                    "lb-conda",
                    lbconda_env,
                    "hadd",
                    "-ff",
                    "-j",
                    str(self.n_cpus),
                    str(output_fn),
                    f"@{tmpfile.name}",
                ]
            else:
                cmd = ["touch", str(output_fn)]
            self.log.info("Running command:", shlex.join(cmd))
            ret = subprocess.run(cmd, capture_output=True, text=True)
            level = self.log.debug if ret.returncode == 0 else self.log.info
            level("stdout:", ret.stdout)
            level("stderr:", ret.stderr)
            ret.check_returncode()
            return ret

    def _upload_and_register(self, output_lfn, output_fn, job_info, output_guid):
        bk_xml = job_info.to_xml().decode()
        if gStandAlone or not gDoRealUpdate:
            return
        returnValueOrRaise(self.bk_client.sendXMLBookkeepingReport(bk_xml))
        res = returnValueOrRaise(self.dm_client.putAndRegister(output_lfn, str(output_fn), self.hist_se, output_guid))
        if res["Failed"]:
            raise NotImplementedError(res)
        if {"put", "register"} - set(res["Successful"].get(output_lfn, [])):
            raise NotImplementedError(res)

    def _checkout_metadata(self):
        if (self.simdq_dir / ".git").is_dir():
            repo = git.Repo(self.simdq_dir)
            with repo.git.custom_environment(GIT_SSH_COMMAND=f"ssh -i {self.ssh_key}"):
                repo.remotes.origin.fetch()
            return repo

        repo = git.Repo.init(self.simdq_dir)
        if gUseGitRepo:
            if "origin" in [r.name for r in repo.remotes]:
                origin = repo.remotes.origin
                origin.set_url(self.simdq_url)
            else:
                origin = repo.create_remote("origin", self.simdq_url)
            with repo.git.custom_environment(GIT_SSH_COMMAND=f"ssh -i {self.ssh_key}"):
                origin.fetch()
            remote_branch = getattr(origin.refs, self.simdq_branch)
            repo.create_head(self.simdq_branch, remote_branch).set_tracking_branch(remote_branch).checkout()
        return repo

    def _commit_and_push_metadata(self, new_files: list[Path], message: str):
        if gStandAlone or not (gUseGitRepo and gDoRealUpdate):
            return
        with self.simdq_repo.git.custom_environment(GIT_SSH_COMMAND=f"ssh -i {self.ssh_key}"):
            self.simdq_repo.remotes.origin.pull(rebase=True, autostash=True)
            self.simdq_repo.index.add(map(str, new_files))
            self.simdq_repo.index.commit(message, author=self.git_author, committer=self.git_author)
            self.simdq_repo.remotes.origin.push().raise_if_error()
