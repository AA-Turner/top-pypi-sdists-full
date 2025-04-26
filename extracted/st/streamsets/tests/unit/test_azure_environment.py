# Copyright 2023 StreamSets Inc.

# fmt: off
import pytest

from streamsets.sdk.sch_models import AzureEnvironment

# fmt: on


def test_azure_environment_credential_type_setter_invalidates(azure_environment_json):
    azure_env = AzureEnvironment(azure_environment_json)
    with pytest.raises(Exception) as e:
        azure_env.credential_type = "Wouldn't work"
    assert str(e.value) == "Only valid value for the credential_type is Service Principal Client Secret"


def test_azure_environment_credential_type_setter_works(azure_environment_json):
    azure_env = AzureEnvironment(azure_environment_json)
    credential_type = "Service Principal Client Secret"
    assert azure_env.credential_type is None
    azure_env.credential_type = credential_type
    assert azure_env.credential_type == credential_type
