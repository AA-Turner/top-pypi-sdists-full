#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#


import pytest

from tests.utils import random_string

from snowflake.core.exceptions import NotFoundError
from snowflake.core.image_repository import ImageRepository


def test_drop(image_repositories):
    try:
        ir_name = random_string(5, "test_ir_")
        test_ir = ImageRepository(
            name=ir_name,
        )
        image_repositories.create(test_ir)
        image_repositories[test_ir.name].drop()
        with pytest.raises(
            NotFoundError,
        ):
            image_repositories[test_ir.name].fetch()

        # creating again, making sure it's not an issue
        image_repositories.create(test_ir)
        image_repositories[test_ir.name].drop()
    finally:
        image_repositories[test_ir.name].drop(if_exists=True)
