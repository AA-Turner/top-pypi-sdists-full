from operator import attrgetter

import pytest


@pytest.mark.min_sf_ver("8.37.0")
def test_iter(notebooks, executable_notebook, temp_stage_case_sensitive):
    notebook_names = tuple(
        map(
            attrgetter("name"),
            notebooks.iter(),
        )
    )
    assert any(
        map(
            notebook_names.__contains__,
            (
                executable_notebook.name.upper(),  # for upper/lower case names
            ),
        )
    )


@pytest.mark.min_sf_ver("8.37.0")
def test_iter_like_with_from_name(notebooks, executable_notebook):
    notebook_names = tuple(
        map(
            attrgetter("name"),
            notebooks.iter(like="test_notebook%"),
        )
    )
    assert any(
        map(
            notebook_names.__contains__,
            (
                executable_notebook.name.upper(),  # for upper/lower case names
            ),
        )
    )
    notebook_def = executable_notebook.fetch()
    notebook_def.name += "_COPY"
    notebook_2 = notebooks.create(notebook_def)
    try:
        notebooks_from_name_limit = list(
            notebooks.iter(
                like=f"{notebook_def.name[:-5]}%",
                show_limit=1,
                from_name=notebook_def.name,
            )
        )
        assert tuple(map(attrgetter("name"), notebooks_from_name_limit)) == (notebook_def.name,)
    finally:
        notebook_2.drop()

