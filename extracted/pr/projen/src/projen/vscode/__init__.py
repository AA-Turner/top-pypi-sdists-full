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
    DevEnvironmentDockerImage as _DevEnvironmentDockerImage_4a8d8ffd,
    DevEnvironmentOptions as _DevEnvironmentOptions_b10d89d1,
    IDevEnvironment as _IDevEnvironment_9a084622,
    JsonFile as _JsonFile_fa8164db,
    Project as _Project_57d89203,
    Task as _Task_9fa875b6,
)


@jsii.enum(jsii_type="projen.vscode.Console")
class Console(enum.Enum):
    '''(experimental) Controls where to launch the debug target Source: https://code.visualstudio.com/docs/editor/debugging#_launchjson-attributes.

    :stability: experimental
    '''

    INTERNAL_CONSOLE = "INTERNAL_CONSOLE"
    '''
    :stability: experimental
    '''
    INTEGRATED_TERMINAL = "INTEGRATED_TERMINAL"
    '''
    :stability: experimental
    '''
    EXTERNAL_TERMINAL = "EXTERNAL_TERMINAL"
    '''
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.vscode.DevContainerFeature",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "version": "version"},
)
class DevContainerFeature:
    def __init__(
        self,
        *,
        name: builtins.str,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) devcontainer features options.

        :param name: (experimental) feature name.
        :param version: (experimental) feature version. Default: latest

        :see: https://containers.dev/implementors/features/#devcontainer-json-properties
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a7f73b2b024ecc62d8491484836d55c16fc65fe902d48c89e27920fb1de29e7)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) feature name.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''(experimental) feature version.

        :default: latest

        :stability: experimental
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DevContainerFeature(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.vscode.DevContainerOptions",
    jsii_struct_bases=[_DevEnvironmentOptions_b10d89d1],
    name_mapping={
        "docker_image": "dockerImage",
        "ports": "ports",
        "tasks": "tasks",
        "vscode_extensions": "vscodeExtensions",
        "features": "features",
    },
)
class DevContainerOptions(_DevEnvironmentOptions_b10d89d1):
    def __init__(
        self,
        *,
        docker_image: typing.Optional[_DevEnvironmentDockerImage_4a8d8ffd] = None,
        ports: typing.Optional[typing.Sequence[builtins.str]] = None,
        tasks: typing.Optional[typing.Sequence[_Task_9fa875b6]] = None,
        vscode_extensions: typing.Optional[typing.Sequence[builtins.str]] = None,
        features: typing.Optional[typing.Sequence[typing.Union[DevContainerFeature, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Constructor options for the DevContainer component.

        The default docker image used for GitHub Codespaces is defined here:

        :param docker_image: (experimental) A Docker image or Dockerfile for the container.
        :param ports: (experimental) An array of ports that should be exposed from the container.
        :param tasks: (experimental) An array of tasks that should be run when the container starts.
        :param vscode_extensions: (experimental) An array of extension IDs that specify the extensions that should be installed inside the container when it is created.
        :param features: (experimental) An array of VSCode features that specify the features that should be installed inside the container when it is created.

        :see: https://github.com/microsoft/vscode-dev-containers/tree/master/containers/codespaces-linux
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b22d9ca6de29afcacfab2404c9835e6e3021ec640c49dfdad9bfb651e564c725)
            check_type(argname="argument docker_image", value=docker_image, expected_type=type_hints["docker_image"])
            check_type(argname="argument ports", value=ports, expected_type=type_hints["ports"])
            check_type(argname="argument tasks", value=tasks, expected_type=type_hints["tasks"])
            check_type(argname="argument vscode_extensions", value=vscode_extensions, expected_type=type_hints["vscode_extensions"])
            check_type(argname="argument features", value=features, expected_type=type_hints["features"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if docker_image is not None:
            self._values["docker_image"] = docker_image
        if ports is not None:
            self._values["ports"] = ports
        if tasks is not None:
            self._values["tasks"] = tasks
        if vscode_extensions is not None:
            self._values["vscode_extensions"] = vscode_extensions
        if features is not None:
            self._values["features"] = features

    @builtins.property
    def docker_image(self) -> typing.Optional[_DevEnvironmentDockerImage_4a8d8ffd]:
        '''(experimental) A Docker image or Dockerfile for the container.

        :stability: experimental
        '''
        result = self._values.get("docker_image")
        return typing.cast(typing.Optional[_DevEnvironmentDockerImage_4a8d8ffd], result)

    @builtins.property
    def ports(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) An array of ports that should be exposed from the container.

        :stability: experimental
        '''
        result = self._values.get("ports")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tasks(self) -> typing.Optional[typing.List[_Task_9fa875b6]]:
        '''(experimental) An array of tasks that should be run when the container starts.

        :stability: experimental
        '''
        result = self._values.get("tasks")
        return typing.cast(typing.Optional[typing.List[_Task_9fa875b6]], result)

    @builtins.property
    def vscode_extensions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) An array of extension IDs that specify the extensions that should be installed inside the container when it is created.

        :stability: experimental
        '''
        result = self._values.get("vscode_extensions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def features(self) -> typing.Optional[typing.List[DevContainerFeature]]:
        '''(experimental) An array of VSCode features that specify the features that should be installed inside the container when it is created.

        :stability: experimental
        '''
        result = self._values.get("features")
        return typing.cast(typing.Optional[typing.List[DevContainerFeature]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DevContainerOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="projen.vscode.IDevContainerEnvironment")
class IDevContainerEnvironment(_IDevEnvironment_9a084622, typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="addFeatures")
    def add_features(self, *features: DevContainerFeature) -> None:
        '''(experimental) Adds a list of VSCode features that should be automatically installed in the container.

        :param features: featureName and version(optional default: latest).

        :stability: experimental
        '''
        ...


class _IDevContainerEnvironmentProxy(
    jsii.proxy_for(_IDevEnvironment_9a084622), # type: ignore[misc]
):
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.vscode.IDevContainerEnvironment"

    @jsii.member(jsii_name="addFeatures")
    def add_features(self, *features: DevContainerFeature) -> None:
        '''(experimental) Adds a list of VSCode features that should be automatically installed in the container.

        :param features: featureName and version(optional default: latest).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59f53078ad4f94636f7ad21968f318db42126c330e189eccadb0cb6fefb6bfd3)
            check_type(argname="argument features", value=features, expected_type=typing.Tuple[type_hints["features"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addFeatures", [*features]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDevContainerEnvironment).__jsii_proxy_class__ = lambda : _IDevContainerEnvironmentProxy


@jsii.enum(jsii_type="projen.vscode.InternalConsoleOptions")
class InternalConsoleOptions(enum.Enum):
    '''(experimental) Controls the visibility of the VSCode Debug Console panel during a debugging session Source: https://code.visualstudio.com/docs/editor/debugging#_launchjson-attributes.

    :stability: experimental
    '''

    NEVER_OPEN = "NEVER_OPEN"
    '''
    :stability: experimental
    '''
    OPEN_ON_FIRST_SESSION_START = "OPEN_ON_FIRST_SESSION_START"
    '''
    :stability: experimental
    '''
    OPEN_ON_SESSION_START = "OPEN_ON_SESSION_START"
    '''
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.vscode.Presentation",
    jsii_struct_bases=[],
    name_mapping={"group": "group", "hidden": "hidden", "order": "order"},
)
class Presentation:
    def __init__(
        self,
        *,
        group: builtins.str,
        hidden: builtins.bool,
        order: jsii.Number,
    ) -> None:
        '''(experimental) VSCode launch configuration Presentation interface "using the order, group, and hidden attributes in the presentation object you can sort, group, and hide configurations and compounds in the Debug configuration dropdown and in the Debug quick pick." Source: https://code.visualstudio.com/docs/editor/debugging#_launchjson-attributes.

        :param group: 
        :param hidden: 
        :param order: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__924d6d8e838c592ce2bb743a8e91cb4b0f379f000355379bd65232dabc6f4efe)
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
            check_type(argname="argument hidden", value=hidden, expected_type=type_hints["hidden"])
            check_type(argname="argument order", value=order, expected_type=type_hints["order"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "group": group,
            "hidden": hidden,
            "order": order,
        }

    @builtins.property
    def group(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("group")
        assert result is not None, "Required property 'group' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hidden(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        result = self._values.get("hidden")
        assert result is not None, "Required property 'hidden' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def order(self) -> jsii.Number:
        '''
        :stability: experimental
        '''
        result = self._values.get("order")
        assert result is not None, "Required property 'order' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Presentation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.vscode.ServerReadyAction",
    jsii_struct_bases=[],
    name_mapping={"action": "action", "pattern": "pattern", "uri_format": "uriFormat"},
)
class ServerReadyAction:
    def __init__(
        self,
        *,
        action: builtins.str,
        pattern: typing.Optional[builtins.str] = None,
        uri_format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) VSCode launch configuration ServerReadyAction interface "if you want to open a URL in a web browser whenever the program under debugging outputs a specific message to the debug console or integrated terminal." Source: https://code.visualstudio.com/docs/editor/debugging#_launchjson-attributes.

        :param action: 
        :param pattern: 
        :param uri_format: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66fa6feb4bea9673155e5f489baae5bbdd6d528f7ce29ff754c6915092eb7036)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
            check_type(argname="argument uri_format", value=uri_format, expected_type=type_hints["uri_format"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
        }
        if pattern is not None:
            self._values["pattern"] = pattern
        if uri_format is not None:
            self._values["uri_format"] = uri_format

    @builtins.property
    def action(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pattern(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("pattern")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def uri_format(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("uri_format")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServerReadyAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VsCode(
    _Component_2b0ad27f,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.vscode.VsCode",
):
    '''
    :stability: experimental
    '''

    def __init__(self, project: _Project_57d89203) -> None:
        '''
        :param project: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f494cab4044809f412c6dee4a08eb9aa6d128399b6c0dfdbe5d9be6e2622fed5)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        jsii.create(self.__class__, self, [project])

    @builtins.property
    @jsii.member(jsii_name="extensions")
    def extensions(self) -> "VsCodeRecommendedExtensions":
        '''
        :stability: experimental
        '''
        return typing.cast("VsCodeRecommendedExtensions", jsii.get(self, "extensions"))

    @builtins.property
    @jsii.member(jsii_name="launchConfiguration")
    def launch_configuration(self) -> "VsCodeLaunchConfig":
        '''
        :stability: experimental
        '''
        return typing.cast("VsCodeLaunchConfig", jsii.get(self, "launchConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="settings")
    def settings(self) -> "VsCodeSettings":
        '''
        :stability: experimental
        '''
        return typing.cast("VsCodeSettings", jsii.get(self, "settings"))


class VsCodeLaunchConfig(
    _Component_2b0ad27f,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.vscode.VsCodeLaunchConfig",
):
    '''(experimental) VSCode launch configuration file (launch.json), useful for enabling in-editor debugger.

    :stability: experimental
    '''

    def __init__(self, vscode: VsCode) -> None:
        '''
        :param vscode: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbb203f423ffcc3e6227caf2f8624610dfdc5c528c756efd2e3094d0db32f059)
            check_type(argname="argument vscode", value=vscode, expected_type=type_hints["vscode"])
        jsii.create(self.__class__, self, [vscode])

    @jsii.member(jsii_name="addCommandInput")
    def add_command_input(
        self,
        *,
        command: builtins.str,
        args: typing.Any = None,
        id: builtins.str,
    ) -> None:
        '''(experimental) Adds an input variable with type ``command`` to ``.vscode/launch.json``.

        See https://code.visualstudio.com/docs/editor/variables-reference#_input-variables for details.

        :param command: 
        :param args: 
        :param id: 

        :stability: experimental
        '''
        cfg = VsCodeLaunchCommandInputEntry(command=command, args=args, id=id)

        return typing.cast(None, jsii.invoke(self, "addCommandInput", [cfg]))

    @jsii.member(jsii_name="addConfiguration")
    def add_configuration(
        self,
        *,
        name: builtins.str,
        request: builtins.str,
        type: builtins.str,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        console: typing.Optional[Console] = None,
        cwd: typing.Optional[builtins.str] = None,
        debug_server: typing.Optional[jsii.Number] = None,
        disable_optimistic_b_ps: typing.Optional[builtins.bool] = None,
        env: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, builtins.bool]]] = None,
        env_file: typing.Optional[builtins.str] = None,
        internal_console_options: typing.Optional[InternalConsoleOptions] = None,
        out_files: typing.Optional[typing.Sequence[builtins.str]] = None,
        port: typing.Optional[jsii.Number] = None,
        post_debug_task: typing.Optional[builtins.str] = None,
        pre_launch_task: typing.Optional[builtins.str] = None,
        presentation: typing.Optional[typing.Union[Presentation, typing.Dict[builtins.str, typing.Any]]] = None,
        program: typing.Optional[builtins.str] = None,
        runtime_args: typing.Optional[typing.Sequence[builtins.str]] = None,
        server_ready_action: typing.Optional[typing.Union[ServerReadyAction, typing.Dict[builtins.str, typing.Any]]] = None,
        skip_files: typing.Optional[typing.Sequence[builtins.str]] = None,
        stop_on_entry: typing.Optional[builtins.bool] = None,
        url: typing.Optional[builtins.str] = None,
        web_root: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Adds a VsCodeLaunchConfigurationEntry (e.g. a node.js debugger) to `.vscode/launch.json. Each configuration entry has following mandatory fields: type, request and name. See https://code.visualstudio.com/docs/editor/debugging#_launchjson-attributes for details.

        :param name: 
        :param request: 
        :param type: 
        :param args: 
        :param console: 
        :param cwd: 
        :param debug_server: 
        :param disable_optimistic_b_ps: 
        :param env: (experimental) Set value to ``false`` to unset an existing environment variable.
        :param env_file: 
        :param internal_console_options: 
        :param out_files: 
        :param port: 
        :param post_debug_task: 
        :param pre_launch_task: 
        :param presentation: 
        :param program: 
        :param runtime_args: 
        :param server_ready_action: 
        :param skip_files: 
        :param stop_on_entry: 
        :param url: 
        :param web_root: 

        :stability: experimental
        '''
        cfg = VsCodeLaunchConfigurationEntry(
            name=name,
            request=request,
            type=type,
            args=args,
            console=console,
            cwd=cwd,
            debug_server=debug_server,
            disable_optimistic_b_ps=disable_optimistic_b_ps,
            env=env,
            env_file=env_file,
            internal_console_options=internal_console_options,
            out_files=out_files,
            port=port,
            post_debug_task=post_debug_task,
            pre_launch_task=pre_launch_task,
            presentation=presentation,
            program=program,
            runtime_args=runtime_args,
            server_ready_action=server_ready_action,
            skip_files=skip_files,
            stop_on_entry=stop_on_entry,
            url=url,
            web_root=web_root,
        )

        return typing.cast(None, jsii.invoke(self, "addConfiguration", [cfg]))

    @jsii.member(jsii_name="addPickStringInput")
    def add_pick_string_input(
        self,
        *,
        description: builtins.str,
        options: typing.Sequence[builtins.str],
        default: typing.Optional[builtins.str] = None,
        id: builtins.str,
    ) -> None:
        '''(experimental) Adds an input variable with type ``pickString`` to ``.vscode/launch.json``.

        See https://code.visualstudio.com/docs/editor/variables-reference#_input-variables for details.

        :param description: 
        :param options: 
        :param default: 
        :param id: 

        :stability: experimental
        '''
        cfg = VsCodeLaunchPickStringInputEntry(
            description=description, options=options, default=default, id=id
        )

        return typing.cast(None, jsii.invoke(self, "addPickStringInput", [cfg]))

    @jsii.member(jsii_name="addPromptStringInput")
    def add_prompt_string_input(
        self,
        *,
        description: builtins.str,
        default: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.bool] = None,
        id: builtins.str,
    ) -> None:
        '''(experimental) Adds an input variable with type ``promptString`` to ``.vscode/launch.json``.

        See https://code.visualstudio.com/docs/editor/variables-reference#_input-variables for details.

        :param description: 
        :param default: 
        :param password: 
        :param id: 

        :stability: experimental
        '''
        cfg = VsCodeLaunchPromptStringInputEntry(
            description=description, default=default, password=password, id=id
        )

        return typing.cast(None, jsii.invoke(self, "addPromptStringInput", [cfg]))

    @builtins.property
    @jsii.member(jsii_name="file")
    def file(self) -> _JsonFile_fa8164db:
        '''
        :stability: experimental
        '''
        return typing.cast(_JsonFile_fa8164db, jsii.get(self, "file"))


@jsii.data_type(
    jsii_type="projen.vscode.VsCodeLaunchConfigurationEntry",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "request": "request",
        "type": "type",
        "args": "args",
        "console": "console",
        "cwd": "cwd",
        "debug_server": "debugServer",
        "disable_optimistic_b_ps": "disableOptimisticBPs",
        "env": "env",
        "env_file": "envFile",
        "internal_console_options": "internalConsoleOptions",
        "out_files": "outFiles",
        "port": "port",
        "post_debug_task": "postDebugTask",
        "pre_launch_task": "preLaunchTask",
        "presentation": "presentation",
        "program": "program",
        "runtime_args": "runtimeArgs",
        "server_ready_action": "serverReadyAction",
        "skip_files": "skipFiles",
        "stop_on_entry": "stopOnEntry",
        "url": "url",
        "web_root": "webRoot",
    },
)
class VsCodeLaunchConfigurationEntry:
    def __init__(
        self,
        *,
        name: builtins.str,
        request: builtins.str,
        type: builtins.str,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        console: typing.Optional[Console] = None,
        cwd: typing.Optional[builtins.str] = None,
        debug_server: typing.Optional[jsii.Number] = None,
        disable_optimistic_b_ps: typing.Optional[builtins.bool] = None,
        env: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, builtins.bool]]] = None,
        env_file: typing.Optional[builtins.str] = None,
        internal_console_options: typing.Optional[InternalConsoleOptions] = None,
        out_files: typing.Optional[typing.Sequence[builtins.str]] = None,
        port: typing.Optional[jsii.Number] = None,
        post_debug_task: typing.Optional[builtins.str] = None,
        pre_launch_task: typing.Optional[builtins.str] = None,
        presentation: typing.Optional[typing.Union[Presentation, typing.Dict[builtins.str, typing.Any]]] = None,
        program: typing.Optional[builtins.str] = None,
        runtime_args: typing.Optional[typing.Sequence[builtins.str]] = None,
        server_ready_action: typing.Optional[typing.Union[ServerReadyAction, typing.Dict[builtins.str, typing.Any]]] = None,
        skip_files: typing.Optional[typing.Sequence[builtins.str]] = None,
        stop_on_entry: typing.Optional[builtins.bool] = None,
        url: typing.Optional[builtins.str] = None,
        web_root: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options for a 'VsCodeLaunchConfigurationEntry' Source: https://code.visualstudio.com/docs/editor/debugging#_launchjson-attributes.

        :param name: 
        :param request: 
        :param type: 
        :param args: 
        :param console: 
        :param cwd: 
        :param debug_server: 
        :param disable_optimistic_b_ps: 
        :param env: (experimental) Set value to ``false`` to unset an existing environment variable.
        :param env_file: 
        :param internal_console_options: 
        :param out_files: 
        :param port: 
        :param post_debug_task: 
        :param pre_launch_task: 
        :param presentation: 
        :param program: 
        :param runtime_args: 
        :param server_ready_action: 
        :param skip_files: 
        :param stop_on_entry: 
        :param url: 
        :param web_root: 

        :stability: experimental
        '''
        if isinstance(presentation, dict):
            presentation = Presentation(**presentation)
        if isinstance(server_ready_action, dict):
            server_ready_action = ServerReadyAction(**server_ready_action)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76028c8d6272b5133841fb2049bcddc9a00879405477a0aa27f058f8ac6dc481)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument request", value=request, expected_type=type_hints["request"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument console", value=console, expected_type=type_hints["console"])
            check_type(argname="argument cwd", value=cwd, expected_type=type_hints["cwd"])
            check_type(argname="argument debug_server", value=debug_server, expected_type=type_hints["debug_server"])
            check_type(argname="argument disable_optimistic_b_ps", value=disable_optimistic_b_ps, expected_type=type_hints["disable_optimistic_b_ps"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument env_file", value=env_file, expected_type=type_hints["env_file"])
            check_type(argname="argument internal_console_options", value=internal_console_options, expected_type=type_hints["internal_console_options"])
            check_type(argname="argument out_files", value=out_files, expected_type=type_hints["out_files"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument post_debug_task", value=post_debug_task, expected_type=type_hints["post_debug_task"])
            check_type(argname="argument pre_launch_task", value=pre_launch_task, expected_type=type_hints["pre_launch_task"])
            check_type(argname="argument presentation", value=presentation, expected_type=type_hints["presentation"])
            check_type(argname="argument program", value=program, expected_type=type_hints["program"])
            check_type(argname="argument runtime_args", value=runtime_args, expected_type=type_hints["runtime_args"])
            check_type(argname="argument server_ready_action", value=server_ready_action, expected_type=type_hints["server_ready_action"])
            check_type(argname="argument skip_files", value=skip_files, expected_type=type_hints["skip_files"])
            check_type(argname="argument stop_on_entry", value=stop_on_entry, expected_type=type_hints["stop_on_entry"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument web_root", value=web_root, expected_type=type_hints["web_root"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "request": request,
            "type": type,
        }
        if args is not None:
            self._values["args"] = args
        if console is not None:
            self._values["console"] = console
        if cwd is not None:
            self._values["cwd"] = cwd
        if debug_server is not None:
            self._values["debug_server"] = debug_server
        if disable_optimistic_b_ps is not None:
            self._values["disable_optimistic_b_ps"] = disable_optimistic_b_ps
        if env is not None:
            self._values["env"] = env
        if env_file is not None:
            self._values["env_file"] = env_file
        if internal_console_options is not None:
            self._values["internal_console_options"] = internal_console_options
        if out_files is not None:
            self._values["out_files"] = out_files
        if port is not None:
            self._values["port"] = port
        if post_debug_task is not None:
            self._values["post_debug_task"] = post_debug_task
        if pre_launch_task is not None:
            self._values["pre_launch_task"] = pre_launch_task
        if presentation is not None:
            self._values["presentation"] = presentation
        if program is not None:
            self._values["program"] = program
        if runtime_args is not None:
            self._values["runtime_args"] = runtime_args
        if server_ready_action is not None:
            self._values["server_ready_action"] = server_ready_action
        if skip_files is not None:
            self._values["skip_files"] = skip_files
        if stop_on_entry is not None:
            self._values["stop_on_entry"] = stop_on_entry
        if url is not None:
            self._values["url"] = url
        if web_root is not None:
            self._values["web_root"] = web_root

    @builtins.property
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def request(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("request")
        assert result is not None, "Required property 'request' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def console(self) -> typing.Optional[Console]:
        '''
        :stability: experimental
        '''
        result = self._values.get("console")
        return typing.cast(typing.Optional[Console], result)

    @builtins.property
    def cwd(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("cwd")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def debug_server(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("debug_server")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def disable_optimistic_b_ps(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("disable_optimistic_b_ps")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def env(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, builtins.bool]]]:
        '''(experimental) Set value to ``false`` to unset an existing environment variable.

        :stability: experimental
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, builtins.bool]]], result)

    @builtins.property
    def env_file(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("env_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def internal_console_options(self) -> typing.Optional[InternalConsoleOptions]:
        '''
        :stability: experimental
        '''
        result = self._values.get("internal_console_options")
        return typing.cast(typing.Optional[InternalConsoleOptions], result)

    @builtins.property
    def out_files(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("out_files")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def post_debug_task(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("post_debug_task")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pre_launch_task(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("pre_launch_task")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def presentation(self) -> typing.Optional[Presentation]:
        '''
        :stability: experimental
        '''
        result = self._values.get("presentation")
        return typing.cast(typing.Optional[Presentation], result)

    @builtins.property
    def program(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("program")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime_args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("runtime_args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def server_ready_action(self) -> typing.Optional[ServerReadyAction]:
        '''
        :stability: experimental
        '''
        result = self._values.get("server_ready_action")
        return typing.cast(typing.Optional[ServerReadyAction], result)

    @builtins.property
    def skip_files(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("skip_files")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def stop_on_entry(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("stop_on_entry")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def web_root(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("web_root")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VsCodeLaunchConfigurationEntry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.vscode.VsCodeLaunchInputEntry",
    jsii_struct_bases=[],
    name_mapping={"id": "id"},
)
class VsCodeLaunchInputEntry:
    def __init__(self, *, id: builtins.str) -> None:
        '''(experimental) Base options for a 'VsCodeLaunchInputEntry' Source: https://code.visualstudio.com/docs/editor/variables-reference#_input-variables.

        :param id: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e841e7e4ef3640a56bd02bfa85775b91ed62dd7fc9a8fcd482e487b75d2d4baa)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
        }

    @builtins.property
    def id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VsCodeLaunchInputEntry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.vscode.VsCodeLaunchPickStringInputEntry",
    jsii_struct_bases=[VsCodeLaunchInputEntry],
    name_mapping={
        "id": "id",
        "description": "description",
        "options": "options",
        "default": "default",
    },
)
class VsCodeLaunchPickStringInputEntry(VsCodeLaunchInputEntry):
    def __init__(
        self,
        *,
        id: builtins.str,
        description: builtins.str,
        options: typing.Sequence[builtins.str],
        default: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options for a 'VsCodeLaunchPickStringInputEntry' Source: https://code.visualstudio.com/docs/editor/variables-reference#_input-variables.

        :param id: 
        :param description: 
        :param options: 
        :param default: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1efc4534d421a4d5a6d1ee19a7af423129f26ea3d3e365b0cbd5d316713e44b2)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
            check_type(argname="argument default", value=default, expected_type=type_hints["default"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "description": description,
            "options": options,
        }
        if default is not None:
            self._values["default"] = default

    @builtins.property
    def id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def options(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("options")
        assert result is not None, "Required property 'options' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def default(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("default")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VsCodeLaunchPickStringInputEntry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.vscode.VsCodeLaunchPromptStringInputEntry",
    jsii_struct_bases=[VsCodeLaunchInputEntry],
    name_mapping={
        "id": "id",
        "description": "description",
        "default": "default",
        "password": "password",
    },
)
class VsCodeLaunchPromptStringInputEntry(VsCodeLaunchInputEntry):
    def __init__(
        self,
        *,
        id: builtins.str,
        description: builtins.str,
        default: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options for a 'VsCodeLaunchPromptStringInputEntry' Source: https://code.visualstudio.com/docs/editor/variables-reference#_input-variables.

        :param id: 
        :param description: 
        :param default: 
        :param password: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd9f5a97332f0e03a451cdcfdd927992c1488c8dafe0f46761677f3cb7f195f7)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument default", value=default, expected_type=type_hints["default"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "description": description,
        }
        if default is not None:
            self._values["default"] = default
        if password is not None:
            self._values["password"] = password

    @builtins.property
    def id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("default")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VsCodeLaunchPromptStringInputEntry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VsCodeRecommendedExtensions(
    _Component_2b0ad27f,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.vscode.VsCodeRecommendedExtensions",
):
    '''(experimental) VS Code Workspace recommended extensions Source: https://code.visualstudio.com/docs/editor/extension-marketplace#_workspace-recommended-extensions.

    :stability: experimental
    '''

    def __init__(self, vscode: VsCode) -> None:
        '''
        :param vscode: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e672107e647965d3df7010fe525812b0c15f85ddada55b01f48ebe2c3d565725)
            check_type(argname="argument vscode", value=vscode, expected_type=type_hints["vscode"])
        jsii.create(self.__class__, self, [vscode])

    @jsii.member(jsii_name="addRecommendations")
    def add_recommendations(self, *extensions: builtins.str) -> None:
        '''(experimental) Adds a list of VS Code extensions as recommendations for this workspace.

        :param extensions: The extension IDs.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee54c74ab4b20a8248223537312409aad3f546c2c5aeca6044e4346ce5a952d8)
            check_type(argname="argument extensions", value=extensions, expected_type=typing.Tuple[type_hints["extensions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addRecommendations", [*extensions]))

    @jsii.member(jsii_name="addUnwantedRecommendations")
    def add_unwanted_recommendations(self, *extensions: builtins.str) -> None:
        '''(experimental) Marks a list of VS Code extensions as unwanted recommendations for this workspace.

        VS Code should not be recommend these extensions for users of this workspace.

        :param extensions: The extension IDs.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1a69619f76a087ea88b4c83f8cee17e5d30db36f27b14f84da086de6e449d0c)
            check_type(argname="argument extensions", value=extensions, expected_type=typing.Tuple[type_hints["extensions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addUnwantedRecommendations", [*extensions]))

    @builtins.property
    @jsii.member(jsii_name="file")
    def file(self) -> _JsonFile_fa8164db:
        '''
        :stability: experimental
        '''
        return typing.cast(_JsonFile_fa8164db, jsii.get(self, "file"))


class VsCodeSettings(
    _Component_2b0ad27f,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.vscode.VsCodeSettings",
):
    '''(experimental) VS Code Workspace settings Source: https://code.visualstudio.com/docs/getstarted/settings#_workspace-settings.

    :stability: experimental
    '''

    def __init__(self, vscode: VsCode) -> None:
        '''
        :param vscode: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__513f68cf91869cc8da990fa2a1bc57a9c643d25b8264e1c057f76e3decc6dea1)
            check_type(argname="argument vscode", value=vscode, expected_type=type_hints["vscode"])
        jsii.create(self.__class__, self, [vscode])

    @jsii.member(jsii_name="addSetting")
    def add_setting(
        self,
        setting: builtins.str,
        value: typing.Any,
        language: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Adds a workspace setting.

        :param setting: The setting ID.
        :param value: The value of the setting.
        :param language: Scope the setting to a specific language.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__369e06bc45a74498b4cfed5bf740550cd9a57917b148178ef260593cb40c2a59)
            check_type(argname="argument setting", value=setting, expected_type=type_hints["setting"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument language", value=language, expected_type=type_hints["language"])
        return typing.cast(None, jsii.invoke(self, "addSetting", [setting, value, language]))

    @jsii.member(jsii_name="addSettings")
    def add_settings(
        self,
        settings: typing.Mapping[builtins.str, typing.Any],
        languages: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
    ) -> None:
        '''(experimental) Adds a workspace setting.

        :param settings: Array structure: [setting: string, value: any, languages?: string[]].
        :param languages: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa3e27ee6b180fccd6eab5d9670c7024eb3f8067cb08859636119e69f07de239)
            check_type(argname="argument settings", value=settings, expected_type=type_hints["settings"])
            check_type(argname="argument languages", value=languages, expected_type=type_hints["languages"])
        return typing.cast(None, jsii.invoke(self, "addSettings", [settings, languages]))

    @builtins.property
    @jsii.member(jsii_name="file")
    def file(self) -> _JsonFile_fa8164db:
        '''
        :stability: experimental
        '''
        return typing.cast(_JsonFile_fa8164db, jsii.get(self, "file"))


@jsii.implements(IDevContainerEnvironment)
class DevContainer(
    _Component_2b0ad27f,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.vscode.DevContainer",
):
    '''(experimental) A development environment running VSCode in a container;

    used by GitHub
    codespaces.

    :stability: experimental
    '''

    def __init__(
        self,
        project: _Project_57d89203,
        *,
        features: typing.Optional[typing.Sequence[typing.Union[DevContainerFeature, typing.Dict[builtins.str, typing.Any]]]] = None,
        docker_image: typing.Optional[_DevEnvironmentDockerImage_4a8d8ffd] = None,
        ports: typing.Optional[typing.Sequence[builtins.str]] = None,
        tasks: typing.Optional[typing.Sequence[_Task_9fa875b6]] = None,
        vscode_extensions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param project: -
        :param features: (experimental) An array of VSCode features that specify the features that should be installed inside the container when it is created.
        :param docker_image: (experimental) A Docker image or Dockerfile for the container.
        :param ports: (experimental) An array of ports that should be exposed from the container.
        :param tasks: (experimental) An array of tasks that should be run when the container starts.
        :param vscode_extensions: (experimental) An array of extension IDs that specify the extensions that should be installed inside the container when it is created.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50747b0b39db339de569d0b44aea84c4de3c0d9d7b268479f1a3852dfb712c0b)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        options = DevContainerOptions(
            features=features,
            docker_image=docker_image,
            ports=ports,
            tasks=tasks,
            vscode_extensions=vscode_extensions,
        )

        jsii.create(self.__class__, self, [project, options])

    @jsii.member(jsii_name="addDockerImage")
    def add_docker_image(self, image: _DevEnvironmentDockerImage_4a8d8ffd) -> None:
        '''(experimental) Add a custom Docker image or Dockerfile for the container.

        :param image: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24cf7d35da522ed5017c6db46a2565a5b5a09fbffc1dafabdf917aa798fea91d)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
        return typing.cast(None, jsii.invoke(self, "addDockerImage", [image]))

    @jsii.member(jsii_name="addFeatures")
    def add_features(self, *features: DevContainerFeature) -> None:
        '''(experimental) Adds a list of VSCode features that should be automatically installed in the container.

        :param features: featureName and version(optional default: latest).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ed3f741b9b118a06d8b8f3508504c5ecb8bcbfc9c285b78e0382ac0aa4186c7)
            check_type(argname="argument features", value=features, expected_type=typing.Tuple[type_hints["features"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addFeatures", [*features]))

    @jsii.member(jsii_name="addPorts")
    def add_ports(self, *ports: builtins.str) -> None:
        '''(experimental) Adds ports that should be exposed (forwarded) from the container.

        :param ports: The new ports.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3898b547dc05a8cd9427e24743e3ec87b3108cfb90befb94e77c24e156c3559d)
            check_type(argname="argument ports", value=ports, expected_type=typing.Tuple[type_hints["ports"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addPorts", [*ports]))

    @jsii.member(jsii_name="addTasks")
    def add_tasks(self, *tasks: _Task_9fa875b6) -> None:
        '''(experimental) Adds tasks to run when the container starts.

        Tasks will be run in sequence.

        :param tasks: The new tasks.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eccb3fb9f6eca40de5ffa59e4b75a85830e1113729bd9b08dc7e4128c2bfde0)
            check_type(argname="argument tasks", value=tasks, expected_type=typing.Tuple[type_hints["tasks"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addTasks", [*tasks]))

    @jsii.member(jsii_name="addVscodeExtensions")
    def add_vscode_extensions(self, *extensions: builtins.str) -> None:
        '''(experimental) Adds a list of VSCode extensions that should be automatically installed in the container.

        :param extensions: The extension IDs.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c13b0cafe05fa1eb28182ec3465e43421a4aa7c7e44e035db34dd4cdbce24537)
            check_type(argname="argument extensions", value=extensions, expected_type=typing.Tuple[type_hints["extensions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addVscodeExtensions", [*extensions]))

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(self) -> typing.Any:
        '''(experimental) Direct access to the devcontainer configuration (escape hatch).

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.get(self, "config"))


@jsii.data_type(
    jsii_type="projen.vscode.VsCodeLaunchCommandInputEntry",
    jsii_struct_bases=[VsCodeLaunchInputEntry],
    name_mapping={"id": "id", "command": "command", "args": "args"},
)
class VsCodeLaunchCommandInputEntry(VsCodeLaunchInputEntry):
    def __init__(
        self,
        *,
        id: builtins.str,
        command: builtins.str,
        args: typing.Any = None,
    ) -> None:
        '''(experimental) Options for a 'VsCodeLaunchCommandInputEntry' Source: https://code.visualstudio.com/docs/editor/variables-reference#_input-variables.

        :param id: 
        :param command: 
        :param args: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3572ac292b4bd9b3dc808ba9caa4797adcb64703144da90f4ad010fdedc62a30)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "command": command,
        }
        if args is not None:
            self._values["args"] = args

    @builtins.property
    def id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def command(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("command")
        assert result is not None, "Required property 'command' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def args(self) -> typing.Any:
        '''
        :stability: experimental
        '''
        result = self._values.get("args")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VsCodeLaunchCommandInputEntry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Console",
    "DevContainer",
    "DevContainerFeature",
    "DevContainerOptions",
    "IDevContainerEnvironment",
    "InternalConsoleOptions",
    "Presentation",
    "ServerReadyAction",
    "VsCode",
    "VsCodeLaunchCommandInputEntry",
    "VsCodeLaunchConfig",
    "VsCodeLaunchConfigurationEntry",
    "VsCodeLaunchInputEntry",
    "VsCodeLaunchPickStringInputEntry",
    "VsCodeLaunchPromptStringInputEntry",
    "VsCodeRecommendedExtensions",
    "VsCodeSettings",
]

publication.publish()

def _typecheckingstub__5a7f73b2b024ecc62d8491484836d55c16fc65fe902d48c89e27920fb1de29e7(
    *,
    name: builtins.str,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b22d9ca6de29afcacfab2404c9835e6e3021ec640c49dfdad9bfb651e564c725(
    *,
    docker_image: typing.Optional[_DevEnvironmentDockerImage_4a8d8ffd] = None,
    ports: typing.Optional[typing.Sequence[builtins.str]] = None,
    tasks: typing.Optional[typing.Sequence[_Task_9fa875b6]] = None,
    vscode_extensions: typing.Optional[typing.Sequence[builtins.str]] = None,
    features: typing.Optional[typing.Sequence[typing.Union[DevContainerFeature, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59f53078ad4f94636f7ad21968f318db42126c330e189eccadb0cb6fefb6bfd3(
    *features: DevContainerFeature,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__924d6d8e838c592ce2bb743a8e91cb4b0f379f000355379bd65232dabc6f4efe(
    *,
    group: builtins.str,
    hidden: builtins.bool,
    order: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66fa6feb4bea9673155e5f489baae5bbdd6d528f7ce29ff754c6915092eb7036(
    *,
    action: builtins.str,
    pattern: typing.Optional[builtins.str] = None,
    uri_format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f494cab4044809f412c6dee4a08eb9aa6d128399b6c0dfdbe5d9be6e2622fed5(
    project: _Project_57d89203,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbb203f423ffcc3e6227caf2f8624610dfdc5c528c756efd2e3094d0db32f059(
    vscode: VsCode,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76028c8d6272b5133841fb2049bcddc9a00879405477a0aa27f058f8ac6dc481(
    *,
    name: builtins.str,
    request: builtins.str,
    type: builtins.str,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    console: typing.Optional[Console] = None,
    cwd: typing.Optional[builtins.str] = None,
    debug_server: typing.Optional[jsii.Number] = None,
    disable_optimistic_b_ps: typing.Optional[builtins.bool] = None,
    env: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, builtins.bool]]] = None,
    env_file: typing.Optional[builtins.str] = None,
    internal_console_options: typing.Optional[InternalConsoleOptions] = None,
    out_files: typing.Optional[typing.Sequence[builtins.str]] = None,
    port: typing.Optional[jsii.Number] = None,
    post_debug_task: typing.Optional[builtins.str] = None,
    pre_launch_task: typing.Optional[builtins.str] = None,
    presentation: typing.Optional[typing.Union[Presentation, typing.Dict[builtins.str, typing.Any]]] = None,
    program: typing.Optional[builtins.str] = None,
    runtime_args: typing.Optional[typing.Sequence[builtins.str]] = None,
    server_ready_action: typing.Optional[typing.Union[ServerReadyAction, typing.Dict[builtins.str, typing.Any]]] = None,
    skip_files: typing.Optional[typing.Sequence[builtins.str]] = None,
    stop_on_entry: typing.Optional[builtins.bool] = None,
    url: typing.Optional[builtins.str] = None,
    web_root: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e841e7e4ef3640a56bd02bfa85775b91ed62dd7fc9a8fcd482e487b75d2d4baa(
    *,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1efc4534d421a4d5a6d1ee19a7af423129f26ea3d3e365b0cbd5d316713e44b2(
    *,
    id: builtins.str,
    description: builtins.str,
    options: typing.Sequence[builtins.str],
    default: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd9f5a97332f0e03a451cdcfdd927992c1488c8dafe0f46761677f3cb7f195f7(
    *,
    id: builtins.str,
    description: builtins.str,
    default: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e672107e647965d3df7010fe525812b0c15f85ddada55b01f48ebe2c3d565725(
    vscode: VsCode,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee54c74ab4b20a8248223537312409aad3f546c2c5aeca6044e4346ce5a952d8(
    *extensions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1a69619f76a087ea88b4c83f8cee17e5d30db36f27b14f84da086de6e449d0c(
    *extensions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__513f68cf91869cc8da990fa2a1bc57a9c643d25b8264e1c057f76e3decc6dea1(
    vscode: VsCode,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__369e06bc45a74498b4cfed5bf740550cd9a57917b148178ef260593cb40c2a59(
    setting: builtins.str,
    value: typing.Any,
    language: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa3e27ee6b180fccd6eab5d9670c7024eb3f8067cb08859636119e69f07de239(
    settings: typing.Mapping[builtins.str, typing.Any],
    languages: typing.Optional[typing.Union[builtins.str, typing.Sequence[builtins.str]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50747b0b39db339de569d0b44aea84c4de3c0d9d7b268479f1a3852dfb712c0b(
    project: _Project_57d89203,
    *,
    features: typing.Optional[typing.Sequence[typing.Union[DevContainerFeature, typing.Dict[builtins.str, typing.Any]]]] = None,
    docker_image: typing.Optional[_DevEnvironmentDockerImage_4a8d8ffd] = None,
    ports: typing.Optional[typing.Sequence[builtins.str]] = None,
    tasks: typing.Optional[typing.Sequence[_Task_9fa875b6]] = None,
    vscode_extensions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24cf7d35da522ed5017c6db46a2565a5b5a09fbffc1dafabdf917aa798fea91d(
    image: _DevEnvironmentDockerImage_4a8d8ffd,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ed3f741b9b118a06d8b8f3508504c5ecb8bcbfc9c285b78e0382ac0aa4186c7(
    *features: DevContainerFeature,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3898b547dc05a8cd9427e24743e3ec87b3108cfb90befb94e77c24e156c3559d(
    *ports: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eccb3fb9f6eca40de5ffa59e4b75a85830e1113729bd9b08dc7e4128c2bfde0(
    *tasks: _Task_9fa875b6,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c13b0cafe05fa1eb28182ec3465e43421a4aa7c7e44e035db34dd4cdbce24537(
    *extensions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3572ac292b4bd9b3dc808ba9caa4797adcb64703144da90f4ad010fdedc62a30(
    *,
    id: builtins.str,
    command: builtins.str,
    args: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass
