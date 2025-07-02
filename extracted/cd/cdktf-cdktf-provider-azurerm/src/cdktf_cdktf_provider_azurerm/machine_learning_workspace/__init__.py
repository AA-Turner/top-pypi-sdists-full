r'''
# `azurerm_machine_learning_workspace`

Refer to the Terraform Registry for docs: [`azurerm_machine_learning_workspace`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace).
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


class MachineLearningWorkspace(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.machineLearningWorkspace.MachineLearningWorkspace",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace azurerm_machine_learning_workspace}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        application_insights_id: builtins.str,
        identity: typing.Union["MachineLearningWorkspaceIdentity", typing.Dict[builtins.str, typing.Any]],
        key_vault_id: builtins.str,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        storage_account_id: builtins.str,
        container_registry_id: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        encryption: typing.Optional[typing.Union["MachineLearningWorkspaceEncryption", typing.Dict[builtins.str, typing.Any]]] = None,
        feature_store: typing.Optional[typing.Union["MachineLearningWorkspaceFeatureStore", typing.Dict[builtins.str, typing.Any]]] = None,
        friendly_name: typing.Optional[builtins.str] = None,
        high_business_impact: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        image_build_compute_name: typing.Optional[builtins.str] = None,
        kind: typing.Optional[builtins.str] = None,
        managed_network: typing.Optional[typing.Union["MachineLearningWorkspaceManagedNetwork", typing.Dict[builtins.str, typing.Any]]] = None,
        primary_user_assigned_identity: typing.Optional[builtins.str] = None,
        public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        serverless_compute: typing.Optional[typing.Union["MachineLearningWorkspaceServerlessCompute", typing.Dict[builtins.str, typing.Any]]] = None,
        sku_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MachineLearningWorkspaceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        v1_legacy_mode_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace azurerm_machine_learning_workspace} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param application_insights_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#application_insights_id MachineLearningWorkspace#application_insights_id}.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#identity MachineLearningWorkspace#identity}
        :param key_vault_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#key_vault_id MachineLearningWorkspace#key_vault_id}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#location MachineLearningWorkspace#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#name MachineLearningWorkspace#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#resource_group_name MachineLearningWorkspace#resource_group_name}.
        :param storage_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#storage_account_id MachineLearningWorkspace#storage_account_id}.
        :param container_registry_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#container_registry_id MachineLearningWorkspace#container_registry_id}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#description MachineLearningWorkspace#description}.
        :param encryption: encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#encryption MachineLearningWorkspace#encryption}
        :param feature_store: feature_store block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#feature_store MachineLearningWorkspace#feature_store}
        :param friendly_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#friendly_name MachineLearningWorkspace#friendly_name}.
        :param high_business_impact: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#high_business_impact MachineLearningWorkspace#high_business_impact}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#id MachineLearningWorkspace#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image_build_compute_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#image_build_compute_name MachineLearningWorkspace#image_build_compute_name}.
        :param kind: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#kind MachineLearningWorkspace#kind}.
        :param managed_network: managed_network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#managed_network MachineLearningWorkspace#managed_network}
        :param primary_user_assigned_identity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#primary_user_assigned_identity MachineLearningWorkspace#primary_user_assigned_identity}.
        :param public_network_access_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#public_network_access_enabled MachineLearningWorkspace#public_network_access_enabled}.
        :param serverless_compute: serverless_compute block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#serverless_compute MachineLearningWorkspace#serverless_compute}
        :param sku_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#sku_name MachineLearningWorkspace#sku_name}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#tags MachineLearningWorkspace#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#timeouts MachineLearningWorkspace#timeouts}
        :param v1_legacy_mode_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#v1_legacy_mode_enabled MachineLearningWorkspace#v1_legacy_mode_enabled}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdd26fffe8b0fc4beb6d8154345cf87a5d69d2ca754b1195d794971c2a14c6f8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MachineLearningWorkspaceConfig(
            application_insights_id=application_insights_id,
            identity=identity,
            key_vault_id=key_vault_id,
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            storage_account_id=storage_account_id,
            container_registry_id=container_registry_id,
            description=description,
            encryption=encryption,
            feature_store=feature_store,
            friendly_name=friendly_name,
            high_business_impact=high_business_impact,
            id=id,
            image_build_compute_name=image_build_compute_name,
            kind=kind,
            managed_network=managed_network,
            primary_user_assigned_identity=primary_user_assigned_identity,
            public_network_access_enabled=public_network_access_enabled,
            serverless_compute=serverless_compute,
            sku_name=sku_name,
            tags=tags,
            timeouts=timeouts,
            v1_legacy_mode_enabled=v1_legacy_mode_enabled,
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
        '''Generates CDKTF code for importing a MachineLearningWorkspace resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the MachineLearningWorkspace to import.
        :param import_from_id: The id of the existing MachineLearningWorkspace that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the MachineLearningWorkspace to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0e5da3dcbdde976100e2acf47ac791a5af471011485ceaf0e83cffc7d54e31d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEncryption")
    def put_encryption(
        self,
        *,
        key_id: builtins.str,
        key_vault_id: builtins.str,
        user_assigned_identity_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#key_id MachineLearningWorkspace#key_id}.
        :param key_vault_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#key_vault_id MachineLearningWorkspace#key_vault_id}.
        :param user_assigned_identity_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#user_assigned_identity_id MachineLearningWorkspace#user_assigned_identity_id}.
        '''
        value = MachineLearningWorkspaceEncryption(
            key_id=key_id,
            key_vault_id=key_vault_id,
            user_assigned_identity_id=user_assigned_identity_id,
        )

        return typing.cast(None, jsii.invoke(self, "putEncryption", [value]))

    @jsii.member(jsii_name="putFeatureStore")
    def put_feature_store(
        self,
        *,
        computer_spark_runtime_version: typing.Optional[builtins.str] = None,
        offline_connection_name: typing.Optional[builtins.str] = None,
        online_connection_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param computer_spark_runtime_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#computer_spark_runtime_version MachineLearningWorkspace#computer_spark_runtime_version}.
        :param offline_connection_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#offline_connection_name MachineLearningWorkspace#offline_connection_name}.
        :param online_connection_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#online_connection_name MachineLearningWorkspace#online_connection_name}.
        '''
        value = MachineLearningWorkspaceFeatureStore(
            computer_spark_runtime_version=computer_spark_runtime_version,
            offline_connection_name=offline_connection_name,
            online_connection_name=online_connection_name,
        )

        return typing.cast(None, jsii.invoke(self, "putFeatureStore", [value]))

    @jsii.member(jsii_name="putIdentity")
    def put_identity(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#type MachineLearningWorkspace#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#identity_ids MachineLearningWorkspace#identity_ids}.
        '''
        value = MachineLearningWorkspaceIdentity(type=type, identity_ids=identity_ids)

        return typing.cast(None, jsii.invoke(self, "putIdentity", [value]))

    @jsii.member(jsii_name="putManagedNetwork")
    def put_managed_network(
        self,
        *,
        isolation_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param isolation_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#isolation_mode MachineLearningWorkspace#isolation_mode}.
        '''
        value = MachineLearningWorkspaceManagedNetwork(isolation_mode=isolation_mode)

        return typing.cast(None, jsii.invoke(self, "putManagedNetwork", [value]))

    @jsii.member(jsii_name="putServerlessCompute")
    def put_serverless_compute(
        self,
        *,
        public_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param public_ip_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#public_ip_enabled MachineLearningWorkspace#public_ip_enabled}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#subnet_id MachineLearningWorkspace#subnet_id}.
        '''
        value = MachineLearningWorkspaceServerlessCompute(
            public_ip_enabled=public_ip_enabled, subnet_id=subnet_id
        )

        return typing.cast(None, jsii.invoke(self, "putServerlessCompute", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#create MachineLearningWorkspace#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#delete MachineLearningWorkspace#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#read MachineLearningWorkspace#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#update MachineLearningWorkspace#update}.
        '''
        value = MachineLearningWorkspaceTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetContainerRegistryId")
    def reset_container_registry_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerRegistryId", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEncryption")
    def reset_encryption(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryption", []))

    @jsii.member(jsii_name="resetFeatureStore")
    def reset_feature_store(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFeatureStore", []))

    @jsii.member(jsii_name="resetFriendlyName")
    def reset_friendly_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFriendlyName", []))

    @jsii.member(jsii_name="resetHighBusinessImpact")
    def reset_high_business_impact(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHighBusinessImpact", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetImageBuildComputeName")
    def reset_image_build_compute_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageBuildComputeName", []))

    @jsii.member(jsii_name="resetKind")
    def reset_kind(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKind", []))

    @jsii.member(jsii_name="resetManagedNetwork")
    def reset_managed_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedNetwork", []))

    @jsii.member(jsii_name="resetPrimaryUserAssignedIdentity")
    def reset_primary_user_assigned_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryUserAssignedIdentity", []))

    @jsii.member(jsii_name="resetPublicNetworkAccessEnabled")
    def reset_public_network_access_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicNetworkAccessEnabled", []))

    @jsii.member(jsii_name="resetServerlessCompute")
    def reset_serverless_compute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerlessCompute", []))

    @jsii.member(jsii_name="resetSkuName")
    def reset_sku_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkuName", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetV1LegacyModeEnabled")
    def reset_v1_legacy_mode_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetV1LegacyModeEnabled", []))

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
    @jsii.member(jsii_name="discoveryUrl")
    def discovery_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "discoveryUrl"))

    @builtins.property
    @jsii.member(jsii_name="encryption")
    def encryption(self) -> "MachineLearningWorkspaceEncryptionOutputReference":
        return typing.cast("MachineLearningWorkspaceEncryptionOutputReference", jsii.get(self, "encryption"))

    @builtins.property
    @jsii.member(jsii_name="featureStore")
    def feature_store(self) -> "MachineLearningWorkspaceFeatureStoreOutputReference":
        return typing.cast("MachineLearningWorkspaceFeatureStoreOutputReference", jsii.get(self, "featureStore"))

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> "MachineLearningWorkspaceIdentityOutputReference":
        return typing.cast("MachineLearningWorkspaceIdentityOutputReference", jsii.get(self, "identity"))

    @builtins.property
    @jsii.member(jsii_name="managedNetwork")
    def managed_network(
        self,
    ) -> "MachineLearningWorkspaceManagedNetworkOutputReference":
        return typing.cast("MachineLearningWorkspaceManagedNetworkOutputReference", jsii.get(self, "managedNetwork"))

    @builtins.property
    @jsii.member(jsii_name="serverlessCompute")
    def serverless_compute(
        self,
    ) -> "MachineLearningWorkspaceServerlessComputeOutputReference":
        return typing.cast("MachineLearningWorkspaceServerlessComputeOutputReference", jsii.get(self, "serverlessCompute"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "MachineLearningWorkspaceTimeoutsOutputReference":
        return typing.cast("MachineLearningWorkspaceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="workspaceId")
    def workspace_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workspaceId"))

    @builtins.property
    @jsii.member(jsii_name="applicationInsightsIdInput")
    def application_insights_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationInsightsIdInput"))

    @builtins.property
    @jsii.member(jsii_name="containerRegistryIdInput")
    def container_registry_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerRegistryIdInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionInput")
    def encryption_input(self) -> typing.Optional["MachineLearningWorkspaceEncryption"]:
        return typing.cast(typing.Optional["MachineLearningWorkspaceEncryption"], jsii.get(self, "encryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="featureStoreInput")
    def feature_store_input(
        self,
    ) -> typing.Optional["MachineLearningWorkspaceFeatureStore"]:
        return typing.cast(typing.Optional["MachineLearningWorkspaceFeatureStore"], jsii.get(self, "featureStoreInput"))

    @builtins.property
    @jsii.member(jsii_name="friendlyNameInput")
    def friendly_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "friendlyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="highBusinessImpactInput")
    def high_business_impact_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "highBusinessImpactInput"))

    @builtins.property
    @jsii.member(jsii_name="identityInput")
    def identity_input(self) -> typing.Optional["MachineLearningWorkspaceIdentity"]:
        return typing.cast(typing.Optional["MachineLearningWorkspaceIdentity"], jsii.get(self, "identityInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="imageBuildComputeNameInput")
    def image_build_compute_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageBuildComputeNameInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultIdInput")
    def key_vault_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyVaultIdInput"))

    @builtins.property
    @jsii.member(jsii_name="kindInput")
    def kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kindInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="managedNetworkInput")
    def managed_network_input(
        self,
    ) -> typing.Optional["MachineLearningWorkspaceManagedNetwork"]:
        return typing.cast(typing.Optional["MachineLearningWorkspaceManagedNetwork"], jsii.get(self, "managedNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryUserAssignedIdentityInput")
    def primary_user_assigned_identity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "primaryUserAssignedIdentityInput"))

    @builtins.property
    @jsii.member(jsii_name="publicNetworkAccessEnabledInput")
    def public_network_access_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "publicNetworkAccessEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="serverlessComputeInput")
    def serverless_compute_input(
        self,
    ) -> typing.Optional["MachineLearningWorkspaceServerlessCompute"]:
        return typing.cast(typing.Optional["MachineLearningWorkspaceServerlessCompute"], jsii.get(self, "serverlessComputeInput"))

    @builtins.property
    @jsii.member(jsii_name="skuNameInput")
    def sku_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "skuNameInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountIdInput")
    def storage_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MachineLearningWorkspaceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MachineLearningWorkspaceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="v1LegacyModeEnabledInput")
    def v1_legacy_mode_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "v1LegacyModeEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationInsightsId")
    def application_insights_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationInsightsId"))

    @application_insights_id.setter
    def application_insights_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46dae51e3be224007d6c6bb49f307393ae181dc29f89ea46ec8d1498614d6c8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationInsightsId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="containerRegistryId")
    def container_registry_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerRegistryId"))

    @container_registry_id.setter
    def container_registry_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c2dbf73b33f03a723c28f17d16b8e698592e46beece77fcc9182e936627e0af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerRegistryId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44c85b93c06e23450044972bd860f0740325094cf3d5fd84adfd70491571824d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="friendlyName")
    def friendly_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "friendlyName"))

    @friendly_name.setter
    def friendly_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6274ef853140249d9158f917305566420faae44955944b5d9d352d414f65aa5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "friendlyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="highBusinessImpact")
    def high_business_impact(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "highBusinessImpact"))

    @high_business_impact.setter
    def high_business_impact(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbb65822ce44c1bda65c2e084ba5a24b310c1d4bf2f7783ad06838104eae912c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "highBusinessImpact", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b71d49b48cbdd6f94388622ca44dd75bcca5c0d4bc24d24166d4ad50a088c41b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageBuildComputeName")
    def image_build_compute_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageBuildComputeName"))

    @image_build_compute_name.setter
    def image_build_compute_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b43eb42e79ade3a51dc419a2f8c30c7778f56be2b3ed6ef1c93e38efb0ec705c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageBuildComputeName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyVaultId")
    def key_vault_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultId"))

    @key_vault_id.setter
    def key_vault_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45183795b1dd071b12b404190e2e7929ba89edc6415c4a1fb4f5765ff102117d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kind"))

    @kind.setter
    def kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c42c8a1e36c5e0be9c34d85071c9a4aa38efac0887ab0daa34e812156d1bc9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ab78d156f76948371139d59049eacabc44787894e3b07f853d8024e44fdbaff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f72587a53e01e2404a13acecb1580cdd4183873e752118a960e645c9d24dad76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="primaryUserAssignedIdentity")
    def primary_user_assigned_identity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryUserAssignedIdentity"))

    @primary_user_assigned_identity.setter
    def primary_user_assigned_identity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ef5a416be162f61a55a074efaea1b074bbcf9901fe8d9b2888450902c92138b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryUserAssignedIdentity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicNetworkAccessEnabled")
    def public_network_access_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "publicNetworkAccessEnabled"))

    @public_network_access_enabled.setter
    def public_network_access_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba8342c9b7371f3f04a9b0380c338c45896547c4ecfba8edd961125b8df967c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicNetworkAccessEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85a5ec5c2cfc20dc582874ba1af31e7cd717bf606fff0e5233c5aa52a06cd997)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skuName")
    def sku_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "skuName"))

    @sku_name.setter
    def sku_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31be4917da1abb8844314e7b794e2b520d0eed3f69a1e11a95ef0dccc905782b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skuName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageAccountId")
    def storage_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountId"))

    @storage_account_id.setter
    def storage_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__090cbc65e21f8315e91ede02949256fde437c19e582b1bb0a03b83bc4e8da4cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ee3e6449ec1784ee132f97cf16faf6a679492ff8b531cac984a65290fc13ed4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="v1LegacyModeEnabled")
    def v1_legacy_mode_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "v1LegacyModeEnabled"))

    @v1_legacy_mode_enabled.setter
    def v1_legacy_mode_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e695bbc43535d870f3352d86cc216c5e53f980ea4716eb362c4a53d06a6d7595)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "v1LegacyModeEnabled", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.machineLearningWorkspace.MachineLearningWorkspaceConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "application_insights_id": "applicationInsightsId",
        "identity": "identity",
        "key_vault_id": "keyVaultId",
        "location": "location",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "storage_account_id": "storageAccountId",
        "container_registry_id": "containerRegistryId",
        "description": "description",
        "encryption": "encryption",
        "feature_store": "featureStore",
        "friendly_name": "friendlyName",
        "high_business_impact": "highBusinessImpact",
        "id": "id",
        "image_build_compute_name": "imageBuildComputeName",
        "kind": "kind",
        "managed_network": "managedNetwork",
        "primary_user_assigned_identity": "primaryUserAssignedIdentity",
        "public_network_access_enabled": "publicNetworkAccessEnabled",
        "serverless_compute": "serverlessCompute",
        "sku_name": "skuName",
        "tags": "tags",
        "timeouts": "timeouts",
        "v1_legacy_mode_enabled": "v1LegacyModeEnabled",
    },
)
class MachineLearningWorkspaceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        application_insights_id: builtins.str,
        identity: typing.Union["MachineLearningWorkspaceIdentity", typing.Dict[builtins.str, typing.Any]],
        key_vault_id: builtins.str,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        storage_account_id: builtins.str,
        container_registry_id: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        encryption: typing.Optional[typing.Union["MachineLearningWorkspaceEncryption", typing.Dict[builtins.str, typing.Any]]] = None,
        feature_store: typing.Optional[typing.Union["MachineLearningWorkspaceFeatureStore", typing.Dict[builtins.str, typing.Any]]] = None,
        friendly_name: typing.Optional[builtins.str] = None,
        high_business_impact: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        image_build_compute_name: typing.Optional[builtins.str] = None,
        kind: typing.Optional[builtins.str] = None,
        managed_network: typing.Optional[typing.Union["MachineLearningWorkspaceManagedNetwork", typing.Dict[builtins.str, typing.Any]]] = None,
        primary_user_assigned_identity: typing.Optional[builtins.str] = None,
        public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        serverless_compute: typing.Optional[typing.Union["MachineLearningWorkspaceServerlessCompute", typing.Dict[builtins.str, typing.Any]]] = None,
        sku_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MachineLearningWorkspaceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        v1_legacy_mode_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param application_insights_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#application_insights_id MachineLearningWorkspace#application_insights_id}.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#identity MachineLearningWorkspace#identity}
        :param key_vault_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#key_vault_id MachineLearningWorkspace#key_vault_id}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#location MachineLearningWorkspace#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#name MachineLearningWorkspace#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#resource_group_name MachineLearningWorkspace#resource_group_name}.
        :param storage_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#storage_account_id MachineLearningWorkspace#storage_account_id}.
        :param container_registry_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#container_registry_id MachineLearningWorkspace#container_registry_id}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#description MachineLearningWorkspace#description}.
        :param encryption: encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#encryption MachineLearningWorkspace#encryption}
        :param feature_store: feature_store block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#feature_store MachineLearningWorkspace#feature_store}
        :param friendly_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#friendly_name MachineLearningWorkspace#friendly_name}.
        :param high_business_impact: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#high_business_impact MachineLearningWorkspace#high_business_impact}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#id MachineLearningWorkspace#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image_build_compute_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#image_build_compute_name MachineLearningWorkspace#image_build_compute_name}.
        :param kind: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#kind MachineLearningWorkspace#kind}.
        :param managed_network: managed_network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#managed_network MachineLearningWorkspace#managed_network}
        :param primary_user_assigned_identity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#primary_user_assigned_identity MachineLearningWorkspace#primary_user_assigned_identity}.
        :param public_network_access_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#public_network_access_enabled MachineLearningWorkspace#public_network_access_enabled}.
        :param serverless_compute: serverless_compute block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#serverless_compute MachineLearningWorkspace#serverless_compute}
        :param sku_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#sku_name MachineLearningWorkspace#sku_name}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#tags MachineLearningWorkspace#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#timeouts MachineLearningWorkspace#timeouts}
        :param v1_legacy_mode_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#v1_legacy_mode_enabled MachineLearningWorkspace#v1_legacy_mode_enabled}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(identity, dict):
            identity = MachineLearningWorkspaceIdentity(**identity)
        if isinstance(encryption, dict):
            encryption = MachineLearningWorkspaceEncryption(**encryption)
        if isinstance(feature_store, dict):
            feature_store = MachineLearningWorkspaceFeatureStore(**feature_store)
        if isinstance(managed_network, dict):
            managed_network = MachineLearningWorkspaceManagedNetwork(**managed_network)
        if isinstance(serverless_compute, dict):
            serverless_compute = MachineLearningWorkspaceServerlessCompute(**serverless_compute)
        if isinstance(timeouts, dict):
            timeouts = MachineLearningWorkspaceTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf41c5e3fa1e1f1a651109710eab9d6658441c243abbed2af4718ec61a6ed83d)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument application_insights_id", value=application_insights_id, expected_type=type_hints["application_insights_id"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument key_vault_id", value=key_vault_id, expected_type=type_hints["key_vault_id"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument storage_account_id", value=storage_account_id, expected_type=type_hints["storage_account_id"])
            check_type(argname="argument container_registry_id", value=container_registry_id, expected_type=type_hints["container_registry_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument encryption", value=encryption, expected_type=type_hints["encryption"])
            check_type(argname="argument feature_store", value=feature_store, expected_type=type_hints["feature_store"])
            check_type(argname="argument friendly_name", value=friendly_name, expected_type=type_hints["friendly_name"])
            check_type(argname="argument high_business_impact", value=high_business_impact, expected_type=type_hints["high_business_impact"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument image_build_compute_name", value=image_build_compute_name, expected_type=type_hints["image_build_compute_name"])
            check_type(argname="argument kind", value=kind, expected_type=type_hints["kind"])
            check_type(argname="argument managed_network", value=managed_network, expected_type=type_hints["managed_network"])
            check_type(argname="argument primary_user_assigned_identity", value=primary_user_assigned_identity, expected_type=type_hints["primary_user_assigned_identity"])
            check_type(argname="argument public_network_access_enabled", value=public_network_access_enabled, expected_type=type_hints["public_network_access_enabled"])
            check_type(argname="argument serverless_compute", value=serverless_compute, expected_type=type_hints["serverless_compute"])
            check_type(argname="argument sku_name", value=sku_name, expected_type=type_hints["sku_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument v1_legacy_mode_enabled", value=v1_legacy_mode_enabled, expected_type=type_hints["v1_legacy_mode_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_insights_id": application_insights_id,
            "identity": identity,
            "key_vault_id": key_vault_id,
            "location": location,
            "name": name,
            "resource_group_name": resource_group_name,
            "storage_account_id": storage_account_id,
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
        if container_registry_id is not None:
            self._values["container_registry_id"] = container_registry_id
        if description is not None:
            self._values["description"] = description
        if encryption is not None:
            self._values["encryption"] = encryption
        if feature_store is not None:
            self._values["feature_store"] = feature_store
        if friendly_name is not None:
            self._values["friendly_name"] = friendly_name
        if high_business_impact is not None:
            self._values["high_business_impact"] = high_business_impact
        if id is not None:
            self._values["id"] = id
        if image_build_compute_name is not None:
            self._values["image_build_compute_name"] = image_build_compute_name
        if kind is not None:
            self._values["kind"] = kind
        if managed_network is not None:
            self._values["managed_network"] = managed_network
        if primary_user_assigned_identity is not None:
            self._values["primary_user_assigned_identity"] = primary_user_assigned_identity
        if public_network_access_enabled is not None:
            self._values["public_network_access_enabled"] = public_network_access_enabled
        if serverless_compute is not None:
            self._values["serverless_compute"] = serverless_compute
        if sku_name is not None:
            self._values["sku_name"] = sku_name
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if v1_legacy_mode_enabled is not None:
            self._values["v1_legacy_mode_enabled"] = v1_legacy_mode_enabled

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
    def application_insights_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#application_insights_id MachineLearningWorkspace#application_insights_id}.'''
        result = self._values.get("application_insights_id")
        assert result is not None, "Required property 'application_insights_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identity(self) -> "MachineLearningWorkspaceIdentity":
        '''identity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#identity MachineLearningWorkspace#identity}
        '''
        result = self._values.get("identity")
        assert result is not None, "Required property 'identity' is missing"
        return typing.cast("MachineLearningWorkspaceIdentity", result)

    @builtins.property
    def key_vault_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#key_vault_id MachineLearningWorkspace#key_vault_id}.'''
        result = self._values.get("key_vault_id")
        assert result is not None, "Required property 'key_vault_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#location MachineLearningWorkspace#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#name MachineLearningWorkspace#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#resource_group_name MachineLearningWorkspace#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_account_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#storage_account_id MachineLearningWorkspace#storage_account_id}.'''
        result = self._values.get("storage_account_id")
        assert result is not None, "Required property 'storage_account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def container_registry_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#container_registry_id MachineLearningWorkspace#container_registry_id}.'''
        result = self._values.get("container_registry_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#description MachineLearningWorkspace#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption(self) -> typing.Optional["MachineLearningWorkspaceEncryption"]:
        '''encryption block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#encryption MachineLearningWorkspace#encryption}
        '''
        result = self._values.get("encryption")
        return typing.cast(typing.Optional["MachineLearningWorkspaceEncryption"], result)

    @builtins.property
    def feature_store(self) -> typing.Optional["MachineLearningWorkspaceFeatureStore"]:
        '''feature_store block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#feature_store MachineLearningWorkspace#feature_store}
        '''
        result = self._values.get("feature_store")
        return typing.cast(typing.Optional["MachineLearningWorkspaceFeatureStore"], result)

    @builtins.property
    def friendly_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#friendly_name MachineLearningWorkspace#friendly_name}.'''
        result = self._values.get("friendly_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def high_business_impact(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#high_business_impact MachineLearningWorkspace#high_business_impact}.'''
        result = self._values.get("high_business_impact")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#id MachineLearningWorkspace#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_build_compute_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#image_build_compute_name MachineLearningWorkspace#image_build_compute_name}.'''
        result = self._values.get("image_build_compute_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kind(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#kind MachineLearningWorkspace#kind}.'''
        result = self._values.get("kind")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed_network(
        self,
    ) -> typing.Optional["MachineLearningWorkspaceManagedNetwork"]:
        '''managed_network block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#managed_network MachineLearningWorkspace#managed_network}
        '''
        result = self._values.get("managed_network")
        return typing.cast(typing.Optional["MachineLearningWorkspaceManagedNetwork"], result)

    @builtins.property
    def primary_user_assigned_identity(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#primary_user_assigned_identity MachineLearningWorkspace#primary_user_assigned_identity}.'''
        result = self._values.get("primary_user_assigned_identity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_network_access_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#public_network_access_enabled MachineLearningWorkspace#public_network_access_enabled}.'''
        result = self._values.get("public_network_access_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def serverless_compute(
        self,
    ) -> typing.Optional["MachineLearningWorkspaceServerlessCompute"]:
        '''serverless_compute block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#serverless_compute MachineLearningWorkspace#serverless_compute}
        '''
        result = self._values.get("serverless_compute")
        return typing.cast(typing.Optional["MachineLearningWorkspaceServerlessCompute"], result)

    @builtins.property
    def sku_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#sku_name MachineLearningWorkspace#sku_name}.'''
        result = self._values.get("sku_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#tags MachineLearningWorkspace#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["MachineLearningWorkspaceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#timeouts MachineLearningWorkspace#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MachineLearningWorkspaceTimeouts"], result)

    @builtins.property
    def v1_legacy_mode_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#v1_legacy_mode_enabled MachineLearningWorkspace#v1_legacy_mode_enabled}.'''
        result = self._values.get("v1_legacy_mode_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MachineLearningWorkspaceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.machineLearningWorkspace.MachineLearningWorkspaceEncryption",
    jsii_struct_bases=[],
    name_mapping={
        "key_id": "keyId",
        "key_vault_id": "keyVaultId",
        "user_assigned_identity_id": "userAssignedIdentityId",
    },
)
class MachineLearningWorkspaceEncryption:
    def __init__(
        self,
        *,
        key_id: builtins.str,
        key_vault_id: builtins.str,
        user_assigned_identity_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#key_id MachineLearningWorkspace#key_id}.
        :param key_vault_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#key_vault_id MachineLearningWorkspace#key_vault_id}.
        :param user_assigned_identity_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#user_assigned_identity_id MachineLearningWorkspace#user_assigned_identity_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a91264109e09691e529c02d016e43387121fc5791322edcc849c81b05615c0ed)
            check_type(argname="argument key_id", value=key_id, expected_type=type_hints["key_id"])
            check_type(argname="argument key_vault_id", value=key_vault_id, expected_type=type_hints["key_vault_id"])
            check_type(argname="argument user_assigned_identity_id", value=user_assigned_identity_id, expected_type=type_hints["user_assigned_identity_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key_id": key_id,
            "key_vault_id": key_vault_id,
        }
        if user_assigned_identity_id is not None:
            self._values["user_assigned_identity_id"] = user_assigned_identity_id

    @builtins.property
    def key_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#key_id MachineLearningWorkspace#key_id}.'''
        result = self._values.get("key_id")
        assert result is not None, "Required property 'key_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key_vault_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#key_vault_id MachineLearningWorkspace#key_vault_id}.'''
        result = self._values.get("key_vault_id")
        assert result is not None, "Required property 'key_vault_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_assigned_identity_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#user_assigned_identity_id MachineLearningWorkspace#user_assigned_identity_id}.'''
        result = self._values.get("user_assigned_identity_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MachineLearningWorkspaceEncryption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MachineLearningWorkspaceEncryptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.machineLearningWorkspace.MachineLearningWorkspaceEncryptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab40a8fb1ab561592316751ede76a73902d1e2385d36c13c74539b532374d4c1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetUserAssignedIdentityId")
    def reset_user_assigned_identity_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserAssignedIdentityId", []))

    @builtins.property
    @jsii.member(jsii_name="keyIdInput")
    def key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultIdInput")
    def key_vault_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyVaultIdInput"))

    @builtins.property
    @jsii.member(jsii_name="userAssignedIdentityIdInput")
    def user_assigned_identity_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userAssignedIdentityIdInput"))

    @builtins.property
    @jsii.member(jsii_name="keyId")
    def key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyId"))

    @key_id.setter
    def key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfd0c1ee79902cfafbaeb754e24b026b5928a9df8220ec8c437e41321dddb868)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyVaultId")
    def key_vault_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultId"))

    @key_vault_id.setter
    def key_vault_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dd6a189b6629da2077172f685fb62201bba6ef335bf0e566caf6f6c97b3af37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userAssignedIdentityId")
    def user_assigned_identity_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userAssignedIdentityId"))

    @user_assigned_identity_id.setter
    def user_assigned_identity_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbb8b7a03ec24c051bc744e66a1f6325324be21a69d5e91225a7193879fb83c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userAssignedIdentityId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MachineLearningWorkspaceEncryption]:
        return typing.cast(typing.Optional[MachineLearningWorkspaceEncryption], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MachineLearningWorkspaceEncryption],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f291cbdc1def7d5f9102cfa41237b9b4a42d4e9cc1572c4a18c1b9365f92a305)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.machineLearningWorkspace.MachineLearningWorkspaceFeatureStore",
    jsii_struct_bases=[],
    name_mapping={
        "computer_spark_runtime_version": "computerSparkRuntimeVersion",
        "offline_connection_name": "offlineConnectionName",
        "online_connection_name": "onlineConnectionName",
    },
)
class MachineLearningWorkspaceFeatureStore:
    def __init__(
        self,
        *,
        computer_spark_runtime_version: typing.Optional[builtins.str] = None,
        offline_connection_name: typing.Optional[builtins.str] = None,
        online_connection_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param computer_spark_runtime_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#computer_spark_runtime_version MachineLearningWorkspace#computer_spark_runtime_version}.
        :param offline_connection_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#offline_connection_name MachineLearningWorkspace#offline_connection_name}.
        :param online_connection_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#online_connection_name MachineLearningWorkspace#online_connection_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ca262e1529501bbfcd4616f25a35a48dab9e9ee3a35d01d79b14e68ce0f13d8)
            check_type(argname="argument computer_spark_runtime_version", value=computer_spark_runtime_version, expected_type=type_hints["computer_spark_runtime_version"])
            check_type(argname="argument offline_connection_name", value=offline_connection_name, expected_type=type_hints["offline_connection_name"])
            check_type(argname="argument online_connection_name", value=online_connection_name, expected_type=type_hints["online_connection_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if computer_spark_runtime_version is not None:
            self._values["computer_spark_runtime_version"] = computer_spark_runtime_version
        if offline_connection_name is not None:
            self._values["offline_connection_name"] = offline_connection_name
        if online_connection_name is not None:
            self._values["online_connection_name"] = online_connection_name

    @builtins.property
    def computer_spark_runtime_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#computer_spark_runtime_version MachineLearningWorkspace#computer_spark_runtime_version}.'''
        result = self._values.get("computer_spark_runtime_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def offline_connection_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#offline_connection_name MachineLearningWorkspace#offline_connection_name}.'''
        result = self._values.get("offline_connection_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def online_connection_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#online_connection_name MachineLearningWorkspace#online_connection_name}.'''
        result = self._values.get("online_connection_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MachineLearningWorkspaceFeatureStore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MachineLearningWorkspaceFeatureStoreOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.machineLearningWorkspace.MachineLearningWorkspaceFeatureStoreOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2e5bd4bcea9903a69f6928874fe6b5d2f8ffeebbf17c1f666d32163f3d85794)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetComputerSparkRuntimeVersion")
    def reset_computer_spark_runtime_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComputerSparkRuntimeVersion", []))

    @jsii.member(jsii_name="resetOfflineConnectionName")
    def reset_offline_connection_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOfflineConnectionName", []))

    @jsii.member(jsii_name="resetOnlineConnectionName")
    def reset_online_connection_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnlineConnectionName", []))

    @builtins.property
    @jsii.member(jsii_name="computerSparkRuntimeVersionInput")
    def computer_spark_runtime_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "computerSparkRuntimeVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="offlineConnectionNameInput")
    def offline_connection_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "offlineConnectionNameInput"))

    @builtins.property
    @jsii.member(jsii_name="onlineConnectionNameInput")
    def online_connection_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "onlineConnectionNameInput"))

    @builtins.property
    @jsii.member(jsii_name="computerSparkRuntimeVersion")
    def computer_spark_runtime_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "computerSparkRuntimeVersion"))

    @computer_spark_runtime_version.setter
    def computer_spark_runtime_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba07d2d6f4bc9f373c5296fda968b2d456022d99c7c088c1ed1717d1fb877035)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computerSparkRuntimeVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="offlineConnectionName")
    def offline_connection_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "offlineConnectionName"))

    @offline_connection_name.setter
    def offline_connection_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e91372b59657af9b8bf0b425442c35340ceff1fa35e8eb998c19053087095178)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "offlineConnectionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="onlineConnectionName")
    def online_connection_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onlineConnectionName"))

    @online_connection_name.setter
    def online_connection_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7c973296d79d27019d0fe0c72e8a6fca053cb10738aa2e6dd8d917cf227c9d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onlineConnectionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MachineLearningWorkspaceFeatureStore]:
        return typing.cast(typing.Optional[MachineLearningWorkspaceFeatureStore], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MachineLearningWorkspaceFeatureStore],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bac191b3469dd304c9a86753c8ebe0739f90a0e8a1b732d1278758ad946162fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.machineLearningWorkspace.MachineLearningWorkspaceIdentity",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "identity_ids": "identityIds"},
)
class MachineLearningWorkspaceIdentity:
    def __init__(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#type MachineLearningWorkspace#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#identity_ids MachineLearningWorkspace#identity_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0f17ce6fd19f03719d0ab3475f2ee2ca5690aa4d8803cadb20181d3bb701600)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument identity_ids", value=identity_ids, expected_type=type_hints["identity_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if identity_ids is not None:
            self._values["identity_ids"] = identity_ids

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#type MachineLearningWorkspace#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identity_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#identity_ids MachineLearningWorkspace#identity_ids}.'''
        result = self._values.get("identity_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MachineLearningWorkspaceIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MachineLearningWorkspaceIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.machineLearningWorkspace.MachineLearningWorkspaceIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9b379f3aa7807ef9e87d9e70127215940957c08cad3d59848782a3a9ead3b33)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIdentityIds")
    def reset_identity_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityIds", []))

    @builtins.property
    @jsii.member(jsii_name="principalId")
    def principal_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "principalId"))

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @builtins.property
    @jsii.member(jsii_name="identityIdsInput")
    def identity_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "identityIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="identityIds")
    def identity_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "identityIds"))

    @identity_ids.setter
    def identity_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b667496eafd0cb950befe3aea044caf314cbfbb0510a118138aab1aca06ce3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c86015df416c52fc9b82e222a24f9ee018da726cf427b3bfc054a65283ba5ea8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MachineLearningWorkspaceIdentity]:
        return typing.cast(typing.Optional[MachineLearningWorkspaceIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MachineLearningWorkspaceIdentity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78aa45a6e16beb034266205c98d8d19dd732115bc15891ff887bd066c6e1218f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.machineLearningWorkspace.MachineLearningWorkspaceManagedNetwork",
    jsii_struct_bases=[],
    name_mapping={"isolation_mode": "isolationMode"},
)
class MachineLearningWorkspaceManagedNetwork:
    def __init__(self, *, isolation_mode: typing.Optional[builtins.str] = None) -> None:
        '''
        :param isolation_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#isolation_mode MachineLearningWorkspace#isolation_mode}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5435043d36f3cee365b3468bb2054fad4bc4144b117b12fbf5c11b17f4eec1dc)
            check_type(argname="argument isolation_mode", value=isolation_mode, expected_type=type_hints["isolation_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if isolation_mode is not None:
            self._values["isolation_mode"] = isolation_mode

    @builtins.property
    def isolation_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#isolation_mode MachineLearningWorkspace#isolation_mode}.'''
        result = self._values.get("isolation_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MachineLearningWorkspaceManagedNetwork(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MachineLearningWorkspaceManagedNetworkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.machineLearningWorkspace.MachineLearningWorkspaceManagedNetworkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e04699d85fedbc23b04581fd60f33c4c49424acd8bdf222b09b354886f1b7f08)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIsolationMode")
    def reset_isolation_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsolationMode", []))

    @builtins.property
    @jsii.member(jsii_name="isolationModeInput")
    def isolation_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "isolationModeInput"))

    @builtins.property
    @jsii.member(jsii_name="isolationMode")
    def isolation_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "isolationMode"))

    @isolation_mode.setter
    def isolation_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3af9e905681092264e93cf42d02a7fb827d5c8c6fc9a5d52f0a57b6f6489a8d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isolationMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MachineLearningWorkspaceManagedNetwork]:
        return typing.cast(typing.Optional[MachineLearningWorkspaceManagedNetwork], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MachineLearningWorkspaceManagedNetwork],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46d70227fa568adab4d3b3d911c0d85f502438873f0909244b58a67ca1eb0c25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.machineLearningWorkspace.MachineLearningWorkspaceServerlessCompute",
    jsii_struct_bases=[],
    name_mapping={"public_ip_enabled": "publicIpEnabled", "subnet_id": "subnetId"},
)
class MachineLearningWorkspaceServerlessCompute:
    def __init__(
        self,
        *,
        public_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param public_ip_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#public_ip_enabled MachineLearningWorkspace#public_ip_enabled}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#subnet_id MachineLearningWorkspace#subnet_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb3123dffa8c530d6ae79139a3e6f0c943d2e0282bc0053b2bfdc1a1c86928da)
            check_type(argname="argument public_ip_enabled", value=public_ip_enabled, expected_type=type_hints["public_ip_enabled"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if public_ip_enabled is not None:
            self._values["public_ip_enabled"] = public_ip_enabled
        if subnet_id is not None:
            self._values["subnet_id"] = subnet_id

    @builtins.property
    def public_ip_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#public_ip_enabled MachineLearningWorkspace#public_ip_enabled}.'''
        result = self._values.get("public_ip_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#subnet_id MachineLearningWorkspace#subnet_id}.'''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MachineLearningWorkspaceServerlessCompute(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MachineLearningWorkspaceServerlessComputeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.machineLearningWorkspace.MachineLearningWorkspaceServerlessComputeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d098d966f0debe70520b535fabee58da50098f42aed5fd918f7466db73f30246)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPublicIpEnabled")
    def reset_public_ip_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicIpEnabled", []))

    @jsii.member(jsii_name="resetSubnetId")
    def reset_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetId", []))

    @builtins.property
    @jsii.member(jsii_name="publicIpEnabledInput")
    def public_ip_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "publicIpEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__464d548f38f4862f34fd3fdd05262f1558094a081f39ee77301dfe386e8376a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicIpEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43ba32fd7b22ea816b180506063486f83119120cb6f95bf8a2a9d686f967c360)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MachineLearningWorkspaceServerlessCompute]:
        return typing.cast(typing.Optional[MachineLearningWorkspaceServerlessCompute], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MachineLearningWorkspaceServerlessCompute],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5f049c514d78bab156db6cb59f11d1d0483ccbcde2e4524a2a52a09773bbb73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.machineLearningWorkspace.MachineLearningWorkspaceTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class MachineLearningWorkspaceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#create MachineLearningWorkspace#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#delete MachineLearningWorkspace#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#read MachineLearningWorkspace#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#update MachineLearningWorkspace#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dca13852c373e2e0c42aef3a1a450c42ca85d75ebbd7c2d2542e20cb5449c39e)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#create MachineLearningWorkspace#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#delete MachineLearningWorkspace#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#read MachineLearningWorkspace#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/machine_learning_workspace#update MachineLearningWorkspace#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MachineLearningWorkspaceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MachineLearningWorkspaceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.machineLearningWorkspace.MachineLearningWorkspaceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__acf5f27679d393b11f2d6a00e0f273cbc60d87097417c1c2484aeca79efeea9e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4998ed5d30a31ee626dff339b2b86931aeabb600cd66c4329b6ea1ffeb6f2d6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__486fb3aac800c3bd5753b2ec1adfe5b9bee94fa59f87c774f35448f5ac7a4a98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa2293693aaf02748b009753b8b3766168a46b49500967ea67db31b384e12e85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66445d72973ea14496cd78db37b82a8edb2441f10dac27015e162e9f866b188a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MachineLearningWorkspaceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MachineLearningWorkspaceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MachineLearningWorkspaceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bfc4e56538e2e67fb3b9ae7e5a19397c53d17633388077335b158270f25ff89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "MachineLearningWorkspace",
    "MachineLearningWorkspaceConfig",
    "MachineLearningWorkspaceEncryption",
    "MachineLearningWorkspaceEncryptionOutputReference",
    "MachineLearningWorkspaceFeatureStore",
    "MachineLearningWorkspaceFeatureStoreOutputReference",
    "MachineLearningWorkspaceIdentity",
    "MachineLearningWorkspaceIdentityOutputReference",
    "MachineLearningWorkspaceManagedNetwork",
    "MachineLearningWorkspaceManagedNetworkOutputReference",
    "MachineLearningWorkspaceServerlessCompute",
    "MachineLearningWorkspaceServerlessComputeOutputReference",
    "MachineLearningWorkspaceTimeouts",
    "MachineLearningWorkspaceTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__cdd26fffe8b0fc4beb6d8154345cf87a5d69d2ca754b1195d794971c2a14c6f8(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    application_insights_id: builtins.str,
    identity: typing.Union[MachineLearningWorkspaceIdentity, typing.Dict[builtins.str, typing.Any]],
    key_vault_id: builtins.str,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    storage_account_id: builtins.str,
    container_registry_id: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    encryption: typing.Optional[typing.Union[MachineLearningWorkspaceEncryption, typing.Dict[builtins.str, typing.Any]]] = None,
    feature_store: typing.Optional[typing.Union[MachineLearningWorkspaceFeatureStore, typing.Dict[builtins.str, typing.Any]]] = None,
    friendly_name: typing.Optional[builtins.str] = None,
    high_business_impact: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    image_build_compute_name: typing.Optional[builtins.str] = None,
    kind: typing.Optional[builtins.str] = None,
    managed_network: typing.Optional[typing.Union[MachineLearningWorkspaceManagedNetwork, typing.Dict[builtins.str, typing.Any]]] = None,
    primary_user_assigned_identity: typing.Optional[builtins.str] = None,
    public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    serverless_compute: typing.Optional[typing.Union[MachineLearningWorkspaceServerlessCompute, typing.Dict[builtins.str, typing.Any]]] = None,
    sku_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MachineLearningWorkspaceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    v1_legacy_mode_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__c0e5da3dcbdde976100e2acf47ac791a5af471011485ceaf0e83cffc7d54e31d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46dae51e3be224007d6c6bb49f307393ae181dc29f89ea46ec8d1498614d6c8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c2dbf73b33f03a723c28f17d16b8e698592e46beece77fcc9182e936627e0af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44c85b93c06e23450044972bd860f0740325094cf3d5fd84adfd70491571824d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6274ef853140249d9158f917305566420faae44955944b5d9d352d414f65aa5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbb65822ce44c1bda65c2e084ba5a24b310c1d4bf2f7783ad06838104eae912c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b71d49b48cbdd6f94388622ca44dd75bcca5c0d4bc24d24166d4ad50a088c41b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b43eb42e79ade3a51dc419a2f8c30c7778f56be2b3ed6ef1c93e38efb0ec705c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45183795b1dd071b12b404190e2e7929ba89edc6415c4a1fb4f5765ff102117d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c42c8a1e36c5e0be9c34d85071c9a4aa38efac0887ab0daa34e812156d1bc9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ab78d156f76948371139d59049eacabc44787894e3b07f853d8024e44fdbaff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f72587a53e01e2404a13acecb1580cdd4183873e752118a960e645c9d24dad76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ef5a416be162f61a55a074efaea1b074bbcf9901fe8d9b2888450902c92138b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba8342c9b7371f3f04a9b0380c338c45896547c4ecfba8edd961125b8df967c6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85a5ec5c2cfc20dc582874ba1af31e7cd717bf606fff0e5233c5aa52a06cd997(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31be4917da1abb8844314e7b794e2b520d0eed3f69a1e11a95ef0dccc905782b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__090cbc65e21f8315e91ede02949256fde437c19e582b1bb0a03b83bc4e8da4cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ee3e6449ec1784ee132f97cf16faf6a679492ff8b531cac984a65290fc13ed4(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e695bbc43535d870f3352d86cc216c5e53f980ea4716eb362c4a53d06a6d7595(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf41c5e3fa1e1f1a651109710eab9d6658441c243abbed2af4718ec61a6ed83d(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    application_insights_id: builtins.str,
    identity: typing.Union[MachineLearningWorkspaceIdentity, typing.Dict[builtins.str, typing.Any]],
    key_vault_id: builtins.str,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    storage_account_id: builtins.str,
    container_registry_id: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    encryption: typing.Optional[typing.Union[MachineLearningWorkspaceEncryption, typing.Dict[builtins.str, typing.Any]]] = None,
    feature_store: typing.Optional[typing.Union[MachineLearningWorkspaceFeatureStore, typing.Dict[builtins.str, typing.Any]]] = None,
    friendly_name: typing.Optional[builtins.str] = None,
    high_business_impact: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    image_build_compute_name: typing.Optional[builtins.str] = None,
    kind: typing.Optional[builtins.str] = None,
    managed_network: typing.Optional[typing.Union[MachineLearningWorkspaceManagedNetwork, typing.Dict[builtins.str, typing.Any]]] = None,
    primary_user_assigned_identity: typing.Optional[builtins.str] = None,
    public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    serverless_compute: typing.Optional[typing.Union[MachineLearningWorkspaceServerlessCompute, typing.Dict[builtins.str, typing.Any]]] = None,
    sku_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MachineLearningWorkspaceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    v1_legacy_mode_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a91264109e09691e529c02d016e43387121fc5791322edcc849c81b05615c0ed(
    *,
    key_id: builtins.str,
    key_vault_id: builtins.str,
    user_assigned_identity_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab40a8fb1ab561592316751ede76a73902d1e2385d36c13c74539b532374d4c1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfd0c1ee79902cfafbaeb754e24b026b5928a9df8220ec8c437e41321dddb868(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dd6a189b6629da2077172f685fb62201bba6ef335bf0e566caf6f6c97b3af37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbb8b7a03ec24c051bc744e66a1f6325324be21a69d5e91225a7193879fb83c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f291cbdc1def7d5f9102cfa41237b9b4a42d4e9cc1572c4a18c1b9365f92a305(
    value: typing.Optional[MachineLearningWorkspaceEncryption],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ca262e1529501bbfcd4616f25a35a48dab9e9ee3a35d01d79b14e68ce0f13d8(
    *,
    computer_spark_runtime_version: typing.Optional[builtins.str] = None,
    offline_connection_name: typing.Optional[builtins.str] = None,
    online_connection_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2e5bd4bcea9903a69f6928874fe6b5d2f8ffeebbf17c1f666d32163f3d85794(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba07d2d6f4bc9f373c5296fda968b2d456022d99c7c088c1ed1717d1fb877035(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e91372b59657af9b8bf0b425442c35340ceff1fa35e8eb998c19053087095178(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7c973296d79d27019d0fe0c72e8a6fca053cb10738aa2e6dd8d917cf227c9d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bac191b3469dd304c9a86753c8ebe0739f90a0e8a1b732d1278758ad946162fe(
    value: typing.Optional[MachineLearningWorkspaceFeatureStore],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0f17ce6fd19f03719d0ab3475f2ee2ca5690aa4d8803cadb20181d3bb701600(
    *,
    type: builtins.str,
    identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9b379f3aa7807ef9e87d9e70127215940957c08cad3d59848782a3a9ead3b33(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b667496eafd0cb950befe3aea044caf314cbfbb0510a118138aab1aca06ce3e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c86015df416c52fc9b82e222a24f9ee018da726cf427b3bfc054a65283ba5ea8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78aa45a6e16beb034266205c98d8d19dd732115bc15891ff887bd066c6e1218f(
    value: typing.Optional[MachineLearningWorkspaceIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5435043d36f3cee365b3468bb2054fad4bc4144b117b12fbf5c11b17f4eec1dc(
    *,
    isolation_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e04699d85fedbc23b04581fd60f33c4c49424acd8bdf222b09b354886f1b7f08(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3af9e905681092264e93cf42d02a7fb827d5c8c6fc9a5d52f0a57b6f6489a8d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46d70227fa568adab4d3b3d911c0d85f502438873f0909244b58a67ca1eb0c25(
    value: typing.Optional[MachineLearningWorkspaceManagedNetwork],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb3123dffa8c530d6ae79139a3e6f0c943d2e0282bc0053b2bfdc1a1c86928da(
    *,
    public_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    subnet_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d098d966f0debe70520b535fabee58da50098f42aed5fd918f7466db73f30246(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__464d548f38f4862f34fd3fdd05262f1558094a081f39ee77301dfe386e8376a3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43ba32fd7b22ea816b180506063486f83119120cb6f95bf8a2a9d686f967c360(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5f049c514d78bab156db6cb59f11d1d0483ccbcde2e4524a2a52a09773bbb73(
    value: typing.Optional[MachineLearningWorkspaceServerlessCompute],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dca13852c373e2e0c42aef3a1a450c42ca85d75ebbd7c2d2542e20cb5449c39e(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acf5f27679d393b11f2d6a00e0f273cbc60d87097417c1c2484aeca79efeea9e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4998ed5d30a31ee626dff339b2b86931aeabb600cd66c4329b6ea1ffeb6f2d6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__486fb3aac800c3bd5753b2ec1adfe5b9bee94fa59f87c774f35448f5ac7a4a98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa2293693aaf02748b009753b8b3766168a46b49500967ea67db31b384e12e85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66445d72973ea14496cd78db37b82a8edb2441f10dac27015e162e9f866b188a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bfc4e56538e2e67fb3b9ae7e5a19397c53d17633388077335b158270f25ff89(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MachineLearningWorkspaceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
