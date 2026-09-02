r'''
# `github_actions_hosted_runner`

Refer to the Terraform Registry for docs: [`github_actions_hosted_runner`](https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/actions_hosted_runner).
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


class ActionsHostedRunner(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.actionsHostedRunner.ActionsHostedRunner",
):
    '''Represents a {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/actions_hosted_runner github_actions_hosted_runner}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        image: typing.Union["ActionsHostedRunnerImage", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        runner_group_id: jsii.Number,
        size: builtins.str,
        image_gen: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        image_version: typing.Optional[builtins.str] = None,
        maximum_runners: typing.Optional[jsii.Number] = None,
        public_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["ActionsHostedRunnerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/actions_hosted_runner github_actions_hosted_runner} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param image: image block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/actions_hosted_runner#image ActionsHostedRunner#image}
        :param name: Name of the hosted runner. Must be between 1 and 64 characters and may only contain upper and lowercase letters a-z, numbers 0-9, '.', '-', and '_'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/actions_hosted_runner#name ActionsHostedRunner#name}
        :param runner_group_id: The runner group ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/actions_hosted_runner#runner_group_id ActionsHostedRunner#runner_group_id}
        :param size: Machine size (e.g., '4-core', '8-core'). Can be updated to scale the runner. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/actions_hosted_runner#size ActionsHostedRunner#size}
        :param image_gen: Whether this runner should be used to generate custom images. Cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/actions_hosted_runner#image_gen ActionsHostedRunner#image_gen}
        :param image_version: The version of the runner image to deploy. This is relevant only for runners using custom images. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/actions_hosted_runner#image_version ActionsHostedRunner#image_version}
        :param maximum_runners: Maximum number of runners to scale up to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/actions_hosted_runner#maximum_runners ActionsHostedRunner#maximum_runners}
        :param public_ip_enabled: Whether to enable static public IP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/actions_hosted_runner#public_ip_enabled ActionsHostedRunner#public_ip_enabled}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/actions_hosted_runner#timeouts ActionsHostedRunner#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76f4a323331c601ab528acb8e01cda5d4e166d3407e7878efc62ea7bfff24ea5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = ActionsHostedRunnerConfig(
            image=image,
            name=name,
            runner_group_id=runner_group_id,
            size=size,
            image_gen=image_gen,
            image_version=image_version,
            maximum_runners=maximum_runners,
            public_ip_enabled=public_ip_enabled,
            timeouts=timeouts,
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
        '''Generates CDKTF code for importing a ActionsHostedRunner resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ActionsHostedRunner to import.
        :param import_from_id: The id of the existing ActionsHostedRunner that should be imported. Refer to the {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/actions_hosted_runner#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ActionsHostedRunner to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6c35ee684e17bac129136431985e36d72b638b15e62a92c37b1d3b43557b699)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putImage")
    def put_image(
        self,
        *,
        id: builtins.str,
        source: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: The image ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/actions_hosted_runner#id ActionsHostedRunner#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param source: The image source (github, partner, or custom). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/actions_hosted_runner#source ActionsHostedRunner#source}
        '''
        value = ActionsHostedRunnerImage(id=id, source=source)

        return typing.cast(None, jsii.invoke(self, "putImage", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(self, *, delete: typing.Optional[builtins.str] = None) -> None:
        '''
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/actions_hosted_runner#delete ActionsHostedRunner#delete}.
        '''
        value = ActionsHostedRunnerTimeouts(delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetImageGen")
    def reset_image_gen(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageGen", []))

    @jsii.member(jsii_name="resetImageVersion")
    def reset_image_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageVersion", []))

    @jsii.member(jsii_name="resetMaximumRunners")
    def reset_maximum_runners(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumRunners", []))

    @jsii.member(jsii_name="resetPublicIpEnabled")
    def reset_public_ip_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicIpEnabled", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

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
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> "ActionsHostedRunnerImageOutputReference":
        return typing.cast("ActionsHostedRunnerImageOutputReference", jsii.get(self, "image"))

    @builtins.property
    @jsii.member(jsii_name="lastActiveOn")
    def last_active_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastActiveOn"))

    @builtins.property
    @jsii.member(jsii_name="machineSizeDetails")
    def machine_size_details(self) -> "ActionsHostedRunnerMachineSizeDetailsList":
        return typing.cast("ActionsHostedRunnerMachineSizeDetailsList", jsii.get(self, "machineSizeDetails"))

    @builtins.property
    @jsii.member(jsii_name="platform")
    def platform(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "platform"))

    @builtins.property
    @jsii.member(jsii_name="publicIps")
    def public_ips(self) -> "ActionsHostedRunnerPublicIpsList":
        return typing.cast("ActionsHostedRunnerPublicIpsList", jsii.get(self, "publicIps"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ActionsHostedRunnerTimeoutsOutputReference":
        return typing.cast("ActionsHostedRunnerTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="imageGenInput")
    def image_gen_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "imageGenInput"))

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(self) -> typing.Optional["ActionsHostedRunnerImage"]:
        return typing.cast(typing.Optional["ActionsHostedRunnerImage"], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="imageVersionInput")
    def image_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumRunnersInput")
    def maximum_runners_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumRunnersInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="publicIpEnabledInput")
    def public_ip_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "publicIpEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="runnerGroupIdInput")
    def runner_group_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "runnerGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeInput")
    def size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sizeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ActionsHostedRunnerTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ActionsHostedRunnerTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="imageGen")
    def image_gen(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "imageGen"))

    @image_gen.setter
    def image_gen(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69d01a951a49651f463cde4da807eab561eea47eb7c7af82ad497409b643838f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageGen", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageVersion")
    def image_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageVersion"))

    @image_version.setter
    def image_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d93d00a7ee46e7ad82349be3f38042743909d15173868ec8f8137a51bbde79ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumRunners")
    def maximum_runners(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumRunners"))

    @maximum_runners.setter
    def maximum_runners(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__146fe15aa6cf9bf76cdf0c6ff8f25673fd2ee9878a0f1d58f2be59e9f4fe9696)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumRunners", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40c56e0bc78d5561287221511c2c59a6ef7c261a0a103a589f2d5412db585370)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicIpEnabled")
    def public_ip_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "publicIpEnabled"))

    @public_ip_enabled.setter
    def public_ip_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c1c433340c1c448023a2415c0429c99c47e1fad8bae2f2d6d3d4bb9994ec25b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicIpEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runnerGroupId")
    def runner_group_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "runnerGroupId"))

    @runner_group_id.setter
    def runner_group_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbbe3bcc69923ea16a5275fe9c9d974e6c75df07a54865b2f1292a47a58ff21c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runnerGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "size"))

    @size.setter
    def size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73ef24f8eab0f1ab81b62b8e05c3b1666e66dc2d20e558d8b6d5fcdeba7096be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "size", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.actionsHostedRunner.ActionsHostedRunnerConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "image": "image",
        "name": "name",
        "runner_group_id": "runnerGroupId",
        "size": "size",
        "image_gen": "imageGen",
        "image_version": "imageVersion",
        "maximum_runners": "maximumRunners",
        "public_ip_enabled": "publicIpEnabled",
        "timeouts": "timeouts",
    },
)
class ActionsHostedRunnerConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        image: typing.Union["ActionsHostedRunnerImage", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        runner_group_id: jsii.Number,
        size: builtins.str,
        image_gen: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        image_version: typing.Optional[builtins.str] = None,
        maximum_runners: typing.Optional[jsii.Number] = None,
        public_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["ActionsHostedRunnerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param image: image block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/actions_hosted_runner#image ActionsHostedRunner#image}
        :param name: Name of the hosted runner. Must be between 1 and 64 characters and may only contain upper and lowercase letters a-z, numbers 0-9, '.', '-', and '_'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/actions_hosted_runner#name ActionsHostedRunner#name}
        :param runner_group_id: The runner group ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/actions_hosted_runner#runner_group_id ActionsHostedRunner#runner_group_id}
        :param size: Machine size (e.g., '4-core', '8-core'). Can be updated to scale the runner. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/actions_hosted_runner#size ActionsHostedRunner#size}
        :param image_gen: Whether this runner should be used to generate custom images. Cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/actions_hosted_runner#image_gen ActionsHostedRunner#image_gen}
        :param image_version: The version of the runner image to deploy. This is relevant only for runners using custom images. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/actions_hosted_runner#image_version ActionsHostedRunner#image_version}
        :param maximum_runners: Maximum number of runners to scale up to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/actions_hosted_runner#maximum_runners ActionsHostedRunner#maximum_runners}
        :param public_ip_enabled: Whether to enable static public IP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/actions_hosted_runner#public_ip_enabled ActionsHostedRunner#public_ip_enabled}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/actions_hosted_runner#timeouts ActionsHostedRunner#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(image, dict):
            image = ActionsHostedRunnerImage(**image)
        if isinstance(timeouts, dict):
            timeouts = ActionsHostedRunnerTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fec65bac3271da22221361974b8590eee77de7bce4944eeff9f2dbbac056196f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument runner_group_id", value=runner_group_id, expected_type=type_hints["runner_group_id"])
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
            check_type(argname="argument image_gen", value=image_gen, expected_type=type_hints["image_gen"])
            check_type(argname="argument image_version", value=image_version, expected_type=type_hints["image_version"])
            check_type(argname="argument maximum_runners", value=maximum_runners, expected_type=type_hints["maximum_runners"])
            check_type(argname="argument public_ip_enabled", value=public_ip_enabled, expected_type=type_hints["public_ip_enabled"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image": image,
            "name": name,
            "runner_group_id": runner_group_id,
            "size": size,
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
        if image_gen is not None:
            self._values["image_gen"] = image_gen
        if image_version is not None:
            self._values["image_version"] = image_version
        if maximum_runners is not None:
            self._values["maximum_runners"] = maximum_runners
        if public_ip_enabled is not None:
            self._values["public_ip_enabled"] = public_ip_enabled
        if timeouts is not None:
            self._values["timeouts"] = timeouts

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
    def image(self) -> "ActionsHostedRunnerImage":
        '''image block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/actions_hosted_runner#image ActionsHostedRunner#image}
        '''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast("ActionsHostedRunnerImage", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the hosted runner.

        Must be between 1 and 64 characters and may only contain upper and lowercase letters a-z, numbers 0-9, '.', '-', and '_'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/actions_hosted_runner#name ActionsHostedRunner#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def runner_group_id(self) -> jsii.Number:
        '''The runner group ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/actions_hosted_runner#runner_group_id ActionsHostedRunner#runner_group_id}
        '''
        result = self._values.get("runner_group_id")
        assert result is not None, "Required property 'runner_group_id' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def size(self) -> builtins.str:
        '''Machine size (e.g., '4-core', '8-core'). Can be updated to scale the runner.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/actions_hosted_runner#size ActionsHostedRunner#size}
        '''
        result = self._values.get("size")
        assert result is not None, "Required property 'size' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def image_gen(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether this runner should be used to generate custom images. Cannot be changed after creation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/actions_hosted_runner#image_gen ActionsHostedRunner#image_gen}
        '''
        result = self._values.get("image_gen")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def image_version(self) -> typing.Optional[builtins.str]:
        '''The version of the runner image to deploy. This is relevant only for runners using custom images.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/actions_hosted_runner#image_version ActionsHostedRunner#image_version}
        '''
        result = self._values.get("image_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maximum_runners(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of runners to scale up to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/actions_hosted_runner#maximum_runners ActionsHostedRunner#maximum_runners}
        '''
        result = self._values.get("maximum_runners")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def public_ip_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to enable static public IP.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/actions_hosted_runner#public_ip_enabled ActionsHostedRunner#public_ip_enabled}
        '''
        result = self._values.get("public_ip_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ActionsHostedRunnerTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/actions_hosted_runner#timeouts ActionsHostedRunner#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ActionsHostedRunnerTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActionsHostedRunnerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-github.actionsHostedRunner.ActionsHostedRunnerImage",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "source": "source"},
)
class ActionsHostedRunnerImage:
    def __init__(
        self,
        *,
        id: builtins.str,
        source: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: The image ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/actions_hosted_runner#id ActionsHostedRunner#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param source: The image source (github, partner, or custom). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/actions_hosted_runner#source ActionsHostedRunner#source}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02ac1de1277853b7c8ede125fd1854e700c9a5393f8c245cdd8c8999bd46ddd0)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
        }
        if source is not None:
            self._values["source"] = source

    @builtins.property
    def id(self) -> builtins.str:
        '''The image ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/actions_hosted_runner#id ActionsHostedRunner#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''The image source (github, partner, or custom).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/actions_hosted_runner#source ActionsHostedRunner#source}
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActionsHostedRunnerImage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ActionsHostedRunnerImageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.actionsHostedRunner.ActionsHostedRunnerImageOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e17923af562c983d3063b61bd314714bbe941a8e47db3e4145cd3fc18ce9244e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSource")
    def reset_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSource", []))

    @builtins.property
    @jsii.member(jsii_name="sizeGb")
    def size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sizeGb"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a41bfe6f3da517a2366f68013bcf598e807065f2516df226f1ca4707bf1fb19a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91086f46707235304990b4c486c68a3ad6f7adcea1b45385a029f8eba40d1f12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ActionsHostedRunnerImage]:
        return typing.cast(typing.Optional[ActionsHostedRunnerImage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ActionsHostedRunnerImage]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__265c81667c06cc1a279223e8a054fb821a1f95fa1eaabc4d4bd160e0be3dd37e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.actionsHostedRunner.ActionsHostedRunnerMachineSizeDetails",
    jsii_struct_bases=[],
    name_mapping={},
)
class ActionsHostedRunnerMachineSizeDetails:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActionsHostedRunnerMachineSizeDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ActionsHostedRunnerMachineSizeDetailsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.actionsHostedRunner.ActionsHostedRunnerMachineSizeDetailsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6abdd9dbce190183d7f1afec6d68d3083cedecd7923d1bffd62f265a7bb3d3a8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ActionsHostedRunnerMachineSizeDetailsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c409f01ce671de748ba868d2861a2de99c042d7d53e1a8bf41211c42ed24bb1c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ActionsHostedRunnerMachineSizeDetailsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df21e2e91a1240262feb93b48c88162bd82aaf2c3e6c861702dcc49c89816335)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5288c883dd20c64950c1dad2ae045f04a9914e8a4a57c886b415bc7ad59e31c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d55908bb71eeac28a8177104352ed0d1d52e67d2a38f2cce2b74b720324c661)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ActionsHostedRunnerMachineSizeDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.actionsHostedRunner.ActionsHostedRunnerMachineSizeDetailsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf29c50a676bad73ef479b8ed9ecbef2f686459a8d7213e88eb61b0db5a04dcc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="cpuCores")
    def cpu_cores(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuCores"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="memoryGb")
    def memory_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memoryGb"))

    @builtins.property
    @jsii.member(jsii_name="storageGb")
    def storage_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "storageGb"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ActionsHostedRunnerMachineSizeDetails]:
        return typing.cast(typing.Optional[ActionsHostedRunnerMachineSizeDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ActionsHostedRunnerMachineSizeDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbc088bd103364b5f57908e4e9f5c28609adffbb6c5ef8fd0631c53427ab2c8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.actionsHostedRunner.ActionsHostedRunnerPublicIps",
    jsii_struct_bases=[],
    name_mapping={},
)
class ActionsHostedRunnerPublicIps:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActionsHostedRunnerPublicIps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ActionsHostedRunnerPublicIpsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.actionsHostedRunner.ActionsHostedRunnerPublicIpsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f64d5fb6613d48e959e5bf66f2e522d3ab9253aa17f46ac759190dec731f53e7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ActionsHostedRunnerPublicIpsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afd0ad6800c5defa39c7da09172c655a32ca652be0f940f7673b7d0cce3ab7d2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ActionsHostedRunnerPublicIpsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c26f629ee52b3c0c5e87a9550758e58e9e88b680caf4c88fc017a840e131325)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c8e12801378f72aa43d55fda7742c2abdb0bad329ab27dee99b5fce428e85bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a5aa84cd790ba4f016d092b919b26f79eafc4fecc5060585f3f34ad8e36c1bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ActionsHostedRunnerPublicIpsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.actionsHostedRunner.ActionsHostedRunnerPublicIpsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e74177e5078506e309ca6551bc910a69de4a5002976036a48bd86d8b2ebd807)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "enabled"))

    @builtins.property
    @jsii.member(jsii_name="length")
    def length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "length"))

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ActionsHostedRunnerPublicIps]:
        return typing.cast(typing.Optional[ActionsHostedRunnerPublicIps], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ActionsHostedRunnerPublicIps],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8767a977702959b9f9a95a8363db2833921b7658e84769396cd8be17bc2effe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.actionsHostedRunner.ActionsHostedRunnerTimeouts",
    jsii_struct_bases=[],
    name_mapping={"delete": "delete"},
)
class ActionsHostedRunnerTimeouts:
    def __init__(self, *, delete: typing.Optional[builtins.str] = None) -> None:
        '''
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/actions_hosted_runner#delete ActionsHostedRunner#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff468a07c85c4cf95ec66ac27fda5e6ca2ec1ef5a73261e76270a3e285cbd04c)
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/actions_hosted_runner#delete ActionsHostedRunner#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActionsHostedRunnerTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ActionsHostedRunnerTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.actionsHostedRunner.ActionsHostedRunnerTimeoutsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__defcbe998ea2adb7d4a4fff4e035cd3db1ea4521af10623964802e3b7b68f5e9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc1f6b98978a330b786813c652538c55b37fc672fa82ef3224a177fc4342fd16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ActionsHostedRunnerTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ActionsHostedRunnerTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ActionsHostedRunnerTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43e7c5a421d2a884812bda3e08e3891f230e7850baa89357abfba8f4aee7279a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ActionsHostedRunner",
    "ActionsHostedRunnerConfig",
    "ActionsHostedRunnerImage",
    "ActionsHostedRunnerImageOutputReference",
    "ActionsHostedRunnerMachineSizeDetails",
    "ActionsHostedRunnerMachineSizeDetailsList",
    "ActionsHostedRunnerMachineSizeDetailsOutputReference",
    "ActionsHostedRunnerPublicIps",
    "ActionsHostedRunnerPublicIpsList",
    "ActionsHostedRunnerPublicIpsOutputReference",
    "ActionsHostedRunnerTimeouts",
    "ActionsHostedRunnerTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__76f4a323331c601ab528acb8e01cda5d4e166d3407e7878efc62ea7bfff24ea5(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    image: typing.Union[ActionsHostedRunnerImage, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    runner_group_id: jsii.Number,
    size: builtins.str,
    image_gen: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    image_version: typing.Optional[builtins.str] = None,
    maximum_runners: typing.Optional[jsii.Number] = None,
    public_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[ActionsHostedRunnerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__f6c35ee684e17bac129136431985e36d72b638b15e62a92c37b1d3b43557b699(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69d01a951a49651f463cde4da807eab561eea47eb7c7af82ad497409b643838f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d93d00a7ee46e7ad82349be3f38042743909d15173868ec8f8137a51bbde79ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__146fe15aa6cf9bf76cdf0c6ff8f25673fd2ee9878a0f1d58f2be59e9f4fe9696(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40c56e0bc78d5561287221511c2c59a6ef7c261a0a103a589f2d5412db585370(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c1c433340c1c448023a2415c0429c99c47e1fad8bae2f2d6d3d4bb9994ec25b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbbe3bcc69923ea16a5275fe9c9d974e6c75df07a54865b2f1292a47a58ff21c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73ef24f8eab0f1ab81b62b8e05c3b1666e66dc2d20e558d8b6d5fcdeba7096be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fec65bac3271da22221361974b8590eee77de7bce4944eeff9f2dbbac056196f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    image: typing.Union[ActionsHostedRunnerImage, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    runner_group_id: jsii.Number,
    size: builtins.str,
    image_gen: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    image_version: typing.Optional[builtins.str] = None,
    maximum_runners: typing.Optional[jsii.Number] = None,
    public_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[ActionsHostedRunnerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02ac1de1277853b7c8ede125fd1854e700c9a5393f8c245cdd8c8999bd46ddd0(
    *,
    id: builtins.str,
    source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e17923af562c983d3063b61bd314714bbe941a8e47db3e4145cd3fc18ce9244e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a41bfe6f3da517a2366f68013bcf598e807065f2516df226f1ca4707bf1fb19a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91086f46707235304990b4c486c68a3ad6f7adcea1b45385a029f8eba40d1f12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__265c81667c06cc1a279223e8a054fb821a1f95fa1eaabc4d4bd160e0be3dd37e(
    value: typing.Optional[ActionsHostedRunnerImage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6abdd9dbce190183d7f1afec6d68d3083cedecd7923d1bffd62f265a7bb3d3a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c409f01ce671de748ba868d2861a2de99c042d7d53e1a8bf41211c42ed24bb1c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df21e2e91a1240262feb93b48c88162bd82aaf2c3e6c861702dcc49c89816335(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5288c883dd20c64950c1dad2ae045f04a9914e8a4a57c886b415bc7ad59e31c9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d55908bb71eeac28a8177104352ed0d1d52e67d2a38f2cce2b74b720324c661(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf29c50a676bad73ef479b8ed9ecbef2f686459a8d7213e88eb61b0db5a04dcc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbc088bd103364b5f57908e4e9f5c28609adffbb6c5ef8fd0631c53427ab2c8b(
    value: typing.Optional[ActionsHostedRunnerMachineSizeDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f64d5fb6613d48e959e5bf66f2e522d3ab9253aa17f46ac759190dec731f53e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afd0ad6800c5defa39c7da09172c655a32ca652be0f940f7673b7d0cce3ab7d2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c26f629ee52b3c0c5e87a9550758e58e9e88b680caf4c88fc017a840e131325(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c8e12801378f72aa43d55fda7742c2abdb0bad329ab27dee99b5fce428e85bc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a5aa84cd790ba4f016d092b919b26f79eafc4fecc5060585f3f34ad8e36c1bb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e74177e5078506e309ca6551bc910a69de4a5002976036a48bd86d8b2ebd807(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8767a977702959b9f9a95a8363db2833921b7658e84769396cd8be17bc2effe(
    value: typing.Optional[ActionsHostedRunnerPublicIps],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff468a07c85c4cf95ec66ac27fda5e6ca2ec1ef5a73261e76270a3e285cbd04c(
    *,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__defcbe998ea2adb7d4a4fff4e035cd3db1ea4521af10623964802e3b7b68f5e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc1f6b98978a330b786813c652538c55b37fc672fa82ef3224a177fc4342fd16(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43e7c5a421d2a884812bda3e08e3891f230e7850baa89357abfba8f4aee7279a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ActionsHostedRunnerTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
