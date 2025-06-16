import datetime

from CTADIRAC.Interfaces.API.CTAJob import MetadataDict

software_version = "v0.19.2"
simulation_software_version = "2020-06-29b"
simpipe_software_version = "v0.16-avx2"

SIMULATION_CONFIG = {
    "ID": 1,
    "input_meta_query": {"parentID": None, "dataset": None},
    "job_config": {
        "type": "MCSimulation",
        "version": simulation_software_version,
        "array_layout": "Advanced-Baseline",
        "site": "LaPalma",
        "particle": "gamma-diffuse",
        "pointing_dir": "North",
        "zenith_angle": 20,
        "n_shower": 50,
        "magic": None,
        "sct": None,
        "moon": "dark",
        "start_run_number": 0,
    },
}
SIMPIPE_CONFIG = {
    "ID": 1,
    "input_meta_query": {"parentID": None, "dataset": None},
    "job_config": {
        "type": "SimPipe",
        "version": simpipe_software_version,
        "simpipe_config": "simpipe_config.yml",
        "run_number": 1,
        "run_number_offset": 0,
    },
}
SIM_TELARRAY_PROCESSING_CONFIG = {
    "ID": 2,
    "input_meta_query": {"parentID": 1},
    "job_config": {
        "type": "SimTelProcessing",
        "version": simulation_software_version,
        "moon": "dark",
        "sct": None,
        "instrument_random_seeds": False,
        "group_size": 1,
    },
}
PROCESSING_CONFIG = {
    "ID": 2,
    "input_meta_query": {"parentID": 1, "moon": "dark"},
    "job_config": {
        "type": "CtapipeProcessing",
        "version": software_version,
        "output_extension": "DL2.h5",
        "options": "--config v3/dl0_to_dl2.yml --config v3/prod5b/subarray_north_alpha.yml",
        "array_layout": "Alpha",
        "data_level": 2,
        "group_size": 1,
    },
}
MERGING_CONFIG_1 = {
    "ID": 3,
    "input_meta_query": {"parentID": 2, "dataset": None},
    "job_config": {
        "type": "Merging",
        "version": software_version,
        "group_size": 5,
        "output_extension": "merged.DL2.h5",
    },
}
MERGING_CONFIG_2 = {
    "ID": 4,
    "input_meta_query": {"parentID": 3, "dataset": None},
    "job_config": {
        "type": "Merging",
        "version": software_version,
        "group_size": 2,
        "output_extension": "alpha_train_en_merged.DL2.h5",
        "options": "--no-dl1-images --no-true-images",
        "catalogs": "DIRACFileCatalog",
    },
}
COMMON_CONFIG = {
    "MCCampaign": "Prod5bTest",
    "configuration_id": 1,
    "base_path": "/vo.cta.in2p3.fr/tests/",
}

WORKFLOW_CONFIG = {
    "ProdSteps": [
        SIMULATION_CONFIG,
        PROCESSING_CONFIG,
        MERGING_CONFIG_1,
        MERGING_CONFIG_2,
    ],
    "Common": COMMON_CONFIG,
}

SIMULATION_OUTPUT_METADATA = MetadataDict(
    [
        ("array_layout", "Advanced-Baseline"),
        ("site", "LaPalma"),
        ("particle", "gamma-diffuse"),
        ("phiP", 180.0),
        ("thetaP", 20.0),
        ("sct", "False"),
        ("tel_sim_prog", "sim_telarray"),
        ("tel_sim_prog_version", "2020-06-29b"),
        ("data_level", -1),
        ("outputType", "Data"),
        ("configuration_id", 1),
        ("MCCampaign", "Prod5bTest"),
    ]
)

SIMPIPE_OUTPUT_METADATA = MetadataDict(
    [
        ("array_layout", "Alpha"),
        ("site", "LaPalma"),
        ("particle", "gamma-diffuse"),
        ("phiP", 180.0),
        ("thetaP", 20.0),
        ("sct", "False"),
        ("tel_sim_prog", "simpipe"),
        ("tel_sim_prog_version", simpipe_software_version),
        ("data_level", -1),
        ("outputType", "Data"),
        ("configuration_id", 1),
        ("MCCampaign", "Prod5bTest"),
        ("type", "SimPipe"),
        ("version", simpipe_software_version),
    ]
)

