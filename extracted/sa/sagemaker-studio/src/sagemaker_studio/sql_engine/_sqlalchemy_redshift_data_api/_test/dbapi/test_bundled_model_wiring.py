"""
Unit tests for the bundled redshift-data service model and the loader wiring that
points the driver's client at it.

Feature: remove-redshift-data-api-query-timeout

This is the only file in the driver suite that reads the real bundled service model and
exercises the real client-construction path. Everywhere else -- `test_cursor.py`,
`test_error_handling.py` -- the client is a `Mock` and the service model is stubbed, on
purpose: Requirement 11.8 says the polling suite must pass whatever the resolved model
declares. These cases are the deliberate exception, because what the resolved model
declares is exactly what they are about.

No AWS call is made. A botocore service model can be inspected without one, and
`_validate_connection` is patched out so the `list_databases` probe never fires.

Why this file has to exist at all: a missing `package_data` entry or a wiring that does
not engage both degrade *silently* to classic polling. The capability check fails open
by design (Requirement 12.8), so neither failure raises, neither warns, and every other
test in the suite stays green -- in a source checkout the model file is on disk whether
or not it is packaged. The Property 18 cases below are the only check in the suite that
goes red when the wiring breaks.

The correctness properties realized here are specified as property-based, but the
package declares only pytest and carries no property-testing dependency,
so they are realized as parameterized pytest cases over tables of inputs -- matching
how the rest of this suite is written.
"""

import contextlib
import json
import os
from unittest.mock import Mock, patch

import boto3
import botocore
import pytest
from botocore.loaders import Loader

from ...dbapi import client as client_module
from ...dbapi.client import _BUNDLED_MODELS_PATH, RedshiftDataAPIClient
from ...dbapi.connection import Connection
from ...dbapi.connection_params import ConnectionParams
from ...dbapi.cursor import StatementExecutor
from ...dbapi.exceptions import InterfaceError

# ---------------------------------------------------------------------------
# Coordinates of the bundled model, written as literals rather than imported from the
# driver. Importing the names would make these cases agree with whatever the module
# happens to say; the point is to pin what the design fixes: the member botocore's own
# model omits, the shape it belongs to, and the API version the loader looks for under
# <search path>/<service>/<apiVersion>/service-2.json.
# ---------------------------------------------------------------------------

_LONG_POLL_MEMBER = "WaitTimeSeconds"
_DESCRIBE_REQUEST_SHAPE = "DescribeStatementRequest"
_SERVICE_NAME = "redshift-data"
_API_VERSION = "2019-12-20"
_MODEL_TYPE_NAME = "service-2"
_MODEL_FILE_NAME = f"{_MODEL_TYPE_NAME}.json"

# The wait a long-poll request carries. See the same note in test_cursor.py: the design
# adapted CR-311220612's min(30, remaining timeout) to the constant service maximum,
# because this change removes the client-side timeout there is no term to clamp against.
_EXPECTED_WAIT_SECONDS = 30

# The shipped model file, located through the same module constant the wiring hands to
# botocore's loader. Deriving it from `_BUNDLED_MODELS_PATH` rather than from this test
# file's own location is deliberate: it ties the file these cases read to the directory
# the driver actually searches, so a model that exists but sits where the driver will
# never look fails Property 17 rather than passing it.
_BUNDLED_MODEL_FILE = os.path.join(
    _BUNDLED_MODELS_PATH, _SERVICE_NAME, _API_VERSION, _MODEL_FILE_NAME
)

# botocore's own data directory, the one the bundled path has to outrank.
_BOTOCORE_DATA_PATH = os.path.join(os.path.dirname(botocore.__file__), "data")

_SETUP_PY = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", "..", "setup.py")
)


def _botocore_model_declares_the_member():
    """
    Whether the installed botocore's own redshift-data model declares the long-poll
    member.

    Measured at import time. It is read rather than assumed because two kinds of
    assertion below are only observable while it stays false: that the bundled model is
    what *supplies* the member, and that a client whose wiring failed polls in classic
    mode. Where botocore ships the member itself, those cases cannot tell the bundled
    model apart from botocore's own and are skipped rather than left to fail for an
    environmental reason.

    The model is resolved through botocore's own loader, restricted to botocore's data
    directory, rather than by opening a file name this test picks. botocore ships the
    model in more than one form -- `service-2.json` in some distributions and a gzipped
    `service-2.json.gz` in others -- so reading a fixed uncompressed name reports "omits
    the member" for any distribution that gzips it, whatever the model inside actually
    declares. That is a false negative in the unsafe direction: it suppresses the skip,
    and the guarded cases then fail against a botocore that supplies the member on its
    own. Asking the loader resolves whichever form is present, which is also the form
    the driver's client will resolve at runtime.
    """
    try:
        model = Loader(
            extra_search_paths=[_BOTOCORE_DATA_PATH],
            include_default_search_paths=False,
        ).load_service_model(_SERVICE_NAME, _MODEL_TYPE_NAME, _API_VERSION)
    except Exception:
        return False
    return _LONG_POLL_MEMBER in model.get("shapes", {}).get(_DESCRIBE_REQUEST_SHAPE, {}).get(
        "members", {}
    )


