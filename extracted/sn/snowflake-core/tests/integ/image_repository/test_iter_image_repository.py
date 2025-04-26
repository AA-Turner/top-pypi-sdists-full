#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#


import pytest

from tests.utils import random_string

from snowflake.core.image_repository import ImageRepository


def test_iter(image_repositories):
    ir_names = []
    try:
        ir_name = random_string(5, "test_ir_1")
        ir_names += [ir_name]
        test_ir = ImageRepository(name=ir_name)
        image_repo_1 = image_repositories.create(test_ir)

        ir_name = random_string(5, "test_ir_2")
        ir_names += [ir_name]
        test_ir = ImageRepository(name=ir_name)
        image_repo_2 = image_repositories.create(test_ir)

        image_repo_names = [image_repo.name for image_repo in image_repositories.iter()]

        assert image_repo_1.name.upper() in image_repo_names
        assert image_repo_2.name.upper() in image_repo_names

        image_repo_names = [image_repo.name for image_repo in image_repositories.iter(like="TEst_Ir_%")]

        assert image_repo_1.name.upper() in image_repo_names
        assert image_repo_2.name.upper() in image_repo_names

        image_repo_names = [image_repo.name for image_repo in image_repositories.iter(like="TEst_Ir_2%")]

        assert image_repo_1.name.upper() not in image_repo_names
        assert image_repo_2.name.upper() in image_repo_names

        image_repo_names = [image_repo.name for image_repo in image_repositories.iter(like="TEst_Ir_3%")]

        assert image_repo_1.name.upper() not in image_repo_names
        assert image_repo_2.name.upper() not in image_repo_names

    finally:
        for ir_name in ir_names:
            image_repositories[ir_name].drop(if_exists=True)


@pytest.mark.skip(reason="SNOW-1555422")
def test_list_images(image_repositories):
    try:
        ir_name = random_string(5, "test_ir_3")
        test_ir = ImageRepository(name=ir_name)
        image_repo_1 = image_repositories.create(test_ir)

        images = image_repo_1.list_images_in_repository()

        assert len(list(images)) == 0
    finally:
        image_repo_1.drop(if_exists=True)
