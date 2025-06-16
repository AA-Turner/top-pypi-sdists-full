r'''
# `google_data_fusion_instance`

Refer to the Terraform Registry for docs: [`google_data_fusion_instance`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance).
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


class GoogleDataFusionInstance(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataFusionInstance.GoogleDataFusionInstance",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance google_data_fusion_instance}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        type: builtins.str,
        accelerators: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataFusionInstanceAccelerators", typing.Dict[builtins.str, typing.Any]]]]] = None,
        crypto_key_config: typing.Optional[typing.Union["GoogleDataFusionInstanceCryptoKeyConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        dataproc_service_account: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        enable_rbac: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_stackdriver_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_stackdriver_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        event_publish_config: typing.Optional[typing.Union["GoogleDataFusionInstanceEventPublishConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        network_config: typing.Optional[typing.Union["GoogleDataFusionInstanceNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        private_instance: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["GoogleDataFusionInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
        zone: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance google_data_fusion_instance} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The ID of the instance or a fully qualified identifier for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#name GoogleDataFusionInstance#name}
        :param type: Represents the type of Data Fusion instance. Each type is configured with the default settings for processing and memory. - BASIC: Basic Data Fusion instance. In Basic type, the user will be able to create data pipelines using point and click UI. However, there are certain limitations, such as fewer number of concurrent pipelines, no support for streaming pipelines, etc. - ENTERPRISE: Enterprise Data Fusion instance. In Enterprise type, the user will have more features available, such as support for streaming pipelines, higher number of concurrent pipelines, etc. - DEVELOPER: Developer Data Fusion instance. In Developer type, the user will have all features available but with restrictive capabilities. This is to help enterprises design and develop their data ingestion and integration pipelines at low cost. Possible values: ["BASIC", "ENTERPRISE", "DEVELOPER"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#type GoogleDataFusionInstance#type}
        :param accelerators: accelerators block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#accelerators GoogleDataFusionInstance#accelerators}
        :param crypto_key_config: crypto_key_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#crypto_key_config GoogleDataFusionInstance#crypto_key_config}
        :param dataproc_service_account: User-managed service account to set on Dataproc when Cloud Data Fusion creates Dataproc to run data processing pipelines. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#dataproc_service_account GoogleDataFusionInstance#dataproc_service_account}
        :param description: An optional description of the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#description GoogleDataFusionInstance#description}
        :param display_name: Display name for an instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#display_name GoogleDataFusionInstance#display_name}
        :param enable_rbac: Option to enable granular role-based access control. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#enable_rbac GoogleDataFusionInstance#enable_rbac}
        :param enable_stackdriver_logging: Option to enable Stackdriver Logging. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#enable_stackdriver_logging GoogleDataFusionInstance#enable_stackdriver_logging}
        :param enable_stackdriver_monitoring: Option to enable Stackdriver Monitoring. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#enable_stackdriver_monitoring GoogleDataFusionInstance#enable_stackdriver_monitoring}
        :param event_publish_config: event_publish_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#event_publish_config GoogleDataFusionInstance#event_publish_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#id GoogleDataFusionInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The resource labels for instance to use to annotate any related underlying resources, such as Compute Engine VMs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#labels GoogleDataFusionInstance#labels}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#network_config GoogleDataFusionInstance#network_config}
        :param options: Map of additional options used to configure the behavior of Data Fusion instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#options GoogleDataFusionInstance#options}
        :param private_instance: Specifies whether the Data Fusion instance should be private. If set to true, all Data Fusion nodes will have private IP addresses and will not be able to access the public internet. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#private_instance GoogleDataFusionInstance#private_instance}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#project GoogleDataFusionInstance#project}.
        :param region: The region of the Data Fusion instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#region GoogleDataFusionInstance#region}
        :param tags: A map of resource manager tags. Resource manager tag keys and values have the same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/{tag_value_id}. The field is ignored (both PUT & PATCH) when empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#tags GoogleDataFusionInstance#tags}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#timeouts GoogleDataFusionInstance#timeouts}
        :param version: Current version of the Data Fusion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#version GoogleDataFusionInstance#version}
        :param zone: Name of the zone in which the Data Fusion instance will be created. Only DEVELOPER instances use this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#zone GoogleDataFusionInstance#zone}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7789be7c498adef1cee8428333a671dbb197d94b9bd65a3cc84c5d8b9d9bc4a7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleDataFusionInstanceConfig(
            name=name,
            type=type,
            accelerators=accelerators,
            crypto_key_config=crypto_key_config,
            dataproc_service_account=dataproc_service_account,
            description=description,
            display_name=display_name,
            enable_rbac=enable_rbac,
            enable_stackdriver_logging=enable_stackdriver_logging,
            enable_stackdriver_monitoring=enable_stackdriver_monitoring,
            event_publish_config=event_publish_config,
            id=id,
            labels=labels,
            network_config=network_config,
            options=options,
            private_instance=private_instance,
            project=project,
            region=region,
            tags=tags,
            timeouts=timeouts,
            version=version,
            zone=zone,
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
        '''Generates CDKTF code for importing a GoogleDataFusionInstance resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleDataFusionInstance to import.
        :param import_from_id: The id of the existing GoogleDataFusionInstance that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleDataFusionInstance to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cb0e3d9a69129564488727f8650e010e96e3758e814bd385a7e5ebc5e320cb3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAccelerators")
    def put_accelerators(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataFusionInstanceAccelerators", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8dd1983f31e31a32e29581339547c68d12f882535136b6e7b9d20127b264a39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAccelerators", [value]))

    @jsii.member(jsii_name="putCryptoKeyConfig")
    def put_crypto_key_config(self, *, key_reference: builtins.str) -> None:
        '''
        :param key_reference: The name of the key which is used to encrypt/decrypt customer data. For key in Cloud KMS, the key should be in the format of projects/* /locations/* /keyRings/* /cryptoKeys/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#key_reference GoogleDataFusionInstance#key_reference} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = GoogleDataFusionInstanceCryptoKeyConfig(key_reference=key_reference)

        return typing.cast(None, jsii.invoke(self, "putCryptoKeyConfig", [value]))

    @jsii.member(jsii_name="putEventPublishConfig")
    def put_event_publish_config(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        topic: builtins.str,
    ) -> None:
        '''
        :param enabled: Option to enable Event Publishing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#enabled GoogleDataFusionInstance#enabled}
        :param topic: The resource name of the Pub/Sub topic. Format: projects/{projectId}/topics/{topic_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#topic GoogleDataFusionInstance#topic}
        '''
        value = GoogleDataFusionInstanceEventPublishConfig(
            enabled=enabled, topic=topic
        )

        return typing.cast(None, jsii.invoke(self, "putEventPublishConfig", [value]))

    @jsii.member(jsii_name="putNetworkConfig")
    def put_network_config(
        self,
        *,
        connection_type: typing.Optional[builtins.str] = None,
        ip_allocation: typing.Optional[builtins.str] = None,
        network: typing.Optional[builtins.str] = None,
        private_service_connect_config: typing.Optional[typing.Union["GoogleDataFusionInstanceNetworkConfigPrivateServiceConnectConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection_type: Optional. Type of connection for establishing private IP connectivity between the Data Fusion customer project VPC and the corresponding tenant project from a predefined list of available connection modes. If this field is unspecified for a private instance, VPC peering is used. Possible values: ["VPC_PEERING", "PRIVATE_SERVICE_CONNECT_INTERFACES"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#connection_type GoogleDataFusionInstance#connection_type}
        :param ip_allocation: The IP range in CIDR notation to use for the managed Data Fusion instance nodes. This range must not overlap with any other ranges used in the Data Fusion instance network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#ip_allocation GoogleDataFusionInstance#ip_allocation}
        :param network: Name of the network in the project with which the tenant project will be peered for executing pipelines. In case of shared VPC where the network resides in another host project the network should specified in the form of projects/{host-project-id}/global/networks/{network} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#network GoogleDataFusionInstance#network}
        :param private_service_connect_config: private_service_connect_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#private_service_connect_config GoogleDataFusionInstance#private_service_connect_config}
        '''
        value = GoogleDataFusionInstanceNetworkConfig(
            connection_type=connection_type,
            ip_allocation=ip_allocation,
            network=network,
            private_service_connect_config=private_service_connect_config,
        )

        return typing.cast(None, jsii.invoke(self, "putNetworkConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#create GoogleDataFusionInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#delete GoogleDataFusionInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#update GoogleDataFusionInstance#update}.
        '''
        value = GoogleDataFusionInstanceTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAccelerators")
    def reset_accelerators(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccelerators", []))

    @jsii.member(jsii_name="resetCryptoKeyConfig")
    def reset_crypto_key_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCryptoKeyConfig", []))

    @jsii.member(jsii_name="resetDataprocServiceAccount")
    def reset_dataproc_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataprocServiceAccount", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetEnableRbac")
    def reset_enable_rbac(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableRbac", []))

    @jsii.member(jsii_name="resetEnableStackdriverLogging")
    def reset_enable_stackdriver_logging(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableStackdriverLogging", []))

    @jsii.member(jsii_name="resetEnableStackdriverMonitoring")
    def reset_enable_stackdriver_monitoring(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableStackdriverMonitoring", []))

    @jsii.member(jsii_name="resetEventPublishConfig")
    def reset_event_publish_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventPublishConfig", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetNetworkConfig")
    def reset_network_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkConfig", []))

    @jsii.member(jsii_name="resetOptions")
    def reset_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOptions", []))

    @jsii.member(jsii_name="resetPrivateInstance")
    def reset_private_instance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateInstance", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @jsii.member(jsii_name="resetZone")
    def reset_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZone", []))

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
    @jsii.member(jsii_name="accelerators")
    def accelerators(self) -> "GoogleDataFusionInstanceAcceleratorsList":
        return typing.cast("GoogleDataFusionInstanceAcceleratorsList", jsii.get(self, "accelerators"))

    @builtins.property
    @jsii.member(jsii_name="apiEndpoint")
    def api_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="cryptoKeyConfig")
    def crypto_key_config(
        self,
    ) -> "GoogleDataFusionInstanceCryptoKeyConfigOutputReference":
        return typing.cast("GoogleDataFusionInstanceCryptoKeyConfigOutputReference", jsii.get(self, "cryptoKeyConfig"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="eventPublishConfig")
    def event_publish_config(
        self,
    ) -> "GoogleDataFusionInstanceEventPublishConfigOutputReference":
        return typing.cast("GoogleDataFusionInstanceEventPublishConfigOutputReference", jsii.get(self, "eventPublishConfig"))

    @builtins.property
    @jsii.member(jsii_name="gcsBucket")
    def gcs_bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gcsBucket"))

    @builtins.property
    @jsii.member(jsii_name="networkConfig")
    def network_config(self) -> "GoogleDataFusionInstanceNetworkConfigOutputReference":
        return typing.cast("GoogleDataFusionInstanceNetworkConfigOutputReference", jsii.get(self, "networkConfig"))

    @builtins.property
    @jsii.member(jsii_name="p4ServiceAccount")
    def p4_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "p4ServiceAccount"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @builtins.property
    @jsii.member(jsii_name="serviceEndpoint")
    def service_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="stateMessage")
    def state_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stateMessage"))

    @builtins.property
    @jsii.member(jsii_name="tenantProjectId")
    def tenant_project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantProjectId"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleDataFusionInstanceTimeoutsOutputReference":
        return typing.cast("GoogleDataFusionInstanceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorsInput")
    def accelerators_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataFusionInstanceAccelerators"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataFusionInstanceAccelerators"]]], jsii.get(self, "acceleratorsInput"))

    @builtins.property
    @jsii.member(jsii_name="cryptoKeyConfigInput")
    def crypto_key_config_input(
        self,
    ) -> typing.Optional["GoogleDataFusionInstanceCryptoKeyConfig"]:
        return typing.cast(typing.Optional["GoogleDataFusionInstanceCryptoKeyConfig"], jsii.get(self, "cryptoKeyConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="dataprocServiceAccountInput")
    def dataproc_service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataprocServiceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="enableRbacInput")
    def enable_rbac_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableRbacInput"))

    @builtins.property
    @jsii.member(jsii_name="enableStackdriverLoggingInput")
    def enable_stackdriver_logging_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableStackdriverLoggingInput"))

    @builtins.property
    @jsii.member(jsii_name="enableStackdriverMonitoringInput")
    def enable_stackdriver_monitoring_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableStackdriverMonitoringInput"))

    @builtins.property
    @jsii.member(jsii_name="eventPublishConfigInput")
    def event_publish_config_input(
        self,
    ) -> typing.Optional["GoogleDataFusionInstanceEventPublishConfig"]:
        return typing.cast(typing.Optional["GoogleDataFusionInstanceEventPublishConfig"], jsii.get(self, "eventPublishConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkConfigInput")
    def network_config_input(
        self,
    ) -> typing.Optional["GoogleDataFusionInstanceNetworkConfig"]:
        return typing.cast(typing.Optional["GoogleDataFusionInstanceNetworkConfig"], jsii.get(self, "networkConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="optionsInput")
    def options_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "optionsInput"))

    @builtins.property
    @jsii.member(jsii_name="privateInstanceInput")
    def private_instance_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "privateInstanceInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDataFusionInstanceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDataFusionInstanceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneInput")
    def zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneInput"))

    @builtins.property
    @jsii.member(jsii_name="dataprocServiceAccount")
    def dataproc_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataprocServiceAccount"))

    @dataproc_service_account.setter
    def dataproc_service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f5ec404efa02fbc35038d1c9a336b4cee33ceea941a67d9d8610f1ab9abdc0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataprocServiceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__744d131f1108c8696518fdb772b8b8053ffead20929030ae514f05c9e58f276f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bfa957bc0c475f861e3f72dc44a339b20b09d06759d9b5ca8de029fb064188e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableRbac")
    def enable_rbac(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableRbac"))

    @enable_rbac.setter
    def enable_rbac(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c9fa7cad5f8c036dd7ab917d3d33a183a22d30ed427731e17f0839a804f28e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableRbac", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableStackdriverLogging")
    def enable_stackdriver_logging(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableStackdriverLogging"))

    @enable_stackdriver_logging.setter
    def enable_stackdriver_logging(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d605ad85027d35195cfe80e694d5677a1a66f68aa386bea62d852ceac9088ff0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableStackdriverLogging", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableStackdriverMonitoring")
    def enable_stackdriver_monitoring(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableStackdriverMonitoring"))

    @enable_stackdriver_monitoring.setter
    def enable_stackdriver_monitoring(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d685110ee01f9725d528481ddb4b55e02a0627de75060561c8c475ad9cc21364)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableStackdriverMonitoring", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__317e60267c2b5da01d5ef6f74f5ba88b9bb659f759ed3a987312781f5bb33650)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03dca31ae2bbca2e1c499146785a2d3299d60a7be4c6ffabf7cc7cdabd4b7b91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56befd806ad4089d9ba29940282c4fee581b8f84f68294f0311c8dd7c0505d2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "options"))

    @options.setter
    def options(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5aa49545e65b70832ec9c6b6a155f204fa8726be1ffce107ac10ab504591df6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "options", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateInstance")
    def private_instance(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "privateInstance"))

    @private_instance.setter
    def private_instance(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f9dc75794f2911de2e80f53224b7da4a6f455e308b4574ed8871f59a5b8c84d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateInstance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__439de5f95798ec6433a64cdca76b6f373adf6cdede208f96e7c72e7f13c86740)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50dc9a5dd56732964797d5bc9887b50f6e27f1002958ea7acb41542e370263c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17e9c1dd15b504cd08f072b06acf13cb224e29e6f40f59c98df0b94dfc3c7ee0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52ba9e5494b3fa7ca19a583c6b25655cf8e759670ebb174d57875a98974ced08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54c4ae188c466376779b323750adbb2d76200314a08f8888b955a990dc0835ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03a1c02adf87cb000feb6672d1fc146241bb4c0620e35c4314dac679e9e7d0a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataFusionInstance.GoogleDataFusionInstanceAccelerators",
    jsii_struct_bases=[],
    name_mapping={"accelerator_type": "acceleratorType", "state": "state"},
)
class GoogleDataFusionInstanceAccelerators:
    def __init__(self, *, accelerator_type: builtins.str, state: builtins.str) -> None:
        '''
        :param accelerator_type: The type of an accelator for a CDF instance. Possible values: ["CDC", "HEALTHCARE", "CCAI_INSIGHTS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#accelerator_type GoogleDataFusionInstance#accelerator_type}
        :param state: The type of an accelator for a CDF instance. Possible values: ["ENABLED", "DISABLED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#state GoogleDataFusionInstance#state}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2edd4fbe57c4ebe92ac9ebbc8c9b44ecc7b3745335e485cb4cf402334786813)
            check_type(argname="argument accelerator_type", value=accelerator_type, expected_type=type_hints["accelerator_type"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "accelerator_type": accelerator_type,
            "state": state,
        }

    @builtins.property
    def accelerator_type(self) -> builtins.str:
        '''The type of an accelator for a CDF instance. Possible values: ["CDC", "HEALTHCARE", "CCAI_INSIGHTS"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#accelerator_type GoogleDataFusionInstance#accelerator_type}
        '''
        result = self._values.get("accelerator_type")
        assert result is not None, "Required property 'accelerator_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def state(self) -> builtins.str:
        '''The type of an accelator for a CDF instance. Possible values: ["ENABLED", "DISABLED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#state GoogleDataFusionInstance#state}
        '''
        result = self._values.get("state")
        assert result is not None, "Required property 'state' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataFusionInstanceAccelerators(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataFusionInstanceAcceleratorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataFusionInstance.GoogleDataFusionInstanceAcceleratorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__16c2eefaee34489ed2d04a313ac1df67f6c16b63843257cccb082c9a9205c2f0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataFusionInstanceAcceleratorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e0d500b5db0762d67ab5dfcd2123b35464e0f0df338d397969d3ef2c9ae8288)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataFusionInstanceAcceleratorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04651d32cd36e46c9d09161d0c998fae3cc678623e5bcea94e56d11077e76253)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fd2110c404d13bdf0136b1644e9ea1279590dee061858405ad37fe68a14f41d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__be34e757aeb4c6d8ffec3cc2338bf38361c00506ca4f763a657758c4c837fd97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataFusionInstanceAccelerators]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataFusionInstanceAccelerators]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataFusionInstanceAccelerators]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccab8c77e647663f8e7f2b40d37b3e53d4b6e67ca4bafd8be03e0912167c8a89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataFusionInstanceAcceleratorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataFusionInstance.GoogleDataFusionInstanceAcceleratorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb4a0bbe0ede14de7ae3bc99c6c9890a174232945e42d568c040f09c22987912)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="acceleratorTypeInput")
    def accelerator_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "acceleratorTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorType")
    def accelerator_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "acceleratorType"))

    @accelerator_type.setter
    def accelerator_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aafbd0fa4552cc9e7fd25c77cd292a5a568ab83ec363217eb1784711095af6fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99e9c047652205ba3fba893a017123b1f62aeaa54c3cfb7d7c1dee2bf1bdd8b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataFusionInstanceAccelerators]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataFusionInstanceAccelerators]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataFusionInstanceAccelerators]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a547b6fc9bfb52f795757f68717bc24d951524704029f867c5575f32c8b6fbcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataFusionInstance.GoogleDataFusionInstanceConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "type": "type",
        "accelerators": "accelerators",
        "crypto_key_config": "cryptoKeyConfig",
        "dataproc_service_account": "dataprocServiceAccount",
        "description": "description",
        "display_name": "displayName",
        "enable_rbac": "enableRbac",
        "enable_stackdriver_logging": "enableStackdriverLogging",
        "enable_stackdriver_monitoring": "enableStackdriverMonitoring",
        "event_publish_config": "eventPublishConfig",
        "id": "id",
        "labels": "labels",
        "network_config": "networkConfig",
        "options": "options",
        "private_instance": "privateInstance",
        "project": "project",
        "region": "region",
        "tags": "tags",
        "timeouts": "timeouts",
        "version": "version",
        "zone": "zone",
    },
)
class GoogleDataFusionInstanceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        type: builtins.str,
        accelerators: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataFusionInstanceAccelerators, typing.Dict[builtins.str, typing.Any]]]]] = None,
        crypto_key_config: typing.Optional[typing.Union["GoogleDataFusionInstanceCryptoKeyConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        dataproc_service_account: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        enable_rbac: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_stackdriver_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_stackdriver_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        event_publish_config: typing.Optional[typing.Union["GoogleDataFusionInstanceEventPublishConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        network_config: typing.Optional[typing.Union["GoogleDataFusionInstanceNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        private_instance: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["GoogleDataFusionInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The ID of the instance or a fully qualified identifier for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#name GoogleDataFusionInstance#name}
        :param type: Represents the type of Data Fusion instance. Each type is configured with the default settings for processing and memory. - BASIC: Basic Data Fusion instance. In Basic type, the user will be able to create data pipelines using point and click UI. However, there are certain limitations, such as fewer number of concurrent pipelines, no support for streaming pipelines, etc. - ENTERPRISE: Enterprise Data Fusion instance. In Enterprise type, the user will have more features available, such as support for streaming pipelines, higher number of concurrent pipelines, etc. - DEVELOPER: Developer Data Fusion instance. In Developer type, the user will have all features available but with restrictive capabilities. This is to help enterprises design and develop their data ingestion and integration pipelines at low cost. Possible values: ["BASIC", "ENTERPRISE", "DEVELOPER"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#type GoogleDataFusionInstance#type}
        :param accelerators: accelerators block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#accelerators GoogleDataFusionInstance#accelerators}
        :param crypto_key_config: crypto_key_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#crypto_key_config GoogleDataFusionInstance#crypto_key_config}
        :param dataproc_service_account: User-managed service account to set on Dataproc when Cloud Data Fusion creates Dataproc to run data processing pipelines. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#dataproc_service_account GoogleDataFusionInstance#dataproc_service_account}
        :param description: An optional description of the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#description GoogleDataFusionInstance#description}
        :param display_name: Display name for an instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#display_name GoogleDataFusionInstance#display_name}
        :param enable_rbac: Option to enable granular role-based access control. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#enable_rbac GoogleDataFusionInstance#enable_rbac}
        :param enable_stackdriver_logging: Option to enable Stackdriver Logging. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#enable_stackdriver_logging GoogleDataFusionInstance#enable_stackdriver_logging}
        :param enable_stackdriver_monitoring: Option to enable Stackdriver Monitoring. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#enable_stackdriver_monitoring GoogleDataFusionInstance#enable_stackdriver_monitoring}
        :param event_publish_config: event_publish_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#event_publish_config GoogleDataFusionInstance#event_publish_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#id GoogleDataFusionInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The resource labels for instance to use to annotate any related underlying resources, such as Compute Engine VMs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#labels GoogleDataFusionInstance#labels}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#network_config GoogleDataFusionInstance#network_config}
        :param options: Map of additional options used to configure the behavior of Data Fusion instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#options GoogleDataFusionInstance#options}
        :param private_instance: Specifies whether the Data Fusion instance should be private. If set to true, all Data Fusion nodes will have private IP addresses and will not be able to access the public internet. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#private_instance GoogleDataFusionInstance#private_instance}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#project GoogleDataFusionInstance#project}.
        :param region: The region of the Data Fusion instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#region GoogleDataFusionInstance#region}
        :param tags: A map of resource manager tags. Resource manager tag keys and values have the same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/{tag_value_id}. The field is ignored (both PUT & PATCH) when empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#tags GoogleDataFusionInstance#tags}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#timeouts GoogleDataFusionInstance#timeouts}
        :param version: Current version of the Data Fusion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#version GoogleDataFusionInstance#version}
        :param zone: Name of the zone in which the Data Fusion instance will be created. Only DEVELOPER instances use this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#zone GoogleDataFusionInstance#zone}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(crypto_key_config, dict):
            crypto_key_config = GoogleDataFusionInstanceCryptoKeyConfig(**crypto_key_config)
        if isinstance(event_publish_config, dict):
            event_publish_config = GoogleDataFusionInstanceEventPublishConfig(**event_publish_config)
        if isinstance(network_config, dict):
            network_config = GoogleDataFusionInstanceNetworkConfig(**network_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleDataFusionInstanceTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34a00b923d119c4a94228b2215b942b3757255dbd94a42839580a801c9e25d78)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument accelerators", value=accelerators, expected_type=type_hints["accelerators"])
            check_type(argname="argument crypto_key_config", value=crypto_key_config, expected_type=type_hints["crypto_key_config"])
            check_type(argname="argument dataproc_service_account", value=dataproc_service_account, expected_type=type_hints["dataproc_service_account"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument enable_rbac", value=enable_rbac, expected_type=type_hints["enable_rbac"])
            check_type(argname="argument enable_stackdriver_logging", value=enable_stackdriver_logging, expected_type=type_hints["enable_stackdriver_logging"])
            check_type(argname="argument enable_stackdriver_monitoring", value=enable_stackdriver_monitoring, expected_type=type_hints["enable_stackdriver_monitoring"])
            check_type(argname="argument event_publish_config", value=event_publish_config, expected_type=type_hints["event_publish_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument network_config", value=network_config, expected_type=type_hints["network_config"])
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
            check_type(argname="argument private_instance", value=private_instance, expected_type=type_hints["private_instance"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument zone", value=zone, expected_type=type_hints["zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "type": type,
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
        if accelerators is not None:
            self._values["accelerators"] = accelerators
        if crypto_key_config is not None:
            self._values["crypto_key_config"] = crypto_key_config
        if dataproc_service_account is not None:
            self._values["dataproc_service_account"] = dataproc_service_account
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if enable_rbac is not None:
            self._values["enable_rbac"] = enable_rbac
        if enable_stackdriver_logging is not None:
            self._values["enable_stackdriver_logging"] = enable_stackdriver_logging
        if enable_stackdriver_monitoring is not None:
            self._values["enable_stackdriver_monitoring"] = enable_stackdriver_monitoring
        if event_publish_config is not None:
            self._values["event_publish_config"] = event_publish_config
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if network_config is not None:
            self._values["network_config"] = network_config
        if options is not None:
            self._values["options"] = options
        if private_instance is not None:
            self._values["private_instance"] = private_instance
        if project is not None:
            self._values["project"] = project
        if region is not None:
            self._values["region"] = region
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if version is not None:
            self._values["version"] = version
        if zone is not None:
            self._values["zone"] = zone

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
    def name(self) -> builtins.str:
        '''The ID of the instance or a fully qualified identifier for the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#name GoogleDataFusionInstance#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Represents the type of Data Fusion instance.

        Each type is configured with
        the default settings for processing and memory.

        - BASIC: Basic Data Fusion instance. In Basic type, the user will be able to create data pipelines
          using point and click UI. However, there are certain limitations, such as fewer number
          of concurrent pipelines, no support for streaming pipelines, etc.
        - ENTERPRISE: Enterprise Data Fusion instance. In Enterprise type, the user will have more features
          available, such as support for streaming pipelines, higher number of concurrent pipelines, etc.
        - DEVELOPER: Developer Data Fusion instance. In Developer type, the user will have all features available but
          with restrictive capabilities. This is to help enterprises design and develop their data ingestion and integration
          pipelines at low cost. Possible values: ["BASIC", "ENTERPRISE", "DEVELOPER"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#type GoogleDataFusionInstance#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def accelerators(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataFusionInstanceAccelerators]]]:
        '''accelerators block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#accelerators GoogleDataFusionInstance#accelerators}
        '''
        result = self._values.get("accelerators")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataFusionInstanceAccelerators]]], result)

    @builtins.property
    def crypto_key_config(
        self,
    ) -> typing.Optional["GoogleDataFusionInstanceCryptoKeyConfig"]:
        '''crypto_key_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#crypto_key_config GoogleDataFusionInstance#crypto_key_config}
        '''
        result = self._values.get("crypto_key_config")
        return typing.cast(typing.Optional["GoogleDataFusionInstanceCryptoKeyConfig"], result)

    @builtins.property
    def dataproc_service_account(self) -> typing.Optional[builtins.str]:
        '''User-managed service account to set on Dataproc when Cloud Data Fusion creates Dataproc to run data processing pipelines.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#dataproc_service_account GoogleDataFusionInstance#dataproc_service_account}
        '''
        result = self._values.get("dataproc_service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#description GoogleDataFusionInstance#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Display name for an instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#display_name GoogleDataFusionInstance#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_rbac(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Option to enable granular role-based access control.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#enable_rbac GoogleDataFusionInstance#enable_rbac}
        '''
        result = self._values.get("enable_rbac")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_stackdriver_logging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Option to enable Stackdriver Logging.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#enable_stackdriver_logging GoogleDataFusionInstance#enable_stackdriver_logging}
        '''
        result = self._values.get("enable_stackdriver_logging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_stackdriver_monitoring(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Option to enable Stackdriver Monitoring.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#enable_stackdriver_monitoring GoogleDataFusionInstance#enable_stackdriver_monitoring}
        '''
        result = self._values.get("enable_stackdriver_monitoring")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def event_publish_config(
        self,
    ) -> typing.Optional["GoogleDataFusionInstanceEventPublishConfig"]:
        '''event_publish_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#event_publish_config GoogleDataFusionInstance#event_publish_config}
        '''
        result = self._values.get("event_publish_config")
        return typing.cast(typing.Optional["GoogleDataFusionInstanceEventPublishConfig"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#id GoogleDataFusionInstance#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The resource labels for instance to use to annotate any related underlying resources, such as Compute Engine VMs.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#labels GoogleDataFusionInstance#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def network_config(
        self,
    ) -> typing.Optional["GoogleDataFusionInstanceNetworkConfig"]:
        '''network_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#network_config GoogleDataFusionInstance#network_config}
        '''
        result = self._values.get("network_config")
        return typing.cast(typing.Optional["GoogleDataFusionInstanceNetworkConfig"], result)

    @builtins.property
    def options(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Map of additional options used to configure the behavior of Data Fusion instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#options GoogleDataFusionInstance#options}
        '''
        result = self._values.get("options")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def private_instance(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether the Data Fusion instance should be private.

        If set to
        true, all Data Fusion nodes will have private IP addresses and will not be
        able to access the public internet.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#private_instance GoogleDataFusionInstance#private_instance}
        '''
        result = self._values.get("private_instance")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#project GoogleDataFusionInstance#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The region of the Data Fusion instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#region GoogleDataFusionInstance#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of resource manager tags.

        Resource manager tag keys and values have the same definition as resource manager tags.
        Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/{tag_value_id}.
        The field is ignored (both PUT & PATCH) when empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#tags GoogleDataFusionInstance#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleDataFusionInstanceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#timeouts GoogleDataFusionInstance#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleDataFusionInstanceTimeouts"], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Current version of the Data Fusion.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#version GoogleDataFusionInstance#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zone(self) -> typing.Optional[builtins.str]:
        '''Name of the zone in which the Data Fusion instance will be created. Only DEVELOPER instances use this field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#zone GoogleDataFusionInstance#zone}
        '''
        result = self._values.get("zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataFusionInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataFusionInstance.GoogleDataFusionInstanceCryptoKeyConfig",
    jsii_struct_bases=[],
    name_mapping={"key_reference": "keyReference"},
)
class GoogleDataFusionInstanceCryptoKeyConfig:
    def __init__(self, *, key_reference: builtins.str) -> None:
        '''
        :param key_reference: The name of the key which is used to encrypt/decrypt customer data. For key in Cloud KMS, the key should be in the format of projects/* /locations/* /keyRings/* /cryptoKeys/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#key_reference GoogleDataFusionInstance#key_reference} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b92dd082834a0a47df7441f1c313f4e8bb2ec49c01ca9e49cd9940f8b4e9886f)
            check_type(argname="argument key_reference", value=key_reference, expected_type=type_hints["key_reference"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key_reference": key_reference,
        }

    @builtins.property
    def key_reference(self) -> builtins.str:
        '''The name of the key which is used to encrypt/decrypt customer data.

        For key in Cloud KMS, the key should be in the format of projects/* /locations/* /keyRings/* /cryptoKeys/*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#key_reference GoogleDataFusionInstance#key_reference}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("key_reference")
        assert result is not None, "Required property 'key_reference' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataFusionInstanceCryptoKeyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataFusionInstanceCryptoKeyConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataFusionInstance.GoogleDataFusionInstanceCryptoKeyConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__244ebe708c604cee63a11510d10c1fb40af9685852cd23fb54c2d8679f42c733)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="keyReferenceInput")
    def key_reference_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyReferenceInput"))

    @builtins.property
    @jsii.member(jsii_name="keyReference")
    def key_reference(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyReference"))

    @key_reference.setter
    def key_reference(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2b91e38f4dd58c410ac36c63ce1f2e74033d51784a9555aa9e290599db272bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyReference", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataFusionInstanceCryptoKeyConfig]:
        return typing.cast(typing.Optional[GoogleDataFusionInstanceCryptoKeyConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataFusionInstanceCryptoKeyConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__908585032d77855006419d007b6a7bf71090163435eb0bf4182966f112de959c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataFusionInstance.GoogleDataFusionInstanceEventPublishConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "topic": "topic"},
)
class GoogleDataFusionInstanceEventPublishConfig:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        topic: builtins.str,
    ) -> None:
        '''
        :param enabled: Option to enable Event Publishing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#enabled GoogleDataFusionInstance#enabled}
        :param topic: The resource name of the Pub/Sub topic. Format: projects/{projectId}/topics/{topic_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#topic GoogleDataFusionInstance#topic}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57ff7b3cc26e2b4b736a1e7af1a3cbf96bae21223f813c15ef954a1da6a26d99)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
            "topic": topic,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Option to enable Event Publishing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#enabled GoogleDataFusionInstance#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def topic(self) -> builtins.str:
        '''The resource name of the Pub/Sub topic. Format: projects/{projectId}/topics/{topic_id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#topic GoogleDataFusionInstance#topic}
        '''
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataFusionInstanceEventPublishConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataFusionInstanceEventPublishConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataFusionInstance.GoogleDataFusionInstanceEventPublishConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2308820d1a500b36b2971e0538945d711d329fe7edcd6c722ac85e0122ce129)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="topicInput")
    def topic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "topicInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e17a97ea936df21f1b9751a474968597a7829957b481d4c5b02fcabf421cd01c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topic")
    def topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topic"))

    @topic.setter
    def topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2953a6e06429cc3cbf75efd6a00dcefe201527e7d9ec2b3271c629796d7ed226)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataFusionInstanceEventPublishConfig]:
        return typing.cast(typing.Optional[GoogleDataFusionInstanceEventPublishConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataFusionInstanceEventPublishConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__977294458046efbeb6a918ae4a249b71c74622f88fcafad2b799121b8d0ae26d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataFusionInstance.GoogleDataFusionInstanceNetworkConfig",
    jsii_struct_bases=[],
    name_mapping={
        "connection_type": "connectionType",
        "ip_allocation": "ipAllocation",
        "network": "network",
        "private_service_connect_config": "privateServiceConnectConfig",
    },
)
class GoogleDataFusionInstanceNetworkConfig:
    def __init__(
        self,
        *,
        connection_type: typing.Optional[builtins.str] = None,
        ip_allocation: typing.Optional[builtins.str] = None,
        network: typing.Optional[builtins.str] = None,
        private_service_connect_config: typing.Optional[typing.Union["GoogleDataFusionInstanceNetworkConfigPrivateServiceConnectConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection_type: Optional. Type of connection for establishing private IP connectivity between the Data Fusion customer project VPC and the corresponding tenant project from a predefined list of available connection modes. If this field is unspecified for a private instance, VPC peering is used. Possible values: ["VPC_PEERING", "PRIVATE_SERVICE_CONNECT_INTERFACES"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#connection_type GoogleDataFusionInstance#connection_type}
        :param ip_allocation: The IP range in CIDR notation to use for the managed Data Fusion instance nodes. This range must not overlap with any other ranges used in the Data Fusion instance network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#ip_allocation GoogleDataFusionInstance#ip_allocation}
        :param network: Name of the network in the project with which the tenant project will be peered for executing pipelines. In case of shared VPC where the network resides in another host project the network should specified in the form of projects/{host-project-id}/global/networks/{network} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#network GoogleDataFusionInstance#network}
        :param private_service_connect_config: private_service_connect_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#private_service_connect_config GoogleDataFusionInstance#private_service_connect_config}
        '''
        if isinstance(private_service_connect_config, dict):
            private_service_connect_config = GoogleDataFusionInstanceNetworkConfigPrivateServiceConnectConfig(**private_service_connect_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f5de47fe1715e3d337809712de178099cfbf3d176d4575e6e9d4dfe051e3998)
            check_type(argname="argument connection_type", value=connection_type, expected_type=type_hints["connection_type"])
            check_type(argname="argument ip_allocation", value=ip_allocation, expected_type=type_hints["ip_allocation"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument private_service_connect_config", value=private_service_connect_config, expected_type=type_hints["private_service_connect_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connection_type is not None:
            self._values["connection_type"] = connection_type
        if ip_allocation is not None:
            self._values["ip_allocation"] = ip_allocation
        if network is not None:
            self._values["network"] = network
        if private_service_connect_config is not None:
            self._values["private_service_connect_config"] = private_service_connect_config

    @builtins.property
    def connection_type(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Type of connection for establishing private IP connectivity between the Data Fusion customer project VPC and
        the corresponding tenant project from a predefined list of available connection modes.
        If this field is unspecified for a private instance, VPC peering is used. Possible values: ["VPC_PEERING", "PRIVATE_SERVICE_CONNECT_INTERFACES"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#connection_type GoogleDataFusionInstance#connection_type}
        '''
        result = self._values.get("connection_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_allocation(self) -> typing.Optional[builtins.str]:
        '''The IP range in CIDR notation to use for the managed Data Fusion instance nodes.

        This range must not overlap with any other ranges used in the Data Fusion instance network.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#ip_allocation GoogleDataFusionInstance#ip_allocation}
        '''
        result = self._values.get("ip_allocation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''Name of the network in the project with which the tenant project will be peered for executing pipelines.

        In case of shared VPC where the network resides in another host
        project the network should specified in the form of projects/{host-project-id}/global/networks/{network}

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#network GoogleDataFusionInstance#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_service_connect_config(
        self,
    ) -> typing.Optional["GoogleDataFusionInstanceNetworkConfigPrivateServiceConnectConfig"]:
        '''private_service_connect_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#private_service_connect_config GoogleDataFusionInstance#private_service_connect_config}
        '''
        result = self._values.get("private_service_connect_config")
        return typing.cast(typing.Optional["GoogleDataFusionInstanceNetworkConfigPrivateServiceConnectConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataFusionInstanceNetworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataFusionInstanceNetworkConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataFusionInstance.GoogleDataFusionInstanceNetworkConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6065d2b027e7c3666d0e15e105f30457db855f4051cf3e99f19983f9d6e27b48)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPrivateServiceConnectConfig")
    def put_private_service_connect_config(
        self,
        *,
        network_attachment: typing.Optional[builtins.str] = None,
        unreachable_cidr_block: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param network_attachment: Optional. The reference to the network attachment used to establish private connectivity. It will be of the form projects/{project-id}/regions/{region}/networkAttachments/{network-attachment-id}. This is required only when using connection type PRIVATE_SERVICE_CONNECT_INTERFACES. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#network_attachment GoogleDataFusionInstance#network_attachment}
        :param unreachable_cidr_block: Optional. Input only. The CIDR block to which the CDF instance can't route traffic to in the consumer project VPC. The size of this block should be at least /25. This range should not overlap with the primary address range of any subnetwork used by the network attachment. This range can be used for other purposes in the consumer VPC as long as there is no requirement for CDF to reach destinations using these addresses. If this value is not provided, the server chooses a non RFC 1918 address range. The format of this field is governed by RFC 4632. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#unreachable_cidr_block GoogleDataFusionInstance#unreachable_cidr_block}
        '''
        value = GoogleDataFusionInstanceNetworkConfigPrivateServiceConnectConfig(
            network_attachment=network_attachment,
            unreachable_cidr_block=unreachable_cidr_block,
        )

        return typing.cast(None, jsii.invoke(self, "putPrivateServiceConnectConfig", [value]))

    @jsii.member(jsii_name="resetConnectionType")
    def reset_connection_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionType", []))

    @jsii.member(jsii_name="resetIpAllocation")
    def reset_ip_allocation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAllocation", []))

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @jsii.member(jsii_name="resetPrivateServiceConnectConfig")
    def reset_private_service_connect_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateServiceConnectConfig", []))

    @builtins.property
    @jsii.member(jsii_name="privateServiceConnectConfig")
    def private_service_connect_config(
        self,
    ) -> "GoogleDataFusionInstanceNetworkConfigPrivateServiceConnectConfigOutputReference":
        return typing.cast("GoogleDataFusionInstanceNetworkConfigPrivateServiceConnectConfigOutputReference", jsii.get(self, "privateServiceConnectConfig"))

    @builtins.property
    @jsii.member(jsii_name="connectionTypeInput")
    def connection_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAllocationInput")
    def ip_allocation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAllocationInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="privateServiceConnectConfigInput")
    def private_service_connect_config_input(
        self,
    ) -> typing.Optional["GoogleDataFusionInstanceNetworkConfigPrivateServiceConnectConfig"]:
        return typing.cast(typing.Optional["GoogleDataFusionInstanceNetworkConfigPrivateServiceConnectConfig"], jsii.get(self, "privateServiceConnectConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionType")
    def connection_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionType"))

    @connection_type.setter
    def connection_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40504c525390872556c0b6630b8c9e6efed2810d5c18ac2403fb902ddfdc0f67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipAllocation")
    def ip_allocation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAllocation"))

    @ip_allocation.setter
    def ip_allocation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cffd1b9709574e5f5d88bf4db5f0d02beaad0e8216cdea7d68ec15878359e97a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAllocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46b05e5fb430a6a66261c3fdf30a41a2fe385ac1aa995a8aaad16094e508964b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleDataFusionInstanceNetworkConfig]:
        return typing.cast(typing.Optional[GoogleDataFusionInstanceNetworkConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataFusionInstanceNetworkConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1493362c4f05b94b85020babb7e9cea2b8f9fd7dbb4eabd8b84e596b47e07c85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataFusionInstance.GoogleDataFusionInstanceNetworkConfigPrivateServiceConnectConfig",
    jsii_struct_bases=[],
    name_mapping={
        "network_attachment": "networkAttachment",
        "unreachable_cidr_block": "unreachableCidrBlock",
    },
)
class GoogleDataFusionInstanceNetworkConfigPrivateServiceConnectConfig:
    def __init__(
        self,
        *,
        network_attachment: typing.Optional[builtins.str] = None,
        unreachable_cidr_block: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param network_attachment: Optional. The reference to the network attachment used to establish private connectivity. It will be of the form projects/{project-id}/regions/{region}/networkAttachments/{network-attachment-id}. This is required only when using connection type PRIVATE_SERVICE_CONNECT_INTERFACES. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#network_attachment GoogleDataFusionInstance#network_attachment}
        :param unreachable_cidr_block: Optional. Input only. The CIDR block to which the CDF instance can't route traffic to in the consumer project VPC. The size of this block should be at least /25. This range should not overlap with the primary address range of any subnetwork used by the network attachment. This range can be used for other purposes in the consumer VPC as long as there is no requirement for CDF to reach destinations using these addresses. If this value is not provided, the server chooses a non RFC 1918 address range. The format of this field is governed by RFC 4632. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#unreachable_cidr_block GoogleDataFusionInstance#unreachable_cidr_block}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98e3a8322e4c2519d0ec12169a46fe3c7ab070eaad26264773f809e21369c959)
            check_type(argname="argument network_attachment", value=network_attachment, expected_type=type_hints["network_attachment"])
            check_type(argname="argument unreachable_cidr_block", value=unreachable_cidr_block, expected_type=type_hints["unreachable_cidr_block"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if network_attachment is not None:
            self._values["network_attachment"] = network_attachment
        if unreachable_cidr_block is not None:
            self._values["unreachable_cidr_block"] = unreachable_cidr_block

    @builtins.property
    def network_attachment(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The reference to the network attachment used to establish private connectivity.
        It will be of the form projects/{project-id}/regions/{region}/networkAttachments/{network-attachment-id}.
        This is required only when using connection type PRIVATE_SERVICE_CONNECT_INTERFACES.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#network_attachment GoogleDataFusionInstance#network_attachment}
        '''
        result = self._values.get("network_attachment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def unreachable_cidr_block(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Input only. The CIDR block to which the CDF instance can't route traffic to in the consumer project VPC.
        The size of this block should be at least /25. This range should not overlap with the primary address range of any subnetwork used by the network attachment.
        This range can be used for other purposes in the consumer VPC as long as there is no requirement for CDF to reach destinations using these addresses.
        If this value is not provided, the server chooses a non RFC 1918 address range. The format of this field is governed by RFC 4632.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#unreachable_cidr_block GoogleDataFusionInstance#unreachable_cidr_block}
        '''
        result = self._values.get("unreachable_cidr_block")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataFusionInstanceNetworkConfigPrivateServiceConnectConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataFusionInstanceNetworkConfigPrivateServiceConnectConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataFusionInstance.GoogleDataFusionInstanceNetworkConfigPrivateServiceConnectConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a188b29f0e875b3d7d4d7cd06eef1536ee004763a8a0748a91412719e487dd5e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNetworkAttachment")
    def reset_network_attachment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkAttachment", []))

    @jsii.member(jsii_name="resetUnreachableCidrBlock")
    def reset_unreachable_cidr_block(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnreachableCidrBlock", []))

    @builtins.property
    @jsii.member(jsii_name="effectiveUnreachableCidrBlock")
    def effective_unreachable_cidr_block(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "effectiveUnreachableCidrBlock"))

    @builtins.property
    @jsii.member(jsii_name="networkAttachmentInput")
    def network_attachment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkAttachmentInput"))

    @builtins.property
    @jsii.member(jsii_name="unreachableCidrBlockInput")
    def unreachable_cidr_block_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "unreachableCidrBlockInput"))

    @builtins.property
    @jsii.member(jsii_name="networkAttachment")
    def network_attachment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkAttachment"))

    @network_attachment.setter
    def network_attachment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fc70d67aaca0f58b9b1c7a0877c299b8898b99bc21f9517e9c90060447e1ba4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkAttachment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="unreachableCidrBlock")
    def unreachable_cidr_block(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unreachableCidrBlock"))

    @unreachable_cidr_block.setter
    def unreachable_cidr_block(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29f0673fc6c592ff4911b85de860b575a9e3deb1dd37b6bd6d84112ddc4cc974)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unreachableCidrBlock", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataFusionInstanceNetworkConfigPrivateServiceConnectConfig]:
        return typing.cast(typing.Optional[GoogleDataFusionInstanceNetworkConfigPrivateServiceConnectConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataFusionInstanceNetworkConfigPrivateServiceConnectConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d5167dd88fe795f2a0b90269556b6dd8934be29ac1c9c5e4d7aebe9339bd500)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataFusionInstance.GoogleDataFusionInstanceTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleDataFusionInstanceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#create GoogleDataFusionInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#delete GoogleDataFusionInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#update GoogleDataFusionInstance#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e8177d2520509451d304af68c118fd0728fe02d6298aed4896474584c72d9ff)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#create GoogleDataFusionInstance#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#delete GoogleDataFusionInstance#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_data_fusion_instance#update GoogleDataFusionInstance#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataFusionInstanceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataFusionInstanceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataFusionInstance.GoogleDataFusionInstanceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__336de91740d2e933a4df01f1ea72b12bcad466307609b0534610b61af9f67d46)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__d9676b5bdcbb93c7828392dce7a75e4c1de48bd652bff1fabb70a95c2830f1af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab1e684152d5707b72ff42385faca313fd75b0fa162c73d4408b8ee90989abba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9d17707a54194827171087e5d537b495d212fe41d5d0a30be5d46044a6158af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataFusionInstanceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataFusionInstanceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataFusionInstanceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f431e3e2edf48363ea4df4cf9ca3360b44a1b8e7188b9c211b2b1f4ae4ae0ba7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleDataFusionInstance",
    "GoogleDataFusionInstanceAccelerators",
    "GoogleDataFusionInstanceAcceleratorsList",
    "GoogleDataFusionInstanceAcceleratorsOutputReference",
    "GoogleDataFusionInstanceConfig",
    "GoogleDataFusionInstanceCryptoKeyConfig",
    "GoogleDataFusionInstanceCryptoKeyConfigOutputReference",
    "GoogleDataFusionInstanceEventPublishConfig",
    "GoogleDataFusionInstanceEventPublishConfigOutputReference",
    "GoogleDataFusionInstanceNetworkConfig",
    "GoogleDataFusionInstanceNetworkConfigOutputReference",
    "GoogleDataFusionInstanceNetworkConfigPrivateServiceConnectConfig",
    "GoogleDataFusionInstanceNetworkConfigPrivateServiceConnectConfigOutputReference",
    "GoogleDataFusionInstanceTimeouts",
    "GoogleDataFusionInstanceTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__7789be7c498adef1cee8428333a671dbb197d94b9bd65a3cc84c5d8b9d9bc4a7(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    type: builtins.str,
    accelerators: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataFusionInstanceAccelerators, typing.Dict[builtins.str, typing.Any]]]]] = None,
    crypto_key_config: typing.Optional[typing.Union[GoogleDataFusionInstanceCryptoKeyConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    dataproc_service_account: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    enable_rbac: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_stackdriver_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_stackdriver_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    event_publish_config: typing.Optional[typing.Union[GoogleDataFusionInstanceEventPublishConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    network_config: typing.Optional[typing.Union[GoogleDataFusionInstanceNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    private_instance: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[GoogleDataFusionInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
    zone: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__1cb0e3d9a69129564488727f8650e010e96e3758e814bd385a7e5ebc5e320cb3(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8dd1983f31e31a32e29581339547c68d12f882535136b6e7b9d20127b264a39(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataFusionInstanceAccelerators, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f5ec404efa02fbc35038d1c9a336b4cee33ceea941a67d9d8610f1ab9abdc0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__744d131f1108c8696518fdb772b8b8053ffead20929030ae514f05c9e58f276f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bfa957bc0c475f861e3f72dc44a339b20b09d06759d9b5ca8de029fb064188e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c9fa7cad5f8c036dd7ab917d3d33a183a22d30ed427731e17f0839a804f28e2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d605ad85027d35195cfe80e694d5677a1a66f68aa386bea62d852ceac9088ff0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d685110ee01f9725d528481ddb4b55e02a0627de75060561c8c475ad9cc21364(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__317e60267c2b5da01d5ef6f74f5ba88b9bb659f759ed3a987312781f5bb33650(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03dca31ae2bbca2e1c499146785a2d3299d60a7be4c6ffabf7cc7cdabd4b7b91(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56befd806ad4089d9ba29940282c4fee581b8f84f68294f0311c8dd7c0505d2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5aa49545e65b70832ec9c6b6a155f204fa8726be1ffce107ac10ab504591df6(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f9dc75794f2911de2e80f53224b7da4a6f455e308b4574ed8871f59a5b8c84d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__439de5f95798ec6433a64cdca76b6f373adf6cdede208f96e7c72e7f13c86740(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50dc9a5dd56732964797d5bc9887b50f6e27f1002958ea7acb41542e370263c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17e9c1dd15b504cd08f072b06acf13cb224e29e6f40f59c98df0b94dfc3c7ee0(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52ba9e5494b3fa7ca19a583c6b25655cf8e759670ebb174d57875a98974ced08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54c4ae188c466376779b323750adbb2d76200314a08f8888b955a990dc0835ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03a1c02adf87cb000feb6672d1fc146241bb4c0620e35c4314dac679e9e7d0a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2edd4fbe57c4ebe92ac9ebbc8c9b44ecc7b3745335e485cb4cf402334786813(
    *,
    accelerator_type: builtins.str,
    state: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16c2eefaee34489ed2d04a313ac1df67f6c16b63843257cccb082c9a9205c2f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e0d500b5db0762d67ab5dfcd2123b35464e0f0df338d397969d3ef2c9ae8288(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04651d32cd36e46c9d09161d0c998fae3cc678623e5bcea94e56d11077e76253(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fd2110c404d13bdf0136b1644e9ea1279590dee061858405ad37fe68a14f41d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be34e757aeb4c6d8ffec3cc2338bf38361c00506ca4f763a657758c4c837fd97(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccab8c77e647663f8e7f2b40d37b3e53d4b6e67ca4bafd8be03e0912167c8a89(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataFusionInstanceAccelerators]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb4a0bbe0ede14de7ae3bc99c6c9890a174232945e42d568c040f09c22987912(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aafbd0fa4552cc9e7fd25c77cd292a5a568ab83ec363217eb1784711095af6fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99e9c047652205ba3fba893a017123b1f62aeaa54c3cfb7d7c1dee2bf1bdd8b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a547b6fc9bfb52f795757f68717bc24d951524704029f867c5575f32c8b6fbcd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataFusionInstanceAccelerators]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34a00b923d119c4a94228b2215b942b3757255dbd94a42839580a801c9e25d78(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    type: builtins.str,
    accelerators: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataFusionInstanceAccelerators, typing.Dict[builtins.str, typing.Any]]]]] = None,
    crypto_key_config: typing.Optional[typing.Union[GoogleDataFusionInstanceCryptoKeyConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    dataproc_service_account: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    enable_rbac: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_stackdriver_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_stackdriver_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    event_publish_config: typing.Optional[typing.Union[GoogleDataFusionInstanceEventPublishConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    network_config: typing.Optional[typing.Union[GoogleDataFusionInstanceNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    private_instance: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[GoogleDataFusionInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b92dd082834a0a47df7441f1c313f4e8bb2ec49c01ca9e49cd9940f8b4e9886f(
    *,
    key_reference: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__244ebe708c604cee63a11510d10c1fb40af9685852cd23fb54c2d8679f42c733(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2b91e38f4dd58c410ac36c63ce1f2e74033d51784a9555aa9e290599db272bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__908585032d77855006419d007b6a7bf71090163435eb0bf4182966f112de959c(
    value: typing.Optional[GoogleDataFusionInstanceCryptoKeyConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57ff7b3cc26e2b4b736a1e7af1a3cbf96bae21223f813c15ef954a1da6a26d99(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    topic: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2308820d1a500b36b2971e0538945d711d329fe7edcd6c722ac85e0122ce129(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e17a97ea936df21f1b9751a474968597a7829957b481d4c5b02fcabf421cd01c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2953a6e06429cc3cbf75efd6a00dcefe201527e7d9ec2b3271c629796d7ed226(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__977294458046efbeb6a918ae4a249b71c74622f88fcafad2b799121b8d0ae26d(
    value: typing.Optional[GoogleDataFusionInstanceEventPublishConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f5de47fe1715e3d337809712de178099cfbf3d176d4575e6e9d4dfe051e3998(
    *,
    connection_type: typing.Optional[builtins.str] = None,
    ip_allocation: typing.Optional[builtins.str] = None,
    network: typing.Optional[builtins.str] = None,
    private_service_connect_config: typing.Optional[typing.Union[GoogleDataFusionInstanceNetworkConfigPrivateServiceConnectConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6065d2b027e7c3666d0e15e105f30457db855f4051cf3e99f19983f9d6e27b48(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40504c525390872556c0b6630b8c9e6efed2810d5c18ac2403fb902ddfdc0f67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cffd1b9709574e5f5d88bf4db5f0d02beaad0e8216cdea7d68ec15878359e97a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46b05e5fb430a6a66261c3fdf30a41a2fe385ac1aa995a8aaad16094e508964b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1493362c4f05b94b85020babb7e9cea2b8f9fd7dbb4eabd8b84e596b47e07c85(
    value: typing.Optional[GoogleDataFusionInstanceNetworkConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98e3a8322e4c2519d0ec12169a46fe3c7ab070eaad26264773f809e21369c959(
    *,
    network_attachment: typing.Optional[builtins.str] = None,
    unreachable_cidr_block: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a188b29f0e875b3d7d4d7cd06eef1536ee004763a8a0748a91412719e487dd5e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fc70d67aaca0f58b9b1c7a0877c299b8898b99bc21f9517e9c90060447e1ba4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29f0673fc6c592ff4911b85de860b575a9e3deb1dd37b6bd6d84112ddc4cc974(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d5167dd88fe795f2a0b90269556b6dd8934be29ac1c9c5e4d7aebe9339bd500(
    value: typing.Optional[GoogleDataFusionInstanceNetworkConfigPrivateServiceConnectConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e8177d2520509451d304af68c118fd0728fe02d6298aed4896474584c72d9ff(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__336de91740d2e933a4df01f1ea72b12bcad466307609b0534610b61af9f67d46(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9676b5bdcbb93c7828392dce7a75e4c1de48bd652bff1fabb70a95c2830f1af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab1e684152d5707b72ff42385faca313fd75b0fa162c73d4408b8ee90989abba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9d17707a54194827171087e5d537b495d212fe41d5d0a30be5d46044a6158af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f431e3e2edf48363ea4df4cf9ca3360b44a1b8e7188b9c211b2b1f4ae4ae0ba7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataFusionInstanceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
