from io import BytesIO
from textwrap import dedent

import pytest as pytest

from snowflake.core.notebook import Notebook
from snowflake.core.stage import Stage
from tests.integ.utils import random_string


notebook_file = "test_notebook.ipynb"


@pytest.fixture(scope="module")
def table_name_for_execute_notebook_test():
    # This returns a table name that is used in the notebook to create a table;
    # We then check the existence of the table to verify the notebook execution
    return random_string(5, "test_table_execute_notebook")


@pytest.fixture(scope="module")
def notebook_stage_with_file(session, stages, table_name_for_execute_notebook_test) -> Stage:
    stage_name = random_string(5, "test_notebook_stage_")
    stage = Stage(name=stage_name, kind="PERMANENT")

    notebook_st = stages.create(stage)

    try:
        file_path = f"@{notebook_st.name}/{notebook_file}"

        session.file.put_stream(
            BytesIO(
                dedent(f"""{{ 
 "metadata": {{ 
  "kernelspec": {{ 
   "display_name": "Streamlit Notebook", 
   "name": "streamlit" 
  }} 
 }}, 
 "nbformat_minor": 5, 
 "nbformat": 4, 
 "cells": [ 
  {{ 
   "cell_type": "code", 
   "id": "8d50cbf4-0c8d-4950-86cb-114990437ac9", 
   "metadata": {{ 
    "language": "sql", 
    "name": "cell1" 
   }}, 
   "source": "create table {table_name_for_execute_notebook_test}(a int)", 
   "execution_count": null, 
   "outputs": [] 
  }}
 ] 
}}
""").encode()  #noqa
            ),
            file_path,
            auto_compress=False
        )

        yield notebook_st
    finally:
        notebook_st.drop()


@pytest.fixture
def executable_notebook(set_internal_params, notebook_stage_with_file, notebooks, warehouse):
    notebook_name = random_string(5, "test_notebook_stage_")

    notebook = Notebook(name=notebook_name,
                        from_location=f"@{notebook_stage_with_file.database.name}"
                                      f".{notebook_stage_with_file.schema.name}."
                                      f"{notebook_stage_with_file.name}",
                        main_file=notebook_file,
                        query_warehouse=warehouse.name)

    nb = notebooks.create(notebook)

    with set_internal_params({"FEATURE_NOTEBOOKS_NON_INTERACTIVE_EXECUTION": "ENABLED"}):
        try:
            nb.add_live_version(from_last=True)
            yield nb
        finally:
            nb.drop()
