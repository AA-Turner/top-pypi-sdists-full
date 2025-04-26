###############################################################################
# (c) Copyright 2024 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
"""
Retrieve and verify information about the inputs to an Analysis Production
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
import re
from itertools import islice
from pathlib import Path
import sys

from rich.progress import track

from DIRAC import gLogger
from DIRAC.Core.Base.Script import Script
from DIRAC.Core.Utilities.ReturnValues import returnValueOrRaise, convertToReturnValue
from DIRAC.ConfigurationSystem.Client.ConfigurationClient import ConfigurationClient
from LHCbDIRAC.ProductionManagementSystem.Client.AnalysisProductionsClient import AnalysisProductionsClient
from LHCbDIRAC.BookkeepingSystem.Client.BookkeepingClient import BookkeepingClient
from LHCbDIRAC.TransformationSystem.Client.TransformationClient import TransformationClient


def parseArgs():
    version = ""
    with_ancestors = False
    output = ""

    @convertToReturnValue
    def setVersion(s: str):
        nonlocal version
        version = s

    @convertToReturnValue
    def withAncestors(_):
        nonlocal with_ancestors
        with_ancestors = True

    @convertToReturnValue
    def setOutput(s: str):
        nonlocal output
        output = s

    switches = [
        ("", "version=", "Version of the Analysis Production (optional)", setVersion),
        (
            "",
            "with-ancestors",
            "Return all ancestors of the production -- usually a LOT of files. Not recommended unless --output is also set.",
            withAncestors,
        ),
        ("", "output=", "Path to a .json file to dump the output to", setOutput),
    ]
    Script.registerSwitches(switches)
    Script.registerArgument("wg: Name of the WG the production belongs to e.g. `bnoc`")
    Script.registerArgument("analysis: Name of the analysis e.g. `bds2kstkstb`")
    Script.registerArgument("name: Name of the job in the production e.g. `13104007_bs2kst_892_kstb_892_2011_magup`")
    Script.parseCommandLine(ignoreErrors=False)
    wg, analysis, name = Script.getPositionalArgs(group=True)
    wg = wg.lower()
    analysis = analysis.lower()
    name = name.lower()

    if not ConfigurationClient().ping()["OK"]:
        gLogger.fatal("Failed to contact CS, do you have a valid proxy?")
        sys.exit(1)

    return (
        wg,
        analysis,
        name,
        version,
        with_ancestors,
        output,
    )


@Script()
def main():
    wg, analysis, name, version, with_ancestors, output = parseArgs()
    config = {
        "wg": wg,
        "analysis": analysis,
        "name": name,
    }
    if version != "":
        config["version"] = version
    save_output = False
    if output != "":
        output = Path(output)
        save_output = True

    tc = TransformationClient()
    bk = BookkeepingClient()
    apc = AnalysisProductionsClient()

    apd_info = _get_info_from_apd(apc, config)
    # Add the ancestors information
    all_ancestors = _get_ancestors_info(apd_info, bk)
    relational_ancestors = [{"lfn": lfn, "ancestors": []} for lfn in apd_info["apd_lfns"]]

    relational_ancestors = _attach_ancestors(relational_ancestors, all_ancestors, 1, apd_info["depth"])

    # Check the ancestors info matches the bk query and no duplicate files
    extra_info = _check_inputs(apd_info, all_ancestors, bk, tc)
    oldest_ancestors = []
    # pylint: disable-next=E1126
    for anc_list in all_ancestors[apd_info["depth"]].values():
        oldest_ancestors += anc_list

    events_ancestors, empty_files_ancestors = _get_total_num_events(oldest_ancestors, bk)
    events_expected, empty_files_expected = _get_total_num_events(extra_info["input_lfns"], bk)

    if events_ancestors != events_expected:
        gLogger.warn("The number of input events does not match the expeced number of events from bookeeping")
        gLogger.warn("Check `missing_ancestors` or `extra_ancestors` to see if a file was skipped or duplicated.")
    gLogger.always(f"Input events: {events_ancestors}")
    gLogger.always(f"Expected events: {events_expected}")

    all_info = {
        "ancestors_timestamp": datetime.now(tz=timezone.utc).isoformat(),
        "wg": config["wg"],
        "analysis": config["analysis"],
        "version": _get_aprod_version(apd_info, config),
        "name": config["name"],
        "input_query": extra_info["query"],
        "n_input_events": events_ancestors,
        "n_expected_events": events_expected,
        "missing_ancestors": extra_info["missing_ancestors"],
        "extra_ancestors": extra_info["extra_ancestors"],
        "duplicate_ancestors": extra_info["duplicate_ancestors"],
    }

    if with_ancestors:
        all_info["ancestors"] = relational_ancestors

    if save_output:
        with open(output, "w") as out_f:
            gLogger.info(f"Writing info to requested json file {output}")
            json.dump(all_info, out_f, indent=4)
    else:
        # could maybe make the output a bit nicer
        # i.e. some fields only on verbose
        for info_name, field in all_info.items():
            if info_name != "ancestors":
                gLogger.info(f"{info_name}: {field}")
        if with_ancestors:
            gLogger.warn("All ancestors information only prints to stdout if verbose (`use -d`)")
            gLogger.verbose("Ancestors:\n")
            gLogger.verbose(all_info["ancestors"])


def _batched(iterable, n):
    """
    batched("ABCDEFG", 3) -> ABC DEF G
    """
    if n < 1:
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch


def _get_info_from_apd(apc, apc_kwargs):
    apd_info = {"apd_lfns": [], "depth": None}
    prods = returnValueOrRaise(
        apc.getProductions(**apc_kwargs, with_transformations=True, with_lfns=True, with_pfns=False)
    )

    if len(prods) == 0:
        raise ValueError(f"Could not find a production matching tags {apc_kwargs}")
    if len(prods) > 1:
        raise NotImplementedError(f"Tags must match only one production")

    prod = prods[0]

    # Output lfns from this production
    lfns = prod["lfns"]
    apd_info["apd_lfns"] = lfns

    # Should always be 2 but can have > 2 steps
    if len(prod["transformations"]) != 2:
        raise NotImplementedError("Production has more than 2 transformations!")

    depth = sum([len(x["steps"]) for x in prod["transformations"]])
    apd_info["depth"] = depth

    gLogger.always(f"{len(lfns)} LFNs and depth of {depth}")
    apd_info["transformations"] = prod["transformations"]
    return apd_info


def _get_aprod_version(apd_info, config):
    """
    Version is an optional argument but if not supplied can be determined
    from the apd_info
    """
    if "version" not in config:
        found_version = False
        for transformation in apd_info["transformations"]:
            for step in transformation["steps"]:
                if "extras" in step:
                    version = re.findall(
                        r"AnalysisProductions\.(v\d+r\d+p\d+|v\dr\d+)",
                        " ".join(step["extras"]),
                    )
                    if len(version) == 1:
                        return version[0]
                    elif len(version) > 1:
                        raise NotImplementedError(
                            f"Found multiple versions in production:\
                            {step['extras']} for transformation {transformation}"
                        )
        if not found_version:
            raise RuntimeError(f"Could not find AnalysisProduction version from {apd_info}")
    else:
        version = config["version"]
    return version


def _get_ancestors_info(apd_info, bk):
    """
    Get the ancestors for every LFN produced by the Aprod
    A separate step `attach_ancestors` will then recover the relationship
    between the different levels of LFNs.
    """
    all_ancestors = [apd_info["apd_lfns"]]
    for depth in range(apd_info["depth"]):
        if depth == 0:
            lfn_names = all_ancestors[depth]
        else:
            lfn_names = []
            for anc_dict in all_ancestors[depth].values():
                lfn_names += [parent_dict["lfn"] for parent_dict in anc_dict]
        ancestors = {}
        for lfn_batch in track(
            _batched(lfn_names, 50), total=len(lfn_names) // 50, description=f"Getting ancestors at depth {depth + 1}"
        ):
            ancestors_dict = returnValueOrRaise(bk.getFileAncestors(list(lfn_batch), depth=1, replica=False))
            if ancestors_dict["Failed"] != []:
                raise RuntimeError(f"Failed to get all file ancestors: {ancestors_dict['Failed']}")
            ancestors |= ancestors_dict["Successful"]
        # need to use getFileMetadata() as well to get the size
        ancestors_trimmed = {}
        lfns = []
        for child_lfn, ancestor_dicts in ancestors.items():
            lfns += [[anc_dict["FileName"], child_lfn] for anc_dict in ancestor_dicts]

        for lfn_batch in track(
            _batched(lfns, 10_000), total=len(lfns) // 10_000, description=f"Getting file metadata at depth {depth + 1}"
        ):
            childs = []
            parents = []
            for lfn_names in lfn_batch:
                parent, child = lfn_names
                childs.append(child)
                parents.append(parent)
            metadata = returnValueOrRaise(bk.getFileMetadata(parents))
            if metadata["Failed"] != []:
                raise RuntimeError(f"Failed to get metadata for {metadata['Failed']}")
            meta_success = metadata["Successful"]
            for child, parent in zip(childs, parents):
                if child not in ancestors_trimmed:
                    ancestors_trimmed[child] = []
                ancestors_trimmed[child] += [
                    {
                        "lfn": parent,
                        "n_events": meta_success[parent]["EventStat"],
                        "size": meta_success[parent]["FileSize"],
                    }
                ]
        all_ancestors.append(ancestors_trimmed)

    return all_ancestors


def _attach_ancestors(top_dict, all_dicts, i, depth):
    """
    Recursively attach the ancestor LFNs from each transformation
    to the resulting LFN
    """
    for j, lfn_dict in enumerate(top_dict):
        lfn_dict["ancestors"] = all_dicts[i][lfn_dict["lfn"]]
        if i + 1 <= depth:
            lfn_dict["ancestors"] = _attach_ancestors(lfn_dict["ancestors"], all_dicts, i + 1, depth)
            top_dict[j] = lfn_dict
    return top_dict


def _check_inputs(apd_info, all_ancestors, bk, tc):
    """
    Checks the ancestors against the bk query result
    Should hopefully be the same but in case they are not we can report it
    """
    # These will always be the deepest LFNs
    from_ancestors_lfns = []
    for anc_list in all_ancestors[apd_info["depth"]].values():
        from_ancestors_lfns += [anc_dict["lfn"] for anc_dict in anc_list]
    output_info = {"missing_ancestors": [], "extra_ancestors": [], "from_ancestors_lfns": from_ancestors_lfns}
    # Already check earlier we should have only 2 transformations but check
    # which is the merge step
    prev_tid = apd_info["transformations"][0]["id"]
    next_tid = apd_info["transformations"][1]["id"]
    query = None
    prev_query = returnValueOrRaise(tc.getBookkeepingQuery(prev_tid))
    next_query = returnValueOrRaise(tc.getBookkeepingQuery(next_tid))
    if "ProductionID" in prev_query and prev_query["ProductionID"] == next_tid:
        query = next_query
    elif "ProductionID" in next_query and next_query["ProductionID"] == prev_tid:
        query = prev_query
    else:
        raise RuntimeError(
            f"Could not determine the merge step for\
                           {apd_info['transformations']}"
        )

    input_lfns = returnValueOrRaise(bk.getFiles(query))
    output_info["input_lfns"] = input_lfns
    output_info["query"] = query
    found_mismatch = False
    if len(input_lfns) != len(from_ancestors_lfns):
        gLogger.warn(
            "Mismatch between number of input LFNs from bookeeping query"
            + f" ({len(input_lfns)}) and ancestor information ({len(from_ancestors_lfns)})"
        )
        found_mismatch = True
    for anc_lfn in from_ancestors_lfns:
        if anc_lfn not in input_lfns:
            output_info["extra_ancestors"].append(anc_lfn)
            found_mismatch = True
    for in_lfn in input_lfns:
        if in_lfn not in from_ancestors_lfns:
            output_info["missing_ancestors"].append(in_lfn)
            found_mismatch = True
    # Can check here too that files have not been run-over multiple times
    dupes = []
    if len(set(from_ancestors_lfns)) != len(from_ancestors_lfns):
        # now we know we have duplicates find out which ones
        no_dupes = set()
        prev_len = 0
        for lfn in from_ancestors_lfns:
            no_dupes.add(lfn)
            if len(no_dupes) == prev_len:
                dupes.append(lfn)
            else:
                prev_len += 1
        gLogger.warn("Found LFN(s) that have been run-over more than once!")
    output_info["duplicate_ancestors"] = dupes
    if not found_mismatch:
        gLogger.always("All checks passed!")
    return output_info


def _get_total_num_events(lfns, bk):
    """
    `lfns` can be a list of dicts with `lfn` and `n_events` as keys or
    just a list of LFN strings and it will lookup the number of events
    """
    total_events = 0
    no_events_lfns = []
    lfns_to_sum = []
    # if a dict of lfns we may already have EventStat/n_events
    bad_input = False
    if all([isinstance(entry, dict) for entry in lfns]):
        if all(["n_events" in entry for entry in lfns]):
            lfns_to_sum = lfns
        else:
            bad_input = True
    elif all([isinstance(entry, str) for entry in lfns]):
        lfns_meta_success = {}
        for lfn_batch in track(
            _batched(lfns, 10_000), total=len(lfns) // 10_000, description="Getting file metadata from input query"
        ):
            lfns_meta = returnValueOrRaise(bk.getFileMetadata(list(lfn_batch)))
            if lfns_meta["Failed"] != []:
                raise RuntimeError(f"Failed to get all metadata for LFNs: {lfns_meta['Failed']}")
            lfns_meta_success |= lfns_meta["Successful"]
        lfns_to_sum = [{"lfn": lfn, "n_events": lfn_info["EventStat"]} for lfn, lfn_info in lfns_meta_success.items()]
    else:
        bad_input = True
    if bad_input:
        raise NotImplementedError(
            "Must provide a list of dictionaries with the fields `lfn` and\
            `n_events` or just a list of LFN names"
        )

    for lfn_info in lfns_to_sum:
        events = lfn_info["n_events"]
        # Seems there are some files with EventStat = 0 but still have a
        # Luminosity value in data
        if events == 0 or events is None:
            no_events_lfns.append(lfn_info["lfn"])
        else:
            total_events += events
    return total_events, no_events_lfns


if __name__ == "__main__":
    main()