_BOTOCORE_OMITS_THE_MEMBER = not _botocore_model_declares_the_member()

_requires_botocore_without_the_member = pytest.mark.skipif(
    not _BOTOCORE_OMITS_THE_MEMBER,
    reason=(
        f"the installed botocore's own {_SERVICE_NAME} model declares {_LONG_POLL_MEMBER}, "
        "so an unwired client would long-poll on botocore's model and the bundled model "
        "cannot be told apart from it"
    ),
)


# ---------------------------------------------------------------------------
# Connection parameters and credential sources.
# ---------------------------------------------------------------------------

_BASE_PARAMS = {
    "cluster_identifier": "test-cluster",
    "database_name": "test_db",
    "db_user": "test_user",
    "region": "us-east-1",
}

_EXPLICIT_KEY = "AKIAIOSFODNN7EXAMPLE"
_EXPLICIT_SECRET = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
_PROFILE_NAME = "test-profile"
_PROFILE_KEY = "AKIAPROFILEEXAMPLE12"
_PROFILE_SECRET = "profilesecretprofilesecret"
_PROVIDER_KEY = "ASIAPROVIDEREXAMPLE1"
_PROVIDER_SECRET = "providersecretprovidersecret"
_CHAIN_KEY = "AKIADEFAULTCHAIN1234"
_CHAIN_SECRET = "defaultchainsecretdefaultchain"

# The four credential sources _create_boto3_session supports, in the order it tests
# them. The fresh-botocore-session pattern Requirement 12.6 forbids would break each of
# these differently, which is why the wiring mutates the loader already attached to the
# session instead; these labels drive the cases that hold it to that.
_CREDENTIAL_SOURCES = [
    "credential_provider",
    "named_profile",
    "explicit_keys",
    "default_chain",
]


def _stub_credential_provider():
    """A refreshable credential provider returning fixed keys and a far-future expiry."""
    return {
        "access_key_id": _PROVIDER_KEY,
        "secret_access_key": _PROVIDER_SECRET,
        "session_token": "provider-session-token",
        "expiration": "2999-01-01T00:00:00Z",
    }


def _credential_source_setup(label, monkeypatch, tmp_path):
    """
    Prepare the environment one credential source reads and return
    (ConnectionParams overrides, the access key that source should resolve to).
    """
    if label == "credential_provider":
        return {"credential_provider": _stub_credential_provider}, _PROVIDER_KEY

    if label == "named_profile":
        credentials_file = tmp_path / "profile-credentials"
        credentials_file.write_text(
            f"[{_PROFILE_NAME}]\n"
            f"aws_access_key_id = {_PROFILE_KEY}\n"
            f"aws_secret_access_key = {_PROFILE_SECRET}\n",
            encoding="utf-8",
        )
        monkeypatch.setenv("AWS_SHARED_CREDENTIALS_FILE", str(credentials_file))
        return {"profile_name": _PROFILE_NAME}, _PROFILE_KEY

    if label == "explicit_keys":
        return {
            "aws_access_key_id": _EXPLICIT_KEY,
            "aws_secret_access_key": _EXPLICIT_SECRET,
        }, _EXPLICIT_KEY

    if label == "default_chain":
        monkeypatch.setenv("AWS_ACCESS_KEY_ID", _CHAIN_KEY)
        monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", _CHAIN_SECRET)
        return {}, _CHAIN_KEY

    raise AssertionError(f"unknown credential source: {label!r}")


