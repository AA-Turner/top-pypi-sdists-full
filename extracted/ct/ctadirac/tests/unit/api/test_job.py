from unittest.mock import MagicMock, call, mock_open, patch

import pytest
from ruamel.yaml import YAML

from CTADIRAC.Interfaces.API.CTAJob import (
    MetadataDict,
)
from CTADIRAC.Interfaces.API.CtapipeMergeJob import CtapipeMergeJob
from CTADIRAC.Interfaces.API.CtapipeProcessJob import CtapipeProcessJob
from CTADIRAC.Interfaces.API.MCPipeJob import MCPipeJob
from CTADIRAC.Interfaces.API.MCSimTelProcessJob import MCSimTelProcessJob
from CTADIRAC.Interfaces.API.SimPipeJob import SimPipeJob
from tests.unit.production import (
    COMMON_CONFIG,
    CTAPIPE_PROCESS_METADATA,
    CTAPIPE_PROCESS_OUTPUT_METADATA,
    MERGING1_METADATA,
    MERGING1_OUTPUT_METADATA,
    MERGING_CONFIG_1,
    PROCESSING_CONFIG,
    SIMPIPE_CONFIG,
    SIMPIPE_OUTPUT_METADATA,
    SIMULATION_CONFIG,
    SIMULATION_OUTPUT_METADATA,
)

yaml = YAML(typ="safe", pure=True)
software_version = "v0.19.2"
parents_list: list[int] = [1, 2, 3]

KEY_VALUE_STR = '{"key": "value"}'
TEMP_OUTPUT_DIRECTORY = "/output/directory"


def test_metadata_dict() -> None:
    metadata = MetadataDict()
    key = "unknown_key"
    error_message = f"Key '{key}' is not allowed in MetadataDict"
    with pytest.raises(KeyError) as exc_info:
        metadata[key] = "unknown"
    assert error_message in str(exc_info)


sim_job = MCPipeJob()
process_job = CtapipeProcessJob()
merge_job = CtapipeMergeJob()
sim_process_job = MCSimTelProcessJob()


def test_set_output_metadata() -> None:
    # Simulation Job:
    # Setting class variables 'as' done in WorkflowElement
    sim_job.particle = SIMULATION_CONFIG["job_config"]["particle"]
    sim_job.array_layout = SIMULATION_CONFIG["job_config"]["array_layout"]
    sim_job.site = SIMULATION_CONFIG["job_config"]["site"]
    sim_job.pointing_dir = SIMULATION_CONFIG["job_config"]["pointing_dir"]
    sim_job.version = SIMULATION_CONFIG["job_config"]["version"]
    sim_job.MCCampaign = COMMON_CONFIG["MCCampaign"]
    sim_job.configuration_id = COMMON_CONFIG["configuration_id"]
    assert sim_job.output_metadata == MetadataDict()
    sim_job.set_output_metadata(SIMULATION_OUTPUT_METADATA)
    assert sim_job.output_metadata == SIMULATION_OUTPUT_METADATA

    # Processing Job:
    # Setting class variables 'as' done in WorkflowElement
    process_job.particle = SIMULATION_CONFIG["job_config"]["particle"]
    process_job.array_layout = PROCESSING_CONFIG["job_config"]["array_layout"]
    process_job.site = SIMULATION_CONFIG["job_config"]["site"]
    process_job.pointing_dir = SIMULATION_CONFIG["job_config"]["pointing_dir"]
    process_job.version = PROCESSING_CONFIG["job_config"]["version"]
    process_job.MCCampaign = COMMON_CONFIG["MCCampaign"]
    process_job.configuration_id = COMMON_CONFIG["configuration_id"]

    assert process_job.output_metadata == MetadataDict()
    process_job.set_output_metadata(CTAPIPE_PROCESS_METADATA)
    assert process_job.output_metadata == CTAPIPE_PROCESS_OUTPUT_METADATA

    # Merging Job:
    # Setting class variables 'as' done in WorkflowElement
    merge_job.MCCampaign = COMMON_CONFIG["MCCampaign"]
    merge_job.version = MERGING_CONFIG_1["job_config"]["version"]

    assert merge_job.output_metadata == MetadataDict()
    merge_job.set_output_metadata(MERGING1_METADATA)
    assert merge_job.output_metadata == MERGING1_OUTPUT_METADATA


