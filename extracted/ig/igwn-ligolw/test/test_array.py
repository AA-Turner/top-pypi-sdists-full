import numpy as np
import pytest

from igwn_ligolw import ligolw
from igwn_ligolw import utils as ligolw_utils

orig = np.arange(20**3, dtype=float).reshape((20, 20, 20))


@pytest.fixture
def filename(tmp_path):
    return str(tmp_path / "big_array.xml")


@pytest.fixture(params=["Text", "base64"])
def xmldoc(request):
    xmldoc = ligolw.Document()
    xmldoc.appendChild(ligolw.LIGO_LW()).appendChild(
        ligolw.Array.build("test", orig, encoding=request.param)
    )
    return xmldoc


def test_io_iteration_order(xmldoc, filename):
    ligolw_utils.write_filename(xmldoc, filename, compress="gz", with_mv=False)
    recov = ligolw.Array.get_array(ligolw_utils.load_filename(filename), "test").array
    np.testing.assert_array_equal(recov, orig)


def test_bench_write(xmldoc, filename, benchmark):
    benchmark(ligolw_utils.write_filename, xmldoc, filename)


def test_bench_read(xmldoc, filename, benchmark):
    ligolw_utils.write_filename(xmldoc, filename)
    benchmark(ligolw_utils.load_filename, filename)


def test_dtt():
    """Test reading Base64-encoded files from DTT."""
    xmldoc = ligolw_utils.load_filename("test/dtt.xml")

    array = (
        ligolw.LIGO_LW.get_ligo_lw(xmldoc, "Result[2]")
        .getElementsByTagName(ligolw.Array.tagName)[0]
        .array
    )
    np.testing.assert_array_equal(
        array,
        np.asarray(
            [
                1.000000000000000000e01,
                3.080070304870605469e01,
                9.486833190917968750e01,
                2.922011108398437500e02,
                9.000000000000000000e02,
                1.000000000000000000e00,
                1.000000000000000000e00,
                1.000000000000000000e00,
                1.000000000000000000e00,
                1.000000000000000000e00,
                9.999928474426269531e-01,
                9.999943375587463379e-01,
                9.999797940254211426e-01,
                9.999941587448120117e-01,
                9.999967813491821289e-01,
            ],
            dtype=np.float32,
        ),
    )

    array = (
        ligolw.LIGO_LW.get_ligo_lw(xmldoc, "Result[3]")
        .getElementsByTagName(ligolw.Array.tagName)[0]
        .array
    )
    np.testing.assert_array_equal(
        array,
        np.asarray(
            [
                1.000000000000000000e01,
                3.080070304870605469e01,
                9.486833190917968750e01,
                2.922011108398437500e02,
                9.000000000000000000e02,
                9.999928474426269531e-01,
                9.999943375587463379e-01,
                9.999797940254211426e-01,
                9.999941587448120117e-01,
                9.999967813491821289e-01,
                1.000000000000000000e00,
                1.000000000000000000e00,
                1.000000000000000000e00,
                1.000000000000000000e00,
                1.000000000000000000e00,
            ],
            dtype=np.float32,
        ),
    )
