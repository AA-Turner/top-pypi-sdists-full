from snowflake.core.image_repository import ImageRepository


def test_fetch(image_repositories, temp_ir):
    ir: ImageRepository = image_repositories[temp_ir.name].fetch()
    assert ir.name == temp_ir.name.upper()  # for upper/lower case names
    assert ir.created_on
    assert ir.repository_url
    assert ir.owner
    assert ir.owner_role_type
