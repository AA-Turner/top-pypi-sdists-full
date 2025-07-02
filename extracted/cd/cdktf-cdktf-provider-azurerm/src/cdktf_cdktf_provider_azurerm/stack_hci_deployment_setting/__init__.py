r'''
# `azurerm_stack_hci_deployment_setting`

Refer to the Terraform Registry for docs: [`azurerm_stack_hci_deployment_setting`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting).
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


class StackHciDeploymentSetting(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.stackHciDeploymentSetting.StackHciDeploymentSetting",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting azurerm_stack_hci_deployment_setting}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        arc_resource_ids: typing.Sequence[builtins.str],
        scale_unit: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["StackHciDeploymentSettingScaleUnit", typing.Dict[builtins.str, typing.Any]]]],
        stack_hci_cluster_id: builtins.str,
        version: builtins.str,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["StackHciDeploymentSettingTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting azurerm_stack_hci_deployment_setting} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param arc_resource_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#arc_resource_ids StackHciDeploymentSetting#arc_resource_ids}.
        :param scale_unit: scale_unit block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#scale_unit StackHciDeploymentSetting#scale_unit}
        :param stack_hci_cluster_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#stack_hci_cluster_id StackHciDeploymentSetting#stack_hci_cluster_id}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#version StackHciDeploymentSetting#version}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#id StackHciDeploymentSetting#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#timeouts StackHciDeploymentSetting#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bda13f15368304cfc1ec40ba110edf0213facc845478e273e35bd3d8a476d8c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = StackHciDeploymentSettingConfig(
            arc_resource_ids=arc_resource_ids,
            scale_unit=scale_unit,
            stack_hci_cluster_id=stack_hci_cluster_id,
            version=version,
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
        '''Generates CDKTF code for importing a StackHciDeploymentSetting resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the StackHciDeploymentSetting to import.
        :param import_from_id: The id of the existing StackHciDeploymentSetting that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the StackHciDeploymentSetting to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93074f80ac18130f8a4e941e67bbc04ad5f738054a7b75b7634d63d9ed067e5f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putScaleUnit")
    def put_scale_unit(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["StackHciDeploymentSettingScaleUnit", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5cb11028dcdd68f6ce02aa2712ef3b461debcb56a7f55323fc409f202efb245)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putScaleUnit", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#create StackHciDeploymentSetting#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#delete StackHciDeploymentSetting#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#read StackHciDeploymentSetting#read}.
        '''
        value = StackHciDeploymentSettingTimeouts(
            create=create, delete=delete, read=read
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

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
    @jsii.member(jsii_name="scaleUnit")
    def scale_unit(self) -> "StackHciDeploymentSettingScaleUnitList":
        return typing.cast("StackHciDeploymentSettingScaleUnitList", jsii.get(self, "scaleUnit"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "StackHciDeploymentSettingTimeoutsOutputReference":
        return typing.cast("StackHciDeploymentSettingTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="arcResourceIdsInput")
    def arc_resource_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "arcResourceIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleUnitInput")
    def scale_unit_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StackHciDeploymentSettingScaleUnit"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StackHciDeploymentSettingScaleUnit"]]], jsii.get(self, "scaleUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="stackHciClusterIdInput")
    def stack_hci_cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stackHciClusterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "StackHciDeploymentSettingTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "StackHciDeploymentSettingTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="arcResourceIds")
    def arc_resource_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "arcResourceIds"))

    @arc_resource_ids.setter
    def arc_resource_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__290298f24114f8352fda965a19094cfbf567c6f7cc6c9ec85630d407f30f6fd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "arcResourceIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eeed5f338b740c9f9960c94c09038d80ebc54bbf2b58353b1d8e9f89d74001f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stackHciClusterId")
    def stack_hci_cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stackHciClusterId"))

    @stack_hci_cluster_id.setter
    def stack_hci_cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b91d7cdd987d8054bc5bddbc6f6db4cb21442fcae31fa9bf0e3b25c19019956d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stackHciClusterId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77bc36cb8f63c1871bd883ab138a36f9629ac8d6f3e68a59ba7d42e42d7cb905)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.stackHciDeploymentSetting.StackHciDeploymentSettingConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "arc_resource_ids": "arcResourceIds",
        "scale_unit": "scaleUnit",
        "stack_hci_cluster_id": "stackHciClusterId",
        "version": "version",
        "id": "id",
        "timeouts": "timeouts",
    },
)
class StackHciDeploymentSettingConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        arc_resource_ids: typing.Sequence[builtins.str],
        scale_unit: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["StackHciDeploymentSettingScaleUnit", typing.Dict[builtins.str, typing.Any]]]],
        stack_hci_cluster_id: builtins.str,
        version: builtins.str,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["StackHciDeploymentSettingTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param arc_resource_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#arc_resource_ids StackHciDeploymentSetting#arc_resource_ids}.
        :param scale_unit: scale_unit block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#scale_unit StackHciDeploymentSetting#scale_unit}
        :param stack_hci_cluster_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#stack_hci_cluster_id StackHciDeploymentSetting#stack_hci_cluster_id}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#version StackHciDeploymentSetting#version}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#id StackHciDeploymentSetting#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#timeouts StackHciDeploymentSetting#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = StackHciDeploymentSettingTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8e0ff3a4dca8b3481b393ecf29d994e8a03949e433bc6640410dcbd99d8e1c5)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument arc_resource_ids", value=arc_resource_ids, expected_type=type_hints["arc_resource_ids"])
            check_type(argname="argument scale_unit", value=scale_unit, expected_type=type_hints["scale_unit"])
            check_type(argname="argument stack_hci_cluster_id", value=stack_hci_cluster_id, expected_type=type_hints["stack_hci_cluster_id"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "arc_resource_ids": arc_resource_ids,
            "scale_unit": scale_unit,
            "stack_hci_cluster_id": stack_hci_cluster_id,
            "version": version,
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
    def arc_resource_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#arc_resource_ids StackHciDeploymentSetting#arc_resource_ids}.'''
        result = self._values.get("arc_resource_ids")
        assert result is not None, "Required property 'arc_resource_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def scale_unit(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StackHciDeploymentSettingScaleUnit"]]:
        '''scale_unit block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#scale_unit StackHciDeploymentSetting#scale_unit}
        '''
        result = self._values.get("scale_unit")
        assert result is not None, "Required property 'scale_unit' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StackHciDeploymentSettingScaleUnit"]], result)

    @builtins.property
    def stack_hci_cluster_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#stack_hci_cluster_id StackHciDeploymentSetting#stack_hci_cluster_id}.'''
        result = self._values.get("stack_hci_cluster_id")
        assert result is not None, "Required property 'stack_hci_cluster_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#version StackHciDeploymentSetting#version}.'''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#id StackHciDeploymentSetting#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["StackHciDeploymentSettingTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#timeouts StackHciDeploymentSetting#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["StackHciDeploymentSettingTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StackHciDeploymentSettingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.stackHciDeploymentSetting.StackHciDeploymentSettingScaleUnit",
    jsii_struct_bases=[],
    name_mapping={
        "active_directory_organizational_unit_path": "activeDirectoryOrganizationalUnitPath",
        "cluster": "cluster",
        "domain_fqdn": "domainFqdn",
        "host_network": "hostNetwork",
        "infrastructure_network": "infrastructureNetwork",
        "name_prefix": "namePrefix",
        "optional_service": "optionalService",
        "physical_node": "physicalNode",
        "secrets_location": "secretsLocation",
        "storage": "storage",
        "bitlocker_boot_volume_enabled": "bitlockerBootVolumeEnabled",
        "bitlocker_data_volume_enabled": "bitlockerDataVolumeEnabled",
        "credential_guard_enabled": "credentialGuardEnabled",
        "drift_control_enabled": "driftControlEnabled",
        "drtm_protection_enabled": "drtmProtectionEnabled",
        "episodic_data_upload_enabled": "episodicDataUploadEnabled",
        "eu_location_enabled": "euLocationEnabled",
        "hvci_protection_enabled": "hvciProtectionEnabled",
        "side_channel_mitigation_enabled": "sideChannelMitigationEnabled",
        "smb_cluster_encryption_enabled": "smbClusterEncryptionEnabled",
        "smb_signing_enabled": "smbSigningEnabled",
        "streaming_data_client_enabled": "streamingDataClientEnabled",
        "wdac_enabled": "wdacEnabled",
    },
)
class StackHciDeploymentSettingScaleUnit:
    def __init__(
        self,
        *,
        active_directory_organizational_unit_path: builtins.str,
        cluster: typing.Union["StackHciDeploymentSettingScaleUnitCluster", typing.Dict[builtins.str, typing.Any]],
        domain_fqdn: builtins.str,
        host_network: typing.Union["StackHciDeploymentSettingScaleUnitHostNetwork", typing.Dict[builtins.str, typing.Any]],
        infrastructure_network: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["StackHciDeploymentSettingScaleUnitInfrastructureNetwork", typing.Dict[builtins.str, typing.Any]]]],
        name_prefix: builtins.str,
        optional_service: typing.Union["StackHciDeploymentSettingScaleUnitOptionalService", typing.Dict[builtins.str, typing.Any]],
        physical_node: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["StackHciDeploymentSettingScaleUnitPhysicalNode", typing.Dict[builtins.str, typing.Any]]]],
        secrets_location: builtins.str,
        storage: typing.Union["StackHciDeploymentSettingScaleUnitStorage", typing.Dict[builtins.str, typing.Any]],
        bitlocker_boot_volume_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        bitlocker_data_volume_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        credential_guard_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        drift_control_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        drtm_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        episodic_data_upload_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        eu_location_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hvci_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        side_channel_mitigation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        smb_cluster_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        smb_signing_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        streaming_data_client_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        wdac_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param active_directory_organizational_unit_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#active_directory_organizational_unit_path StackHciDeploymentSetting#active_directory_organizational_unit_path}.
        :param cluster: cluster block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#cluster StackHciDeploymentSetting#cluster}
        :param domain_fqdn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#domain_fqdn StackHciDeploymentSetting#domain_fqdn}.
        :param host_network: host_network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#host_network StackHciDeploymentSetting#host_network}
        :param infrastructure_network: infrastructure_network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#infrastructure_network StackHciDeploymentSetting#infrastructure_network}
        :param name_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#name_prefix StackHciDeploymentSetting#name_prefix}.
        :param optional_service: optional_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#optional_service StackHciDeploymentSetting#optional_service}
        :param physical_node: physical_node block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#physical_node StackHciDeploymentSetting#physical_node}
        :param secrets_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#secrets_location StackHciDeploymentSetting#secrets_location}.
        :param storage: storage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#storage StackHciDeploymentSetting#storage}
        :param bitlocker_boot_volume_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#bitlocker_boot_volume_enabled StackHciDeploymentSetting#bitlocker_boot_volume_enabled}.
        :param bitlocker_data_volume_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#bitlocker_data_volume_enabled StackHciDeploymentSetting#bitlocker_data_volume_enabled}.
        :param credential_guard_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#credential_guard_enabled StackHciDeploymentSetting#credential_guard_enabled}.
        :param drift_control_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#drift_control_enabled StackHciDeploymentSetting#drift_control_enabled}.
        :param drtm_protection_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#drtm_protection_enabled StackHciDeploymentSetting#drtm_protection_enabled}.
        :param episodic_data_upload_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#episodic_data_upload_enabled StackHciDeploymentSetting#episodic_data_upload_enabled}.
        :param eu_location_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#eu_location_enabled StackHciDeploymentSetting#eu_location_enabled}.
        :param hvci_protection_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#hvci_protection_enabled StackHciDeploymentSetting#hvci_protection_enabled}.
        :param side_channel_mitigation_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#side_channel_mitigation_enabled StackHciDeploymentSetting#side_channel_mitigation_enabled}.
        :param smb_cluster_encryption_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#smb_cluster_encryption_enabled StackHciDeploymentSetting#smb_cluster_encryption_enabled}.
        :param smb_signing_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#smb_signing_enabled StackHciDeploymentSetting#smb_signing_enabled}.
        :param streaming_data_client_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#streaming_data_client_enabled StackHciDeploymentSetting#streaming_data_client_enabled}.
        :param wdac_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#wdac_enabled StackHciDeploymentSetting#wdac_enabled}.
        '''
        if isinstance(cluster, dict):
            cluster = StackHciDeploymentSettingScaleUnitCluster(**cluster)
        if isinstance(host_network, dict):
            host_network = StackHciDeploymentSettingScaleUnitHostNetwork(**host_network)
        if isinstance(optional_service, dict):
            optional_service = StackHciDeploymentSettingScaleUnitOptionalService(**optional_service)
        if isinstance(storage, dict):
            storage = StackHciDeploymentSettingScaleUnitStorage(**storage)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa88e9c8da993f3f649ecdb496c64fe4aca298df4e82aade26572601549b976b)
            check_type(argname="argument active_directory_organizational_unit_path", value=active_directory_organizational_unit_path, expected_type=type_hints["active_directory_organizational_unit_path"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument domain_fqdn", value=domain_fqdn, expected_type=type_hints["domain_fqdn"])
            check_type(argname="argument host_network", value=host_network, expected_type=type_hints["host_network"])
            check_type(argname="argument infrastructure_network", value=infrastructure_network, expected_type=type_hints["infrastructure_network"])
            check_type(argname="argument name_prefix", value=name_prefix, expected_type=type_hints["name_prefix"])
            check_type(argname="argument optional_service", value=optional_service, expected_type=type_hints["optional_service"])
            check_type(argname="argument physical_node", value=physical_node, expected_type=type_hints["physical_node"])
            check_type(argname="argument secrets_location", value=secrets_location, expected_type=type_hints["secrets_location"])
            check_type(argname="argument storage", value=storage, expected_type=type_hints["storage"])
            check_type(argname="argument bitlocker_boot_volume_enabled", value=bitlocker_boot_volume_enabled, expected_type=type_hints["bitlocker_boot_volume_enabled"])
            check_type(argname="argument bitlocker_data_volume_enabled", value=bitlocker_data_volume_enabled, expected_type=type_hints["bitlocker_data_volume_enabled"])
            check_type(argname="argument credential_guard_enabled", value=credential_guard_enabled, expected_type=type_hints["credential_guard_enabled"])
            check_type(argname="argument drift_control_enabled", value=drift_control_enabled, expected_type=type_hints["drift_control_enabled"])
            check_type(argname="argument drtm_protection_enabled", value=drtm_protection_enabled, expected_type=type_hints["drtm_protection_enabled"])
            check_type(argname="argument episodic_data_upload_enabled", value=episodic_data_upload_enabled, expected_type=type_hints["episodic_data_upload_enabled"])
            check_type(argname="argument eu_location_enabled", value=eu_location_enabled, expected_type=type_hints["eu_location_enabled"])
            check_type(argname="argument hvci_protection_enabled", value=hvci_protection_enabled, expected_type=type_hints["hvci_protection_enabled"])
            check_type(argname="argument side_channel_mitigation_enabled", value=side_channel_mitigation_enabled, expected_type=type_hints["side_channel_mitigation_enabled"])
            check_type(argname="argument smb_cluster_encryption_enabled", value=smb_cluster_encryption_enabled, expected_type=type_hints["smb_cluster_encryption_enabled"])
            check_type(argname="argument smb_signing_enabled", value=smb_signing_enabled, expected_type=type_hints["smb_signing_enabled"])
            check_type(argname="argument streaming_data_client_enabled", value=streaming_data_client_enabled, expected_type=type_hints["streaming_data_client_enabled"])
            check_type(argname="argument wdac_enabled", value=wdac_enabled, expected_type=type_hints["wdac_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "active_directory_organizational_unit_path": active_directory_organizational_unit_path,
            "cluster": cluster,
            "domain_fqdn": domain_fqdn,
            "host_network": host_network,
            "infrastructure_network": infrastructure_network,
            "name_prefix": name_prefix,
            "optional_service": optional_service,
            "physical_node": physical_node,
            "secrets_location": secrets_location,
            "storage": storage,
        }
        if bitlocker_boot_volume_enabled is not None:
            self._values["bitlocker_boot_volume_enabled"] = bitlocker_boot_volume_enabled
        if bitlocker_data_volume_enabled is not None:
            self._values["bitlocker_data_volume_enabled"] = bitlocker_data_volume_enabled
        if credential_guard_enabled is not None:
            self._values["credential_guard_enabled"] = credential_guard_enabled
        if drift_control_enabled is not None:
            self._values["drift_control_enabled"] = drift_control_enabled
        if drtm_protection_enabled is not None:
            self._values["drtm_protection_enabled"] = drtm_protection_enabled
        if episodic_data_upload_enabled is not None:
            self._values["episodic_data_upload_enabled"] = episodic_data_upload_enabled
        if eu_location_enabled is not None:
            self._values["eu_location_enabled"] = eu_location_enabled
        if hvci_protection_enabled is not None:
            self._values["hvci_protection_enabled"] = hvci_protection_enabled
        if side_channel_mitigation_enabled is not None:
            self._values["side_channel_mitigation_enabled"] = side_channel_mitigation_enabled
        if smb_cluster_encryption_enabled is not None:
            self._values["smb_cluster_encryption_enabled"] = smb_cluster_encryption_enabled
        if smb_signing_enabled is not None:
            self._values["smb_signing_enabled"] = smb_signing_enabled
        if streaming_data_client_enabled is not None:
            self._values["streaming_data_client_enabled"] = streaming_data_client_enabled
        if wdac_enabled is not None:
            self._values["wdac_enabled"] = wdac_enabled

    @builtins.property
    def active_directory_organizational_unit_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#active_directory_organizational_unit_path StackHciDeploymentSetting#active_directory_organizational_unit_path}.'''
        result = self._values.get("active_directory_organizational_unit_path")
        assert result is not None, "Required property 'active_directory_organizational_unit_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cluster(self) -> "StackHciDeploymentSettingScaleUnitCluster":
        '''cluster block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#cluster StackHciDeploymentSetting#cluster}
        '''
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast("StackHciDeploymentSettingScaleUnitCluster", result)

    @builtins.property
    def domain_fqdn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#domain_fqdn StackHciDeploymentSetting#domain_fqdn}.'''
        result = self._values.get("domain_fqdn")
        assert result is not None, "Required property 'domain_fqdn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host_network(self) -> "StackHciDeploymentSettingScaleUnitHostNetwork":
        '''host_network block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#host_network StackHciDeploymentSetting#host_network}
        '''
        result = self._values.get("host_network")
        assert result is not None, "Required property 'host_network' is missing"
        return typing.cast("StackHciDeploymentSettingScaleUnitHostNetwork", result)

    @builtins.property
    def infrastructure_network(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StackHciDeploymentSettingScaleUnitInfrastructureNetwork"]]:
        '''infrastructure_network block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#infrastructure_network StackHciDeploymentSetting#infrastructure_network}
        '''
        result = self._values.get("infrastructure_network")
        assert result is not None, "Required property 'infrastructure_network' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StackHciDeploymentSettingScaleUnitInfrastructureNetwork"]], result)

    @builtins.property
    def name_prefix(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#name_prefix StackHciDeploymentSetting#name_prefix}.'''
        result = self._values.get("name_prefix")
        assert result is not None, "Required property 'name_prefix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def optional_service(self) -> "StackHciDeploymentSettingScaleUnitOptionalService":
        '''optional_service block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#optional_service StackHciDeploymentSetting#optional_service}
        '''
        result = self._values.get("optional_service")
        assert result is not None, "Required property 'optional_service' is missing"
        return typing.cast("StackHciDeploymentSettingScaleUnitOptionalService", result)

    @builtins.property
    def physical_node(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StackHciDeploymentSettingScaleUnitPhysicalNode"]]:
        '''physical_node block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#physical_node StackHciDeploymentSetting#physical_node}
        '''
        result = self._values.get("physical_node")
        assert result is not None, "Required property 'physical_node' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StackHciDeploymentSettingScaleUnitPhysicalNode"]], result)

    @builtins.property
    def secrets_location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#secrets_location StackHciDeploymentSetting#secrets_location}.'''
        result = self._values.get("secrets_location")
        assert result is not None, "Required property 'secrets_location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage(self) -> "StackHciDeploymentSettingScaleUnitStorage":
        '''storage block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#storage StackHciDeploymentSetting#storage}
        '''
        result = self._values.get("storage")
        assert result is not None, "Required property 'storage' is missing"
        return typing.cast("StackHciDeploymentSettingScaleUnitStorage", result)

    @builtins.property
    def bitlocker_boot_volume_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#bitlocker_boot_volume_enabled StackHciDeploymentSetting#bitlocker_boot_volume_enabled}.'''
        result = self._values.get("bitlocker_boot_volume_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def bitlocker_data_volume_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#bitlocker_data_volume_enabled StackHciDeploymentSetting#bitlocker_data_volume_enabled}.'''
        result = self._values.get("bitlocker_data_volume_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def credential_guard_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#credential_guard_enabled StackHciDeploymentSetting#credential_guard_enabled}.'''
        result = self._values.get("credential_guard_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def drift_control_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#drift_control_enabled StackHciDeploymentSetting#drift_control_enabled}.'''
        result = self._values.get("drift_control_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def drtm_protection_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#drtm_protection_enabled StackHciDeploymentSetting#drtm_protection_enabled}.'''
        result = self._values.get("drtm_protection_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def episodic_data_upload_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#episodic_data_upload_enabled StackHciDeploymentSetting#episodic_data_upload_enabled}.'''
        result = self._values.get("episodic_data_upload_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def eu_location_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#eu_location_enabled StackHciDeploymentSetting#eu_location_enabled}.'''
        result = self._values.get("eu_location_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def hvci_protection_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#hvci_protection_enabled StackHciDeploymentSetting#hvci_protection_enabled}.'''
        result = self._values.get("hvci_protection_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def side_channel_mitigation_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#side_channel_mitigation_enabled StackHciDeploymentSetting#side_channel_mitigation_enabled}.'''
        result = self._values.get("side_channel_mitigation_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def smb_cluster_encryption_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#smb_cluster_encryption_enabled StackHciDeploymentSetting#smb_cluster_encryption_enabled}.'''
        result = self._values.get("smb_cluster_encryption_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def smb_signing_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#smb_signing_enabled StackHciDeploymentSetting#smb_signing_enabled}.'''
        result = self._values.get("smb_signing_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def streaming_data_client_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#streaming_data_client_enabled StackHciDeploymentSetting#streaming_data_client_enabled}.'''
        result = self._values.get("streaming_data_client_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def wdac_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#wdac_enabled StackHciDeploymentSetting#wdac_enabled}.'''
        result = self._values.get("wdac_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StackHciDeploymentSettingScaleUnit(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.stackHciDeploymentSetting.StackHciDeploymentSettingScaleUnitCluster",
    jsii_struct_bases=[],
    name_mapping={
        "azure_service_endpoint": "azureServiceEndpoint",
        "cloud_account_name": "cloudAccountName",
        "name": "name",
        "witness_path": "witnessPath",
        "witness_type": "witnessType",
    },
)
class StackHciDeploymentSettingScaleUnitCluster:
    def __init__(
        self,
        *,
        azure_service_endpoint: builtins.str,
        cloud_account_name: builtins.str,
        name: builtins.str,
        witness_path: builtins.str,
        witness_type: builtins.str,
    ) -> None:
        '''
        :param azure_service_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#azure_service_endpoint StackHciDeploymentSetting#azure_service_endpoint}.
        :param cloud_account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#cloud_account_name StackHciDeploymentSetting#cloud_account_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#name StackHciDeploymentSetting#name}.
        :param witness_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#witness_path StackHciDeploymentSetting#witness_path}.
        :param witness_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#witness_type StackHciDeploymentSetting#witness_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5981d76b1d4543edeb2371fc6b301d293099ae1c2067e11a415e948b7e8af897)
            check_type(argname="argument azure_service_endpoint", value=azure_service_endpoint, expected_type=type_hints["azure_service_endpoint"])
            check_type(argname="argument cloud_account_name", value=cloud_account_name, expected_type=type_hints["cloud_account_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument witness_path", value=witness_path, expected_type=type_hints["witness_path"])
            check_type(argname="argument witness_type", value=witness_type, expected_type=type_hints["witness_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "azure_service_endpoint": azure_service_endpoint,
            "cloud_account_name": cloud_account_name,
            "name": name,
            "witness_path": witness_path,
            "witness_type": witness_type,
        }

    @builtins.property
    def azure_service_endpoint(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#azure_service_endpoint StackHciDeploymentSetting#azure_service_endpoint}.'''
        result = self._values.get("azure_service_endpoint")
        assert result is not None, "Required property 'azure_service_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cloud_account_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#cloud_account_name StackHciDeploymentSetting#cloud_account_name}.'''
        result = self._values.get("cloud_account_name")
        assert result is not None, "Required property 'cloud_account_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#name StackHciDeploymentSetting#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def witness_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#witness_path StackHciDeploymentSetting#witness_path}.'''
        result = self._values.get("witness_path")
        assert result is not None, "Required property 'witness_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def witness_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#witness_type StackHciDeploymentSetting#witness_type}.'''
        result = self._values.get("witness_type")
        assert result is not None, "Required property 'witness_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StackHciDeploymentSettingScaleUnitCluster(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StackHciDeploymentSettingScaleUnitClusterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.stackHciDeploymentSetting.StackHciDeploymentSettingScaleUnitClusterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__022da8a5881bb52c8970d612ba9367fdaed82f12c4cd41c39905e2aca9c421d6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="azureServiceEndpointInput")
    def azure_service_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "azureServiceEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudAccountNameInput")
    def cloud_account_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudAccountNameInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="witnessPathInput")
    def witness_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "witnessPathInput"))

    @builtins.property
    @jsii.member(jsii_name="witnessTypeInput")
    def witness_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "witnessTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="azureServiceEndpoint")
    def azure_service_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "azureServiceEndpoint"))

    @azure_service_endpoint.setter
    def azure_service_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d025b201c66bcdeaa554369149abe4f07ee763a460440183fae2fdb12c64aa5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "azureServiceEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudAccountName")
    def cloud_account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudAccountName"))

    @cloud_account_name.setter
    def cloud_account_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beea3fc2fc2acaf52359fe5767f33305a36f52939ca65ab5fa42ad76a236c80c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudAccountName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0049547cdd24a9ae8db7dc28ae35cb56e02b0bd277b3c740b35fa026f822e451)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="witnessPath")
    def witness_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "witnessPath"))

    @witness_path.setter
    def witness_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33450096beee92da7ecb97f3579c5d4a83ef42e326fd7da66080c363b42f1e61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "witnessPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="witnessType")
    def witness_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "witnessType"))

    @witness_type.setter
    def witness_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99e2f98cc66e7c074e02bf2ebe157b8de3011e4c4118d4e9d3d5b3a336d20218)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "witnessType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StackHciDeploymentSettingScaleUnitCluster]:
        return typing.cast(typing.Optional[StackHciDeploymentSettingScaleUnitCluster], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StackHciDeploymentSettingScaleUnitCluster],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcf02ac1bb0e1ddea9249fddd4d93f382bbab03a036dc7fb74850d02cc7a00ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.stackHciDeploymentSetting.StackHciDeploymentSettingScaleUnitHostNetwork",
    jsii_struct_bases=[],
    name_mapping={
        "intent": "intent",
        "storage_network": "storageNetwork",
        "storage_auto_ip_enabled": "storageAutoIpEnabled",
        "storage_connectivity_switchless_enabled": "storageConnectivitySwitchlessEnabled",
    },
)
class StackHciDeploymentSettingScaleUnitHostNetwork:
    def __init__(
        self,
        *,
        intent: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["StackHciDeploymentSettingScaleUnitHostNetworkIntent", typing.Dict[builtins.str, typing.Any]]]],
        storage_network: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["StackHciDeploymentSettingScaleUnitHostNetworkStorageNetwork", typing.Dict[builtins.str, typing.Any]]]],
        storage_auto_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        storage_connectivity_switchless_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param intent: intent block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#intent StackHciDeploymentSetting#intent}
        :param storage_network: storage_network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#storage_network StackHciDeploymentSetting#storage_network}
        :param storage_auto_ip_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#storage_auto_ip_enabled StackHciDeploymentSetting#storage_auto_ip_enabled}.
        :param storage_connectivity_switchless_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#storage_connectivity_switchless_enabled StackHciDeploymentSetting#storage_connectivity_switchless_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc71bd211a9ca565a92b4c7d1dedb4002605becf38cc3e4ca422fcbff54269e4)
            check_type(argname="argument intent", value=intent, expected_type=type_hints["intent"])
            check_type(argname="argument storage_network", value=storage_network, expected_type=type_hints["storage_network"])
            check_type(argname="argument storage_auto_ip_enabled", value=storage_auto_ip_enabled, expected_type=type_hints["storage_auto_ip_enabled"])
            check_type(argname="argument storage_connectivity_switchless_enabled", value=storage_connectivity_switchless_enabled, expected_type=type_hints["storage_connectivity_switchless_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "intent": intent,
            "storage_network": storage_network,
        }
        if storage_auto_ip_enabled is not None:
            self._values["storage_auto_ip_enabled"] = storage_auto_ip_enabled
        if storage_connectivity_switchless_enabled is not None:
            self._values["storage_connectivity_switchless_enabled"] = storage_connectivity_switchless_enabled

    @builtins.property
    def intent(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StackHciDeploymentSettingScaleUnitHostNetworkIntent"]]:
        '''intent block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#intent StackHciDeploymentSetting#intent}
        '''
        result = self._values.get("intent")
        assert result is not None, "Required property 'intent' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StackHciDeploymentSettingScaleUnitHostNetworkIntent"]], result)

    @builtins.property
    def storage_network(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StackHciDeploymentSettingScaleUnitHostNetworkStorageNetwork"]]:
        '''storage_network block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#storage_network StackHciDeploymentSetting#storage_network}
        '''
        result = self._values.get("storage_network")
        assert result is not None, "Required property 'storage_network' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StackHciDeploymentSettingScaleUnitHostNetworkStorageNetwork"]], result)

    @builtins.property
    def storage_auto_ip_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#storage_auto_ip_enabled StackHciDeploymentSetting#storage_auto_ip_enabled}.'''
        result = self._values.get("storage_auto_ip_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def storage_connectivity_switchless_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#storage_connectivity_switchless_enabled StackHciDeploymentSetting#storage_connectivity_switchless_enabled}.'''
        result = self._values.get("storage_connectivity_switchless_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StackHciDeploymentSettingScaleUnitHostNetwork(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.stackHciDeploymentSetting.StackHciDeploymentSettingScaleUnitHostNetworkIntent",
    jsii_struct_bases=[],
    name_mapping={
        "adapter": "adapter",
        "name": "name",
        "traffic_type": "trafficType",
        "adapter_property_override": "adapterPropertyOverride",
        "adapter_property_override_enabled": "adapterPropertyOverrideEnabled",
        "qos_policy_override": "qosPolicyOverride",
        "qos_policy_override_enabled": "qosPolicyOverrideEnabled",
        "virtual_switch_configuration_override": "virtualSwitchConfigurationOverride",
        "virtual_switch_configuration_override_enabled": "virtualSwitchConfigurationOverrideEnabled",
    },
)
class StackHciDeploymentSettingScaleUnitHostNetworkIntent:
    def __init__(
        self,
        *,
        adapter: typing.Sequence[builtins.str],
        name: builtins.str,
        traffic_type: typing.Sequence[builtins.str],
        adapter_property_override: typing.Optional[typing.Union["StackHciDeploymentSettingScaleUnitHostNetworkIntentAdapterPropertyOverride", typing.Dict[builtins.str, typing.Any]]] = None,
        adapter_property_override_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        qos_policy_override: typing.Optional[typing.Union["StackHciDeploymentSettingScaleUnitHostNetworkIntentQosPolicyOverride", typing.Dict[builtins.str, typing.Any]]] = None,
        qos_policy_override_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        virtual_switch_configuration_override: typing.Optional[typing.Union["StackHciDeploymentSettingScaleUnitHostNetworkIntentVirtualSwitchConfigurationOverride", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_switch_configuration_override_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param adapter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#adapter StackHciDeploymentSetting#adapter}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#name StackHciDeploymentSetting#name}.
        :param traffic_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#traffic_type StackHciDeploymentSetting#traffic_type}.
        :param adapter_property_override: adapter_property_override block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#adapter_property_override StackHciDeploymentSetting#adapter_property_override}
        :param adapter_property_override_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#adapter_property_override_enabled StackHciDeploymentSetting#adapter_property_override_enabled}.
        :param qos_policy_override: qos_policy_override block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#qos_policy_override StackHciDeploymentSetting#qos_policy_override}
        :param qos_policy_override_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#qos_policy_override_enabled StackHciDeploymentSetting#qos_policy_override_enabled}.
        :param virtual_switch_configuration_override: virtual_switch_configuration_override block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#virtual_switch_configuration_override StackHciDeploymentSetting#virtual_switch_configuration_override}
        :param virtual_switch_configuration_override_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#virtual_switch_configuration_override_enabled StackHciDeploymentSetting#virtual_switch_configuration_override_enabled}.
        '''
        if isinstance(adapter_property_override, dict):
            adapter_property_override = StackHciDeploymentSettingScaleUnitHostNetworkIntentAdapterPropertyOverride(**adapter_property_override)
        if isinstance(qos_policy_override, dict):
            qos_policy_override = StackHciDeploymentSettingScaleUnitHostNetworkIntentQosPolicyOverride(**qos_policy_override)
        if isinstance(virtual_switch_configuration_override, dict):
            virtual_switch_configuration_override = StackHciDeploymentSettingScaleUnitHostNetworkIntentVirtualSwitchConfigurationOverride(**virtual_switch_configuration_override)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00815a283e091ea35fbff56392dafa835468319ccbedb5c3b950f3730daae635)
            check_type(argname="argument adapter", value=adapter, expected_type=type_hints["adapter"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument traffic_type", value=traffic_type, expected_type=type_hints["traffic_type"])
            check_type(argname="argument adapter_property_override", value=adapter_property_override, expected_type=type_hints["adapter_property_override"])
            check_type(argname="argument adapter_property_override_enabled", value=adapter_property_override_enabled, expected_type=type_hints["adapter_property_override_enabled"])
            check_type(argname="argument qos_policy_override", value=qos_policy_override, expected_type=type_hints["qos_policy_override"])
            check_type(argname="argument qos_policy_override_enabled", value=qos_policy_override_enabled, expected_type=type_hints["qos_policy_override_enabled"])
            check_type(argname="argument virtual_switch_configuration_override", value=virtual_switch_configuration_override, expected_type=type_hints["virtual_switch_configuration_override"])
            check_type(argname="argument virtual_switch_configuration_override_enabled", value=virtual_switch_configuration_override_enabled, expected_type=type_hints["virtual_switch_configuration_override_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "adapter": adapter,
            "name": name,
            "traffic_type": traffic_type,
        }
        if adapter_property_override is not None:
            self._values["adapter_property_override"] = adapter_property_override
        if adapter_property_override_enabled is not None:
            self._values["adapter_property_override_enabled"] = adapter_property_override_enabled
        if qos_policy_override is not None:
            self._values["qos_policy_override"] = qos_policy_override
        if qos_policy_override_enabled is not None:
            self._values["qos_policy_override_enabled"] = qos_policy_override_enabled
        if virtual_switch_configuration_override is not None:
            self._values["virtual_switch_configuration_override"] = virtual_switch_configuration_override
        if virtual_switch_configuration_override_enabled is not None:
            self._values["virtual_switch_configuration_override_enabled"] = virtual_switch_configuration_override_enabled

    @builtins.property
    def adapter(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#adapter StackHciDeploymentSetting#adapter}.'''
        result = self._values.get("adapter")
        assert result is not None, "Required property 'adapter' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#name StackHciDeploymentSetting#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def traffic_type(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#traffic_type StackHciDeploymentSetting#traffic_type}.'''
        result = self._values.get("traffic_type")
        assert result is not None, "Required property 'traffic_type' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def adapter_property_override(
        self,
    ) -> typing.Optional["StackHciDeploymentSettingScaleUnitHostNetworkIntentAdapterPropertyOverride"]:
        '''adapter_property_override block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#adapter_property_override StackHciDeploymentSetting#adapter_property_override}
        '''
        result = self._values.get("adapter_property_override")
        return typing.cast(typing.Optional["StackHciDeploymentSettingScaleUnitHostNetworkIntentAdapterPropertyOverride"], result)

    @builtins.property
    def adapter_property_override_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#adapter_property_override_enabled StackHciDeploymentSetting#adapter_property_override_enabled}.'''
        result = self._values.get("adapter_property_override_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def qos_policy_override(
        self,
    ) -> typing.Optional["StackHciDeploymentSettingScaleUnitHostNetworkIntentQosPolicyOverride"]:
        '''qos_policy_override block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#qos_policy_override StackHciDeploymentSetting#qos_policy_override}
        '''
        result = self._values.get("qos_policy_override")
        return typing.cast(typing.Optional["StackHciDeploymentSettingScaleUnitHostNetworkIntentQosPolicyOverride"], result)

    @builtins.property
    def qos_policy_override_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#qos_policy_override_enabled StackHciDeploymentSetting#qos_policy_override_enabled}.'''
        result = self._values.get("qos_policy_override_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def virtual_switch_configuration_override(
        self,
    ) -> typing.Optional["StackHciDeploymentSettingScaleUnitHostNetworkIntentVirtualSwitchConfigurationOverride"]:
        '''virtual_switch_configuration_override block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#virtual_switch_configuration_override StackHciDeploymentSetting#virtual_switch_configuration_override}
        '''
        result = self._values.get("virtual_switch_configuration_override")
        return typing.cast(typing.Optional["StackHciDeploymentSettingScaleUnitHostNetworkIntentVirtualSwitchConfigurationOverride"], result)

    @builtins.property
    def virtual_switch_configuration_override_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#virtual_switch_configuration_override_enabled StackHciDeploymentSetting#virtual_switch_configuration_override_enabled}.'''
        result = self._values.get("virtual_switch_configuration_override_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StackHciDeploymentSettingScaleUnitHostNetworkIntent(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.stackHciDeploymentSetting.StackHciDeploymentSettingScaleUnitHostNetworkIntentAdapterPropertyOverride",
    jsii_struct_bases=[],
    name_mapping={
        "jumbo_packet": "jumboPacket",
        "network_direct": "networkDirect",
        "network_direct_technology": "networkDirectTechnology",
    },
)
class StackHciDeploymentSettingScaleUnitHostNetworkIntentAdapterPropertyOverride:
    def __init__(
        self,
        *,
        jumbo_packet: typing.Optional[builtins.str] = None,
        network_direct: typing.Optional[builtins.str] = None,
        network_direct_technology: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param jumbo_packet: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#jumbo_packet StackHciDeploymentSetting#jumbo_packet}.
        :param network_direct: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#network_direct StackHciDeploymentSetting#network_direct}.
        :param network_direct_technology: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#network_direct_technology StackHciDeploymentSetting#network_direct_technology}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44a45f532c90cdd76480e7cf99729e0e60da82bdf9983beb0d019b3ce1a7e227)
            check_type(argname="argument jumbo_packet", value=jumbo_packet, expected_type=type_hints["jumbo_packet"])
            check_type(argname="argument network_direct", value=network_direct, expected_type=type_hints["network_direct"])
            check_type(argname="argument network_direct_technology", value=network_direct_technology, expected_type=type_hints["network_direct_technology"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if jumbo_packet is not None:
            self._values["jumbo_packet"] = jumbo_packet
        if network_direct is not None:
            self._values["network_direct"] = network_direct
        if network_direct_technology is not None:
            self._values["network_direct_technology"] = network_direct_technology

    @builtins.property
    def jumbo_packet(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#jumbo_packet StackHciDeploymentSetting#jumbo_packet}.'''
        result = self._values.get("jumbo_packet")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_direct(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#network_direct StackHciDeploymentSetting#network_direct}.'''
        result = self._values.get("network_direct")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_direct_technology(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#network_direct_technology StackHciDeploymentSetting#network_direct_technology}.'''
        result = self._values.get("network_direct_technology")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StackHciDeploymentSettingScaleUnitHostNetworkIntentAdapterPropertyOverride(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StackHciDeploymentSettingScaleUnitHostNetworkIntentAdapterPropertyOverrideOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.stackHciDeploymentSetting.StackHciDeploymentSettingScaleUnitHostNetworkIntentAdapterPropertyOverrideOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fcacd2fa801cb29b2c682fb1b033375fd96b6ace058dfe61ee9401d840ee803e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetJumboPacket")
    def reset_jumbo_packet(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJumboPacket", []))

    @jsii.member(jsii_name="resetNetworkDirect")
    def reset_network_direct(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkDirect", []))

    @jsii.member(jsii_name="resetNetworkDirectTechnology")
    def reset_network_direct_technology(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkDirectTechnology", []))

    @builtins.property
    @jsii.member(jsii_name="jumboPacketInput")
    def jumbo_packet_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jumboPacketInput"))

    @builtins.property
    @jsii.member(jsii_name="networkDirectInput")
    def network_direct_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkDirectInput"))

    @builtins.property
    @jsii.member(jsii_name="networkDirectTechnologyInput")
    def network_direct_technology_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkDirectTechnologyInput"))

    @builtins.property
    @jsii.member(jsii_name="jumboPacket")
    def jumbo_packet(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jumboPacket"))

    @jumbo_packet.setter
    def jumbo_packet(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da0a954571584d40dd9b92e191759c2bad0724ef8a1572071dbec9a0641747ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jumboPacket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkDirect")
    def network_direct(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkDirect"))

    @network_direct.setter
    def network_direct(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acf2fa4ecc516c5aef78ae75495d4e7b574224def3eaac9e3fbedf98bb4fe4ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkDirect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkDirectTechnology")
    def network_direct_technology(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkDirectTechnology"))

    @network_direct_technology.setter
    def network_direct_technology(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b88cad996d331039a43c3b670914f20713a69097b0e5bb3dd039965a332306b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkDirectTechnology", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StackHciDeploymentSettingScaleUnitHostNetworkIntentAdapterPropertyOverride]:
        return typing.cast(typing.Optional[StackHciDeploymentSettingScaleUnitHostNetworkIntentAdapterPropertyOverride], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StackHciDeploymentSettingScaleUnitHostNetworkIntentAdapterPropertyOverride],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__691b90666b156aae3964aaac81d3e156aa3518bd545bf60c7002bc118b3f02d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class StackHciDeploymentSettingScaleUnitHostNetworkIntentList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.stackHciDeploymentSetting.StackHciDeploymentSettingScaleUnitHostNetworkIntentList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__525c3e3686906ef069331f2b588e398738ced49ee1963706a5669e629d4bb3ed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "StackHciDeploymentSettingScaleUnitHostNetworkIntentOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9161507eab2b4b950ac2f0262e84b0a4872cffdf370e30a28e13fc4d7ba2ee0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("StackHciDeploymentSettingScaleUnitHostNetworkIntentOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57ecd506d132e099265d4868cde82760e25cfed59ef3cc5e392c7d9257fa14b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c3e3ed94b5b4f83c582caeef4e7de0bdb835df6196d44f26952f789e81c4594)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad136bf619c0a1518813897058bebba5f4dacec2c2111ad96d72c29ad5ea1180)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StackHciDeploymentSettingScaleUnitHostNetworkIntent]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StackHciDeploymentSettingScaleUnitHostNetworkIntent]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StackHciDeploymentSettingScaleUnitHostNetworkIntent]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d29bb2540f1fe427d7754b615c96746698810a2aa0438a6d7d84bc1f4020403c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class StackHciDeploymentSettingScaleUnitHostNetworkIntentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.stackHciDeploymentSetting.StackHciDeploymentSettingScaleUnitHostNetworkIntentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__743fb4d1b7641a77097bbf456c2ec0796c914eeffc0fea40879baccada89fcf2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAdapterPropertyOverride")
    def put_adapter_property_override(
        self,
        *,
        jumbo_packet: typing.Optional[builtins.str] = None,
        network_direct: typing.Optional[builtins.str] = None,
        network_direct_technology: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param jumbo_packet: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#jumbo_packet StackHciDeploymentSetting#jumbo_packet}.
        :param network_direct: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#network_direct StackHciDeploymentSetting#network_direct}.
        :param network_direct_technology: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#network_direct_technology StackHciDeploymentSetting#network_direct_technology}.
        '''
        value = StackHciDeploymentSettingScaleUnitHostNetworkIntentAdapterPropertyOverride(
            jumbo_packet=jumbo_packet,
            network_direct=network_direct,
            network_direct_technology=network_direct_technology,
        )

        return typing.cast(None, jsii.invoke(self, "putAdapterPropertyOverride", [value]))

    @jsii.member(jsii_name="putQosPolicyOverride")
    def put_qos_policy_override(
        self,
        *,
        bandwidth_percentage_smb: typing.Optional[builtins.str] = None,
        priority_value8021_action_cluster: typing.Optional[builtins.str] = None,
        priority_value8021_action_smb: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bandwidth_percentage_smb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#bandwidth_percentage_smb StackHciDeploymentSetting#bandwidth_percentage_smb}.
        :param priority_value8021_action_cluster: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#priority_value8021_action_cluster StackHciDeploymentSetting#priority_value8021_action_cluster}.
        :param priority_value8021_action_smb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#priority_value8021_action_smb StackHciDeploymentSetting#priority_value8021_action_smb}.
        '''
        value = StackHciDeploymentSettingScaleUnitHostNetworkIntentQosPolicyOverride(
            bandwidth_percentage_smb=bandwidth_percentage_smb,
            priority_value8021_action_cluster=priority_value8021_action_cluster,
            priority_value8021_action_smb=priority_value8021_action_smb,
        )

        return typing.cast(None, jsii.invoke(self, "putQosPolicyOverride", [value]))

    @jsii.member(jsii_name="putVirtualSwitchConfigurationOverride")
    def put_virtual_switch_configuration_override(
        self,
        *,
        enable_iov: typing.Optional[builtins.str] = None,
        load_balancing_algorithm: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enable_iov: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#enable_iov StackHciDeploymentSetting#enable_iov}.
        :param load_balancing_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#load_balancing_algorithm StackHciDeploymentSetting#load_balancing_algorithm}.
        '''
        value = StackHciDeploymentSettingScaleUnitHostNetworkIntentVirtualSwitchConfigurationOverride(
            enable_iov=enable_iov, load_balancing_algorithm=load_balancing_algorithm
        )

        return typing.cast(None, jsii.invoke(self, "putVirtualSwitchConfigurationOverride", [value]))

    @jsii.member(jsii_name="resetAdapterPropertyOverride")
    def reset_adapter_property_override(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdapterPropertyOverride", []))

    @jsii.member(jsii_name="resetAdapterPropertyOverrideEnabled")
    def reset_adapter_property_override_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdapterPropertyOverrideEnabled", []))

    @jsii.member(jsii_name="resetQosPolicyOverride")
    def reset_qos_policy_override(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQosPolicyOverride", []))

    @jsii.member(jsii_name="resetQosPolicyOverrideEnabled")
    def reset_qos_policy_override_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQosPolicyOverrideEnabled", []))

    @jsii.member(jsii_name="resetVirtualSwitchConfigurationOverride")
    def reset_virtual_switch_configuration_override(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualSwitchConfigurationOverride", []))

    @jsii.member(jsii_name="resetVirtualSwitchConfigurationOverrideEnabled")
    def reset_virtual_switch_configuration_override_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualSwitchConfigurationOverrideEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="adapterPropertyOverride")
    def adapter_property_override(
        self,
    ) -> StackHciDeploymentSettingScaleUnitHostNetworkIntentAdapterPropertyOverrideOutputReference:
        return typing.cast(StackHciDeploymentSettingScaleUnitHostNetworkIntentAdapterPropertyOverrideOutputReference, jsii.get(self, "adapterPropertyOverride"))

    @builtins.property
    @jsii.member(jsii_name="qosPolicyOverride")
    def qos_policy_override(
        self,
    ) -> "StackHciDeploymentSettingScaleUnitHostNetworkIntentQosPolicyOverrideOutputReference":
        return typing.cast("StackHciDeploymentSettingScaleUnitHostNetworkIntentQosPolicyOverrideOutputReference", jsii.get(self, "qosPolicyOverride"))

    @builtins.property
    @jsii.member(jsii_name="virtualSwitchConfigurationOverride")
    def virtual_switch_configuration_override(
        self,
    ) -> "StackHciDeploymentSettingScaleUnitHostNetworkIntentVirtualSwitchConfigurationOverrideOutputReference":
        return typing.cast("StackHciDeploymentSettingScaleUnitHostNetworkIntentVirtualSwitchConfigurationOverrideOutputReference", jsii.get(self, "virtualSwitchConfigurationOverride"))

    @builtins.property
    @jsii.member(jsii_name="adapterInput")
    def adapter_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "adapterInput"))

    @builtins.property
    @jsii.member(jsii_name="adapterPropertyOverrideEnabledInput")
    def adapter_property_override_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "adapterPropertyOverrideEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="adapterPropertyOverrideInput")
    def adapter_property_override_input(
        self,
    ) -> typing.Optional[StackHciDeploymentSettingScaleUnitHostNetworkIntentAdapterPropertyOverride]:
        return typing.cast(typing.Optional[StackHciDeploymentSettingScaleUnitHostNetworkIntentAdapterPropertyOverride], jsii.get(self, "adapterPropertyOverrideInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="qosPolicyOverrideEnabledInput")
    def qos_policy_override_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "qosPolicyOverrideEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="qosPolicyOverrideInput")
    def qos_policy_override_input(
        self,
    ) -> typing.Optional["StackHciDeploymentSettingScaleUnitHostNetworkIntentQosPolicyOverride"]:
        return typing.cast(typing.Optional["StackHciDeploymentSettingScaleUnitHostNetworkIntentQosPolicyOverride"], jsii.get(self, "qosPolicyOverrideInput"))

    @builtins.property
    @jsii.member(jsii_name="trafficTypeInput")
    def traffic_type_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "trafficTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualSwitchConfigurationOverrideEnabledInput")
    def virtual_switch_configuration_override_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "virtualSwitchConfigurationOverrideEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualSwitchConfigurationOverrideInput")
    def virtual_switch_configuration_override_input(
        self,
    ) -> typing.Optional["StackHciDeploymentSettingScaleUnitHostNetworkIntentVirtualSwitchConfigurationOverride"]:
        return typing.cast(typing.Optional["StackHciDeploymentSettingScaleUnitHostNetworkIntentVirtualSwitchConfigurationOverride"], jsii.get(self, "virtualSwitchConfigurationOverrideInput"))

    @builtins.property
    @jsii.member(jsii_name="adapter")
    def adapter(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "adapter"))

    @adapter.setter
    def adapter(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3d312bdc66706132f747129e2047a07c40cb1f0e26ec67822f63cc0948be8cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adapter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="adapterPropertyOverrideEnabled")
    def adapter_property_override_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "adapterPropertyOverrideEnabled"))

    @adapter_property_override_enabled.setter
    def adapter_property_override_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__731f5633aae2338037f001ae14c10bad743ea98a4e9e123ab307f13530654aa6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adapterPropertyOverrideEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85d4d030ccf379d2bad645226681dfec4429e2b0bbc9d72bf00d568da2d620ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="qosPolicyOverrideEnabled")
    def qos_policy_override_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "qosPolicyOverrideEnabled"))

    @qos_policy_override_enabled.setter
    def qos_policy_override_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fc6db1a24023462d4c83f5dee3077204dad4ee53e0f17455a34bcd756b26ee1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "qosPolicyOverrideEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trafficType")
    def traffic_type(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "trafficType"))

    @traffic_type.setter
    def traffic_type(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a893356e9b83a678a052f73d68b516c9664a467762efc1d03d552857419866bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trafficType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualSwitchConfigurationOverrideEnabled")
    def virtual_switch_configuration_override_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "virtualSwitchConfigurationOverrideEnabled"))

    @virtual_switch_configuration_override_enabled.setter
    def virtual_switch_configuration_override_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2456baecb1cde83d0f40e564ca0d92db03ffabbd652ded5481f5e9a05cb1fb17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualSwitchConfigurationOverrideEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StackHciDeploymentSettingScaleUnitHostNetworkIntent]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StackHciDeploymentSettingScaleUnitHostNetworkIntent]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StackHciDeploymentSettingScaleUnitHostNetworkIntent]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc079b04ecec38f4f59d4dd1f05112f9281efe0ee01eb1c6615ffc13a7fe2333)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.stackHciDeploymentSetting.StackHciDeploymentSettingScaleUnitHostNetworkIntentQosPolicyOverride",
    jsii_struct_bases=[],
    name_mapping={
        "bandwidth_percentage_smb": "bandwidthPercentageSmb",
        "priority_value8021_action_cluster": "priorityValue8021ActionCluster",
        "priority_value8021_action_smb": "priorityValue8021ActionSmb",
    },
)
class StackHciDeploymentSettingScaleUnitHostNetworkIntentQosPolicyOverride:
    def __init__(
        self,
        *,
        bandwidth_percentage_smb: typing.Optional[builtins.str] = None,
        priority_value8021_action_cluster: typing.Optional[builtins.str] = None,
        priority_value8021_action_smb: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bandwidth_percentage_smb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#bandwidth_percentage_smb StackHciDeploymentSetting#bandwidth_percentage_smb}.
        :param priority_value8021_action_cluster: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#priority_value8021_action_cluster StackHciDeploymentSetting#priority_value8021_action_cluster}.
        :param priority_value8021_action_smb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#priority_value8021_action_smb StackHciDeploymentSetting#priority_value8021_action_smb}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95231d03870f48168995cc2dd94b625fc76040ad2cfdfe7fb7f9ce4ebdf1cb36)
            check_type(argname="argument bandwidth_percentage_smb", value=bandwidth_percentage_smb, expected_type=type_hints["bandwidth_percentage_smb"])
            check_type(argname="argument priority_value8021_action_cluster", value=priority_value8021_action_cluster, expected_type=type_hints["priority_value8021_action_cluster"])
            check_type(argname="argument priority_value8021_action_smb", value=priority_value8021_action_smb, expected_type=type_hints["priority_value8021_action_smb"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bandwidth_percentage_smb is not None:
            self._values["bandwidth_percentage_smb"] = bandwidth_percentage_smb
        if priority_value8021_action_cluster is not None:
            self._values["priority_value8021_action_cluster"] = priority_value8021_action_cluster
        if priority_value8021_action_smb is not None:
            self._values["priority_value8021_action_smb"] = priority_value8021_action_smb

    @builtins.property
    def bandwidth_percentage_smb(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#bandwidth_percentage_smb StackHciDeploymentSetting#bandwidth_percentage_smb}.'''
        result = self._values.get("bandwidth_percentage_smb")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def priority_value8021_action_cluster(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#priority_value8021_action_cluster StackHciDeploymentSetting#priority_value8021_action_cluster}.'''
        result = self._values.get("priority_value8021_action_cluster")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def priority_value8021_action_smb(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#priority_value8021_action_smb StackHciDeploymentSetting#priority_value8021_action_smb}.'''
        result = self._values.get("priority_value8021_action_smb")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StackHciDeploymentSettingScaleUnitHostNetworkIntentQosPolicyOverride(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StackHciDeploymentSettingScaleUnitHostNetworkIntentQosPolicyOverrideOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.stackHciDeploymentSetting.StackHciDeploymentSettingScaleUnitHostNetworkIntentQosPolicyOverrideOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__86868a2f428f26deaff4aaccef763d8808e5b8d8cc5879b807c397622f74c8b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBandwidthPercentageSmb")
    def reset_bandwidth_percentage_smb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBandwidthPercentageSmb", []))

    @jsii.member(jsii_name="resetPriorityValue8021ActionCluster")
    def reset_priority_value8021_action_cluster(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPriorityValue8021ActionCluster", []))

    @jsii.member(jsii_name="resetPriorityValue8021ActionSmb")
    def reset_priority_value8021_action_smb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPriorityValue8021ActionSmb", []))

    @builtins.property
    @jsii.member(jsii_name="bandwidthPercentageSmbInput")
    def bandwidth_percentage_smb_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bandwidthPercentageSmbInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityValue8021ActionClusterInput")
    def priority_value8021_action_cluster_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "priorityValue8021ActionClusterInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityValue8021ActionSmbInput")
    def priority_value8021_action_smb_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "priorityValue8021ActionSmbInput"))

    @builtins.property
    @jsii.member(jsii_name="bandwidthPercentageSmb")
    def bandwidth_percentage_smb(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bandwidthPercentageSmb"))

    @bandwidth_percentage_smb.setter
    def bandwidth_percentage_smb(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc922b09388af2943eb66fdd255833e0e8e5e6a02c2fddf517ca55052415c4c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bandwidthPercentageSmb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priorityValue8021ActionCluster")
    def priority_value8021_action_cluster(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "priorityValue8021ActionCluster"))

    @priority_value8021_action_cluster.setter
    def priority_value8021_action_cluster(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b2d3ebab4679717fe8a64db2c6aa2401e5d96d07ff76c4fcd3a54d40e0592db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priorityValue8021ActionCluster", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priorityValue8021ActionSmb")
    def priority_value8021_action_smb(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "priorityValue8021ActionSmb"))

    @priority_value8021_action_smb.setter
    def priority_value8021_action_smb(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__173f2326c07a1e9bfea04d906cb28eec0bb483c98132d022cc572367d0296e23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priorityValue8021ActionSmb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StackHciDeploymentSettingScaleUnitHostNetworkIntentQosPolicyOverride]:
        return typing.cast(typing.Optional[StackHciDeploymentSettingScaleUnitHostNetworkIntentQosPolicyOverride], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StackHciDeploymentSettingScaleUnitHostNetworkIntentQosPolicyOverride],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c282b78b191ceed89307c30bc790372a892bc699aa92dadbea91bb217ac812df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.stackHciDeploymentSetting.StackHciDeploymentSettingScaleUnitHostNetworkIntentVirtualSwitchConfigurationOverride",
    jsii_struct_bases=[],
    name_mapping={
        "enable_iov": "enableIov",
        "load_balancing_algorithm": "loadBalancingAlgorithm",
    },
)
class StackHciDeploymentSettingScaleUnitHostNetworkIntentVirtualSwitchConfigurationOverride:
    def __init__(
        self,
        *,
        enable_iov: typing.Optional[builtins.str] = None,
        load_balancing_algorithm: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enable_iov: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#enable_iov StackHciDeploymentSetting#enable_iov}.
        :param load_balancing_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#load_balancing_algorithm StackHciDeploymentSetting#load_balancing_algorithm}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92c09917f8d674c18c9b80152eff42e2519e95de4aaad01234a65de7488d0e27)
            check_type(argname="argument enable_iov", value=enable_iov, expected_type=type_hints["enable_iov"])
            check_type(argname="argument load_balancing_algorithm", value=load_balancing_algorithm, expected_type=type_hints["load_balancing_algorithm"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_iov is not None:
            self._values["enable_iov"] = enable_iov
        if load_balancing_algorithm is not None:
            self._values["load_balancing_algorithm"] = load_balancing_algorithm

    @builtins.property
    def enable_iov(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#enable_iov StackHciDeploymentSetting#enable_iov}.'''
        result = self._values.get("enable_iov")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def load_balancing_algorithm(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#load_balancing_algorithm StackHciDeploymentSetting#load_balancing_algorithm}.'''
        result = self._values.get("load_balancing_algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StackHciDeploymentSettingScaleUnitHostNetworkIntentVirtualSwitchConfigurationOverride(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StackHciDeploymentSettingScaleUnitHostNetworkIntentVirtualSwitchConfigurationOverrideOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.stackHciDeploymentSetting.StackHciDeploymentSettingScaleUnitHostNetworkIntentVirtualSwitchConfigurationOverrideOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__36eff91940f925f14754357a3b832bcb29947089b1dcdc0c09fa56efdfc32a0a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnableIov")
    def reset_enable_iov(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableIov", []))

    @jsii.member(jsii_name="resetLoadBalancingAlgorithm")
    def reset_load_balancing_algorithm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoadBalancingAlgorithm", []))

    @builtins.property
    @jsii.member(jsii_name="enableIovInput")
    def enable_iov_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enableIovInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancingAlgorithmInput")
    def load_balancing_algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loadBalancingAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="enableIov")
    def enable_iov(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enableIov"))

    @enable_iov.setter
    def enable_iov(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4ff9dbbb9b2a5d5a8fcadb1da254d21e485cab1daf8fa534398fb2a37f491ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableIov", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loadBalancingAlgorithm")
    def load_balancing_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadBalancingAlgorithm"))

    @load_balancing_algorithm.setter
    def load_balancing_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad1ff031c18974e980bedc6373376df8c0943c1f551243fc72845fbef6e6d0b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancingAlgorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StackHciDeploymentSettingScaleUnitHostNetworkIntentVirtualSwitchConfigurationOverride]:
        return typing.cast(typing.Optional[StackHciDeploymentSettingScaleUnitHostNetworkIntentVirtualSwitchConfigurationOverride], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StackHciDeploymentSettingScaleUnitHostNetworkIntentVirtualSwitchConfigurationOverride],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5602214d3a0ca4bd15a7ff434b9c99bacffe593829bd7ace8600735b8e790009)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class StackHciDeploymentSettingScaleUnitHostNetworkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.stackHciDeploymentSetting.StackHciDeploymentSettingScaleUnitHostNetworkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__75ab6826e3196cea0542ee54c24441ad6db11d73f5fa50e97c69dab495af0e8b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIntent")
    def put_intent(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StackHciDeploymentSettingScaleUnitHostNetworkIntent, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fe9cda1e7b9407fa867b1b60c9e7866f8920c9e268b147f7509aab6818e7128)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIntent", [value]))

    @jsii.member(jsii_name="putStorageNetwork")
    def put_storage_network(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["StackHciDeploymentSettingScaleUnitHostNetworkStorageNetwork", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b87e1f1cb0a20e04a72b86d32878eadc3cf3aa16e86ae7ac831dacdf84bb949)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStorageNetwork", [value]))

    @jsii.member(jsii_name="resetStorageAutoIpEnabled")
    def reset_storage_auto_ip_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageAutoIpEnabled", []))

    @jsii.member(jsii_name="resetStorageConnectivitySwitchlessEnabled")
    def reset_storage_connectivity_switchless_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageConnectivitySwitchlessEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="intent")
    def intent(self) -> StackHciDeploymentSettingScaleUnitHostNetworkIntentList:
        return typing.cast(StackHciDeploymentSettingScaleUnitHostNetworkIntentList, jsii.get(self, "intent"))

    @builtins.property
    @jsii.member(jsii_name="storageNetwork")
    def storage_network(
        self,
    ) -> "StackHciDeploymentSettingScaleUnitHostNetworkStorageNetworkList":
        return typing.cast("StackHciDeploymentSettingScaleUnitHostNetworkStorageNetworkList", jsii.get(self, "storageNetwork"))

    @builtins.property
    @jsii.member(jsii_name="intentInput")
    def intent_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StackHciDeploymentSettingScaleUnitHostNetworkIntent]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StackHciDeploymentSettingScaleUnitHostNetworkIntent]]], jsii.get(self, "intentInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAutoIpEnabledInput")
    def storage_auto_ip_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "storageAutoIpEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="storageConnectivitySwitchlessEnabledInput")
    def storage_connectivity_switchless_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "storageConnectivitySwitchlessEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="storageNetworkInput")
    def storage_network_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StackHciDeploymentSettingScaleUnitHostNetworkStorageNetwork"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StackHciDeploymentSettingScaleUnitHostNetworkStorageNetwork"]]], jsii.get(self, "storageNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAutoIpEnabled")
    def storage_auto_ip_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "storageAutoIpEnabled"))

    @storage_auto_ip_enabled.setter
    def storage_auto_ip_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3ac8a0d6fe5534bf9a9a8f9c462cfd7cc96ff1c20cfd1c9de6df158ea43c718)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAutoIpEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageConnectivitySwitchlessEnabled")
    def storage_connectivity_switchless_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "storageConnectivitySwitchlessEnabled"))

    @storage_connectivity_switchless_enabled.setter
    def storage_connectivity_switchless_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbf1379b64d7328385d32948f8da2f444f17cef576e74f5bc4f34e3d160314a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageConnectivitySwitchlessEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StackHciDeploymentSettingScaleUnitHostNetwork]:
        return typing.cast(typing.Optional[StackHciDeploymentSettingScaleUnitHostNetwork], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StackHciDeploymentSettingScaleUnitHostNetwork],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd2a7f98ab0fa7e53cfdff600f8ffb69b35b88e0ac6668228c0da55b379617fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.stackHciDeploymentSetting.StackHciDeploymentSettingScaleUnitHostNetworkStorageNetwork",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "network_adapter_name": "networkAdapterName",
        "vlan_id": "vlanId",
    },
)
class StackHciDeploymentSettingScaleUnitHostNetworkStorageNetwork:
    def __init__(
        self,
        *,
        name: builtins.str,
        network_adapter_name: builtins.str,
        vlan_id: builtins.str,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#name StackHciDeploymentSetting#name}.
        :param network_adapter_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#network_adapter_name StackHciDeploymentSetting#network_adapter_name}.
        :param vlan_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#vlan_id StackHciDeploymentSetting#vlan_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d10a12e0918f485a854f54e6cb30a396b21a79c95bbcbcbec9213b512d45c358)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network_adapter_name", value=network_adapter_name, expected_type=type_hints["network_adapter_name"])
            check_type(argname="argument vlan_id", value=vlan_id, expected_type=type_hints["vlan_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "network_adapter_name": network_adapter_name,
            "vlan_id": vlan_id,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#name StackHciDeploymentSetting#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_adapter_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#network_adapter_name StackHciDeploymentSetting#network_adapter_name}.'''
        result = self._values.get("network_adapter_name")
        assert result is not None, "Required property 'network_adapter_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vlan_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#vlan_id StackHciDeploymentSetting#vlan_id}.'''
        result = self._values.get("vlan_id")
        assert result is not None, "Required property 'vlan_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StackHciDeploymentSettingScaleUnitHostNetworkStorageNetwork(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StackHciDeploymentSettingScaleUnitHostNetworkStorageNetworkList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.stackHciDeploymentSetting.StackHciDeploymentSettingScaleUnitHostNetworkStorageNetworkList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__264c8bad7b99a4f63c947f4f8d2087c9dd7396f60e45de176a706adbdd058adc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "StackHciDeploymentSettingScaleUnitHostNetworkStorageNetworkOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee0b19225087877e59cf9d24e18155de3a81d05b4a323476dce6b4f9af62ed4a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("StackHciDeploymentSettingScaleUnitHostNetworkStorageNetworkOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dd03d7a0e864d97d0db8d396489f51dc800d1467d2fc7eca2cdd1190eda6e2c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__42e50eeaa90c5e49b8aab9c975d010ff4efd8785f432eb3212d9399d163f25ba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d58feef1fcaf8784024289427abea4c5e3441d21dbb77bc2de393ec18243fd8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StackHciDeploymentSettingScaleUnitHostNetworkStorageNetwork]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StackHciDeploymentSettingScaleUnitHostNetworkStorageNetwork]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StackHciDeploymentSettingScaleUnitHostNetworkStorageNetwork]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb5eba85e3b8931f293af5840b02627d27a048223413a3dbbcf6e13d76c7e9a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class StackHciDeploymentSettingScaleUnitHostNetworkStorageNetworkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.stackHciDeploymentSetting.StackHciDeploymentSettingScaleUnitHostNetworkStorageNetworkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e9be8d88b47e24b760d53914cb29201ba657afa443b8233d4e4ce4eadfd26ae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkAdapterNameInput")
    def network_adapter_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkAdapterNameInput"))

    @builtins.property
    @jsii.member(jsii_name="vlanIdInput")
    def vlan_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vlanIdInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5aa5d2928a1dc5bc0726e806054e2ea929f143470d0deae7551f1a911576c78e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkAdapterName")
    def network_adapter_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkAdapterName"))

    @network_adapter_name.setter
    def network_adapter_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__496dd2c1157a9a825d36281d6b62c54e2554c787be45dbc08868693a73e11e3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkAdapterName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vlanId")
    def vlan_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vlanId"))

    @vlan_id.setter
    def vlan_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dd9080ee04e631a20cf3fd1e0522da5c24b565c8cb6fab72f7e79d61fb39228)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vlanId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StackHciDeploymentSettingScaleUnitHostNetworkStorageNetwork]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StackHciDeploymentSettingScaleUnitHostNetworkStorageNetwork]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StackHciDeploymentSettingScaleUnitHostNetworkStorageNetwork]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89b4ac5acd17d60fc7813962496ec8bebf1f5396a66900e8cb7aee59c01db5c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.stackHciDeploymentSetting.StackHciDeploymentSettingScaleUnitInfrastructureNetwork",
    jsii_struct_bases=[],
    name_mapping={
        "dns_server": "dnsServer",
        "gateway": "gateway",
        "ip_pool": "ipPool",
        "subnet_mask": "subnetMask",
        "dhcp_enabled": "dhcpEnabled",
    },
)
class StackHciDeploymentSettingScaleUnitInfrastructureNetwork:
    def __init__(
        self,
        *,
        dns_server: typing.Sequence[builtins.str],
        gateway: builtins.str,
        ip_pool: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["StackHciDeploymentSettingScaleUnitInfrastructureNetworkIpPool", typing.Dict[builtins.str, typing.Any]]]],
        subnet_mask: builtins.str,
        dhcp_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param dns_server: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#dns_server StackHciDeploymentSetting#dns_server}.
        :param gateway: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#gateway StackHciDeploymentSetting#gateway}.
        :param ip_pool: ip_pool block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#ip_pool StackHciDeploymentSetting#ip_pool}
        :param subnet_mask: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#subnet_mask StackHciDeploymentSetting#subnet_mask}.
        :param dhcp_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#dhcp_enabled StackHciDeploymentSetting#dhcp_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69dea3c8324a77a29903ff53f89cf34424370f0476890d0a449b6993979e1b6f)
            check_type(argname="argument dns_server", value=dns_server, expected_type=type_hints["dns_server"])
            check_type(argname="argument gateway", value=gateway, expected_type=type_hints["gateway"])
            check_type(argname="argument ip_pool", value=ip_pool, expected_type=type_hints["ip_pool"])
            check_type(argname="argument subnet_mask", value=subnet_mask, expected_type=type_hints["subnet_mask"])
            check_type(argname="argument dhcp_enabled", value=dhcp_enabled, expected_type=type_hints["dhcp_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dns_server": dns_server,
            "gateway": gateway,
            "ip_pool": ip_pool,
            "subnet_mask": subnet_mask,
        }
        if dhcp_enabled is not None:
            self._values["dhcp_enabled"] = dhcp_enabled

    @builtins.property
    def dns_server(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#dns_server StackHciDeploymentSetting#dns_server}.'''
        result = self._values.get("dns_server")
        assert result is not None, "Required property 'dns_server' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def gateway(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#gateway StackHciDeploymentSetting#gateway}.'''
        result = self._values.get("gateway")
        assert result is not None, "Required property 'gateway' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip_pool(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StackHciDeploymentSettingScaleUnitInfrastructureNetworkIpPool"]]:
        '''ip_pool block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#ip_pool StackHciDeploymentSetting#ip_pool}
        '''
        result = self._values.get("ip_pool")
        assert result is not None, "Required property 'ip_pool' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StackHciDeploymentSettingScaleUnitInfrastructureNetworkIpPool"]], result)

    @builtins.property
    def subnet_mask(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#subnet_mask StackHciDeploymentSetting#subnet_mask}.'''
        result = self._values.get("subnet_mask")
        assert result is not None, "Required property 'subnet_mask' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dhcp_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#dhcp_enabled StackHciDeploymentSetting#dhcp_enabled}.'''
        result = self._values.get("dhcp_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StackHciDeploymentSettingScaleUnitInfrastructureNetwork(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.stackHciDeploymentSetting.StackHciDeploymentSettingScaleUnitInfrastructureNetworkIpPool",
    jsii_struct_bases=[],
    name_mapping={
        "ending_address": "endingAddress",
        "starting_address": "startingAddress",
    },
)
class StackHciDeploymentSettingScaleUnitInfrastructureNetworkIpPool:
    def __init__(
        self,
        *,
        ending_address: builtins.str,
        starting_address: builtins.str,
    ) -> None:
        '''
        :param ending_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#ending_address StackHciDeploymentSetting#ending_address}.
        :param starting_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#starting_address StackHciDeploymentSetting#starting_address}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17837551bf9943c49df86e838a86593520b16fe62c03669319865dd8feebecd3)
            check_type(argname="argument ending_address", value=ending_address, expected_type=type_hints["ending_address"])
            check_type(argname="argument starting_address", value=starting_address, expected_type=type_hints["starting_address"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ending_address": ending_address,
            "starting_address": starting_address,
        }

    @builtins.property
    def ending_address(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#ending_address StackHciDeploymentSetting#ending_address}.'''
        result = self._values.get("ending_address")
        assert result is not None, "Required property 'ending_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def starting_address(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#starting_address StackHciDeploymentSetting#starting_address}.'''
        result = self._values.get("starting_address")
        assert result is not None, "Required property 'starting_address' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StackHciDeploymentSettingScaleUnitInfrastructureNetworkIpPool(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StackHciDeploymentSettingScaleUnitInfrastructureNetworkIpPoolList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.stackHciDeploymentSetting.StackHciDeploymentSettingScaleUnitInfrastructureNetworkIpPoolList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__523b1bba340a4419e1141d6959cabde1bbdd4cf6403ffaeba34f4ba354330398)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "StackHciDeploymentSettingScaleUnitInfrastructureNetworkIpPoolOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89de318c66637bca999c4f4b5167c79f66001249fbf4df822ea024fa2685ec6f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("StackHciDeploymentSettingScaleUnitInfrastructureNetworkIpPoolOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e0eaba0ea4dff49396fa2f9ac9976a9b5a19aeace46809ab9227c11a3ae6fa0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a0da4904b7ad8ce72a19c7afd668b51b30fd190ab983e85f4b274e63bd1757d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__63e5c0c1902ea7a2502419b52dda890bdd8c1e923361062966b6e5135a3514b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StackHciDeploymentSettingScaleUnitInfrastructureNetworkIpPool]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StackHciDeploymentSettingScaleUnitInfrastructureNetworkIpPool]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StackHciDeploymentSettingScaleUnitInfrastructureNetworkIpPool]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3f6a9b61219cf3ed78a58e3d1277c6e5a129cba0568ad182ee58592d590a134)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class StackHciDeploymentSettingScaleUnitInfrastructureNetworkIpPoolOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.stackHciDeploymentSetting.StackHciDeploymentSettingScaleUnitInfrastructureNetworkIpPoolOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b67fa274012a1b7c3c541347abd869c2f5994140c3dae31cd7b02cc605f3a6a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="endingAddressInput")
    def ending_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endingAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="startingAddressInput")
    def starting_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startingAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="endingAddress")
    def ending_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endingAddress"))

    @ending_address.setter
    def ending_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff0f1e91e5eda0438895d6a7ae81ff45ce8816bd6c55c7aa40ba5b0eed3529ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endingAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startingAddress")
    def starting_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startingAddress"))

    @starting_address.setter
    def starting_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d22e5d1d551aa989a1f41a98281c044ed173f29d2a9d4abf75eff7bb5d4eaa3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startingAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StackHciDeploymentSettingScaleUnitInfrastructureNetworkIpPool]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StackHciDeploymentSettingScaleUnitInfrastructureNetworkIpPool]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StackHciDeploymentSettingScaleUnitInfrastructureNetworkIpPool]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c80f8104cdded28b351c27ce10efff748d7ed3fa36d0edc0f9e447950b9bf69c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class StackHciDeploymentSettingScaleUnitInfrastructureNetworkList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.stackHciDeploymentSetting.StackHciDeploymentSettingScaleUnitInfrastructureNetworkList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc28e9f6ba0d69c19e8fe97ffcf0e17745987e07c2bbcb03394c0e26a512b488)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "StackHciDeploymentSettingScaleUnitInfrastructureNetworkOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e2326dd6048185a022223ba8cfc3098ce7bf33eb8d11c0a061da70099bdb184)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("StackHciDeploymentSettingScaleUnitInfrastructureNetworkOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf84c7696460a222013098d5a288669a7001a8f4ee3326db8845e5e625f434e0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6584c6c3e9d87d1d783e9a83fa12b921a63db66d37a7b4a724f23acf760fdca6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__584899b19ad3b5c80b2e212d8dd8967e9a2644beae7c061ed0022c2256e1b8f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StackHciDeploymentSettingScaleUnitInfrastructureNetwork]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StackHciDeploymentSettingScaleUnitInfrastructureNetwork]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StackHciDeploymentSettingScaleUnitInfrastructureNetwork]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50b9fdca3f5a196c9c86d03e7da43470c1a1be67db4b3422b401d2a594bb7584)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class StackHciDeploymentSettingScaleUnitInfrastructureNetworkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.stackHciDeploymentSetting.StackHciDeploymentSettingScaleUnitInfrastructureNetworkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__61515a8d2794dc36a39085239978fcded9bfed263224f8b4eaed99c654ca388b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putIpPool")
    def put_ip_pool(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StackHciDeploymentSettingScaleUnitInfrastructureNetworkIpPool, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__287836af6e83e86af1202b2f7b3af5d7a8d34c37cb9e0a20af6513951333b512)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIpPool", [value]))

    @jsii.member(jsii_name="resetDhcpEnabled")
    def reset_dhcp_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDhcpEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="ipPool")
    def ip_pool(
        self,
    ) -> StackHciDeploymentSettingScaleUnitInfrastructureNetworkIpPoolList:
        return typing.cast(StackHciDeploymentSettingScaleUnitInfrastructureNetworkIpPoolList, jsii.get(self, "ipPool"))

    @builtins.property
    @jsii.member(jsii_name="dhcpEnabledInput")
    def dhcp_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dhcpEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsServerInput")
    def dns_server_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dnsServerInput"))

    @builtins.property
    @jsii.member(jsii_name="gatewayInput")
    def gateway_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="ipPoolInput")
    def ip_pool_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StackHciDeploymentSettingScaleUnitInfrastructureNetworkIpPool]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StackHciDeploymentSettingScaleUnitInfrastructureNetworkIpPool]]], jsii.get(self, "ipPoolInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetMaskInput")
    def subnet_mask_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetMaskInput"))

    @builtins.property
    @jsii.member(jsii_name="dhcpEnabled")
    def dhcp_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dhcpEnabled"))

    @dhcp_enabled.setter
    def dhcp_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39594515f721205263607b4fb621c78df241f90c3cce3a2206b38d7848f882a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dhcpEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dnsServer")
    def dns_server(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dnsServer"))

    @dns_server.setter
    def dns_server(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab6e791bd8c8813df6a2e13abd61094c709b71146688118a5b0589b8d8a897f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsServer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gateway")
    def gateway(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gateway"))

    @gateway.setter
    def gateway(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__519ae112f835130232a0fb86a4b203ce9d9692fd214c7a07ce0019bef0c94970)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gateway", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetMask")
    def subnet_mask(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetMask"))

    @subnet_mask.setter
    def subnet_mask(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4edc9254f6847631f8e78bf7772c206f844cc0c82bb672083db899e4abc51a0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetMask", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StackHciDeploymentSettingScaleUnitInfrastructureNetwork]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StackHciDeploymentSettingScaleUnitInfrastructureNetwork]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StackHciDeploymentSettingScaleUnitInfrastructureNetwork]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c2a8a4b1d8f27348eaaa2337e3d2f2e682f78c44099a8f84abd883c9263f3cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class StackHciDeploymentSettingScaleUnitList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.stackHciDeploymentSetting.StackHciDeploymentSettingScaleUnitList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb593a54d3b86ba7b0480a86c7abf46e88d1812042092618b893865110dfe2c9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "StackHciDeploymentSettingScaleUnitOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44a9024468860f2770c8c9316ccc7b803d5e307037dd00e7151ce0a6eaea18e0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("StackHciDeploymentSettingScaleUnitOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a558142e922db6916ce5db66929c79781edbcef64b277e6fc027d34b21342507)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac1a16210243aa9d25825510a113c9eb02a4e1045c081c8368cd6829cb7af831)
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
            type_hints = typing.get_type_hints(_typecheckingstub__09767d49325ffcc9175247d5183bb687deaf883c2a3b75e19d0c78d0bd82e391)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StackHciDeploymentSettingScaleUnit]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StackHciDeploymentSettingScaleUnit]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StackHciDeploymentSettingScaleUnit]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e787b3f93077f87fb7a2b39b6d899cf676de6ee798d3479359268cde066b08b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.stackHciDeploymentSetting.StackHciDeploymentSettingScaleUnitOptionalService",
    jsii_struct_bases=[],
    name_mapping={"custom_location": "customLocation"},
)
class StackHciDeploymentSettingScaleUnitOptionalService:
    def __init__(self, *, custom_location: builtins.str) -> None:
        '''
        :param custom_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#custom_location StackHciDeploymentSetting#custom_location}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af1ed602c64045b9f36cdd88c3e591f7b4133f101a61bc623602c786638a1c05)
            check_type(argname="argument custom_location", value=custom_location, expected_type=type_hints["custom_location"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "custom_location": custom_location,
        }

    @builtins.property
    def custom_location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#custom_location StackHciDeploymentSetting#custom_location}.'''
        result = self._values.get("custom_location")
        assert result is not None, "Required property 'custom_location' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StackHciDeploymentSettingScaleUnitOptionalService(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StackHciDeploymentSettingScaleUnitOptionalServiceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.stackHciDeploymentSetting.StackHciDeploymentSettingScaleUnitOptionalServiceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b96103c464bd89b5c26d0305cde9ed20c95c85231d2fed95d25f43840d94cb5e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="customLocationInput")
    def custom_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="customLocation")
    def custom_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customLocation"))

    @custom_location.setter
    def custom_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbe84dbf7e34fa29f6177ee2bdbc124213d8cf31e1241c4a612fa602c117ee14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StackHciDeploymentSettingScaleUnitOptionalService]:
        return typing.cast(typing.Optional[StackHciDeploymentSettingScaleUnitOptionalService], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StackHciDeploymentSettingScaleUnitOptionalService],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e1288fb419f5abf48d19209a046f68cd9cedefe54d832524d182a417c1be02d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class StackHciDeploymentSettingScaleUnitOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.stackHciDeploymentSetting.StackHciDeploymentSettingScaleUnitOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__85ea498e978632a146d1ab4fa71fcd4ae8af8872a97c2094b70d56d6f7281d54)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCluster")
    def put_cluster(
        self,
        *,
        azure_service_endpoint: builtins.str,
        cloud_account_name: builtins.str,
        name: builtins.str,
        witness_path: builtins.str,
        witness_type: builtins.str,
    ) -> None:
        '''
        :param azure_service_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#azure_service_endpoint StackHciDeploymentSetting#azure_service_endpoint}.
        :param cloud_account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#cloud_account_name StackHciDeploymentSetting#cloud_account_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#name StackHciDeploymentSetting#name}.
        :param witness_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#witness_path StackHciDeploymentSetting#witness_path}.
        :param witness_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#witness_type StackHciDeploymentSetting#witness_type}.
        '''
        value = StackHciDeploymentSettingScaleUnitCluster(
            azure_service_endpoint=azure_service_endpoint,
            cloud_account_name=cloud_account_name,
            name=name,
            witness_path=witness_path,
            witness_type=witness_type,
        )

        return typing.cast(None, jsii.invoke(self, "putCluster", [value]))

    @jsii.member(jsii_name="putHostNetwork")
    def put_host_network(
        self,
        *,
        intent: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StackHciDeploymentSettingScaleUnitHostNetworkIntent, typing.Dict[builtins.str, typing.Any]]]],
        storage_network: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StackHciDeploymentSettingScaleUnitHostNetworkStorageNetwork, typing.Dict[builtins.str, typing.Any]]]],
        storage_auto_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        storage_connectivity_switchless_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param intent: intent block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#intent StackHciDeploymentSetting#intent}
        :param storage_network: storage_network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#storage_network StackHciDeploymentSetting#storage_network}
        :param storage_auto_ip_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#storage_auto_ip_enabled StackHciDeploymentSetting#storage_auto_ip_enabled}.
        :param storage_connectivity_switchless_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#storage_connectivity_switchless_enabled StackHciDeploymentSetting#storage_connectivity_switchless_enabled}.
        '''
        value = StackHciDeploymentSettingScaleUnitHostNetwork(
            intent=intent,
            storage_network=storage_network,
            storage_auto_ip_enabled=storage_auto_ip_enabled,
            storage_connectivity_switchless_enabled=storage_connectivity_switchless_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putHostNetwork", [value]))

    @jsii.member(jsii_name="putInfrastructureNetwork")
    def put_infrastructure_network(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StackHciDeploymentSettingScaleUnitInfrastructureNetwork, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41cb6220b64b6196275741cb5d32281162271c1f8bb7cc56c39d277273250d93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInfrastructureNetwork", [value]))

    @jsii.member(jsii_name="putOptionalService")
    def put_optional_service(self, *, custom_location: builtins.str) -> None:
        '''
        :param custom_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#custom_location StackHciDeploymentSetting#custom_location}.
        '''
        value = StackHciDeploymentSettingScaleUnitOptionalService(
            custom_location=custom_location
        )

        return typing.cast(None, jsii.invoke(self, "putOptionalService", [value]))

    @jsii.member(jsii_name="putPhysicalNode")
    def put_physical_node(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["StackHciDeploymentSettingScaleUnitPhysicalNode", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fbf23f4c0116e87405f9a87f3920c3581d4d6991fe8912602b82bb6f3bae1e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPhysicalNode", [value]))

    @jsii.member(jsii_name="putStorage")
    def put_storage(self, *, configuration_mode: builtins.str) -> None:
        '''
        :param configuration_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#configuration_mode StackHciDeploymentSetting#configuration_mode}.
        '''
        value = StackHciDeploymentSettingScaleUnitStorage(
            configuration_mode=configuration_mode
        )

        return typing.cast(None, jsii.invoke(self, "putStorage", [value]))

    @jsii.member(jsii_name="resetBitlockerBootVolumeEnabled")
    def reset_bitlocker_boot_volume_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBitlockerBootVolumeEnabled", []))

    @jsii.member(jsii_name="resetBitlockerDataVolumeEnabled")
    def reset_bitlocker_data_volume_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBitlockerDataVolumeEnabled", []))

    @jsii.member(jsii_name="resetCredentialGuardEnabled")
    def reset_credential_guard_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCredentialGuardEnabled", []))

    @jsii.member(jsii_name="resetDriftControlEnabled")
    def reset_drift_control_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDriftControlEnabled", []))

    @jsii.member(jsii_name="resetDrtmProtectionEnabled")
    def reset_drtm_protection_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDrtmProtectionEnabled", []))

    @jsii.member(jsii_name="resetEpisodicDataUploadEnabled")
    def reset_episodic_data_upload_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEpisodicDataUploadEnabled", []))

    @jsii.member(jsii_name="resetEuLocationEnabled")
    def reset_eu_location_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEuLocationEnabled", []))

    @jsii.member(jsii_name="resetHvciProtectionEnabled")
    def reset_hvci_protection_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHvciProtectionEnabled", []))

    @jsii.member(jsii_name="resetSideChannelMitigationEnabled")
    def reset_side_channel_mitigation_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSideChannelMitigationEnabled", []))

    @jsii.member(jsii_name="resetSmbClusterEncryptionEnabled")
    def reset_smb_cluster_encryption_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSmbClusterEncryptionEnabled", []))

    @jsii.member(jsii_name="resetSmbSigningEnabled")
    def reset_smb_signing_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSmbSigningEnabled", []))

    @jsii.member(jsii_name="resetStreamingDataClientEnabled")
    def reset_streaming_data_client_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStreamingDataClientEnabled", []))

    @jsii.member(jsii_name="resetWdacEnabled")
    def reset_wdac_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWdacEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> StackHciDeploymentSettingScaleUnitClusterOutputReference:
        return typing.cast(StackHciDeploymentSettingScaleUnitClusterOutputReference, jsii.get(self, "cluster"))

    @builtins.property
    @jsii.member(jsii_name="hostNetwork")
    def host_network(
        self,
    ) -> StackHciDeploymentSettingScaleUnitHostNetworkOutputReference:
        return typing.cast(StackHciDeploymentSettingScaleUnitHostNetworkOutputReference, jsii.get(self, "hostNetwork"))

    @builtins.property
    @jsii.member(jsii_name="infrastructureNetwork")
    def infrastructure_network(
        self,
    ) -> StackHciDeploymentSettingScaleUnitInfrastructureNetworkList:
        return typing.cast(StackHciDeploymentSettingScaleUnitInfrastructureNetworkList, jsii.get(self, "infrastructureNetwork"))

    @builtins.property
    @jsii.member(jsii_name="optionalService")
    def optional_service(
        self,
    ) -> StackHciDeploymentSettingScaleUnitOptionalServiceOutputReference:
        return typing.cast(StackHciDeploymentSettingScaleUnitOptionalServiceOutputReference, jsii.get(self, "optionalService"))

    @builtins.property
    @jsii.member(jsii_name="physicalNode")
    def physical_node(self) -> "StackHciDeploymentSettingScaleUnitPhysicalNodeList":
        return typing.cast("StackHciDeploymentSettingScaleUnitPhysicalNodeList", jsii.get(self, "physicalNode"))

    @builtins.property
    @jsii.member(jsii_name="storage")
    def storage(self) -> "StackHciDeploymentSettingScaleUnitStorageOutputReference":
        return typing.cast("StackHciDeploymentSettingScaleUnitStorageOutputReference", jsii.get(self, "storage"))

    @builtins.property
    @jsii.member(jsii_name="activeDirectoryOrganizationalUnitPathInput")
    def active_directory_organizational_unit_path_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "activeDirectoryOrganizationalUnitPathInput"))

    @builtins.property
    @jsii.member(jsii_name="bitlockerBootVolumeEnabledInput")
    def bitlocker_boot_volume_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "bitlockerBootVolumeEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="bitlockerDataVolumeEnabledInput")
    def bitlocker_data_volume_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "bitlockerDataVolumeEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterInput")
    def cluster_input(
        self,
    ) -> typing.Optional[StackHciDeploymentSettingScaleUnitCluster]:
        return typing.cast(typing.Optional[StackHciDeploymentSettingScaleUnitCluster], jsii.get(self, "clusterInput"))

    @builtins.property
    @jsii.member(jsii_name="credentialGuardEnabledInput")
    def credential_guard_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "credentialGuardEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="domainFqdnInput")
    def domain_fqdn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainFqdnInput"))

    @builtins.property
    @jsii.member(jsii_name="driftControlEnabledInput")
    def drift_control_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "driftControlEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="drtmProtectionEnabledInput")
    def drtm_protection_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "drtmProtectionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="episodicDataUploadEnabledInput")
    def episodic_data_upload_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "episodicDataUploadEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="euLocationEnabledInput")
    def eu_location_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "euLocationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="hostNetworkInput")
    def host_network_input(
        self,
    ) -> typing.Optional[StackHciDeploymentSettingScaleUnitHostNetwork]:
        return typing.cast(typing.Optional[StackHciDeploymentSettingScaleUnitHostNetwork], jsii.get(self, "hostNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="hvciProtectionEnabledInput")
    def hvci_protection_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "hvciProtectionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="infrastructureNetworkInput")
    def infrastructure_network_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StackHciDeploymentSettingScaleUnitInfrastructureNetwork]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StackHciDeploymentSettingScaleUnitInfrastructureNetwork]]], jsii.get(self, "infrastructureNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="namePrefixInput")
    def name_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namePrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="optionalServiceInput")
    def optional_service_input(
        self,
    ) -> typing.Optional[StackHciDeploymentSettingScaleUnitOptionalService]:
        return typing.cast(typing.Optional[StackHciDeploymentSettingScaleUnitOptionalService], jsii.get(self, "optionalServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="physicalNodeInput")
    def physical_node_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StackHciDeploymentSettingScaleUnitPhysicalNode"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StackHciDeploymentSettingScaleUnitPhysicalNode"]]], jsii.get(self, "physicalNodeInput"))

    @builtins.property
    @jsii.member(jsii_name="secretsLocationInput")
    def secrets_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretsLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="sideChannelMitigationEnabledInput")
    def side_channel_mitigation_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sideChannelMitigationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="smbClusterEncryptionEnabledInput")
    def smb_cluster_encryption_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "smbClusterEncryptionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="smbSigningEnabledInput")
    def smb_signing_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "smbSigningEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="storageInput")
    def storage_input(
        self,
    ) -> typing.Optional["StackHciDeploymentSettingScaleUnitStorage"]:
        return typing.cast(typing.Optional["StackHciDeploymentSettingScaleUnitStorage"], jsii.get(self, "storageInput"))

    @builtins.property
    @jsii.member(jsii_name="streamingDataClientEnabledInput")
    def streaming_data_client_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "streamingDataClientEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="wdacEnabledInput")
    def wdac_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "wdacEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="activeDirectoryOrganizationalUnitPath")
    def active_directory_organizational_unit_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "activeDirectoryOrganizationalUnitPath"))

    @active_directory_organizational_unit_path.setter
    def active_directory_organizational_unit_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50eed12517257c89b937ccc9a258ee4394bdb08229e00d77ebc148b329042192)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "activeDirectoryOrganizationalUnitPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bitlockerBootVolumeEnabled")
    def bitlocker_boot_volume_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "bitlockerBootVolumeEnabled"))

    @bitlocker_boot_volume_enabled.setter
    def bitlocker_boot_volume_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9208a94daa223bf0112c75b2a664ca9d654881fb2bd8a819703afa26b07416d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bitlockerBootVolumeEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bitlockerDataVolumeEnabled")
    def bitlocker_data_volume_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "bitlockerDataVolumeEnabled"))

    @bitlocker_data_volume_enabled.setter
    def bitlocker_data_volume_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e6957051f9f7f93d6c35f3591eeeed9e191d5070ddbd828e39d838db4d81688)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bitlockerDataVolumeEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="credentialGuardEnabled")
    def credential_guard_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "credentialGuardEnabled"))

    @credential_guard_enabled.setter
    def credential_guard_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf63dbdf0aa7d28fe9d877d5846c4418ce5ce1a9b206fa97dec959d55d5ff532)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "credentialGuardEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainFqdn")
    def domain_fqdn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainFqdn"))

    @domain_fqdn.setter
    def domain_fqdn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bb7fbd7c74933e6bade76d819264f3703d47c0d160faf56313fb255bf08c6de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainFqdn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="driftControlEnabled")
    def drift_control_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "driftControlEnabled"))

    @drift_control_enabled.setter
    def drift_control_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3af221553016938362c22842e02e52d6ba80b232cfe87b8325a43d426389f32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "driftControlEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="drtmProtectionEnabled")
    def drtm_protection_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "drtmProtectionEnabled"))

    @drtm_protection_enabled.setter
    def drtm_protection_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcc7603934b75457003dd3f97b68b043787ea42ce900d2d94a5fd4345724c7ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "drtmProtectionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="episodicDataUploadEnabled")
    def episodic_data_upload_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "episodicDataUploadEnabled"))

    @episodic_data_upload_enabled.setter
    def episodic_data_upload_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f4b39626af565723d61efb3da11cd442b4f2044f66c32e46c3e2f7287060379)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "episodicDataUploadEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="euLocationEnabled")
    def eu_location_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "euLocationEnabled"))

    @eu_location_enabled.setter
    def eu_location_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8cd9fe8ffe833a9b483280b89ca12bf245a701294faa02bf9f4d9b597316a37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "euLocationEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hvciProtectionEnabled")
    def hvci_protection_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "hvciProtectionEnabled"))

    @hvci_protection_enabled.setter
    def hvci_protection_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0624b19bce84ef1f77ce5a34cd6887e0bbb929222764b243f1545d2eab49db78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hvciProtectionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namePrefix")
    def name_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namePrefix"))

    @name_prefix.setter
    def name_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99498eba2254771dbbc72edefba2dffe05293ccb3d0842eeff2bac340cb18517)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namePrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretsLocation")
    def secrets_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretsLocation"))

    @secrets_location.setter
    def secrets_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd0af9bb5713833e3581dea425ec6470fd1015d16e1d13c693f4eca68ec3b158)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretsLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sideChannelMitigationEnabled")
    def side_channel_mitigation_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sideChannelMitigationEnabled"))

    @side_channel_mitigation_enabled.setter
    def side_channel_mitigation_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d10644fca8971e77f889b5e1947fcd8db944bb6338603df10975e04548cf2a74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sideChannelMitigationEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="smbClusterEncryptionEnabled")
    def smb_cluster_encryption_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "smbClusterEncryptionEnabled"))

    @smb_cluster_encryption_enabled.setter
    def smb_cluster_encryption_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a22aee7182da38b6fadc48042f8ede7db719c888ec304d64a081de8a361cc2e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "smbClusterEncryptionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="smbSigningEnabled")
    def smb_signing_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "smbSigningEnabled"))

    @smb_signing_enabled.setter
    def smb_signing_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16b32a4a1846194a2f99a57d7b658dd69b7c1714bdfe190b8862a8ef91bfcac8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "smbSigningEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="streamingDataClientEnabled")
    def streaming_data_client_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "streamingDataClientEnabled"))

    @streaming_data_client_enabled.setter
    def streaming_data_client_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8eeaf698d05adba024666f1975b0709599e1c33280ebc9c58bdc8616bb10c50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streamingDataClientEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wdacEnabled")
    def wdac_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "wdacEnabled"))

    @wdac_enabled.setter
    def wdac_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72ceaedfa834e0103689cd5ade65831651063b821240738bd367387f4bdf4d1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wdacEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StackHciDeploymentSettingScaleUnit]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StackHciDeploymentSettingScaleUnit]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StackHciDeploymentSettingScaleUnit]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64633266558e4c792b8b398ed58dfa8beb37981b8d768d6b343b6dc5fb8dafda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.stackHciDeploymentSetting.StackHciDeploymentSettingScaleUnitPhysicalNode",
    jsii_struct_bases=[],
    name_mapping={"ipv4_address": "ipv4Address", "name": "name"},
)
class StackHciDeploymentSettingScaleUnitPhysicalNode:
    def __init__(self, *, ipv4_address: builtins.str, name: builtins.str) -> None:
        '''
        :param ipv4_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#ipv4_address StackHciDeploymentSetting#ipv4_address}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#name StackHciDeploymentSetting#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edb552175e461323ab76a40476f4a648b1d6e4d298d475b4b5f23e86602f2377)
            check_type(argname="argument ipv4_address", value=ipv4_address, expected_type=type_hints["ipv4_address"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ipv4_address": ipv4_address,
            "name": name,
        }

    @builtins.property
    def ipv4_address(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#ipv4_address StackHciDeploymentSetting#ipv4_address}.'''
        result = self._values.get("ipv4_address")
        assert result is not None, "Required property 'ipv4_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#name StackHciDeploymentSetting#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StackHciDeploymentSettingScaleUnitPhysicalNode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StackHciDeploymentSettingScaleUnitPhysicalNodeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.stackHciDeploymentSetting.StackHciDeploymentSettingScaleUnitPhysicalNodeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0f48fe216fbdaab3e15fc7cbefa7b2370299022ccae37b1163fbcbe9e1a8685)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "StackHciDeploymentSettingScaleUnitPhysicalNodeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acfb70ceecb57d5a3940202e70641cb78dbafa01045fb81f3c94e4b82010b34e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("StackHciDeploymentSettingScaleUnitPhysicalNodeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0759aaff0c16464d4692f1741d6668d5a9ceb62dcdde2b2bf54b7670aadfbba8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__78c90112129a3c1b67c8b3087377e628a0eb0fba3cc86a2c141daaadc04137c5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b89226affea50f8850b564fe3f999b53955cac28d47e963b3245b8d8dfd4d2d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StackHciDeploymentSettingScaleUnitPhysicalNode]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StackHciDeploymentSettingScaleUnitPhysicalNode]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StackHciDeploymentSettingScaleUnitPhysicalNode]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82435128621ebdb2d04b386334ab5d4ff52922c757b55013e77de748016b5340)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class StackHciDeploymentSettingScaleUnitPhysicalNodeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.stackHciDeploymentSetting.StackHciDeploymentSettingScaleUnitPhysicalNodeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__248c0470ab51762f1eebc5fb940a2fddbcbb40d2388cb41808f2ca7b83944595)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="ipv4AddressInput")
    def ipv4_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipv4AddressInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="ipv4Address")
    def ipv4_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv4Address"))

    @ipv4_address.setter
    def ipv4_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__654a7afeaf2ab3f416b56d73e0912da628f9c80e3ca01d5e711eceba5af0f599)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv4Address", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11ebbfe1cc27bd14d3ebae6a2913579dc3906cbfb3e4ebf6c066565c954720c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StackHciDeploymentSettingScaleUnitPhysicalNode]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StackHciDeploymentSettingScaleUnitPhysicalNode]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StackHciDeploymentSettingScaleUnitPhysicalNode]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64a88b07e17cc6f49af5ee4a95e7913e7d8db0e82c1194f3c03bdcad049b91f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.stackHciDeploymentSetting.StackHciDeploymentSettingScaleUnitStorage",
    jsii_struct_bases=[],
    name_mapping={"configuration_mode": "configurationMode"},
)
class StackHciDeploymentSettingScaleUnitStorage:
    def __init__(self, *, configuration_mode: builtins.str) -> None:
        '''
        :param configuration_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#configuration_mode StackHciDeploymentSetting#configuration_mode}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb573095c1a549e7585f69edb911e79be37cdf47af10818fb63343f759d81058)
            check_type(argname="argument configuration_mode", value=configuration_mode, expected_type=type_hints["configuration_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "configuration_mode": configuration_mode,
        }

    @builtins.property
    def configuration_mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#configuration_mode StackHciDeploymentSetting#configuration_mode}.'''
        result = self._values.get("configuration_mode")
        assert result is not None, "Required property 'configuration_mode' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StackHciDeploymentSettingScaleUnitStorage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StackHciDeploymentSettingScaleUnitStorageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.stackHciDeploymentSetting.StackHciDeploymentSettingScaleUnitStorageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dfb4a5fd20fef9193206219d70854812629f5d3bbb7d8ee99db35ab6a64af430)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="configurationModeInput")
    def configuration_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "configurationModeInput"))

    @builtins.property
    @jsii.member(jsii_name="configurationMode")
    def configuration_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "configurationMode"))

    @configuration_mode.setter
    def configuration_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a06ef5db010903e02dabc7e28891555e9eab9a417da8a04d79aee7adb755944)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configurationMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StackHciDeploymentSettingScaleUnitStorage]:
        return typing.cast(typing.Optional[StackHciDeploymentSettingScaleUnitStorage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StackHciDeploymentSettingScaleUnitStorage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59c62daf80bee5f6b2ffb4671efc1538acfb6024c93456300caae2f1939226fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.stackHciDeploymentSetting.StackHciDeploymentSettingTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "read": "read"},
)
class StackHciDeploymentSettingTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#create StackHciDeploymentSetting#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#delete StackHciDeploymentSetting#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#read StackHciDeploymentSetting#read}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__047f2974a6fb8838efc484f709163e4fd7bead10bc42a57705daf3420fb903e9)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#create StackHciDeploymentSetting#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#delete StackHciDeploymentSetting#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/stack_hci_deployment_setting#read StackHciDeploymentSetting#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StackHciDeploymentSettingTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StackHciDeploymentSettingTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.stackHciDeploymentSetting.StackHciDeploymentSettingTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__57b752473df945c25cee0f77418e51fb52c5341a086e5c2f7c163054ce749e8c)
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
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19f7db84c799a71b2fdc6d83b90aa976898a6b09f84a4b77ced1b10c658b8e89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffd93742d7ce5dda253922f199eeaaa62dc8228ed08632b612e1619ad5b62e74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c75cc25283db74fbced3a326de2a90485ff60b783c749ab43495f25bbba454d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StackHciDeploymentSettingTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StackHciDeploymentSettingTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StackHciDeploymentSettingTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67bcaaf5ea8733f154d18f434544eb1457b484ddeda9a592354dfeb3b5f3760a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "StackHciDeploymentSetting",
    "StackHciDeploymentSettingConfig",
    "StackHciDeploymentSettingScaleUnit",
    "StackHciDeploymentSettingScaleUnitCluster",
    "StackHciDeploymentSettingScaleUnitClusterOutputReference",
    "StackHciDeploymentSettingScaleUnitHostNetwork",
    "StackHciDeploymentSettingScaleUnitHostNetworkIntent",
    "StackHciDeploymentSettingScaleUnitHostNetworkIntentAdapterPropertyOverride",
    "StackHciDeploymentSettingScaleUnitHostNetworkIntentAdapterPropertyOverrideOutputReference",
    "StackHciDeploymentSettingScaleUnitHostNetworkIntentList",
    "StackHciDeploymentSettingScaleUnitHostNetworkIntentOutputReference",
    "StackHciDeploymentSettingScaleUnitHostNetworkIntentQosPolicyOverride",
    "StackHciDeploymentSettingScaleUnitHostNetworkIntentQosPolicyOverrideOutputReference",
    "StackHciDeploymentSettingScaleUnitHostNetworkIntentVirtualSwitchConfigurationOverride",
    "StackHciDeploymentSettingScaleUnitHostNetworkIntentVirtualSwitchConfigurationOverrideOutputReference",
    "StackHciDeploymentSettingScaleUnitHostNetworkOutputReference",
    "StackHciDeploymentSettingScaleUnitHostNetworkStorageNetwork",
    "StackHciDeploymentSettingScaleUnitHostNetworkStorageNetworkList",
    "StackHciDeploymentSettingScaleUnitHostNetworkStorageNetworkOutputReference",
    "StackHciDeploymentSettingScaleUnitInfrastructureNetwork",
    "StackHciDeploymentSettingScaleUnitInfrastructureNetworkIpPool",
    "StackHciDeploymentSettingScaleUnitInfrastructureNetworkIpPoolList",
    "StackHciDeploymentSettingScaleUnitInfrastructureNetworkIpPoolOutputReference",
    "StackHciDeploymentSettingScaleUnitInfrastructureNetworkList",
    "StackHciDeploymentSettingScaleUnitInfrastructureNetworkOutputReference",
    "StackHciDeploymentSettingScaleUnitList",
    "StackHciDeploymentSettingScaleUnitOptionalService",
    "StackHciDeploymentSettingScaleUnitOptionalServiceOutputReference",
    "StackHciDeploymentSettingScaleUnitOutputReference",
    "StackHciDeploymentSettingScaleUnitPhysicalNode",
    "StackHciDeploymentSettingScaleUnitPhysicalNodeList",
    "StackHciDeploymentSettingScaleUnitPhysicalNodeOutputReference",
    "StackHciDeploymentSettingScaleUnitStorage",
    "StackHciDeploymentSettingScaleUnitStorageOutputReference",
    "StackHciDeploymentSettingTimeouts",
    "StackHciDeploymentSettingTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__5bda13f15368304cfc1ec40ba110edf0213facc845478e273e35bd3d8a476d8c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    arc_resource_ids: typing.Sequence[builtins.str],
    scale_unit: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StackHciDeploymentSettingScaleUnit, typing.Dict[builtins.str, typing.Any]]]],
    stack_hci_cluster_id: builtins.str,
    version: builtins.str,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[StackHciDeploymentSettingTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__93074f80ac18130f8a4e941e67bbc04ad5f738054a7b75b7634d63d9ed067e5f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5cb11028dcdd68f6ce02aa2712ef3b461debcb56a7f55323fc409f202efb245(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StackHciDeploymentSettingScaleUnit, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__290298f24114f8352fda965a19094cfbf567c6f7cc6c9ec85630d407f30f6fd5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeed5f338b740c9f9960c94c09038d80ebc54bbf2b58353b1d8e9f89d74001f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b91d7cdd987d8054bc5bddbc6f6db4cb21442fcae31fa9bf0e3b25c19019956d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77bc36cb8f63c1871bd883ab138a36f9629ac8d6f3e68a59ba7d42e42d7cb905(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8e0ff3a4dca8b3481b393ecf29d994e8a03949e433bc6640410dcbd99d8e1c5(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    arc_resource_ids: typing.Sequence[builtins.str],
    scale_unit: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StackHciDeploymentSettingScaleUnit, typing.Dict[builtins.str, typing.Any]]]],
    stack_hci_cluster_id: builtins.str,
    version: builtins.str,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[StackHciDeploymentSettingTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa88e9c8da993f3f649ecdb496c64fe4aca298df4e82aade26572601549b976b(
    *,
    active_directory_organizational_unit_path: builtins.str,
    cluster: typing.Union[StackHciDeploymentSettingScaleUnitCluster, typing.Dict[builtins.str, typing.Any]],
    domain_fqdn: builtins.str,
    host_network: typing.Union[StackHciDeploymentSettingScaleUnitHostNetwork, typing.Dict[builtins.str, typing.Any]],
    infrastructure_network: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StackHciDeploymentSettingScaleUnitInfrastructureNetwork, typing.Dict[builtins.str, typing.Any]]]],
    name_prefix: builtins.str,
    optional_service: typing.Union[StackHciDeploymentSettingScaleUnitOptionalService, typing.Dict[builtins.str, typing.Any]],
    physical_node: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StackHciDeploymentSettingScaleUnitPhysicalNode, typing.Dict[builtins.str, typing.Any]]]],
    secrets_location: builtins.str,
    storage: typing.Union[StackHciDeploymentSettingScaleUnitStorage, typing.Dict[builtins.str, typing.Any]],
    bitlocker_boot_volume_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    bitlocker_data_volume_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    credential_guard_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    drift_control_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    drtm_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    episodic_data_upload_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    eu_location_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hvci_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    side_channel_mitigation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    smb_cluster_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    smb_signing_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    streaming_data_client_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    wdac_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5981d76b1d4543edeb2371fc6b301d293099ae1c2067e11a415e948b7e8af897(
    *,
    azure_service_endpoint: builtins.str,
    cloud_account_name: builtins.str,
    name: builtins.str,
    witness_path: builtins.str,
    witness_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__022da8a5881bb52c8970d612ba9367fdaed82f12c4cd41c39905e2aca9c421d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d025b201c66bcdeaa554369149abe4f07ee763a460440183fae2fdb12c64aa5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beea3fc2fc2acaf52359fe5767f33305a36f52939ca65ab5fa42ad76a236c80c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0049547cdd24a9ae8db7dc28ae35cb56e02b0bd277b3c740b35fa026f822e451(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33450096beee92da7ecb97f3579c5d4a83ef42e326fd7da66080c363b42f1e61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99e2f98cc66e7c074e02bf2ebe157b8de3011e4c4118d4e9d3d5b3a336d20218(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcf02ac1bb0e1ddea9249fddd4d93f382bbab03a036dc7fb74850d02cc7a00ea(
    value: typing.Optional[StackHciDeploymentSettingScaleUnitCluster],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc71bd211a9ca565a92b4c7d1dedb4002605becf38cc3e4ca422fcbff54269e4(
    *,
    intent: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StackHciDeploymentSettingScaleUnitHostNetworkIntent, typing.Dict[builtins.str, typing.Any]]]],
    storage_network: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StackHciDeploymentSettingScaleUnitHostNetworkStorageNetwork, typing.Dict[builtins.str, typing.Any]]]],
    storage_auto_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    storage_connectivity_switchless_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00815a283e091ea35fbff56392dafa835468319ccbedb5c3b950f3730daae635(
    *,
    adapter: typing.Sequence[builtins.str],
    name: builtins.str,
    traffic_type: typing.Sequence[builtins.str],
    adapter_property_override: typing.Optional[typing.Union[StackHciDeploymentSettingScaleUnitHostNetworkIntentAdapterPropertyOverride, typing.Dict[builtins.str, typing.Any]]] = None,
    adapter_property_override_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    qos_policy_override: typing.Optional[typing.Union[StackHciDeploymentSettingScaleUnitHostNetworkIntentQosPolicyOverride, typing.Dict[builtins.str, typing.Any]]] = None,
    qos_policy_override_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    virtual_switch_configuration_override: typing.Optional[typing.Union[StackHciDeploymentSettingScaleUnitHostNetworkIntentVirtualSwitchConfigurationOverride, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_switch_configuration_override_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44a45f532c90cdd76480e7cf99729e0e60da82bdf9983beb0d019b3ce1a7e227(
    *,
    jumbo_packet: typing.Optional[builtins.str] = None,
    network_direct: typing.Optional[builtins.str] = None,
    network_direct_technology: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcacd2fa801cb29b2c682fb1b033375fd96b6ace058dfe61ee9401d840ee803e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da0a954571584d40dd9b92e191759c2bad0724ef8a1572071dbec9a0641747ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acf2fa4ecc516c5aef78ae75495d4e7b574224def3eaac9e3fbedf98bb4fe4ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b88cad996d331039a43c3b670914f20713a69097b0e5bb3dd039965a332306b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__691b90666b156aae3964aaac81d3e156aa3518bd545bf60c7002bc118b3f02d3(
    value: typing.Optional[StackHciDeploymentSettingScaleUnitHostNetworkIntentAdapterPropertyOverride],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__525c3e3686906ef069331f2b588e398738ced49ee1963706a5669e629d4bb3ed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9161507eab2b4b950ac2f0262e84b0a4872cffdf370e30a28e13fc4d7ba2ee0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57ecd506d132e099265d4868cde82760e25cfed59ef3cc5e392c7d9257fa14b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c3e3ed94b5b4f83c582caeef4e7de0bdb835df6196d44f26952f789e81c4594(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad136bf619c0a1518813897058bebba5f4dacec2c2111ad96d72c29ad5ea1180(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d29bb2540f1fe427d7754b615c96746698810a2aa0438a6d7d84bc1f4020403c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StackHciDeploymentSettingScaleUnitHostNetworkIntent]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__743fb4d1b7641a77097bbf456c2ec0796c914eeffc0fea40879baccada89fcf2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3d312bdc66706132f747129e2047a07c40cb1f0e26ec67822f63cc0948be8cc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__731f5633aae2338037f001ae14c10bad743ea98a4e9e123ab307f13530654aa6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85d4d030ccf379d2bad645226681dfec4429e2b0bbc9d72bf00d568da2d620ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fc6db1a24023462d4c83f5dee3077204dad4ee53e0f17455a34bcd756b26ee1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a893356e9b83a678a052f73d68b516c9664a467762efc1d03d552857419866bb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2456baecb1cde83d0f40e564ca0d92db03ffabbd652ded5481f5e9a05cb1fb17(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc079b04ecec38f4f59d4dd1f05112f9281efe0ee01eb1c6615ffc13a7fe2333(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StackHciDeploymentSettingScaleUnitHostNetworkIntent]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95231d03870f48168995cc2dd94b625fc76040ad2cfdfe7fb7f9ce4ebdf1cb36(
    *,
    bandwidth_percentage_smb: typing.Optional[builtins.str] = None,
    priority_value8021_action_cluster: typing.Optional[builtins.str] = None,
    priority_value8021_action_smb: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86868a2f428f26deaff4aaccef763d8808e5b8d8cc5879b807c397622f74c8b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc922b09388af2943eb66fdd255833e0e8e5e6a02c2fddf517ca55052415c4c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b2d3ebab4679717fe8a64db2c6aa2401e5d96d07ff76c4fcd3a54d40e0592db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__173f2326c07a1e9bfea04d906cb28eec0bb483c98132d022cc572367d0296e23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c282b78b191ceed89307c30bc790372a892bc699aa92dadbea91bb217ac812df(
    value: typing.Optional[StackHciDeploymentSettingScaleUnitHostNetworkIntentQosPolicyOverride],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92c09917f8d674c18c9b80152eff42e2519e95de4aaad01234a65de7488d0e27(
    *,
    enable_iov: typing.Optional[builtins.str] = None,
    load_balancing_algorithm: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36eff91940f925f14754357a3b832bcb29947089b1dcdc0c09fa56efdfc32a0a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4ff9dbbb9b2a5d5a8fcadb1da254d21e485cab1daf8fa534398fb2a37f491ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad1ff031c18974e980bedc6373376df8c0943c1f551243fc72845fbef6e6d0b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5602214d3a0ca4bd15a7ff434b9c99bacffe593829bd7ace8600735b8e790009(
    value: typing.Optional[StackHciDeploymentSettingScaleUnitHostNetworkIntentVirtualSwitchConfigurationOverride],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75ab6826e3196cea0542ee54c24441ad6db11d73f5fa50e97c69dab495af0e8b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fe9cda1e7b9407fa867b1b60c9e7866f8920c9e268b147f7509aab6818e7128(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StackHciDeploymentSettingScaleUnitHostNetworkIntent, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b87e1f1cb0a20e04a72b86d32878eadc3cf3aa16e86ae7ac831dacdf84bb949(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StackHciDeploymentSettingScaleUnitHostNetworkStorageNetwork, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3ac8a0d6fe5534bf9a9a8f9c462cfd7cc96ff1c20cfd1c9de6df158ea43c718(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbf1379b64d7328385d32948f8da2f444f17cef576e74f5bc4f34e3d160314a1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd2a7f98ab0fa7e53cfdff600f8ffb69b35b88e0ac6668228c0da55b379617fe(
    value: typing.Optional[StackHciDeploymentSettingScaleUnitHostNetwork],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d10a12e0918f485a854f54e6cb30a396b21a79c95bbcbcbec9213b512d45c358(
    *,
    name: builtins.str,
    network_adapter_name: builtins.str,
    vlan_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__264c8bad7b99a4f63c947f4f8d2087c9dd7396f60e45de176a706adbdd058adc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee0b19225087877e59cf9d24e18155de3a81d05b4a323476dce6b4f9af62ed4a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dd03d7a0e864d97d0db8d396489f51dc800d1467d2fc7eca2cdd1190eda6e2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42e50eeaa90c5e49b8aab9c975d010ff4efd8785f432eb3212d9399d163f25ba(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d58feef1fcaf8784024289427abea4c5e3441d21dbb77bc2de393ec18243fd8a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb5eba85e3b8931f293af5840b02627d27a048223413a3dbbcf6e13d76c7e9a7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StackHciDeploymentSettingScaleUnitHostNetworkStorageNetwork]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e9be8d88b47e24b760d53914cb29201ba657afa443b8233d4e4ce4eadfd26ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aa5d2928a1dc5bc0726e806054e2ea929f143470d0deae7551f1a911576c78e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__496dd2c1157a9a825d36281d6b62c54e2554c787be45dbc08868693a73e11e3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dd9080ee04e631a20cf3fd1e0522da5c24b565c8cb6fab72f7e79d61fb39228(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89b4ac5acd17d60fc7813962496ec8bebf1f5396a66900e8cb7aee59c01db5c2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StackHciDeploymentSettingScaleUnitHostNetworkStorageNetwork]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69dea3c8324a77a29903ff53f89cf34424370f0476890d0a449b6993979e1b6f(
    *,
    dns_server: typing.Sequence[builtins.str],
    gateway: builtins.str,
    ip_pool: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StackHciDeploymentSettingScaleUnitInfrastructureNetworkIpPool, typing.Dict[builtins.str, typing.Any]]]],
    subnet_mask: builtins.str,
    dhcp_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17837551bf9943c49df86e838a86593520b16fe62c03669319865dd8feebecd3(
    *,
    ending_address: builtins.str,
    starting_address: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__523b1bba340a4419e1141d6959cabde1bbdd4cf6403ffaeba34f4ba354330398(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89de318c66637bca999c4f4b5167c79f66001249fbf4df822ea024fa2685ec6f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e0eaba0ea4dff49396fa2f9ac9976a9b5a19aeace46809ab9227c11a3ae6fa0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a0da4904b7ad8ce72a19c7afd668b51b30fd190ab983e85f4b274e63bd1757d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63e5c0c1902ea7a2502419b52dda890bdd8c1e923361062966b6e5135a3514b8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3f6a9b61219cf3ed78a58e3d1277c6e5a129cba0568ad182ee58592d590a134(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StackHciDeploymentSettingScaleUnitInfrastructureNetworkIpPool]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b67fa274012a1b7c3c541347abd869c2f5994140c3dae31cd7b02cc605f3a6a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff0f1e91e5eda0438895d6a7ae81ff45ce8816bd6c55c7aa40ba5b0eed3529ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d22e5d1d551aa989a1f41a98281c044ed173f29d2a9d4abf75eff7bb5d4eaa3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c80f8104cdded28b351c27ce10efff748d7ed3fa36d0edc0f9e447950b9bf69c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StackHciDeploymentSettingScaleUnitInfrastructureNetworkIpPool]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc28e9f6ba0d69c19e8fe97ffcf0e17745987e07c2bbcb03394c0e26a512b488(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e2326dd6048185a022223ba8cfc3098ce7bf33eb8d11c0a061da70099bdb184(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf84c7696460a222013098d5a288669a7001a8f4ee3326db8845e5e625f434e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6584c6c3e9d87d1d783e9a83fa12b921a63db66d37a7b4a724f23acf760fdca6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__584899b19ad3b5c80b2e212d8dd8967e9a2644beae7c061ed0022c2256e1b8f2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50b9fdca3f5a196c9c86d03e7da43470c1a1be67db4b3422b401d2a594bb7584(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StackHciDeploymentSettingScaleUnitInfrastructureNetwork]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61515a8d2794dc36a39085239978fcded9bfed263224f8b4eaed99c654ca388b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__287836af6e83e86af1202b2f7b3af5d7a8d34c37cb9e0a20af6513951333b512(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StackHciDeploymentSettingScaleUnitInfrastructureNetworkIpPool, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39594515f721205263607b4fb621c78df241f90c3cce3a2206b38d7848f882a5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab6e791bd8c8813df6a2e13abd61094c709b71146688118a5b0589b8d8a897f3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__519ae112f835130232a0fb86a4b203ce9d9692fd214c7a07ce0019bef0c94970(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4edc9254f6847631f8e78bf7772c206f844cc0c82bb672083db899e4abc51a0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c2a8a4b1d8f27348eaaa2337e3d2f2e682f78c44099a8f84abd883c9263f3cc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StackHciDeploymentSettingScaleUnitInfrastructureNetwork]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb593a54d3b86ba7b0480a86c7abf46e88d1812042092618b893865110dfe2c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44a9024468860f2770c8c9316ccc7b803d5e307037dd00e7151ce0a6eaea18e0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a558142e922db6916ce5db66929c79781edbcef64b277e6fc027d34b21342507(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac1a16210243aa9d25825510a113c9eb02a4e1045c081c8368cd6829cb7af831(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09767d49325ffcc9175247d5183bb687deaf883c2a3b75e19d0c78d0bd82e391(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e787b3f93077f87fb7a2b39b6d899cf676de6ee798d3479359268cde066b08b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StackHciDeploymentSettingScaleUnit]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af1ed602c64045b9f36cdd88c3e591f7b4133f101a61bc623602c786638a1c05(
    *,
    custom_location: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b96103c464bd89b5c26d0305cde9ed20c95c85231d2fed95d25f43840d94cb5e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbe84dbf7e34fa29f6177ee2bdbc124213d8cf31e1241c4a612fa602c117ee14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e1288fb419f5abf48d19209a046f68cd9cedefe54d832524d182a417c1be02d(
    value: typing.Optional[StackHciDeploymentSettingScaleUnitOptionalService],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85ea498e978632a146d1ab4fa71fcd4ae8af8872a97c2094b70d56d6f7281d54(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41cb6220b64b6196275741cb5d32281162271c1f8bb7cc56c39d277273250d93(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StackHciDeploymentSettingScaleUnitInfrastructureNetwork, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fbf23f4c0116e87405f9a87f3920c3581d4d6991fe8912602b82bb6f3bae1e3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StackHciDeploymentSettingScaleUnitPhysicalNode, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50eed12517257c89b937ccc9a258ee4394bdb08229e00d77ebc148b329042192(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9208a94daa223bf0112c75b2a664ca9d654881fb2bd8a819703afa26b07416d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e6957051f9f7f93d6c35f3591eeeed9e191d5070ddbd828e39d838db4d81688(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf63dbdf0aa7d28fe9d877d5846c4418ce5ce1a9b206fa97dec959d55d5ff532(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bb7fbd7c74933e6bade76d819264f3703d47c0d160faf56313fb255bf08c6de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3af221553016938362c22842e02e52d6ba80b232cfe87b8325a43d426389f32(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcc7603934b75457003dd3f97b68b043787ea42ce900d2d94a5fd4345724c7ab(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f4b39626af565723d61efb3da11cd442b4f2044f66c32e46c3e2f7287060379(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8cd9fe8ffe833a9b483280b89ca12bf245a701294faa02bf9f4d9b597316a37(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0624b19bce84ef1f77ce5a34cd6887e0bbb929222764b243f1545d2eab49db78(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99498eba2254771dbbc72edefba2dffe05293ccb3d0842eeff2bac340cb18517(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd0af9bb5713833e3581dea425ec6470fd1015d16e1d13c693f4eca68ec3b158(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d10644fca8971e77f889b5e1947fcd8db944bb6338603df10975e04548cf2a74(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a22aee7182da38b6fadc48042f8ede7db719c888ec304d64a081de8a361cc2e5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16b32a4a1846194a2f99a57d7b658dd69b7c1714bdfe190b8862a8ef91bfcac8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8eeaf698d05adba024666f1975b0709599e1c33280ebc9c58bdc8616bb10c50(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72ceaedfa834e0103689cd5ade65831651063b821240738bd367387f4bdf4d1d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64633266558e4c792b8b398ed58dfa8beb37981b8d768d6b343b6dc5fb8dafda(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StackHciDeploymentSettingScaleUnit]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edb552175e461323ab76a40476f4a648b1d6e4d298d475b4b5f23e86602f2377(
    *,
    ipv4_address: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0f48fe216fbdaab3e15fc7cbefa7b2370299022ccae37b1163fbcbe9e1a8685(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acfb70ceecb57d5a3940202e70641cb78dbafa01045fb81f3c94e4b82010b34e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0759aaff0c16464d4692f1741d6668d5a9ceb62dcdde2b2bf54b7670aadfbba8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78c90112129a3c1b67c8b3087377e628a0eb0fba3cc86a2c141daaadc04137c5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b89226affea50f8850b564fe3f999b53955cac28d47e963b3245b8d8dfd4d2d4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82435128621ebdb2d04b386334ab5d4ff52922c757b55013e77de748016b5340(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StackHciDeploymentSettingScaleUnitPhysicalNode]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__248c0470ab51762f1eebc5fb940a2fddbcbb40d2388cb41808f2ca7b83944595(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__654a7afeaf2ab3f416b56d73e0912da628f9c80e3ca01d5e711eceba5af0f599(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11ebbfe1cc27bd14d3ebae6a2913579dc3906cbfb3e4ebf6c066565c954720c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64a88b07e17cc6f49af5ee4a95e7913e7d8db0e82c1194f3c03bdcad049b91f8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StackHciDeploymentSettingScaleUnitPhysicalNode]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb573095c1a549e7585f69edb911e79be37cdf47af10818fb63343f759d81058(
    *,
    configuration_mode: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfb4a5fd20fef9193206219d70854812629f5d3bbb7d8ee99db35ab6a64af430(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a06ef5db010903e02dabc7e28891555e9eab9a417da8a04d79aee7adb755944(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59c62daf80bee5f6b2ffb4671efc1538acfb6024c93456300caae2f1939226fc(
    value: typing.Optional[StackHciDeploymentSettingScaleUnitStorage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__047f2974a6fb8838efc484f709163e4fd7bead10bc42a57705daf3420fb903e9(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57b752473df945c25cee0f77418e51fb52c5341a086e5c2f7c163054ce749e8c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19f7db84c799a71b2fdc6d83b90aa976898a6b09f84a4b77ced1b10c658b8e89(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffd93742d7ce5dda253922f199eeaaa62dc8228ed08632b612e1619ad5b62e74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c75cc25283db74fbced3a326de2a90485ff60b783c749ab43495f25bbba454d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67bcaaf5ea8733f154d18f434544eb1457b484ddeda9a592354dfeb3b5f3760a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StackHciDeploymentSettingTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