@pytest.fixture(autouse=True)
def isolated_aws_environment(monkeypatch, tmp_path):
    """
    Strip the AWS environment these cases must not inherit.

    `AWS_DATA_PATH` is cleared because Requirement 12.3 is precisely that the driver
    needs no environment variable set beforehand by another component; leaving an
    inherited value in place would let a developer's shell supply the bundled model and
    the wiring could be entirely broken without a single case failing. The credentials
    and config files are pointed at empty temporary files so the default-chain and
    named-profile cases read what the test wrote rather than what the developer's
    ~/.aws happens to hold. The two driver env overrides are cleared so the region and
    endpoint assertions read the connection parameters.
    """
    for variable in (
        "AWS_DATA_PATH",
        "AWS_PROFILE",
        "AWS_DEFAULT_PROFILE",
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY",
        "AWS_SESSION_TOKEN",
        client_module.REDSHIFT_DATA_REGION_ENV_VAR,
        client_module.REDSHIFT_DATA_ENDPOINT_URL_ENV_VAR,
    ):
        monkeypatch.delenv(variable, raising=False)

    empty_credentials = tmp_path / "empty-credentials"
    empty_credentials.write_text("", encoding="utf-8")
    empty_config = tmp_path / "empty-config"
    empty_config.write_text("", encoding="utf-8")
    monkeypatch.setenv("AWS_SHARED_CREDENTIALS_FILE", str(empty_credentials))
    monkeypatch.setenv("AWS_CONFIG_FILE", str(empty_config))


# ---------------------------------------------------------------------------
# Helpers shared by the wiring cases.
# ---------------------------------------------------------------------------


def _build_driver_client(**param_overrides):
    """
    Build a real RedshiftDataAPIClient through the real `_initialize_client` path.

    `_validate_connection` is patched out, and only that: the session, the loader, the
    wiring, and the botocore client are all genuine, which is the whole point -- a
    mocked session would make the wiring's `except Exception` swallow the test's intent
    and leave it passing for the wrong reason.
    """
    params = ConnectionParams(**{**_BASE_PARAMS, **param_overrides})
    with patch.object(RedshiftDataAPIClient, "_validate_connection"):
        return RedshiftDataAPIClient(params)


def _describe_request_members(driver_client):
    """The member names the client's resolved DescribeStatementRequest shape declares."""
    operation_model = driver_client.client.meta.service_model.operation_model("DescribeStatement")
    return operation_model.input_shape.members


def _resolving_loader(driver_client):
    """
    The botocore data loader that resolved this client's service model.

    Reaches through the same non-public attributes the wiring itself uses. There is no
    public boto3 route to a session's loader, which is the cost the design accepts and
    states.
    """
    return driver_client.session._session.get_component("data_loader")


def _session_with_explicit_credentials():
    """A real boto3 session, so a stubbed loader is the only stubbed thing in play."""
    return boto3.Session(
        aws_access_key_id=_EXPLICIT_KEY,
        aws_secret_access_key=_EXPLICIT_SECRET,
    )


def _poll_to_completion(driver_client, statement_id):
    """
    Drive the real polling loop once over this client and report the requests it made.

    The executor is built on the client the wiring produced, so the capability check
    reads that client's resolved service model -- the thing under test -- while
    `describe_statement` itself is patched to a fixed sequence of statuses. Returns
    (result, [(args, kwargs), ...]) for every poll.
    """
    connection = Mock(spec=Connection)
    connection.client = driver_client.client
    connection.connection_params = driver_client.connection_params
    executor = StatementExecutor(connection)

    with patch.object(driver_client.client, "describe_statement") as describe:
        describe.side_effect = [
            {"Status": "SUBMITTED"},
            {"Status": "STARTED"},
            {"Status": "FINISHED", "HasResultSet": True},
        ]
        with patch("time.sleep"):
            result = executor._poll_statement_completion(statement_id, {})
        calls = [(call.args, call.kwargs) for call in describe.call_args_list]

    return result, calls


class _TupleSearchPathLoader(Loader):
    """
    A real botocore loader whose search paths cannot be mutated.

    `Loader.search_paths` is a read-only property over a list, so the list itself is
    what the wiring mutates. Overriding the property to hand back a tuple is how a
    "search paths that are not a mutable list" is modelled without replacing the loader
    with something that no longer loads models: everything else about it is botocore's
    own, so the client it backs is real.
    """

    @property
    def search_paths(self):
        return tuple(self._search_paths)


