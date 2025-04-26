# Copyright Streamsets 2023

import copy
import logging

import pytest
from requests.exceptions import HTTPError

logger = logging.getLogger(__name__)


# Session scope because all tests run on the same organization
@pytest.fixture(scope="session")
def org_config(sch):
    org_config = sch.organizations.get(id=sch.organization).configuration

    original_config = copy.deepcopy(org_config)
    try:
        yield org_config
    finally:
        # reset org configs to the original config
        for key, value in original_config.items():
            # check to avoid making extra api calls
            if org_config[key] != value:
                try:
                    org_config[key] = value
                except HTTPError as e:
                    # certain keys for organizations cannot be updated on platform by the organization itself.
                    # we just catch and log these, in case something weird happened, and we want to debug.
                    logger.error("Failed to update key {} with error {}".format(key, e))


def test_update_org_config_fails_for_disabled_setting(org_config):
    KEY_THAT_CANNOT_BE_MODIFIED_BY_ORG_ADMIN = 'Maximum number of topology commits for the organization'
    with pytest.raises(HTTPError):
        org_config[KEY_THAT_CANNOT_BE_MODIFIED_BY_ORG_ADMIN] = 14
