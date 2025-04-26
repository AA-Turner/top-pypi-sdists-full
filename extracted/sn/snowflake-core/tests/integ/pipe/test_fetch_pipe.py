import pytest


pytestmark = [pytest.mark.min_sf_ver("8.35.0")]


def test_fetch_pipe(pipes, template_pipe):
    try:
        pipe_resource = pipes.create(template_pipe)
        fetched_pipe = pipe_resource.fetch()
        assert fetched_pipe.name == template_pipe.name.upper()
        assert fetched_pipe.comment == template_pipe.comment
        assert fetched_pipe.copy_statement == template_pipe.copy_statement
        assert not fetched_pipe.auto_ingest
        assert fetched_pipe.created_on is not None
        assert fetched_pipe.database_name is not None
        assert fetched_pipe.schema_name is not None
        assert fetched_pipe.owner is not None
        assert fetched_pipe.owner_role_type is not None

        # create pipe with the same name but with or_replace
        template_pipe.comment = "new comment"
        pipe_resource = pipes.create(template_pipe, mode="or_replace")
        fetched_pipe = pipe_resource.fetch()
        assert fetched_pipe.comment == template_pipe.comment
    finally:
        pipe_resource.drop(if_exists=True)
