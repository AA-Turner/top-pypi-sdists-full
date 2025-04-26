from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from .._jsii import *

from .. import (
    Component as _Component_2b0ad27f,
    GroupRunnerOptions as _GroupRunnerOptions_148c59c1,
    Project as _Project_57d89203,
    Task as _Task_9fa875b6,
)
from ..github import GitIdentity as _GitIdentity_6effc3de
from ..github.workflows import (
    ContainerOptions as _ContainerOptions_f50907af,
    Job as _Job_20ffcf45,
    JobDefaults as _JobDefaults_965f0d10,
    JobPermissions as _JobPermissions_3b5b53dc,
    JobStep as _JobStep_c3287c05,
    JobStepOutput as _JobStepOutput_acebe827,
    JobStrategy as _JobStrategy_15089712,
    Tools as _Tools_75b93a2a,
    Triggers as _Triggers_e9ae7617,
)


@jsii.data_type(
    jsii_type="projen.build.AddPostBuildJobCommandsOptions",
    jsii_struct_bases=[],
    name_mapping={
        "checkout_repo": "checkoutRepo",
        "install_deps": "installDeps",
        "runs_on": "runsOn",
        "runs_on_group": "runsOnGroup",
        "tools": "tools",
    },
)
class AddPostBuildJobCommandsOptions:
    def __init__(
        self,
        *,
        checkout_repo: typing.Optional[builtins.bool] = None,
        install_deps: typing.Optional[builtins.bool] = None,
        runs_on: typing.Optional[typing.Sequence[builtins.str]] = None,
        runs_on_group: typing.Optional[typing.Union[_GroupRunnerOptions_148c59c1, typing.Dict[builtins.str, typing.Any]]] = None,
        tools: typing.Optional[typing.Union[_Tools_75b93a2a, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Options for ``BuildWorkflow.addPostBuildJobCommands``.

        :param checkout_repo: (experimental) Check out the repository at the pull request branch before commands are run. Default: false
        :param install_deps: (experimental) Install project dependencies before running commands. ``checkoutRepo`` must also be set to true. Currently only supported for ``NodeProject``. Default: false
        :param runs_on: (experimental) Github Runner selection labels. Default: ["ubuntu-latest"]
        :param runs_on_group: (experimental) Github Runner Group selection options.
        :param tools: (experimental) Tools that should be installed before the commands are run.

        :stability: experimental
        '''
        if isinstance(runs_on_group, dict):
            runs_on_group = _GroupRunnerOptions_148c59c1(**runs_on_group)
        if isinstance(tools, dict):
            tools = _Tools_75b93a2a(**tools)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bdd180796a6f791c19f1e1e0a010ee04dc75776d1793b433579cae27121efdc)
            check_type(argname="argument checkout_repo", value=checkout_repo, expected_type=type_hints["checkout_repo"])
            check_type(argname="argument install_deps", value=install_deps, expected_type=type_hints["install_deps"])
            check_type(argname="argument runs_on", value=runs_on, expected_type=type_hints["runs_on"])
            check_type(argname="argument runs_on_group", value=runs_on_group, expected_type=type_hints["runs_on_group"])
            check_type(argname="argument tools", value=tools, expected_type=type_hints["tools"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if checkout_repo is not None:
            self._values["checkout_repo"] = checkout_repo
        if install_deps is not None:
            self._values["install_deps"] = install_deps
        if runs_on is not None:
            self._values["runs_on"] = runs_on
        if runs_on_group is not None:
            self._values["runs_on_group"] = runs_on_group
        if tools is not None:
            self._values["tools"] = tools

    @builtins.property
    def checkout_repo(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Check out the repository at the pull request branch before commands are run.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("checkout_repo")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def install_deps(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Install project dependencies before running commands. ``checkoutRepo`` must also be set to true.

        Currently only supported for ``NodeProject``.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("install_deps")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def runs_on(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Github Runner selection labels.

        :default: ["ubuntu-latest"]

        :stability: experimental
        :description: Defines a target Runner by labels
        :throws: {Error} if both ``runsOn`` and ``runsOnGroup`` are specified
        '''
        result = self._values.get("runs_on")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def runs_on_group(self) -> typing.Optional[_GroupRunnerOptions_148c59c1]:
        '''(experimental) Github Runner Group selection options.

        :stability: experimental
        :description: Defines a target Runner Group by name and/or labels
        :throws: {Error} if both ``runsOn`` and ``runsOnGroup`` are specified
        '''
        result = self._values.get("runs_on_group")
        return typing.cast(typing.Optional[_GroupRunnerOptions_148c59c1], result)

    @builtins.property
    def tools(self) -> typing.Optional[_Tools_75b93a2a]:
        '''(experimental) Tools that should be installed before the commands are run.

        :stability: experimental
        '''
        result = self._values.get("tools")
        return typing.cast(typing.Optional[_Tools_75b93a2a], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddPostBuildJobCommandsOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.build.AddPostBuildJobTaskOptions",
    jsii_struct_bases=[],
    name_mapping={
        "runs_on": "runsOn",
        "runs_on_group": "runsOnGroup",
        "tools": "tools",
    },
)
class AddPostBuildJobTaskOptions:
    def __init__(
        self,
        *,
        runs_on: typing.Optional[typing.Sequence[builtins.str]] = None,
        runs_on_group: typing.Optional[typing.Union[_GroupRunnerOptions_148c59c1, typing.Dict[builtins.str, typing.Any]]] = None,
        tools: typing.Optional[typing.Union[_Tools_75b93a2a, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Options for ``BuildWorkflow.addPostBuildJobTask``.

        :param runs_on: (experimental) Github Runner selection labels. Default: ["ubuntu-latest"]
        :param runs_on_group: (experimental) Github Runner Group selection options.
        :param tools: (experimental) Tools that should be installed before the task is run.

        :stability: experimental
        '''
        if isinstance(runs_on_group, dict):
            runs_on_group = _GroupRunnerOptions_148c59c1(**runs_on_group)
        if isinstance(tools, dict):
            tools = _Tools_75b93a2a(**tools)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8875bca09077fb03ccffe7b968539b2dfce687a745e71024f884a06b58076947)
            check_type(argname="argument runs_on", value=runs_on, expected_type=type_hints["runs_on"])
            check_type(argname="argument runs_on_group", value=runs_on_group, expected_type=type_hints["runs_on_group"])
            check_type(argname="argument tools", value=tools, expected_type=type_hints["tools"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if runs_on is not None:
            self._values["runs_on"] = runs_on
        if runs_on_group is not None:
            self._values["runs_on_group"] = runs_on_group
        if tools is not None:
            self._values["tools"] = tools

    @builtins.property
    def runs_on(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Github Runner selection labels.

        :default: ["ubuntu-latest"]

        :stability: experimental
        :description: Defines a target Runner by labels
        :throws: {Error} if both ``runsOn`` and ``runsOnGroup`` are specified
        '''
        result = self._values.get("runs_on")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def runs_on_group(self) -> typing.Optional[_GroupRunnerOptions_148c59c1]:
        '''(experimental) Github Runner Group selection options.

        :stability: experimental
        :description: Defines a target Runner Group by name and/or labels
        :throws: {Error} if both ``runsOn`` and ``runsOnGroup`` are specified
        '''
        result = self._values.get("runs_on_group")
        return typing.cast(typing.Optional[_GroupRunnerOptions_148c59c1], result)

    @builtins.property
    def tools(self) -> typing.Optional[_Tools_75b93a2a]:
        '''(experimental) Tools that should be installed before the task is run.

        :stability: experimental
        '''
        result = self._values.get("tools")
        return typing.cast(typing.Optional[_Tools_75b93a2a], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddPostBuildJobTaskOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BuildWorkflow(
    _Component_2b0ad27f,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.build.BuildWorkflow",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        project: _Project_57d89203,
        *,
        build_task: _Task_9fa875b6,
        artifacts_directory: typing.Optional[builtins.str] = None,
        container_image: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        git_identity: typing.Optional[typing.Union[_GitIdentity_6effc3de, typing.Dict[builtins.str, typing.Any]]] = None,
        mutable_build: typing.Optional[builtins.bool] = None,
        post_build_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        runs_on: typing.Optional[typing.Sequence[builtins.str]] = None,
        runs_on_group: typing.Optional[typing.Union[_GroupRunnerOptions_148c59c1, typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        permissions: typing.Optional[typing.Union[_JobPermissions_3b5b53dc, typing.Dict[builtins.str, typing.Any]]] = None,
        pre_build_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        workflow_triggers: typing.Optional[typing.Union[_Triggers_e9ae7617, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param project: -
        :param build_task: (experimental) The task to execute in order to build the project.
        :param artifacts_directory: (experimental) A name of a directory that includes build artifacts. Default: "dist"
        :param container_image: (experimental) The container image to use for builds. Default: - the default workflow container
        :param env: (experimental) Build environment variables. Default: {}
        :param git_identity: (experimental) Git identity to use for the workflow. Default: - default identity
        :param mutable_build: (experimental) Automatically update files modified during builds to pull-request branches. This means that any files synthesized by projen or e.g. test snapshots will always be up-to-date before a PR is merged. Implies that PR builds do not have anti-tamper checks. This is enabled by default only if ``githubTokenSecret`` is set. Otherwise it is disabled, which implies that file changes that happen during build will not be pushed back to the branch. Default: true
        :param post_build_steps: (experimental) Steps to execute after build. Default: []
        :param runs_on: (experimental) Github Runner selection labels. Default: ["ubuntu-latest"]
        :param runs_on_group: (experimental) Github Runner Group selection options.
        :param name: (experimental) Name of the buildfile (e.g. "build" becomes "build.yml"). Default: "build"
        :param permissions: (experimental) Permissions granted to the build job To limit job permissions for ``contents``, the desired permissions have to be explicitly set, e.g.: ``{ contents: JobPermission.NONE }``. Default: ``{ contents: JobPermission.WRITE }``
        :param pre_build_steps: (experimental) Steps to execute before the build. Default: []
        :param workflow_triggers: (experimental) Build workflow triggers. Default: "{ pullRequest: {}, workflowDispatch: {} }"

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4d192684ec38f19e56855947a401da7aa8d483beaeef832704f28ff43d5ffe5)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        options = BuildWorkflowOptions(
            build_task=build_task,
            artifacts_directory=artifacts_directory,
            container_image=container_image,
            env=env,
            git_identity=git_identity,
            mutable_build=mutable_build,
            post_build_steps=post_build_steps,
            runs_on=runs_on,
            runs_on_group=runs_on_group,
            name=name,
            permissions=permissions,
            pre_build_steps=pre_build_steps,
            workflow_triggers=workflow_triggers,
        )

        jsii.create(self.__class__, self, [project, options])

    @jsii.member(jsii_name="addPostBuildJob")
    def add_post_build_job(
        self,
        id: builtins.str,
        *,
        steps: typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]],
        container: typing.Optional[typing.Union[_ContainerOptions_f50907af, typing.Dict[builtins.str, typing.Any]]] = None,
        continue_on_error: typing.Optional[builtins.bool] = None,
        defaults: typing.Optional[typing.Union[_JobDefaults_965f0d10, typing.Dict[builtins.str, typing.Any]]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        environment: typing.Any = None,
        outputs: typing.Optional[typing.Mapping[builtins.str, typing.Union[_JobStepOutput_acebe827, typing.Dict[builtins.str, typing.Any]]]] = None,
        runs_on: typing.Optional[typing.Sequence[builtins.str]] = None,
        runs_on_group: typing.Optional[typing.Union[_GroupRunnerOptions_148c59c1, typing.Dict[builtins.str, typing.Any]]] = None,
        services: typing.Optional[typing.Mapping[builtins.str, typing.Union[_ContainerOptions_f50907af, typing.Dict[builtins.str, typing.Any]]]] = None,
        timeout_minutes: typing.Optional[jsii.Number] = None,
        tools: typing.Optional[typing.Union[_Tools_75b93a2a, typing.Dict[builtins.str, typing.Any]]] = None,
        permissions: typing.Union[_JobPermissions_3b5b53dc, typing.Dict[builtins.str, typing.Any]],
        concurrency: typing.Any = None,
        if_: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        needs: typing.Optional[typing.Sequence[builtins.str]] = None,
        strategy: typing.Optional[typing.Union[_JobStrategy_15089712, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Adds another job to the build workflow which is executed after the build job succeeded.

        Jobs are executed *only* if the build did NOT self mutate. If the build
        self-mutate, the branch will either be updated or the build will fail (in
        forks), so there is no point in executing the post-build job.

        :param id: The id of the new job.
        :param steps: (experimental) A job contains a sequence of tasks called steps. Steps can run commands, run setup tasks, or run an action in your repository, a public repository, or an action published in a Docker registry. Not all steps run actions, but all actions run as a step. Each step runs in its own process in the runner environment and has access to the workspace and filesystem. Because steps run in their own process, changes to environment variables are not preserved between steps. GitHub provides built-in steps to set up and complete a job.
        :param container: (experimental) A container to run any steps in a job that don't already specify a container. If you have steps that use both script and container actions, the container actions will run as sibling containers on the same network with the same volume mounts.
        :param continue_on_error: (experimental) Prevents a workflow run from failing when a job fails. Set to true to allow a workflow run to pass when this job fails.
        :param defaults: (experimental) A map of default settings that will apply to all steps in the job. You can also set default settings for the entire workflow.
        :param env: (experimental) A map of environment variables that are available to all steps in the job. You can also set environment variables for the entire workflow or an individual step.
        :param environment: (experimental) The environment that the job references. All environment protection rules must pass before a job referencing the environment is sent to a runner.
        :param outputs: (experimental) A map of outputs for a job. Job outputs are available to all downstream jobs that depend on this job.
        :param runs_on: (experimental) The type of machine to run the job on. The machine can be either a GitHub-hosted runner or a self-hosted runner.
        :param runs_on_group: (experimental) Github Runner Group selection options.
        :param services: (experimental) Used to host service containers for a job in a workflow. Service containers are useful for creating databases or cache services like Redis. The runner automatically creates a Docker network and manages the life cycle of the service containers.
        :param timeout_minutes: (experimental) The maximum number of minutes to let a job run before GitHub automatically cancels it. Default: 360
        :param tools: (experimental) Tools required for this job. Translates into ``actions/setup-xxx`` steps at the beginning of the job.
        :param permissions: (experimental) You can modify the default permissions granted to the GITHUB_TOKEN, adding or removing access as required, so that you only allow the minimum required access. Use ``{ contents: READ }`` if your job only needs to clone code. This is intentionally a required field since it is required in order to allow workflows to run in GitHub repositories with restricted default access.
        :param concurrency: (experimental) Concurrency ensures that only a single job or workflow using the same concurrency group will run at a time. A concurrency group can be any string or expression. The expression can use any context except for the secrets context.
        :param if_: (experimental) You can use the if conditional to prevent a job from running unless a condition is met. You can use any supported context and expression to create a conditional.
        :param name: (experimental) The name of the job displayed on GitHub.
        :param needs: (experimental) Identifies any jobs that must complete successfully before this job will run. It can be a string or array of strings. If a job fails, all jobs that need it are skipped unless the jobs use a conditional expression that causes the job to continue.
        :param strategy: (experimental) A strategy creates a build matrix for your jobs. You can define different variations to run each job in.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__888ab8af7c03eeaa07ed3e67ba74b689b9baf8622baa2d4e0a2e3b138007c4ec)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        job = _Job_20ffcf45(
            steps=steps,
            container=container,
            continue_on_error=continue_on_error,
            defaults=defaults,
            env=env,
            environment=environment,
            outputs=outputs,
            runs_on=runs_on,
            runs_on_group=runs_on_group,
            services=services,
            timeout_minutes=timeout_minutes,
            tools=tools,
            permissions=permissions,
            concurrency=concurrency,
            if_=if_,
            name=name,
            needs=needs,
            strategy=strategy,
        )

        return typing.cast(None, jsii.invoke(self, "addPostBuildJob", [id, job]))

    @jsii.member(jsii_name="addPostBuildJobCommands")
    def add_post_build_job_commands(
        self,
        id: builtins.str,
        commands: typing.Sequence[builtins.str],
        *,
        checkout_repo: typing.Optional[builtins.bool] = None,
        install_deps: typing.Optional[builtins.bool] = None,
        runs_on: typing.Optional[typing.Sequence[builtins.str]] = None,
        runs_on_group: typing.Optional[typing.Union[_GroupRunnerOptions_148c59c1, typing.Dict[builtins.str, typing.Any]]] = None,
        tools: typing.Optional[typing.Union[_Tools_75b93a2a, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Run a sequence of commands as a job within the build workflow which is executed after the build job succeeded.

        Jobs are executed *only* if the build did NOT self mutate. If the build
        self-mutate, the branch will either be updated or the build will fail (in
        forks), so there is no point in executing the post-build job.

        :param id: -
        :param commands: -
        :param checkout_repo: (experimental) Check out the repository at the pull request branch before commands are run. Default: false
        :param install_deps: (experimental) Install project dependencies before running commands. ``checkoutRepo`` must also be set to true. Currently only supported for ``NodeProject``. Default: false
        :param runs_on: (experimental) Github Runner selection labels. Default: ["ubuntu-latest"]
        :param runs_on_group: (experimental) Github Runner Group selection options.
        :param tools: (experimental) Tools that should be installed before the commands are run.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7277bb1c03dfd43b03774fdd6ac56b0c2eaeca1eff7566e375594542fd75415b)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument commands", value=commands, expected_type=type_hints["commands"])
        options = AddPostBuildJobCommandsOptions(
            checkout_repo=checkout_repo,
            install_deps=install_deps,
            runs_on=runs_on,
            runs_on_group=runs_on_group,
            tools=tools,
        )

        return typing.cast(None, jsii.invoke(self, "addPostBuildJobCommands", [id, commands, options]))

    @jsii.member(jsii_name="addPostBuildJobTask")
    def add_post_build_job_task(
        self,
        task: _Task_9fa875b6,
        *,
        runs_on: typing.Optional[typing.Sequence[builtins.str]] = None,
        runs_on_group: typing.Optional[typing.Union[_GroupRunnerOptions_148c59c1, typing.Dict[builtins.str, typing.Any]]] = None,
        tools: typing.Optional[typing.Union[_Tools_75b93a2a, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Run a task as a job within the build workflow which is executed after the build job succeeded.

        The job will have access to build artifacts and will install project
        dependencies in order to be able to run any commands used in the tasks.

        Jobs are executed *only* if the build did NOT self mutate. If the build
        self-mutate, the branch will either be updated or the build will fail (in
        forks), so there is no point in executing the post-build job.

        :param task: -
        :param runs_on: (experimental) Github Runner selection labels. Default: ["ubuntu-latest"]
        :param runs_on_group: (experimental) Github Runner Group selection options.
        :param tools: (experimental) Tools that should be installed before the task is run.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c03f04bdb16e40ac3b3cb03035363b39ad66a2154cbc7522d85d07261602d4c8)
            check_type(argname="argument task", value=task, expected_type=type_hints["task"])
        options = AddPostBuildJobTaskOptions(
            runs_on=runs_on, runs_on_group=runs_on_group, tools=tools
        )

        return typing.cast(None, jsii.invoke(self, "addPostBuildJobTask", [task, options]))

    @jsii.member(jsii_name="addPostBuildSteps")
    def add_post_build_steps(self, *steps: _JobStep_c3287c05) -> None:
        '''(experimental) Adds steps that are executed after the build.

        :param steps: The job steps.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43bc47daca0c138fa9c8bc13154f9acea9c452e82f2dc45b3f3a655c654decc0)
            check_type(argname="argument steps", value=steps, expected_type=typing.Tuple[type_hints["steps"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addPostBuildSteps", [*steps]))

    @builtins.property
    @jsii.member(jsii_name="buildJobIds")
    def build_job_ids(self) -> typing.List[builtins.str]:
        '''(experimental) Returns a list of job IDs that are part of the build.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "buildJobIds"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) Name of generated github workflow.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))


@jsii.data_type(
    jsii_type="projen.build.BuildWorkflowCommonOptions",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "permissions": "permissions",
        "pre_build_steps": "preBuildSteps",
        "workflow_triggers": "workflowTriggers",
    },
)
class BuildWorkflowCommonOptions:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        permissions: typing.Optional[typing.Union[_JobPermissions_3b5b53dc, typing.Dict[builtins.str, typing.Any]]] = None,
        pre_build_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        workflow_triggers: typing.Optional[typing.Union[_Triggers_e9ae7617, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: (experimental) Name of the buildfile (e.g. "build" becomes "build.yml"). Default: "build"
        :param permissions: (experimental) Permissions granted to the build job To limit job permissions for ``contents``, the desired permissions have to be explicitly set, e.g.: ``{ contents: JobPermission.NONE }``. Default: ``{ contents: JobPermission.WRITE }``
        :param pre_build_steps: (experimental) Steps to execute before the build. Default: []
        :param workflow_triggers: (experimental) Build workflow triggers. Default: "{ pullRequest: {}, workflowDispatch: {} }"

        :stability: experimental
        '''
        if isinstance(permissions, dict):
            permissions = _JobPermissions_3b5b53dc(**permissions)
        if isinstance(workflow_triggers, dict):
            workflow_triggers = _Triggers_e9ae7617(**workflow_triggers)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c47ecd67d7b1fa42db0bfe937571471191786b92fd702c85fceb89eb2d1b05c5)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
            check_type(argname="argument pre_build_steps", value=pre_build_steps, expected_type=type_hints["pre_build_steps"])
            check_type(argname="argument workflow_triggers", value=workflow_triggers, expected_type=type_hints["workflow_triggers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if permissions is not None:
            self._values["permissions"] = permissions
        if pre_build_steps is not None:
            self._values["pre_build_steps"] = pre_build_steps
        if workflow_triggers is not None:
            self._values["workflow_triggers"] = workflow_triggers

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the buildfile (e.g. "build" becomes "build.yml").

        :default: "build"

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions(self) -> typing.Optional[_JobPermissions_3b5b53dc]:
        '''(experimental) Permissions granted to the build job To limit job permissions for ``contents``, the desired permissions have to be explicitly set, e.g.: ``{ contents: JobPermission.NONE }``.

        :default: ``{ contents: JobPermission.WRITE }``

        :stability: experimental
        '''
        result = self._values.get("permissions")
        return typing.cast(typing.Optional[_JobPermissions_3b5b53dc], result)

    @builtins.property
    def pre_build_steps(self) -> typing.Optional[typing.List[_JobStep_c3287c05]]:
        '''(experimental) Steps to execute before the build.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("pre_build_steps")
        return typing.cast(typing.Optional[typing.List[_JobStep_c3287c05]], result)

    @builtins.property
    def workflow_triggers(self) -> typing.Optional[_Triggers_e9ae7617]:
        '''(experimental) Build workflow triggers.

        :default: "{ pullRequest: {}, workflowDispatch: {} }"

        :stability: experimental
        '''
        result = self._values.get("workflow_triggers")
        return typing.cast(typing.Optional[_Triggers_e9ae7617], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BuildWorkflowCommonOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.build.BuildWorkflowOptions",
    jsii_struct_bases=[BuildWorkflowCommonOptions],
    name_mapping={
        "name": "name",
        "permissions": "permissions",
        "pre_build_steps": "preBuildSteps",
        "workflow_triggers": "workflowTriggers",
        "build_task": "buildTask",
        "artifacts_directory": "artifactsDirectory",
        "container_image": "containerImage",
        "env": "env",
        "git_identity": "gitIdentity",
        "mutable_build": "mutableBuild",
        "post_build_steps": "postBuildSteps",
        "runs_on": "runsOn",
        "runs_on_group": "runsOnGroup",
    },
)
class BuildWorkflowOptions(BuildWorkflowCommonOptions):
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        permissions: typing.Optional[typing.Union[_JobPermissions_3b5b53dc, typing.Dict[builtins.str, typing.Any]]] = None,
        pre_build_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        workflow_triggers: typing.Optional[typing.Union[_Triggers_e9ae7617, typing.Dict[builtins.str, typing.Any]]] = None,
        build_task: _Task_9fa875b6,
        artifacts_directory: typing.Optional[builtins.str] = None,
        container_image: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        git_identity: typing.Optional[typing.Union[_GitIdentity_6effc3de, typing.Dict[builtins.str, typing.Any]]] = None,
        mutable_build: typing.Optional[builtins.bool] = None,
        post_build_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        runs_on: typing.Optional[typing.Sequence[builtins.str]] = None,
        runs_on_group: typing.Optional[typing.Union[_GroupRunnerOptions_148c59c1, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: (experimental) Name of the buildfile (e.g. "build" becomes "build.yml"). Default: "build"
        :param permissions: (experimental) Permissions granted to the build job To limit job permissions for ``contents``, the desired permissions have to be explicitly set, e.g.: ``{ contents: JobPermission.NONE }``. Default: ``{ contents: JobPermission.WRITE }``
        :param pre_build_steps: (experimental) Steps to execute before the build. Default: []
        :param workflow_triggers: (experimental) Build workflow triggers. Default: "{ pullRequest: {}, workflowDispatch: {} }"
        :param build_task: (experimental) The task to execute in order to build the project.
        :param artifacts_directory: (experimental) A name of a directory that includes build artifacts. Default: "dist"
        :param container_image: (experimental) The container image to use for builds. Default: - the default workflow container
        :param env: (experimental) Build environment variables. Default: {}
        :param git_identity: (experimental) Git identity to use for the workflow. Default: - default identity
        :param mutable_build: (experimental) Automatically update files modified during builds to pull-request branches. This means that any files synthesized by projen or e.g. test snapshots will always be up-to-date before a PR is merged. Implies that PR builds do not have anti-tamper checks. This is enabled by default only if ``githubTokenSecret`` is set. Otherwise it is disabled, which implies that file changes that happen during build will not be pushed back to the branch. Default: true
        :param post_build_steps: (experimental) Steps to execute after build. Default: []
        :param runs_on: (experimental) Github Runner selection labels. Default: ["ubuntu-latest"]
        :param runs_on_group: (experimental) Github Runner Group selection options.

        :stability: experimental
        '''
        if isinstance(permissions, dict):
            permissions = _JobPermissions_3b5b53dc(**permissions)
        if isinstance(workflow_triggers, dict):
            workflow_triggers = _Triggers_e9ae7617(**workflow_triggers)
        if isinstance(git_identity, dict):
            git_identity = _GitIdentity_6effc3de(**git_identity)
        if isinstance(runs_on_group, dict):
            runs_on_group = _GroupRunnerOptions_148c59c1(**runs_on_group)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d08c9df51ed0147527f9d30b5f0f37c5e4482b10a1ea4f55a14885626d0721e)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
            check_type(argname="argument pre_build_steps", value=pre_build_steps, expected_type=type_hints["pre_build_steps"])
            check_type(argname="argument workflow_triggers", value=workflow_triggers, expected_type=type_hints["workflow_triggers"])
            check_type(argname="argument build_task", value=build_task, expected_type=type_hints["build_task"])
            check_type(argname="argument artifacts_directory", value=artifacts_directory, expected_type=type_hints["artifacts_directory"])
            check_type(argname="argument container_image", value=container_image, expected_type=type_hints["container_image"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument git_identity", value=git_identity, expected_type=type_hints["git_identity"])
            check_type(argname="argument mutable_build", value=mutable_build, expected_type=type_hints["mutable_build"])
            check_type(argname="argument post_build_steps", value=post_build_steps, expected_type=type_hints["post_build_steps"])
            check_type(argname="argument runs_on", value=runs_on, expected_type=type_hints["runs_on"])
            check_type(argname="argument runs_on_group", value=runs_on_group, expected_type=type_hints["runs_on_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "build_task": build_task,
        }
        if name is not None:
            self._values["name"] = name
        if permissions is not None:
            self._values["permissions"] = permissions
        if pre_build_steps is not None:
            self._values["pre_build_steps"] = pre_build_steps
        if workflow_triggers is not None:
            self._values["workflow_triggers"] = workflow_triggers
        if artifacts_directory is not None:
            self._values["artifacts_directory"] = artifacts_directory
        if container_image is not None:
            self._values["container_image"] = container_image
        if env is not None:
            self._values["env"] = env
        if git_identity is not None:
            self._values["git_identity"] = git_identity
        if mutable_build is not None:
            self._values["mutable_build"] = mutable_build
        if post_build_steps is not None:
            self._values["post_build_steps"] = post_build_steps
        if runs_on is not None:
            self._values["runs_on"] = runs_on
        if runs_on_group is not None:
            self._values["runs_on_group"] = runs_on_group

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the buildfile (e.g. "build" becomes "build.yml").

        :default: "build"

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions(self) -> typing.Optional[_JobPermissions_3b5b53dc]:
        '''(experimental) Permissions granted to the build job To limit job permissions for ``contents``, the desired permissions have to be explicitly set, e.g.: ``{ contents: JobPermission.NONE }``.

        :default: ``{ contents: JobPermission.WRITE }``

        :stability: experimental
        '''
        result = self._values.get("permissions")
        return typing.cast(typing.Optional[_JobPermissions_3b5b53dc], result)

    @builtins.property
    def pre_build_steps(self) -> typing.Optional[typing.List[_JobStep_c3287c05]]:
        '''(experimental) Steps to execute before the build.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("pre_build_steps")
        return typing.cast(typing.Optional[typing.List[_JobStep_c3287c05]], result)

    @builtins.property
    def workflow_triggers(self) -> typing.Optional[_Triggers_e9ae7617]:
        '''(experimental) Build workflow triggers.

        :default: "{ pullRequest: {}, workflowDispatch: {} }"

        :stability: experimental
        '''
        result = self._values.get("workflow_triggers")
        return typing.cast(typing.Optional[_Triggers_e9ae7617], result)

    @builtins.property
    def build_task(self) -> _Task_9fa875b6:
        '''(experimental) The task to execute in order to build the project.

        :stability: experimental
        '''
        result = self._values.get("build_task")
        assert result is not None, "Required property 'build_task' is missing"
        return typing.cast(_Task_9fa875b6, result)

    @builtins.property
    def artifacts_directory(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name of a directory that includes build artifacts.

        :default: "dist"

        :stability: experimental
        '''
        result = self._values.get("artifacts_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def container_image(self) -> typing.Optional[builtins.str]:
        '''(experimental) The container image to use for builds.

        :default: - the default workflow container

        :stability: experimental
        '''
        result = self._values.get("container_image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Build environment variables.

        :default: {}

        :stability: experimental
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def git_identity(self) -> typing.Optional[_GitIdentity_6effc3de]:
        '''(experimental) Git identity to use for the workflow.

        :default: - default identity

        :stability: experimental
        '''
        result = self._values.get("git_identity")
        return typing.cast(typing.Optional[_GitIdentity_6effc3de], result)

    @builtins.property
    def mutable_build(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically update files modified during builds to pull-request branches.

        This means that any files synthesized by projen or e.g. test snapshots will
        always be up-to-date before a PR is merged.

        Implies that PR builds do not have anti-tamper checks.

        This is enabled by default only if ``githubTokenSecret`` is set. Otherwise it
        is disabled, which implies that file changes that happen during build will
        not be pushed back to the branch.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("mutable_build")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def post_build_steps(self) -> typing.Optional[typing.List[_JobStep_c3287c05]]:
        '''(experimental) Steps to execute after build.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("post_build_steps")
        return typing.cast(typing.Optional[typing.List[_JobStep_c3287c05]], result)

    @builtins.property
    def runs_on(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Github Runner selection labels.

        :default: ["ubuntu-latest"]

        :stability: experimental
        :description: Defines a target Runner by labels
        :throws: {Error} if both ``runsOn`` and ``runsOnGroup`` are specified
        '''
        result = self._values.get("runs_on")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def runs_on_group(self) -> typing.Optional[_GroupRunnerOptions_148c59c1]:
        '''(experimental) Github Runner Group selection options.

        :stability: experimental
        :description: Defines a target Runner Group by name and/or labels
        :throws: {Error} if both ``runsOn`` and ``runsOnGroup`` are specified
        '''
        result = self._values.get("runs_on_group")
        return typing.cast(typing.Optional[_GroupRunnerOptions_148c59c1], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BuildWorkflowOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AddPostBuildJobCommandsOptions",
    "AddPostBuildJobTaskOptions",
    "BuildWorkflow",
    "BuildWorkflowCommonOptions",
    "BuildWorkflowOptions",
]

publication.publish()

def _typecheckingstub__7bdd180796a6f791c19f1e1e0a010ee04dc75776d1793b433579cae27121efdc(
    *,
    checkout_repo: typing.Optional[builtins.bool] = None,
    install_deps: typing.Optional[builtins.bool] = None,
    runs_on: typing.Optional[typing.Sequence[builtins.str]] = None,
    runs_on_group: typing.Optional[typing.Union[_GroupRunnerOptions_148c59c1, typing.Dict[builtins.str, typing.Any]]] = None,
    tools: typing.Optional[typing.Union[_Tools_75b93a2a, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8875bca09077fb03ccffe7b968539b2dfce687a745e71024f884a06b58076947(
    *,
    runs_on: typing.Optional[typing.Sequence[builtins.str]] = None,
    runs_on_group: typing.Optional[typing.Union[_GroupRunnerOptions_148c59c1, typing.Dict[builtins.str, typing.Any]]] = None,
    tools: typing.Optional[typing.Union[_Tools_75b93a2a, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4d192684ec38f19e56855947a401da7aa8d483beaeef832704f28ff43d5ffe5(
    project: _Project_57d89203,
    *,
    build_task: _Task_9fa875b6,
    artifacts_directory: typing.Optional[builtins.str] = None,
    container_image: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    git_identity: typing.Optional[typing.Union[_GitIdentity_6effc3de, typing.Dict[builtins.str, typing.Any]]] = None,
    mutable_build: typing.Optional[builtins.bool] = None,
    post_build_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
    runs_on: typing.Optional[typing.Sequence[builtins.str]] = None,
    runs_on_group: typing.Optional[typing.Union[_GroupRunnerOptions_148c59c1, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    permissions: typing.Optional[typing.Union[_JobPermissions_3b5b53dc, typing.Dict[builtins.str, typing.Any]]] = None,
    pre_build_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
    workflow_triggers: typing.Optional[typing.Union[_Triggers_e9ae7617, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__888ab8af7c03eeaa07ed3e67ba74b689b9baf8622baa2d4e0a2e3b138007c4ec(
    id: builtins.str,
    *,
    steps: typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]],
    container: typing.Optional[typing.Union[_ContainerOptions_f50907af, typing.Dict[builtins.str, typing.Any]]] = None,
    continue_on_error: typing.Optional[builtins.bool] = None,
    defaults: typing.Optional[typing.Union[_JobDefaults_965f0d10, typing.Dict[builtins.str, typing.Any]]] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    environment: typing.Any = None,
    outputs: typing.Optional[typing.Mapping[builtins.str, typing.Union[_JobStepOutput_acebe827, typing.Dict[builtins.str, typing.Any]]]] = None,
    runs_on: typing.Optional[typing.Sequence[builtins.str]] = None,
    runs_on_group: typing.Optional[typing.Union[_GroupRunnerOptions_148c59c1, typing.Dict[builtins.str, typing.Any]]] = None,
    services: typing.Optional[typing.Mapping[builtins.str, typing.Union[_ContainerOptions_f50907af, typing.Dict[builtins.str, typing.Any]]]] = None,
    timeout_minutes: typing.Optional[jsii.Number] = None,
    tools: typing.Optional[typing.Union[_Tools_75b93a2a, typing.Dict[builtins.str, typing.Any]]] = None,
    permissions: typing.Union[_JobPermissions_3b5b53dc, typing.Dict[builtins.str, typing.Any]],
    concurrency: typing.Any = None,
    if_: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    needs: typing.Optional[typing.Sequence[builtins.str]] = None,
    strategy: typing.Optional[typing.Union[_JobStrategy_15089712, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7277bb1c03dfd43b03774fdd6ac56b0c2eaeca1eff7566e375594542fd75415b(
    id: builtins.str,
    commands: typing.Sequence[builtins.str],
    *,
    checkout_repo: typing.Optional[builtins.bool] = None,
    install_deps: typing.Optional[builtins.bool] = None,
    runs_on: typing.Optional[typing.Sequence[builtins.str]] = None,
    runs_on_group: typing.Optional[typing.Union[_GroupRunnerOptions_148c59c1, typing.Dict[builtins.str, typing.Any]]] = None,
    tools: typing.Optional[typing.Union[_Tools_75b93a2a, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c03f04bdb16e40ac3b3cb03035363b39ad66a2154cbc7522d85d07261602d4c8(
    task: _Task_9fa875b6,
    *,
    runs_on: typing.Optional[typing.Sequence[builtins.str]] = None,
    runs_on_group: typing.Optional[typing.Union[_GroupRunnerOptions_148c59c1, typing.Dict[builtins.str, typing.Any]]] = None,
    tools: typing.Optional[typing.Union[_Tools_75b93a2a, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43bc47daca0c138fa9c8bc13154f9acea9c452e82f2dc45b3f3a655c654decc0(
    *steps: _JobStep_c3287c05,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c47ecd67d7b1fa42db0bfe937571471191786b92fd702c85fceb89eb2d1b05c5(
    *,
    name: typing.Optional[builtins.str] = None,
    permissions: typing.Optional[typing.Union[_JobPermissions_3b5b53dc, typing.Dict[builtins.str, typing.Any]]] = None,
    pre_build_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
    workflow_triggers: typing.Optional[typing.Union[_Triggers_e9ae7617, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d08c9df51ed0147527f9d30b5f0f37c5e4482b10a1ea4f55a14885626d0721e(
    *,
    name: typing.Optional[builtins.str] = None,
    permissions: typing.Optional[typing.Union[_JobPermissions_3b5b53dc, typing.Dict[builtins.str, typing.Any]]] = None,
    pre_build_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
    workflow_triggers: typing.Optional[typing.Union[_Triggers_e9ae7617, typing.Dict[builtins.str, typing.Any]]] = None,
    build_task: _Task_9fa875b6,
    artifacts_directory: typing.Optional[builtins.str] = None,
    container_image: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    git_identity: typing.Optional[typing.Union[_GitIdentity_6effc3de, typing.Dict[builtins.str, typing.Any]]] = None,
    mutable_build: typing.Optional[builtins.bool] = None,
    post_build_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
    runs_on: typing.Optional[typing.Sequence[builtins.str]] = None,
    runs_on_group: typing.Optional[typing.Union[_GroupRunnerOptions_148c59c1, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass
