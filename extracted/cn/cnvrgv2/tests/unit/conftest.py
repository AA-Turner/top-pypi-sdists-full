import os
import pytest
from cnvrgv2 import Project
from cnvrgv2.cnvrg import Cnvrg
from cnvrgv2.context import Context


@pytest.fixture(scope="function")
def empty_context(mocker):
    # Test that the load_credentials function was called on empty input
    def mock_context_init(obj, *args, **kwargs):
        # Set the credentials variables:
        obj.token = "empty"
        obj.domain = "empty"
        obj.user = "empty"

        # Set context variables:
        obj.project = "empty"
        obj.experiment = "empty"
        obj.organization = "empty"
        obj.dataset = "empty"
        obj.datasource = "empty"
        obj.flow = "empty"
        obj.resource = "empty"
        obj.sso_version = None

    mocker.patch.object(Context, "__init__", mock_context_init)

    return Context()


@pytest.fixture(scope="function")
def empty_cnvrg(mocker, empty_context):
    def mock_cnvrg_init(obj, *args, **kwargs):
        obj._domain = "domain"
        obj._email = "test@email.com"
        obj._password = "password"
        obj._organization = "example-org"

    mocker.patch.object(Cnvrg, "__init__", mock_cnvrg_init)
    cnvrg = Cnvrg()
    cnvrg._context = empty_context

    return cnvrg


@pytest.fixture(scope="function")
def sample_netrc(request, mocker):
    fake_netrc_home = os.path.expanduser("~")

    def clear_netrc():
        os.remove(fake_netrc_home + "/.netrc")

    mocker.patch.dict(os.environ, {"HOME": fake_netrc_home}, clear=True)
    netrc_content = [
        "machine cnvrg.io",
        "  login test@test.com",
        "  password sample_token"
    ]
    with open(fake_netrc_home + "/.netrc", "w+") as f:
        f.writelines('\n'.join(netrc_content))

    os.chmod(fake_netrc_home + "/.netrc", 0o600)
    request.addfinalizer(clear_netrc)


@pytest.fixture(scope="function")
def empty_project(empty_context):
    return Project(context=empty_context)