def test_set_site() -> None:
    sites = ["Paranal", "LaPalma"]
    for site in sites:
        sim_job.set_site(site)
        assert sim_job.site == site


def test_set_particle() -> None:
    particles = ["gamma", "gamma-diffuse", "electron", "proton", "helium"]
    for particle in particles:
        sim_job.set_particle(particle)
        assert sim_job.particle == particle


def test_set_pointing_dir() -> None:
    pointing_dirs: list[str] = ["North", "South", "East", "West"]
    for pointing in pointing_dirs:
        sim_job.set_pointing_dir(pointing)
        assert sim_job.pointing_dir == pointing


def test_set_moon() -> None:
    moon: list[str] = ["dark"]
    sim_job.set_moon(moon)
    assert sim_job.moon == ""
    assert sim_job.output_file_metadata["nsb"] == [1]

    moon = ["dark", "half"]
    sim_job.set_moon(moon)
    assert sim_job.moon == "--with-half-moon"
    assert sim_job.output_file_metadata["nsb"] == [1, 5]

    moon = ["dark", "half", "full"]
    sim_job.set_moon(moon)
    assert sim_job.moon == "--with-full-moon"
    assert sim_job.output_file_metadata["nsb"] == [1, 5, 19]

    moon: str = "dark"
    sim_process_job.set_moon(moon)
    assert sim_process_job.moon == ""
    assert sim_process_job.output_file_metadata["nsb"] == 1

    moon: str = "half"
    sim_process_job.set_moon(moon)
    assert sim_process_job.moon == "--with-half-moon"
    assert sim_process_job.output_file_metadata["nsb"] == 5

    moon: str = "full"
    sim_process_job.set_moon(moon)
    assert sim_process_job.moon == "--with-full-moon"
    assert sim_process_job.output_file_metadata["nsb"] == 19


def test_set_div_ang() -> None:
    div_ang = [
        "0.0098",
        "0.0075",
        "0.0089",
        "0.01568",
        "0.04568",
    ]
    with pytest.raises(SystemExit) as exc_info:
        sim_job.set_div_ang(div_ang)
    assert str(exc_info.value) == "-1"


def test_set_magic() -> None:
    sim_job.set_magic(True)
    assert sim_job.magic == "--with-magic"


def set_sct() -> None:
    sim_version = sim_job.version
    sim_job.set_sct(None)
    assert sim_job.sct == ""
    assert sim_job.version == sim_version

    sim_job.set_sct("all")
    assert sim_job.sct == "--with-all-scts"
    assert sim_job.version == sim_version + "-sc"

    sim_job.set_sct("non-alpha")
    assert sim_job.sct == "--with-sct"
    assert sim_job.version == sim_version + "-sc"


