from cnvrgv2.config import routes, error_messages
from cnvrgv2.config.error_messages import FAULTY_KEY
from cnvrgv2.proxy import Proxy, HTTP
from cnvrgv2.context import Context, SCOPE
from cnvrgv2.modules.base.data_owner import DataOwner
from cnvrgv2.utils.json_api_format import JAF
from cnvrgv2.utils.url_utils import urljoin
from cnvrgv2.utils.validators import attributes_validator, validate_secret_key
from cnvrgv2.errors import CnvrgArgumentsError, CnvrgFileError


class ProjectSettings(DataOwner):
    available_attributes = {
        "title": str,
        "default_image": str,
        "privacy": str,
        "mount_folders": list,
        "env_variables": list,
        "check_stuckiness": bool,
        "max_restarts": int,
        "stuck_time": int,
        "autosync": bool,
        "sync_time": int,
        "default_computes": list,
        "use_org_deploy_key": bool,
        "deploy_key": str,
        "webhooks_url": str,
        "slack_webhooks": bool,
        "slack_webhook_channel": str,
        "command_to_execute": str,
        "run_tensorboard_by_default": bool,
        "run_jupyter_by_default": bool,
        "email_on_error": bool,
        "email_on_success": bool,
        "working_directory": str,
        "requirements_path": str,
        "secrets": list,
        "project_idle_time": float,
        "is_git": bool,
        "git_repo": str,
        "git_branch": str,
        "private_repo": bool,
        "description": str,
        "tags": list,
        "collaborators": list,
        "git_access_token": bool,
        "output_dir": str
    }

    def __init__(self, project):
        self._context = Context(context=project._context)
        scope = self._context.get_scope(SCOPE.PROJECT)

        self._proxy = Proxy(context=self._context)

        org_base = routes.PROJECT_BASE.format(scope["organization"], scope["project"])
        self._route = urljoin(org_base, "settings")

        self._attributes = {}

    def save(self):
        """
        Save the local settings in the current project
        @return: None
        """
        valid_attributes = {**self._attributes}

        # Secrets are being updates in a separate function
        if valid_attributes.get("secrets") is not None:
            del valid_attributes["secrets"]

        self.update(**valid_attributes)

    def update(self, **kwargs):
        """
        Updates current project's settings with the given params
        @param kwargs: any param out of the available attributes can be sent
        @return: None
        """
        attributes_validator(
            available_attributes=ProjectSettings.available_attributes,
            attributes=kwargs,
        )

        if "secrets" in kwargs:
            raise CnvrgArgumentsError(error_messages.SECRETS_NOT_SUPPORTED.format("secrets"))

        response = self._proxy.call_api(
            route=self._route,
            http_method=HTTP.POST,
            payload=JAF.serialize(type="settings", attributes={**self._attributes, **kwargs})
        )

        response_attributes = response.attributes
        response_attributes.pop('slug', None)
        self._attributes = response_attributes

    def update_secret(self, secret_key, secret_value, force=False):
        """
        update or add a single secret
        @param secret_key: [String] Secret Key
        @param secret_value: [String] Secret Value
        @param force: Override existing secrets
        @return: None
        """
        if not validate_secret_key(secret_key):
            raise CnvrgArgumentsError(FAULTY_KEY.format(secret_key))

        update_secret_url = urljoin(self._route, routes.PROJECT_UPDATE_SECRET)

        self._proxy.call_api(
            route=update_secret_url,
            http_method=HTTP.POST,
            payload=JAF.serialize(type="settings", attributes={
                "secret_key": secret_key,
                "secret_value": secret_value,
                "force": force
            })
        )

    def delete_secret(self, secrets):
        """
        delete single or list of secrets
        @param secrets: [List] of Keys
        @return: None
        """
        if isinstance(secrets, str):
            secrets = [secrets]

        delete_secret_url = urljoin(self._route, routes.PROJECT_DELETE_SECRET)

        self._proxy.call_api(
            route=delete_secret_url,
            http_method=HTTP.POST,
            payload=JAF.serialize(type="settings", attributes={"secrets": secrets})
        )

    def setup_git(self, git_repo, branch, token=None, ssh_key=None, ssh_key_type="plain"):
        if all([token, ssh_key]):
            raise CnvrgArgumentsError(error_messages.CANT_USE_BOTH_SSH_AND_TOKEN)

        if ssh_key_type not in ("plain", "file"):
            raise CnvrgArgumentsError(error_messages.INVALID_SSH_KEY_TYPE)

        if ssh_key_type == "file" and ssh_key is not None:
            try:
                with open(ssh_key, "r") as file:
                    ssh_key = file.read()
            except Exception:
                raise CnvrgFileError(error_messages.CANT_READ_SSH_KEY_FILE)

        if ssh_key is not None:
            authentication_method = "sshKey"
        elif token is not None:
            authentication_method = "token"
        else:
            authentication_method = "public"

        self._proxy.call_api(route=urljoin(self._route, routes.GIT), http_method=HTTP.POST, payload={
            "git_repo": git_repo,
            "branch": branch,
            "token": token,
            "ssh_key": ssh_key,
            "authentication_method": authentication_method
        })
        self.reload()

    def remove_git(self):
        self._proxy.call_api(route=urljoin(self._route, routes.GIT), http_method=HTTP.DELETE)
        self._attributes.pop("git_repo", None)
        self._attributes.pop("git_branch", None)
        self._attributes.pop("is_git", None)
