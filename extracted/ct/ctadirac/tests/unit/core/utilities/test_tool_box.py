from CTADIRAC.Core.Utilities.tool_box import (
    extract_run_number_from_chimp_mars,
    extract_run_number_from_corsika_sim_telarray,
    extract_run_number_from_ctapipe,
    extract_run_number_from_dl1_data_handler,
    extract_run_number_from_evndisplay,
    extract_run_number_from_image_extractor,
    extract_run_number_from_logs_tgz,
    extract_run_number_from_simpipe,
    run_number_from_filename,
)


def test_run_number_from_filename_logs_tgz():
    filename = "/path/to/file_000456.logs.tgz"
    package = "any_package"
    assert extract_run_number_from_logs_tgz(filename) == 456
    assert run_number_from_filename(filename, package) == 456


def test_run_number_from_filename_chimp():
    filename = "/path/to/run000456___cta.anything"
    package = "chimp"
    assert extract_run_number_from_chimp_mars(filename) == 456
    assert run_number_from_filename(filename, package) == 456


def test_run_number_from_filename_corsika_simhessarray():
    filename = "/path/to/run000456___cta.corsika.zst"
    package = "corsika_simhessarray"
    assert extract_run_number_from_corsika_sim_telarray(filename) == 456
    assert run_number_from_filename(filename, package) == 456


def test_run_number_from_filename_corsika_simtelarray():
    filename = (
        "/path/to/electron_40deg_0deg_run0000347___cta-prod6-2147m-"
        "Paranal-moon.simtel.zst"
    )
    package = "corsika_simtelarray"
    assert extract_run_number_from_corsika_sim_telarray(filename) == 347
    assert run_number_from_filename(filename, package) == 347


def test_run_number_from_filename_corsika_simtelarray_zero_padded():
    filename = (
        "/path/to/gamma_20deg_180deg_run2243___cta-prod5-paranal"
        "_desert-2147m-Paranal-dark_cone10.simtel.zst"
    )
    package = "corsika_simtelarray"
    assert extract_run_number_from_corsika_sim_telarray(filename) == 2243
    assert run_number_from_filename(filename, package) == 2243


def test_run_number_from_filename_corsika_simtelarray_tid():
    filename = "/path/to/file_tid000456.anything"
    package = "corsika_simtelarray"
    assert extract_run_number_from_corsika_sim_telarray(filename) == 456
    assert run_number_from_filename(filename, package) == 456


def test_run_number_from_filename_corsika_simtelarray_log():
    filename = "/path/to/run000456.log"
    package = "corsika_simtelarray"
    assert extract_run_number_from_corsika_sim_telarray(filename) == 456
    assert run_number_from_filename(filename, package) == 456


def test_run_number_from_filename_corsika_simtelarray_gz_log():
    filename = (
        "/path/to/proton_20deg_180deg_run17375___cta-prod5-paranal"
        "_desert-2147m-Paranal-dark.log.gz"
    )
    package = "corsika_simtelarray"
    assert extract_run_number_from_corsika_sim_telarray(filename) == 17375
    assert run_number_from_filename(filename, package) == 17375


def test_run_number_from_filename_corsika_log():
    filename = (
        "/path/to/run000900_gamma-diffuse_za20deg_azm0deg"
        "_cta-prod6-lapalma.corsika.log.gz"
    )
    package = "corsika_simtelarray"
    assert extract_run_number_from_corsika_sim_telarray(filename) == 900
    assert run_number_from_filename(filename, package) == 900


def test_run_number_from_filename_simpipe():
    filename = (
        "/path/to/gamma_run000004_za20deg_azm000deg_South_alpha_"
        "6.0.0_test_simpipe_wms_interface.zst"
    )
    package = "simpipe"
    assert extract_run_number_from_simpipe(filename) == 4
    assert run_number_from_filename(filename, package) == 4

    filename = (
        "/path/to/gamma_run000004_za20deg_azm000deg_South_alpha_"
        "6.1.0_test_simpipe_wms_interface.log_hist.tar.gz"
    )
    package = "simpipe"
    assert extract_run_number_from_simpipe(filename) == 4
    assert run_number_from_filename(filename, package) == 4


def test_run_number_from_filename_evndisplay_tid():
    filename = "/path/to/file_tid000456.anything"
    package = "evndisplay_dl1"
    assert extract_run_number_from_evndisplay(filename) == 456
    assert run_number_from_filename(filename, package) == 456


def test_run_number_from_filename_evndisplay_dl1_root():
    filename = "/path/to/run000456___cta.DL1.root"
    package = "evndisplay_dl1"
    assert extract_run_number_from_evndisplay(filename) == 456
    assert run_number_from_filename(filename, package) == 456


def test_run_number_from_filename_evndisplay_dl1_tar_gz():
    filename = "/path/to/run000456___cta.DL1.tar.gz"
    package = "evndisplay_dl1"
    assert extract_run_number_from_evndisplay(filename) == 456
    assert run_number_from_filename(filename, package) == 456


def test_run_number_from_filename_image_extractor():
    filename = "/path/to/srun000456-anything"
    package = "image_extractor"
    assert extract_run_number_from_image_extractor(filename) == 456
    assert run_number_from_filename(filename, package) == 456


def test_run_number_from_filename_dl1_data_handler():
    filename = "/path/to/runs000456-anything"
    package = "dl1_data_handler"
    assert extract_run_number_from_dl1_data_handler(filename) == 456
    assert run_number_from_filename(filename, package) == 456


def test_run_number_from_filename_ctapipe():
    filename = "/path/to/run000456___cta.anything"
    package = "ctapipe_dl1"
    assert extract_run_number_from_ctapipe(filename) == 456
    assert run_number_from_filename(filename, package) == 456


def test_run_number_from_filename_unknown_package():
    filename = "/path/to/000456-anything"
    package = "unknown_package"
    assert run_number_from_filename(filename, package) == -1
