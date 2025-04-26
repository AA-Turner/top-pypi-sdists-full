import os

import pytest

from snowflake.core.exceptions import ServerError


pytestmark = [pytest.mark.min_sf_ver("8.35.0")]

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


def test_refresh_pipe(pipes, template_pipe, temp_stage):
    try:
        temp_stage.upload_file(CURRENT_DIR + "/../../resources/schema.yaml", "/dir1", auto_compress=False)
        temp_stage.upload_file(CURRENT_DIR + "/../../resources/schema.yaml", "/dir1/dir2", auto_compress=False)
        pipe_resource = pipes.create(template_pipe)

        # refresh pipe in valid format
        pipe_resource.refresh(prefix="dir1/")

        # refresh pipe with non valid dir
        with pytest.raises(ServerError):
            pipe_resource.refresh(prefix="dir3/")
    finally:
        pipe_resource.drop(if_exists=True)
