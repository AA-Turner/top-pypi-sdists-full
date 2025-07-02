r'''
# `azurerm_kusto_cluster`

Refer to the Terraform Registry for docs: [`azurerm_kusto_cluster`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster).
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


class KustoCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kustoCluster.KustoCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster azurerm_kusto_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        sku: typing.Union["KustoClusterSku", typing.Dict[builtins.str, typing.Any]],
        allowed_fqdns: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        auto_stop_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disk_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        double_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["KustoClusterIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        language_extensions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KustoClusterLanguageExtensions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        optimized_auto_scale: typing.Optional[typing.Union["KustoClusterOptimizedAutoScale", typing.Dict[builtins.str, typing.Any]]] = None,
        outbound_network_access_restricted: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        public_ip_type: typing.Optional[builtins.str] = None,
        public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        purge_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        streaming_ingestion_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["KustoClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        trusted_external_tenants: typing.Optional[typing.Sequence[builtins.str]] = None,
        virtual_network_configuration: typing.Optional[typing.Union["KustoClusterVirtualNetworkConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster azurerm_kusto_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#location KustoCluster#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#name KustoCluster#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#resource_group_name KustoCluster#resource_group_name}.
        :param sku: sku block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#sku KustoCluster#sku}
        :param allowed_fqdns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#allowed_fqdns KustoCluster#allowed_fqdns}.
        :param allowed_ip_ranges: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#allowed_ip_ranges KustoCluster#allowed_ip_ranges}.
        :param auto_stop_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#auto_stop_enabled KustoCluster#auto_stop_enabled}.
        :param disk_encryption_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#disk_encryption_enabled KustoCluster#disk_encryption_enabled}.
        :param double_encryption_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#double_encryption_enabled KustoCluster#double_encryption_enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#id KustoCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#identity KustoCluster#identity}
        :param language_extensions: language_extensions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#language_extensions KustoCluster#language_extensions}
        :param optimized_auto_scale: optimized_auto_scale block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#optimized_auto_scale KustoCluster#optimized_auto_scale}
        :param outbound_network_access_restricted: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#outbound_network_access_restricted KustoCluster#outbound_network_access_restricted}.
        :param public_ip_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#public_ip_type KustoCluster#public_ip_type}.
        :param public_network_access_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#public_network_access_enabled KustoCluster#public_network_access_enabled}.
        :param purge_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#purge_enabled KustoCluster#purge_enabled}.
        :param streaming_ingestion_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#streaming_ingestion_enabled KustoCluster#streaming_ingestion_enabled}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#tags KustoCluster#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#timeouts KustoCluster#timeouts}
        :param trusted_external_tenants: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#trusted_external_tenants KustoCluster#trusted_external_tenants}.
        :param virtual_network_configuration: virtual_network_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#virtual_network_configuration KustoCluster#virtual_network_configuration}
        :param zones: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#zones KustoCluster#zones}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9a7fff23a05da91f8143a0a180ddea278a85538968a4da60b38874740bc6a4d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = KustoClusterConfig(
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            sku=sku,
            allowed_fqdns=allowed_fqdns,
            allowed_ip_ranges=allowed_ip_ranges,
            auto_stop_enabled=auto_stop_enabled,
            disk_encryption_enabled=disk_encryption_enabled,
            double_encryption_enabled=double_encryption_enabled,
            id=id,
            identity=identity,
            language_extensions=language_extensions,
            optimized_auto_scale=optimized_auto_scale,
            outbound_network_access_restricted=outbound_network_access_restricted,
            public_ip_type=public_ip_type,
            public_network_access_enabled=public_network_access_enabled,
            purge_enabled=purge_enabled,
            streaming_ingestion_enabled=streaming_ingestion_enabled,
            tags=tags,
            timeouts=timeouts,
            trusted_external_tenants=trusted_external_tenants,
            virtual_network_configuration=virtual_network_configuration,
            zones=zones,
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
        '''Generates CDKTF code for importing a KustoCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the KustoCluster to import.
        :param import_from_id: The id of the existing KustoCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the KustoCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60680647ecb4645b41d195b68fb6b4b608fb3fa6e238a9f219d0c747b238af34)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putIdentity")
    def put_identity(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#type KustoCluster#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#identity_ids KustoCluster#identity_ids}.
        '''
        value = KustoClusterIdentity(type=type, identity_ids=identity_ids)

        return typing.cast(None, jsii.invoke(self, "putIdentity", [value]))

    @jsii.member(jsii_name="putLanguageExtensions")
    def put_language_extensions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KustoClusterLanguageExtensions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05f60f52b65ca385d49617de5536ab6567190f6abc605ca8b3414b5f93735746)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLanguageExtensions", [value]))

    @jsii.member(jsii_name="putOptimizedAutoScale")
    def put_optimized_auto_scale(
        self,
        *,
        maximum_instances: jsii.Number,
        minimum_instances: jsii.Number,
    ) -> None:
        '''
        :param maximum_instances: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#maximum_instances KustoCluster#maximum_instances}.
        :param minimum_instances: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#minimum_instances KustoCluster#minimum_instances}.
        '''
        value = KustoClusterOptimizedAutoScale(
            maximum_instances=maximum_instances, minimum_instances=minimum_instances
        )

        return typing.cast(None, jsii.invoke(self, "putOptimizedAutoScale", [value]))

    @jsii.member(jsii_name="putSku")
    def put_sku(
        self,
        *,
        name: builtins.str,
        capacity: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#name KustoCluster#name}.
        :param capacity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#capacity KustoCluster#capacity}.
        '''
        value = KustoClusterSku(name=name, capacity=capacity)

        return typing.cast(None, jsii.invoke(self, "putSku", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#create KustoCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#delete KustoCluster#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#read KustoCluster#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#update KustoCluster#update}.
        '''
        value = KustoClusterTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putVirtualNetworkConfiguration")
    def put_virtual_network_configuration(
        self,
        *,
        data_management_public_ip_id: builtins.str,
        engine_public_ip_id: builtins.str,
        subnet_id: builtins.str,
    ) -> None:
        '''
        :param data_management_public_ip_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#data_management_public_ip_id KustoCluster#data_management_public_ip_id}.
        :param engine_public_ip_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#engine_public_ip_id KustoCluster#engine_public_ip_id}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#subnet_id KustoCluster#subnet_id}.
        '''
        value = KustoClusterVirtualNetworkConfiguration(
            data_management_public_ip_id=data_management_public_ip_id,
            engine_public_ip_id=engine_public_ip_id,
            subnet_id=subnet_id,
        )

        return typing.cast(None, jsii.invoke(self, "putVirtualNetworkConfiguration", [value]))

    @jsii.member(jsii_name="resetAllowedFqdns")
    def reset_allowed_fqdns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedFqdns", []))

    @jsii.member(jsii_name="resetAllowedIpRanges")
    def reset_allowed_ip_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedIpRanges", []))

    @jsii.member(jsii_name="resetAutoStopEnabled")
    def reset_auto_stop_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoStopEnabled", []))

    @jsii.member(jsii_name="resetDiskEncryptionEnabled")
    def reset_disk_encryption_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskEncryptionEnabled", []))

    @jsii.member(jsii_name="resetDoubleEncryptionEnabled")
    def reset_double_encryption_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDoubleEncryptionEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdentity")
    def reset_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentity", []))

    @jsii.member(jsii_name="resetLanguageExtensions")
    def reset_language_extensions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLanguageExtensions", []))

    @jsii.member(jsii_name="resetOptimizedAutoScale")
    def reset_optimized_auto_scale(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOptimizedAutoScale", []))

    @jsii.member(jsii_name="resetOutboundNetworkAccessRestricted")
    def reset_outbound_network_access_restricted(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutboundNetworkAccessRestricted", []))

    @jsii.member(jsii_name="resetPublicIpType")
    def reset_public_ip_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicIpType", []))

    @jsii.member(jsii_name="resetPublicNetworkAccessEnabled")
    def reset_public_network_access_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicNetworkAccessEnabled", []))

    @jsii.member(jsii_name="resetPurgeEnabled")
    def reset_purge_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPurgeEnabled", []))

    @jsii.member(jsii_name="resetStreamingIngestionEnabled")
    def reset_streaming_ingestion_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStreamingIngestionEnabled", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTrustedExternalTenants")
    def reset_trusted_external_tenants(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrustedExternalTenants", []))

    @jsii.member(jsii_name="resetVirtualNetworkConfiguration")
    def reset_virtual_network_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualNetworkConfiguration", []))

    @jsii.member(jsii_name="resetZones")
    def reset_zones(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZones", []))

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
    @jsii.member(jsii_name="dataIngestionUri")
    def data_ingestion_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataIngestionUri"))

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> "KustoClusterIdentityOutputReference":
        return typing.cast("KustoClusterIdentityOutputReference", jsii.get(self, "identity"))

    @builtins.property
    @jsii.member(jsii_name="languageExtensions")
    def language_extensions(self) -> "KustoClusterLanguageExtensionsList":
        return typing.cast("KustoClusterLanguageExtensionsList", jsii.get(self, "languageExtensions"))

    @builtins.property
    @jsii.member(jsii_name="optimizedAutoScale")
    def optimized_auto_scale(self) -> "KustoClusterOptimizedAutoScaleOutputReference":
        return typing.cast("KustoClusterOptimizedAutoScaleOutputReference", jsii.get(self, "optimizedAutoScale"))

    @builtins.property
    @jsii.member(jsii_name="sku")
    def sku(self) -> "KustoClusterSkuOutputReference":
        return typing.cast("KustoClusterSkuOutputReference", jsii.get(self, "sku"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "KustoClusterTimeoutsOutputReference":
        return typing.cast("KustoClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkConfiguration")
    def virtual_network_configuration(
        self,
    ) -> "KustoClusterVirtualNetworkConfigurationOutputReference":
        return typing.cast("KustoClusterVirtualNetworkConfigurationOutputReference", jsii.get(self, "virtualNetworkConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="allowedFqdnsInput")
    def allowed_fqdns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedFqdnsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedIpRangesInput")
    def allowed_ip_ranges_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedIpRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="autoStopEnabledInput")
    def auto_stop_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoStopEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionEnabledInput")
    def disk_encryption_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "diskEncryptionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="doubleEncryptionEnabledInput")
    def double_encryption_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "doubleEncryptionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="identityInput")
    def identity_input(self) -> typing.Optional["KustoClusterIdentity"]:
        return typing.cast(typing.Optional["KustoClusterIdentity"], jsii.get(self, "identityInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="languageExtensionsInput")
    def language_extensions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KustoClusterLanguageExtensions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KustoClusterLanguageExtensions"]]], jsii.get(self, "languageExtensionsInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="optimizedAutoScaleInput")
    def optimized_auto_scale_input(
        self,
    ) -> typing.Optional["KustoClusterOptimizedAutoScale"]:
        return typing.cast(typing.Optional["KustoClusterOptimizedAutoScale"], jsii.get(self, "optimizedAutoScaleInput"))

    @builtins.property
    @jsii.member(jsii_name="outboundNetworkAccessRestrictedInput")
    def outbound_network_access_restricted_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "outboundNetworkAccessRestrictedInput"))

    @builtins.property
    @jsii.member(jsii_name="publicIpTypeInput")
    def public_ip_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicIpTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="publicNetworkAccessEnabledInput")
    def public_network_access_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "publicNetworkAccessEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="purgeEnabledInput")
    def purge_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "purgeEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="skuInput")
    def sku_input(self) -> typing.Optional["KustoClusterSku"]:
        return typing.cast(typing.Optional["KustoClusterSku"], jsii.get(self, "skuInput"))

    @builtins.property
    @jsii.member(jsii_name="streamingIngestionEnabledInput")
    def streaming_ingestion_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "streamingIngestionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "KustoClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "KustoClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="trustedExternalTenantsInput")
    def trusted_external_tenants_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "trustedExternalTenantsInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkConfigurationInput")
    def virtual_network_configuration_input(
        self,
    ) -> typing.Optional["KustoClusterVirtualNetworkConfiguration"]:
        return typing.cast(typing.Optional["KustoClusterVirtualNetworkConfiguration"], jsii.get(self, "virtualNetworkConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="zonesInput")
    def zones_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "zonesInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedFqdns")
    def allowed_fqdns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedFqdns"))

    @allowed_fqdns.setter
    def allowed_fqdns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50ea96f924d1d44d34c7bd3187119c1645e754f9856234d092a966e6f34c9209)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedFqdns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedIpRanges")
    def allowed_ip_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedIpRanges"))

    @allowed_ip_ranges.setter
    def allowed_ip_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf54a55fe90e960da698908a48a00687e9220c0847b5cd8a0b90222df514900f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedIpRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autoStopEnabled")
    def auto_stop_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoStopEnabled"))

    @auto_stop_enabled.setter
    def auto_stop_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c60d81a8d0c10456679b5a4d3c98185c82ac580eb850598d301ef649348ae2c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoStopEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionEnabled")
    def disk_encryption_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "diskEncryptionEnabled"))

    @disk_encryption_enabled.setter
    def disk_encryption_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0173dde998bf4e3d1f1386d6581830cd591e3da45156871c1a708aa6a948d342)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskEncryptionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="doubleEncryptionEnabled")
    def double_encryption_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "doubleEncryptionEnabled"))

    @double_encryption_enabled.setter
    def double_encryption_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__670e034c5ad20a0397b2441061c07aa893b27f3d6e75b86ca71868b0e3fff168)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "doubleEncryptionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64d253591ffb1a4cbdcf50cb7c3fb0033c45135a98a19553231223b08d439ac1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53d4d6268583770d64ab1fbf1d30d4c2f81d1cca1c83befedfdaea47d93a2ed4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3668f3b4f78833296bbe739635df074a681d39922c8abc28e11adbe30a32db8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outboundNetworkAccessRestricted")
    def outbound_network_access_restricted(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "outboundNetworkAccessRestricted"))

    @outbound_network_access_restricted.setter
    def outbound_network_access_restricted(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d46189776cbd3ef7a80f04a8d20a2ee4824b1ad7ea4eb2c44d2d9ef3b3d73bfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outboundNetworkAccessRestricted", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicIpType")
    def public_ip_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicIpType"))

    @public_ip_type.setter
    def public_ip_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bee647a87ee7efd7d1a025f707661143bdbe0f80393d0070c5d7825839d345d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicIpType", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__4a962f810946f68197918a0e52b6927530d574e30fb0124699d829f625a13b6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicNetworkAccessEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="purgeEnabled")
    def purge_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "purgeEnabled"))

    @purge_enabled.setter
    def purge_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__287933fc36b13db723d92a8204ea01c53c2c31a7c48101d8edb3179bd265fefe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "purgeEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac0863ab61674f1029644536751a5eb3e49b1bad3236954890773062864489f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="streamingIngestionEnabled")
    def streaming_ingestion_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "streamingIngestionEnabled"))

    @streaming_ingestion_enabled.setter
    def streaming_ingestion_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ed0971b6b24fbc0999b49eaab0f846d1816e8675642a3712566b88a54d21e08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streamingIngestionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00e69afe4e42b542a0cdc00ab2c232b82abb0f77f969318f4840e37158132ce1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trustedExternalTenants")
    def trusted_external_tenants(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "trustedExternalTenants"))

    @trusted_external_tenants.setter
    def trusted_external_tenants(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9316dea60f9fd4ead70ba6cef156c815c780190353940f170493626c04af2ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trustedExternalTenants", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zones")
    def zones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "zones"))

    @zones.setter
    def zones(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fafbc7c4677a76d9863ebd2e9ea3a52def5ae13a438edbf3c55905a6ea70beb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zones", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kustoCluster.KustoClusterConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "sku": "sku",
        "allowed_fqdns": "allowedFqdns",
        "allowed_ip_ranges": "allowedIpRanges",
        "auto_stop_enabled": "autoStopEnabled",
        "disk_encryption_enabled": "diskEncryptionEnabled",
        "double_encryption_enabled": "doubleEncryptionEnabled",
        "id": "id",
        "identity": "identity",
        "language_extensions": "languageExtensions",
        "optimized_auto_scale": "optimizedAutoScale",
        "outbound_network_access_restricted": "outboundNetworkAccessRestricted",
        "public_ip_type": "publicIpType",
        "public_network_access_enabled": "publicNetworkAccessEnabled",
        "purge_enabled": "purgeEnabled",
        "streaming_ingestion_enabled": "streamingIngestionEnabled",
        "tags": "tags",
        "timeouts": "timeouts",
        "trusted_external_tenants": "trustedExternalTenants",
        "virtual_network_configuration": "virtualNetworkConfiguration",
        "zones": "zones",
    },
)
class KustoClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        sku: typing.Union["KustoClusterSku", typing.Dict[builtins.str, typing.Any]],
        allowed_fqdns: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        auto_stop_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disk_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        double_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["KustoClusterIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        language_extensions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KustoClusterLanguageExtensions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        optimized_auto_scale: typing.Optional[typing.Union["KustoClusterOptimizedAutoScale", typing.Dict[builtins.str, typing.Any]]] = None,
        outbound_network_access_restricted: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        public_ip_type: typing.Optional[builtins.str] = None,
        public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        purge_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        streaming_ingestion_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["KustoClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        trusted_external_tenants: typing.Optional[typing.Sequence[builtins.str]] = None,
        virtual_network_configuration: typing.Optional[typing.Union["KustoClusterVirtualNetworkConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#location KustoCluster#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#name KustoCluster#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#resource_group_name KustoCluster#resource_group_name}.
        :param sku: sku block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#sku KustoCluster#sku}
        :param allowed_fqdns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#allowed_fqdns KustoCluster#allowed_fqdns}.
        :param allowed_ip_ranges: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#allowed_ip_ranges KustoCluster#allowed_ip_ranges}.
        :param auto_stop_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#auto_stop_enabled KustoCluster#auto_stop_enabled}.
        :param disk_encryption_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#disk_encryption_enabled KustoCluster#disk_encryption_enabled}.
        :param double_encryption_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#double_encryption_enabled KustoCluster#double_encryption_enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#id KustoCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#identity KustoCluster#identity}
        :param language_extensions: language_extensions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#language_extensions KustoCluster#language_extensions}
        :param optimized_auto_scale: optimized_auto_scale block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#optimized_auto_scale KustoCluster#optimized_auto_scale}
        :param outbound_network_access_restricted: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#outbound_network_access_restricted KustoCluster#outbound_network_access_restricted}.
        :param public_ip_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#public_ip_type KustoCluster#public_ip_type}.
        :param public_network_access_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#public_network_access_enabled KustoCluster#public_network_access_enabled}.
        :param purge_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#purge_enabled KustoCluster#purge_enabled}.
        :param streaming_ingestion_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#streaming_ingestion_enabled KustoCluster#streaming_ingestion_enabled}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#tags KustoCluster#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#timeouts KustoCluster#timeouts}
        :param trusted_external_tenants: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#trusted_external_tenants KustoCluster#trusted_external_tenants}.
        :param virtual_network_configuration: virtual_network_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#virtual_network_configuration KustoCluster#virtual_network_configuration}
        :param zones: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#zones KustoCluster#zones}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(sku, dict):
            sku = KustoClusterSku(**sku)
        if isinstance(identity, dict):
            identity = KustoClusterIdentity(**identity)
        if isinstance(optimized_auto_scale, dict):
            optimized_auto_scale = KustoClusterOptimizedAutoScale(**optimized_auto_scale)
        if isinstance(timeouts, dict):
            timeouts = KustoClusterTimeouts(**timeouts)
        if isinstance(virtual_network_configuration, dict):
            virtual_network_configuration = KustoClusterVirtualNetworkConfiguration(**virtual_network_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14d19caef219ffd5772c893762737d4ba11a9480d8b1e00c5260e4f9dc93f690)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument sku", value=sku, expected_type=type_hints["sku"])
            check_type(argname="argument allowed_fqdns", value=allowed_fqdns, expected_type=type_hints["allowed_fqdns"])
            check_type(argname="argument allowed_ip_ranges", value=allowed_ip_ranges, expected_type=type_hints["allowed_ip_ranges"])
            check_type(argname="argument auto_stop_enabled", value=auto_stop_enabled, expected_type=type_hints["auto_stop_enabled"])
            check_type(argname="argument disk_encryption_enabled", value=disk_encryption_enabled, expected_type=type_hints["disk_encryption_enabled"])
            check_type(argname="argument double_encryption_enabled", value=double_encryption_enabled, expected_type=type_hints["double_encryption_enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument language_extensions", value=language_extensions, expected_type=type_hints["language_extensions"])
            check_type(argname="argument optimized_auto_scale", value=optimized_auto_scale, expected_type=type_hints["optimized_auto_scale"])
            check_type(argname="argument outbound_network_access_restricted", value=outbound_network_access_restricted, expected_type=type_hints["outbound_network_access_restricted"])
            check_type(argname="argument public_ip_type", value=public_ip_type, expected_type=type_hints["public_ip_type"])
            check_type(argname="argument public_network_access_enabled", value=public_network_access_enabled, expected_type=type_hints["public_network_access_enabled"])
            check_type(argname="argument purge_enabled", value=purge_enabled, expected_type=type_hints["purge_enabled"])
            check_type(argname="argument streaming_ingestion_enabled", value=streaming_ingestion_enabled, expected_type=type_hints["streaming_ingestion_enabled"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument trusted_external_tenants", value=trusted_external_tenants, expected_type=type_hints["trusted_external_tenants"])
            check_type(argname="argument virtual_network_configuration", value=virtual_network_configuration, expected_type=type_hints["virtual_network_configuration"])
            check_type(argname="argument zones", value=zones, expected_type=type_hints["zones"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "name": name,
            "resource_group_name": resource_group_name,
            "sku": sku,
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
        if allowed_fqdns is not None:
            self._values["allowed_fqdns"] = allowed_fqdns
        if allowed_ip_ranges is not None:
            self._values["allowed_ip_ranges"] = allowed_ip_ranges
        if auto_stop_enabled is not None:
            self._values["auto_stop_enabled"] = auto_stop_enabled
        if disk_encryption_enabled is not None:
            self._values["disk_encryption_enabled"] = disk_encryption_enabled
        if double_encryption_enabled is not None:
            self._values["double_encryption_enabled"] = double_encryption_enabled
        if id is not None:
            self._values["id"] = id
        if identity is not None:
            self._values["identity"] = identity
        if language_extensions is not None:
            self._values["language_extensions"] = language_extensions
        if optimized_auto_scale is not None:
            self._values["optimized_auto_scale"] = optimized_auto_scale
        if outbound_network_access_restricted is not None:
            self._values["outbound_network_access_restricted"] = outbound_network_access_restricted
        if public_ip_type is not None:
            self._values["public_ip_type"] = public_ip_type
        if public_network_access_enabled is not None:
            self._values["public_network_access_enabled"] = public_network_access_enabled
        if purge_enabled is not None:
            self._values["purge_enabled"] = purge_enabled
        if streaming_ingestion_enabled is not None:
            self._values["streaming_ingestion_enabled"] = streaming_ingestion_enabled
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if trusted_external_tenants is not None:
            self._values["trusted_external_tenants"] = trusted_external_tenants
        if virtual_network_configuration is not None:
            self._values["virtual_network_configuration"] = virtual_network_configuration
        if zones is not None:
            self._values["zones"] = zones

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
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#location KustoCluster#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#name KustoCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#resource_group_name KustoCluster#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sku(self) -> "KustoClusterSku":
        '''sku block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#sku KustoCluster#sku}
        '''
        result = self._values.get("sku")
        assert result is not None, "Required property 'sku' is missing"
        return typing.cast("KustoClusterSku", result)

    @builtins.property
    def allowed_fqdns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#allowed_fqdns KustoCluster#allowed_fqdns}.'''
        result = self._values.get("allowed_fqdns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allowed_ip_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#allowed_ip_ranges KustoCluster#allowed_ip_ranges}.'''
        result = self._values.get("allowed_ip_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def auto_stop_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#auto_stop_enabled KustoCluster#auto_stop_enabled}.'''
        result = self._values.get("auto_stop_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disk_encryption_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#disk_encryption_enabled KustoCluster#disk_encryption_enabled}.'''
        result = self._values.get("disk_encryption_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def double_encryption_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#double_encryption_enabled KustoCluster#double_encryption_enabled}.'''
        result = self._values.get("double_encryption_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#id KustoCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity(self) -> typing.Optional["KustoClusterIdentity"]:
        '''identity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#identity KustoCluster#identity}
        '''
        result = self._values.get("identity")
        return typing.cast(typing.Optional["KustoClusterIdentity"], result)

    @builtins.property
    def language_extensions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KustoClusterLanguageExtensions"]]]:
        '''language_extensions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#language_extensions KustoCluster#language_extensions}
        '''
        result = self._values.get("language_extensions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KustoClusterLanguageExtensions"]]], result)

    @builtins.property
    def optimized_auto_scale(self) -> typing.Optional["KustoClusterOptimizedAutoScale"]:
        '''optimized_auto_scale block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#optimized_auto_scale KustoCluster#optimized_auto_scale}
        '''
        result = self._values.get("optimized_auto_scale")
        return typing.cast(typing.Optional["KustoClusterOptimizedAutoScale"], result)

    @builtins.property
    def outbound_network_access_restricted(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#outbound_network_access_restricted KustoCluster#outbound_network_access_restricted}.'''
        result = self._values.get("outbound_network_access_restricted")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def public_ip_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#public_ip_type KustoCluster#public_ip_type}.'''
        result = self._values.get("public_ip_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_network_access_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#public_network_access_enabled KustoCluster#public_network_access_enabled}.'''
        result = self._values.get("public_network_access_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def purge_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#purge_enabled KustoCluster#purge_enabled}.'''
        result = self._values.get("purge_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def streaming_ingestion_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#streaming_ingestion_enabled KustoCluster#streaming_ingestion_enabled}.'''
        result = self._values.get("streaming_ingestion_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#tags KustoCluster#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["KustoClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#timeouts KustoCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["KustoClusterTimeouts"], result)

    @builtins.property
    def trusted_external_tenants(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#trusted_external_tenants KustoCluster#trusted_external_tenants}.'''
        result = self._values.get("trusted_external_tenants")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def virtual_network_configuration(
        self,
    ) -> typing.Optional["KustoClusterVirtualNetworkConfiguration"]:
        '''virtual_network_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#virtual_network_configuration KustoCluster#virtual_network_configuration}
        '''
        result = self._values.get("virtual_network_configuration")
        return typing.cast(typing.Optional["KustoClusterVirtualNetworkConfiguration"], result)

    @builtins.property
    def zones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#zones KustoCluster#zones}.'''
        result = self._values.get("zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KustoClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kustoCluster.KustoClusterIdentity",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "identity_ids": "identityIds"},
)
class KustoClusterIdentity:
    def __init__(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#type KustoCluster#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#identity_ids KustoCluster#identity_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__931bf5230f8be06e754b52504f484085902a6d9d92366018b040d4b313cda5ba)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument identity_ids", value=identity_ids, expected_type=type_hints["identity_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if identity_ids is not None:
            self._values["identity_ids"] = identity_ids

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#type KustoCluster#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identity_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#identity_ids KustoCluster#identity_ids}.'''
        result = self._values.get("identity_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KustoClusterIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KustoClusterIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kustoCluster.KustoClusterIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b735b8373796b17227358feb64d8220db2be8f612351bde4d4aadd6e509eb1ba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b41fa38cfde6c0f608ce62d8e383443767147848e05044fc124401adeafd6aa8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc92ae542ef3025ff95caaa120c85218592bfcf58f05b9b44cd253676517b5b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KustoClusterIdentity]:
        return typing.cast(typing.Optional[KustoClusterIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[KustoClusterIdentity]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfbed8b31b6f0e3e5f2b64c5e0526bf8a44f97997e4e7f31e53af9df677a7ce9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kustoCluster.KustoClusterLanguageExtensions",
    jsii_struct_bases=[],
    name_mapping={"image": "image", "name": "name"},
)
class KustoClusterLanguageExtensions:
    def __init__(self, *, image: builtins.str, name: builtins.str) -> None:
        '''
        :param image: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#image KustoCluster#image}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#name KustoCluster#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1ecaddd6bde7681b0dfe42ab45a7129084bc867429d4a3b88d4911dcba3c1a5)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image": image,
            "name": name,
        }

    @builtins.property
    def image(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#image KustoCluster#image}.'''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#name KustoCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KustoClusterLanguageExtensions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KustoClusterLanguageExtensionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kustoCluster.KustoClusterLanguageExtensionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__71370b8969762e9edde661366c017ccb51907700e566f9066dc737a06293c967)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KustoClusterLanguageExtensionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b30c0e5fdf3308fc82047457c92c5ffaa43793102d8d1f3ecdcd0ccb490121d4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KustoClusterLanguageExtensionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c77e25476febbb8ce7a42fde57e58dacfcd473c2d75c6d5ab7c55de1b2fa646d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f6e949b512acfadb10efc7f2442f54a656116e3abe114f51da21138c91bad7e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7670d36d1aa76206cd218dc21463170a5a74740e73e065b80c5d2d4e78e1d48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KustoClusterLanguageExtensions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KustoClusterLanguageExtensions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KustoClusterLanguageExtensions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d611f25f98c4f1c61bb2cb132c09e434338a882118332ec7303fa31cf7f4018d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KustoClusterLanguageExtensionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kustoCluster.KustoClusterLanguageExtensionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4035d8b1b3b878b359b6bbfc5de8a41a3986b78e92b7d99583afc1b5e363ec9f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "image"))

    @image.setter
    def image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ef839a36b61fe1c21c1e57a6b69ed3a86856efb58c5e20cf9a845ad52f5d414)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "image", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f647a7cdcd105dfe3895dae59f502e75ab6e79da51a0a64e76e93f24102293f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KustoClusterLanguageExtensions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KustoClusterLanguageExtensions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KustoClusterLanguageExtensions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b82919ed4c93c84e0c206381b5f94b26413787100f551c53712843dacbc6c084)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kustoCluster.KustoClusterOptimizedAutoScale",
    jsii_struct_bases=[],
    name_mapping={
        "maximum_instances": "maximumInstances",
        "minimum_instances": "minimumInstances",
    },
)
class KustoClusterOptimizedAutoScale:
    def __init__(
        self,
        *,
        maximum_instances: jsii.Number,
        minimum_instances: jsii.Number,
    ) -> None:
        '''
        :param maximum_instances: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#maximum_instances KustoCluster#maximum_instances}.
        :param minimum_instances: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#minimum_instances KustoCluster#minimum_instances}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f130d857d8085fe9b505ae9745647f72a13e326e744bc8952cfc9c204b97a63e)
            check_type(argname="argument maximum_instances", value=maximum_instances, expected_type=type_hints["maximum_instances"])
            check_type(argname="argument minimum_instances", value=minimum_instances, expected_type=type_hints["minimum_instances"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "maximum_instances": maximum_instances,
            "minimum_instances": minimum_instances,
        }

    @builtins.property
    def maximum_instances(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#maximum_instances KustoCluster#maximum_instances}.'''
        result = self._values.get("maximum_instances")
        assert result is not None, "Required property 'maximum_instances' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def minimum_instances(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#minimum_instances KustoCluster#minimum_instances}.'''
        result = self._values.get("minimum_instances")
        assert result is not None, "Required property 'minimum_instances' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KustoClusterOptimizedAutoScale(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KustoClusterOptimizedAutoScaleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kustoCluster.KustoClusterOptimizedAutoScaleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f487e2e6d735ce136777cb8e4405cb1e5d7b0bf23eb5c6adc5dbd837051fada)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="maximumInstancesInput")
    def maximum_instances_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumInstancesInput"))

    @builtins.property
    @jsii.member(jsii_name="minimumInstancesInput")
    def minimum_instances_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minimumInstancesInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumInstances")
    def maximum_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumInstances"))

    @maximum_instances.setter
    def maximum_instances(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2c1f2a095123d2d3802a4fd3e15cbfc13ee46bed9068f8b68c898c2724e7e6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumInstances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minimumInstances")
    def minimum_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minimumInstances"))

    @minimum_instances.setter
    def minimum_instances(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__120b271b88183e6c65b1acefe4587545b416589b60d0ec026e29ecb1c0198f63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumInstances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KustoClusterOptimizedAutoScale]:
        return typing.cast(typing.Optional[KustoClusterOptimizedAutoScale], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KustoClusterOptimizedAutoScale],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4c27ae5ef23ec1f57197aa8117e7926e3b8eeffd3598232ce7c143ffd5799f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kustoCluster.KustoClusterSku",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "capacity": "capacity"},
)
class KustoClusterSku:
    def __init__(
        self,
        *,
        name: builtins.str,
        capacity: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#name KustoCluster#name}.
        :param capacity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#capacity KustoCluster#capacity}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8260b2133adda64885e8cfc2df850a2deb22b31bc1fe355ab9b1b013296c0526)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument capacity", value=capacity, expected_type=type_hints["capacity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if capacity is not None:
            self._values["capacity"] = capacity

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#name KustoCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def capacity(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#capacity KustoCluster#capacity}.'''
        result = self._values.get("capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KustoClusterSku(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KustoClusterSkuOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kustoCluster.KustoClusterSkuOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d579d48640cd6b2d7d93f10a8993e35c1e4ad7763d3217229568a0b3f78b6f9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCapacity")
    def reset_capacity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCapacity", []))

    @builtins.property
    @jsii.member(jsii_name="capacityInput")
    def capacity_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "capacityInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="capacity")
    def capacity(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "capacity"))

    @capacity.setter
    def capacity(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d69b656e760f64a9336c715c9cfb2b138abd1e7bffb4a9c643ccdd01fd4b377)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capacity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__865d3da76bd0ab68697c4797084ba6b7e605d1014ac4e5472cec97cc54d42ac3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KustoClusterSku]:
        return typing.cast(typing.Optional[KustoClusterSku], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[KustoClusterSku]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d87454cdfb477b6c44279c7f998b9276bac061e15fdbe50b477dec0b56e3e19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kustoCluster.KustoClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class KustoClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#create KustoCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#delete KustoCluster#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#read KustoCluster#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#update KustoCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bfc20b6dbb89fd3fd3bc5bf2649afe1f6dd1dd68c4caf9b094f05c6f4ee5137)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#create KustoCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#delete KustoCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#read KustoCluster#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#update KustoCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KustoClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KustoClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kustoCluster.KustoClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4cf650731d89ba06effe8de7efc1a2811d4686aed3aa13b6f5e52041c4ac0673)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aeeba03f47a2b4571cc09f55269e3a4e76985114d63191ada38972b98c14a1f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41a9d5daeae5e3705ad39e426fde912afcc28621a6a4c0c2274a87af8e2b1f20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e484fbe592bb4a41b677b1ee1f0669fcf8f3531c5e8ad615ad37a24de23ddbc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__317260a721911ac17811f9e7a4ef53dff0a7d92d3a394d60f4278e4f00ef688f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KustoClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KustoClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KustoClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a0f97c1223c13db528f65379b94b0f3a72e1337a65224556d6b39a589409d4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kustoCluster.KustoClusterVirtualNetworkConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "data_management_public_ip_id": "dataManagementPublicIpId",
        "engine_public_ip_id": "enginePublicIpId",
        "subnet_id": "subnetId",
    },
)
class KustoClusterVirtualNetworkConfiguration:
    def __init__(
        self,
        *,
        data_management_public_ip_id: builtins.str,
        engine_public_ip_id: builtins.str,
        subnet_id: builtins.str,
    ) -> None:
        '''
        :param data_management_public_ip_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#data_management_public_ip_id KustoCluster#data_management_public_ip_id}.
        :param engine_public_ip_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#engine_public_ip_id KustoCluster#engine_public_ip_id}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#subnet_id KustoCluster#subnet_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d44d72ab6398be0111e98c2d632eeee233add9e8dad3375e58b5bdb169a336d)
            check_type(argname="argument data_management_public_ip_id", value=data_management_public_ip_id, expected_type=type_hints["data_management_public_ip_id"])
            check_type(argname="argument engine_public_ip_id", value=engine_public_ip_id, expected_type=type_hints["engine_public_ip_id"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_management_public_ip_id": data_management_public_ip_id,
            "engine_public_ip_id": engine_public_ip_id,
            "subnet_id": subnet_id,
        }

    @builtins.property
    def data_management_public_ip_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#data_management_public_ip_id KustoCluster#data_management_public_ip_id}.'''
        result = self._values.get("data_management_public_ip_id")
        assert result is not None, "Required property 'data_management_public_ip_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def engine_public_ip_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#engine_public_ip_id KustoCluster#engine_public_ip_id}.'''
        result = self._values.get("engine_public_ip_id")
        assert result is not None, "Required property 'engine_public_ip_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_cluster#subnet_id KustoCluster#subnet_id}.'''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KustoClusterVirtualNetworkConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KustoClusterVirtualNetworkConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kustoCluster.KustoClusterVirtualNetworkConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f2a8af098282e840dc94349d1c3e943ce1a4c3525345264b0ec7a4d249f7f5f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="dataManagementPublicIpIdInput")
    def data_management_public_ip_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataManagementPublicIpIdInput"))

    @builtins.property
    @jsii.member(jsii_name="enginePublicIpIdInput")
    def engine_public_ip_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enginePublicIpIdInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="dataManagementPublicIpId")
    def data_management_public_ip_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataManagementPublicIpId"))

    @data_management_public_ip_id.setter
    def data_management_public_ip_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__842a92ddce624aa1dc544cc59c5a394b727196ed143db89d3f44065eac6f7b0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataManagementPublicIpId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enginePublicIpId")
    def engine_public_ip_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enginePublicIpId"))

    @engine_public_ip_id.setter
    def engine_public_ip_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45ea72d9b5d517c5a088fc41a8109bdaf676649d723eb68bb929bfe2627d6652)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enginePublicIpId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92b5517b2eacdbc5fee2c8df92c1821c4e831c58d4e0c27225b891579152b24d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KustoClusterVirtualNetworkConfiguration]:
        return typing.cast(typing.Optional[KustoClusterVirtualNetworkConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KustoClusterVirtualNetworkConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adc6ccee443e81e506d176750c4567994c3319493eb1f09477ab3a9cfe56ad08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "KustoCluster",
    "KustoClusterConfig",
    "KustoClusterIdentity",
    "KustoClusterIdentityOutputReference",
    "KustoClusterLanguageExtensions",
    "KustoClusterLanguageExtensionsList",
    "KustoClusterLanguageExtensionsOutputReference",
    "KustoClusterOptimizedAutoScale",
    "KustoClusterOptimizedAutoScaleOutputReference",
    "KustoClusterSku",
    "KustoClusterSkuOutputReference",
    "KustoClusterTimeouts",
    "KustoClusterTimeoutsOutputReference",
    "KustoClusterVirtualNetworkConfiguration",
    "KustoClusterVirtualNetworkConfigurationOutputReference",
]

publication.publish()

def _typecheckingstub__a9a7fff23a05da91f8143a0a180ddea278a85538968a4da60b38874740bc6a4d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    sku: typing.Union[KustoClusterSku, typing.Dict[builtins.str, typing.Any]],
    allowed_fqdns: typing.Optional[typing.Sequence[builtins.str]] = None,
    allowed_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    auto_stop_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disk_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    double_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[KustoClusterIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    language_extensions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KustoClusterLanguageExtensions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    optimized_auto_scale: typing.Optional[typing.Union[KustoClusterOptimizedAutoScale, typing.Dict[builtins.str, typing.Any]]] = None,
    outbound_network_access_restricted: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    public_ip_type: typing.Optional[builtins.str] = None,
    public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    purge_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    streaming_ingestion_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[KustoClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    trusted_external_tenants: typing.Optional[typing.Sequence[builtins.str]] = None,
    virtual_network_configuration: typing.Optional[typing.Union[KustoClusterVirtualNetworkConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    zones: typing.Optional[typing.Sequence[builtins.str]] = None,
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

def _typecheckingstub__60680647ecb4645b41d195b68fb6b4b608fb3fa6e238a9f219d0c747b238af34(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05f60f52b65ca385d49617de5536ab6567190f6abc605ca8b3414b5f93735746(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KustoClusterLanguageExtensions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50ea96f924d1d44d34c7bd3187119c1645e754f9856234d092a966e6f34c9209(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf54a55fe90e960da698908a48a00687e9220c0847b5cd8a0b90222df514900f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c60d81a8d0c10456679b5a4d3c98185c82ac580eb850598d301ef649348ae2c7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0173dde998bf4e3d1f1386d6581830cd591e3da45156871c1a708aa6a948d342(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__670e034c5ad20a0397b2441061c07aa893b27f3d6e75b86ca71868b0e3fff168(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64d253591ffb1a4cbdcf50cb7c3fb0033c45135a98a19553231223b08d439ac1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53d4d6268583770d64ab1fbf1d30d4c2f81d1cca1c83befedfdaea47d93a2ed4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3668f3b4f78833296bbe739635df074a681d39922c8abc28e11adbe30a32db8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d46189776cbd3ef7a80f04a8d20a2ee4824b1ad7ea4eb2c44d2d9ef3b3d73bfc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bee647a87ee7efd7d1a025f707661143bdbe0f80393d0070c5d7825839d345d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a962f810946f68197918a0e52b6927530d574e30fb0124699d829f625a13b6c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__287933fc36b13db723d92a8204ea01c53c2c31a7c48101d8edb3179bd265fefe(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac0863ab61674f1029644536751a5eb3e49b1bad3236954890773062864489f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ed0971b6b24fbc0999b49eaab0f846d1816e8675642a3712566b88a54d21e08(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00e69afe4e42b542a0cdc00ab2c232b82abb0f77f969318f4840e37158132ce1(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9316dea60f9fd4ead70ba6cef156c815c780190353940f170493626c04af2ff(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fafbc7c4677a76d9863ebd2e9ea3a52def5ae13a438edbf3c55905a6ea70beb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14d19caef219ffd5772c893762737d4ba11a9480d8b1e00c5260e4f9dc93f690(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    sku: typing.Union[KustoClusterSku, typing.Dict[builtins.str, typing.Any]],
    allowed_fqdns: typing.Optional[typing.Sequence[builtins.str]] = None,
    allowed_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    auto_stop_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disk_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    double_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[KustoClusterIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    language_extensions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KustoClusterLanguageExtensions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    optimized_auto_scale: typing.Optional[typing.Union[KustoClusterOptimizedAutoScale, typing.Dict[builtins.str, typing.Any]]] = None,
    outbound_network_access_restricted: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    public_ip_type: typing.Optional[builtins.str] = None,
    public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    purge_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    streaming_ingestion_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[KustoClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    trusted_external_tenants: typing.Optional[typing.Sequence[builtins.str]] = None,
    virtual_network_configuration: typing.Optional[typing.Union[KustoClusterVirtualNetworkConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    zones: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__931bf5230f8be06e754b52504f484085902a6d9d92366018b040d4b313cda5ba(
    *,
    type: builtins.str,
    identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b735b8373796b17227358feb64d8220db2be8f612351bde4d4aadd6e509eb1ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b41fa38cfde6c0f608ce62d8e383443767147848e05044fc124401adeafd6aa8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc92ae542ef3025ff95caaa120c85218592bfcf58f05b9b44cd253676517b5b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfbed8b31b6f0e3e5f2b64c5e0526bf8a44f97997e4e7f31e53af9df677a7ce9(
    value: typing.Optional[KustoClusterIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1ecaddd6bde7681b0dfe42ab45a7129084bc867429d4a3b88d4911dcba3c1a5(
    *,
    image: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71370b8969762e9edde661366c017ccb51907700e566f9066dc737a06293c967(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b30c0e5fdf3308fc82047457c92c5ffaa43793102d8d1f3ecdcd0ccb490121d4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c77e25476febbb8ce7a42fde57e58dacfcd473c2d75c6d5ab7c55de1b2fa646d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f6e949b512acfadb10efc7f2442f54a656116e3abe114f51da21138c91bad7e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7670d36d1aa76206cd218dc21463170a5a74740e73e065b80c5d2d4e78e1d48(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d611f25f98c4f1c61bb2cb132c09e434338a882118332ec7303fa31cf7f4018d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KustoClusterLanguageExtensions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4035d8b1b3b878b359b6bbfc5de8a41a3986b78e92b7d99583afc1b5e363ec9f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ef839a36b61fe1c21c1e57a6b69ed3a86856efb58c5e20cf9a845ad52f5d414(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f647a7cdcd105dfe3895dae59f502e75ab6e79da51a0a64e76e93f24102293f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b82919ed4c93c84e0c206381b5f94b26413787100f551c53712843dacbc6c084(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KustoClusterLanguageExtensions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f130d857d8085fe9b505ae9745647f72a13e326e744bc8952cfc9c204b97a63e(
    *,
    maximum_instances: jsii.Number,
    minimum_instances: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f487e2e6d735ce136777cb8e4405cb1e5d7b0bf23eb5c6adc5dbd837051fada(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2c1f2a095123d2d3802a4fd3e15cbfc13ee46bed9068f8b68c898c2724e7e6f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__120b271b88183e6c65b1acefe4587545b416589b60d0ec026e29ecb1c0198f63(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4c27ae5ef23ec1f57197aa8117e7926e3b8eeffd3598232ce7c143ffd5799f9(
    value: typing.Optional[KustoClusterOptimizedAutoScale],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8260b2133adda64885e8cfc2df850a2deb22b31bc1fe355ab9b1b013296c0526(
    *,
    name: builtins.str,
    capacity: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d579d48640cd6b2d7d93f10a8993e35c1e4ad7763d3217229568a0b3f78b6f9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d69b656e760f64a9336c715c9cfb2b138abd1e7bffb4a9c643ccdd01fd4b377(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__865d3da76bd0ab68697c4797084ba6b7e605d1014ac4e5472cec97cc54d42ac3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d87454cdfb477b6c44279c7f998b9276bac061e15fdbe50b477dec0b56e3e19(
    value: typing.Optional[KustoClusterSku],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bfc20b6dbb89fd3fd3bc5bf2649afe1f6dd1dd68c4caf9b094f05c6f4ee5137(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cf650731d89ba06effe8de7efc1a2811d4686aed3aa13b6f5e52041c4ac0673(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeeba03f47a2b4571cc09f55269e3a4e76985114d63191ada38972b98c14a1f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41a9d5daeae5e3705ad39e426fde912afcc28621a6a4c0c2274a87af8e2b1f20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e484fbe592bb4a41b677b1ee1f0669fcf8f3531c5e8ad615ad37a24de23ddbc9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__317260a721911ac17811f9e7a4ef53dff0a7d92d3a394d60f4278e4f00ef688f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a0f97c1223c13db528f65379b94b0f3a72e1337a65224556d6b39a589409d4c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KustoClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d44d72ab6398be0111e98c2d632eeee233add9e8dad3375e58b5bdb169a336d(
    *,
    data_management_public_ip_id: builtins.str,
    engine_public_ip_id: builtins.str,
    subnet_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f2a8af098282e840dc94349d1c3e943ce1a4c3525345264b0ec7a4d249f7f5f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__842a92ddce624aa1dc544cc59c5a394b727196ed143db89d3f44065eac6f7b0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45ea72d9b5d517c5a088fc41a8109bdaf676649d723eb68bb929bfe2627d6652(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92b5517b2eacdbc5fee2c8df92c1821c4e831c58d4e0c27225b891579152b24d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adc6ccee443e81e506d176750c4567994c3319493eb1f09477ab3a9cfe56ad08(
    value: typing.Optional[KustoClusterVirtualNetworkConfiguration],
) -> None:
    """Type checking stubs"""
    pass
