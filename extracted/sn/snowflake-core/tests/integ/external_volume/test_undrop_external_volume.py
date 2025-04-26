import pytest

from snowflake.core.exceptions import APIError, ConflictError
from tests.integ.external_volume.utils import get_aws_external_volume_template


pytestmark = [pytest.mark.internal_only]


def test_undrop_external_volume(external_volumes, setup_credentials_fixture):
    try:
        external_volume_to_drop = []
        # happy path aws
        external_volume = get_aws_external_volume_template()
        external_volume_handler = external_volumes.create(external_volume)
        external_volume_to_drop += [external_volume_handler]

        # happy drop
        external_volume_handler.drop()

        # happy undrop
        external_volume_handler.undrop()

        # undrop when it is not dropped
        with pytest.raises(ConflictError):
            external_volume_handler.undrop()

        # undrop random external volume
        with pytest.raises(APIError):
            external_volumes["RANDOM"].undrop()

    finally:
        for external_volume_handler in external_volume_to_drop:
            external_volume_handler.drop(if_exists=True)