CTAPIPE_PROCESS_METADATA = MetadataDict(
    [
        ("array_layout", "Alpha"),
        ("site", "LaPalma"),
        ("particle", "gamma-diffuse"),
        ("phiP", 180),
        ("thetaP", 20.0),
        ("sct", "False"),
        ("tel_sim_prog", "sim_telarray"),
        ("tel_sim_prog_version", "2020-06-29b"),
        ("data_level", 2),
        ("outputType", "Data"),
        ("configuration_id", 1),
        ("MCCampaign", "Prod5bTest"),
        ("nsb", 1),
        ("type", "CtapipeProcessing"),
        ("version", software_version),
        ("output_extension", "DL2.h5"),
        (
            "options",
            "--config v3/dl0_to_dl2.yml --config v3/prod5b/subarray_north_alpha.yml",
        ),
        ("group_size", 1),
    ]
)

CTAPIPE_PROCESS_OUTPUT_METADATA = MetadataDict(
    [
        ("array_layout", "Alpha"),
        ("site", "LaPalma"),
        ("particle", "gamma-diffuse"),
        ("phiP", 180),
        ("thetaP", 20.0),
        ("sct", "False"),
        ("analysis_prog", "ctapipe-process"),
        ("analysis_prog_version", software_version),
        ("data_level", 2),
        ("outputType", "Data"),
        ("configuration_id", 1),
        ("MCCampaign", "Prod5bTest"),
    ]
)

MERGING1_METADATA = MetadataDict(
    [
        ("array_layout", "Alpha"),
        ("site", "LaPalma"),
        ("particle", "gamma-diffuse"),
        ("phiP", 180),
        ("thetaP", 20.0),
        ("sct", "False"),
        ("analysis_prog", "ctapipe-process"),
        ("analysis_prog_version", software_version),
        ("data_level", 2),
        ("outputType", "Data"),
        ("configuration_id", 1),
        ("MCCampaign", "Prod5bTest"),
        ("nsb", 1),
        ("type", "Merging"),
        ("version", software_version),
        ("group_size", 5),
        ("output_extension", "merged.DL2.h5"),
        ("merged", 0),
    ]
)
MERGING1_OUTPUT_METADATA = MetadataDict(
    [
        ("array_layout", "Alpha"),
        ("site", "LaPalma"),
        ("particle", "gamma-diffuse"),
        ("phiP", 180),
        ("thetaP", 20.0),
        ("sct", "False"),
        ("analysis_prog", "ctapipe-merge"),
        ("analysis_prog_version", software_version),
        ("data_level", 2),
        ("outputType", "Data"),
        ("configuration_id", 1),
        ("MCCampaign", "Prod5bTest"),
        ("merged", 1),
    ]
)

PRODUCTION_RESULTS = [
    {
        "ProductionID": 376,
        "ProductionName": "AF_ProdTest_nodiv",
        "Description": '{"Step1_MC_Simulation": {"stepID": 1678, "parentStep": []}, "Step2_Modeling_ctapipe": {"stepID": 1679, "parentStep": ["Step1_MC_Simulation"]}, "Step3_Merge": {"stepID": 1680, "parentStep": ["Step2_Modeling_ctapipe"]}}',
        "CreationDate": datetime.datetime(2023, 2, 8, 10, 45, 49),
        "LastUpdate": datetime.datetime(2023, 2, 8, 10, 45, 53),
        "AuthorDN": "/O=GRID-FR/C=FR/O=CNRS/OU=LUPM/CN=Alice Faure",
        "AuthorGroup": "cta_prod",
        "Status": "Active",
    },
    {
        "ProductionID": 377,
        "ProductionName": "AF_ProdTest_nodiv_2",
        "Description": '{"Step1_MC_Simulation": {"stepID": 1681, "parentStep": []}, "Step2_Modeling_ctapipe": {"stepID": 1682, "parentStep": ["Step1_MC_Simulation"]}, "Step3_Merge": {"stepID": 1683, "parentStep": ["Step2_Modeling_ctapipe"]}}',
        "CreationDate": datetime.datetime(2023, 2, 8, 10, 48, 2),
        "LastUpdate": datetime.datetime(2023, 2, 8, 10, 48, 5),
        "AuthorDN": "/O=GRID-FR/C=FR/O=CNRS/OU=LUPM/CN=Alice Faure",
        "AuthorGroup": "cta_prod",
        "Status": "Active",
    },
]  # noqa: F821
