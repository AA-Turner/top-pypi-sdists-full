import os
import sys
import tempfile
import agilicus
import yaml

from . import apps, context, files
from .output.table import (
    format_table,
    column,
)

# Fields the tools below carry forward from the configuration already on the
# server. mount_password is left out on purpose: the API keeps a field that the
# body omits, so there is no reason to send a stored credential back.
MOUNT_FIELDS = (
    "mount_domain",
    "mount_hostname",
    "mount_share",
    "mount_src_path",
    "mount_username",
    "mount_path",
)

# Fields the server returns but the generated model marks read only, so they
# cannot be set on a request body.
READ_ONLY_FIELDS = ("id", "app_id", "environment_name")


def _without_none(values):
    """Drop unset values: the generated models reject None for optional
    fields even though the API treats a missing field as "unchanged"."""
    return {key: value for key, value in values.items() if value is not None}


def add(
    ctx,
    application,
    env_name,
    org_id=None,
    config_type=None,
    mount_src_path=None,
    username=None,
    password=None,
    share=None,
    domain=None,
    hostname=None,
    file_store_uri=None,
    filename=None,
    env_config_vars=None,
    **kwargs,
):
    token = context.get_token(ctx)
    if not org_id:
        org_id = context.get_org_id(ctx, token)

    if filename:
        _file = files.upload(
            ctx,
            filename,
            org_id=org_id,
            label=config_type,
            tag=env_name,
            name=os.path.basename(filename),
        )
        file_store_uri = f"/v1/files/{_file['id']}"

    app = apps.get_app(ctx, org_id, application, maintained=True)
    config = {
        "maintenance_org_id": org_id,
        "config_type": config_type,
        "mount_src_path": mount_src_path,
        "mount_username": username,
        "mount_password": password,
        "mount_share": share,
        "mount_domain": domain,
        "mount_hostname": hostname,
        "file_store_uri": file_store_uri,
        "env_config_vars": env_config_vars,
        **kwargs,
    }
    _config = agilicus.EnvironmentConfig(**_without_none(config))
    apiclient = context.get_apiclient(ctx, token)
    return apiclient.application_api.add_config(app["id"], env_name, _config)


def update(
    ctx,
    application,
    env_name,
    id,
    org_id=None,
    config_type=None,
    mount_path=None,
    file_store_uri=None,
    env_config_vars=None,
    **kwargs,
):
    token = context.get_token(ctx)
    if not org_id:
        org_id = context.get_org_id(ctx, token)

    app = apps.get_app(ctx, org_id, application, maintained=True)

    apiclient = context.get_apiclient(ctx, token)
    _config = apiclient.application_api.get_config(
        app["id"], env_name, id, maintenance_org_id=org_id
    )

    # Start from what the server already holds so that a partial update never
    # strips a mount point, a file backed configuration or the variables of a
    # configuration this command is not touching.
    config = {
        "maintenance_org_id": org_id,
        "config_type": config_type or _config.config_type,
    }
    for key in MOUNT_FIELDS + ("file_store_uri", "env_config_vars"):
        value = getattr(_config, key, None)
        if value is not None:
            config[key] = value

    overrides = {
        key: value for key, value in kwargs.items() if key not in READ_ONLY_FIELDS
    }
    config.update(
        _without_none(
            {
                "config_type": config_type,
                "mount_path": mount_path,
                "file_store_uri": file_store_uri,
                "env_config_vars": env_config_vars,
                **overrides,
            }
        )
    )

    _update = agilicus.EnvironmentConfig(**config)
    return apiclient.application_api.replace_config(app["id"], env_name, id, _update)


def delete(ctx, application, env_name, id, org_id=None, **kwargs):
    token = context.get_token(ctx)
    if not org_id:
        org_id = context.get_org_id(ctx, token)

    app = apps.get_app(ctx, org_id, application, maintained=True)
    apiclient = context.get_apiclient(ctx, token)

    _config = apiclient.application_api.get_config(
        app["id"], env_name, id, maintenance_org_id=org_id
    )

    if _config.file_store_uri:
        file_id = os.path.basename(_config.file_store_uri)
        try:
            files.delete(ctx, file_id, org_id=org_id, _continue_on_error=True)
        except Exception:
            print(f"Failed to delete the {_config.file_store_uri}")

    return apiclient.application_api.delete_config(app["id"], env_name, id, org_id)


def query(ctx, application, env_name, org_id=None, **kwargs):
    token = context.get_token(ctx)
    if not org_id:
        org_id = context.get_org_id(ctx, token)

    app = apps.get_app(ctx, org_id, application, maintained=True)
    apiclient = context.get_apiclient(ctx, token)
    return apiclient.application_api.list_configs(app["id"], env_name, org_id).configs


def convert_to_env_config_var(env_config_dict):
    env_list = []
    for k, v in env_config_dict.items():
        env_var_obj = agilicus.EnvironmentConfigVar(name=k, value=v)
        env_list.append(env_var_obj)
    return env_list


