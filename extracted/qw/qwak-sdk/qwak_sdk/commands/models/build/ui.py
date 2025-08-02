import click
from qwak.inner.build_config.build_config_v1 import (
    BuildConfigV1,
    BuildProperties,
    DockerConf,
    ModelUri,
    RemoteBuildResources,
)
from qwak.inner.build_logic.execute_build_pipeline import execute_build_pipeline
from qwak.inner.build_logic.run_handlers.programmatic_phase_run_handler import (
    ProgrammaticPhaseRunHandler,
)
from qwak.inner.const import QwakConstants

from qwak_sdk.commands.models.build._logic.build_steps import create_pipeline
from qwak_sdk.commands.models.build._logic.wait_until_finished import wait_until_finished, is_final_status_successful
from qwak_sdk.commands.models.build._logic.client_logs.cli_phase_run_handler import (
    CLIPhaseRunHandler,
)
from qwak_sdk.commands.models.build._logic.client_logs.logger import get_build_logger
from qwak_sdk.commands.models.build._logic.client_logs.utils import zip_logs
from qwak_sdk.inner.tools.cli_tools import QwakCommand
from qwak_sdk.inner.tools.config_handler import config_handler


@click.command("build", cls=QwakCommand)
@click.option(
    "--model-id",
    metavar="NAME",
    required=False,
    help="Model ID to assign the build for",
)
@click.option(
    "--main-dir",
    metavar="NAME",
    help=f"Model main directory name, [Default: {ModelUri.main_dir}]",
)
@click.option(
    "-P",
    "--param-list",
    required=False,
    metavar="NAME=VALUE",
    multiple=True,
    help="A parameter for the build, of the form -P name=value. the params will be saved and can be viewed later",
)
@click.option(
    "-E",
    "--env-vars",
    required=False,
    metavar="NAME=VALUE",
    multiple=True,
    help="A parameter for the build, of the form -E name=value",
)
@click.option(
    "-T",
    "--tags",
    required=False,
    multiple=True,
    help="A tag for the model build",
)
@click.option(
    "--git-credentials",
    required=False,
    metavar="USERNAME:ACCESS_TOKEN",
    help="Access credentials for private repositories listed in the python dependencies file",
)
@click.option(
    "--git-branch",
    metavar="NAME",
    required=False,
    help=f"Branch to use for git repo model code if defined."
    f"\n[Default: {ModelUri.git_branch}]",
)
@click.option(
    "--git-credentials-secret",
    metavar="NAME",
    required=False,
    help="Predefined Qwak secret secret name, that contains access credentials to private repositories"
    + "Secrets should be of the form USERNAME:ACCESS_TOKEN. For info regarding defining Qwak Secrets using the"
    + "`qwak secret` command",
)
@click.option(
    "--cpus",
    metavar="NAME",
    required=False,
    help="Number of cpus to use on the remote build. [Default (If GPU not configured): 2] "
    "(DO NOT CONFIGURE GPU AND CPU TOGETHER)",
    type=click.FLOAT,
)
@click.option(
    "--memory",
    metavar="NAME",
    required=False,
    help="Memory to use on the remote build. [Default (If GPU not configured): 4Gi] "
    "(DO NOT CONFIGURE GPU AND CPU TOGETHER)",
)
@click.option(
    "--gpu-type",
    metavar="NAME",
    required=False,
    help=f"Type of GPU to use on the remote build ({', '.join([x for x in QwakConstants.GPU_TYPES])})."
    f"\n[Default: {RemoteBuildResources.gpu_type}]"
    "(DO NOT CONFIGURE GPU AND CPU TOGETHER)",
    type=click.STRING,
)
@click.option(
    "--gpu-amount",
    metavar="NAME",
    required=False,
    type=int,
    help=f"Amount of GPU's to use on the remote build."
    f"\n[Default: {RemoteBuildResources.gpu_amount}] "
    "(DO NOT CONFIGURE GPU AND CPU TOGETHER)",
)
@click.option(
    "--gpu-compatible",
    help=f"Whether to build an image that is compatible to be deployd on a GPU instance."
    f"\n[Default: {BuildProperties.gpu_compatible}] ",
    default=False,
    is_flag=True,
)
@click.option(
    "--iam-role-arn",
    required=False,
    type=str,
    help="Custom IAM Role ARN for AWS based builds",
)
@click.option(
    "--service-account-key-secret-name",
    type=str,
    help="Custom service account for GCP",
)
@click.option(
    "--cache/--no-cache",
    default=None,
    help="Disable docker build cache. [Default: Cache enabled]",
)
@click.option(
    "-v",
    "--verbose",
    count=True,
    default=None,
    help="Log verbosity level - v: INFO, vv: DEBUG [default: WARNING], Default ERROR",
)
@click.option(
    "--base-image",
    help="Used for customizing the docker container image built for train, build and deploy."
    "Docker images should be based on qwak images, The entrypoint or cmd of the docker "
    "image should not be changed."
    f"\n[Default: {DockerConf.base_image}]",
    required=False,
)
@click.option(
    "-f",
    "--from-file",
    help="Build by run_config file, Command arguments will overwrite any run_config.",
    required=False,
    type=click.Path(exists=True, resolve_path=True, dir_okay=False),
)
@click.option(
    "--out-conf",
    help="Extract models build conf from command arguments, the command will not run it wil only output valid yaml "
    "structure",
    default=False,
    is_flag=True,
)
@click.option(
    "--json-logs",
    help="Output logs as json for easier parsing",
    default=False,
    is_flag=True,
)
@click.option(
    "--programmatic",
    help="Run the _logic without the UI and receive the build id and any exception as return values",
    default=False,
    is_flag=True,
)
@click.option(
    "--validate-build-artifact/--no-validate-build-artifact",
    help="Skip validate build artifact step",
    default=None,
)
@click.option(
    "--tests/--no-tests",
    help="Skip tests step",
    default=None,
)
@click.option(
    "--dependency-file-path",
    help="Custom dependency file path",
    default=None,
)
@click.option(
    "--validate-build-artifact-timeout",
    help="Timeout in seconds for the validation step",
    default=120,
)
@click.option(
    "--dependency-required-folders",
    help="Folder to be copied into the build. In order to copy several folders, use this flag several times",
    default=None,
    required=False,
    multiple=True,
)
@click.option(
    "--deploy",
    help="Whether you want to deploy the build if it finishes successfully. "
    "Choosing this will follow the build process in the terminal and will trigger a deployment when the "
    "build finishes.",
    default=False,
    is_flag=True,
)
@click.option(
    "--instance",
    required=False,
    type=str,
    help="The instance size to build on - 'small', 'medium', 'large', etc...",
    default=None,
)
@click.option(
    "--deployment-instance",
    required=False,
    type=str,
    help="The instance size to deploy on - 'small', 'medium', 'large', etc...",
    default=None,
)
@click.option(
    "--purchase-option",
    required=False,
    type=str,
    help="The type of the instance to build on - 'ondemand' or 'spot'",
    default=None,
)
@click.option(
    "--id-only",
    help="Receiving only the build id and any exception as return values (Depends on "
    "--programmatic in order to avoid UI output too)",
    default=False,
    is_flag=True,
)
@click.option(
    "--sync",
    help="Waits until the build is finished (successfully or not) and return the build status",
    default=False,
    is_flag=True,
)
@click.option(
    "--git-secret-ssh",
    metavar="NAME",
    required=False,
    help="[REMOTE BUILD] Predefined Qwak ssh secret name, that contains access credentials to private repositories"
    + "secret ssh key should contain the private ssh key."
    + "`qwak secret` command",
)
@click.option(
    "--push/--no-push",
    help="Whether to push the build image to the registry (default is True)",
    default=True,
    is_flag=True,
)
@click.option(
    "--provision-instance-timeout",
    help="Timeout in minutes for the provision instance step",
    default=120,
)
@click.option(
    "-N",
    "--name",
    "build_name",
    required=False,
    help="The build's name",
)
@click.argument("uri", required=False)
def models_build(**kwargs):
    return build(**kwargs)