@contextlib.contextmanager
def _broken_wiring(failure_mode, tmp_path):
    """
    Break the Model_Loader_Wiring one way, leaving everything else real.

    Each mode trips a different arm of the wiring's guard: the `os.path.isdir` test, the
    `get_component` call, the `insert` on `search_paths`, and the model load botocore
    performs when the client is created.
    """
    if failure_mode == "nonexistent_model_directory":
        missing = str(tmp_path / "no-such-models-directory")
        assert not os.path.isdir(missing)
        with patch.object(client_module, "_BUNDLED_MODELS_PATH", missing):
            yield
        return

    if failure_mode == "get_component_raises":
        session = _session_with_explicit_credentials()
        real_get_component = session._session.get_component
        state = {"raised": False}

        def get_component(name):
            # Raise only for the wiring's own lookup. Raising for every data_loader
            # lookup would break client creation itself and the case would assert the
            # wrong thing.
            if name == "data_loader" and not state["raised"]:
                state["raised"] = True
                raise RuntimeError("session exposes no data_loader component")
            return real_get_component(name)

        session._session.get_component = get_component
        with patch.object(RedshiftDataAPIClient, "_create_boto3_session", return_value=session):
            yield
        assert state["raised"], "the wiring never asked the session for its data loader"
        return

    if failure_mode == "search_paths_cannot_be_mutated":
        session = _session_with_explicit_credentials()
        session._session.register_component("data_loader", _TupleSearchPathLoader())
        with patch.object(RedshiftDataAPIClient, "_create_boto3_session", return_value=session):
            yield
        return

    if failure_mode == "unparseable_model_file":
        broken_root = tmp_path / "broken-models"
        model_directory = broken_root / _SERVICE_NAME / _API_VERSION
        model_directory.mkdir(parents=True)
        (model_directory / _MODEL_FILE_NAME).write_text(
            "{ this is not valid JSON", encoding="utf-8"
        )
        with patch.object(client_module, "_BUNDLED_MODELS_PATH", str(broken_root)):
            yield
        return

    raise AssertionError(f"unknown wiring failure mode: {failure_mode!r}")


_WIRING_FAILURE_MODES = [
    "nonexistent_model_directory",
    "get_component_raises",
    "search_paths_cannot_be_mutated",
    "unparseable_model_file",
]


# ---------------------------------------------------------------------------
# Property 17
# ---------------------------------------------------------------------------


class TestBundledModelDeclaresTheLongPollMember:
    """
    Feature: remove-redshift-data-api-query-timeout

    A pure file read of the shipped model. No session, no client, no loader: if the file
    is dropped from the package, moved out from under `_BUNDLED_MODELS_PATH`, or
    replaced with a model that omits the member, these cases fail immediately and name
    the reason -- which is what makes them worth stating separately from the wiring
    cases, where the same breakage shows up as a silent slide into classic polling.
    """

    @staticmethod
    def _bundled_model():
        assert os.path.isfile(
            _BUNDLED_MODEL_FILE
        ), f"bundled service model missing at {_BUNDLED_MODEL_FILE}"
        with open(_BUNDLED_MODEL_FILE, encoding="utf-8") as handle:
            return json.load(handle)

    def test_bundled_model_declares_the_long_poll_member(self):
        """
        Feature: remove-redshift-data-api-query-timeout, Property 17: The bundled model
        declares the long-poll member

        The request shape the driver long-polls on declares `WaitTimeSeconds`. Asserted
        on the parsed `members` mapping rather than on the file's text, so a member that
        appears only in a comment, in a different shape, or in a documentation string
        does not satisfy it.

        **Validates: Requirements 12.1, 12.9**
        """
        model = self._bundled_model()

        shapes = model["shapes"]
        assert _DESCRIBE_REQUEST_SHAPE in shapes
        members = shapes[_DESCRIBE_REQUEST_SHAPE]["members"]

        assert _LONG_POLL_MEMBER in members
        # The statement id has to survive alongside it, or the request the driver sends
        # in long-poll mode would be malformed in the other direction.
        assert "Id" in members

    def test_bundled_model_api_version_matches_the_path_the_loader_searches(self):
        """
        Feature: remove-redshift-data-api-query-timeout, Property 17: The bundled model
        declares the long-poll member

        botocore resolves a model at `<search path>/<service>/<apiVersion>/service-2.json`
        and reads the version from the directory name, so a model whose own
        `metadata.apiVersion` disagrees with the directory it ships in is a model the
        loader will hand back under the wrong version. The two are asserted equal.

        **Validates: Requirements 12.1, 12.9**
        """
        model = self._bundled_model()

        assert model["metadata"]["apiVersion"] == _API_VERSION
        assert os.path.basename(os.path.dirname(_BUNDLED_MODEL_FILE)) == _API_VERSION

    def test_bundled_model_declares_the_describe_statement_operation(self):
        """
        Feature: remove-redshift-data-api-query-timeout, Property 17: The bundled model
        declares the long-poll member

        The member is only reachable through the operation that takes the shape. A model
        declaring `DescribeStatementRequest` but no `DescribeStatement` operation would
        satisfy the member assertion above and still leave the capability check reading
        nothing, because the check goes through `operation_model("DescribeStatement")`.

        **Validates: Requirements 12.1, 12.9**
        """
        model = self._bundled_model()

        operations = model["operations"]
        assert "DescribeStatement" in operations
        assert operations["DescribeStatement"]["input"]["shape"] == _DESCRIBE_REQUEST_SHAPE


