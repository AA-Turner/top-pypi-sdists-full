import airbyte_cloud_cli


def test_package_import() -> None:
    assert airbyte_cloud_cli.__name__ == "airbyte_cloud_cli"