class EnvVarConfigObj:
    def __init__(self, ctx, application, env_name, org_id=None, secret=False):
        self.ctx = ctx
        self.application = application
        self.env_name = env_name
        self.org_id = org_id
        if secret:
            self.env_file = "secret-env.yaml"
            self.config_type = "secret_env"
        else:
            self.env_file = "config-env.yaml"
            self.config_type = "configmap_env"
        self.env_config = None
        self.old_file_envs = {}
        self.old_env_configs = {}
        self.env_vars = {}
        self.env_var_list = []
        self.build_env_list()

    def get_env_list(self):
        return self.env_var_list

    def get_old_env(self, env_config_vars):
        self.old_env_configs = {}
        if env_config_vars:
            for env in env_config_vars:
                self.old_env_configs[env.name] = env.value

    def merge_env(self, file_env, env_config):
        self.env_vars = dict(file_env or {})
        self.env_vars.update(env_config or {})

    def build_env_list(self):
        configs = query(self.ctx, self.application, self.env_name, self.org_id)
        for config in configs:
            if config.config_type.upper() == self.config_type.upper():
                if config.file_store_uri:
                    with tempfile.TemporaryDirectory() as tempdir:
                        destination = os.path.join(tempdir, self.env_file)
                        files.download(
                            self.ctx,
                            os.path.basename(config.file_store_uri),
                            org_id=self.org_id,
                            destination=destination,
                        )
                        with open(destination) as stream:
                            self.old_file_envs = yaml.safe_load(stream) or {}
                self.get_old_env(config.env_config_vars)
                self.merge_env(self.old_file_envs, self.old_env_configs)
                self.env_var_list = convert_to_env_config_var(self.env_vars)
                self.env_config = config
                return

    def write_env_vars(self, data):
        self.env_vars.update(data)

    def write_env_list(self):
        if self.config_type.upper() != "SECRET_ENV":
            # The API only returns env_config_vars for secret_env, so the
            # current variables of any other config type cannot be read back.
            # Writing would replace every variable on the workload with just
            # the ones named in this command.
            raise RuntimeError(
                "{} variables cannot be read back, so replacing them would "
                "discard the ones this command does not name; use the secret "
                "environment variables (the default) instead".format(self.config_type)
            )
        self.env_var_list = convert_to_env_config_var(self.env_vars)
        self.warn_about_removed_file_vars()

        if not self.env_config and not self.env_vars:
            return

        if not self.env_config:
            self.env_config = add(
                self.ctx,
                self.application,
                self.env_name,
                org_id=self.org_id,
                config_type=self.config_type,
                env_config_vars=self.env_var_list,
            )
        elif not self.env_vars:
            # replace_config ignores an empty env_config_vars list, and
            # deleting the configuration is the only way to clear the
            # variables off the workload.
            delete(
                self.ctx,
                self.application,
                self.env_name,
                self.env_config.id,
                self.org_id,
            )
            self.env_config = None
        else:
            # Update in place: a delete followed by an add leaves a window in
            # which the environment has no configuration at all, and the
            # delete clears the variables off the workload before the add can
            # put them back.
            self.env_config = update(
                self.ctx,
                self.application,
                self.env_name,
                self.env_config.id,
                org_id=self.org_id,
                config_type=self.config_type,
                env_config_vars=self.env_var_list,
            )
        self.verify_env_list()

    def warn_about_removed_file_vars(self):
        """A file backed configuration keeps defining the variables in its
        file, so removing one from the inline list does not remove it from the
        environment."""
        if not getattr(self.env_config, "file_store_uri", None):
            return
        removed = sorted(set(self.old_file_envs) - set(self.env_vars))
        if not removed:
            return
        print(
            "warning: {} is still defined by {}; delete the configuration to "
            "remove it".format(", ".join(removed), self.env_config.file_store_uri),
            file=sys.stderr,
        )

    def verify_env_list(self):
        """Read the variables back: the API's view, not our request, is what
        the workload will run with."""
        if self.config_type.upper() != "SECRET_ENV":
            # list_configs only echoes env_config_vars for secret_env
            return
        configs = query(self.ctx, self.application, self.env_name, self.org_id)
        for config in configs:
            if config.config_type.upper() != self.config_type.upper():
                continue
            server_vars = getattr(config, "env_config_vars", None)
            if server_vars is None:
                return
            server = {var.name: var.value for var in server_vars}
            if server == self.env_vars:
                return
            raise RuntimeError(
                "environment {} on {} does not match after write: missing {}, "
                "unexpected {}, changed {}".format(
                    self.env_name,
                    self.application,
                    sorted(set(self.env_vars) - set(server)),
                    sorted(set(server) - set(self.env_vars)),
                    sorted(
                        name
                        for name in set(self.env_vars) & set(server)
                        if server[name] != self.env_vars[name]
                    ),
                )
            )

    def add_env_var(self, env_name, env_value):
        env_data = {}
        env_data[env_name] = env_value
        self.write_env_vars(env_data)
        self.write_env_list()

    def del_env_var(self, env_var_name):
        self.env_vars.pop(env_var_name, None)
        self.write_env_list()

    def update_env_var(self, env_config_name, env_config_value):
        env_data = {}
        env_data[env_config_name] = env_config_value
        self.write_env_vars(env_data)
        self.write_env_list()


def format_env_vars_as_text(ctx, env_vars):
    columns = [
        column("name"),
        column("value"),
    ]
    return format_table(ctx, env_vars, columns)
