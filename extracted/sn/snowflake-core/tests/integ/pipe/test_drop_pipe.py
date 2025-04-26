import pytest

from snowflake.core.exceptions import NotFoundError


pytestmark = [pytest.mark.min_sf_ver("8.35.0")]


def test_drop_pipe(pipes, template_pipe):
    try:
        pipe_resource = pipes.create(template_pipe)
        pipe_names = [pipe.name for pipe in pipes.iter(like="test_create_pipe_%")]
        assert template_pipe.name.upper() in pipe_names

        pipe_resource.drop()
        pipe_names = [pipe.name for pipe in pipes.iter(like="test_create_pipe_%")]
        assert len(pipe_names) == 0

        # drop the already dropped pipe
        with pytest.raises(NotFoundError):
            pipe_resource.drop()

        # drop the already dropped pipe with if_exists
        pipe_resource.drop(if_exists=True)
    finally:
        pipe_resource.drop(if_exists=True)
