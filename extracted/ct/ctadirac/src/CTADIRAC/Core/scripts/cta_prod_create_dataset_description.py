#!/usr/bin/env python
"""
Create datasets descriptions (in json format) for DL2 processing with ctapipe
If unmerged DL2 files contain images, the corresponding datasets can be created using with_images=True (default False)
The produced json files can be used as inputs to cta-prod-add-dataset

Usage example:
   cta-prod-create-dataset-description --MCCampaign=PROD5b --site=LaPalma --array_layout=Alpha --az=180 --zen=20.0
   --ctapipe_ver=v0.19.0 --nsb=1 --with_images=True
"""

__RCSID__ = "$Id$"

import json

import DIRAC
from DIRAC.Core.Base.Script import Script


@Script()
def main():
    Script.registerSwitch("", "MCCampaign=", "MCCampaign")
    Script.registerSwitch("", "site=", "site")
    Script.registerSwitch("", "array_layout=", "array layout")
    Script.registerSwitch("", "az=", "azimuth angle")
    Script.registerSwitch("", "zen=", "zenith angle")
    Script.registerSwitch("", "div_ang=", "divergent angle")
    Script.registerSwitch("", "nsb=", "nsb")
    Script.registerSwitch("", "max_merged=", "max_merged")
    Script.registerSwitch("", "ctapipe_ver=", "ctapipe version")
    Script.registerSwitch("", "with_images=", "with images flag")
    switches, argss = Script.parseCommandLine(ignoreErrors=True)

    if not switches:
        Script.showHelp()

    # defaults
    MCCampaign = "PROD5b"
    site = "LaPalma"
    array_layout = "Alpha"
    phiP = 180.0
    thetaP = 20
    div_ang = None
    nsb = 1
    max_merged = 3
    analysis_prog_version = "v0.19.0"
    with_images = "False"

    for switch in switches:
        if switch[0] == "MCCampaign":
            MCCampaign = switch[1]
        elif switch[0] == "site":
            site = switch[1]
        elif switch[0] == "array_layout":
            array_layout = switch[1]
        elif switch[0] == "az":
            if switch[1] == "0":
                phiP = 180.0
            elif switch[1] == "180":
                phiP = 0.0
            else:
                DIRAC.gLogger.error("az allowed values are: 0, 180")
                DIRAC.exit(-1)
        elif switch[0] == "zen":
            thetaP = float(switch[1])
        elif switch[0] == "div_ang":
            div_ang = switch[1]
        elif switch[0] == "nsb":
            nsb = int(switch[1])
        elif switch[0] == "max_merged":
            max_merged = int(switch[1])
        elif switch[0] == "ctapipe_ver":
            analysis_prog_version = switch[1]
        elif switch[0] == "with_images":
            with_images = switch[1]

    if with_images == "True":
        file_ext_list = [
            ".DL1ImgParDL2Geo.json",
            ".DL1ParDL2Geo.json",
            ".DL2GeoEneGam.json",
        ]
    else:
        file_ext_list = [
            ".DL1ParDL2Geo.json",
            ".DL2GeoEneGam.json",
        ]
    file_name_list = []

    for file_ext in file_ext_list:
        if file_ext == ".DL1ImgParDL2Geo.json":
            analysis_prog = "ctapipe-merge"
            merged = 1
        if file_ext == ".DL1ParDL2Geo.json":
            analysis_prog = "ctapipe-merge"
            merged = max_merged
        if file_ext == ".DL2GeoEneGam.json":
            analysis_prog = "ctapipe-apply-models"
            merged = 0

        MDdict_common = {
            "analysis_prog": analysis_prog,
            "data_level": {"=": 2},
            "merged": {"=": merged},
            "sct": "False",
            "outputType": "Data",
        }

        for particle in ["gamma-diffuse", "proton", "gamma", "electron"]:
            MDdict = {
                "MCCampaign": MCCampaign,
                "site": site,
                "array_layout": array_layout,
                "particle": particle,
                "thetaP": {"=": int(thetaP)},
                "phiP": {"=": phiP},
                "nsb": {"=": nsb},
            }

            if div_ang:
                MDdict.update({"div_ang": {"=": div_ang}})

            MDdict.update({"analysis_prog_version": analysis_prog_version})

            if particle == "gamma-diffuse":
                if file_ext == ".DL2GeoEneGam.json":
                    split_list = ["test"]
                else:
                    split_list = ["train_en", "train_cl", "test"]
            elif particle == "proton":
                if file_ext == ".DL2GeoEneGam.json":
                    split_list = ["test"]
                else:
                    split_list = ["train_cl", "test"]
            elif particle in ["gamma", "electron"]:
                split_list = ["test"]

            for split in split_list:
                fields = []
                MDdict["split"] = split

                for key, value in MDdict.items():
                    if key == "thetaP":
                        fields.append("zen0" + str(value["="]))
                    elif key == "phiP":
                        if value["="] == 180:
                            az = "000"
                        elif value["="] == 0:
                            az = "180"
                        fields.append("az" + az)
                    elif key == "split":
                        fields.append(str(value) + "_merged")
                    elif key == "nsb":
                        fields.append("nsb0" + str(value["="]) + "x")
                    elif key == "div_ang":
                        fields.append("div" + str(value["="]))
                    elif key == "site":
                        fields.append(value.lower())
                    elif key in [
                        "MCCampaign",
                        "array_layout",
                        "particle",
                        "site",
                        "analysis_prog_version",
                    ]:
                        fields.append(value.lower())

                if particle in ["gamma", "electron"]:
                    MDdict.pop("split")

                MDdict.update(MDdict_common)
                json_string = json.dumps(MDdict)

                if div_ang:
                    file_name = (
                        "_".join(fields[0:4])
                        + "_"
                        + "".join(fields[4:8])
                        + "_"
                        + "_".join(fields[8:10])
                    )
                else:
                    file_name = (
                        "_".join(fields[0:4])
                        + "_"
                        + "".join(fields[4:7])
                        + "_"
                        + fields[7]
                        + "_"
                        + "_".join(fields[8:10])
                    )

                file_list = (
                    "_".join(fields[0:3])
                    + "_"
                    + "".join(fields[4:7])
                    + "_"
                    + fields[7]
                    + "_dataset_json.list"
                )
                file_name_list.append(file_name.capitalize() + file_ext)
                # Write a json file with dataset query
                f = open(file_name.capitalize() + file_ext, "w")
                f.write(json_string.replace('"', "'") + "\n")
                f.close()

    # Add another dataset for all final DL1 and or DL2 files
    MDdict.pop("particle")
    MDdict["split"] = "test"
    MDdict["data_level"] = {"<=": 2}
    json_string = json.dumps(MDdict)
    if div_ang:
        file_name = (
            "_".join(fields[0:3])
            + "_"
            + "".join(fields[4:8])
            + "_"
            + "_".join(fields[8:10])
        )
    else:
        file_name = (
            "_".join(fields[0:3])
            + "_"
            + "".join(fields[4:7])
            + "_"
            + fields[7]
            + "_"
            + "_".join(fields[8:10])
        )

    file_name_list.append(file_name.capitalize() + file_ext)
    f = open(file_name.capitalize() + file_ext, "w")
    f.write(json_string.replace('"', "'") + "\n")
    f.close()

    # Add a dataset with all processing final and intermediate products (Data, Models)
    file_ext = ".Data.json"
    MDdict.pop("split")
    MDdict.pop("merged")
    MDdict["outputType"] = {"in": ["Data", "Model"]}
    MDdict["analysis_prog"] = {
        "in": [
            "ctapipe-merge",
            "ctapipe-process",
            "ctapipe-apply-models",
            "ctapipe-train-particle-classifier",
            "ctapipe-train-energy-regressor",
        ]
    }
    json_string = json.dumps(MDdict)
    file_name = "_".join(fields[0:3]) + "_" + "".join(fields[4:7]) + "_" + fields[7]

    file_name_list.append(file_name.capitalize() + file_ext)
    f = open(file_name.capitalize() + file_ext, "w")
    f.write(json_string.replace('"', "'") + "\n")
    f.close()

    # Add a dataset with Logs for all processing final and intermediate products
    file_ext = ".Log.json"
    MDdict.pop("nsb")
    MDdict["outputType"] = "Log"
    MDdict["analysis_prog"] = {
        "in": [
            "ctapipe-merge",
            "ctapipe-process",
            "ctapipe-apply-models",
            "ctapipe-train-particle-classifier",
            "ctapipe-train-energy-regressor",
        ]
    }
    json_string = json.dumps(MDdict)
    file_name = "_".join(fields[0:3]) + "_" + "".join(fields[4:7]) + "_" + fields[7]

    file_name_list.append(file_name.capitalize() + file_ext)
    f = open(file_name.capitalize() + file_ext, "w")
    f.write(json_string.replace('"', "'") + "\n")
    f.close()

    # Add dataset names to _dataset.list
    f = open(file_list.capitalize(), "w")
    for file_name in file_name_list:
        f.write(file_name + "\n")
    f.close()

    DIRAC.gLogger.notice(
        "list of dataset descriptions dumped into:", file_list.capitalize()
    )


####################################################
if __name__ == "__main__":
    main()
