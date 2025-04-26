import pytest

from snowflake.core.exceptions import ConflictError


pytestmark = [pytest.mark.min_sf_ver("8.35.0")]


def test_create_pipe(pipes, template_pipe):
    try:
        pipe_resource = pipes.create(template_pipe)
        fetched_pipe = pipe_resource.fetch()
        assert fetched_pipe.name == template_pipe.name.upper()
        assert fetched_pipe.comment == template_pipe.comment

        # create pipe with the same name
        with pytest.raises(ConflictError):
            pipes.create(template_pipe)

        # create pipe with the same name but with if_not_exists
        pipes.create(template_pipe, mode="if_not_exists")

        # create pipe with the same name but with or_replace
        template_pipe.comment = "new comment"
        pipe_resource = pipes.create(template_pipe, mode="or_replace")
        fetched_pipe = pipe_resource.fetch()
        assert fetched_pipe.comment == template_pipe.comment

        # use the fetch to create with or_replace
        pipe_resource = pipes.create(fetched_pipe, mode="or_replace")

    finally:
        pipe_resource.drop(if_exists=True)
