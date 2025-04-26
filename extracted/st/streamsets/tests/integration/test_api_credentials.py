# Copyright Streamsets 2024
import copy
import time
from datetime import datetime

import pytest
from requests.exceptions import HTTPError

from streamsets.sdk import ControlHub
from streamsets.sdk.utils import get_random_string

TIME_TAKEN_TO_CHANGE_CREDENTIAL_STATE_SECONDS = 30


@pytest.fixture()
def sample_credentials(sch):
    builder = sch.get_api_credential_builder()

    # basically impossible to have 2 integration test runs on the same org at *exactly* the same time
    creds = builder.build('SDK Integration Test Credentials Run At ' + str(datetime.now()))
    sch.add_api_credential(creds)

    try:
        yield creds
    finally:
        sch.delete_api_credentials(creds)


def test_add_api_credential(sch):
    builder = sch.get_api_credential_builder()
    new_credentials = builder.build('SDK Integration Test Run At ' + str(datetime.now()))
    sch.add_api_credential(new_credentials)

    try:
        # when we add create and add credentials to Control Hub, these values are filled in
        assert new_credentials.credential_id is not None
        assert new_credentials.auth_token is not None

        # make a privileged call to control hub to verify it's working properly
        sch_with_new_creds = ControlHub(
            new_credentials.credential_id, new_credentials.auth_token, aster_url=sch._aster_url
        )

        assert sch_with_new_creds.organization == sch.organization

    finally:
        sch.delete_api_credentials(new_credentials)


def test_org_admin_can_create_api_credentials_for_other_users(sch, test_user):
    if 'org-admin' not in sch._roles:
        pytest.skip('Skipping the test as it needs to be run as an Org-Admin')

    current_organization = sch.organizations.get(id=sch.organization)
    if not current_organization.configuration['Enable service accounts.']:
        pytest.skip('Skipping the test as service accounts are not enabled for the organization.')

    builder = sch.get_api_credential_builder()
    new_credentials = builder.build(
        'SDK Integration Test Run At ' + str(datetime.now()), user_id=test_user.id
    )  # this lines creates the credentials for someone else
    sch.add_api_credential(new_credentials)

    try:
        # when we add create and add credentials to Control Hub, these values are filled in
        assert new_credentials.credential_id is not None
        assert new_credentials.auth_token is not None

        # ensure created_by and created_for are filled in correctly
        current_user = sch.api_client.get_current_user().response.json()
        assert new_credentials.created_for == test_user.id
        assert new_credentials.created_by == current_user['principalId']

        # make a privileged call to control hub to verify it's working properly
        sch_with_new_creds = ControlHub(
            new_credentials.credential_id, new_credentials.auth_token, aster_url=sch._aster_url
        )

        assert sch_with_new_creds.organization == sch.organization

        # verify that the current user is the one making the calls
        assert sch_with_new_creds.api_client.get_current_user().response.json()['email'] == test_user.email_address

    finally:
        sch.delete_api_credentials(new_credentials)


@pytest.mark.xfail(reason="Test is expected to fail until TASER-2764 is resolved.")
def test_delete_api_credentials(sch):
    builder = sch.get_api_credential_builder()
    new_credentials = builder.build('SDK Integration Test Run At ' + str(datetime.now()))
    sch.add_api_credential(new_credentials)

    # when we add create and add credentials to Control Hub, these values are filled in
    assert new_credentials.credential_id is not None
    assert new_credentials.auth_token is not None

    # make a privileged call to control hub to verify it's working properly
    sch_with_new_creds = ControlHub(new_credentials.credential_id, new_credentials.auth_token, aster_url=sch._aster_url)

    assert sch_with_new_creds.organization == sch.organization

    # now we can delete the credentials
    sch.delete_api_credentials(new_credentials)

    # we should not be able to see it anymore
    with pytest.raises(ValueError):
        sch.api_credentials.get(credential_id=new_credentials.credential_id)

    time.sleep(TIME_TAKEN_TO_CHANGE_CREDENTIAL_STATE_SECONDS)

    # new credentials should not work anymore
    with pytest.raises(HTTPError):
        _ = ControlHub(new_credentials.credential_id, new_credentials.auth_token, aster_url=sch._aster_url)


def test_rename_api_credentials(sch, sample_credentials):
    new_name = 'What a beautiful new name ^___________^ ' + get_random_string()

    sample_credentials.name = new_name
    sch.rename_api_credential(sample_credentials)

    sample_credentials = sch.api_credentials.get(credential_id=sample_credentials.credential_id)

    assert sample_credentials.name == new_name


@pytest.mark.xfail(reason="Test is expected to fail until TASER-2764 is resolved.")
def test_deactivate_api_credentials(sch, sample_credentials):
    sch_with_sample_credentials = ControlHub(
        sample_credentials.credential_id, sample_credentials.auth_token, aster_url=sch._aster_url
    )

    # verify it's active before deactivating
    assert sch_with_sample_credentials.pipelines is not None

    copied_credentials = copy.deepcopy(sample_credentials)
    sch.deactivate_api_credential(sample_credentials)
    time.sleep(TIME_TAKEN_TO_CHANGE_CREDENTIAL_STATE_SECONDS)

    assert sample_credentials.active is False

    with pytest.raises(HTTPError):
        _ = ControlHub(copied_credentials.credential_id, copied_credentials.auth_token, aster_url=sch._aster_url)


@pytest.mark.xfail(reason="Test is expected to fail until TASER-2764 is resolved.")
def test_activate_api_credentials(sch, sample_credentials):
    sch_with_sample_credentials = ControlHub(
        sample_credentials.credential_id, sample_credentials.auth_token, aster_url=sch._aster_url
    )

    # verify it's active before deactivating
    assert sch_with_sample_credentials.pipelines is not None

    copied_credentials = copy.deepcopy(sample_credentials)
    sch.deactivate_api_credential(sample_credentials)
    time.sleep(TIME_TAKEN_TO_CHANGE_CREDENTIAL_STATE_SECONDS)

    assert sample_credentials.active is False

    with pytest.raises(HTTPError):
        _ = ControlHub(copied_credentials.credential_id, copied_credentials.auth_token, aster_url=sch._aster_url)

    # now that we are sure it's deactivated, we can activate it again
    sch.activate_api_credential(sample_credentials)
    time.sleep(TIME_TAKEN_TO_CHANGE_CREDENTIAL_STATE_SECONDS)

    assert sample_credentials.active
    assert sch.pipelines is not None


def test_regenerate_auth_token_for_api_credentials(sch, sample_credentials):
    # when we get a credential object, we cannot access the auth token anymore
    # only when creating credentials can we see the auth token, after that they are gone forever
    credentials_with_no_auth_token = sch.api_credentials.get(credential_id=sample_credentials.credential_id)

    assert credentials_with_no_auth_token.auth_token is None

    sch.regenerate_api_credential_auth_token(credentials_with_no_auth_token)

    # check if it exists and is not equal to the old value
    assert credentials_with_no_auth_token.auth_token is not None
    assert credentials_with_no_auth_token.auth_token != sample_credentials.auth_token

    # check if it works
    sch_with_new_creds = ControlHub(
        credentials_with_no_auth_token.credential_id,
        credentials_with_no_auth_token.auth_token,
        aster_url=sch._aster_url,
    )

    assert sch_with_new_creds.pipelines is not None
