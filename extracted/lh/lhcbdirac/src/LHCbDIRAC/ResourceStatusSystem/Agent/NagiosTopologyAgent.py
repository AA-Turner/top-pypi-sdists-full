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
"""LHCbDIRAC.ResourceStatusSystem.Agent.NagiosTopologyAgent.

NagiosTopologyAgent.__bases__: DIRAC.Core.Base.AgentModule.AgentModule

xml_append
"""
import os
import socket
import json

from urllib.parse import urlparse
from typing import Optional

from DIRAC import S_OK, gConfig, rootPath
from DIRAC.ConfigurationSystem.Client.Helpers.Resources import getSites
from DIRAC.ConfigurationSystem.Client.Helpers.Path import cfgPath
from DIRAC.Core.Base.AgentModule import AgentModule
from DIRAC.Resources.Storage.StorageElement import StorageElement

AGENT_NAME = "ResourceStatus/NagiosTopologyAgent"


MAPPING_CE_TYPE = {
    "lcg": "CE",
    "cream": "CREAM-CE",
    "arc": "ARC-CE",
    "arc6": "ARC-CE",
    "arex": "ARC-CE",
    "htcondorce": "HTCONDOR-CE",
    "vac": "VAC",
    "cloud": "CLOUD",
    "boinc": "BOINC",
    "vcycle": "VCYCLE",
    "dirac": "DIRAC",
}


def isHostIPV6(host: str) -> bool | None:
    """Test if the given host is ipv6 capable.

    :returns: True if IPv6 capable, False if only IPv4, None in case of resolution problem
    """
    try:  # First try IPV6
        socket.getaddrinfo(host, None, socket.AF_INET6)
        return True
    except socket.gaierror:  # No IPv6 address
        try:  # Next try IPv4
            socket.getaddrinfo(host, None, socket.AF_INET)
            return False
        except socket.gaierror:  # The host does not exist (no IPv6 or IPv4 address)
            return None