# ---------------------------------------------------------------------------
# Property 18
# ---------------------------------------------------------------------------

# (label, how the pre-existing AWS_DATA_PATH is set before the client is built). The
# driver must need none of them: "unset" is the clean case Requirement 12.3 names,
# "empty" is the shape a shell that exports the variable without a value leaves behind,
# and "unrelated_directory" is another component having already pointed the variable
# somewhere that holds no redshift-data model.
_DATA_PATH_STATES = ["unset", "empty", "unrelated_directory"]


def _apply_data_path_state(label, monkeypatch, tmp_path):
    if label == "unset":
        monkeypatch.delenv("AWS_DATA_PATH", raising=False)
        return
    if label == "empty":
        monkeypatch.setenv("AWS_DATA_PATH", "")
        return
    if label == "unrelated_directory":
        unrelated = tmp_path / "unrelated-models"
        unrelated.mkdir()
        monkeypatch.setenv("AWS_DATA_PATH", str(unrelated))
        return
    raise AssertionError(f"unknown AWS_DATA_PATH state: {label!r}")


class TestDriverClientResolvesTheBundledModel:
    """
    Feature: remove-redshift-data-api-query-timeout

    The cases that catch a broken wiring. Both failure modes the design warns about --
    a `package_data` entry that was never added and a wiring that does not engage --
    produce a client that polls in classic mode with no error, no warning, and a green
    suite everywhere else. These go red for either.
    """

    @pytest.mark.parametrize("data_path_state", _DATA_PATH_STATES)
    def test_client_resolves_the_member_with_no_environment_preparation(
        self, data_path_state, monkeypatch, tmp_path
    ):
        """
        Feature: remove-redshift-data-api-query-timeout, Property 18: The driver's client
        resolves the bundled model without environment preparation

        Whatever `AWS_DATA_PATH` held beforehand -- nothing, an empty value, or an
        unrelated directory -- the client the driver builds resolves a service model
        whose `DescribeStatementRequest` declares `WaitTimeSeconds`. Read off the
        botocore service model the client actually resolved, which is the same path the
        capability check reads, so this is the member being *available to the driver*
        rather than merely present in a file.

        **Validates: Requirements 12.3, 12.4, 12.10**
        """
        _apply_data_path_state(data_path_state, monkeypatch, tmp_path)

        driver_client = _build_driver_client(
            aws_access_key_id=_EXPLICIT_KEY, aws_secret_access_key=_EXPLICIT_SECRET
        )

        assert _LONG_POLL_MEMBER in _describe_request_members(driver_client)

    @pytest.mark.parametrize("data_path_state", _DATA_PATH_STATES)
    def test_bundled_path_precedes_botocores_own_data_directory(
        self, data_path_state, monkeypatch, tmp_path
    ):
        """
        Feature: remove-redshift-data-api-query-timeout, Property 18: The driver's client
        resolves the bundled model without environment preparation

        botocore searches `search_paths` in order and takes the first match, and it
        always ships its own `redshift-data` model, so the bundled directory has to come
        first or the wiring is a no-op in exactly the case it exists for. This is the
        case the `insert(0, ...)` / `append(...)` distinction turns on: under `append`
        the bundled path still appears in the list and the model file is still on disk,
        so only the ordering shows the difference.

        **Validates: Requirements 12.3, 12.4, 12.10**
        """
        _apply_data_path_state(data_path_state, monkeypatch, tmp_path)

        driver_client = _build_driver_client(
            aws_access_key_id=_EXPLICIT_KEY, aws_secret_access_key=_EXPLICIT_SECRET
        )
        search_paths = list(_resolving_loader(driver_client).search_paths)

        assert _BUNDLED_MODELS_PATH in search_paths, search_paths
        assert _BOTOCORE_DATA_PATH in search_paths, search_paths
        assert search_paths.index(_BUNDLED_MODELS_PATH) < search_paths.index(
            _BOTOCORE_DATA_PATH
        ), search_paths

    @pytest.mark.parametrize("credential_source", _CREDENTIAL_SOURCES)
    def test_every_credential_source_resolves_the_member(
        self, credential_source, monkeypatch, tmp_path
    ):
        """
        Feature: remove-redshift-data-api-query-timeout, Property 18: The driver's client
        resolves the bundled model without environment preparation

        The wiring is additive to whatever `_create_boto3_session` returned, so it does
        not branch on which credential source ran -- and this is what holds it to that.
        One of the four paths builds its own botocore session internally (the
        refreshable provider), which is the one most likely to drift away from the
        others if the wiring ever moves.

        **Validates: Requirements 12.3, 12.4, 12.10**
        """
        overrides, _ = _credential_source_setup(credential_source, monkeypatch, tmp_path)

        driver_client = _build_driver_client(**overrides)

        assert _LONG_POLL_MEMBER in _describe_request_members(driver_client)

    @_requires_botocore_without_the_member
    def test_the_bundled_model_is_what_supplies_the_member(self):
        """
        Feature: remove-redshift-data-api-query-timeout, Property 18: The driver's client
        resolves the bundled model without environment preparation

        The control for every case above. With the bundled path unwired -- the module
        constant pointed at a directory that does not exist, so the guard's `isdir` arm
        declines -- the same connection parameters produce a client that does *not*
        declare the member. Without this, an environment that supplied the member by
        some other route would make the assertions above pass while saying nothing about
        the wiring.

        **Validates: Requirements 12.4, 12.10**
        """
        with patch.object(client_module, "_BUNDLED_MODELS_PATH", "/nonexistent/boto3_models"):
            unwired = _build_driver_client(
                aws_access_key_id=_EXPLICIT_KEY, aws_secret_access_key=_EXPLICIT_SECRET
            )

        assert _LONG_POLL_MEMBER not in _describe_request_members(unwired)

    def test_live_polling_sends_the_wait_on_the_real_client(self):
        """
        Feature: remove-redshift-data-api-query-timeout, Property 18: The driver's client
        resolves the bundled model without environment preparation

        The end the wiring exists for: long polling is the live path, not a dormant
        branch. The polling loop running against a real wired client -- real session,
        real loader, real service model, only `describe_statement` itself stubbed --
        carries `WaitTimeSeconds=30` on every poll and never sleeps. Every other
        long-poll case in the suite reaches this branch through a faked service model;
        this one does not.

        **Validates: Requirements 12.3, 12.4, 12.10**
        """
        driver_client = _build_driver_client(
            aws_access_key_id=_EXPLICIT_KEY, aws_secret_access_key=_EXPLICIT_SECRET
        )

        result, calls = _poll_to_completion(driver_client, "live-long-poll-stmt")

        assert result["status"] == "FINISHED"
        assert calls, "the loop issued no describe_statement call"
        for index, (args, kwargs) in enumerate(calls):
            assert args == (), f"poll {index} passed positional arguments"
            assert kwargs == {
                "Id": "live-long-poll-stmt",
                _LONG_POLL_MEMBER: _EXPECTED_WAIT_SECONDS,
            }, f"poll {index}"