def test_set_output_metadata_simpipe():
    mock_file_content = """
    array_layout_name: Alpha
    site: North
    primary: gamma-diffuse
    zenith_angle: 20.0
    azimuth_angle: North
    model_version: 0.6.0
    """

    with patch("builtins.open", mock_open(read_data=mock_file_content)):
        simpipe_job = SimPipeJob()
        simpipe_job.set_simpipe_config("mock_config.yaml")

        simpipe_job.version = SIMPIPE_CONFIG["job_config"]["version"]
        simpipe_job.MCCampaign = COMMON_CONFIG["MCCampaign"]
        simpipe_job.configuration_id = COMMON_CONFIG["configuration_id"]

        metadata = MetadataDict(
            array_layout=simpipe_job.array_layout,
            site=simpipe_job.site,
            particle=simpipe_job.particle,
            phiP=float(round((float(simpipe_job.azimuth_angle) + 180) % 360, 2)),
            thetaP=float(simpipe_job.zenith_angle),
            sct="True" if simpipe_job.sct else "False",
            outputType=simpipe_job.output_type,
        )

        simpipe_job.set_output_metadata(metadata)

        expected_metadata = MetadataDict(
            array_layout=SIMPIPE_OUTPUT_METADATA["array_layout"],
            site=SIMPIPE_OUTPUT_METADATA["site"],
            particle=SIMPIPE_OUTPUT_METADATA["particle"],
            phiP=SIMPIPE_OUTPUT_METADATA["phiP"],
            thetaP=SIMPIPE_OUTPUT_METADATA["thetaP"],
            sct=SIMPIPE_OUTPUT_METADATA["sct"],
            tel_sim_prog=SIMPIPE_OUTPUT_METADATA["tel_sim_prog"],
            tel_sim_prog_version=SIMPIPE_OUTPUT_METADATA["tel_sim_prog_version"],
            data_level=SIMPIPE_OUTPUT_METADATA["data_level"],
            outputType=SIMPIPE_OUTPUT_METADATA["outputType"],
            configuration_id=SIMPIPE_OUTPUT_METADATA["configuration_id"],
            MCCampaign=SIMPIPE_OUTPUT_METADATA["MCCampaign"],
        )
        assert simpipe_job.output_metadata == expected_metadata


def test_build_file_metadata_with_propagate_run_number():
    simpipe_job = SimPipeJob()
    simpipe_job.run_number = "@{JOB_ID}"
    simpipe_job.run_number_offset = 10
    combination = {"key1": "value1", "key2": "value2"}
    result = simpipe_job.build_file_metadata(combination, propagate_run_number=True)

    # Assert that runNumber is included and equals the default run_number
    assert "runNumber" in result
    assert result["runNumber"] == "@{JOB_ID}"

    # Assert that combination keys and values are included
    assert result["key1"] == "value1"
    assert result["key2"] == "value2"


def test_build_file_metadata_without_propagate_run_number():
    simpipe_job = SimPipeJob()
    simpipe_job.run_number = "@{JOB_ID}"
    simpipe_job.run_number_offset = 10
    combination = {"key1": "value1", "key2": "value2"}
    result = simpipe_job.build_file_metadata(combination, propagate_run_number=False)

    # Assert that runNumber is not included
    assert "runNumber" not in result

    # Assert that combination keys and values are included
    assert result["key1"] == "value1"
    assert result["key2"] == "value2"


def test_build_file_metadata_with_custom_run_number():
    simpipe_job = SimPipeJob()
    simpipe_job.run_number = 1000
    simpipe_job.run_number_offset = 10
    combination = {"key1": "value1"}
    result = simpipe_job.build_file_metadata(combination, propagate_run_number=True)

    # Assert that runNumber includes the offset
    assert "runNumber" in result
    assert result["runNumber"] == 1010  # 1000 + offset (10)

    # Assert that combination keys and values are included
    assert result["key1"] == "value1"


@patch("CTADIRAC.Interfaces.API.SimPipeJob.json.dumps")
@patch("CTADIRAC.Interfaces.API.SimPipeJob.SimPipeJob.setExecutable")
def test_run_simpipe(mock_set_executable, mock_json_dumps):
    job = SimPipeJob()
    job.simpipe_config_options = {"key": "value"}
    job.run_number_offset = 10
    job.run_number = 12345
    mock_json_dumps.return_value = KEY_VALUE_STR

    mock_set_executable.return_value = {
        "Value": {
            "name": "Step_SimPipe",
            "descr_short": "Run SimPipe simulation step",
        }
    }

    job.run_simpipe()

    mock_set_executable.assert_called_once_with(
        "dirac_simpipe_simulate_prod_wrapper",
        arguments='10 12345 \'{"key": "value"}\'',
        logFile="SimPipe_Log.txt",
        modulesList=["cta_script"],
    )
    step = mock_set_executable.return_value
    assert step["Value"]["name"] == "Step_SimPipe"
    assert step["Value"]["descr_short"] == "Run SimPipe simulation step"


