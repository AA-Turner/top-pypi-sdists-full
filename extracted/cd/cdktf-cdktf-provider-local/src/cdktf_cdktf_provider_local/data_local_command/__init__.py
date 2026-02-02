r'''
# `data_local_command`

Refer to the Terraform Registry for docs: [`data_local_command`](https://registry.terraform.io/providers/hashicorp/local/2.6.1/docs/data-sources/command).
'''
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

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class DataLocalCommand(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-local.dataLocalCommand.DataLocalCommand",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/local/2.6.1/docs/data-sources/command local_command}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        command: builtins.str,
        allow_non_zero_exit_code: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        arguments: typing.Optional[typing.Sequence[builtins.str]] = None,
        stdin: typing.Optional[builtins.str] = None,
        working_directory: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/local/2.6.1/docs/data-sources/command local_command} Data Source.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param command: Executable name to be discovered on the PATH or absolute path to executable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.6.1/docs/data-sources/command#command DataLocalCommand#command}
        :param allow_non_zero_exit_code: Indicates that the command returning a non-zero exit code should be treated as a successful execution. Further assertions can be made of the ``exit_code`` value with the ```check`` block <https://developer.hashicorp.com/terraform/language/block/check>`_. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.6.1/docs/data-sources/command#allow_non_zero_exit_code DataLocalCommand#allow_non_zero_exit_code}
        :param arguments: Arguments to be passed to the given command. Any ``null`` arguments will be removed from the list. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.6.1/docs/data-sources/command#arguments DataLocalCommand#arguments}
        :param stdin: Data to be passed to the given command's standard input as a UTF-8 string. `Terraform values <https://developer.hashicorp.com/terraform/language/expressions/types>`_ can be encoded by any Terraform encode function, for example, ```jsonencode`` <https://developer.hashicorp.com/terraform/language/functions/jsonencode>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.6.1/docs/data-sources/command#stdin DataLocalCommand#stdin}
        :param working_directory: The directory path where the command should be executed, either an absolute path or relative to the Terraform working directory. If not provided, defaults to the Terraform working directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.6.1/docs/data-sources/command#working_directory DataLocalCommand#working_directory}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__319501a080bbd4ae73fecb14fc4a827eaedc12e286b4fdcbe1729c3e5354ffb4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = DataLocalCommandConfig(
            command=command,
            allow_non_zero_exit_code=allow_non_zero_exit_code,
            arguments=arguments,
            stdin=stdin,
            working_directory=working_directory,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a DataLocalCommand resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataLocalCommand to import.
        :param import_from_id: The id of the existing DataLocalCommand that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/local/2.6.1/docs/data-sources/command#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataLocalCommand to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbf3bfcb7e7ebb575322d2c54e29339f936882bccbfe8438a0296ebc6a1e8fc8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAllowNonZeroExitCode")
    def reset_allow_non_zero_exit_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowNonZeroExitCode", []))

    @jsii.member(jsii_name="resetArguments")
    def reset_arguments(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArguments", []))

    @jsii.member(jsii_name="resetStdin")
    def reset_stdin(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStdin", []))

    @jsii.member(jsii_name="resetWorkingDirectory")
    def reset_working_directory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkingDirectory", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="exitCode")
    def exit_code(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "exitCode"))

    @builtins.property
    @jsii.member(jsii_name="stderr")
    def stderr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stderr"))

    @builtins.property
    @jsii.member(jsii_name="stdout")
    def stdout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stdout"))

    @builtins.property
    @jsii.member(jsii_name="allowNonZeroExitCodeInput")
    def allow_non_zero_exit_code_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowNonZeroExitCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="argumentsInput")
    def arguments_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "argumentsInput"))

    @builtins.property
    @jsii.member(jsii_name="commandInput")
    def command_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commandInput"))

    @builtins.property
    @jsii.member(jsii_name="stdinInput")
    def stdin_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stdinInput"))

    @builtins.property
    @jsii.member(jsii_name="workingDirectoryInput")
    def working_directory_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workingDirectoryInput"))

    @builtins.property
    @jsii.member(jsii_name="allowNonZeroExitCode")
    def allow_non_zero_exit_code(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowNonZeroExitCode"))

    @allow_non_zero_exit_code.setter
    def allow_non_zero_exit_code(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__293582efb1602c2bc97a609f471f5e0ea53f2303742537acb19dab71391e9080)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowNonZeroExitCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="arguments")
    def arguments(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "arguments"))

    @arguments.setter
    def arguments(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d92158658fe8f983b809f05e9ab03c54a1d68aee2772ec9cda026eee3aa854c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "arguments", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="command")
    def command(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "command"))

    @command.setter
    def command(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ac1e21fa0fd609f845406ba7841ede9177a2cf44a8da5af7ade464542ca9e78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "command", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stdin")
    def stdin(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stdin"))

    @stdin.setter
    def stdin(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11d812a03f2f958b04a314a1f3dd0d470daa7e44e7cb8d080a0ed3463ae4b1d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stdin", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workingDirectory")
    def working_directory(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workingDirectory"))

    @working_directory.setter
    def working_directory(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82d44f55ec81e19f85c3c37feb481c4e9e9a4d5afd98ddfa12518413f4cf460b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workingDirectory", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-local.dataLocalCommand.DataLocalCommandConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "command": "command",
        "allow_non_zero_exit_code": "allowNonZeroExitCode",
        "arguments": "arguments",
        "stdin": "stdin",
        "working_directory": "workingDirectory",
    },
)
class DataLocalCommandConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        command: builtins.str,
        allow_non_zero_exit_code: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        arguments: typing.Optional[typing.Sequence[builtins.str]] = None,
        stdin: typing.Optional[builtins.str] = None,
        working_directory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param command: Executable name to be discovered on the PATH or absolute path to executable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.6.1/docs/data-sources/command#command DataLocalCommand#command}
        :param allow_non_zero_exit_code: Indicates that the command returning a non-zero exit code should be treated as a successful execution. Further assertions can be made of the ``exit_code`` value with the ```check`` block <https://developer.hashicorp.com/terraform/language/block/check>`_. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.6.1/docs/data-sources/command#allow_non_zero_exit_code DataLocalCommand#allow_non_zero_exit_code}
        :param arguments: Arguments to be passed to the given command. Any ``null`` arguments will be removed from the list. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.6.1/docs/data-sources/command#arguments DataLocalCommand#arguments}
        :param stdin: Data to be passed to the given command's standard input as a UTF-8 string. `Terraform values <https://developer.hashicorp.com/terraform/language/expressions/types>`_ can be encoded by any Terraform encode function, for example, ```jsonencode`` <https://developer.hashicorp.com/terraform/language/functions/jsonencode>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.6.1/docs/data-sources/command#stdin DataLocalCommand#stdin}
        :param working_directory: The directory path where the command should be executed, either an absolute path or relative to the Terraform working directory. If not provided, defaults to the Terraform working directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.6.1/docs/data-sources/command#working_directory DataLocalCommand#working_directory}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8181b5a6677bd19058d83b782ad5d0003aa0799df5261c60f642d27eb5b34453)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
            check_type(argname="argument allow_non_zero_exit_code", value=allow_non_zero_exit_code, expected_type=type_hints["allow_non_zero_exit_code"])
            check_type(argname="argument arguments", value=arguments, expected_type=type_hints["arguments"])
            check_type(argname="argument stdin", value=stdin, expected_type=type_hints["stdin"])
            check_type(argname="argument working_directory", value=working_directory, expected_type=type_hints["working_directory"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "command": command,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if allow_non_zero_exit_code is not None:
            self._values["allow_non_zero_exit_code"] = allow_non_zero_exit_code
        if arguments is not None:
            self._values["arguments"] = arguments
        if stdin is not None:
            self._values["stdin"] = stdin
        if working_directory is not None:
            self._values["working_directory"] = working_directory

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def command(self) -> builtins.str:
        '''Executable name to be discovered on the PATH or absolute path to executable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.6.1/docs/data-sources/command#command DataLocalCommand#command}
        '''
        result = self._values.get("command")
        assert result is not None, "Required property 'command' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_non_zero_exit_code(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates that the command returning a non-zero exit code should be treated as a successful execution.

        Further assertions can be made of the ``exit_code`` value with the ```check`` block <https://developer.hashicorp.com/terraform/language/block/check>`_. Defaults to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.6.1/docs/data-sources/command#allow_non_zero_exit_code DataLocalCommand#allow_non_zero_exit_code}
        '''
        result = self._values.get("allow_non_zero_exit_code")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def arguments(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Arguments to be passed to the given command. Any ``null`` arguments will be removed from the list.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.6.1/docs/data-sources/command#arguments DataLocalCommand#arguments}
        '''
        result = self._values.get("arguments")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def stdin(self) -> typing.Optional[builtins.str]:
        '''Data to be passed to the given command's standard input as a UTF-8 string.

        `Terraform values <https://developer.hashicorp.com/terraform/language/expressions/types>`_ can be encoded by any Terraform encode function, for example, ```jsonencode`` <https://developer.hashicorp.com/terraform/language/functions/jsonencode>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.6.1/docs/data-sources/command#stdin DataLocalCommand#stdin}
        '''
        result = self._values.get("stdin")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def working_directory(self) -> typing.Optional[builtins.str]:
        '''The directory path where the command should be executed, either an absolute path or relative to the Terraform working directory.

        If not provided, defaults to the Terraform working directory.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.6.1/docs/data-sources/command#working_directory DataLocalCommand#working_directory}
        '''
        result = self._values.get("working_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLocalCommandConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DataLocalCommand",
    "DataLocalCommandConfig",
]

publication.publish()

def _typecheckingstub__319501a080bbd4ae73fecb14fc4a827eaedc12e286b4fdcbe1729c3e5354ffb4(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    command: builtins.str,
    allow_non_zero_exit_code: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    arguments: typing.Optional[typing.Sequence[builtins.str]] = None,
    stdin: typing.Optional[builtins.str] = None,
    working_directory: typing.Optional[builtins.str] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbf3bfcb7e7ebb575322d2c54e29339f936882bccbfe8438a0296ebc6a1e8fc8(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__293582efb1602c2bc97a609f471f5e0ea53f2303742537acb19dab71391e9080(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d92158658fe8f983b809f05e9ab03c54a1d68aee2772ec9cda026eee3aa854c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ac1e21fa0fd609f845406ba7841ede9177a2cf44a8da5af7ade464542ca9e78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11d812a03f2f958b04a314a1f3dd0d470daa7e44e7cb8d080a0ed3463ae4b1d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82d44f55ec81e19f85c3c37feb481c4e9e9a4d5afd98ddfa12518413f4cf460b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8181b5a6677bd19058d83b782ad5d0003aa0799df5261c60f642d27eb5b34453(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    command: builtins.str,
    allow_non_zero_exit_code: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    arguments: typing.Optional[typing.Sequence[builtins.str]] = None,
    stdin: typing.Optional[builtins.str] = None,
    working_directory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