# ---------------------------------------------------------------------------
# Property 19
# ---------------------------------------------------------------------------


class TestWiringPreservesTheSessionItWasGiven:
    """
    Feature: remove-redshift-data-api-query-timeout

    Requirement 12.6 forbids the pattern four other modules in this package use --
    build a fresh botocore session around a loader and wrap it in a fresh boto3 session
    -- because here that would throw away everything `_create_boto3_session` resolved.
    These cases compare a wired client against the unwired client the same parameters
    produce, across all four credential sources, and assert the only thing the wiring
    changed is model resolution.
    """

    @staticmethod
    def _identity(driver_client):
        """Everything about a client the wiring must leave alone."""
        credentials = driver_client.session.get_credentials()
        return {
            "access_key": credentials.access_key if credentials else None,
            "region": driver_client.client.meta.region_name,
            "endpoint": driver_client.client.meta.endpoint_url,
            "profile": driver_client.session.profile_name,
        }

    @pytest.mark.parametrize("credential_source", _CREDENTIAL_SOURCES)
    def test_wiring_preserves_credentials_region_endpoint_and_profile(
        self, credential_source, monkeypatch, tmp_path
    ):
        """
        Feature: remove-redshift-data-api-query-timeout, Property 19: The wiring
        preserves credentials, region, endpoint, and profile

        For each credential source, the client built with the wiring in place reports
        the same resolved access key, region, endpoint, and profile as the client the
        same parameters produce with the wiring declining to engage. The expected access
        key is asserted outright as well, so a source that silently resolved to nothing
        on both sides cannot satisfy the comparison by matching `None` to `None`.

        **Validates: Requirements 12.5, 12.6, 12.11**
        """
        overrides, expected_access_key = _credential_source_setup(
            credential_source, monkeypatch, tmp_path
        )

        wired = _build_driver_client(**overrides)
        with patch.object(client_module, "_BUNDLED_MODELS_PATH", "/nonexistent/boto3_models"):
            unwired = _build_driver_client(**overrides)

        assert self._identity(wired) == self._identity(unwired)
        assert self._identity(wired)["access_key"] == expected_access_key
        assert self._identity(wired)["region"] == _BASE_PARAMS["region"]
        # The comparison is only worth making if the wiring did engage on one side.
        assert _LONG_POLL_MEMBER in _describe_request_members(wired)

    @pytest.mark.parametrize("credential_source", _CREDENTIAL_SOURCES)
    def test_client_is_built_on_the_session_create_boto3_session_returned(
        self, credential_source, monkeypatch, tmp_path
    ):
        """
        Feature: remove-redshift-data-api-query-timeout, Property 19: The wiring
        preserves credentials, region, endpoint, and profile

        The structural half of the property, and the one that fails the moment someone
        reaches for the fresh-botocore-session pattern: the session object the client is
        built on is identically the object `_create_boto3_session` returned. A
        replacement session could still report matching keys and region -- the
        default-chain source would resolve the same environment twice -- so identity is
        what has to be asserted, not equivalence.

        **Validates: Requirements 12.5, 12.6, 12.11**
        """
        overrides, _ = _credential_source_setup(credential_source, monkeypatch, tmp_path)
        created_sessions = []
        real_create = RedshiftDataAPIClient._create_boto3_session

        def spy(self):
            session = real_create(self)
            created_sessions.append(session)
            return session

        with patch.object(RedshiftDataAPIClient, "_create_boto3_session", spy):
            driver_client = _build_driver_client(**overrides)

        assert len(created_sessions) == 1
        assert driver_client.session is created_sessions[0]
        # And the loader the client resolved through is that session's own loader,
        # rather than one attached to something the wiring built on the side.
        assert (
            _BUNDLED_MODELS_PATH
            in created_sessions[0]._session.get_component("data_loader").search_paths
        )