def test_set_array_layout_without_scts():
    """Test _set_array_layout when the value does not contain '_scts'."""
    simpipe_job = SimPipeJob()
    simpipe_job._set_array_layout("array_layout_standard")
    assert simpipe_job.array_layout == "array_layout_standard"
    assert not simpipe_job.sct


def test_set_array_layout_with_scts():
    """Test _set_array_layout when the value contains '_scts'."""
    simpipe_job = SimPipeJob()
    simpipe_job._set_array_layout("array_layout_scts")
    assert simpipe_job.array_layout == "array_layout_scts"
    assert simpipe_job.sct


def test_set_site_north():
    """Test _set_site with value 'North'."""
    simpipe_job = SimPipeJob()
    simpipe_job._set_site("North")
    assert simpipe_job.site == "LaPalma"


def test_set_site_south():
    """Test _set_site with value 'South'."""
    simpipe_job = SimPipeJob()
    simpipe_job._set_site("South")
    assert simpipe_job.site == "Paranal"


def test_set_site_invalid():
    """Test _set_site with an invalid value."""
    simpipe_job = SimPipeJob()

    with pytest.raises(SystemExit) as exc_info:
        simpipe_job._set_site("InvalidSite")
    assert str(exc_info.value) == "-1"


def test_azimuth_angle_not_set():
    """Test azimuth_angle property when _azimuth_angle is not set."""
    simpipe_job = SimPipeJob()

    with pytest.raises(SystemExit) as exc_info:
        _ = simpipe_job.azimuth_angle
    assert str(exc_info.value) == "-1"


def test_azimuth_angle_set():
    """Test azimuth_angle property when _azimuth_angle is set."""
    simpipe_job = SimPipeJob()
    simpipe_job._azimuth_angle = 45.0
    assert simpipe_job.azimuth_angle == 45.0


def test_azimuth_angle_set_valid_float():
    """Test azimuth_angle setter with a valid float value."""
    simpipe_job = SimPipeJob()
    simpipe_job.azimuth_angle = 90.0
    assert simpipe_job._azimuth_angle == 90.0


def test_azimuth_angle_set_valid_direction():
    """Test azimuth_angle setter with a valid direction string."""
    simpipe_job = SimPipeJob()
    simpipe_job.azimuth_angle = "north"
    assert simpipe_job._azimuth_angle == 0


def test_azimuth_angle_set_invalid_direction():
    """Test azimuth_angle setter with an invalid direction string."""
    simpipe_job = SimPipeJob()

    with pytest.raises(SystemExit) as exc_info:
        simpipe_job.azimuth_angle = "invalid_direction"
    assert str(exc_info.value) == "-1"


def test_set_simulation_software_corsika():
    """Test _set_simulation_software with value 'corsika'."""
    simpipe_job = SimPipeJob()
    simpipe_job._set_simulation_software("corsika")
    assert simpipe_job.only_corsika
    assert simpipe_job.program_category == "airshower_sim"
    assert simpipe_job.prog_name == "corsika"


def test_set_simulation_software_invalid():
    """Test _set_simulation_software with an invalid value."""
    simpipe_job = SimPipeJob()
    simpipe_job._set_simulation_software("invalid_software")
    assert not simpipe_job.only_corsika
    assert simpipe_job.program_category == "tel_sim"
    assert simpipe_job.prog_name == "simpipe"


