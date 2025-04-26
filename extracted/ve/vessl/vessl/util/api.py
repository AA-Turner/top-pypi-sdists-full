import functools
import inspect
import os
import time
from typing import Optional

from openapi_client import ApiClient, APIV1Api, Configuration, ExecAPIV1Api
from openapi_client.exceptions import ApiException
from openapi_client.models import (
    ResponseMyUser,
    ResponseOrganization,
    ResponseProjectInfo,
)
from vessl._version import __VERSION__
from vessl.util.browser import try_open_gui_browser
from vessl.util.config import VesslConfigLoader
from vessl.util.constant import (
    ACCESS_TOKEN_ENV_VAR,
    API_HOST,
    CLUSTER_KUBECONFIG_ENV_VAR,
    CREDENTIALS_FILE_ENV_VAR,
    DEFAULT_ORGANIZATION_ENV_VAR,
    DEFAULT_PROJECT_ENV_VAR,
    JWT_PATH,
    LOGIN_TIMEOUT_SECONDS,
    PROJECT_NAME_ENV_VAR,
    VESSL_LOG_LEVEL,
    VESSL_LOG_LEVEL_DEBUG,
    WEB_HOST, MODEL_SERVICE_JOIN_TOKEN_ENV_VAR,
)
from vessl.util.exception import (
    GitError,
    InvalidOrganizationError,
    InvalidProjectError,
    InvalidTokenError,
    VesslApiException,
    VesslException,
    VesslRuntimeException,
)
from vessl.util.git_local_repo import GitRepository


