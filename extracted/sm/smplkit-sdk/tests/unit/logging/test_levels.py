"""Tests for level mapping utilities."""

from smplkit.logging._levels import (
    PYTHON_TO_SMPL,
    SMPL_TO_PYTHON,
    python_level_to_smpl,
    smpl_level_to_python,
)


class TestPythonToSmpl:
    def test_trace(self):
        assert python_level_to_smpl(5) == "TRACE"

    def test_debug(self):
        assert python_level_to_smpl(10) == "DEBUG"

    def test_info(self):
        assert python_level_to_smpl(20) == "INFO"

    def test_warning(self):
        assert python_level_to_smpl(30) == "WARN"

    def test_error(self):
        assert python_level_to_smpl(40) == "ERROR"

    def test_critical(self):
        assert python_level_to_smpl(50) == "FATAL"

    def test_nonstandard_level_15(self):
        # Between DEBUG(10) and INFO(20), rounds down to DEBUG
        assert python_level_to_smpl(15) == "DEBUG"

    def test_nonstandard_level_25(self):
        # Between INFO(20) and WARN(30), rounds down to INFO
        assert python_level_to_smpl(25) == "INFO"

    def test_nonstandard_level_45(self):
        # Between ERROR(40) and FATAL(50), rounds down to ERROR
        assert python_level_to_smpl(45) == "ERROR"

    def test_below_trace(self):
        # Below TRACE(5), should still return TRACE
        assert python_level_to_smpl(1) == "TRACE"

    def test_above_fatal(self):
        # Above FATAL(50), rounds down to FATAL
        assert python_level_to_smpl(60) == "FATAL"

    def test_all_standard_mappings(self):
        for py_level, smpl_level in PYTHON_TO_SMPL.items():
            assert python_level_to_smpl(py_level) == smpl_level


class TestSmplToPython:
    def test_trace(self):
        assert smpl_level_to_python("TRACE") == 5

    def test_debug(self):
        assert smpl_level_to_python("DEBUG") == 10

    def test_info(self):
        assert smpl_level_to_python("INFO") == 20

    def test_warn(self):
        assert smpl_level_to_python("WARN") == 30

    def test_error(self):
        assert smpl_level_to_python("ERROR") == 40

    def test_fatal(self):
        assert smpl_level_to_python("FATAL") == 50

    def test_silent(self):
        assert smpl_level_to_python("SILENT") == 99

    def test_all_standard_mappings(self):
        for smpl_level, py_level in SMPL_TO_PYTHON.items():
            assert smpl_level_to_python(smpl_level) == py_level