@patch("CTADIRAC.Interfaces.API.SimPipeJob.SimPipeJob.setExecutable")
def test_upload_and_register_data_file(mock_set_executable):
    """Test upload_and_register_data_file with valid inputs."""
    simpipe_job = SimPipeJob()
    simpipe_job.output_data_type = "DataType"
    simpipe_job.package = "simpipe"
    simpipe_job.program_category = "tel_sim"
    simpipe_job.catalogs = "catalog"

    meta_data_json = KEY_VALUE_STR
    file_meta_data_json = '{"file_key": "file_value"}'
    data_output_pattern = "/output/pattern/*"
    log_str = "test"

    mock_set_executable.return_value = {
        "Value": {
            "name": "Step_DataManagement",
            "descr_short": "Save data files to SE and register them in DFC",
        }
    }

    simpipe_job.upload_and_register_data_file(
        meta_data_json, file_meta_data_json, data_output_pattern, log_str
    )

    mock_set_executable.assert_called_once_with(
        "cta-prod-managedata",
        arguments=(
            f"'{meta_data_json}' '{file_meta_data_json}' "
            f"{simpipe_job.base_path} '{data_output_pattern}' "
            f"{simpipe_job.package} {simpipe_job.program_category} "
            f"'{simpipe_job.catalogs}' {simpipe_job.output_data_type}"
        ),
        logFile=f"DataManagement_{log_str}_Log.txt",
    )
    step = mock_set_executable.return_value
    assert step["Value"]["name"] == "Step_DataManagement"
    assert (
        step["Value"]["descr_short"] == "Save data files to SE and register them in DFC"
    )


@patch("CTADIRAC.Interfaces.API.SimPipeJob.SimPipeJob.setExecutable")
def test_upload_and_register_log_file(mock_set_executable):
    """Test upload_and_register_data_file with valid inputs."""
    simpipe_job = SimPipeJob()
    simpipe_job.output_data_type = "Log"
    simpipe_job.package = "simpipe"
    simpipe_job.program_category = "tel_sim"
    simpipe_job.catalogs = "catalog"

    meta_data_json = KEY_VALUE_STR
    file_meta_data_json = '{"file_key": "file_value"}'
    log_file_pattern = "/output/pattern/*"
    log_str = "test"

    mock_set_executable.return_value = {
        "Value": {
            "name": "Step_LogManagement",
            "descr_short": "Save log to SE and register them in DFC",
        }
    }

    simpipe_job.upload_and_register_log(
        meta_data_json, file_meta_data_json, log_file_pattern, log_str
    )

    mock_set_executable.assert_called_once_with(
        "cta-prod-managedata",
        arguments=(
            f"'{meta_data_json}' '{file_meta_data_json}' "
            f"{simpipe_job.base_path} '{log_file_pattern}' "
            f"{simpipe_job.package} {simpipe_job.program_category} "
            f"'{simpipe_job.catalogs}' {simpipe_job.output_data_type}"
        ),
        logFile=f"LogManagement_{log_str}_Log.txt",
    )
    step = mock_set_executable.return_value
    assert step["Value"]["name"] == "Step_LogManagement"
    assert step["Value"]["descr_short"] == "Save log to SE and register them in DFC"


def test_run_dedicated_software_calls_run_simpipe():
    """Test run_dedicated_software to ensure it calls run_simpipe."""
    simpipe_job = SimPipeJob()

    # Mock the run_simpipe method
    simpipe_job.run_simpipe = lambda: setattr(simpipe_job, "run_simpipe_called", True)
    simpipe_job.run_simpipe_called = False

    simpipe_job.run_dedicated_software()

    assert (
        simpipe_job.run_simpipe_called
    ), "run_simpipe was not called by run_dedicated_software"


def test_run_dedicated_software_no_side_effects():
    """Test run_dedicated_software to ensure no unexpected side effects."""
    simpipe_job = SimPipeJob()

    # Mock the run_simpipe method
    simpipe_job.run_simpipe = lambda: None

    # Capture initial state
    initial_state = simpipe_job.__dict__.copy()

    simpipe_job.run_dedicated_software()

    # Ensure no state changes occurred
    assert (
        simpipe_job.__dict__ == initial_state
    ), "Unexpected side effects in run_dedicated_software"