def raise_vessl_exception(f):
    @functools.wraps(f)
    def func(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ApiException as e:
            raise VesslApiException.convert_api_exception(e) from None

    return func


class VesslApi(APIV1Api, ExecAPIV1Api):
    """VESSL Client API"""

    def __init__(self, *, api_host=API_HOST, **kwargs):
        _api_configuration = Configuration(host=api_host)
        # Disable verify ssl (https://github.com/urllib3/urllib3/issues/1682#issuecomment-533311857) # noqa E501
        _api_configuration.verify_ssl = False
        _api_configuration.client_side_validation = False
        if VESSL_LOG_LEVEL == VESSL_LOG_LEVEL_DEBUG:
            _api_configuration.debug = True

        Configuration.set_default(_api_configuration)

        _api_client = ApiClient(configuration=_api_configuration)
        import urllib3

        urllib3.disable_warnings()

        for k, v in kwargs:
            _api_client.set_default_header(k, v)
        _api_client.set_default_header("X-Source", "sdk")
        _api_client.set_default_header("X-Version", __VERSION__)
        _api_client.set_default_header("Accept-Encoding", "gzip, deflate, br")
        _api_client.user_agent = f"vessl/{__VERSION__}"
        super().__init__(_api_client)

        # `predicate=inspect.isfunction` does not work for some reason.
        # For more info: https://stackoverflow.com/q/17019949
        for name, value in inspect.getmembers(self, predicate=inspect.ismethod):
            if name.endswith("api"):
                setattr(self, name, raise_vessl_exception(value))

        self.user: ResponseMyUser = None
        self.organization: ResponseOrganization = None
        self.project: ResponseProjectInfo = None
        self.default_git_repo: GitRepository = None

        self.run_execution_default_organization = None
        self.run_execution_default_project = None
        self.run_execution_access_token = None
        self.initialize_run_execution_token()

        self.config_loader = VesslConfigLoader()
        self.cluster_kubeconfig = self.config_loader.cluster_kubeconfig

        try:
            self.set_access_token(no_prompt=True)
            if self.config_loader.default_organization is not None:
                self.set_organization(self.config_loader.default_organization)

            if self.config_loader.default_project is not None:
                self.set_project(self.config_loader.default_project)
        except VesslException:
            pass

        self._initialize_git_repo()

    @staticmethod
    def is_in_run_exec_context() -> bool:
        return os.environ.get("VESSL_RUN_INITIAL_CONFIG") is not None

    def initialize_run_execution_token(self) -> None:
        if not self.is_in_run_exec_context():
            return
        initial_config_path = os.environ.get("VESSL_RUN_INITIAL_CONFIG")
        initial_config = VesslConfigLoader(initial_config_path)
        self.run_execution_access_token = initial_config.access_token
        self.run_execution_default_organization = initial_config.default_organization
        self.run_execution_default_project = initial_config.default_project
        try:
            with open(JWT_PATH, "r") as f:
                access_token = f.read().strip()
                self.run_execution_access_token = access_token
        except FileNotFoundError:
            pass

    def configure(
        self,
        *,
        access_token: str = None,
        organization_name: str = None,
        project_name: str = None,
        credentials_file: str = None,
        force_update_access_token: bool = False,
    ) -> None:
        """Configure VESSL Client API.

        Args:
            access_token(str): Access token to override. Defaults to
                `access_token` from `~/.vessl/config`.
            organization_name(str): Organization name to override. Defaults to
                `organization_name` from `~/.vessl/config`.
            project_name(str): Project name to override. Defaults to
                `project name` from `~/.vessl/config`.
            credentials_file(str): Defaults to None.
            force_update_access_token(bool): True if force update access token,
                False otherwise. Defaults to False.

        Example:
            ```python
            vessl.configure()
            ```
        """
        if self.is_in_run_exec_context():
            print("This environment is currently connected to VESSL with VESSL Run context.")
            print("You can manually configure VESSL SDK, but it will break some run functions (e.g. vessl.log())")
            print("Please refer https://docs.vessl.ai/api-reference/cli/getting-started#configuration-precedence.")
            return
    
        self.configure_access_token(access_token, credentials_file, force_update_access_token)
        self.configure_default_organization(organization_name, credentials_file)

        try:
            self.configure_default_project(project_name, credentials_file)
        except InvalidProjectError:
            # Project is not mandatory
            pass

        print(
            f"""Username: {self.user.username}
Email: {self.user.email}
Default organization: {self.organization.name}
Default project: {'N/A' if self.project is None else self.project.name}"""
        )

    def _initialize_git_repo(self) -> None:
        try:
            self.default_git_repo = GitRepository()
        except GitError:
            return

    def _get_new_access_token(self) -> str:
        cli_token = self.sign_in_cli_token_api().cli_token
        url = f"{WEB_HOST}/cli/grant-access?token={cli_token}"

        try:
            try_open_gui_browser(url)
        finally:
            print(
                f"Please grant CLI access from the URL below.\n" f"{url}\n\nWaiting...\n",
            )

        start_time = time.time()
        while time.time() - start_time < LOGIN_TIMEOUT_SECONDS:
            response = self.sign_in_cli_check_api(cli_token)
            if response.signin_success:
                return response.access_token
            time.sleep(3)

        raise TimeoutError("Login timeout. Please try again.")

    def find_access_token(
        self,
        access_token: str = None,
        credentials_file: str = None,
        force_update: bool = False,
        no_prompt: bool = False,
    ) -> str:
        if force_update:
            return self._get_new_access_token()

        if access_token is not None:
            return access_token

        if credentials_file is not None:
            return VesslConfigLoader(credentials_file).access_token

        if os.environ.get(ACCESS_TOKEN_ENV_VAR):
            return os.environ.get(ACCESS_TOKEN_ENV_VAR)

        if os.environ.get(CREDENTIALS_FILE_ENV_VAR):
            file = os.environ.get(CREDENTIALS_FILE_ENV_VAR)
            return VesslConfigLoader(file).access_token

        if self.config_loader.access_token:
            return self.config_loader.access_token

        if self.run_execution_access_token:
            return self.run_execution_access_token

        if not no_prompt:
            return self._get_new_access_token()
        raise InvalidTokenError("No access token found.")

    def find_model_service_join_token(self):
        if os.environ.get(MODEL_SERVICE_JOIN_TOKEN_ENV_VAR):
            return os.environ.get(MODEL_SERVICE_JOIN_TOKEN_ENV_VAR)
        raise InvalidTokenError("No access token found.")

    def find_organization_name(
        self, organization_name: str = None, credentials_file: str = None
    ) -> str:
        if organization_name is not None:
            return organization_name

        if credentials_file is not None:
            return VesslConfigLoader(credentials_file).default_organization

        if os.environ.get(DEFAULT_ORGANIZATION_ENV_VAR):
            return os.environ.get(DEFAULT_ORGANIZATION_ENV_VAR)

        if os.environ.get(CREDENTIALS_FILE_ENV_VAR):
            file = os.environ.get(CREDENTIALS_FILE_ENV_VAR)
            return VesslConfigLoader(file).default_organization

        if self.config_loader.default_organization:
            return self.config_loader.default_organization

        if self.run_execution_default_organization:
            return self.run_execution_default_organization

        raise InvalidOrganizationError("Please specify an organization.")

    def find_project_name(self, project_name: str = None, credentials_file: str = None) -> str:
        if project_name is not None:
            return project_name

        if credentials_file is not None:
            return VesslConfigLoader(credentials_file).default_project

        if os.environ.get(CREDENTIALS_FILE_ENV_VAR):
            file = os.environ.get(CREDENTIALS_FILE_ENV_VAR)
            return VesslConfigLoader(file).default_project

        if os.environ.get(DEFAULT_PROJECT_ENV_VAR):
            return os.environ.get(DEFAULT_PROJECT_ENV_VAR)

        if os.environ.get(PROJECT_NAME_ENV_VAR):
            return os.environ.get(PROJECT_NAME_ENV_VAR)

        if self.config_loader.default_project:
            return self.config_loader.default_project

        if self.run_execution_default_project:
            return self.run_execution_default_project

        raise InvalidProjectError("Please specify a project.")

    def find_cluster_kubeconfig(
        self, kubeconfig_path: str = None, credentials_file: str = None
    ) -> str:
        if kubeconfig_path is not None:
            return kubeconfig_path

        if credentials_file is not None:
            return VesslConfigLoader(credentials_file).cluster_kubeconfig

        if os.environ.get(CLUSTER_KUBECONFIG_ENV_VAR):
            return os.environ.get(CLUSTER_KUBECONFIG_ENV_VAR)

        if os.environ.get(CREDENTIALS_FILE_ENV_VAR):
            file = os.environ.get(CREDENTIALS_FILE_ENV_VAR)
            return VesslConfigLoader(file).cluster_kubeconfig

        if self.config_loader.cluster_kubeconfig:
            return self.config_loader.cluster_kubeconfig

        raise VesslRuntimeException("No Kubernetes cluster found.")

    def set_access_token(
        self,
        access_token: str = None,
        credentials_file: str = None,
        force_update: bool = False,
        no_prompt: bool = False,
    ) -> str:
        access_token = self.find_access_token(
            access_token,
            credentials_file,
            force_update,
            no_prompt,
        )
        self.api_client.set_default_header(
            "Authorization",
            f"Token {access_token}",
        )

        try:
            self.user = self.get_my_user_info_api()
        except VesslApiException as e:
            self.api_client.set_default_header("Authorization", "")
            raise InvalidTokenError("Expired. Please renew your access token.")

        return access_token

    def set_organization(self, organization_name: str = None, credentials_file: str = None) -> str:
        organization_name = self.find_organization_name(organization_name, credentials_file)
        if organization_name:
            try:
                self.organization = self.organization_read_api(organization_name=organization_name)
                return self.organization.name
            except VesslApiException as e:
                raise InvalidOrganizationError(f"Invalid organization {organization_name}.")

        organizations = self.organization_list_api().organizations
        if len(organizations) == 0:
            raise InvalidOrganizationError(
                "No organizations. Create one using vessl.create_organization.",  # TODO: update message
            )
        self.organization = organizations[0]
        return self.organization.name

    def set_project(self, project_name: str = None, credentials_file: str = None) -> Optional[str]:
        if self.organization is None:
            raise InvalidOrganizationError("Please specify an organization first.")

        projects = self.project_list_api(organization_name=self.organization.name).results
        if len(projects) == 0:
            return None

        if len(projects) == 1 and project_name is None:
            project_name = projects[0].name
        elif len(projects) > 1:
            project_name = self.find_project_name(project_name, credentials_file)

        for project in projects:
            if project.name == project_name:
                self.project = project
                break
        else:
            raise InvalidProjectError(
                f'Invalid project "{project_name}".',
            )

        return project_name

    def reconfigure_access_token_on_jwt_refresh(
        self,
        access_token: str = None,
    ) -> None:
        self.run_execution_access_token = access_token
        self.set_access_token(no_prompt=True)

    def configure_jwt_access_token(self, access_token: str):
        with open(JWT_PATH, "w") as f:
            f.write(access_token)

    def configure_access_token(
        self,
        access_token: str = None,
        credentials_file: str = None,
        force_update: bool = False,
    ) -> None:
        access_token = self.set_access_token(access_token, credentials_file, force_update)
        self.config_loader.access_token = access_token

    def configure_default_organization(
        self, organization_name: str = None, credentials_file: str = None
    ) -> None:
        organization_name = self.set_organization(organization_name, credentials_file)
        self.config_loader.default_organization = organization_name

    def configure_default_project(
        self, project_name: str = None, credentials_file: str = None
    ) -> None:
        project_name = self.set_project(project_name, credentials_file)
        self.config_loader.default_project = project_name
