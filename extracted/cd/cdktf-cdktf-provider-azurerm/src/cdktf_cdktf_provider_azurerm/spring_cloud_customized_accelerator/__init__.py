r'''
# `azurerm_spring_cloud_customized_accelerator`

Refer to the Terraform Registry for docs: [`azurerm_spring_cloud_customized_accelerator`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator).
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


class SpringCloudCustomizedAccelerator(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.springCloudCustomizedAccelerator.SpringCloudCustomizedAccelerator",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator azurerm_spring_cloud_customized_accelerator}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        git_repository: typing.Union["SpringCloudCustomizedAcceleratorGitRepository", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        spring_cloud_accelerator_id: builtins.str,
        accelerator_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        accelerator_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        icon_url: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["SpringCloudCustomizedAcceleratorTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator azurerm_spring_cloud_customized_accelerator} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param git_repository: git_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#git_repository SpringCloudCustomizedAccelerator#git_repository}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#name SpringCloudCustomizedAccelerator#name}.
        :param spring_cloud_accelerator_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#spring_cloud_accelerator_id SpringCloudCustomizedAccelerator#spring_cloud_accelerator_id}.
        :param accelerator_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#accelerator_tags SpringCloudCustomizedAccelerator#accelerator_tags}.
        :param accelerator_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#accelerator_type SpringCloudCustomizedAccelerator#accelerator_type}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#description SpringCloudCustomizedAccelerator#description}.
        :param display_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#display_name SpringCloudCustomizedAccelerator#display_name}.
        :param icon_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#icon_url SpringCloudCustomizedAccelerator#icon_url}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#id SpringCloudCustomizedAccelerator#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#timeouts SpringCloudCustomizedAccelerator#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__721b699bbc6f71618f3551292c52c336a94e6cf63ede51076de1666b11683eab)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SpringCloudCustomizedAcceleratorConfig(
            git_repository=git_repository,
            name=name,
            spring_cloud_accelerator_id=spring_cloud_accelerator_id,
            accelerator_tags=accelerator_tags,
            accelerator_type=accelerator_type,
            description=description,
            display_name=display_name,
            icon_url=icon_url,
            id=id,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a SpringCloudCustomizedAccelerator resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SpringCloudCustomizedAccelerator to import.
        :param import_from_id: The id of the existing SpringCloudCustomizedAccelerator that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SpringCloudCustomizedAccelerator to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38c3951daeb41ef9db522505605439f1a15bf4516ecd711db79e51710da953e4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putGitRepository")
    def put_git_repository(
        self,
        *,
        url: builtins.str,
        basic_auth: typing.Optional[typing.Union["SpringCloudCustomizedAcceleratorGitRepositoryBasicAuth", typing.Dict[builtins.str, typing.Any]]] = None,
        branch: typing.Optional[builtins.str] = None,
        ca_certificate_id: typing.Optional[builtins.str] = None,
        commit: typing.Optional[builtins.str] = None,
        git_tag: typing.Optional[builtins.str] = None,
        interval_in_seconds: typing.Optional[jsii.Number] = None,
        path: typing.Optional[builtins.str] = None,
        ssh_auth: typing.Optional[typing.Union["SpringCloudCustomizedAcceleratorGitRepositorySshAuth", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#url SpringCloudCustomizedAccelerator#url}.
        :param basic_auth: basic_auth block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#basic_auth SpringCloudCustomizedAccelerator#basic_auth}
        :param branch: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#branch SpringCloudCustomizedAccelerator#branch}.
        :param ca_certificate_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#ca_certificate_id SpringCloudCustomizedAccelerator#ca_certificate_id}.
        :param commit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#commit SpringCloudCustomizedAccelerator#commit}.
        :param git_tag: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#git_tag SpringCloudCustomizedAccelerator#git_tag}.
        :param interval_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#interval_in_seconds SpringCloudCustomizedAccelerator#interval_in_seconds}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#path SpringCloudCustomizedAccelerator#path}.
        :param ssh_auth: ssh_auth block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#ssh_auth SpringCloudCustomizedAccelerator#ssh_auth}
        '''
        value = SpringCloudCustomizedAcceleratorGitRepository(
            url=url,
            basic_auth=basic_auth,
            branch=branch,
            ca_certificate_id=ca_certificate_id,
            commit=commit,
            git_tag=git_tag,
            interval_in_seconds=interval_in_seconds,
            path=path,
            ssh_auth=ssh_auth,
        )

        return typing.cast(None, jsii.invoke(self, "putGitRepository", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#create SpringCloudCustomizedAccelerator#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#delete SpringCloudCustomizedAccelerator#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#read SpringCloudCustomizedAccelerator#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#update SpringCloudCustomizedAccelerator#update}.
        '''
        value = SpringCloudCustomizedAcceleratorTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAcceleratorTags")
    def reset_accelerator_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcceleratorTags", []))

    @jsii.member(jsii_name="resetAcceleratorType")
    def reset_accelerator_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcceleratorType", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetIconUrl")
    def reset_icon_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIconUrl", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="gitRepository")
    def git_repository(
        self,
    ) -> "SpringCloudCustomizedAcceleratorGitRepositoryOutputReference":
        return typing.cast("SpringCloudCustomizedAcceleratorGitRepositoryOutputReference", jsii.get(self, "gitRepository"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "SpringCloudCustomizedAcceleratorTimeoutsOutputReference":
        return typing.cast("SpringCloudCustomizedAcceleratorTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorTagsInput")
    def accelerator_tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "acceleratorTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorTypeInput")
    def accelerator_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "acceleratorTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="gitRepositoryInput")
    def git_repository_input(
        self,
    ) -> typing.Optional["SpringCloudCustomizedAcceleratorGitRepository"]:
        return typing.cast(typing.Optional["SpringCloudCustomizedAcceleratorGitRepository"], jsii.get(self, "gitRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="iconUrlInput")
    def icon_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iconUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="springCloudAcceleratorIdInput")
    def spring_cloud_accelerator_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "springCloudAcceleratorIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SpringCloudCustomizedAcceleratorTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SpringCloudCustomizedAcceleratorTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorTags")
    def accelerator_tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "acceleratorTags"))

    @accelerator_tags.setter
    def accelerator_tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72e4975032c86a1d30050ab5584a681ef4e9f55d0d250f2601e6f73cd0d8c1a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="acceleratorType")
    def accelerator_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "acceleratorType"))

    @accelerator_type.setter
    def accelerator_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d94911f14246923bd82514a47e0fd388ede2904a7c37ac62344530804f257ff1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__881f59f8118f3048369ac90e2a2d634d296ecab6d97fdb6d0dc1d33cb51239ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fa0aed4bb563e3543099e3f1e48dbce06abcc683ebc348905dca0684001f5a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="iconUrl")
    def icon_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "iconUrl"))

    @icon_url.setter
    def icon_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77303490445e4b96123b9b3e82dc057dabade5e959baba96c7873871267cf153)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iconUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a173ae8595bad5b9c815095148176ed49af29b12e4c66e8eaccf987e99b64fa5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c08146f15cc44c2df0e1c18ebc09b9440c18f2cc213d10f29cb8cf6e5e9bc208)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="springCloudAcceleratorId")
    def spring_cloud_accelerator_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "springCloudAcceleratorId"))

    @spring_cloud_accelerator_id.setter
    def spring_cloud_accelerator_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e12e5188560e5f8a33afc9633766246a9f2e88fb49cad547f46a6f5dc0bfaf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "springCloudAcceleratorId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.springCloudCustomizedAccelerator.SpringCloudCustomizedAcceleratorConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "git_repository": "gitRepository",
        "name": "name",
        "spring_cloud_accelerator_id": "springCloudAcceleratorId",
        "accelerator_tags": "acceleratorTags",
        "accelerator_type": "acceleratorType",
        "description": "description",
        "display_name": "displayName",
        "icon_url": "iconUrl",
        "id": "id",
        "timeouts": "timeouts",
    },
)
class SpringCloudCustomizedAcceleratorConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        git_repository: typing.Union["SpringCloudCustomizedAcceleratorGitRepository", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        spring_cloud_accelerator_id: builtins.str,
        accelerator_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        accelerator_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        icon_url: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["SpringCloudCustomizedAcceleratorTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param git_repository: git_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#git_repository SpringCloudCustomizedAccelerator#git_repository}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#name SpringCloudCustomizedAccelerator#name}.
        :param spring_cloud_accelerator_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#spring_cloud_accelerator_id SpringCloudCustomizedAccelerator#spring_cloud_accelerator_id}.
        :param accelerator_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#accelerator_tags SpringCloudCustomizedAccelerator#accelerator_tags}.
        :param accelerator_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#accelerator_type SpringCloudCustomizedAccelerator#accelerator_type}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#description SpringCloudCustomizedAccelerator#description}.
        :param display_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#display_name SpringCloudCustomizedAccelerator#display_name}.
        :param icon_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#icon_url SpringCloudCustomizedAccelerator#icon_url}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#id SpringCloudCustomizedAccelerator#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#timeouts SpringCloudCustomizedAccelerator#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(git_repository, dict):
            git_repository = SpringCloudCustomizedAcceleratorGitRepository(**git_repository)
        if isinstance(timeouts, dict):
            timeouts = SpringCloudCustomizedAcceleratorTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bd7b86cdea3d49e6ad884690b5fd977c78ed7dd69344ff2123d8ff4de05ef47)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument git_repository", value=git_repository, expected_type=type_hints["git_repository"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument spring_cloud_accelerator_id", value=spring_cloud_accelerator_id, expected_type=type_hints["spring_cloud_accelerator_id"])
            check_type(argname="argument accelerator_tags", value=accelerator_tags, expected_type=type_hints["accelerator_tags"])
            check_type(argname="argument accelerator_type", value=accelerator_type, expected_type=type_hints["accelerator_type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument icon_url", value=icon_url, expected_type=type_hints["icon_url"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "git_repository": git_repository,
            "name": name,
            "spring_cloud_accelerator_id": spring_cloud_accelerator_id,
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
        if accelerator_tags is not None:
            self._values["accelerator_tags"] = accelerator_tags
        if accelerator_type is not None:
            self._values["accelerator_type"] = accelerator_type
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if icon_url is not None:
            self._values["icon_url"] = icon_url
        if id is not None:
            self._values["id"] = id
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
    def git_repository(self) -> "SpringCloudCustomizedAcceleratorGitRepository":
        '''git_repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#git_repository SpringCloudCustomizedAccelerator#git_repository}
        '''
        result = self._values.get("git_repository")
        assert result is not None, "Required property 'git_repository' is missing"
        return typing.cast("SpringCloudCustomizedAcceleratorGitRepository", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#name SpringCloudCustomizedAccelerator#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def spring_cloud_accelerator_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#spring_cloud_accelerator_id SpringCloudCustomizedAccelerator#spring_cloud_accelerator_id}.'''
        result = self._values.get("spring_cloud_accelerator_id")
        assert result is not None, "Required property 'spring_cloud_accelerator_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def accelerator_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#accelerator_tags SpringCloudCustomizedAccelerator#accelerator_tags}.'''
        result = self._values.get("accelerator_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def accelerator_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#accelerator_type SpringCloudCustomizedAccelerator#accelerator_type}.'''
        result = self._values.get("accelerator_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#description SpringCloudCustomizedAccelerator#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#display_name SpringCloudCustomizedAccelerator#display_name}.'''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def icon_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#icon_url SpringCloudCustomizedAccelerator#icon_url}.'''
        result = self._values.get("icon_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#id SpringCloudCustomizedAccelerator#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["SpringCloudCustomizedAcceleratorTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#timeouts SpringCloudCustomizedAccelerator#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["SpringCloudCustomizedAcceleratorTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpringCloudCustomizedAcceleratorConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.springCloudCustomizedAccelerator.SpringCloudCustomizedAcceleratorGitRepository",
    jsii_struct_bases=[],
    name_mapping={
        "url": "url",
        "basic_auth": "basicAuth",
        "branch": "branch",
        "ca_certificate_id": "caCertificateId",
        "commit": "commit",
        "git_tag": "gitTag",
        "interval_in_seconds": "intervalInSeconds",
        "path": "path",
        "ssh_auth": "sshAuth",
    },
)
class SpringCloudCustomizedAcceleratorGitRepository:
    def __init__(
        self,
        *,
        url: builtins.str,
        basic_auth: typing.Optional[typing.Union["SpringCloudCustomizedAcceleratorGitRepositoryBasicAuth", typing.Dict[builtins.str, typing.Any]]] = None,
        branch: typing.Optional[builtins.str] = None,
        ca_certificate_id: typing.Optional[builtins.str] = None,
        commit: typing.Optional[builtins.str] = None,
        git_tag: typing.Optional[builtins.str] = None,
        interval_in_seconds: typing.Optional[jsii.Number] = None,
        path: typing.Optional[builtins.str] = None,
        ssh_auth: typing.Optional[typing.Union["SpringCloudCustomizedAcceleratorGitRepositorySshAuth", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#url SpringCloudCustomizedAccelerator#url}.
        :param basic_auth: basic_auth block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#basic_auth SpringCloudCustomizedAccelerator#basic_auth}
        :param branch: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#branch SpringCloudCustomizedAccelerator#branch}.
        :param ca_certificate_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#ca_certificate_id SpringCloudCustomizedAccelerator#ca_certificate_id}.
        :param commit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#commit SpringCloudCustomizedAccelerator#commit}.
        :param git_tag: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#git_tag SpringCloudCustomizedAccelerator#git_tag}.
        :param interval_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#interval_in_seconds SpringCloudCustomizedAccelerator#interval_in_seconds}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#path SpringCloudCustomizedAccelerator#path}.
        :param ssh_auth: ssh_auth block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#ssh_auth SpringCloudCustomizedAccelerator#ssh_auth}
        '''
        if isinstance(basic_auth, dict):
            basic_auth = SpringCloudCustomizedAcceleratorGitRepositoryBasicAuth(**basic_auth)
        if isinstance(ssh_auth, dict):
            ssh_auth = SpringCloudCustomizedAcceleratorGitRepositorySshAuth(**ssh_auth)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4229e340dcfbabb84d48041b43629477b1cb0621d93d1a1b5968d47ffaf219d0)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument basic_auth", value=basic_auth, expected_type=type_hints["basic_auth"])
            check_type(argname="argument branch", value=branch, expected_type=type_hints["branch"])
            check_type(argname="argument ca_certificate_id", value=ca_certificate_id, expected_type=type_hints["ca_certificate_id"])
            check_type(argname="argument commit", value=commit, expected_type=type_hints["commit"])
            check_type(argname="argument git_tag", value=git_tag, expected_type=type_hints["git_tag"])
            check_type(argname="argument interval_in_seconds", value=interval_in_seconds, expected_type=type_hints["interval_in_seconds"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument ssh_auth", value=ssh_auth, expected_type=type_hints["ssh_auth"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "url": url,
        }
        if basic_auth is not None:
            self._values["basic_auth"] = basic_auth
        if branch is not None:
            self._values["branch"] = branch
        if ca_certificate_id is not None:
            self._values["ca_certificate_id"] = ca_certificate_id
        if commit is not None:
            self._values["commit"] = commit
        if git_tag is not None:
            self._values["git_tag"] = git_tag
        if interval_in_seconds is not None:
            self._values["interval_in_seconds"] = interval_in_seconds
        if path is not None:
            self._values["path"] = path
        if ssh_auth is not None:
            self._values["ssh_auth"] = ssh_auth

    @builtins.property
    def url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#url SpringCloudCustomizedAccelerator#url}.'''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def basic_auth(
        self,
    ) -> typing.Optional["SpringCloudCustomizedAcceleratorGitRepositoryBasicAuth"]:
        '''basic_auth block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#basic_auth SpringCloudCustomizedAccelerator#basic_auth}
        '''
        result = self._values.get("basic_auth")
        return typing.cast(typing.Optional["SpringCloudCustomizedAcceleratorGitRepositoryBasicAuth"], result)

    @builtins.property
    def branch(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#branch SpringCloudCustomizedAccelerator#branch}.'''
        result = self._values.get("branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ca_certificate_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#ca_certificate_id SpringCloudCustomizedAccelerator#ca_certificate_id}.'''
        result = self._values.get("ca_certificate_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def commit(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#commit SpringCloudCustomizedAccelerator#commit}.'''
        result = self._values.get("commit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def git_tag(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#git_tag SpringCloudCustomizedAccelerator#git_tag}.'''
        result = self._values.get("git_tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def interval_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#interval_in_seconds SpringCloudCustomizedAccelerator#interval_in_seconds}.'''
        result = self._values.get("interval_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#path SpringCloudCustomizedAccelerator#path}.'''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssh_auth(
        self,
    ) -> typing.Optional["SpringCloudCustomizedAcceleratorGitRepositorySshAuth"]:
        '''ssh_auth block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#ssh_auth SpringCloudCustomizedAccelerator#ssh_auth}
        '''
        result = self._values.get("ssh_auth")
        return typing.cast(typing.Optional["SpringCloudCustomizedAcceleratorGitRepositorySshAuth"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpringCloudCustomizedAcceleratorGitRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.springCloudCustomizedAccelerator.SpringCloudCustomizedAcceleratorGitRepositoryBasicAuth",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class SpringCloudCustomizedAcceleratorGitRepositoryBasicAuth:
    def __init__(self, *, password: builtins.str, username: builtins.str) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#password SpringCloudCustomizedAccelerator#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#username SpringCloudCustomizedAccelerator#username}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd13642170c27686f7b7c69e40b4298672df005d3f9e899ea5c5946225d449c5)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "password": password,
            "username": username,
        }

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#password SpringCloudCustomizedAccelerator#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#username SpringCloudCustomizedAccelerator#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpringCloudCustomizedAcceleratorGitRepositoryBasicAuth(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SpringCloudCustomizedAcceleratorGitRepositoryBasicAuthOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.springCloudCustomizedAccelerator.SpringCloudCustomizedAcceleratorGitRepositoryBasicAuthOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__590cd79ddb48fb8ed729b411808ef64cab3ff8d5b710d7d16b9b2954cf5aa4d6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97f52a5cde6880bbfec4ff40890a8b4a4d40722523f254e9a686a095827ad535)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e1bb88e3f266f180cad062d9737ce0ce44b87c87b930dfcb91500f4391103eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SpringCloudCustomizedAcceleratorGitRepositoryBasicAuth]:
        return typing.cast(typing.Optional[SpringCloudCustomizedAcceleratorGitRepositoryBasicAuth], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SpringCloudCustomizedAcceleratorGitRepositoryBasicAuth],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b93acadee365b5808cb55daf3af3fec81683a53f91cc825b98b934da5b4ae5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SpringCloudCustomizedAcceleratorGitRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.springCloudCustomizedAccelerator.SpringCloudCustomizedAcceleratorGitRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__52023ca390b94457eb781f2b3195e14cc478152f3e5d52146d1f4ca82a67fec9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBasicAuth")
    def put_basic_auth(self, *, password: builtins.str, username: builtins.str) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#password SpringCloudCustomizedAccelerator#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#username SpringCloudCustomizedAccelerator#username}.
        '''
        value = SpringCloudCustomizedAcceleratorGitRepositoryBasicAuth(
            password=password, username=username
        )

        return typing.cast(None, jsii.invoke(self, "putBasicAuth", [value]))

    @jsii.member(jsii_name="putSshAuth")
    def put_ssh_auth(
        self,
        *,
        private_key: builtins.str,
        host_key: typing.Optional[builtins.str] = None,
        host_key_algorithm: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param private_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#private_key SpringCloudCustomizedAccelerator#private_key}.
        :param host_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#host_key SpringCloudCustomizedAccelerator#host_key}.
        :param host_key_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#host_key_algorithm SpringCloudCustomizedAccelerator#host_key_algorithm}.
        '''
        value = SpringCloudCustomizedAcceleratorGitRepositorySshAuth(
            private_key=private_key,
            host_key=host_key,
            host_key_algorithm=host_key_algorithm,
        )

        return typing.cast(None, jsii.invoke(self, "putSshAuth", [value]))

    @jsii.member(jsii_name="resetBasicAuth")
    def reset_basic_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBasicAuth", []))

    @jsii.member(jsii_name="resetBranch")
    def reset_branch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBranch", []))

    @jsii.member(jsii_name="resetCaCertificateId")
    def reset_ca_certificate_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCaCertificateId", []))

    @jsii.member(jsii_name="resetCommit")
    def reset_commit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommit", []))

    @jsii.member(jsii_name="resetGitTag")
    def reset_git_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGitTag", []))

    @jsii.member(jsii_name="resetIntervalInSeconds")
    def reset_interval_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntervalInSeconds", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetSshAuth")
    def reset_ssh_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSshAuth", []))

    @builtins.property
    @jsii.member(jsii_name="basicAuth")
    def basic_auth(
        self,
    ) -> SpringCloudCustomizedAcceleratorGitRepositoryBasicAuthOutputReference:
        return typing.cast(SpringCloudCustomizedAcceleratorGitRepositoryBasicAuthOutputReference, jsii.get(self, "basicAuth"))

    @builtins.property
    @jsii.member(jsii_name="sshAuth")
    def ssh_auth(
        self,
    ) -> "SpringCloudCustomizedAcceleratorGitRepositorySshAuthOutputReference":
        return typing.cast("SpringCloudCustomizedAcceleratorGitRepositorySshAuthOutputReference", jsii.get(self, "sshAuth"))

    @builtins.property
    @jsii.member(jsii_name="basicAuthInput")
    def basic_auth_input(
        self,
    ) -> typing.Optional[SpringCloudCustomizedAcceleratorGitRepositoryBasicAuth]:
        return typing.cast(typing.Optional[SpringCloudCustomizedAcceleratorGitRepositoryBasicAuth], jsii.get(self, "basicAuthInput"))

    @builtins.property
    @jsii.member(jsii_name="branchInput")
    def branch_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "branchInput"))

    @builtins.property
    @jsii.member(jsii_name="caCertificateIdInput")
    def ca_certificate_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "caCertificateIdInput"))

    @builtins.property
    @jsii.member(jsii_name="commitInput")
    def commit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commitInput"))

    @builtins.property
    @jsii.member(jsii_name="gitTagInput")
    def git_tag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gitTagInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalInSecondsInput")
    def interval_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="sshAuthInput")
    def ssh_auth_input(
        self,
    ) -> typing.Optional["SpringCloudCustomizedAcceleratorGitRepositorySshAuth"]:
        return typing.cast(typing.Optional["SpringCloudCustomizedAcceleratorGitRepositorySshAuth"], jsii.get(self, "sshAuthInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="branch")
    def branch(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "branch"))

    @branch.setter
    def branch(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d8fc6083d62cc4b4c6a19f0e9eaa98242e31205719102e8956a2d60347b29dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "branch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="caCertificateId")
    def ca_certificate_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "caCertificateId"))

    @ca_certificate_id.setter
    def ca_certificate_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6ff7a8970b08c95e03ba2d528d4c2574536c22415d8be178dfe18abe0478d0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caCertificateId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="commit")
    def commit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commit"))

    @commit.setter
    def commit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c774eb7c4523d95413168abdeefc20295c9bde80a97c6733cfd1284a7e3784a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gitTag")
    def git_tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gitTag"))

    @git_tag.setter
    def git_tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f9464e6f3cf64f1805a4f226fef7cdf817149555cf2f336609241398ef2d1eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gitTag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="intervalInSeconds")
    def interval_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "intervalInSeconds"))

    @interval_in_seconds.setter
    def interval_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__739e9effd33fe904fb02dc6d8d3746c6bbbb77ad3dba1b6b33838120620c8a68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intervalInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cece457ed09f79940a6ff8b0eb104ec90902f67001d33f6f6e6e10c644ef623d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf9cd598039d3ef2297fcb235a95c026bc417fcb54fc9b184a475b4a1fad40e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SpringCloudCustomizedAcceleratorGitRepository]:
        return typing.cast(typing.Optional[SpringCloudCustomizedAcceleratorGitRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SpringCloudCustomizedAcceleratorGitRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f459068727dcf74ab0ac615ddcdf2a89f1257a2455472d7376e49923462577c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.springCloudCustomizedAccelerator.SpringCloudCustomizedAcceleratorGitRepositorySshAuth",
    jsii_struct_bases=[],
    name_mapping={
        "private_key": "privateKey",
        "host_key": "hostKey",
        "host_key_algorithm": "hostKeyAlgorithm",
    },
)
class SpringCloudCustomizedAcceleratorGitRepositorySshAuth:
    def __init__(
        self,
        *,
        private_key: builtins.str,
        host_key: typing.Optional[builtins.str] = None,
        host_key_algorithm: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param private_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#private_key SpringCloudCustomizedAccelerator#private_key}.
        :param host_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#host_key SpringCloudCustomizedAccelerator#host_key}.
        :param host_key_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#host_key_algorithm SpringCloudCustomizedAccelerator#host_key_algorithm}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1a1607b250a5eb076d7baf549af9f3dc29dae3f52c200cc3cee8c627cdd8edf)
            check_type(argname="argument private_key", value=private_key, expected_type=type_hints["private_key"])
            check_type(argname="argument host_key", value=host_key, expected_type=type_hints["host_key"])
            check_type(argname="argument host_key_algorithm", value=host_key_algorithm, expected_type=type_hints["host_key_algorithm"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "private_key": private_key,
        }
        if host_key is not None:
            self._values["host_key"] = host_key
        if host_key_algorithm is not None:
            self._values["host_key_algorithm"] = host_key_algorithm

    @builtins.property
    def private_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#private_key SpringCloudCustomizedAccelerator#private_key}.'''
        result = self._values.get("private_key")
        assert result is not None, "Required property 'private_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#host_key SpringCloudCustomizedAccelerator#host_key}.'''
        result = self._values.get("host_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def host_key_algorithm(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#host_key_algorithm SpringCloudCustomizedAccelerator#host_key_algorithm}.'''
        result = self._values.get("host_key_algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpringCloudCustomizedAcceleratorGitRepositorySshAuth(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SpringCloudCustomizedAcceleratorGitRepositorySshAuthOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.springCloudCustomizedAccelerator.SpringCloudCustomizedAcceleratorGitRepositorySshAuthOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ab645b1d87ad1a81b6b4510400a6a70f61bc70230358ff72627e64f8f867356)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHostKey")
    def reset_host_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostKey", []))

    @jsii.member(jsii_name="resetHostKeyAlgorithm")
    def reset_host_key_algorithm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostKeyAlgorithm", []))

    @builtins.property
    @jsii.member(jsii_name="hostKeyAlgorithmInput")
    def host_key_algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostKeyAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="hostKeyInput")
    def host_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="privateKeyInput")
    def private_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="hostKey")
    def host_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostKey"))

    @host_key.setter
    def host_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fcd4cd2df927c5abc38f753c6647c5c743666601f9c339e80859bb3f3c3557f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostKeyAlgorithm")
    def host_key_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostKeyAlgorithm"))

    @host_key_algorithm.setter
    def host_key_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__742a7c39a9d597b2fb8bfb0dd47856816d86ec9986332d367dd7b757fa4c8309)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostKeyAlgorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateKey")
    def private_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateKey"))

    @private_key.setter
    def private_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c16058e7e395c9f7e7e81df8bdfdad5d2ff1b5ac810c590b6ceb481dc2e5784f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SpringCloudCustomizedAcceleratorGitRepositorySshAuth]:
        return typing.cast(typing.Optional[SpringCloudCustomizedAcceleratorGitRepositorySshAuth], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SpringCloudCustomizedAcceleratorGitRepositorySshAuth],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fac9354d3fdd1a2481edfc7e287475447e73254cb462fec176e897583cc3fc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.springCloudCustomizedAccelerator.SpringCloudCustomizedAcceleratorTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class SpringCloudCustomizedAcceleratorTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#create SpringCloudCustomizedAccelerator#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#delete SpringCloudCustomizedAccelerator#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#read SpringCloudCustomizedAccelerator#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#update SpringCloudCustomizedAccelerator#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__434dc2442ed06baac8f43637b4a007d5a367f90585c62ce0966c431532bd09cd)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#create SpringCloudCustomizedAccelerator#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#delete SpringCloudCustomizedAccelerator#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#read SpringCloudCustomizedAccelerator#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_customized_accelerator#update SpringCloudCustomizedAccelerator#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpringCloudCustomizedAcceleratorTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SpringCloudCustomizedAcceleratorTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.springCloudCustomizedAccelerator.SpringCloudCustomizedAcceleratorTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__73e53d170daa2c62b9b5c58da31148e159e758ee4fc0b5585866e67bc21442b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a984db6c1d849b478668c94cb89af0d7825e2bccd398381417087a64d94b37a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d88791ff8d7757a814de002bfb27944bb5587a603dbe181fc12b09cff6a813d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a539c54a8e719cd58d408483b1a05a47f3839ba76adaf5da9b3686f3630ff0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ac753801c4e12c81f0793eb458f47619865e1119733bd7cb95d3a0d92ac44ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SpringCloudCustomizedAcceleratorTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SpringCloudCustomizedAcceleratorTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SpringCloudCustomizedAcceleratorTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57292ff259691506f3c3d934fc8cbc057afb28141d76634cb9c15ab7f13817ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SpringCloudCustomizedAccelerator",
    "SpringCloudCustomizedAcceleratorConfig",
    "SpringCloudCustomizedAcceleratorGitRepository",
    "SpringCloudCustomizedAcceleratorGitRepositoryBasicAuth",
    "SpringCloudCustomizedAcceleratorGitRepositoryBasicAuthOutputReference",
    "SpringCloudCustomizedAcceleratorGitRepositoryOutputReference",
    "SpringCloudCustomizedAcceleratorGitRepositorySshAuth",
    "SpringCloudCustomizedAcceleratorGitRepositorySshAuthOutputReference",
    "SpringCloudCustomizedAcceleratorTimeouts",
    "SpringCloudCustomizedAcceleratorTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__721b699bbc6f71618f3551292c52c336a94e6cf63ede51076de1666b11683eab(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    git_repository: typing.Union[SpringCloudCustomizedAcceleratorGitRepository, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    spring_cloud_accelerator_id: builtins.str,
    accelerator_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    accelerator_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    icon_url: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[SpringCloudCustomizedAcceleratorTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__38c3951daeb41ef9db522505605439f1a15bf4516ecd711db79e51710da953e4(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72e4975032c86a1d30050ab5584a681ef4e9f55d0d250f2601e6f73cd0d8c1a3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d94911f14246923bd82514a47e0fd388ede2904a7c37ac62344530804f257ff1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__881f59f8118f3048369ac90e2a2d634d296ecab6d97fdb6d0dc1d33cb51239ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fa0aed4bb563e3543099e3f1e48dbce06abcc683ebc348905dca0684001f5a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77303490445e4b96123b9b3e82dc057dabade5e959baba96c7873871267cf153(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a173ae8595bad5b9c815095148176ed49af29b12e4c66e8eaccf987e99b64fa5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c08146f15cc44c2df0e1c18ebc09b9440c18f2cc213d10f29cb8cf6e5e9bc208(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e12e5188560e5f8a33afc9633766246a9f2e88fb49cad547f46a6f5dc0bfaf9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bd7b86cdea3d49e6ad884690b5fd977c78ed7dd69344ff2123d8ff4de05ef47(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    git_repository: typing.Union[SpringCloudCustomizedAcceleratorGitRepository, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    spring_cloud_accelerator_id: builtins.str,
    accelerator_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    accelerator_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    icon_url: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[SpringCloudCustomizedAcceleratorTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4229e340dcfbabb84d48041b43629477b1cb0621d93d1a1b5968d47ffaf219d0(
    *,
    url: builtins.str,
    basic_auth: typing.Optional[typing.Union[SpringCloudCustomizedAcceleratorGitRepositoryBasicAuth, typing.Dict[builtins.str, typing.Any]]] = None,
    branch: typing.Optional[builtins.str] = None,
    ca_certificate_id: typing.Optional[builtins.str] = None,
    commit: typing.Optional[builtins.str] = None,
    git_tag: typing.Optional[builtins.str] = None,
    interval_in_seconds: typing.Optional[jsii.Number] = None,
    path: typing.Optional[builtins.str] = None,
    ssh_auth: typing.Optional[typing.Union[SpringCloudCustomizedAcceleratorGitRepositorySshAuth, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd13642170c27686f7b7c69e40b4298672df005d3f9e899ea5c5946225d449c5(
    *,
    password: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__590cd79ddb48fb8ed729b411808ef64cab3ff8d5b710d7d16b9b2954cf5aa4d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97f52a5cde6880bbfec4ff40890a8b4a4d40722523f254e9a686a095827ad535(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e1bb88e3f266f180cad062d9737ce0ce44b87c87b930dfcb91500f4391103eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b93acadee365b5808cb55daf3af3fec81683a53f91cc825b98b934da5b4ae5c(
    value: typing.Optional[SpringCloudCustomizedAcceleratorGitRepositoryBasicAuth],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52023ca390b94457eb781f2b3195e14cc478152f3e5d52146d1f4ca82a67fec9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d8fc6083d62cc4b4c6a19f0e9eaa98242e31205719102e8956a2d60347b29dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6ff7a8970b08c95e03ba2d528d4c2574536c22415d8be178dfe18abe0478d0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c774eb7c4523d95413168abdeefc20295c9bde80a97c6733cfd1284a7e3784a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f9464e6f3cf64f1805a4f226fef7cdf817149555cf2f336609241398ef2d1eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__739e9effd33fe904fb02dc6d8d3746c6bbbb77ad3dba1b6b33838120620c8a68(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cece457ed09f79940a6ff8b0eb104ec90902f67001d33f6f6e6e10c644ef623d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf9cd598039d3ef2297fcb235a95c026bc417fcb54fc9b184a475b4a1fad40e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f459068727dcf74ab0ac615ddcdf2a89f1257a2455472d7376e49923462577c2(
    value: typing.Optional[SpringCloudCustomizedAcceleratorGitRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1a1607b250a5eb076d7baf549af9f3dc29dae3f52c200cc3cee8c627cdd8edf(
    *,
    private_key: builtins.str,
    host_key: typing.Optional[builtins.str] = None,
    host_key_algorithm: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ab645b1d87ad1a81b6b4510400a6a70f61bc70230358ff72627e64f8f867356(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fcd4cd2df927c5abc38f753c6647c5c743666601f9c339e80859bb3f3c3557f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__742a7c39a9d597b2fb8bfb0dd47856816d86ec9986332d367dd7b757fa4c8309(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c16058e7e395c9f7e7e81df8bdfdad5d2ff1b5ac810c590b6ceb481dc2e5784f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fac9354d3fdd1a2481edfc7e287475447e73254cb462fec176e897583cc3fc2(
    value: typing.Optional[SpringCloudCustomizedAcceleratorGitRepositorySshAuth],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__434dc2442ed06baac8f43637b4a007d5a367f90585c62ce0966c431532bd09cd(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73e53d170daa2c62b9b5c58da31148e159e758ee4fc0b5585866e67bc21442b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a984db6c1d849b478668c94cb89af0d7825e2bccd398381417087a64d94b37a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d88791ff8d7757a814de002bfb27944bb5587a603dbe181fc12b09cff6a813d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a539c54a8e719cd58d408483b1a05a47f3839ba76adaf5da9b3686f3630ff0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ac753801c4e12c81f0793eb458f47619865e1119733bd7cb95d3a0d92ac44ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57292ff259691506f3c3d934fc8cbc057afb28141d76634cb9c15ab7f13817ff(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SpringCloudCustomizedAcceleratorTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