def build(
    from_file: str,
    out_conf: bool,
    json_logs: bool,
    programmatic: bool,
    **kwargs,
):
    # If QWAK_DEBUG=true is set then the artifacts will not be deleted, all intermediate files located in ~/.qwak/builds
    # Including all intermediate images
    config: BuildConfigV1 = config_handler(
        config=BuildConfigV1,
        from_file=from_file,
        out_conf=out_conf,
        **kwargs,
    )
    if out_conf:
        return
    else:
        id_only = kwargs.get("id_only")
        is_sync = kwargs.get("sync")
        pipeline, success_msg = create_pipeline(config)
        with get_build_logger(config=config, json_logs=json_logs) as (
            logger,
            log_path,
        ):
            if programmatic:
                build_runner = ProgrammaticPhaseRunHandler(
                    logger, config.verbose, json_logs
                )
            else:
                build_runner = CLIPhaseRunHandler(
                    logger, log_path, config.verbose, json_logs
                )

            execute_build_pipeline(
                pipeline,
                build_runner,
            )

            if is_sync:
                wait_until_finished(pipeline.context.build_id, logger)
                if not is_final_status_successful(pipeline.context.build_id):
                    click.echo(f"Build {pipeline.context.build_id} failed")
                    exit(1)

            if id_only:
                print(pipeline.context.build_id)
            else:
                print(
                    success_msg.format(
                        base_url=pipeline.context.platform_url,
                        build_id=pipeline.context.build_id,
                        model_id=pipeline.context.model_id,
                        project_uuid=pipeline.context.project_uuid,
                    )
                )
            zip_logs(log_path=log_path, build_id=pipeline.context.build_id)

            return pipeline.context.build_id
