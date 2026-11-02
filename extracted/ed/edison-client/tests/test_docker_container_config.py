import pytest
from pydantic import ValidationError

from edison_client.models.app import DockerContainerConfiguration


def test_tmp_size_default():
    config = DockerContainerConfiguration(cpu="1", memory="2Gi")
    assert config.tmp_size == "5Gi"


def test_tmp_size_custom():
    config = DockerContainerConfiguration(cpu="4", memory="8Gi", tmp_size="20Gi")
    assert config.tmp_size == "20Gi"


@pytest.mark.parametrize(
    ("tmp_size", "error_match"),
    [
        ("0Gi", "tmp_size must be at least 1Gi"),
        ("51Gi", "tmp_size must not exceed 50Gi"),
        ("5MB", "tmp_size must be in Gi format"),
        ("abc", "tmp_size must be in Gi format"),
    ],
)
def test_tmp_size_validation(tmp_size, error_match):
    with pytest.raises(ValidationError, match=error_match):
        DockerContainerConfiguration(cpu="4", memory="8Gi", tmp_size=tmp_size)
