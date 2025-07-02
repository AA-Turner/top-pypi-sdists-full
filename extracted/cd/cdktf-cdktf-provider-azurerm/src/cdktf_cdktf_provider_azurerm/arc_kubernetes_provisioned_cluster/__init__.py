r'''
# `azurerm_arc_kubernetes_provisioned_cluster`

Refer to the Terraform Registry for docs: [`azurerm_arc_kubernetes_provisioned_cluster`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster).
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


class ArcKubernetesProvisionedCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.arcKubernetesProvisionedCluster.ArcKubernetesProvisionedCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster azurerm_arc_kubernetes_provisioned_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        identity: typing.Union["ArcKubernetesProvisionedClusterIdentity", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        arc_agent_auto_upgrade_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        arc_agent_desired_version: typing.Optional[builtins.str] = None,
        azure_active_directory: typing.Optional[typing.Union["ArcKubernetesProvisionedClusterAzureActiveDirectory", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ArcKubernetesProvisionedClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster azurerm_arc_kubernetes_provisioned_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#identity ArcKubernetesProvisionedCluster#identity}
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#location ArcKubernetesProvisionedCluster#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#name ArcKubernetesProvisionedCluster#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#resource_group_name ArcKubernetesProvisionedCluster#resource_group_name}.
        :param arc_agent_auto_upgrade_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#arc_agent_auto_upgrade_enabled ArcKubernetesProvisionedCluster#arc_agent_auto_upgrade_enabled}.
        :param arc_agent_desired_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#arc_agent_desired_version ArcKubernetesProvisionedCluster#arc_agent_desired_version}.
        :param azure_active_directory: azure_active_directory block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#azure_active_directory ArcKubernetesProvisionedCluster#azure_active_directory}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#id ArcKubernetesProvisionedCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#tags ArcKubernetesProvisionedCluster#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#timeouts ArcKubernetesProvisionedCluster#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9234239b2a443c62d5b1f346bce766e8decb4e0dd86ec9d3eaae8affc09666b9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ArcKubernetesProvisionedClusterConfig(
            identity=identity,
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            arc_agent_auto_upgrade_enabled=arc_agent_auto_upgrade_enabled,
            arc_agent_desired_version=arc_agent_desired_version,
            azure_active_directory=azure_active_directory,
            id=id,
            tags=tags,
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
        '''Generates CDKTF code for importing a ArcKubernetesProvisionedCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ArcKubernetesProvisionedCluster to import.
        :param import_from_id: The id of the existing ArcKubernetesProvisionedCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ArcKubernetesProvisionedCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45c6e6ebff28c528d8050be89f436cdc15ef6da32d4cbcfd8ce97be292fc9598)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAzureActiveDirectory")
    def put_azure_active_directory(
        self,
        *,
        admin_group_object_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        azure_rbac_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tenant_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param admin_group_object_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#admin_group_object_ids ArcKubernetesProvisionedCluster#admin_group_object_ids}.
        :param azure_rbac_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#azure_rbac_enabled ArcKubernetesProvisionedCluster#azure_rbac_enabled}.
        :param tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#tenant_id ArcKubernetesProvisionedCluster#tenant_id}.
        '''
        value = ArcKubernetesProvisionedClusterAzureActiveDirectory(
            admin_group_object_ids=admin_group_object_ids,
            azure_rbac_enabled=azure_rbac_enabled,
            tenant_id=tenant_id,
        )

        return typing.cast(None, jsii.invoke(self, "putAzureActiveDirectory", [value]))

    @jsii.member(jsii_name="putIdentity")
    def put_identity(self, *, type: builtins.str) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#type ArcKubernetesProvisionedCluster#type}.
        '''
        value = ArcKubernetesProvisionedClusterIdentity(type=type)

        return typing.cast(None, jsii.invoke(self, "putIdentity", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#create ArcKubernetesProvisionedCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#delete ArcKubernetesProvisionedCluster#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#read ArcKubernetesProvisionedCluster#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#update ArcKubernetesProvisionedCluster#update}.
        '''
        value = ArcKubernetesProvisionedClusterTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetArcAgentAutoUpgradeEnabled")
    def reset_arc_agent_auto_upgrade_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArcAgentAutoUpgradeEnabled", []))

    @jsii.member(jsii_name="resetArcAgentDesiredVersion")
    def reset_arc_agent_desired_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArcAgentDesiredVersion", []))

    @jsii.member(jsii_name="resetAzureActiveDirectory")
    def reset_azure_active_directory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureActiveDirectory", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

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
    @jsii.member(jsii_name="agentVersion")
    def agent_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agentVersion"))

    @builtins.property
    @jsii.member(jsii_name="azureActiveDirectory")
    def azure_active_directory(
        self,
    ) -> "ArcKubernetesProvisionedClusterAzureActiveDirectoryOutputReference":
        return typing.cast("ArcKubernetesProvisionedClusterAzureActiveDirectoryOutputReference", jsii.get(self, "azureActiveDirectory"))

    @builtins.property
    @jsii.member(jsii_name="distribution")
    def distribution(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "distribution"))

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> "ArcKubernetesProvisionedClusterIdentityOutputReference":
        return typing.cast("ArcKubernetesProvisionedClusterIdentityOutputReference", jsii.get(self, "identity"))

    @builtins.property
    @jsii.member(jsii_name="infrastructure")
    def infrastructure(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "infrastructure"))

    @builtins.property
    @jsii.member(jsii_name="kubernetesVersion")
    def kubernetes_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kubernetesVersion"))

    @builtins.property
    @jsii.member(jsii_name="offering")
    def offering(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "offering"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ArcKubernetesProvisionedClusterTimeoutsOutputReference":
        return typing.cast("ArcKubernetesProvisionedClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="totalCoreCount")
    def total_core_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "totalCoreCount"))

    @builtins.property
    @jsii.member(jsii_name="totalNodeCount")
    def total_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "totalNodeCount"))

    @builtins.property
    @jsii.member(jsii_name="arcAgentAutoUpgradeEnabledInput")
    def arc_agent_auto_upgrade_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "arcAgentAutoUpgradeEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="arcAgentDesiredVersionInput")
    def arc_agent_desired_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "arcAgentDesiredVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="azureActiveDirectoryInput")
    def azure_active_directory_input(
        self,
    ) -> typing.Optional["ArcKubernetesProvisionedClusterAzureActiveDirectory"]:
        return typing.cast(typing.Optional["ArcKubernetesProvisionedClusterAzureActiveDirectory"], jsii.get(self, "azureActiveDirectoryInput"))

    @builtins.property
    @jsii.member(jsii_name="identityInput")
    def identity_input(
        self,
    ) -> typing.Optional["ArcKubernetesProvisionedClusterIdentity"]:
        return typing.cast(typing.Optional["ArcKubernetesProvisionedClusterIdentity"], jsii.get(self, "identityInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ArcKubernetesProvisionedClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ArcKubernetesProvisionedClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="arcAgentAutoUpgradeEnabled")
    def arc_agent_auto_upgrade_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "arcAgentAutoUpgradeEnabled"))

    @arc_agent_auto_upgrade_enabled.setter
    def arc_agent_auto_upgrade_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d553c38c7b8019d501ba841f18b77f886ebbb7ad42d63a939a9071f060eaa9ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "arcAgentAutoUpgradeEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="arcAgentDesiredVersion")
    def arc_agent_desired_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arcAgentDesiredVersion"))

    @arc_agent_desired_version.setter
    def arc_agent_desired_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__509fe758bfd3d644c5b1552ee1f9025d7a95436755409c46312a919c14bf655f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "arcAgentDesiredVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daf44b4269ce45b61ac559f4fd54bfa545ed75fd51fc7737b936ff5e2ecdeb24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1483936b2999cd8fe815ab5e88e9516071457c3556b1e45b11e235bed3c1427)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ea9ea1bf1b7685d80a95d0c16298510ec2ee75e55b395e88ace71e85b7baf8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__995966eb33b2e9b01296006e1551e5a4df346cf59f811cbfb526a4a4fdac5d1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b64ced9408be5d78e87cdbd414e40e361e73db8301ecc64302d9b8f08d058468)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.arcKubernetesProvisionedCluster.ArcKubernetesProvisionedClusterAzureActiveDirectory",
    jsii_struct_bases=[],
    name_mapping={
        "admin_group_object_ids": "adminGroupObjectIds",
        "azure_rbac_enabled": "azureRbacEnabled",
        "tenant_id": "tenantId",
    },
)
class ArcKubernetesProvisionedClusterAzureActiveDirectory:
    def __init__(
        self,
        *,
        admin_group_object_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        azure_rbac_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tenant_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param admin_group_object_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#admin_group_object_ids ArcKubernetesProvisionedCluster#admin_group_object_ids}.
        :param azure_rbac_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#azure_rbac_enabled ArcKubernetesProvisionedCluster#azure_rbac_enabled}.
        :param tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#tenant_id ArcKubernetesProvisionedCluster#tenant_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69c237341a94d99d78da696a1343781452a015bd2750dfb461e58c07c4c4925c)
            check_type(argname="argument admin_group_object_ids", value=admin_group_object_ids, expected_type=type_hints["admin_group_object_ids"])
            check_type(argname="argument azure_rbac_enabled", value=azure_rbac_enabled, expected_type=type_hints["azure_rbac_enabled"])
            check_type(argname="argument tenant_id", value=tenant_id, expected_type=type_hints["tenant_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if admin_group_object_ids is not None:
            self._values["admin_group_object_ids"] = admin_group_object_ids
        if azure_rbac_enabled is not None:
            self._values["azure_rbac_enabled"] = azure_rbac_enabled
        if tenant_id is not None:
            self._values["tenant_id"] = tenant_id

    @builtins.property
    def admin_group_object_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#admin_group_object_ids ArcKubernetesProvisionedCluster#admin_group_object_ids}.'''
        result = self._values.get("admin_group_object_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def azure_rbac_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#azure_rbac_enabled ArcKubernetesProvisionedCluster#azure_rbac_enabled}.'''
        result = self._values.get("azure_rbac_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tenant_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#tenant_id ArcKubernetesProvisionedCluster#tenant_id}.'''
        result = self._values.get("tenant_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArcKubernetesProvisionedClusterAzureActiveDirectory(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArcKubernetesProvisionedClusterAzureActiveDirectoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.arcKubernetesProvisionedCluster.ArcKubernetesProvisionedClusterAzureActiveDirectoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef5fc0814b842b118f34011fc5316accaeaa1f410a7b0f85783e301c5a1595e4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAdminGroupObjectIds")
    def reset_admin_group_object_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminGroupObjectIds", []))

    @jsii.member(jsii_name="resetAzureRbacEnabled")
    def reset_azure_rbac_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureRbacEnabled", []))

    @jsii.member(jsii_name="resetTenantId")
    def reset_tenant_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTenantId", []))

    @builtins.property
    @jsii.member(jsii_name="adminGroupObjectIdsInput")
    def admin_group_object_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "adminGroupObjectIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="azureRbacEnabledInput")
    def azure_rbac_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "azureRbacEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="tenantIdInput")
    def tenant_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantIdInput"))

    @builtins.property
    @jsii.member(jsii_name="adminGroupObjectIds")
    def admin_group_object_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "adminGroupObjectIds"))

    @admin_group_object_ids.setter
    def admin_group_object_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89b845b3170db34f6e57157d92caa8dfeb89f5ef254dbc11d86ca5f55b9fab13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminGroupObjectIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="azureRbacEnabled")
    def azure_rbac_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "azureRbacEnabled"))

    @azure_rbac_enabled.setter
    def azure_rbac_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4271e4ab51557e5c2c310efc78301284619c217eb80c35c5a86c3074ef74767)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "azureRbacEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @tenant_id.setter
    def tenant_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9974015855e91a7868d409eb4ad4b84f689797df0f0d22249683e0516df77f7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenantId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ArcKubernetesProvisionedClusterAzureActiveDirectory]:
        return typing.cast(typing.Optional[ArcKubernetesProvisionedClusterAzureActiveDirectory], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ArcKubernetesProvisionedClusterAzureActiveDirectory],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__256e26c3e25edd965de612c86ca627fa8163678d3c56b1e242ab784cecc08c91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.arcKubernetesProvisionedCluster.ArcKubernetesProvisionedClusterConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "identity": "identity",
        "location": "location",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "arc_agent_auto_upgrade_enabled": "arcAgentAutoUpgradeEnabled",
        "arc_agent_desired_version": "arcAgentDesiredVersion",
        "azure_active_directory": "azureActiveDirectory",
        "id": "id",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class ArcKubernetesProvisionedClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        identity: typing.Union["ArcKubernetesProvisionedClusterIdentity", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        arc_agent_auto_upgrade_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        arc_agent_desired_version: typing.Optional[builtins.str] = None,
        azure_active_directory: typing.Optional[typing.Union[ArcKubernetesProvisionedClusterAzureActiveDirectory, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ArcKubernetesProvisionedClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#identity ArcKubernetesProvisionedCluster#identity}
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#location ArcKubernetesProvisionedCluster#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#name ArcKubernetesProvisionedCluster#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#resource_group_name ArcKubernetesProvisionedCluster#resource_group_name}.
        :param arc_agent_auto_upgrade_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#arc_agent_auto_upgrade_enabled ArcKubernetesProvisionedCluster#arc_agent_auto_upgrade_enabled}.
        :param arc_agent_desired_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#arc_agent_desired_version ArcKubernetesProvisionedCluster#arc_agent_desired_version}.
        :param azure_active_directory: azure_active_directory block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#azure_active_directory ArcKubernetesProvisionedCluster#azure_active_directory}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#id ArcKubernetesProvisionedCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#tags ArcKubernetesProvisionedCluster#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#timeouts ArcKubernetesProvisionedCluster#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(identity, dict):
            identity = ArcKubernetesProvisionedClusterIdentity(**identity)
        if isinstance(azure_active_directory, dict):
            azure_active_directory = ArcKubernetesProvisionedClusterAzureActiveDirectory(**azure_active_directory)
        if isinstance(timeouts, dict):
            timeouts = ArcKubernetesProvisionedClusterTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff2f4d295c16e205b8ae2834bb40a54ed7283b6535af0d6fb8f0c9202770af3e)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument arc_agent_auto_upgrade_enabled", value=arc_agent_auto_upgrade_enabled, expected_type=type_hints["arc_agent_auto_upgrade_enabled"])
            check_type(argname="argument arc_agent_desired_version", value=arc_agent_desired_version, expected_type=type_hints["arc_agent_desired_version"])
            check_type(argname="argument azure_active_directory", value=azure_active_directory, expected_type=type_hints["azure_active_directory"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "identity": identity,
            "location": location,
            "name": name,
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
        if arc_agent_auto_upgrade_enabled is not None:
            self._values["arc_agent_auto_upgrade_enabled"] = arc_agent_auto_upgrade_enabled
        if arc_agent_desired_version is not None:
            self._values["arc_agent_desired_version"] = arc_agent_desired_version
        if azure_active_directory is not None:
            self._values["azure_active_directory"] = azure_active_directory
        if id is not None:
            self._values["id"] = id
        if tags is not None:
            self._values["tags"] = tags
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
    def identity(self) -> "ArcKubernetesProvisionedClusterIdentity":
        '''identity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#identity ArcKubernetesProvisionedCluster#identity}
        '''
        result = self._values.get("identity")
        assert result is not None, "Required property 'identity' is missing"
        return typing.cast("ArcKubernetesProvisionedClusterIdentity", result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#location ArcKubernetesProvisionedCluster#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#name ArcKubernetesProvisionedCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#resource_group_name ArcKubernetesProvisionedCluster#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def arc_agent_auto_upgrade_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#arc_agent_auto_upgrade_enabled ArcKubernetesProvisionedCluster#arc_agent_auto_upgrade_enabled}.'''
        result = self._values.get("arc_agent_auto_upgrade_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def arc_agent_desired_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#arc_agent_desired_version ArcKubernetesProvisionedCluster#arc_agent_desired_version}.'''
        result = self._values.get("arc_agent_desired_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def azure_active_directory(
        self,
    ) -> typing.Optional[ArcKubernetesProvisionedClusterAzureActiveDirectory]:
        '''azure_active_directory block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#azure_active_directory ArcKubernetesProvisionedCluster#azure_active_directory}
        '''
        result = self._values.get("azure_active_directory")
        return typing.cast(typing.Optional[ArcKubernetesProvisionedClusterAzureActiveDirectory], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#id ArcKubernetesProvisionedCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#tags ArcKubernetesProvisionedCluster#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ArcKubernetesProvisionedClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#timeouts ArcKubernetesProvisionedCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ArcKubernetesProvisionedClusterTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArcKubernetesProvisionedClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.arcKubernetesProvisionedCluster.ArcKubernetesProvisionedClusterIdentity",
    jsii_struct_bases=[],
    name_mapping={"type": "type"},
)
class ArcKubernetesProvisionedClusterIdentity:
    def __init__(self, *, type: builtins.str) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#type ArcKubernetesProvisionedCluster#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec439b6bb4617f893a129d12f67a9e242eeebe2f60ffa7ce9de2114e6dd78df4)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#type ArcKubernetesProvisionedCluster#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArcKubernetesProvisionedClusterIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArcKubernetesProvisionedClusterIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.arcKubernetesProvisionedCluster.ArcKubernetesProvisionedClusterIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e35abe2446051ff384e2520045988361c041e6b3c9adf15c5776dbc031b150b2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="principalId")
    def principal_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "principalId"))

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b91adc384855dcc1e2dc0b8ccfc2353cbe929cabea6bf901f9c5410f9e0eb18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ArcKubernetesProvisionedClusterIdentity]:
        return typing.cast(typing.Optional[ArcKubernetesProvisionedClusterIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ArcKubernetesProvisionedClusterIdentity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c1a1c93e61b0df6cea076a75adf884b7520a65c2d50841819fa3b861b307d9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.arcKubernetesProvisionedCluster.ArcKubernetesProvisionedClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class ArcKubernetesProvisionedClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#create ArcKubernetesProvisionedCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#delete ArcKubernetesProvisionedCluster#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#read ArcKubernetesProvisionedCluster#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#update ArcKubernetesProvisionedCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3123f5c5b44356650fbf001b2664b07c57a52494e8e9a5fa849e888f94760c69)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#create ArcKubernetesProvisionedCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#delete ArcKubernetesProvisionedCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#read ArcKubernetesProvisionedCluster#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/arc_kubernetes_provisioned_cluster#update ArcKubernetesProvisionedCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArcKubernetesProvisionedClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArcKubernetesProvisionedClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.arcKubernetesProvisionedCluster.ArcKubernetesProvisionedClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__22b33e0bc48cb39425604ec3f718f3ba29983f46e65b54d49b37d462a651b049)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3924c8ecbcdb56f79f8e26e25f4f52a250beece553670e8f210ac261c7f9ecfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84c5ab2b7cc05d9df40e508fd634ea846b6cb8f89b0cb39d25a5aa0b0c35cc87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea631b10545ff4a7d514a5e710f0f6fae17f6952cd5e014f0c8eae75cce8330a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5553d28e02af5530d9c8883c8c109e36b33b25ea8449ce5eae45d4c5d153628b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ArcKubernetesProvisionedClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ArcKubernetesProvisionedClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ArcKubernetesProvisionedClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3e3ee8f20167c9e4ee8b80e87ebe93f80fe3cbfcb52819df2afc0068eeadd96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ArcKubernetesProvisionedCluster",
    "ArcKubernetesProvisionedClusterAzureActiveDirectory",
    "ArcKubernetesProvisionedClusterAzureActiveDirectoryOutputReference",
    "ArcKubernetesProvisionedClusterConfig",
    "ArcKubernetesProvisionedClusterIdentity",
    "ArcKubernetesProvisionedClusterIdentityOutputReference",
    "ArcKubernetesProvisionedClusterTimeouts",
    "ArcKubernetesProvisionedClusterTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__9234239b2a443c62d5b1f346bce766e8decb4e0dd86ec9d3eaae8affc09666b9(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    identity: typing.Union[ArcKubernetesProvisionedClusterIdentity, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    arc_agent_auto_upgrade_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    arc_agent_desired_version: typing.Optional[builtins.str] = None,
    azure_active_directory: typing.Optional[typing.Union[ArcKubernetesProvisionedClusterAzureActiveDirectory, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ArcKubernetesProvisionedClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__45c6e6ebff28c528d8050be89f436cdc15ef6da32d4cbcfd8ce97be292fc9598(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d553c38c7b8019d501ba841f18b77f886ebbb7ad42d63a939a9071f060eaa9ed(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__509fe758bfd3d644c5b1552ee1f9025d7a95436755409c46312a919c14bf655f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daf44b4269ce45b61ac559f4fd54bfa545ed75fd51fc7737b936ff5e2ecdeb24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1483936b2999cd8fe815ab5e88e9516071457c3556b1e45b11e235bed3c1427(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ea9ea1bf1b7685d80a95d0c16298510ec2ee75e55b395e88ace71e85b7baf8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__995966eb33b2e9b01296006e1551e5a4df346cf59f811cbfb526a4a4fdac5d1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b64ced9408be5d78e87cdbd414e40e361e73db8301ecc64302d9b8f08d058468(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69c237341a94d99d78da696a1343781452a015bd2750dfb461e58c07c4c4925c(
    *,
    admin_group_object_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    azure_rbac_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tenant_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef5fc0814b842b118f34011fc5316accaeaa1f410a7b0f85783e301c5a1595e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89b845b3170db34f6e57157d92caa8dfeb89f5ef254dbc11d86ca5f55b9fab13(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4271e4ab51557e5c2c310efc78301284619c217eb80c35c5a86c3074ef74767(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9974015855e91a7868d409eb4ad4b84f689797df0f0d22249683e0516df77f7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__256e26c3e25edd965de612c86ca627fa8163678d3c56b1e242ab784cecc08c91(
    value: typing.Optional[ArcKubernetesProvisionedClusterAzureActiveDirectory],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff2f4d295c16e205b8ae2834bb40a54ed7283b6535af0d6fb8f0c9202770af3e(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    identity: typing.Union[ArcKubernetesProvisionedClusterIdentity, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    arc_agent_auto_upgrade_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    arc_agent_desired_version: typing.Optional[builtins.str] = None,
    azure_active_directory: typing.Optional[typing.Union[ArcKubernetesProvisionedClusterAzureActiveDirectory, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ArcKubernetesProvisionedClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec439b6bb4617f893a129d12f67a9e242eeebe2f60ffa7ce9de2114e6dd78df4(
    *,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e35abe2446051ff384e2520045988361c041e6b3c9adf15c5776dbc031b150b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b91adc384855dcc1e2dc0b8ccfc2353cbe929cabea6bf901f9c5410f9e0eb18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c1a1c93e61b0df6cea076a75adf884b7520a65c2d50841819fa3b861b307d9b(
    value: typing.Optional[ArcKubernetesProvisionedClusterIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3123f5c5b44356650fbf001b2664b07c57a52494e8e9a5fa849e888f94760c69(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22b33e0bc48cb39425604ec3f718f3ba29983f46e65b54d49b37d462a651b049(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3924c8ecbcdb56f79f8e26e25f4f52a250beece553670e8f210ac261c7f9ecfa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84c5ab2b7cc05d9df40e508fd634ea846b6cb8f89b0cb39d25a5aa0b0c35cc87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea631b10545ff4a7d514a5e710f0f6fae17f6952cd5e014f0c8eae75cce8330a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5553d28e02af5530d9c8883c8c109e36b33b25ea8449ce5eae45d4c5d153628b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3e3ee8f20167c9e4ee8b80e87ebe93f80fe3cbfcb52819df2afc0068eeadd96(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ArcKubernetesProvisionedClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
