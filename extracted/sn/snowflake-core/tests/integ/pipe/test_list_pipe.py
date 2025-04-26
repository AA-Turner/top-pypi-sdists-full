import pytest

from snowflake.core._internal.utils import normalize_and_unquote_name


pytestmark = [pytest.mark.min_sf_ver("8.35.0")]


def test_list_pipe(pipes, template_pipe, template_pipe_case_sensitive):
    try:
        pipe_resources = []
        pipe_resources += [pipes.create(template_pipe)]
        pipe_names = [pipe.name for pipe in pipes.iter()]
        assert template_pipe.name.upper() in pipe_names

        # check case sensitive pipe name
        pipe_resources += [pipes.create(template_pipe_case_sensitive)]
        pipe_names = [pipe.name for pipe in pipes.iter()]
        assert normalize_and_unquote_name(template_pipe_case_sensitive.name) in pipe_names
        assert template_pipe.name.upper() in pipe_names

        pipe_names = [pipe.name for pipe in pipes.iter(like="test_create_pipe_%")]
        pipe_names = [pipe.name for pipe in pipes.iter()]
        assert normalize_and_unquote_name(template_pipe_case_sensitive.name) in pipe_names
        assert template_pipe.name.upper() in pipe_names

        pipe_names = [pipe.name for pipe in pipes.iter(like="teST_create_pipe_%")]
        assert normalize_and_unquote_name(template_pipe_case_sensitive.name) in pipe_names
        assert template_pipe.name.upper() in pipe_names

        pipe_names = [pipe.name for pipe in pipes.iter(like="%RANDOM%")]
        assert len(pipe_names) == 0
    finally:
        for pipe_resource in pipe_resources:
            pipe_resource.drop(if_exists=True)