# ---------------------------------------------------------------------------
# Property 20
# ---------------------------------------------------------------------------


class TestWiringIsIdempotent:
    """
    Feature: remove-redshift-data-api-query-timeout

    A loader belongs to a botocore session, and nothing stops a process from opening
    several connections over one. Without the membership guard every new client would
    prepend the same path again and `search_paths` would grow without bound. These cases
    pin the guard against a later simplification to an unconditional `insert`.
    """

    @pytest.mark.parametrize("client_count", [1, 2, 3, 8, 17])
    def test_bundled_path_appears_exactly_once_however_many_clients_are_built(self, client_count):
        """
        Feature: remove-redshift-data-api-query-timeout, Property 20: The wiring is
        idempotent across repeated client creation

        For n clients built against one boto3 session, the bundled directory occurs
        exactly once in that session's loader search paths and every one of the n
        clients resolves the member. The count is asserted rather than mere membership,
        because an unconditional `insert` would satisfy membership for every n.

        **Validates: Requirements 12.3, 12.4**
        """
        session = _session_with_explicit_credentials()

        with patch.object(RedshiftDataAPIClient, "_create_boto3_session", return_value=session):
            clients = [_build_driver_client() for _ in range(client_count)]

        search_paths = list(session._session.get_component("data_loader").search_paths)

        assert len(clients) == client_count
        assert search_paths.count(_BUNDLED_MODELS_PATH) == 1, search_paths
        for index, driver_client in enumerate(clients):
            assert _LONG_POLL_MEMBER in _describe_request_members(driver_client), f"client {index}"

    @pytest.mark.parametrize("client_count", [1, 2, 3, 8, 17])
    def test_search_paths_grow_by_exactly_one_entry_in_total(self, client_count):
        """
        Feature: remove-redshift-data-api-query-timeout, Property 20: The wiring is
        idempotent across repeated client creation

        The same guarantee read as a bound on the list rather than as a count of one
        entry: n client creations add one path between them, not n. Stated separately
        because an unbounded `search_paths` is the actual harm -- every model lookup on
        that session walks the list.

        **Validates: Requirements 12.3, 12.4**
        """
        session = _session_with_explicit_credentials()
        loader = session._session.get_component("data_loader")
        paths_before = list(loader.search_paths)

        with patch.object(RedshiftDataAPIClient, "_create_boto3_session", return_value=session):
            for _ in range(client_count):
                _build_driver_client()

        assert list(loader.search_paths) == [_BUNDLED_MODELS_PATH] + paths_before


