import pytest

from snowflake.core.exceptions import NotFoundError
from snowflake.core.notebook import Notebook
from tests.utils import random_string


@pytest.mark.min_sf_ver("8.37.0")
def test_drop(notebooks):
    nb_name = random_string(5, "test_notebook_")
    test_nb = Notebook(
        name=nb_name,
    )
    notebooks.create(test_nb)
    notebooks[test_nb.name].drop()

    with pytest.raises(
        NotFoundError,
    ):
        notebooks[test_nb.name].fetch()

    # creating again, making sure it's not an issue
    notebooks.create(test_nb)
    notebooks[test_nb.name].drop()
