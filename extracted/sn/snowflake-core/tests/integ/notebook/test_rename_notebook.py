import pytest

from snowflake.core.exceptions import NotFoundError
from snowflake.core.notebook import Notebook

from ..utils import random_string
from .conftest import notebook_file


@pytest.mark.min_sf_ver("8.37.0")
def test_rename(temp_db, notebooks, notebook_stage_with_file, warehouse):
    notebook_name = random_string(10, 'test_original_notebook')
    notebook_other_name = random_string(10, 'test_other_notebook')

    nb = notebooks.create(
        Notebook(
            name=notebook_name,
            query_warehouse=warehouse.name,
            from_location=f"@{notebook_stage_with_file.database.name}"
                            f".{notebook_stage_with_file.schema.name}."
                            f"{notebook_stage_with_file.name}",
            main_file=notebook_file,
        )
    )
    try:
        nb.rename(notebook_other_name)
        assert nb.fetch().name.upper() == notebook_other_name.upper()
        with pytest.raises(
            NotFoundError
        ):
            notebooks[notebook_name].fetch()
        nb.rename(nb.fetch().name, target_database=temp_db.name, target_schema="PUBLIC")
        final_def = nb.fetch()
        assert final_def.database_name.upper() == temp_db.name.upper()
        assert final_def.schema_name.upper() == "PUBLIC"
        assert final_def.name.upper() == notebook_other_name.upper()
    finally:
        nb.drop()
