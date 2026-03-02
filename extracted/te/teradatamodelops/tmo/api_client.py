from __future__ import absolute_import

import json
import logging
import os
import re
import time

import aia
import jwt
import oauthlib
import requests
import yaml
from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth
from requests.exceptions import ConnectionError, SSLError
from requests_oauthlib import OAuth2Session
from typing_extensions import deprecated

from .spinner import spin_it
from .types.exceptions import AuthorizationError, ConfigurationError

RECOPY_CLI_CONFIG_MSG = (
    "Please (re)copy the CLI configuration from ModelOps UI -> Session Details -> CLI"
    " Config\n"
)
os.system("")  # enables ansi escape characters in terminal


class TmoClient(object):
    DEFAULT_OLD_CONFIG_DIR = os.path.expanduser("~/.aoa")
    DEFAULT_CONFIG_DIR = os.path.expanduser("~/.tmo")
    DEFAULT_TOKEN_CACHE_FILE_PATH = os.path.join(DEFAULT_CONFIG_DIR, ".token")
    DEFAULT_OLD_CONFIG_FILE_PATH = os.path.join(DEFAULT_OLD_CONFIG_DIR, "config.yaml")
    DEFAULT_CONFIG_FILE_PATH = os.path.join(DEFAULT_CONFIG_DIR, "config.yaml")
    DEFAULT_PAT_PRIVATE_KEY_PATH = os.path.join(DEFAULT_CONFIG_DIR, "modelops_pat.pem")
    MAX_RETRIES = 3
    REFRESH_BEFORE_EXPIRES = 60

    def __init__(self, **kwargs):
        """

        Parameters:
           project_id (str): project id(uuid)
           ssl_verify (bool): enable or disable TLS cert validation
           vmo_url (str): ModelOps api endpoint

           auth_mode (str): device_code|pat|client_credentials|bearer

           If using auth_mode=bearer
           auth_bearer (str): the raw bearer token

           If using auth_mode=client_credentials
           auth_client_id (str): oauth2 client id
           auth_client_secret (str): oauth2 client secret
           auth_token_url (str): oauth2 token endpoint

           if using auth_mode=device_code
           auth_client_id (str): oauth2 client id
           auth_client_secret (str): oauth2 client secret
           auth_token_url (str): oauth2 token endpoint
           auth_device_auth_url (str): oauth2 device code endpoint

           if using auth_mode=pat
           pat (str): Personal Access Token (PAT) value
           user (str): username
        """
        self.logger = logging.getLogger(__name__)

        self.ssl_verify = True
        self.vmo_url = None

        self.auth_mode = None

        self.__client_id = None
        self.__client_secret = None
        self.__token_url = None
        self.__device_auth_url = None
        self.__bearer_token = None

        self.__pat = None
        self.__user = None

        self.__bearer_token = None

        os.makedirs(self.DEFAULT_CONFIG_DIR, exist_ok=True)
        self.__rename_tmo_config()
        self.__parse_tmo_config(**kwargs)

        if self.auth_mode == "device_code":
            self.__handle_device_code()

        elif self.auth_mode == "pat":
            self.__create_auth_session_pat()

        elif self.auth_mode == "client_credentials":
            self.__create_oauth_session_client_credentials()

        elif self.auth_mode == "bearer":
            self.__create_oauth_session_bearer()

        elif self.auth_mode is None:
            raise ConfigurationError(
                "ModelOps endpoint not configured.\nTry (re)copy the CLI configuration"
                " from ModelOps UI -> Session Details -> CLI Config."
            )

        else:
            raise ValueError(f"Auth mode: {self.auth_mode} not supported.")

        if kwargs.get("project_id"):
            self.set_project_id(kwargs.get("project_id"))
        else:
            self.project_id = None

        self.logger.info(f"Connected to {self.vmo_url}\n")

    def __rename_tmo_config(self):
        if os.path.isfile(self.DEFAULT_OLD_CONFIG_FILE_PATH):
            os.rename(self.DEFAULT_OLD_CONFIG_FILE_PATH, self.DEFAULT_CONFIG_FILE_PATH)
            with open(self.DEFAULT_CONFIG_FILE_PATH, "r") as handle:
                conf = yaml.safe_load(handle)
            if "aoa_url" in conf:
                conf["vmo_url"] = conf["aoa_url"]
                del conf["aoa_url"]
            for key in conf:
                if key.startswith("aoa_"):
                    new_key = key.replace("aoa_", "tmo_")
                    conf[new_key] = conf[key]
                    del conf[key]
            yaml.safe_dump(conf, open(self.DEFAULT_CONFIG_FILE_PATH, "w"))

    def __parse_tmo_config(self, **kwargs):
        if "config_file" in kwargs:
            self.__parse_yaml(kwargs["config_file"])
        else:
            if os.path.isfile(self.DEFAULT_CONFIG_FILE_PATH):
                self.__parse_yaml(self.DEFAULT_CONFIG_FILE_PATH)

        self.__parse_env_variables()
        self.__parse_kwargs(**kwargs)

    def __parse_yaml(self, yaml_path: str):
        with open(yaml_path, "r") as handle:
            conf = yaml.safe_load(handle)
        self.__parse_kwargs(**conf)

    def __parse_kwargs(self, **kwargs):
        self.vmo_url = kwargs.get("vmo_url", self.vmo_url)
        self.ssl_verify = kwargs.get("ssl_verify", self.ssl_verify)
        self.auth_mode = kwargs.get("auth_mode", self.auth_mode)

        self.__check_legacy_mode()

        if self.auth_mode == "device_code":
            self.__client_id = kwargs.get("auth_client_id", self.__client_id)
            self.__client_secret = kwargs.get(
                "auth_client_secret", self.__client_secret
            )
            self.__token_url = kwargs.get("auth_token_url", self.__token_url)
            self.__device_auth_url = kwargs.get(
                "auth_device_auth_url", self.__device_auth_url
            )

        elif self.auth_mode == "pat":
            self.__pat = kwargs.get("pat", self.__pat)
            self.__user = kwargs.get("user", self.__user)

        elif self.auth_mode == "client_credentials":
            self.__client_id = kwargs.get("auth_client_id", self.__client_id)
            self.__client_secret = kwargs.get(
                "auth_client_secret", self.__client_secret
            )
            self.__token_url = kwargs.get("auth_token_url", self.__token_url)

        elif self.auth_mode == "bearer":
            self.__bearer_token = kwargs.get("auth_bearer", self.__bearer_token)

        if "verify_connection" in kwargs:
            self.verify_tmo_connection = kwargs["verify_connection"]

    def __parse_env_variables(self):
        self.vmo_url = os.environ.get("VMO_URL", self.vmo_url)
        self.ssl_verify = (
            os.environ.get("VMO_SSL_VERIFY", str(self.ssl_verify)).lower() == "true"
        )
        self.auth_mode = os.environ.get("VMO_API_AUTH_MODE", self.auth_mode)

        self.__check_legacy_mode()

        if self.auth_mode == "device_code":
            self.__client_id = os.environ.get(
                "VMO_API_AUTH_CLIENT_ID", self.__client_id
            )
            self.__client_secret = os.environ.get(
                "VMO_API_AUTH_CLIENT_SECRET", self.__client_secret
            )
            self.__token_url = os.environ.get(
                "VMO_API_AUTH_TOKEN_URL", self.__token_url
            )
            self.__device_auth_url = os.environ.get(
                "VMO_API_AUTH_DEVICE_AUTH_URL", self.__device_auth_url
            )

        elif self.auth_mode == "pat":
            self.__user = os.environ.get("VMO_API_USER", self.__user)
            self.__pat = os.environ.get("VMO_API_PAT", self.__pat)

        elif self.auth_mode == "client_credentials":
            self.__client_id = os.environ.get(
                "VMO_API_AUTH_CLIENT_ID", self.__client_id
            )
            self.__client_secret = os.environ.get(
                "VMO_API_AUTH_CLIENT_SECRET", self.__client_secret
            )
            self.__token_url = os.environ.get(
                "VMO_API_AUTH_TOKEN_URL", self.__token_url
            )

        elif self.auth_mode == "bearer":
            self.__bearer_token = os.environ.get(
                "VMO_API_AUTH_BEARER_TOKEN", self.__bearer_token
            )

    def __check_legacy_mode(self):
        if self.auth_mode == "oauth-cc":
            self.auth_mode = "client_credentials"
        elif self.auth_mode == "oauth":
            self.auth_mode = "device_code"

    def __validate_url(self):
        if not self.vmo_url:
            raise ValueError(
                "ModelOps endpoint not configured.\nTry (re)copy the CLI configuration"
                " from ModelOps UI -> Session Details -> CLI Config."
            )

    def set_project_id(self, project_id: str):
        """
        set project id

        Parameters:
           project_id (str): project id(uuid)
        """
        self.project_id = project_id
        if not self.projects().find_by_id(project_id):
            self.logger.warning(
                f"Project with id {project_id} not found, but we'll set it anyway.\n"
            )

    def get_current_project(self):
        """
        get project id

        Return:
           project_id (str): project id(uuid)
        """
        return self.project_id

    @staticmethod
    def select_header_accept(accepts: list[str]):
        """
        converts list of header into a string

        Return:
            (str): request header
        """
        if not accepts:
            return None

        accepts = [x.lower() for x in accepts]
        return ", ".join(accepts)

    def get_request(
        self, path, header_params: dict[str, str], query_params: dict[str, str]
    ):
        """
        wrapper for get request

        Parameters:
           path (str): url
           header_params (dict): header parameters
           query_params (dict): query parameters

        Returns:
            dict for resources, str for errors, None for 404
        Raise:
            raises HTTPError in case of error status code other than 404
        """

        self.__validate_url()
        retry = 0

        # check token before making call
        if self.auth_mode == "pat":
            self.__validate_stored_token()

        while retry < self.MAX_RETRIES:
            try:
                resp = self.session.get(
                    url=self.__strip_url(self.vmo_url) + path,
                    headers=header_params,
                    params=query_params,
                )

                if resp.status_code == 404:
                    return None

                return self.__validate_and_extract_body(resp)

            except ConnectionError:
                retry += 1
                time.sleep(5)

            except Exception as e:
                logging.error(f"Error: {e}")
                return None

        self.logger.error(
            "Max retries reached. Please check your network connection.\n"
        )
        return None

    def post_request(
        self,
        path,
        header_params: dict[str, str],
        query_params: dict[str, str],
        body: dict[str, str],
    ):
        """
        wrapper for post request

        Parameters:
           path (str): url
           header_params (dict): header parameters
           query_params (dict): query parameters
           body (dict): request body

        Returns:
            dict for resources, str for errors
        Raise:
            raises HTTPError in case of error status code
        """

        self.__validate_url()

        # check token before making call
        if self.auth_mode == "pat":
            self.__validate_stored_token()

        resp = self.session.post(
            url=self.__strip_url(self.vmo_url) + path,
            headers=header_params,
            params=query_params,
            data=json.dumps(body),
        )

        return self.__validate_and_extract_body(resp)

    def put_request(
        self,
        path,
        header_params: dict[str, str],
        query_params: dict[str, str],
        body: dict[str, str],
    ):
        """
        wrapper for put request

        Parameters:
           path (str): url
           header_params (dict): header parameters
           query_params (dict): query parameters
           body (dict): request body

        Returns:
            dict for resources, str for errors
        Raise:
            raises HTTPError in case of error status code
        """

        self.__validate_url()

        # check token before making call
        if self.auth_mode == "pat":
            self.__validate_stored_token()

        resp = self.session.put(
            url=self.__strip_url(self.vmo_url) + path,
            headers=header_params,
            params=query_params,
            data=json.dumps(body),
        )

        return self.__validate_and_extract_body(resp)

    def delete_request(
        self,
        path,
        header_params: dict[str, str],
        query_params: dict[str, str],
        body: dict[str, str],
    ):
        """
        wrapper for delete request
        Parameters:
           path (str): url
           header_params (dict): header parameters
           query_params (dict): query parameters
           body (dict): request body
        Returns:
            dict for resources, str for errors
        Raise:
            raises HTTPError in case of error status code
        """

        self.__validate_url()

        # check token before making call
        if self.auth_mode == "pat":
            self.__validate_stored_token()

        resp = self.session.delete(
            url=self.__strip_url(self.vmo_url) + path,
            headers=header_params,
            params=query_params,
            data=json.dumps(body),
        )

        return self.__validate_and_extract_body(resp)

    def __validate_and_extract_body(self, resp):
        if resp.status_code == 401:
            self.__remove_cached_token()
            self.logger.warning(
                "Clearing the token cache. Please re-run cmd and login again."
            )
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as err:
            if resp.text:
                raise requests.exceptions.HTTPError(f"Error message: {resp.text}")
            else:
                raise err

        try:
            return resp.json()
        except ValueError:
            return resp.text

    @staticmethod
    def __strip_url(url):
        return url.rstrip("/")

    def __create_oauth_session_device_code(self):
        self.logger.debug("Configuring oauth with device_code grant")

        if (
            self.__client_id is None
            or self.__token_url is None
            or self.__device_auth_url is None
        ):
            raise ConfigurationError(
                "Missing CLI configuration.\n" + RECOPY_CLI_CONFIG_MSG
            )

        token = None
        if os.path.exists(self.DEFAULT_TOKEN_CACHE_FILE_PATH):
            self.logger.debug(
                f"Loading cached token data from {self.DEFAULT_TOKEN_CACHE_FILE_PATH}"
            )
            with open(self.DEFAULT_TOKEN_CACHE_FILE_PATH, "r") as f:
                token = json.load(f)

        if not token:
            self.session = requests.session()
            self.__set_session_tls()
            token = self.__get_device_code()

        if "expires_at" in token and int(token["expires_at"]) < int(
            time.time() + self.REFRESH_BEFORE_EXPIRES
        ):
            token_expired = True
        elif "expires_at" not in token and (
            int(time.time()) + int(token["expires_in"])
        ) < int(time.time() + self.REFRESH_BEFORE_EXPIRES):
            token_expired = True
        else:
            token_expired = False

        if "refresh_token" in token and token_expired:
            self.logger.debug(f"Refresh token acquired successfully: {token}")

            session = OAuth2Session(client_id=self.__client_id)

            token = session.refresh_token(
                token_url=self.__token_url,
                refresh_token=token["refresh_token"],
                auth=HTTPBasicAuth(self.__client_id, self.__client_secret),
                verify=self.ssl_verify,
            )

        elif "access_token" in token:
            self.logger.debug(f"Access token acquired successfully: {token}")

            session = OAuth2Session(client_id=self.__client_id)

        else:
            raise ValueError(
                "Token does not contain access_token or refresh_token. Received"
                f" {token}"
            )

        # don't chase certs/print warning for TLS if already done for __get_device_code
        if hasattr(self, "session"):
            session.verify = self.session.verify
            self.session = session
        else:
            self.session = session
            self.__set_session_tls()

        self.__bearer_token = f"Bearer {token['access_token']}"
        self.__create_oauth_session_bearer()
        self.__save_oauth_token(token)

    def __save_oauth_token(self, token):
        if "expires_in" in token and "expires_at" not in token:
            token["expires_at"] = int(time.time()) + int(token["expires_in"])
        try:
            with open(self.DEFAULT_TOKEN_CACHE_FILE_PATH, "w") as f:
                json.dump(token, f)
            self.__bearer_token = f"Bearer {token['access_token']}"
            self.logger.debug("OAuth token saved successfully.")
        except Exception as e:
            self.logger.error(f"Failed to save OAuth token: {e}")

    def __handle_device_code(self):
        try:
            self.__create_oauth_session_device_code()
        except oauthlib.oauth2.rfc6749.errors.InvalidGrantError as ge:
            if ge.description in ["Token is not active", "Session not active"]:
                self.logger.warning(ge.description + "\nRetrying one more time\n")
                self.__remove_cached_token()
                self.__create_oauth_session_device_code()
            else:
                raise ge
        except oauthlib.oauth2.rfc6749.errors.InvalidTokenError as ge:
            self.logger.warning(ge.description + "\nRetrying one more time\n")
            self.__remove_cached_token()
            self.__create_oauth_session_device_code()

    def __create_auth_session_pat(self):
        self.logger.info("Configuring auth with PAT.\n")

        if self.__pat is None or self.__user is None:
            raise ConfigurationError(
                "Missing CLI configuration.\n" + RECOPY_CLI_CONFIG_MSG
            )

        self.__validate_stored_token()

    def __create_oauth_session_client_credentials(self):
        self.logger.debug("Configuring oauth with client_credentials grant")

        if (
            self.__client_id is None
            or self.__client_secret is None
            or self.__token_url is None
        ):
            raise ValueError(
                "VMO_API_AUTH_CLIENT_ID, VMO_API_AUTH_CLIENT_SECRET, "
                "VMO_API_AUTH_TOKEN_URL must be defined "
                "with VMO_API_AUTH_MODE of 'client_credentials'"
            )

        self.session = OAuth2Session(
            client=BackendApplicationClient(client_id=self.__client_id)
        )
        self.__set_session_tls()
        self.session.fetch_token(
            token_url=self.__token_url,
            auth=HTTPBasicAuth(self.__client_id, self.__client_secret),
            verify=self.ssl_verify,
        )

    def __create_oauth_session_bearer(self):
        self.session = requests.session()
        self.session.headers.update({"Authorization": self.__bearer_token})
        self.__set_session_tls()

    def __get_device_code(self):
        request_args = {
            "client_id": self.__client_id,
            "scope": "openid profile",
        }

        if self.__client_secret is not None:
            client_secret = {"client_secret": self.__client_secret}
            request_args = {**request_args, **client_secret}

        device_code_response = self.session.post(
            self.__device_auth_url,
            data=request_args,
        )

        if device_code_response.status_code != 200:
            raise ValueError(
                "Error generating the device code. Received code"
                f" {device_code_response.status_code}."
            )

        device_code_data = device_code_response.json()
        print(
            "1. On your computer or mobile device navigate to: ",
            device_code_data["verification_uri_complete"],
        )
        print("2. Enter the following code: ", device_code_data["user_code"])

        def authorize():
            authenticated = False
            token_data = None

            while not authenticated:
                token_response = self.session.post(
                    self.__token_url,
                    data={
                        "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                        "device_code": device_code_data["device_code"],
                        "client_id": self.__client_id,
                    },
                )

                token_data = token_response.json()
                if token_response.status_code == 200:
                    authenticated = True

                elif "error" in token_data:
                    if token_data["error"] in ("authorization_pending", "slow_down"):
                        time.sleep(device_code_data["interval"])
                    else:
                        raise AuthorizationError(token_data["error_description"])

                else:
                    raise AuthorizationError(
                        f"Bad response code {token_response.status_code}"
                    )

            return token_data

        msg = "Waiting for device code to be authorized"
        res = spin_it(authorize, msg, 0.2)
        print(
            "\033[32m\U0001f512 This device has been authorized successfully.\033[0m\n"
        )
        return res

    def __create_self_signed_jwt(self):

        with open(self.DEFAULT_PAT_PRIVATE_KEY_PATH, "r") as handle:
            private_key = handle.read()

        self.logger.debug("Signing JWT with private key")

        # generate header for JWT
        header = {"alg": "RS256", "kid": "modelops_pat", "typ": "JWT"}

        # generate payload for JWT
        iat = int(time.time())
        exp = iat + 180

        # extract org id from vmo url
        start_index = self.vmo_url.find("https://")
        org_id = self.vmo_url[start_index + len("https://") :].split(".", 1)[0]

        payload = {
            "aud": ["td:service:authentication"],
            "iat": iat,
            "exp": exp,
            "iss": "tdmodelops",
            "multi-use": True,
            "org_id": org_id,
            "pat": self.__pat,
            "sub": self.__user,
        }

        signed_jwt = jwt.encode(
            payload=payload, key=private_key, algorithm="RS256", headers=header
        )
        self.logger.debug("Self signed jwt ready")

        self.__save_signed_jwt(signed_jwt, exp)
        return signed_jwt

    def __set_session_tls(self):
        self.session.verify = self.ssl_verify
        if self.ssl_verify:
            self.__chase_tls_cert_chain()
        else:
            from requests.packages.urllib3.exceptions import (  # noqa
                InsecureRequestWarning,  # noqa
            )

            if os.getenv("CALLED_FROM_TEST", "false").lower() != "true":
                self.logger.warning(
                    "Certificate validation disabled. Adding certificate verification"
                    " is strongly advised"
                )
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # noqa

    def __chase_tls_cert_chain(self):
        if not hasattr(self, "vmo_url"):
            raise ConfigurationError(
                "Wrong or missing CLI configuration.\n" + RECOPY_CLI_CONFIG_MSG
            )
        elif self.vmo_url.startswith("https") and not (
            "REQUESTS_CA_BUNDLE" in os.environ or "CURL_CA_BUNDLE" in os.environ
        ):

            try:
                if re.search("http|https", self.vmo_url):
                    requests.get(f"{self.vmo_url}/admin/info")
                else:
                    raise ConfigurationError("Invalid VMO_URL")
            except requests.exceptions.SSLError:
                from aia import AIASession
                from tempfile import NamedTemporaryFile

                self.logger.debug("Attempting certificate chain chasing via aia")

                # unless, debug logging enabled,
                # change logging level for aia to warning as it prints debug at info level
                if logging.root.level > logging.DEBUG:
                    logging.getLogger("aia").setLevel(logging.WARNING)

                try:
                    aia_session = AIASession()

                    ca_data = aia_session.cadata_from_url(self.vmo_url)
                    with NamedTemporaryFile("w", delete=False) as pem_file:
                        pem_file.write(ca_data)
                        pem_file.flush()

                    self.session.verify = pem_file.name
                except aia.InvalidCAError:
                    raise SSLError(
                        "Attempted to find trusted root certificate via AIA chasing but"
                        " not found.\nPlease configure REQUESTS_CA_BUNDLE or"
                        " CURL_CA_BUNDLE.\nAlternatively, to ignore TLS validation (not"
                        " advised), export VMO_SSL_VERIFY=false"
                    )

    def projects(self):
        """
        get projects client
        """
        from tmo import ProjectApi

        return ProjectApi(tmo_client=self)

    def datasets(self):
        """
        get datasets client
        """
        from tmo import DatasetApi

        return DatasetApi(tmo_client=self)

    def dataset_templates(self):
        """
        get dataset templates client
        """

        from tmo import DatasetTemplateApi

        return DatasetTemplateApi(tmo_client=self)

    def dataset_connections(self):
        """
        get dataset connections client
        """

        from tmo import DatasetConnectionApi

        return DatasetConnectionApi(tmo_client=self)

    def deployments(self):
        """
        get deployments client
        """

        from tmo import DeploymentApi

        return DeploymentApi(tmo_client=self)

    def feature_engineering(self):
        """
        get feature engineering client
        """

        from tmo import FeatureEngineeringApi

        return FeatureEngineeringApi(tmo_client=self)

    def jobs(self):
        """
        get jobs client
        """

        from tmo import JobApi

        return JobApi(tmo_client=self)

    def job_events(self):
        """
        get job events client
        """

        from tmo import JobEventApi

        return JobEventApi(tmo_client=self)

    def messages(self):
        """
        get messages client
        """

        from tmo import MessageApi

        return MessageApi(tmo_client=self)

    def models(self):
        """
        get models client
        """

        from tmo import ModelApi

        return ModelApi(tmo_client=self)

    def trained_models(self):
        """
        get trained models client
        """

        from tmo import TrainedModelApi

        return TrainedModelApi(tmo_client=self)

    def trained_model_artefacts(self):
        """
        get trained model artefacts client
        """

        from tmo import TrainedModelArtefactsApi

        return TrainedModelArtefactsApi(tmo_client=self)

    def trained_model_events(self):
        """
        get trained model events client
        """

        from tmo import TrainedModelEventApi

        return TrainedModelEventApi(tmo_client=self)

    def user_attributes(self):
        """
        get user attributes client
        """

        from tmo import UserAttributesApi

        return UserAttributesApi(tmo_client=self)

    def describe_current_project(self):
        """
        get details of currently selected project
        """
        import pandas as pd

        if self.project_id:
            project_dict = self.projects().find_by_id(self.project_id, "expandProject")
            if project_dict:
                project_data = [
                    [k, v]
                    for (k, v) in project_dict.items()
                    if k not in ["_links", "userAttributes"]
                ]
                return pd.DataFrame(project_data, columns=["attribute", "value"])
            else:
                return None
        else:
            return None

    def get_default_connection_id(self):
        """
        get default dataset connection id
        """
        try:
            conn = self.user_attributes().get_default_connection()
            if conn:
                return conn["value"]["defaultDatasetConnectionId"]
            else:
                return None
        except:  # noqa # NOSONAR
            return None

    @staticmethod
    def __remove_cached_token():
        if os.path.exists(TmoClient.DEFAULT_TOKEN_CACHE_FILE_PATH):
            os.remove(TmoClient.DEFAULT_TOKEN_CACHE_FILE_PATH)

    def __save_signed_jwt(self, signed_jwt, exp):
        try:
            os.makedirs(
                os.path.dirname(self.DEFAULT_TOKEN_CACHE_FILE_PATH), exist_ok=True
            )

            with open(self.DEFAULT_TOKEN_CACHE_FILE_PATH, "w") as f:
                json.dump({"token": signed_jwt, "exp": exp}, f)
            self.logger.debug("Token saved successfully.")
        except Exception as e:
            self.logger.error(f"Failed to save token: {e}")

    def __validate_stored_token(self):
        stored_token = None
        if os.path.exists(self.DEFAULT_TOKEN_CACHE_FILE_PATH):
            self.logger.debug(
                f"Loading cached token data from {self.DEFAULT_TOKEN_CACHE_FILE_PATH}"
            )
            with open(self.DEFAULT_TOKEN_CACHE_FILE_PATH, "r") as f:
                stored_token = json.load(f)

        token = None
        # Clean up token if expired
        if stored_token:
            # in case an old bearer token is stored or if the token is expired
            if "exp" not in stored_token or stored_token["exp"] <= time.time():
                self.logger.debug("Token expired. Refreshing token")
                self.__remove_cached_token()
            else:
                token = stored_token["token"]

        if not token:
            self.logger.debug("No valid token found. Generating new token.")
            token = self.__create_self_signed_jwt()

        # Ensure the session is updated with the new or existing valid token
        if not hasattr(self, "session"):
            self.session = requests.Session()
            self.__set_session_tls()

        self.session.headers.update({"Authorization": f"Bearer {token}"})


@deprecated(
    "AoaClient is deprecated, please use TmoClient instead.",
    category=DeprecationWarning,
)
class AoaClient(TmoClient):
    pass
