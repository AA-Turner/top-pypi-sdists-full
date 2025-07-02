r'''
# `azurerm_logic_app_integration_account_batch_configuration`

Refer to the Terraform Registry for docs: [`azurerm_logic_app_integration_account_batch_configuration`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration).
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


class LogicAppIntegrationAccountBatchConfiguration(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.logicAppIntegrationAccountBatchConfiguration.LogicAppIntegrationAccountBatchConfiguration",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration azurerm_logic_app_integration_account_batch_configuration}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        batch_group_name: builtins.str,
        integration_account_name: builtins.str,
        name: builtins.str,
        release_criteria: typing.Union["LogicAppIntegrationAccountBatchConfigurationReleaseCriteria", typing.Dict[builtins.str, typing.Any]],
        resource_group_name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["LogicAppIntegrationAccountBatchConfigurationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration azurerm_logic_app_integration_account_batch_configuration} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param batch_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#batch_group_name LogicAppIntegrationAccountBatchConfiguration#batch_group_name}.
        :param integration_account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#integration_account_name LogicAppIntegrationAccountBatchConfiguration#integration_account_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#name LogicAppIntegrationAccountBatchConfiguration#name}.
        :param release_criteria: release_criteria block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#release_criteria LogicAppIntegrationAccountBatchConfiguration#release_criteria}
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#resource_group_name LogicAppIntegrationAccountBatchConfiguration#resource_group_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#id LogicAppIntegrationAccountBatchConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param metadata: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#metadata LogicAppIntegrationAccountBatchConfiguration#metadata}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#timeouts LogicAppIntegrationAccountBatchConfiguration#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfe24d620d559737b5cbbf4c8fd0071d6706a4c24a01a6ede2560372cd6913c3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = LogicAppIntegrationAccountBatchConfigurationConfig(
            batch_group_name=batch_group_name,
            integration_account_name=integration_account_name,
            name=name,
            release_criteria=release_criteria,
            resource_group_name=resource_group_name,
            id=id,
            metadata=metadata,
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
        '''Generates CDKTF code for importing a LogicAppIntegrationAccountBatchConfiguration resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the LogicAppIntegrationAccountBatchConfiguration to import.
        :param import_from_id: The id of the existing LogicAppIntegrationAccountBatchConfiguration that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the LogicAppIntegrationAccountBatchConfiguration to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22aa59f7552f8e9e53b78c37160cb40c30ecfda3791bc72af0d998ee14e01211)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putReleaseCriteria")
    def put_release_criteria(
        self,
        *,
        batch_size: typing.Optional[jsii.Number] = None,
        message_count: typing.Optional[jsii.Number] = None,
        recurrence: typing.Optional[typing.Union["LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrence", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param batch_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#batch_size LogicAppIntegrationAccountBatchConfiguration#batch_size}.
        :param message_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#message_count LogicAppIntegrationAccountBatchConfiguration#message_count}.
        :param recurrence: recurrence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#recurrence LogicAppIntegrationAccountBatchConfiguration#recurrence}
        '''
        value = LogicAppIntegrationAccountBatchConfigurationReleaseCriteria(
            batch_size=batch_size, message_count=message_count, recurrence=recurrence
        )

        return typing.cast(None, jsii.invoke(self, "putReleaseCriteria", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#create LogicAppIntegrationAccountBatchConfiguration#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#delete LogicAppIntegrationAccountBatchConfiguration#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#read LogicAppIntegrationAccountBatchConfiguration#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#update LogicAppIntegrationAccountBatchConfiguration#update}.
        '''
        value = LogicAppIntegrationAccountBatchConfigurationTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMetadata")
    def reset_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadata", []))

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
    @jsii.member(jsii_name="releaseCriteria")
    def release_criteria(
        self,
    ) -> "LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaOutputReference":
        return typing.cast("LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaOutputReference", jsii.get(self, "releaseCriteria"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "LogicAppIntegrationAccountBatchConfigurationTimeoutsOutputReference":
        return typing.cast("LogicAppIntegrationAccountBatchConfigurationTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="batchGroupNameInput")
    def batch_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "batchGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="integrationAccountNameInput")
    def integration_account_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "integrationAccountNameInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="releaseCriteriaInput")
    def release_criteria_input(
        self,
    ) -> typing.Optional["LogicAppIntegrationAccountBatchConfigurationReleaseCriteria"]:
        return typing.cast(typing.Optional["LogicAppIntegrationAccountBatchConfigurationReleaseCriteria"], jsii.get(self, "releaseCriteriaInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "LogicAppIntegrationAccountBatchConfigurationTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "LogicAppIntegrationAccountBatchConfigurationTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="batchGroupName")
    def batch_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "batchGroupName"))

    @batch_group_name.setter
    def batch_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6afef2e336a6f37aec818c06c0e62b0a6b88de123ab44385d1b9574922d9fcd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c471e04b6911b9eb1429ec7ccd2977165ce6978f972213c7062ad7fafba04679)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="integrationAccountName")
    def integration_account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "integrationAccountName"))

    @integration_account_name.setter
    def integration_account_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0271554fd25a1a920b646835ce89a80f58dab4d083033d3888449eb1b77308eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integrationAccountName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60e7d904adad8c7ca981ef355a43c225cc10758e46c1eede7fccb354414fd086)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__868143a1517e7157ba00516d413217abbe6d920485c0b5bac16e570ca1c44695)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e0028e6dec68ef6c252f0e82e54d81f251e6330311db05f71aae824911185e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.logicAppIntegrationAccountBatchConfiguration.LogicAppIntegrationAccountBatchConfigurationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "batch_group_name": "batchGroupName",
        "integration_account_name": "integrationAccountName",
        "name": "name",
        "release_criteria": "releaseCriteria",
        "resource_group_name": "resourceGroupName",
        "id": "id",
        "metadata": "metadata",
        "timeouts": "timeouts",
    },
)
class LogicAppIntegrationAccountBatchConfigurationConfig(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        batch_group_name: builtins.str,
        integration_account_name: builtins.str,
        name: builtins.str,
        release_criteria: typing.Union["LogicAppIntegrationAccountBatchConfigurationReleaseCriteria", typing.Dict[builtins.str, typing.Any]],
        resource_group_name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["LogicAppIntegrationAccountBatchConfigurationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param batch_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#batch_group_name LogicAppIntegrationAccountBatchConfiguration#batch_group_name}.
        :param integration_account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#integration_account_name LogicAppIntegrationAccountBatchConfiguration#integration_account_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#name LogicAppIntegrationAccountBatchConfiguration#name}.
        :param release_criteria: release_criteria block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#release_criteria LogicAppIntegrationAccountBatchConfiguration#release_criteria}
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#resource_group_name LogicAppIntegrationAccountBatchConfiguration#resource_group_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#id LogicAppIntegrationAccountBatchConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param metadata: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#metadata LogicAppIntegrationAccountBatchConfiguration#metadata}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#timeouts LogicAppIntegrationAccountBatchConfiguration#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(release_criteria, dict):
            release_criteria = LogicAppIntegrationAccountBatchConfigurationReleaseCriteria(**release_criteria)
        if isinstance(timeouts, dict):
            timeouts = LogicAppIntegrationAccountBatchConfigurationTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b3827ee8904907f16c164664d2a2d2f0cd5831ce8fa26736c2296429e37ff84)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument batch_group_name", value=batch_group_name, expected_type=type_hints["batch_group_name"])
            check_type(argname="argument integration_account_name", value=integration_account_name, expected_type=type_hints["integration_account_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument release_criteria", value=release_criteria, expected_type=type_hints["release_criteria"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "batch_group_name": batch_group_name,
            "integration_account_name": integration_account_name,
            "name": name,
            "release_criteria": release_criteria,
            "resource_group_name": resource_group_name,
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
        if metadata is not None:
            self._values["metadata"] = metadata
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
    def batch_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#batch_group_name LogicAppIntegrationAccountBatchConfiguration#batch_group_name}.'''
        result = self._values.get("batch_group_name")
        assert result is not None, "Required property 'batch_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def integration_account_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#integration_account_name LogicAppIntegrationAccountBatchConfiguration#integration_account_name}.'''
        result = self._values.get("integration_account_name")
        assert result is not None, "Required property 'integration_account_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#name LogicAppIntegrationAccountBatchConfiguration#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def release_criteria(
        self,
    ) -> "LogicAppIntegrationAccountBatchConfigurationReleaseCriteria":
        '''release_criteria block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#release_criteria LogicAppIntegrationAccountBatchConfiguration#release_criteria}
        '''
        result = self._values.get("release_criteria")
        assert result is not None, "Required property 'release_criteria' is missing"
        return typing.cast("LogicAppIntegrationAccountBatchConfigurationReleaseCriteria", result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#resource_group_name LogicAppIntegrationAccountBatchConfiguration#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#id LogicAppIntegrationAccountBatchConfiguration#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metadata(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#metadata LogicAppIntegrationAccountBatchConfiguration#metadata}.'''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["LogicAppIntegrationAccountBatchConfigurationTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#timeouts LogicAppIntegrationAccountBatchConfiguration#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["LogicAppIntegrationAccountBatchConfigurationTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogicAppIntegrationAccountBatchConfigurationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.logicAppIntegrationAccountBatchConfiguration.LogicAppIntegrationAccountBatchConfigurationReleaseCriteria",
    jsii_struct_bases=[],
    name_mapping={
        "batch_size": "batchSize",
        "message_count": "messageCount",
        "recurrence": "recurrence",
    },
)
class LogicAppIntegrationAccountBatchConfigurationReleaseCriteria:
    def __init__(
        self,
        *,
        batch_size: typing.Optional[jsii.Number] = None,
        message_count: typing.Optional[jsii.Number] = None,
        recurrence: typing.Optional[typing.Union["LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrence", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param batch_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#batch_size LogicAppIntegrationAccountBatchConfiguration#batch_size}.
        :param message_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#message_count LogicAppIntegrationAccountBatchConfiguration#message_count}.
        :param recurrence: recurrence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#recurrence LogicAppIntegrationAccountBatchConfiguration#recurrence}
        '''
        if isinstance(recurrence, dict):
            recurrence = LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrence(**recurrence)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5879b00355465facd6acefe4cccd6d82908e1ff00bf98dec324b1f1534c268ba)
            check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
            check_type(argname="argument message_count", value=message_count, expected_type=type_hints["message_count"])
            check_type(argname="argument recurrence", value=recurrence, expected_type=type_hints["recurrence"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if batch_size is not None:
            self._values["batch_size"] = batch_size
        if message_count is not None:
            self._values["message_count"] = message_count
        if recurrence is not None:
            self._values["recurrence"] = recurrence

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#batch_size LogicAppIntegrationAccountBatchConfiguration#batch_size}.'''
        result = self._values.get("batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def message_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#message_count LogicAppIntegrationAccountBatchConfiguration#message_count}.'''
        result = self._values.get("message_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def recurrence(
        self,
    ) -> typing.Optional["LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrence"]:
        '''recurrence block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#recurrence LogicAppIntegrationAccountBatchConfiguration#recurrence}
        '''
        result = self._values.get("recurrence")
        return typing.cast(typing.Optional["LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrence"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogicAppIntegrationAccountBatchConfigurationReleaseCriteria(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.logicAppIntegrationAccountBatchConfiguration.LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a17efece447fda1fd08f19f463791f218d1770e72eee9e0d23f992dcb1df753e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRecurrence")
    def put_recurrence(
        self,
        *,
        frequency: builtins.str,
        interval: jsii.Number,
        end_time: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[typing.Union["LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        start_time: typing.Optional[builtins.str] = None,
        time_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param frequency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#frequency LogicAppIntegrationAccountBatchConfiguration#frequency}.
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#interval LogicAppIntegrationAccountBatchConfiguration#interval}.
        :param end_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#end_time LogicAppIntegrationAccountBatchConfiguration#end_time}.
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#schedule LogicAppIntegrationAccountBatchConfiguration#schedule}
        :param start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#start_time LogicAppIntegrationAccountBatchConfiguration#start_time}.
        :param time_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#time_zone LogicAppIntegrationAccountBatchConfiguration#time_zone}.
        '''
        value = LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrence(
            frequency=frequency,
            interval=interval,
            end_time=end_time,
            schedule=schedule,
            start_time=start_time,
            time_zone=time_zone,
        )

        return typing.cast(None, jsii.invoke(self, "putRecurrence", [value]))

    @jsii.member(jsii_name="resetBatchSize")
    def reset_batch_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatchSize", []))

    @jsii.member(jsii_name="resetMessageCount")
    def reset_message_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessageCount", []))

    @jsii.member(jsii_name="resetRecurrence")
    def reset_recurrence(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecurrence", []))

    @builtins.property
    @jsii.member(jsii_name="recurrence")
    def recurrence(
        self,
    ) -> "LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceOutputReference":
        return typing.cast("LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceOutputReference", jsii.get(self, "recurrence"))

    @builtins.property
    @jsii.member(jsii_name="batchSizeInput")
    def batch_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "batchSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="messageCountInput")
    def message_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "messageCountInput"))

    @builtins.property
    @jsii.member(jsii_name="recurrenceInput")
    def recurrence_input(
        self,
    ) -> typing.Optional["LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrence"]:
        return typing.cast(typing.Optional["LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrence"], jsii.get(self, "recurrenceInput"))

    @builtins.property
    @jsii.member(jsii_name="batchSize")
    def batch_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "batchSize"))

    @batch_size.setter
    def batch_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88dd10d8c49ca3c647db9b4b4e22d1c567c6e905003e9fad630eb811a5b6d8e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="messageCount")
    def message_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "messageCount"))

    @message_count.setter
    def message_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf202e4663b14397fe37c585504c82e5d4923e402686441cbc78e035ee6f2231)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LogicAppIntegrationAccountBatchConfigurationReleaseCriteria]:
        return typing.cast(typing.Optional[LogicAppIntegrationAccountBatchConfigurationReleaseCriteria], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LogicAppIntegrationAccountBatchConfigurationReleaseCriteria],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2bf72fb09ab186f547948d85d53be4b3bf251917df5378e3f76ffabc2d00c59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.logicAppIntegrationAccountBatchConfiguration.LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrence",
    jsii_struct_bases=[],
    name_mapping={
        "frequency": "frequency",
        "interval": "interval",
        "end_time": "endTime",
        "schedule": "schedule",
        "start_time": "startTime",
        "time_zone": "timeZone",
    },
)
class LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrence:
    def __init__(
        self,
        *,
        frequency: builtins.str,
        interval: jsii.Number,
        end_time: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[typing.Union["LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        start_time: typing.Optional[builtins.str] = None,
        time_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param frequency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#frequency LogicAppIntegrationAccountBatchConfiguration#frequency}.
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#interval LogicAppIntegrationAccountBatchConfiguration#interval}.
        :param end_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#end_time LogicAppIntegrationAccountBatchConfiguration#end_time}.
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#schedule LogicAppIntegrationAccountBatchConfiguration#schedule}
        :param start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#start_time LogicAppIntegrationAccountBatchConfiguration#start_time}.
        :param time_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#time_zone LogicAppIntegrationAccountBatchConfiguration#time_zone}.
        '''
        if isinstance(schedule, dict):
            schedule = LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceSchedule(**schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae55155252924ee6025e9f8eb08de46d1e0b66a22561a2e3d09f487d7307240c)
            check_type(argname="argument frequency", value=frequency, expected_type=type_hints["frequency"])
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "frequency": frequency,
            "interval": interval,
        }
        if end_time is not None:
            self._values["end_time"] = end_time
        if schedule is not None:
            self._values["schedule"] = schedule
        if start_time is not None:
            self._values["start_time"] = start_time
        if time_zone is not None:
            self._values["time_zone"] = time_zone

    @builtins.property
    def frequency(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#frequency LogicAppIntegrationAccountBatchConfiguration#frequency}.'''
        result = self._values.get("frequency")
        assert result is not None, "Required property 'frequency' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def interval(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#interval LogicAppIntegrationAccountBatchConfiguration#interval}.'''
        result = self._values.get("interval")
        assert result is not None, "Required property 'interval' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def end_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#end_time LogicAppIntegrationAccountBatchConfiguration#end_time}.'''
        result = self._values.get("end_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule(
        self,
    ) -> typing.Optional["LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceSchedule"]:
        '''schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#schedule LogicAppIntegrationAccountBatchConfiguration#schedule}
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional["LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceSchedule"], result)

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#start_time LogicAppIntegrationAccountBatchConfiguration#start_time}.'''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_zone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#time_zone LogicAppIntegrationAccountBatchConfiguration#time_zone}.'''
        result = self._values.get("time_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrence(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.logicAppIntegrationAccountBatchConfiguration.LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3c49f814dd0c8535f1b7f9a94a0c9fe3ef24c29fdd62d817bd8db840eac2bba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSchedule")
    def put_schedule(
        self,
        *,
        hours: typing.Optional[typing.Sequence[jsii.Number]] = None,
        minutes: typing.Optional[typing.Sequence[jsii.Number]] = None,
        month_days: typing.Optional[typing.Sequence[jsii.Number]] = None,
        monthly: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceScheduleMonthly", typing.Dict[builtins.str, typing.Any]]]]] = None,
        week_days: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param hours: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#hours LogicAppIntegrationAccountBatchConfiguration#hours}.
        :param minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#minutes LogicAppIntegrationAccountBatchConfiguration#minutes}.
        :param month_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#month_days LogicAppIntegrationAccountBatchConfiguration#month_days}.
        :param monthly: monthly block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#monthly LogicAppIntegrationAccountBatchConfiguration#monthly}
        :param week_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#week_days LogicAppIntegrationAccountBatchConfiguration#week_days}.
        '''
        value = LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceSchedule(
            hours=hours,
            minutes=minutes,
            month_days=month_days,
            monthly=monthly,
            week_days=week_days,
        )

        return typing.cast(None, jsii.invoke(self, "putSchedule", [value]))

    @jsii.member(jsii_name="resetEndTime")
    def reset_end_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndTime", []))

    @jsii.member(jsii_name="resetSchedule")
    def reset_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchedule", []))

    @jsii.member(jsii_name="resetStartTime")
    def reset_start_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartTime", []))

    @jsii.member(jsii_name="resetTimeZone")
    def reset_time_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeZone", []))

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(
        self,
    ) -> "LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceScheduleOutputReference":
        return typing.cast("LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceScheduleOutputReference", jsii.get(self, "schedule"))

    @builtins.property
    @jsii.member(jsii_name="endTimeInput")
    def end_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="frequencyInput")
    def frequency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "frequencyInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalInput")
    def interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(
        self,
    ) -> typing.Optional["LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceSchedule"]:
        return typing.cast(typing.Optional["LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceSchedule"], jsii.get(self, "scheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZoneInput")
    def time_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTime"))

    @end_time.setter
    def end_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc9819a16b0a71c17dd570eb38fdd98d484ce9cad3f9e5a267503e4160140521)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="frequency")
    def frequency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "frequency"))

    @frequency.setter
    def frequency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52630aaf81d797741cf8f1fc6c0ae5bfb6267b0517125c2f3896770cc6b33601)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frequency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "interval"))

    @interval.setter
    def interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f988b802a80635249f2c8cb51c5ff713b18734dc13ea1c9321a267bd01a5862d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4347ea954ffa1f00b52339e8f51a31faf369a95258db0594353d572121aea3f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba743a3721d24858dbe3df53b2eb76b65115c1a343b848bf3f27021fd0e966ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrence]:
        return typing.cast(typing.Optional[LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrence], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrence],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e0995bfd7f17e4b44b6d698af35efe657c062e212b9c0871b75f11790941aca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.logicAppIntegrationAccountBatchConfiguration.LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceSchedule",
    jsii_struct_bases=[],
    name_mapping={
        "hours": "hours",
        "minutes": "minutes",
        "month_days": "monthDays",
        "monthly": "monthly",
        "week_days": "weekDays",
    },
)
class LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceSchedule:
    def __init__(
        self,
        *,
        hours: typing.Optional[typing.Sequence[jsii.Number]] = None,
        minutes: typing.Optional[typing.Sequence[jsii.Number]] = None,
        month_days: typing.Optional[typing.Sequence[jsii.Number]] = None,
        monthly: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceScheduleMonthly", typing.Dict[builtins.str, typing.Any]]]]] = None,
        week_days: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param hours: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#hours LogicAppIntegrationAccountBatchConfiguration#hours}.
        :param minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#minutes LogicAppIntegrationAccountBatchConfiguration#minutes}.
        :param month_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#month_days LogicAppIntegrationAccountBatchConfiguration#month_days}.
        :param monthly: monthly block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#monthly LogicAppIntegrationAccountBatchConfiguration#monthly}
        :param week_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#week_days LogicAppIntegrationAccountBatchConfiguration#week_days}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__136a30e97d85be8b358c296112d0e96c0a881afb29c4318d2e29ec1d054201fd)
            check_type(argname="argument hours", value=hours, expected_type=type_hints["hours"])
            check_type(argname="argument minutes", value=minutes, expected_type=type_hints["minutes"])
            check_type(argname="argument month_days", value=month_days, expected_type=type_hints["month_days"])
            check_type(argname="argument monthly", value=monthly, expected_type=type_hints["monthly"])
            check_type(argname="argument week_days", value=week_days, expected_type=type_hints["week_days"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if hours is not None:
            self._values["hours"] = hours
        if minutes is not None:
            self._values["minutes"] = minutes
        if month_days is not None:
            self._values["month_days"] = month_days
        if monthly is not None:
            self._values["monthly"] = monthly
        if week_days is not None:
            self._values["week_days"] = week_days

    @builtins.property
    def hours(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#hours LogicAppIntegrationAccountBatchConfiguration#hours}.'''
        result = self._values.get("hours")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def minutes(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#minutes LogicAppIntegrationAccountBatchConfiguration#minutes}.'''
        result = self._values.get("minutes")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def month_days(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#month_days LogicAppIntegrationAccountBatchConfiguration#month_days}.'''
        result = self._values.get("month_days")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def monthly(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceScheduleMonthly"]]]:
        '''monthly block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#monthly LogicAppIntegrationAccountBatchConfiguration#monthly}
        '''
        result = self._values.get("monthly")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceScheduleMonthly"]]], result)

    @builtins.property
    def week_days(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#week_days LogicAppIntegrationAccountBatchConfiguration#week_days}.'''
        result = self._values.get("week_days")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.logicAppIntegrationAccountBatchConfiguration.LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceScheduleMonthly",
    jsii_struct_bases=[],
    name_mapping={"week": "week", "weekday": "weekday"},
)
class LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceScheduleMonthly:
    def __init__(self, *, week: jsii.Number, weekday: builtins.str) -> None:
        '''
        :param week: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#week LogicAppIntegrationAccountBatchConfiguration#week}.
        :param weekday: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#weekday LogicAppIntegrationAccountBatchConfiguration#weekday}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b62087c449e7796d839a80bf809729560456e35d6da9bacc31cb3728bfa573f5)
            check_type(argname="argument week", value=week, expected_type=type_hints["week"])
            check_type(argname="argument weekday", value=weekday, expected_type=type_hints["weekday"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "week": week,
            "weekday": weekday,
        }

    @builtins.property
    def week(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#week LogicAppIntegrationAccountBatchConfiguration#week}.'''
        result = self._values.get("week")
        assert result is not None, "Required property 'week' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def weekday(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#weekday LogicAppIntegrationAccountBatchConfiguration#weekday}.'''
        result = self._values.get("weekday")
        assert result is not None, "Required property 'weekday' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceScheduleMonthly(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceScheduleMonthlyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.logicAppIntegrationAccountBatchConfiguration.LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceScheduleMonthlyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c55b2ae6303073e9eb2cab3b50bbb3046ae14cd80105ab35f5283791c588c76d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceScheduleMonthlyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c6b802f43a21e1da77cbe996c0a11c3fdf93bd717dc2fe6d98cc4cb90bd4c80)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceScheduleMonthlyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a96874b7789ec498f0fa14d2c1910f4ca668218c874321258aab4a1818c435f8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__138d6e0280a75660af40d755d8fdf1e0786491d0f71bfef946425a6a80f9fe4e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f8001e862d46829c0ae0efb48ae4fbc88270b9e874fe3a696aa09224f61e0f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceScheduleMonthly]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceScheduleMonthly]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceScheduleMonthly]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23a0030a15758ff519646d1e48dc596b2ba9264fdfdb279a95e89b3f42d1aa40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceScheduleMonthlyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.logicAppIntegrationAccountBatchConfiguration.LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceScheduleMonthlyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff5c2b38080c22fd989ca01bb6279a1249225ccbba556963b565754a28a7f507)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="weekdayInput")
    def weekday_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "weekdayInput"))

    @builtins.property
    @jsii.member(jsii_name="weekInput")
    def week_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "weekInput"))

    @builtins.property
    @jsii.member(jsii_name="week")
    def week(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "week"))

    @week.setter
    def week(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac017527beefc8198985e8673640491db1ee8fe6a92d2cf2f814a90cf1b7c399)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "week", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weekday")
    def weekday(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "weekday"))

    @weekday.setter
    def weekday(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c528251bab069848995a37407fd7d15c2c138c92d8a0512d5dd4a4ae450a1910)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weekday", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceScheduleMonthly]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceScheduleMonthly]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceScheduleMonthly]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__019528561cdc39e14d0970e6494c15d37bceb189bbca7820a97e61bbdb01855a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.logicAppIntegrationAccountBatchConfiguration.LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__55edb09349fdea85712e4dee12eff12febe62c4dca931a6f70e471154b5cf161)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMonthly")
    def put_monthly(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceScheduleMonthly, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__899c49ff35ee7d1fa82c8d9c9f2368c12a6733f961653a970ccaf7754d696861)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMonthly", [value]))

    @jsii.member(jsii_name="resetHours")
    def reset_hours(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHours", []))

    @jsii.member(jsii_name="resetMinutes")
    def reset_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinutes", []))

    @jsii.member(jsii_name="resetMonthDays")
    def reset_month_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonthDays", []))

    @jsii.member(jsii_name="resetMonthly")
    def reset_monthly(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonthly", []))

    @jsii.member(jsii_name="resetWeekDays")
    def reset_week_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeekDays", []))

    @builtins.property
    @jsii.member(jsii_name="monthly")
    def monthly(
        self,
    ) -> LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceScheduleMonthlyList:
        return typing.cast(LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceScheduleMonthlyList, jsii.get(self, "monthly"))

    @builtins.property
    @jsii.member(jsii_name="hoursInput")
    def hours_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "hoursInput"))

    @builtins.property
    @jsii.member(jsii_name="minutesInput")
    def minutes_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "minutesInput"))

    @builtins.property
    @jsii.member(jsii_name="monthDaysInput")
    def month_days_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "monthDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="monthlyInput")
    def monthly_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceScheduleMonthly]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceScheduleMonthly]]], jsii.get(self, "monthlyInput"))

    @builtins.property
    @jsii.member(jsii_name="weekDaysInput")
    def week_days_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "weekDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="hours")
    def hours(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "hours"))

    @hours.setter
    def hours(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea406cf296f380838be31adfb3a2e35e58bc03ebeb48ae84050d9f8ff92e03d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minutes")
    def minutes(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "minutes"))

    @minutes.setter
    def minutes(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bbf8c60b48ae5c3c9fee53d46074686bd3146257381bc1eb8cc8b68ae8f4f3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="monthDays")
    def month_days(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "monthDays"))

    @month_days.setter
    def month_days(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89878bfe8f2f97c91c845528d10ab4b92da37e960ce02e26aff087e1eefec0b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monthDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weekDays")
    def week_days(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "weekDays"))

    @week_days.setter
    def week_days(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2994a951b8e2e10f52662a7ba4803fa48dabb937470bc0876a5d13a3177fbd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weekDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceSchedule]:
        return typing.cast(typing.Optional[LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceSchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceSchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f76a8a927902887163e02befd1a180e29b3d1fe38fc8f0ae441967d7dcb87b45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.logicAppIntegrationAccountBatchConfiguration.LogicAppIntegrationAccountBatchConfigurationTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class LogicAppIntegrationAccountBatchConfigurationTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#create LogicAppIntegrationAccountBatchConfiguration#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#delete LogicAppIntegrationAccountBatchConfiguration#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#read LogicAppIntegrationAccountBatchConfiguration#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#update LogicAppIntegrationAccountBatchConfiguration#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b5dba60071d0b42be32876936adbddc743f2031697eedb18fca472fc87e710b)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#create LogicAppIntegrationAccountBatchConfiguration#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#delete LogicAppIntegrationAccountBatchConfiguration#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#read LogicAppIntegrationAccountBatchConfiguration#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/logic_app_integration_account_batch_configuration#update LogicAppIntegrationAccountBatchConfiguration#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogicAppIntegrationAccountBatchConfigurationTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogicAppIntegrationAccountBatchConfigurationTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.logicAppIntegrationAccountBatchConfiguration.LogicAppIntegrationAccountBatchConfigurationTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f8fdcdedf01f19ed254d1b053987ab9d3de248a21e9a7d3f57e59bf61580692)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2254f592380fc5bf6d90960c3964d1ba7ef60afc00b685b53570eab7009db3c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2f1b1424c7c441ad44341927e541ebbfaa25b62907bab1ec508a8ee1cfff1d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a71d7ed5c9af398fde4b993a0c084a407b23468aff90ce2269a5c74c697e56a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b96f83d033702674eb732a75947f65f780d8e655080e76676ab7513a4b2a239)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogicAppIntegrationAccountBatchConfigurationTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogicAppIntegrationAccountBatchConfigurationTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogicAppIntegrationAccountBatchConfigurationTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__653cf0a5a7ea738b66e30ea5ed427ba175c33fcc129df71c30b06c4b969c749b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "LogicAppIntegrationAccountBatchConfiguration",
    "LogicAppIntegrationAccountBatchConfigurationConfig",
    "LogicAppIntegrationAccountBatchConfigurationReleaseCriteria",
    "LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaOutputReference",
    "LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrence",
    "LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceOutputReference",
    "LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceSchedule",
    "LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceScheduleMonthly",
    "LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceScheduleMonthlyList",
    "LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceScheduleMonthlyOutputReference",
    "LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceScheduleOutputReference",
    "LogicAppIntegrationAccountBatchConfigurationTimeouts",
    "LogicAppIntegrationAccountBatchConfigurationTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__bfe24d620d559737b5cbbf4c8fd0071d6706a4c24a01a6ede2560372cd6913c3(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    batch_group_name: builtins.str,
    integration_account_name: builtins.str,
    name: builtins.str,
    release_criteria: typing.Union[LogicAppIntegrationAccountBatchConfigurationReleaseCriteria, typing.Dict[builtins.str, typing.Any]],
    resource_group_name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[LogicAppIntegrationAccountBatchConfigurationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__22aa59f7552f8e9e53b78c37160cb40c30ecfda3791bc72af0d998ee14e01211(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6afef2e336a6f37aec818c06c0e62b0a6b88de123ab44385d1b9574922d9fcd5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c471e04b6911b9eb1429ec7ccd2977165ce6978f972213c7062ad7fafba04679(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0271554fd25a1a920b646835ce89a80f58dab4d083033d3888449eb1b77308eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60e7d904adad8c7ca981ef355a43c225cc10758e46c1eede7fccb354414fd086(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__868143a1517e7157ba00516d413217abbe6d920485c0b5bac16e570ca1c44695(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e0028e6dec68ef6c252f0e82e54d81f251e6330311db05f71aae824911185e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b3827ee8904907f16c164664d2a2d2f0cd5831ce8fa26736c2296429e37ff84(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    batch_group_name: builtins.str,
    integration_account_name: builtins.str,
    name: builtins.str,
    release_criteria: typing.Union[LogicAppIntegrationAccountBatchConfigurationReleaseCriteria, typing.Dict[builtins.str, typing.Any]],
    resource_group_name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[LogicAppIntegrationAccountBatchConfigurationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5879b00355465facd6acefe4cccd6d82908e1ff00bf98dec324b1f1534c268ba(
    *,
    batch_size: typing.Optional[jsii.Number] = None,
    message_count: typing.Optional[jsii.Number] = None,
    recurrence: typing.Optional[typing.Union[LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrence, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a17efece447fda1fd08f19f463791f218d1770e72eee9e0d23f992dcb1df753e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88dd10d8c49ca3c647db9b4b4e22d1c567c6e905003e9fad630eb811a5b6d8e9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf202e4663b14397fe37c585504c82e5d4923e402686441cbc78e035ee6f2231(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2bf72fb09ab186f547948d85d53be4b3bf251917df5378e3f76ffabc2d00c59(
    value: typing.Optional[LogicAppIntegrationAccountBatchConfigurationReleaseCriteria],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae55155252924ee6025e9f8eb08de46d1e0b66a22561a2e3d09f487d7307240c(
    *,
    frequency: builtins.str,
    interval: jsii.Number,
    end_time: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[typing.Union[LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    start_time: typing.Optional[builtins.str] = None,
    time_zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3c49f814dd0c8535f1b7f9a94a0c9fe3ef24c29fdd62d817bd8db840eac2bba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc9819a16b0a71c17dd570eb38fdd98d484ce9cad3f9e5a267503e4160140521(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52630aaf81d797741cf8f1fc6c0ae5bfb6267b0517125c2f3896770cc6b33601(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f988b802a80635249f2c8cb51c5ff713b18734dc13ea1c9321a267bd01a5862d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4347ea954ffa1f00b52339e8f51a31faf369a95258db0594353d572121aea3f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba743a3721d24858dbe3df53b2eb76b65115c1a343b848bf3f27021fd0e966ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e0995bfd7f17e4b44b6d698af35efe657c062e212b9c0871b75f11790941aca(
    value: typing.Optional[LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrence],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__136a30e97d85be8b358c296112d0e96c0a881afb29c4318d2e29ec1d054201fd(
    *,
    hours: typing.Optional[typing.Sequence[jsii.Number]] = None,
    minutes: typing.Optional[typing.Sequence[jsii.Number]] = None,
    month_days: typing.Optional[typing.Sequence[jsii.Number]] = None,
    monthly: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceScheduleMonthly, typing.Dict[builtins.str, typing.Any]]]]] = None,
    week_days: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b62087c449e7796d839a80bf809729560456e35d6da9bacc31cb3728bfa573f5(
    *,
    week: jsii.Number,
    weekday: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c55b2ae6303073e9eb2cab3b50bbb3046ae14cd80105ab35f5283791c588c76d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c6b802f43a21e1da77cbe996c0a11c3fdf93bd717dc2fe6d98cc4cb90bd4c80(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a96874b7789ec498f0fa14d2c1910f4ca668218c874321258aab4a1818c435f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__138d6e0280a75660af40d755d8fdf1e0786491d0f71bfef946425a6a80f9fe4e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f8001e862d46829c0ae0efb48ae4fbc88270b9e874fe3a696aa09224f61e0f7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23a0030a15758ff519646d1e48dc596b2ba9264fdfdb279a95e89b3f42d1aa40(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceScheduleMonthly]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff5c2b38080c22fd989ca01bb6279a1249225ccbba556963b565754a28a7f507(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac017527beefc8198985e8673640491db1ee8fe6a92d2cf2f814a90cf1b7c399(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c528251bab069848995a37407fd7d15c2c138c92d8a0512d5dd4a4ae450a1910(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__019528561cdc39e14d0970e6494c15d37bceb189bbca7820a97e61bbdb01855a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceScheduleMonthly]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55edb09349fdea85712e4dee12eff12febe62c4dca931a6f70e471154b5cf161(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__899c49ff35ee7d1fa82c8d9c9f2368c12a6733f961653a970ccaf7754d696861(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceScheduleMonthly, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea406cf296f380838be31adfb3a2e35e58bc03ebeb48ae84050d9f8ff92e03d4(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bbf8c60b48ae5c3c9fee53d46074686bd3146257381bc1eb8cc8b68ae8f4f3e(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89878bfe8f2f97c91c845528d10ab4b92da37e960ce02e26aff087e1eefec0b7(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2994a951b8e2e10f52662a7ba4803fa48dabb937470bc0876a5d13a3177fbd1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f76a8a927902887163e02befd1a180e29b3d1fe38fc8f0ae441967d7dcb87b45(
    value: typing.Optional[LogicAppIntegrationAccountBatchConfigurationReleaseCriteriaRecurrenceSchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b5dba60071d0b42be32876936adbddc743f2031697eedb18fca472fc87e710b(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f8fdcdedf01f19ed254d1b053987ab9d3de248a21e9a7d3f57e59bf61580692(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2254f592380fc5bf6d90960c3964d1ba7ef60afc00b685b53570eab7009db3c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2f1b1424c7c441ad44341927e541ebbfaa25b62907bab1ec508a8ee1cfff1d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a71d7ed5c9af398fde4b993a0c084a407b23468aff90ce2269a5c74c697e56a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b96f83d033702674eb732a75947f65f780d8e655080e76676ab7513a4b2a239(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__653cf0a5a7ea738b66e30ea5ed427ba175c33fcc129df71c30b06c4b969c749b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogicAppIntegrationAccountBatchConfigurationTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