# ---------------------------------------------------------------------------
# Property 21
# ---------------------------------------------------------------------------


class TestUnusableBundledModelStillYieldsAWorkingClient:
    """
    Feature: remove-redshift-data-api-query-timeout

    The bundled model is an optimization, never a reason connection setup fails.
    `_initialize_client` wraps its whole body in a broad `except Exception` that turns
    any failure into `InterfaceError`, so every way the wiring can fail has to be caught
    before it reaches that handler. These cases trip each arm of the guard in turn and
    assert the driver degrades to classic polling instead of failing to connect.
    """

    @pytest.mark.parametrize("failure_mode", _WIRING_FAILURE_MODES)
    def test_broken_wiring_still_yields_a_usable_client(self, failure_mode, tmp_path):
        """
        Feature: remove-redshift-data-api-query-timeout, Property 21: An unusable bundled
        model still yields a working client in classic mode

        Each wiring failure mode still produces a client: a nonexistent model directory,
        a session that raises when asked for its data loader, search paths that cannot
        be mutated, and a model file that cannot be parsed. `InterfaceError` is called
        out separately from the general failure because that is the specific shape a
        wiring failure would take if it escaped the guard, and the message would blame
        connection setup for something that is only an optimization.

        **Validates: Requirements 12.7, 12.8**
        """
        with _broken_wiring(failure_mode, tmp_path):
            try:
                driver_client = _build_driver_client(
                    aws_access_key_id=_EXPLICIT_KEY, aws_secret_access_key=_EXPLICIT_SECRET
                )
            except InterfaceError as error:
                pytest.fail(f"wiring failure {failure_mode!r} surfaced as InterfaceError: {error}")

        assert driver_client.client is not None
        assert driver_client.session is not None

    @_requires_botocore_without_the_member
    @pytest.mark.parametrize("failure_mode", _WIRING_FAILURE_MODES)
    def test_broken_wiring_polls_without_the_long_poll_member(self, failure_mode, tmp_path):
        """
        Feature: remove-redshift-data-api-query-timeout, Property 21: An unusable bundled
        model still yields a working client in classic mode

        Having a client is not enough: the fail-open behavior that makes bundling a
        model safe is that the loop then stops sending the parameter, rather than
        sending one the client would reject on every poll. Every request the loop issues
        for a client whose wiring failed carries nothing but `Id`, compared by exact
        dict equality so an unexpected extra parameter fails rather than slips past.

        **Validates: Requirements 12.7, 12.8**
        """
        with _broken_wiring(failure_mode, tmp_path):
            driver_client = _build_driver_client(
                aws_access_key_id=_EXPLICIT_KEY, aws_secret_access_key=_EXPLICIT_SECRET
            )

        result, calls = _poll_to_completion(driver_client, "fail-open-stmt")

        assert result["status"] == "FINISHED"
        assert calls, "the loop issued no describe_statement call"
        for index, (args, kwargs) in enumerate(calls):
            assert args == (), f"poll {index} passed positional arguments"
            assert kwargs == {"Id": "fail-open-stmt"}, f"poll {index}"
            assert _LONG_POLL_MEMBER not in kwargs, f"poll {index}"


# ---------------------------------------------------------------------------
# Packaging smoke check (Requirement 12.2)
# ---------------------------------------------------------------------------


def test_setup_py_ships_the_bundled_model_directory():
    """
    Feature: remove-redshift-data-api-query-timeout

    Not a property -- one assertion, no input variation -- but the only check in the
    suite that can fail when the packaging entry is missing. `package_data` enumerates
    each model directory explicitly rather than globbing `boto3_models/**`, and a source
    checkout has the file on disk either way, so without this every test and every local
    run would pass while the installed artifact silently lacked the model and installed
    users got classic polling with no error anywhere.

    **Validates: Requirements 12.2**
    """
    with open(_SETUP_PY, encoding="utf-8") as handle:
        setup_source = handle.read()

    assert f"boto3_models/{_SERVICE_NAME}/{_API_VERSION}/*.json" in setup_source