class NagiosTopologyAgent(AgentModule):
    """This agent loops over the Dirac CS and extracts the necessary information
    to create a "topology map" which is used by the IT provided Nagios system to
    test Grid sites. The topology information defines the services to be tested.

    NagiosTopologyAgent, writes the xml topology consumed by Nagios to run
    the tests.
    """

    def __init__(self, *args, **kwargs):
        AgentModule.__init__(self, *args, **kwargs)

        self.dryRun = False

    def execute(self):
        """Generates xml and json topology files"""

        res = getSites()
        if not res["OK"]:
            return res
        sites = res["Value"]

        # First, create the JSON topology, which contains also what the XML topology needs
        res = self.createJSONTopology(sites)
        if not res["OK"]:
            self.log.error("Failed to create JSON topology", res["Message"])
            return res
        self.log.info("Created JSON topology")

        return S_OK()

    def createJSONTopology(self, sites):
        """Function that creates a topology.json file, based on specification from WLCG group"""

        fullSitesDict = dict()
        for site in sites:
            grid = site.split(".")[0]
            res = gConfig.getOptionsDict(f"Resources/Sites/{grid}/{site}")
            if not res["OK"]:
                self.log.error("Failure getting options dict for site", f"{site}: {res['Message']}")
                continue
            siteInfoCS = res["Value"]
            wlcgName = siteInfoCS.get("Name")

            siteInfo = dict()
            siteInfo["WLCG_site"] = wlcgName
            # Tier level 4 is what they want for opportunistic resource
            siteInfo["Tier"] = siteInfoCS.get("MoUTierLevel", "4")
            siteInfo["Type"] = "GRID" if grid == "LCG" else site.split(".")[0]

            # Services is for CEs and SEs
            siteInfoServices = dict()

            # CEs
            res = gConfig.getSections(cfgPath("Resources", "Sites", grid, site, "CEs"), [])
            if not res["OK"]:
                self.log.error("Failure getting CEs section for site", f"{site}: {res['Message']}")
                continue
            if not res["Value"]:
                self.log.warn("Site without CEs", f"({site})")
            else:
                cesList = res["Value"]
                for ce in cesList:
                    res = gConfig.getOptionsDict(cfgPath("Resources", "Sites", grid, site, "CEs", ce))
                    if not res["OK"]:
                        self.log.error("Failure getting info on ce", f"{ce}: {res['Message']}")
                        continue

                    ceDetailsInCS = res["Value"]
                    ceDetails = dict()
                    ceDetails["type"] = "compute"
                    ceDetails["access_points"] = dict()
                    ceDetails["access_points"][ce] = dict()
                    ceDetails["access_points"][ce]["endpoint_url"] = ce
                    ceDetails["access_points"][ce]["ipv6_status"] = isHostIPV6(ce)
                    ceDetails["access_points"][ce]["type"] = MAPPING_CE_TYPE.get(
                        ceDetailsInCS["CEType"].lower(), "UNDEFINED"
                    )
                    # Port
                    if "Port" in ceDetailsInCS:
                        ceDetails["access_points"][ce]["port"] = ceDetailsInCS["Port"]
                    ceDetails["access_points"][ce]["monitored"] = "yes" if wlcgName else "no"
                    ceDetails["access_points"][ce]["quality_level"] = "production"
                    # queues
                    res = gConfig.getSections(cfgPath("Resources", "Sites", grid, site, "CEs", ce, "Queues"), [])
                    if not res["OK"]:
                        self.log.error("Failure getting info on ce/queues", f"{ce}: {res['Message']}")
                        continue
                    if not res["Value"]:
                        self.log.warn("CE without queues", f"({ce})")
                    else:
                        for queue in res["Value"]:
                            ceDetails["compute_shares"] = dict()
                            ceDetails["compute_shares"][queue] = dict()
                            ceDetails["compute_shares"][queue]["type"] = "queue"
                            ceDetails["compute_shares"][queue]["name"] = queue

                    siteInfoServices[ce] = ceDetails

            # SEs
            ses = gConfig.getValue(cfgPath("Resources", "Sites", grid, site, "SE"), [])
            if not ses:
                pass
            for se in ses:
                diracSE = StorageElement(se)  # this 'se' is .e.g. 'CERN-DST-EOS'
                seDetailsForDIRACSE = dict()
                seStorageSharesForDIRACSE = dict()
                writeProtocols = diracSE.localWriteProtocolList
                for diracSEoption in diracSE.protocolOptions:
                    # Building the storage_endpoints section
                    seDetails = dict()
                    proto = diracSEoption["Protocol"]
                    ep = os.path.join(
                        proto + "://" + diracSEoption["Host"].strip("/") + ":" + diracSEoption["Port"],
                        diracSEoption["Path"].strip("/"),
                    )
                    seDetails["endpoint_url"] = ep
                    seDetails["ipv6_status"] = isHostIPV6(urlparse(ep).hostname)
                    seDetails["interface_type"] = proto
                    seDetails["monitored"] = "yes" if wlcgName else "no"
                    seDetails["quality_level"] = "production"
                    seDetails["read_only"] = not (proto in writeProtocols)

                    dseep = "_".join([se, diracSEoption["Protocol"]])  # just a unique name e.g. 'CERN-DST-EOS_root'
                    seDetailsForDIRACSE[dseep] = seDetails

                    if diracSEoption.get("SpaceToken"):
                        # Building the storage_shares section
                        seDetails = dict()
                        seDetails["Name"] = diracSEoption["SpaceToken"]
                        seDetails["path"] = diracSEoption["WSUrl"]
                        if diracSEoption["Protocol"].lower() == "srm":
                            seDetails["assigned_endpoints"] = ep

                        dsess = "_".join(
                            [se, diracSEoption["SpaceToken"]]
                        )  # just a unique name e.g. 'CNAF-DST_LHCb-Disk'
                        seStorageSharesForDIRACSE[dsess] = seDetails

                siteInfoServices[se] = dict()
                siteInfoServices[se]["storage_endpoints"] = seDetailsForDIRACSE
                if seStorageSharesForDIRACSE:
                    siteInfoServices[se]["storage_shares"] = seStorageSharesForDIRACSE

                siteInfoServices[se]["storage_backend"] = {"T1D0": "tape", "T0D1": "disk"}.get(
                    diracSE.options.get("SEType"), "disk"
                )
                siteInfoServices[se]["type"] = "storage"
                siteInfoServices[se]["quality_level"] = "production"
                siteInfoServices[se]["monitored"] = "yes" if wlcgName else "no"

            siteInfo["Services"] = siteInfoServices
            fullSitesDict[site] = siteInfo

        topologyFile = os.path.join(rootPath, "webRoot/www/topology/topology.json")
        if not self.dryRun:
            with open(topologyFile, "w") as tj:
                json.dump(fullSitesDict, tj)
                self.log.verbose("JSON topology saved", topologyFile)
        else:
            self.log.info(f"[DRY RUN]Would have created file {topologyFile} with following content")
            self.log.info(json.dumps(fullSitesDict))

        return S_OK()
