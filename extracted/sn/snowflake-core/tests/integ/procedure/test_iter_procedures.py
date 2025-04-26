
import pytest as pytest

from snowflake.core._common import CreateMode
from snowflake.core.procedure import (
    JavaScriptFunction,
    Procedure,
    ReturnDataType,
)
from tests.utils import random_string


@pytest.mark.min_sf_ver("8.38.0")
def test_iter(procedures):
    procs = []

    try:
        procedure_name_prefix = random_string(10, "test_procedure_")
        for i in range(5):
            proc_name = f"{procedure_name_prefix}_AProc_{i}"

            procedure = Procedure(
                name=proc_name,
                arguments=[],
                return_type=ReturnDataType(datatype="REAL"),
                language_config=JavaScriptFunction(),
                body="""return 3.14"""
            )
            proc = procedures.create(procedure, mode=CreateMode.or_replace)
            procs.append(proc)

        for i in range(3):
            proc_name = f"{procedure_name_prefix}_BProc_{i}"

            procedure = Procedure(
                name=proc_name,
                arguments=[],
                return_type=ReturnDataType(datatype="REAL"),
                language_config=JavaScriptFunction(),
                body="""return 3.14"""
            )
            proc = procedures.create(procedure, mode=CreateMode.or_replace)
            procs.append(proc)

        assert len([proc.name for proc in procedures.iter()]) >= 8
        assert len([proc.name for proc in procedures.iter(like="%APROC%")]) == 5
        assert len([proc.name for proc in procedures.iter(like="%BPROC%")]) == 3

    finally:
        for proc in procs:
            proc.drop()
