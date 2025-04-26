import datetime
import json
import logging
import os
from typing import Tuple, cast

from distributed import Client

from coiled.utils import supress_logs


class _FakeCredentialsBase:
    def __init__(self, *args, **kwargs): ...


try:
    from google.oauth2.credentials import Credentials as GoogleOAuth2Credentials
except ImportError:
    GoogleOAuth2Credentials = _FakeCredentialsBase


logger = logging.getLogger(__name__)


def get_gcp_local_session_token(scopes=None, set_local_token_env: bool = False) -> dict:
    auth_logger = None
    comp_logger = None
    auth_logger_level = 0
    comp_logger_level = 0

    try:
        import google.auth
        import google.oauth2.credentials
        from google.auth.exceptions import RefreshError
        from google.auth.transport.requests import Request

        with supress_logs(["google.auth._default", "google.auth.compute_engine._metadata"]):
            # get token from local auth
            local_creds, project = google.auth.default(scopes=scopes)
            local_creds = cast(google.oauth2.credentials.Credentials, local_creds)
            try:
                local_creds.refresh(Request())
            except RefreshError:
                # when local creds are service account, we need to explicitly specify scope(s)
                # or else we get this exception:
                #   RefreshError:
                #   ('invalid_scope: Invalid OAuth scope or ID token audience provided.',
                #    {'error': 'invalid_scope',
                #     'error_description': 'Invalid OAuth scope or ID token audience provided.'})
                local_creds, project = google.auth.default(
                    scopes=[*(scopes or []), "https://www.googleapis.com/auth/cloud-platform"]
                )
                local_creds = cast(google.oauth2.credentials.Credentials, local_creds)
                local_creds.refresh(Request())

        if set_local_token_env:
            # set local env var with token, in case `CoiledShippedCredentials` is being used locally
            os.environ["COILED_LOCAL_CLOUDSDK_AUTH_ACCESS_TOKEN"] = local_creds.token or ""

        return {
            "token": local_creds.token,
            "project": project,
            "expiry": local_creds.expiry.replace(tzinfo=datetime.timezone.utc) if local_creds.expiry else None,
        }
    except Exception as e:
        if "default credentials were not found" not in str(e):
            logger.warning(
                "Could not get token from client GCP session. "
                f"This is not a concern unless you're planning to use forwarded GCP credentials on your cluster. "
                f"The error was: {e}"
            )
    finally:
        if auth_logger:
            auth_logger.setLevel(auth_logger_level)
        if comp_logger:
            comp_logger.setLevel(comp_logger_level)

    return {}


def get_application_default_credentials(scopes=None):
    try:
        import google.auth
        import google.oauth2.credentials
    except ImportError:
        raise ImportError(
            "Unable to retrieve Google Application Default Credentials because google-auth is not installed."
        ) from None
    local_creds, project = google.auth.default(scopes=scopes)
    local_creds = cast(google.oauth2.credentials.Credentials, local_creds)
    return {
        "client_id": local_creds.client_id,
        "client_secret": local_creds.client_secret,
        "quota_project_id": local_creds.quota_project_id or project,
        "refresh_token": local_creds.refresh_token,
        "type": "authorized_user",
    }


def get_long_lived_adc_to_forward(scopes=None):
    to_forward = {}

    # get *local* credentials
    adf = get_application_default_credentials(scopes)
    adf_json = json.dumps(adf)

    project = adf["quota_project_id"]

    default_config = f"""[core]
    project = {project}
    """

    to_forward["env"] = {
        "GS_OAUTH2_CLIENT_ID": adf["client_id"],
        "GS_OAUTH2_CLIENT_SECRET": adf["client_secret"],
        "GS_OAUTH2_REFRESH_TOKEN": adf["refresh_token"],
        "GOOGLE_CLOUD_PROJECT": project,
    }

    to_forward["files"] = {
        "/gcloud-config/application_default_credentials.json": adf_json,
        "/gcloud-config/configurations/config_default": default_config,
    }

    return to_forward


