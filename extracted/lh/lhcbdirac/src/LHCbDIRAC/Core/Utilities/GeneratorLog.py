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
"""Utilities to parse the XML Generator Logs."""
import ast
import json
import xmltodict
import re


def counterJson(listCounters):
    """returns a dictionary containing counters

    :param list listCounters: list containing all the counter nodes
    """
    dictCounters = dict()
    if isinstance(listCounters, dict):
        listCounters = [listCounters]
    for counter in listCounters:
        dictCounters[counter["@name"]] = int(counter["value"])
    return dictCounters


def efficiencyJson(listEfficiencies):
    """returns a dictionary containing efficiencies

    :param list listEfficiencies: list containing all the efficiency nodes
    """
    dictEfficiencies = dict()
    if isinstance(listEfficiencies, dict):
        listEfficiencies = [listEfficiencies]
    for efficiency in listEfficiencies:
        dictEfficiencies[efficiency["@name"]] = {
            "after": int(efficiency["after"]),
            "before": int(efficiency["before"]),
            "error": float(efficiency["error"]),
            "value": float(efficiency["value"]),
        }
    return dictEfficiencies


def fractionJson(listFractions):
    """returns a dictionary containing fractions

    :param list listFractions: list containing all the fraction nodes
    """
    dictFractions = dict()
    if isinstance(listFractions, dict):
        listFractions = [listFractions]
    for fraction in listFractions:
        dictFractions[fraction["@name"]] = {
            "number": int(fraction["number"]),
            "error": float(fraction["error"]),
            "value": float(fraction["value"]),
        }
    return dictFractions


def crossSectionJson(listCrossSections):
    """returns a dictionary containing cross sections

    :param list listCrossSections: list containing all the cross section nodes
    """
    dictCrossSections = dict()
    if isinstance(listCrossSections, dict):
        listCrossSections = [listCrossSections]
    for crossSection in listCrossSections:
        dictCrossSections[crossSection["description"][1:-1]] = {
            "ID": int(crossSection["@id"]),
            "generated": int(crossSection["generated"]),
            "value": float(crossSection["value"]),
        }
    return dictCrossSections


def methodGeneratorJson(listMethods, listGenerators, numberEventTypes):
    """returns a dictionary containing the generator for each method

    :param list listMethods: list containing all the methods
    :param list listGenerators: list containing all the generators
    :param int numberEventTypes: number of event types in the generator log
    """
    dictMethods = dict()
    if numberEventTypes > 1:
        for i, method in enumerate(listMethods):
            dictMethods[method] = listGenerators[i]
    else:
        dictMethods[listMethods] = listGenerators
    return dictMethods


class GeneratorLog:

    correctiveRegExps = {
        r"[\x00-\x09\x0b\x0c\x0e-\x1f\x7f-\xff]+": "",  # correct for memory garbage from Fortran
        r"-?nan": "-1",  # all NaNs replaced with same invalid value
        r"\?+": "",  # account for replace chars when filtering ASCII
        r'>\s*?"\s*+': ">",  # eliminate padding in XS description tags
        r'(?<=<description>)\s*?"\s*': "",
        r'\s++\S{,2}"\s*(?=</description>)': "",
        r'"\s(?=</description>)': "",
    }

    def __init__(self):
        pass

    def generatorLogJson(self, fileName):
        """converts the xml Generator Log into json format"""
        dictElements = dict()
        dictGenerator = dict()

        with open("GeneratorLog.xml", "rb") as fp:
            fileLines = fp.read().decode("ascii", errors="replace").split("\n")

        fileLines = fileLines[fileLines.index("<generatorCounters>") : fileLines.index("</generatorCounters>") + 1]
        xmlText = "".join(fileLines)
        numberEventTypes = xmlText.count("<eventType>")
        if numberEventTypes > 1:
            # Taking the first set of nodes
            xmlText = (
                xmlText.split("<eventType>")[0]
                + "<eventType>"
                + xmlText.split("<eventType>")[1]
                + "<method>"
                + xmlText.split("<eventType>")[-1].split("<method>", 1)[-1]
            )  # noqa

        for rexp, rrepl in GeneratorLog.correctiveRegExps.items():
            xmlText = re.sub(rexp, rrepl, xmlText, re.I | re.M)

        dicto = xmltodict.parse(xmlText)
        jsonData = ast.literal_eval(json.dumps(dicto))

        listCounters = jsonData["generatorCounters"].get("counter", [])
        listEfficiencies = jsonData["generatorCounters"].get("efficiency", [])
        listFractions = jsonData["generatorCounters"].get("fraction", [])
        listCrossSections = jsonData["generatorCounters"].get("crosssection", [])
        listMethods = jsonData["generatorCounters"]["method"]
        listGenerators = jsonData["generatorCounters"]["generator"]

        dictElements["counter"] = counterJson(listCounters)
        dictElements["efficiency"] = efficiencyJson(listEfficiencies)
        dictElements["fraction"] = fractionJson(listFractions)
        dictElements["crossSection"] = crossSectionJson(listCrossSections)
        dictElements["method"] = methodGeneratorJson(listMethods, listGenerators, numberEventTypes)

        dictGenerator["generatorCounters"] = dictElements

        with open(fileName, "w", encoding="utf-8") as fp:
            fp.write(str(json.dumps(dictGenerator, indent=2)))

        return dictGenerator
