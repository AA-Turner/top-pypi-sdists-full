import os
import pathlib
import shutil

import boto3.session
from dict_tools.data import NamespaceDict

try:
    import tqdm

    HAS_LIBS = (True,)
except ImportError as e:
    HAS_LIBS = False, str(e)


def __virtual__(hub):
    return HAS_LIBS


def __init__(hub):
    hub.pop.sub.load_subdirs(hub.pop_create.aws)


def context(hub, ctx, directory: pathlib.Path):
    ctx = hub.pop_create.idem_cloud.init.context(ctx, directory)
    ctx.servers = [None]

    # AWS already has an acct plugin
    ctx.has_acct_plugin = False
    ctx.service_name = "aws_auto"

    if not ctx.get("templates_dir", None):
        # Use default templates
        ctx["templates_dir"] = (
            os.path.dirname(os.path.realpath(__file__))
            + "/{{cookiecutter.root_dir}}/{{cookiecutter.clean_name}}/autogen/{{cookiecutter.service_name}}/templates/"
        )

    # Copy the templates into directory (aka temporary project folder)
    target = f"{directory}/{ctx.clean_name}/autogen/{ctx.service_name}/templates"
    shutil.copytree(ctx.get("templates_dir"), target, dirs_exist_ok=True)

    # Now start getting into AWS resource plugin creation
    session = boto3.session.Session()

    # If CLI provides services then use those services first
    # e.g. --services rds
    services = hub.OPT.pop_create.services or session.get_available_services()
    # This takes a while because we are making http calls to aws
    for aws_service_name in tqdm.tqdm(services, desc="services"):
        # Clean out the service name
        aws_service_name = (
            aws_service_name.lower().strip().replace(" ", "_").replace("-", "_")
        )
        aws_service_name = hub.tool.format.keyword.unclash(aws_service_name)

        # Get supported operations for this service
        resource_operations = hub.pop_create.aws.service.parse_resource_and_operations(
            service_name=aws_service_name,
            session=session,
        )

        requested_service_resources = hub.OPT.pop_create.service_resources
        if bool(requested_service_resources):
            # if the CLI provides resources, filter the list of resources to process
            # e.g. --service_resources db_cluster db_instance
            resource_operations = {
                r: resource_operations[r]
                for r in requested_service_resources
                if r in resource_operations
            }

        resource_modules = {}
        for resource_name, functions in tqdm.tqdm(
            resource_operations.items(), desc="operations"
        ):
            # Clean out resource name
            resource_name = (
                resource_name.lower().strip().replace(" ", "_").replace("-", "_")
            )

            # Check if the plugin should be created
            #   - see if it exists
            #   - or --overwrite flag is used
            resource_plugin_exists = hub.pop_create.aws.init.plugin_exists(
                ctx, aws_service_name, resource_name
            )
            should_create_resource_plugin = (
                ctx.overwrite_existing or not resource_plugin_exists
            )

            if should_create_resource_plugin:
                # parse known or commonly used resource actions for the resource
                resource_functions = hub.pop_create.aws.resource.parse_functions(
                    session,
                    aws_service_name,
                    resource_name,
                    functions,
                )

                # create shared resource data to be used when creating resource plugins
                shared_resource_data = {
                    "aws_service_name": aws_service_name,
                    "resource_name": resource_name,
                    "functions": resource_functions,
                }

                # get resource exec, state, and tool modules
                resource_modules[
                    f"{aws_service_name}.{resource_name}"
                ] = hub.pop_create.aws.plugin.create_resource_plugin(
                    ctx, shared_resource_data
                )

        # There could be lot many resources in a given service, so it generates code for them
        hub.pop_create.aws.init.generate_resource_modules(
            ctx, directory, aws_service_name, resource_modules
        )

        # Now generate any service related modules e.g. tags
        hub.pop_create.aws.init.generate_service_tag_modules(
            ctx, directory, aws_service_name, session
        )

    return ctx


def plugin_exists(hub, ctx, aws_service_name: str, resource_name: str) -> bool:
    """
    Validate if the plugin path exists based on create plugin
    """
    path = pathlib.Path(ctx.target_directory).absolute() / ctx.clean_name
    if "auto_state" in ctx.create_plugin:
        path = path / "exec"
    elif "state_modules" in ctx.create_plugin:
        path = path / "states"
    elif "tests" in ctx.create_plugin:
        path = path / "tests" / "integration" / "states"

    path = path / aws_service_name / f"{resource_name}.py"
    if path.exists():
        hub.log.info(f"Plugin already exists at '{path}', use `--overwrite` to modify")
        return True

    return False


def generate_resource_modules(
    hub, ctx, directory: str, resource_name: str, resource_plugins: dict
):
    try:
        ctx.cloud_spec = NamespaceDict(
            api_version="",
            project_name=ctx.project_name,
            service_name=ctx.service_name,
            request_format={},
            plugins=resource_plugins,
        )

        # pop-create CLI config '--create-plugin' supports 'auto_states', 'exec_modules', 'sls' or 'templates'
        # The following translates it to CloudSpec's create_plugin and runs the code generation from CloudSpec:
        if ctx.create_plugin in ["auto_states", "exec_modules"]:
            hub.cloudspec.init.run(
                ctx,
                directory,
                # exec_modules creates functions for everything except present/absent/describe
                # auto_state creates functions for get/create/update/list/delete
                # tool creates functions for everything which is NOT present/absent/describe/get/create/update/list/delete
                create_plugins=["auto_state", "tool", "tests"],
            )
        elif ctx.create_plugin == "state_modules":
            hub.cloudspec.init.run(
                ctx,
                directory,
                create_plugins=["auto_state", "tool", "state_modules", "sls", "tests"],
            )
        elif ctx.create_plugin == "sls":
            hub.cloudspec.init.run(
                ctx,
                directory,
                create_plugins=["sls"],
            )
        elif ctx.create_plugin == "templates":
            hub.cloudspec.init.run(
                ctx,
                directory,
                create_plugins=["templates"],
            )
        elif ctx.create_plugin == "test_modules":
            hub.cloudspec.init.run(
                ctx,
                directory,
                create_plugins=["tests"],
            )
        else:
            raise ValueError(
                f"Invalid input '{ctx.create_plugin}' for --create-plugin."
            )
    finally:
        hub.log.info(
            f"Finished generating modules for service [{resource_name}] with create plugin {ctx.create_plugin}]"
        )
        # Reset it for the next resource or plugin
        ctx.cloud_spec = None


def generate_service_tag_modules(
    hub,
    ctx,
    directory,
    aws_service_name: str,
    session: "boto3.session.Session",
):
    try:
        # Get service modules e.g. tag
        service_tag_methods = hub.pop_create.aws.service.parse_service_tag_methods(
            session=session,
            aws_service_name=aws_service_name,
        )

        service_tag_plugin = {
            f"{aws_service_name}.tag": hub.pop_create.aws.plugin.create_tags_plugin(
                aws_service_name, service_tag_methods
            )
        }

        ctx.cloud_spec = NamespaceDict(
            api_version="",
            project_name=ctx.project_name,
            service_name=ctx.service_name,
            request_format={},
            plugins=service_tag_plugin,
        )

        # Tags would go under tool modules
        hub.cloudspec.init.run(
            ctx,
            directory,
            create_plugins=["tool"],
        )
    finally:
        hub.log.info(
            f"Finished generating tag modules for service [{aws_service_name}]"
        )
        # Reset it for the next resource or plugin
        ctx.cloud_spec = None
