import filecmp
import os.path
import tempfile

from pathlib import Path

import pytest

from snowflake.core.stage import Stage, StageDirectoryTable, StageEncryption
from tests.utils import random_string


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


@pytest.mark.skip_notebook
@pytest.mark.skip_storedproc
@pytest.mark.usefixtures("skip_for_snowflake_account")
def test_files(stages):
    comment = "my comment"
    new_stage = Stage(
        name=random_string(5, "test_stage_"),
        encryption=StageEncryption(type="SNOWFLAKE_SSE"),
        directory_table=StageDirectoryTable(enable=True),
        comment=comment,
    )
    try:
        s = stages.create(new_stage)
        assert s.fetch().comment == comment
        # upload file
        s.put(CURRENT_DIR + "/../../resources/schema.yaml", "/", auto_compress=False)
        s.put(Path(CURRENT_DIR + "/../../resources/testCSVheader.csv"), "/")

        # list file
        files = list(s.list_files())
        assert len(files) == 2, files
        assert {"schema.yaml", "testCSVheader.csv.gz"} == {f.name.split("/")[-1] for f in files}
        assert [2, 2] == [len(f.name.split("/")) for f in files]

        # download file
        temp_dir = tempfile.mkdtemp()
        s.get("/schema.yaml", temp_dir)
        s.get("/testCSVheader.csv.gz", Path(temp_dir))

        # compare files
        assert filecmp.cmp(CURRENT_DIR + "/../../resources/schema.yaml", os.path.join(temp_dir, "schema.yaml"))
        assert Path(os.path.join(temp_dir, "testCSVheader.csv.gz")).exists()
    finally:
        s.drop()


@pytest.mark.skip_notebook
@pytest.mark.skip_storedproc
@pytest.mark.usefixtures("skip_for_snowflake_account")
def test_files_legacy(stages):
    comment = "my comment"
    new_stage = Stage(
        name=random_string(5, "test_stage_"),
        encryption=StageEncryption(type="SNOWFLAKE_SSE"),
        directory_table=StageDirectoryTable(enable=True),
        comment=comment,
    )
    try:
        s = stages.create(new_stage)
        assert s.fetch().comment == comment
        # upload file
        s.upload_file(CURRENT_DIR + "/../../resources/schema.yaml", "/", auto_compress=False)

        # list file
        files = list(s.list_files())
        assert len(files) == 1, files
        assert "schema.yaml" in files[0].name
        assert 2 == len(files[0].name.split("/"))

        # download file
        temp_dir = tempfile.mkdtemp()
        s.download_file("/schema.yaml", temp_dir)

        # compare files
        assert filecmp.cmp(CURRENT_DIR + "/../../resources/schema.yaml", os.path.join(temp_dir, "schema.yaml"))
    finally:
        s.drop()
