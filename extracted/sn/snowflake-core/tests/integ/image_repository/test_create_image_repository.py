#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#


import pytest

from tests.utils import random_string

from snowflake.core._common import CreateMode
from snowflake.core.exceptions import APIError, ConflictError
from snowflake.core.image_repository import ImageRepository


def test_create(image_repositories):
    ir_names = []
    try:
        ir_name = random_string(5, "test_ir_")
        ir_names += [ir_name]
        test_ir = ImageRepository(name=ir_name)
        image_repo = image_repositories.create(test_ir)
        ir = image_repo.fetch()
        assert ir.name == ir_name.upper()
        image_repo.drop()

        ir_name = random_string(5, "test_ir_")
        ir_names += [ir_name]
        ir_name = f'"{ir_name}"'
        test_ir = ImageRepository(name=ir_name)
        # image repository with case sensitive names is not supported
        with pytest.raises(APIError):
            image_repo = image_repositories.create(test_ir)

        ir_name = random_string(5, "test_ir_")
        ir_names += [ir_name]
        test_ir = ImageRepository(
            name=ir_name,
        )
        image_repo = image_repositories.create(test_ir)

        # create an already existing image repository with errorifExists
        with pytest.raises(ConflictError):
            image_repo = image_repositories.create(test_ir)

        # create an already existing image repository with ifNotExists
        image_repo = image_repositories.create(test_ir, mode=CreateMode.if_not_exists)
        # create when we do or replace
        image_repo = image_repositories.create(test_ir, mode=CreateMode.or_replace)

        # create from fetch
        fetched_ir = image_repo.fetch()
        image_repositories.create(fetched_ir, mode=CreateMode.or_replace)

    finally:
        for ir_name in ir_names:
            image_repositories[ir_name].drop(if_exists=True)