def test_set_metadata_and_register_data():
    """Test for set_metadata_and_register_data with valid inputs."""
    simpipe_job = SimPipeJob()
    simpipe_job.output_metadata = {"key": "value"}
    simpipe_job.model_version = ["v1", "v2"]
    simpipe_job.output_directory = TEMP_OUTPUT_DIRECTORY
    simpipe_job.only_corsika = False

    simpipe_job.build_file_metadata = MagicMock(return_value={"runNumber": "1234"})
    simpipe_job.upload_and_register_data_file = MagicMock()
    simpipe_job.upload_and_register_log = MagicMock()

    simpipe_job.set_metadata_and_register_data()

    expected_calls = [
        call({"model_version": "v1"}, True),
        call({"model_version": "v2"}, True),
    ]
    simpipe_job.build_file_metadata.assert_has_calls(expected_calls, any_order=False)

    assert simpipe_job.upload_and_register_data_file.call_count == 2
    assert simpipe_job.upload_and_register_log.call_count == 2


def test_set_metadata_and_register_data_with_corsika():
    """Test for set_metadata_and_register_data when only_corsika is True."""
    simpipe_job = SimPipeJob()
    simpipe_job.output_metadata = {"key": "value"}
    simpipe_job.model_version = ["v1"]
    simpipe_job.output_directory = TEMP_OUTPUT_DIRECTORY
    simpipe_job.only_corsika = True

    simpipe_job.build_file_metadata = MagicMock(return_value={"runNumber": "1234"})
    simpipe_job.upload_and_register_data_file = MagicMock()
    simpipe_job.upload_and_register_log = MagicMock()

    simpipe_job.set_metadata_and_register_data()

    expected_calls = [
        call({"model_version": "v1"}, True),
    ]
    simpipe_job.build_file_metadata.assert_has_calls(expected_calls, any_order=False)

    simpipe_job.upload_and_register_data_file.assert_called_once()
    simpipe_job.upload_and_register_log.assert_called_once()


def test_set_metadata_and_register_data_empty_model_version():
    """Test for set_metadata_and_register_data with an empty model_version list."""
    simpipe_job = SimPipeJob()
    simpipe_job.output_metadata = {"key": "value"}
    simpipe_job.model_version = []  # Empty model_version
    simpipe_job.output_directory = TEMP_OUTPUT_DIRECTORY
    simpipe_job.only_corsika = False

    simpipe_job.build_file_metadata = MagicMock()
    simpipe_job.upload_and_register_data_file = MagicMock()
    simpipe_job.upload_and_register_log = MagicMock()

    simpipe_job.set_metadata_and_register_data()

    simpipe_job.build_file_metadata.assert_not_called()
    simpipe_job.upload_and_register_data_file.assert_not_called()
    simpipe_job.upload_and_register_log.assert_not_called()


def test_set_systematic_uncertainty_to_test() -> None:
    systematic_uncertainty_to_test: str = "LaPalma/clouds/ID1"
    sim_process_job.set_systematic_uncertainty_to_test(systematic_uncertainty_to_test)
    assert (
        sim_process_job.systematic_uncertainty_to_test == systematic_uncertainty_to_test
    )


def test_run_sim_telarray(mocker):
    systematic_uncertainty_to_test: str = "LaPalma/clouds/ID1"
    sim_process_job.set_systematic_uncertainty_to_test(systematic_uncertainty_to_test)

    mock_step = {"Value": {"name": "", "descr_short": ""}}
    mock_set_exec = mocker.patch.object(
        sim_process_job, "setExecutable", return_value=mock_step
    )

    sim_process_job.run_sim_telarray(debug=False)

    mock_set_exec.assert_called_once_with(
        "./dirac_sim_telarray_process",
        arguments="LaPalma/clouds/ID1",
        logFile="Simtel_Log.txt",
    )

    assert mock_step["Value"]["name"] == "Step_Simtel"
    assert (
        mock_step["Value"]["descr_short"]
        == "Run sim_telarray processing of CORSIKA file"
    )