def send_application_default_credentials(cluster, scopes=None, return_creds: bool = False):
    to_forward = get_long_lived_adc_to_forward(scopes)

    def write_adf_files():
        for path, content in to_forward["files"].items():
            abs_path = os.path.expanduser(path)
            os.makedirs(os.path.dirname(abs_path), exist_ok=True)
            with open(abs_path, "w") as f:
                f.write(content)

        os.makedirs(os.path.expanduser("~/.config"), exist_ok=True)
        container_adc_dir = os.path.expanduser("~/.config/gcloud")

        # files are written to /gcloud-config, which is then symlinked to ~/.config/gcloud
        if not os.path.exists(container_adc_dir):
            os.symlink("/gcloud-config", container_adc_dir, target_is_directory=True)
        # otherwise, maybe we should copy the files to both places?

    cluster.send_private_envs(to_forward["env"])
    with Client(cluster, name="non-user-write-gcp-adf") as client:
        client.run_on_scheduler(write_adf_files)
        client.run(write_adf_files)

    cluster._queue_cluster_event("credentials", "Google Application Default Credentials forwarded")
    print(
        "Google Application Default Credentials have been written to a file on your Coiled VM(s).\n"
        "These credentials will potentially be valid until explicitly revoked by running\n"
        "gcloud auth application-default revoke"
    )

    if return_creds:
        return to_forward


class CoiledShippedCredentials(GoogleOAuth2Credentials):  # type: ignore
    def __init__(
        self,
        token=None,
        refresh_token=None,
        id_token=None,
        token_uri=None,
        client_id=None,
        client_secret=None,
        scopes=None,
        default_scopes=None,
        quota_project_id=None,
        expiry=None,
        rapt_token=None,
        refresh_handler=None,
        enable_reauth_refresh=False,
        granted_scopes=None,
    ):
        if GoogleOAuth2Credentials is _FakeCredentialsBase:
            raise ImportError("Unable to create Google Credentials object because google-cloud-iam is not installed.")

        env_token = self.get_shipped_token()
        if token and env_token and token != env_token:
            raise ValueError(
                "Specified Google OAuth2 token does not match "
                "token shipped by Coiled in CLOUDSDK_AUTH_ACCESS_TOKEN.\n"
                "We recommend not specifying a token and using the shipped token."
            )
        if token and not env_token:
            # most likely local testing
            logger.warning(
                "Instantiating credentials with explicit token, no shipped token "
                "found in CLOUDSDK_AUTH_ACCESS_TOKEN. Refresh (which uses CLOUDSDK_AUTH_ACCESS_TOKEN) "
                "is unlikely to work."
            )

        super().__init__(token=env_token, refresh_handler=self.coiled_token_refresh_handler)

    @staticmethod
    def get_shipped_token():
        try:
            # file can be updated by nanny plugin even when worker plugins are blocked by event loop,
            # so use token from file if it's present
            with open("/scratch/.creds/gcp-oauth2-token") as f:
                token = f.read()
                if token:
                    return token
        except Exception:
            pass

        token = os.environ.get("CLOUDSDK_AUTH_ACCESS_TOKEN")

        if not token:
            # It's not the normal use-case, but Coiled can also set this env on local client machine
            # so that you can use `CoiledShippedCredentials` (with same OAuth2 token) locally and on cluster.
            token = os.environ.get("COILED_LOCAL_CLOUDSDK_AUTH_ACCESS_TOKEN")

        if not token:
            # print rather than log since we don't know how logging is configure on the cluster
            print("No Google OAuth2 token found, CLOUDSDK_AUTH_ACCESS_TOKEN env var not set")
        return token

    @staticmethod
    def get_token_expiry(token: str) -> datetime.datetime:
        import httpx

        result = httpx.get(f"https://oauth2.googleapis.com/tokeninfo?access_token={token}")
        data = result.json()
        timestamp = int(data["exp"])
        # note that refresh_handler is expected to return naive utc datetime
        expiry = datetime.datetime.utcfromtimestamp(timestamp)
        return expiry

    def coiled_token_refresh_handler(self, request, scopes) -> Tuple[str, datetime.datetime]:
        # this relies on other Coiled mechanisms to have already shipped a non-expired token to the cluster
        token = self.get_shipped_token()

        if not token:
            from google.auth.exceptions import RefreshError

            raise RefreshError(
                "Coiled was unable to find Google OAuth2 token on the cluster. "
                "See https://docs.coiled.io/user_guide/remote-data-access.html#gcp for details about shipping "
                "OAuth2 tokens from the client to the cluster."
            )

        expiry = self.get_token_expiry(token)

        print(f"CoiledShippedCredentials have been refreshed, new expiration is {expiry}")

        return token, expiry


def get_identity(credentials=None):
    import google.auth
    import google.oauth2.credentials
    import httpx
    from google.auth.transport.requests import Request

    if not credentials:
        credentials, _project = google.auth.default()
        credentials = cast(google.oauth2.credentials.Credentials, credentials)
    credentials.refresh(Request())

    result = httpx.get(f"https://oauth2.googleapis.com/tokeninfo?access_token={credentials.token}")
    return result.json()
