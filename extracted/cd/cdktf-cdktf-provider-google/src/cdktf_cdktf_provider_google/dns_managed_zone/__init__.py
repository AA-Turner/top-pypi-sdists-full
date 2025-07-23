r'''
# `google_dns_managed_zone`

Refer to the Terraform Registry for docs: [`google_dns_managed_zone`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone).
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


class DnsManagedZone(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsManagedZone.DnsManagedZone",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone google_dns_managed_zone}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        dns_name: builtins.str,
        name: builtins.str,
        cloud_logging_config: typing.Optional[typing.Union["DnsManagedZoneCloudLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        dnssec_config: typing.Optional[typing.Union["DnsManagedZoneDnssecConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        forwarding_config: typing.Optional[typing.Union["DnsManagedZoneForwardingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        peering_config: typing.Optional[typing.Union["DnsManagedZonePeeringConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        private_visibility_config: typing.Optional[typing.Union["DnsManagedZonePrivateVisibilityConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DnsManagedZoneTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        visibility: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone google_dns_managed_zone} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param dns_name: The DNS name of this managed zone, for instance "example.com.". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#dns_name DnsManagedZone#dns_name}
        :param name: User assigned name for this resource. Must be unique within the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#name DnsManagedZone#name}
        :param cloud_logging_config: cloud_logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#cloud_logging_config DnsManagedZone#cloud_logging_config}
        :param description: A textual description field. Defaults to 'Managed by Terraform'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#description DnsManagedZone#description}
        :param dnssec_config: dnssec_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#dnssec_config DnsManagedZone#dnssec_config}
        :param force_destroy: Set this true to delete all records in the zone. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#force_destroy DnsManagedZone#force_destroy}
        :param forwarding_config: forwarding_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#forwarding_config DnsManagedZone#forwarding_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#id DnsManagedZone#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: A set of key/value label pairs to assign to this ManagedZone. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#labels DnsManagedZone#labels}
        :param peering_config: peering_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#peering_config DnsManagedZone#peering_config}
        :param private_visibility_config: private_visibility_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#private_visibility_config DnsManagedZone#private_visibility_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#project DnsManagedZone#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#timeouts DnsManagedZone#timeouts}
        :param visibility: The zone's visibility: public zones are exposed to the Internet, while private zones are visible only to Virtual Private Cloud resources. Default value: "public" Possible values: ["private", "public"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#visibility DnsManagedZone#visibility}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bae8bd4489e13bb044dac9480d57d0a1567a2f642bf22cd29d21db408c9e44ed)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DnsManagedZoneConfig(
            dns_name=dns_name,
            name=name,
            cloud_logging_config=cloud_logging_config,
            description=description,
            dnssec_config=dnssec_config,
            force_destroy=force_destroy,
            forwarding_config=forwarding_config,
            id=id,
            labels=labels,
            peering_config=peering_config,
            private_visibility_config=private_visibility_config,
            project=project,
            timeouts=timeouts,
            visibility=visibility,
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
        '''Generates CDKTF code for importing a DnsManagedZone resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DnsManagedZone to import.
        :param import_from_id: The id of the existing DnsManagedZone that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DnsManagedZone to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af35231bcee9ffac365c6cfb26e71abd6d216b71902146eb4c463731b8d79d8a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCloudLoggingConfig")
    def put_cloud_logging_config(
        self,
        *,
        enable_logging: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enable_logging: If set, enable query logging for this ManagedZone. False by default, making logging opt-in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#enable_logging DnsManagedZone#enable_logging}
        '''
        value = DnsManagedZoneCloudLoggingConfig(enable_logging=enable_logging)

        return typing.cast(None, jsii.invoke(self, "putCloudLoggingConfig", [value]))

    @jsii.member(jsii_name="putDnssecConfig")
    def put_dnssec_config(
        self,
        *,
        default_key_specs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DnsManagedZoneDnssecConfigDefaultKeySpecs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        kind: typing.Optional[builtins.str] = None,
        non_existence: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param default_key_specs: default_key_specs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#default_key_specs DnsManagedZone#default_key_specs}
        :param kind: Identifies what kind of resource this is. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#kind DnsManagedZone#kind}
        :param non_existence: Specifies the mechanism used to provide authenticated denial-of-existence responses. non_existence can only be updated when the state is 'off'. Possible values: ["nsec", "nsec3"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#non_existence DnsManagedZone#non_existence}
        :param state: Specifies whether DNSSEC is enabled, and what mode it is in Possible values: ["off", "on", "transfer"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#state DnsManagedZone#state}
        '''
        value = DnsManagedZoneDnssecConfig(
            default_key_specs=default_key_specs,
            kind=kind,
            non_existence=non_existence,
            state=state,
        )

        return typing.cast(None, jsii.invoke(self, "putDnssecConfig", [value]))

    @jsii.member(jsii_name="putForwardingConfig")
    def put_forwarding_config(
        self,
        *,
        target_name_servers: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DnsManagedZoneForwardingConfigTargetNameServers", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param target_name_servers: target_name_servers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#target_name_servers DnsManagedZone#target_name_servers}
        '''
        value = DnsManagedZoneForwardingConfig(target_name_servers=target_name_servers)

        return typing.cast(None, jsii.invoke(self, "putForwardingConfig", [value]))

    @jsii.member(jsii_name="putPeeringConfig")
    def put_peering_config(
        self,
        *,
        target_network: typing.Union["DnsManagedZonePeeringConfigTargetNetwork", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param target_network: target_network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#target_network DnsManagedZone#target_network}
        '''
        value = DnsManagedZonePeeringConfig(target_network=target_network)

        return typing.cast(None, jsii.invoke(self, "putPeeringConfig", [value]))

    @jsii.member(jsii_name="putPrivateVisibilityConfig")
    def put_private_visibility_config(
        self,
        *,
        gke_clusters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DnsManagedZonePrivateVisibilityConfigGkeClusters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        networks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DnsManagedZonePrivateVisibilityConfigNetworks", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param gke_clusters: gke_clusters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#gke_clusters DnsManagedZone#gke_clusters}
        :param networks: networks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#networks DnsManagedZone#networks}
        '''
        value = DnsManagedZonePrivateVisibilityConfig(
            gke_clusters=gke_clusters, networks=networks
        )

        return typing.cast(None, jsii.invoke(self, "putPrivateVisibilityConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#create DnsManagedZone#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#delete DnsManagedZone#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#update DnsManagedZone#update}.
        '''
        value = DnsManagedZoneTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCloudLoggingConfig")
    def reset_cloud_logging_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudLoggingConfig", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDnssecConfig")
    def reset_dnssec_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDnssecConfig", []))

    @jsii.member(jsii_name="resetForceDestroy")
    def reset_force_destroy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForceDestroy", []))

    @jsii.member(jsii_name="resetForwardingConfig")
    def reset_forwarding_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForwardingConfig", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetPeeringConfig")
    def reset_peering_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeeringConfig", []))

    @jsii.member(jsii_name="resetPrivateVisibilityConfig")
    def reset_private_visibility_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateVisibilityConfig", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVisibility")
    def reset_visibility(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVisibility", []))

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
    @jsii.member(jsii_name="cloudLoggingConfig")
    def cloud_logging_config(self) -> "DnsManagedZoneCloudLoggingConfigOutputReference":
        return typing.cast("DnsManagedZoneCloudLoggingConfigOutputReference", jsii.get(self, "cloudLoggingConfig"))

    @builtins.property
    @jsii.member(jsii_name="creationTime")
    def creation_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationTime"))

    @builtins.property
    @jsii.member(jsii_name="dnssecConfig")
    def dnssec_config(self) -> "DnsManagedZoneDnssecConfigOutputReference":
        return typing.cast("DnsManagedZoneDnssecConfigOutputReference", jsii.get(self, "dnssecConfig"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="forwardingConfig")
    def forwarding_config(self) -> "DnsManagedZoneForwardingConfigOutputReference":
        return typing.cast("DnsManagedZoneForwardingConfigOutputReference", jsii.get(self, "forwardingConfig"))

    @builtins.property
    @jsii.member(jsii_name="managedZoneId")
    def managed_zone_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "managedZoneId"))

    @builtins.property
    @jsii.member(jsii_name="nameServers")
    def name_servers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "nameServers"))

    @builtins.property
    @jsii.member(jsii_name="peeringConfig")
    def peering_config(self) -> "DnsManagedZonePeeringConfigOutputReference":
        return typing.cast("DnsManagedZonePeeringConfigOutputReference", jsii.get(self, "peeringConfig"))

    @builtins.property
    @jsii.member(jsii_name="privateVisibilityConfig")
    def private_visibility_config(
        self,
    ) -> "DnsManagedZonePrivateVisibilityConfigOutputReference":
        return typing.cast("DnsManagedZonePrivateVisibilityConfigOutputReference", jsii.get(self, "privateVisibilityConfig"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DnsManagedZoneTimeoutsOutputReference":
        return typing.cast("DnsManagedZoneTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="cloudLoggingConfigInput")
    def cloud_logging_config_input(
        self,
    ) -> typing.Optional["DnsManagedZoneCloudLoggingConfig"]:
        return typing.cast(typing.Optional["DnsManagedZoneCloudLoggingConfig"], jsii.get(self, "cloudLoggingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsNameInput")
    def dns_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dnsNameInput"))

    @builtins.property
    @jsii.member(jsii_name="dnssecConfigInput")
    def dnssec_config_input(self) -> typing.Optional["DnsManagedZoneDnssecConfig"]:
        return typing.cast(typing.Optional["DnsManagedZoneDnssecConfig"], jsii.get(self, "dnssecConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="forceDestroyInput")
    def force_destroy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "forceDestroyInput"))

    @builtins.property
    @jsii.member(jsii_name="forwardingConfigInput")
    def forwarding_config_input(
        self,
    ) -> typing.Optional["DnsManagedZoneForwardingConfig"]:
        return typing.cast(typing.Optional["DnsManagedZoneForwardingConfig"], jsii.get(self, "forwardingConfigInput"))

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
    @jsii.member(jsii_name="peeringConfigInput")
    def peering_config_input(self) -> typing.Optional["DnsManagedZonePeeringConfig"]:
        return typing.cast(typing.Optional["DnsManagedZonePeeringConfig"], jsii.get(self, "peeringConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="privateVisibilityConfigInput")
    def private_visibility_config_input(
        self,
    ) -> typing.Optional["DnsManagedZonePrivateVisibilityConfig"]:
        return typing.cast(typing.Optional["DnsManagedZonePrivateVisibilityConfig"], jsii.get(self, "privateVisibilityConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DnsManagedZoneTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DnsManagedZoneTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="visibilityInput")
    def visibility_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "visibilityInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd614a815802671911a4ae34842c47b9463e993029daa6bf0aca4c1c407c073d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dnsName")
    def dns_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dnsName"))

    @dns_name.setter
    def dns_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe223154d0193dea1d55176e2cd9da26f98851a0d89b7df4d70a4a9b5200652c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forceDestroy")
    def force_destroy(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "forceDestroy"))

    @force_destroy.setter
    def force_destroy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b94b968690d09550990d10e8374a5f143eed97a42384d8b7b9a10096752a043e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceDestroy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d901b4f364c5a95f3da17635065a7c052545dc443a03d9f41a5f4e30079d0bae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ec2a1af2508dfe227ec3d61cbde24f9ffd6211ba2f857d8f970279d402cea07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f8b488c57b4be85c21d5d3557eef0beee74006e6abe0dbd01057681bbce7371)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c93cf9eb638559bb180c03aa325e34eced1935cec49f8378a197fa2d350beb23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="visibility")
    def visibility(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "visibility"))

    @visibility.setter
    def visibility(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf7ddc6b35b9bb7163098db435d2d0efa76dd48d3f3744379ba777cc0ed39fd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "visibility", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsManagedZone.DnsManagedZoneCloudLoggingConfig",
    jsii_struct_bases=[],
    name_mapping={"enable_logging": "enableLogging"},
)
class DnsManagedZoneCloudLoggingConfig:
    def __init__(
        self,
        *,
        enable_logging: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enable_logging: If set, enable query logging for this ManagedZone. False by default, making logging opt-in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#enable_logging DnsManagedZone#enable_logging}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e60f1aa42226533e4eb5532cafb11507125f712eef5dab08ac5b8d00adc21b34)
            check_type(argname="argument enable_logging", value=enable_logging, expected_type=type_hints["enable_logging"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enable_logging": enable_logging,
        }

    @builtins.property
    def enable_logging(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''If set, enable query logging for this ManagedZone. False by default, making logging opt-in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#enable_logging DnsManagedZone#enable_logging}
        '''
        result = self._values.get("enable_logging")
        assert result is not None, "Required property 'enable_logging' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsManagedZoneCloudLoggingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DnsManagedZoneCloudLoggingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsManagedZone.DnsManagedZoneCloudLoggingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a3511fa8209871327a0a7fd8d4c1dac7f4ffdd837b2e677ba81b086bacfedf9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="enableLoggingInput")
    def enable_logging_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableLoggingInput"))

    @builtins.property
    @jsii.member(jsii_name="enableLogging")
    def enable_logging(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableLogging"))

    @enable_logging.setter
    def enable_logging(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__599a44fccde2d949440a21873c9daa258f89c2b9d9b6ba491d596c5d1ff4f834)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableLogging", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DnsManagedZoneCloudLoggingConfig]:
        return typing.cast(typing.Optional[DnsManagedZoneCloudLoggingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DnsManagedZoneCloudLoggingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__747bcf9bd518ca66f2fd4e177a309283fee47238499cf305bbbdf07dc8d60822)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsManagedZone.DnsManagedZoneConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "dns_name": "dnsName",
        "name": "name",
        "cloud_logging_config": "cloudLoggingConfig",
        "description": "description",
        "dnssec_config": "dnssecConfig",
        "force_destroy": "forceDestroy",
        "forwarding_config": "forwardingConfig",
        "id": "id",
        "labels": "labels",
        "peering_config": "peeringConfig",
        "private_visibility_config": "privateVisibilityConfig",
        "project": "project",
        "timeouts": "timeouts",
        "visibility": "visibility",
    },
)
class DnsManagedZoneConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        dns_name: builtins.str,
        name: builtins.str,
        cloud_logging_config: typing.Optional[typing.Union[DnsManagedZoneCloudLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        dnssec_config: typing.Optional[typing.Union["DnsManagedZoneDnssecConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        forwarding_config: typing.Optional[typing.Union["DnsManagedZoneForwardingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        peering_config: typing.Optional[typing.Union["DnsManagedZonePeeringConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        private_visibility_config: typing.Optional[typing.Union["DnsManagedZonePrivateVisibilityConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DnsManagedZoneTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        visibility: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param dns_name: The DNS name of this managed zone, for instance "example.com.". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#dns_name DnsManagedZone#dns_name}
        :param name: User assigned name for this resource. Must be unique within the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#name DnsManagedZone#name}
        :param cloud_logging_config: cloud_logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#cloud_logging_config DnsManagedZone#cloud_logging_config}
        :param description: A textual description field. Defaults to 'Managed by Terraform'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#description DnsManagedZone#description}
        :param dnssec_config: dnssec_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#dnssec_config DnsManagedZone#dnssec_config}
        :param force_destroy: Set this true to delete all records in the zone. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#force_destroy DnsManagedZone#force_destroy}
        :param forwarding_config: forwarding_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#forwarding_config DnsManagedZone#forwarding_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#id DnsManagedZone#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: A set of key/value label pairs to assign to this ManagedZone. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#labels DnsManagedZone#labels}
        :param peering_config: peering_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#peering_config DnsManagedZone#peering_config}
        :param private_visibility_config: private_visibility_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#private_visibility_config DnsManagedZone#private_visibility_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#project DnsManagedZone#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#timeouts DnsManagedZone#timeouts}
        :param visibility: The zone's visibility: public zones are exposed to the Internet, while private zones are visible only to Virtual Private Cloud resources. Default value: "public" Possible values: ["private", "public"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#visibility DnsManagedZone#visibility}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(cloud_logging_config, dict):
            cloud_logging_config = DnsManagedZoneCloudLoggingConfig(**cloud_logging_config)
        if isinstance(dnssec_config, dict):
            dnssec_config = DnsManagedZoneDnssecConfig(**dnssec_config)
        if isinstance(forwarding_config, dict):
            forwarding_config = DnsManagedZoneForwardingConfig(**forwarding_config)
        if isinstance(peering_config, dict):
            peering_config = DnsManagedZonePeeringConfig(**peering_config)
        if isinstance(private_visibility_config, dict):
            private_visibility_config = DnsManagedZonePrivateVisibilityConfig(**private_visibility_config)
        if isinstance(timeouts, dict):
            timeouts = DnsManagedZoneTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d67f36e7f80918c4800027e645b6088d484f7d2919b39454c8b8c1d2230fa1f5)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument dns_name", value=dns_name, expected_type=type_hints["dns_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument cloud_logging_config", value=cloud_logging_config, expected_type=type_hints["cloud_logging_config"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument dnssec_config", value=dnssec_config, expected_type=type_hints["dnssec_config"])
            check_type(argname="argument force_destroy", value=force_destroy, expected_type=type_hints["force_destroy"])
            check_type(argname="argument forwarding_config", value=forwarding_config, expected_type=type_hints["forwarding_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument peering_config", value=peering_config, expected_type=type_hints["peering_config"])
            check_type(argname="argument private_visibility_config", value=private_visibility_config, expected_type=type_hints["private_visibility_config"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument visibility", value=visibility, expected_type=type_hints["visibility"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dns_name": dns_name,
            "name": name,
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
        if cloud_logging_config is not None:
            self._values["cloud_logging_config"] = cloud_logging_config
        if description is not None:
            self._values["description"] = description
        if dnssec_config is not None:
            self._values["dnssec_config"] = dnssec_config
        if force_destroy is not None:
            self._values["force_destroy"] = force_destroy
        if forwarding_config is not None:
            self._values["forwarding_config"] = forwarding_config
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if peering_config is not None:
            self._values["peering_config"] = peering_config
        if private_visibility_config is not None:
            self._values["private_visibility_config"] = private_visibility_config
        if project is not None:
            self._values["project"] = project
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if visibility is not None:
            self._values["visibility"] = visibility

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
    def dns_name(self) -> builtins.str:
        '''The DNS name of this managed zone, for instance "example.com.".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#dns_name DnsManagedZone#dns_name}
        '''
        result = self._values.get("dns_name")
        assert result is not None, "Required property 'dns_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''User assigned name for this resource. Must be unique within the project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#name DnsManagedZone#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cloud_logging_config(self) -> typing.Optional[DnsManagedZoneCloudLoggingConfig]:
        '''cloud_logging_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#cloud_logging_config DnsManagedZone#cloud_logging_config}
        '''
        result = self._values.get("cloud_logging_config")
        return typing.cast(typing.Optional[DnsManagedZoneCloudLoggingConfig], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A textual description field. Defaults to 'Managed by Terraform'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#description DnsManagedZone#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dnssec_config(self) -> typing.Optional["DnsManagedZoneDnssecConfig"]:
        '''dnssec_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#dnssec_config DnsManagedZone#dnssec_config}
        '''
        result = self._values.get("dnssec_config")
        return typing.cast(typing.Optional["DnsManagedZoneDnssecConfig"], result)

    @builtins.property
    def force_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set this true to delete all records in the zone.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#force_destroy DnsManagedZone#force_destroy}
        '''
        result = self._values.get("force_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def forwarding_config(self) -> typing.Optional["DnsManagedZoneForwardingConfig"]:
        '''forwarding_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#forwarding_config DnsManagedZone#forwarding_config}
        '''
        result = self._values.get("forwarding_config")
        return typing.cast(typing.Optional["DnsManagedZoneForwardingConfig"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#id DnsManagedZone#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A set of key/value label pairs to assign to this ManagedZone.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#labels DnsManagedZone#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def peering_config(self) -> typing.Optional["DnsManagedZonePeeringConfig"]:
        '''peering_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#peering_config DnsManagedZone#peering_config}
        '''
        result = self._values.get("peering_config")
        return typing.cast(typing.Optional["DnsManagedZonePeeringConfig"], result)

    @builtins.property
    def private_visibility_config(
        self,
    ) -> typing.Optional["DnsManagedZonePrivateVisibilityConfig"]:
        '''private_visibility_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#private_visibility_config DnsManagedZone#private_visibility_config}
        '''
        result = self._values.get("private_visibility_config")
        return typing.cast(typing.Optional["DnsManagedZonePrivateVisibilityConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#project DnsManagedZone#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DnsManagedZoneTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#timeouts DnsManagedZone#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DnsManagedZoneTimeouts"], result)

    @builtins.property
    def visibility(self) -> typing.Optional[builtins.str]:
        '''The zone's visibility: public zones are exposed to the Internet, while private zones are visible only to Virtual Private Cloud resources.

        Default value: "public" Possible values: ["private", "public"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#visibility DnsManagedZone#visibility}
        '''
        result = self._values.get("visibility")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsManagedZoneConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsManagedZone.DnsManagedZoneDnssecConfig",
    jsii_struct_bases=[],
    name_mapping={
        "default_key_specs": "defaultKeySpecs",
        "kind": "kind",
        "non_existence": "nonExistence",
        "state": "state",
    },
)
class DnsManagedZoneDnssecConfig:
    def __init__(
        self,
        *,
        default_key_specs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DnsManagedZoneDnssecConfigDefaultKeySpecs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        kind: typing.Optional[builtins.str] = None,
        non_existence: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param default_key_specs: default_key_specs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#default_key_specs DnsManagedZone#default_key_specs}
        :param kind: Identifies what kind of resource this is. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#kind DnsManagedZone#kind}
        :param non_existence: Specifies the mechanism used to provide authenticated denial-of-existence responses. non_existence can only be updated when the state is 'off'. Possible values: ["nsec", "nsec3"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#non_existence DnsManagedZone#non_existence}
        :param state: Specifies whether DNSSEC is enabled, and what mode it is in Possible values: ["off", "on", "transfer"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#state DnsManagedZone#state}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45926a3339633e062ca5a052aa6e397fca4ebd0ea84d7ccb8c07d8483bea7c5a)
            check_type(argname="argument default_key_specs", value=default_key_specs, expected_type=type_hints["default_key_specs"])
            check_type(argname="argument kind", value=kind, expected_type=type_hints["kind"])
            check_type(argname="argument non_existence", value=non_existence, expected_type=type_hints["non_existence"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_key_specs is not None:
            self._values["default_key_specs"] = default_key_specs
        if kind is not None:
            self._values["kind"] = kind
        if non_existence is not None:
            self._values["non_existence"] = non_existence
        if state is not None:
            self._values["state"] = state

    @builtins.property
    def default_key_specs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DnsManagedZoneDnssecConfigDefaultKeySpecs"]]]:
        '''default_key_specs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#default_key_specs DnsManagedZone#default_key_specs}
        '''
        result = self._values.get("default_key_specs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DnsManagedZoneDnssecConfigDefaultKeySpecs"]]], result)

    @builtins.property
    def kind(self) -> typing.Optional[builtins.str]:
        '''Identifies what kind of resource this is.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#kind DnsManagedZone#kind}
        '''
        result = self._values.get("kind")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def non_existence(self) -> typing.Optional[builtins.str]:
        '''Specifies the mechanism used to provide authenticated denial-of-existence responses.

        non_existence can only be updated when the state is 'off'. Possible values: ["nsec", "nsec3"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#non_existence DnsManagedZone#non_existence}
        '''
        result = self._values.get("non_existence")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''Specifies whether DNSSEC is enabled, and what mode it is in Possible values: ["off", "on", "transfer"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#state DnsManagedZone#state}
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsManagedZoneDnssecConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsManagedZone.DnsManagedZoneDnssecConfigDefaultKeySpecs",
    jsii_struct_bases=[],
    name_mapping={
        "algorithm": "algorithm",
        "key_length": "keyLength",
        "key_type": "keyType",
        "kind": "kind",
    },
)
class DnsManagedZoneDnssecConfigDefaultKeySpecs:
    def __init__(
        self,
        *,
        algorithm: typing.Optional[builtins.str] = None,
        key_length: typing.Optional[jsii.Number] = None,
        key_type: typing.Optional[builtins.str] = None,
        kind: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param algorithm: String mnemonic specifying the DNSSEC algorithm of this key Possible values: ["ecdsap256sha256", "ecdsap384sha384", "rsasha1", "rsasha256", "rsasha512"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#algorithm DnsManagedZone#algorithm}
        :param key_length: Length of the keys in bits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#key_length DnsManagedZone#key_length}
        :param key_type: Specifies whether this is a key signing key (KSK) or a zone signing key (ZSK). Key signing keys have the Secure Entry Point flag set and, when active, will only be used to sign resource record sets of type DNSKEY. Zone signing keys do not have the Secure Entry Point flag set and will be used to sign all other types of resource record sets. Possible values: ["keySigning", "zoneSigning"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#key_type DnsManagedZone#key_type}
        :param kind: Identifies what kind of resource this is. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#kind DnsManagedZone#kind}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6bd0d4afe2836e3de53e859d3d9f664bf1a26f8aabb46c220f81741c8c9863c)
            check_type(argname="argument algorithm", value=algorithm, expected_type=type_hints["algorithm"])
            check_type(argname="argument key_length", value=key_length, expected_type=type_hints["key_length"])
            check_type(argname="argument key_type", value=key_type, expected_type=type_hints["key_type"])
            check_type(argname="argument kind", value=kind, expected_type=type_hints["kind"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if algorithm is not None:
            self._values["algorithm"] = algorithm
        if key_length is not None:
            self._values["key_length"] = key_length
        if key_type is not None:
            self._values["key_type"] = key_type
        if kind is not None:
            self._values["kind"] = kind

    @builtins.property
    def algorithm(self) -> typing.Optional[builtins.str]:
        '''String mnemonic specifying the DNSSEC algorithm of this key Possible values: ["ecdsap256sha256", "ecdsap384sha384", "rsasha1", "rsasha256", "rsasha512"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#algorithm DnsManagedZone#algorithm}
        '''
        result = self._values.get("algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_length(self) -> typing.Optional[jsii.Number]:
        '''Length of the keys in bits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#key_length DnsManagedZone#key_length}
        '''
        result = self._values.get("key_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def key_type(self) -> typing.Optional[builtins.str]:
        '''Specifies whether this is a key signing key (KSK) or a zone signing key (ZSK).

        Key signing keys have the Secure Entry
        Point flag set and, when active, will only be used to sign
        resource record sets of type DNSKEY. Zone signing keys do
        not have the Secure Entry Point flag set and will be used
        to sign all other types of resource record sets. Possible values: ["keySigning", "zoneSigning"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#key_type DnsManagedZone#key_type}
        '''
        result = self._values.get("key_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kind(self) -> typing.Optional[builtins.str]:
        '''Identifies what kind of resource this is.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#kind DnsManagedZone#kind}
        '''
        result = self._values.get("kind")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsManagedZoneDnssecConfigDefaultKeySpecs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DnsManagedZoneDnssecConfigDefaultKeySpecsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsManagedZone.DnsManagedZoneDnssecConfigDefaultKeySpecsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf06550c0388dd93e3137d80ea178eeb126bef063d0964d4f1c477316919ca63)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DnsManagedZoneDnssecConfigDefaultKeySpecsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47ef922b264caa06dce616395dd3ee294050278ad0000a30badb3d78a07759eb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DnsManagedZoneDnssecConfigDefaultKeySpecsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5974926f20c2615d515f2013144457974c4ce7e264a027886202b134feda6d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7290fa3e69af9c628367b1afbd44e3c5b0c378a3a95256bc1a860ee4d5550bb9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed5aab66b2fa1f77497e229ee84fb98af719067df65f7548ed8b90cc7c90634f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsManagedZoneDnssecConfigDefaultKeySpecs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsManagedZoneDnssecConfigDefaultKeySpecs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsManagedZoneDnssecConfigDefaultKeySpecs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c51bfcf059513eb3da5ee3e3cf99a9d8ed23a77a8ef0e4d1a88bdf3d0562748)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DnsManagedZoneDnssecConfigDefaultKeySpecsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsManagedZone.DnsManagedZoneDnssecConfigDefaultKeySpecsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9fe5653a535c7f74c0cc8d48ae650dc7a924005b28a7fc44a67e2cfadbeae28)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAlgorithm")
    def reset_algorithm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlgorithm", []))

    @jsii.member(jsii_name="resetKeyLength")
    def reset_key_length(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyLength", []))

    @jsii.member(jsii_name="resetKeyType")
    def reset_key_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyType", []))

    @jsii.member(jsii_name="resetKind")
    def reset_kind(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKind", []))

    @builtins.property
    @jsii.member(jsii_name="algorithmInput")
    def algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "algorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="keyLengthInput")
    def key_length_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "keyLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="keyTypeInput")
    def key_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="kindInput")
    def kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kindInput"))

    @builtins.property
    @jsii.member(jsii_name="algorithm")
    def algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "algorithm"))

    @algorithm.setter
    def algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b97f78cda891231928f31cf621cc4effd1046a03bb1c542076458c4c8c2edc46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "algorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyLength")
    def key_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "keyLength"))

    @key_length.setter
    def key_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d2bdc3022194c768b561b851be789c54d22d7f168a62736c75af8f725e31be5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyLength", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyType")
    def key_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyType"))

    @key_type.setter
    def key_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caaed901fa594bf801684d1625b994a9a1a443c31de1e1528bef8278c70a4195)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kind"))

    @kind.setter
    def kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20134ecea3e51961ecaacf804d4b6fd3d144316a03489c12405892df19ebc754)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsManagedZoneDnssecConfigDefaultKeySpecs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsManagedZoneDnssecConfigDefaultKeySpecs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsManagedZoneDnssecConfigDefaultKeySpecs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7230c564c815311d663fad547b40b8c41438a3d52c6c6910ce0480f9e44726a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DnsManagedZoneDnssecConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsManagedZone.DnsManagedZoneDnssecConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c32657c0300ff5ea84b819ebd2bba523f52ba416df819bc525d25381345831e7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDefaultKeySpecs")
    def put_default_key_specs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DnsManagedZoneDnssecConfigDefaultKeySpecs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6b8f7bb5551368f379c6a96222325bcd0de906da32ec526badf6714ebee6811)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDefaultKeySpecs", [value]))

    @jsii.member(jsii_name="resetDefaultKeySpecs")
    def reset_default_key_specs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultKeySpecs", []))

    @jsii.member(jsii_name="resetKind")
    def reset_kind(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKind", []))

    @jsii.member(jsii_name="resetNonExistence")
    def reset_non_existence(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNonExistence", []))

    @jsii.member(jsii_name="resetState")
    def reset_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetState", []))

    @builtins.property
    @jsii.member(jsii_name="defaultKeySpecs")
    def default_key_specs(self) -> DnsManagedZoneDnssecConfigDefaultKeySpecsList:
        return typing.cast(DnsManagedZoneDnssecConfigDefaultKeySpecsList, jsii.get(self, "defaultKeySpecs"))

    @builtins.property
    @jsii.member(jsii_name="defaultKeySpecsInput")
    def default_key_specs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsManagedZoneDnssecConfigDefaultKeySpecs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsManagedZoneDnssecConfigDefaultKeySpecs]]], jsii.get(self, "defaultKeySpecsInput"))

    @builtins.property
    @jsii.member(jsii_name="kindInput")
    def kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kindInput"))

    @builtins.property
    @jsii.member(jsii_name="nonExistenceInput")
    def non_existence_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nonExistenceInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kind"))

    @kind.setter
    def kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2d54201cc0d6c1ef29ae96fcb89ae471cc95a019d22ee6b15b4568d73c80e35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nonExistence")
    def non_existence(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nonExistence"))

    @non_existence.setter
    def non_existence(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f4207e5f75eeac30dea9b5573643f6666297402f58627418c7bf5c4272667ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nonExistence", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6db300620150f310a5e3c0c4e06005b903e579d16ed0f7fed3d707297b418e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DnsManagedZoneDnssecConfig]:
        return typing.cast(typing.Optional[DnsManagedZoneDnssecConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DnsManagedZoneDnssecConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab9e9afe733e593338f015722851d94a3273a10833eb59f35b4e197562b77df3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsManagedZone.DnsManagedZoneForwardingConfig",
    jsii_struct_bases=[],
    name_mapping={"target_name_servers": "targetNameServers"},
)
class DnsManagedZoneForwardingConfig:
    def __init__(
        self,
        *,
        target_name_servers: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DnsManagedZoneForwardingConfigTargetNameServers", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param target_name_servers: target_name_servers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#target_name_servers DnsManagedZone#target_name_servers}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f124430e7ef0dcf69b273c0b0e708bb6ba2fa9ea55652d57fb2eea7605eaa78d)
            check_type(argname="argument target_name_servers", value=target_name_servers, expected_type=type_hints["target_name_servers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target_name_servers": target_name_servers,
        }

    @builtins.property
    def target_name_servers(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DnsManagedZoneForwardingConfigTargetNameServers"]]:
        '''target_name_servers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#target_name_servers DnsManagedZone#target_name_servers}
        '''
        result = self._values.get("target_name_servers")
        assert result is not None, "Required property 'target_name_servers' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DnsManagedZoneForwardingConfigTargetNameServers"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsManagedZoneForwardingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DnsManagedZoneForwardingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsManagedZone.DnsManagedZoneForwardingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b54ff33e275c0e7d9497d2af8d39e1f646c8e149ea2081d18d79840ae79f3fbb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTargetNameServers")
    def put_target_name_servers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DnsManagedZoneForwardingConfigTargetNameServers", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__515e11322e3f370c69744d9867ff8a5903d3ed214a3d9ca7a6e12012707e4815)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTargetNameServers", [value]))

    @builtins.property
    @jsii.member(jsii_name="targetNameServers")
    def target_name_servers(
        self,
    ) -> "DnsManagedZoneForwardingConfigTargetNameServersList":
        return typing.cast("DnsManagedZoneForwardingConfigTargetNameServersList", jsii.get(self, "targetNameServers"))

    @builtins.property
    @jsii.member(jsii_name="targetNameServersInput")
    def target_name_servers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DnsManagedZoneForwardingConfigTargetNameServers"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DnsManagedZoneForwardingConfigTargetNameServers"]]], jsii.get(self, "targetNameServersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DnsManagedZoneForwardingConfig]:
        return typing.cast(typing.Optional[DnsManagedZoneForwardingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DnsManagedZoneForwardingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55894e2da55461ed78c5f9630152ccd3e5d148c92a595a921505f59a65bae209)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsManagedZone.DnsManagedZoneForwardingConfigTargetNameServers",
    jsii_struct_bases=[],
    name_mapping={
        "domain_name": "domainName",
        "forwarding_path": "forwardingPath",
        "ipv4_address": "ipv4Address",
    },
)
class DnsManagedZoneForwardingConfigTargetNameServers:
    def __init__(
        self,
        *,
        domain_name: typing.Optional[builtins.str] = None,
        forwarding_path: typing.Optional[builtins.str] = None,
        ipv4_address: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param domain_name: Fully qualified domain name for the forwarding target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#domain_name DnsManagedZone#domain_name}
        :param forwarding_path: Forwarding path for this TargetNameServer. If unset or 'default' Cloud DNS will make forwarding decision based on address ranges, i.e. RFC1918 addresses go to the VPC, Non-RFC1918 addresses go to the Internet. When set to 'private', Cloud DNS will always send queries through VPC for this target Possible values: ["default", "private"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#forwarding_path DnsManagedZone#forwarding_path}
        :param ipv4_address: IPv4 address of a target name server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#ipv4_address DnsManagedZone#ipv4_address}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e84e52b2e964cfb854c1bb4217b98a5238ae6706e8b2e0a5f6d98785b821b94)
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument forwarding_path", value=forwarding_path, expected_type=type_hints["forwarding_path"])
            check_type(argname="argument ipv4_address", value=ipv4_address, expected_type=type_hints["ipv4_address"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if forwarding_path is not None:
            self._values["forwarding_path"] = forwarding_path
        if ipv4_address is not None:
            self._values["ipv4_address"] = ipv4_address

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''Fully qualified domain name for the forwarding target.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#domain_name DnsManagedZone#domain_name}
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def forwarding_path(self) -> typing.Optional[builtins.str]:
        '''Forwarding path for this TargetNameServer.

        If unset or 'default' Cloud DNS will make forwarding
        decision based on address ranges, i.e. RFC1918 addresses go to the VPC, Non-RFC1918 addresses go
        to the Internet. When set to 'private', Cloud DNS will always send queries through VPC for this target Possible values: ["default", "private"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#forwarding_path DnsManagedZone#forwarding_path}
        '''
        result = self._values.get("forwarding_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ipv4_address(self) -> typing.Optional[builtins.str]:
        '''IPv4 address of a target name server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#ipv4_address DnsManagedZone#ipv4_address}
        '''
        result = self._values.get("ipv4_address")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsManagedZoneForwardingConfigTargetNameServers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DnsManagedZoneForwardingConfigTargetNameServersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsManagedZone.DnsManagedZoneForwardingConfigTargetNameServersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc2a2271d3702faa2e2397767dd3f8fdd727d63d7414912e526b1a9ece8b1e73)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DnsManagedZoneForwardingConfigTargetNameServersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0515c95a72b45c4af8b375afbb6a20f3cef3d8aa05212b60412d0640aefe356b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DnsManagedZoneForwardingConfigTargetNameServersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91759fa6610c573694bc48ec170e89ab96807849431ed029a1af6973d50127ee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__515fc1c7d55227fe3e8d783c9bf29022c4f889d1bd81e730f125cdcdaa9a7555)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3618ea26a6744044792607b8f3ed66cd81bcb48fd04639ddb63175498ae971a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsManagedZoneForwardingConfigTargetNameServers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsManagedZoneForwardingConfigTargetNameServers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsManagedZoneForwardingConfigTargetNameServers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b29202d95673896103ae46380412bc6ff6badfc36be9ffdcb079043f186d7118)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DnsManagedZoneForwardingConfigTargetNameServersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsManagedZone.DnsManagedZoneForwardingConfigTargetNameServersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__29623ad39025035f4d35935ed7872dc04dc97173baf580e9993aa131f3c9dced)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDomainName")
    def reset_domain_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomainName", []))

    @jsii.member(jsii_name="resetForwardingPath")
    def reset_forwarding_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForwardingPath", []))

    @jsii.member(jsii_name="resetIpv4Address")
    def reset_ipv4_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpv4Address", []))

    @builtins.property
    @jsii.member(jsii_name="domainNameInput")
    def domain_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainNameInput"))

    @builtins.property
    @jsii.member(jsii_name="forwardingPathInput")
    def forwarding_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "forwardingPathInput"))

    @builtins.property
    @jsii.member(jsii_name="ipv4AddressInput")
    def ipv4_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipv4AddressInput"))

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @domain_name.setter
    def domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__367073ca9e69f465dcb4e2091540f5d4445564e08a2a158004f2488add066e2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forwardingPath")
    def forwarding_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "forwardingPath"))

    @forwarding_path.setter
    def forwarding_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c2926127c0bb0d88a1b0dbe0fb099c093b94fbe2a20ff4c8e3f55bb6e3505c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forwardingPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipv4Address")
    def ipv4_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv4Address"))

    @ipv4_address.setter
    def ipv4_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cda5a5b03d5478a29f4e1268f8a1335eabaf2a83b8d73e358ef080b89ab9b17b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv4Address", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsManagedZoneForwardingConfigTargetNameServers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsManagedZoneForwardingConfigTargetNameServers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsManagedZoneForwardingConfigTargetNameServers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__991de7f82baf633b9a8109cf518adddfc74dd16603dd9cac4ecb2d9891a200e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsManagedZone.DnsManagedZonePeeringConfig",
    jsii_struct_bases=[],
    name_mapping={"target_network": "targetNetwork"},
)
class DnsManagedZonePeeringConfig:
    def __init__(
        self,
        *,
        target_network: typing.Union["DnsManagedZonePeeringConfigTargetNetwork", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param target_network: target_network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#target_network DnsManagedZone#target_network}
        '''
        if isinstance(target_network, dict):
            target_network = DnsManagedZonePeeringConfigTargetNetwork(**target_network)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09ae4f38a76cdf4b02f28bebd45b4eec52ce2fa5d7c5cb12b89f4725bcbd112b)
            check_type(argname="argument target_network", value=target_network, expected_type=type_hints["target_network"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target_network": target_network,
        }

    @builtins.property
    def target_network(self) -> "DnsManagedZonePeeringConfigTargetNetwork":
        '''target_network block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#target_network DnsManagedZone#target_network}
        '''
        result = self._values.get("target_network")
        assert result is not None, "Required property 'target_network' is missing"
        return typing.cast("DnsManagedZonePeeringConfigTargetNetwork", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsManagedZonePeeringConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DnsManagedZonePeeringConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsManagedZone.DnsManagedZonePeeringConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ce46561a60f8c1f27c7d7851f1868d53bf54c9783e9025d98ce4dd74c0f41f4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTargetNetwork")
    def put_target_network(self, *, network_url: builtins.str) -> None:
        '''
        :param network_url: The id or fully qualified URL of the VPC network to forward queries to. This should be formatted like 'projects/{project}/global/networks/{network}' or 'https://www.googleapis.com/compute/v1/projects/{project}/global/networks/{network}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#network_url DnsManagedZone#network_url}
        '''
        value = DnsManagedZonePeeringConfigTargetNetwork(network_url=network_url)

        return typing.cast(None, jsii.invoke(self, "putTargetNetwork", [value]))

    @builtins.property
    @jsii.member(jsii_name="targetNetwork")
    def target_network(
        self,
    ) -> "DnsManagedZonePeeringConfigTargetNetworkOutputReference":
        return typing.cast("DnsManagedZonePeeringConfigTargetNetworkOutputReference", jsii.get(self, "targetNetwork"))

    @builtins.property
    @jsii.member(jsii_name="targetNetworkInput")
    def target_network_input(
        self,
    ) -> typing.Optional["DnsManagedZonePeeringConfigTargetNetwork"]:
        return typing.cast(typing.Optional["DnsManagedZonePeeringConfigTargetNetwork"], jsii.get(self, "targetNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DnsManagedZonePeeringConfig]:
        return typing.cast(typing.Optional[DnsManagedZonePeeringConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DnsManagedZonePeeringConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61d89c23404231585a7464c039b92d201ff5af082898b14097aa9a1329463e18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsManagedZone.DnsManagedZonePeeringConfigTargetNetwork",
    jsii_struct_bases=[],
    name_mapping={"network_url": "networkUrl"},
)
class DnsManagedZonePeeringConfigTargetNetwork:
    def __init__(self, *, network_url: builtins.str) -> None:
        '''
        :param network_url: The id or fully qualified URL of the VPC network to forward queries to. This should be formatted like 'projects/{project}/global/networks/{network}' or 'https://www.googleapis.com/compute/v1/projects/{project}/global/networks/{network}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#network_url DnsManagedZone#network_url}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8665a2078d9e19e765c2921558c91c2069ff907d60e0d097d6627f821a2171c8)
            check_type(argname="argument network_url", value=network_url, expected_type=type_hints["network_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "network_url": network_url,
        }

    @builtins.property
    def network_url(self) -> builtins.str:
        '''The id or fully qualified URL of the VPC network to forward queries to.

        This should be formatted like 'projects/{project}/global/networks/{network}' or
        'https://www.googleapis.com/compute/v1/projects/{project}/global/networks/{network}'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#network_url DnsManagedZone#network_url}
        '''
        result = self._values.get("network_url")
        assert result is not None, "Required property 'network_url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsManagedZonePeeringConfigTargetNetwork(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DnsManagedZonePeeringConfigTargetNetworkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsManagedZone.DnsManagedZonePeeringConfigTargetNetworkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b769689b32ec0d69f02e3558162c507ba12c9d776fa1f0a5ff52fb8e61f329a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="networkUrlInput")
    def network_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="networkUrl")
    def network_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkUrl"))

    @network_url.setter
    def network_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21b8a234fcb2319fe6363d967b26e5ebd7258bb52796965709f4475561680083)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DnsManagedZonePeeringConfigTargetNetwork]:
        return typing.cast(typing.Optional[DnsManagedZonePeeringConfigTargetNetwork], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DnsManagedZonePeeringConfigTargetNetwork],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e91a6410f541696ebae773762670ce12d587894cddb8eba4c0af9e2a1e0aa7f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsManagedZone.DnsManagedZonePrivateVisibilityConfig",
    jsii_struct_bases=[],
    name_mapping={"gke_clusters": "gkeClusters", "networks": "networks"},
)
class DnsManagedZonePrivateVisibilityConfig:
    def __init__(
        self,
        *,
        gke_clusters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DnsManagedZonePrivateVisibilityConfigGkeClusters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        networks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DnsManagedZonePrivateVisibilityConfigNetworks", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param gke_clusters: gke_clusters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#gke_clusters DnsManagedZone#gke_clusters}
        :param networks: networks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#networks DnsManagedZone#networks}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0fba69ff2bdb5d816ce2d21c0dc6b5bb357c6e55ca28e43436797195838549e)
            check_type(argname="argument gke_clusters", value=gke_clusters, expected_type=type_hints["gke_clusters"])
            check_type(argname="argument networks", value=networks, expected_type=type_hints["networks"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if gke_clusters is not None:
            self._values["gke_clusters"] = gke_clusters
        if networks is not None:
            self._values["networks"] = networks

    @builtins.property
    def gke_clusters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DnsManagedZonePrivateVisibilityConfigGkeClusters"]]]:
        '''gke_clusters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#gke_clusters DnsManagedZone#gke_clusters}
        '''
        result = self._values.get("gke_clusters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DnsManagedZonePrivateVisibilityConfigGkeClusters"]]], result)

    @builtins.property
    def networks(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DnsManagedZonePrivateVisibilityConfigNetworks"]]]:
        '''networks block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#networks DnsManagedZone#networks}
        '''
        result = self._values.get("networks")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DnsManagedZonePrivateVisibilityConfigNetworks"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsManagedZonePrivateVisibilityConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsManagedZone.DnsManagedZonePrivateVisibilityConfigGkeClusters",
    jsii_struct_bases=[],
    name_mapping={"gke_cluster_name": "gkeClusterName"},
)
class DnsManagedZonePrivateVisibilityConfigGkeClusters:
    def __init__(self, *, gke_cluster_name: builtins.str) -> None:
        '''
        :param gke_cluster_name: The resource name of the cluster to bind this ManagedZone to. This should be specified in the format like 'projects/* /locations/* /clusters/*' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#gke_cluster_name DnsManagedZone#gke_cluster_name} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bef682efd048dfec5d04994f4030aef2c2bdac4a619429a8725642a58cf1725)
            check_type(argname="argument gke_cluster_name", value=gke_cluster_name, expected_type=type_hints["gke_cluster_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "gke_cluster_name": gke_cluster_name,
        }

    @builtins.property
    def gke_cluster_name(self) -> builtins.str:
        '''The resource name of the cluster to bind this ManagedZone to.

        This should be specified in the format like
        'projects/* /locations/* /clusters/*'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#gke_cluster_name DnsManagedZone#gke_cluster_name}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("gke_cluster_name")
        assert result is not None, "Required property 'gke_cluster_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsManagedZonePrivateVisibilityConfigGkeClusters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DnsManagedZonePrivateVisibilityConfigGkeClustersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsManagedZone.DnsManagedZonePrivateVisibilityConfigGkeClustersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__90abe1c10a33bc02fd625e96d56eeba0adabe0146a954483471ab37492e776f1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DnsManagedZonePrivateVisibilityConfigGkeClustersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70e32be64eb4bc28fbfc19197822e4ba62698429781506f0fd087aafb2de5102)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DnsManagedZonePrivateVisibilityConfigGkeClustersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7f2e0fddd1c9c7875e180e910421b106d0d9e878dc8d9fa082b1f92b9072c87)
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
            type_hints = typing.get_type_hints(_typecheckingstub__42660910dfd6b94b473949cd8518c621c0e23b9b5de44cfae16d7e32087d68fe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6dfbfaf555c13bccbc280eedd304af010d475c80143f459aa0f8b645d155e228)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsManagedZonePrivateVisibilityConfigGkeClusters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsManagedZonePrivateVisibilityConfigGkeClusters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsManagedZonePrivateVisibilityConfigGkeClusters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccfd29ab5e73c54600acccb5fb76f52a5aef1714355cb9a833d1d7cab0fd1727)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DnsManagedZonePrivateVisibilityConfigGkeClustersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsManagedZone.DnsManagedZonePrivateVisibilityConfigGkeClustersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0b73dfa5d6ce7b01f5a6a2efcabc74506fd76b89810e5e584fa00dadb75cb2e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="gkeClusterNameInput")
    def gke_cluster_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gkeClusterNameInput"))

    @builtins.property
    @jsii.member(jsii_name="gkeClusterName")
    def gke_cluster_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gkeClusterName"))

    @gke_cluster_name.setter
    def gke_cluster_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__639fb816d966e53c883ec24697986b7c95448f8209d6e0ccdc1b558faa378da9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gkeClusterName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsManagedZonePrivateVisibilityConfigGkeClusters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsManagedZonePrivateVisibilityConfigGkeClusters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsManagedZonePrivateVisibilityConfigGkeClusters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be72ab82b3f89109377ad703097942702f035746dec0d05d718d1c44d4368563)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsManagedZone.DnsManagedZonePrivateVisibilityConfigNetworks",
    jsii_struct_bases=[],
    name_mapping={"network_url": "networkUrl"},
)
class DnsManagedZonePrivateVisibilityConfigNetworks:
    def __init__(self, *, network_url: builtins.str) -> None:
        '''
        :param network_url: The id or fully qualified URL of the VPC network to bind to. This should be formatted like 'projects/{project}/global/networks/{network}' or 'https://www.googleapis.com/compute/v1/projects/{project}/global/networks/{network}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#network_url DnsManagedZone#network_url}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a9a120e344dbf07eb1d18c5c4dfbb4074d6a4089edf27f64c9afbe4d894a159)
            check_type(argname="argument network_url", value=network_url, expected_type=type_hints["network_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "network_url": network_url,
        }

    @builtins.property
    def network_url(self) -> builtins.str:
        '''The id or fully qualified URL of the VPC network to bind to. This should be formatted like 'projects/{project}/global/networks/{network}' or 'https://www.googleapis.com/compute/v1/projects/{project}/global/networks/{network}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#network_url DnsManagedZone#network_url}
        '''
        result = self._values.get("network_url")
        assert result is not None, "Required property 'network_url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsManagedZonePrivateVisibilityConfigNetworks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DnsManagedZonePrivateVisibilityConfigNetworksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsManagedZone.DnsManagedZonePrivateVisibilityConfigNetworksList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1e34086bc1e12c79b731955898662f3641f3c0e0de2b27c892c1ade8c4da3ab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DnsManagedZonePrivateVisibilityConfigNetworksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d95467639ffb51d03d71fe0fed464efcea90e811caae624e4f4f29b9b6cdefc1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DnsManagedZonePrivateVisibilityConfigNetworksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3ad04a0d138e59510e3f3e453efed38a0b5f8ddde2945a30d229ec2b34c242d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c6fec4eda87b2070f5d033aee2104b620d6e7d5574ce4eab3e79e4ae8d97106)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6fcacfc7457a6b5b9d1d5146cde7dba09ccc00da135c7962786cef986e220742)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsManagedZonePrivateVisibilityConfigNetworks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsManagedZonePrivateVisibilityConfigNetworks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsManagedZonePrivateVisibilityConfigNetworks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b225a91539349f8d520d33877ca42e805977dfc9a63411fa5c53f4622a30a2a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DnsManagedZonePrivateVisibilityConfigNetworksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsManagedZone.DnsManagedZonePrivateVisibilityConfigNetworksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2402c915b57e12113d71a511335e3b2c199528be49c9940f70f0b184b92739b6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="networkUrlInput")
    def network_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="networkUrl")
    def network_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkUrl"))

    @network_url.setter
    def network_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__370307af38940383cb3ddce96bbaf44ddadcb2c68bf9e438be7614f093491b47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsManagedZonePrivateVisibilityConfigNetworks]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsManagedZonePrivateVisibilityConfigNetworks]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsManagedZonePrivateVisibilityConfigNetworks]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__198e44ff2195e46b88dd5e7cda2ee8df517e01ded2058b5a2abbd70af3ad0be0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DnsManagedZonePrivateVisibilityConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsManagedZone.DnsManagedZonePrivateVisibilityConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f39850ed6f4f946063c283b5acf00a097fa89d5061ddad72d461d1bf65f4837)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGkeClusters")
    def put_gke_clusters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DnsManagedZonePrivateVisibilityConfigGkeClusters, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bf879b93c43ba2d8d89c4d04c64bcf9e556557aa09db4809ad1b5238cd7568d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGkeClusters", [value]))

    @jsii.member(jsii_name="putNetworks")
    def put_networks(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DnsManagedZonePrivateVisibilityConfigNetworks, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29302558352ebef2404fa4e0edc11ce42233f74d167f97bbfd09be5e01ec8664)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNetworks", [value]))

    @jsii.member(jsii_name="resetGkeClusters")
    def reset_gke_clusters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGkeClusters", []))

    @jsii.member(jsii_name="resetNetworks")
    def reset_networks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworks", []))

    @builtins.property
    @jsii.member(jsii_name="gkeClusters")
    def gke_clusters(self) -> DnsManagedZonePrivateVisibilityConfigGkeClustersList:
        return typing.cast(DnsManagedZonePrivateVisibilityConfigGkeClustersList, jsii.get(self, "gkeClusters"))

    @builtins.property
    @jsii.member(jsii_name="networks")
    def networks(self) -> DnsManagedZonePrivateVisibilityConfigNetworksList:
        return typing.cast(DnsManagedZonePrivateVisibilityConfigNetworksList, jsii.get(self, "networks"))

    @builtins.property
    @jsii.member(jsii_name="gkeClustersInput")
    def gke_clusters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsManagedZonePrivateVisibilityConfigGkeClusters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsManagedZonePrivateVisibilityConfigGkeClusters]]], jsii.get(self, "gkeClustersInput"))

    @builtins.property
    @jsii.member(jsii_name="networksInput")
    def networks_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsManagedZonePrivateVisibilityConfigNetworks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsManagedZonePrivateVisibilityConfigNetworks]]], jsii.get(self, "networksInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DnsManagedZonePrivateVisibilityConfig]:
        return typing.cast(typing.Optional[DnsManagedZonePrivateVisibilityConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DnsManagedZonePrivateVisibilityConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4a75c243e82e001252c365107f7168282918058f25fa21326244bc645beda9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsManagedZone.DnsManagedZoneTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DnsManagedZoneTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#create DnsManagedZone#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#delete DnsManagedZone#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#update DnsManagedZone#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abcbe8485d22ee9a4813510670107810d06d19da9c282d62d25e3435606f9896)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#create DnsManagedZone#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#delete DnsManagedZone#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_managed_zone#update DnsManagedZone#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsManagedZoneTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DnsManagedZoneTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsManagedZone.DnsManagedZoneTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__69f7e76177a9f14b7c84afd09e3972058e7ee2ff04ca49557d60868e4f6472fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ecf744b12104cb5108f58601149bb66ba34c47115282c934f85e3e57c36ebe8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ae1e3a389f775fab2ee40401dcd76fc6407c55e1e6fa1e070c1d443cc9fbb93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf8511e308201dfabbf89c43a35a0dec9767b8199f6cfcd0b00dbbac4163f817)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsManagedZoneTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsManagedZoneTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsManagedZoneTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f186a61233a70efdb2f61cd683c6c26ef12758df3e115a66d8d83eb91bd61c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DnsManagedZone",
    "DnsManagedZoneCloudLoggingConfig",
    "DnsManagedZoneCloudLoggingConfigOutputReference",
    "DnsManagedZoneConfig",
    "DnsManagedZoneDnssecConfig",
    "DnsManagedZoneDnssecConfigDefaultKeySpecs",
    "DnsManagedZoneDnssecConfigDefaultKeySpecsList",
    "DnsManagedZoneDnssecConfigDefaultKeySpecsOutputReference",
    "DnsManagedZoneDnssecConfigOutputReference",
    "DnsManagedZoneForwardingConfig",
    "DnsManagedZoneForwardingConfigOutputReference",
    "DnsManagedZoneForwardingConfigTargetNameServers",
    "DnsManagedZoneForwardingConfigTargetNameServersList",
    "DnsManagedZoneForwardingConfigTargetNameServersOutputReference",
    "DnsManagedZonePeeringConfig",
    "DnsManagedZonePeeringConfigOutputReference",
    "DnsManagedZonePeeringConfigTargetNetwork",
    "DnsManagedZonePeeringConfigTargetNetworkOutputReference",
    "DnsManagedZonePrivateVisibilityConfig",
    "DnsManagedZonePrivateVisibilityConfigGkeClusters",
    "DnsManagedZonePrivateVisibilityConfigGkeClustersList",
    "DnsManagedZonePrivateVisibilityConfigGkeClustersOutputReference",
    "DnsManagedZonePrivateVisibilityConfigNetworks",
    "DnsManagedZonePrivateVisibilityConfigNetworksList",
    "DnsManagedZonePrivateVisibilityConfigNetworksOutputReference",
    "DnsManagedZonePrivateVisibilityConfigOutputReference",
    "DnsManagedZoneTimeouts",
    "DnsManagedZoneTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__bae8bd4489e13bb044dac9480d57d0a1567a2f642bf22cd29d21db408c9e44ed(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    dns_name: builtins.str,
    name: builtins.str,
    cloud_logging_config: typing.Optional[typing.Union[DnsManagedZoneCloudLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    dnssec_config: typing.Optional[typing.Union[DnsManagedZoneDnssecConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    forwarding_config: typing.Optional[typing.Union[DnsManagedZoneForwardingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    peering_config: typing.Optional[typing.Union[DnsManagedZonePeeringConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    private_visibility_config: typing.Optional[typing.Union[DnsManagedZonePrivateVisibilityConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DnsManagedZoneTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    visibility: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__af35231bcee9ffac365c6cfb26e71abd6d216b71902146eb4c463731b8d79d8a(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd614a815802671911a4ae34842c47b9463e993029daa6bf0aca4c1c407c073d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe223154d0193dea1d55176e2cd9da26f98851a0d89b7df4d70a4a9b5200652c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b94b968690d09550990d10e8374a5f143eed97a42384d8b7b9a10096752a043e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d901b4f364c5a95f3da17635065a7c052545dc443a03d9f41a5f4e30079d0bae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ec2a1af2508dfe227ec3d61cbde24f9ffd6211ba2f857d8f970279d402cea07(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f8b488c57b4be85c21d5d3557eef0beee74006e6abe0dbd01057681bbce7371(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c93cf9eb638559bb180c03aa325e34eced1935cec49f8378a197fa2d350beb23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf7ddc6b35b9bb7163098db435d2d0efa76dd48d3f3744379ba777cc0ed39fd4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e60f1aa42226533e4eb5532cafb11507125f712eef5dab08ac5b8d00adc21b34(
    *,
    enable_logging: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a3511fa8209871327a0a7fd8d4c1dac7f4ffdd837b2e677ba81b086bacfedf9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__599a44fccde2d949440a21873c9daa258f89c2b9d9b6ba491d596c5d1ff4f834(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__747bcf9bd518ca66f2fd4e177a309283fee47238499cf305bbbdf07dc8d60822(
    value: typing.Optional[DnsManagedZoneCloudLoggingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d67f36e7f80918c4800027e645b6088d484f7d2919b39454c8b8c1d2230fa1f5(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dns_name: builtins.str,
    name: builtins.str,
    cloud_logging_config: typing.Optional[typing.Union[DnsManagedZoneCloudLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    dnssec_config: typing.Optional[typing.Union[DnsManagedZoneDnssecConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    forwarding_config: typing.Optional[typing.Union[DnsManagedZoneForwardingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    peering_config: typing.Optional[typing.Union[DnsManagedZonePeeringConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    private_visibility_config: typing.Optional[typing.Union[DnsManagedZonePrivateVisibilityConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DnsManagedZoneTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    visibility: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45926a3339633e062ca5a052aa6e397fca4ebd0ea84d7ccb8c07d8483bea7c5a(
    *,
    default_key_specs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DnsManagedZoneDnssecConfigDefaultKeySpecs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    kind: typing.Optional[builtins.str] = None,
    non_existence: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6bd0d4afe2836e3de53e859d3d9f664bf1a26f8aabb46c220f81741c8c9863c(
    *,
    algorithm: typing.Optional[builtins.str] = None,
    key_length: typing.Optional[jsii.Number] = None,
    key_type: typing.Optional[builtins.str] = None,
    kind: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf06550c0388dd93e3137d80ea178eeb126bef063d0964d4f1c477316919ca63(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47ef922b264caa06dce616395dd3ee294050278ad0000a30badb3d78a07759eb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5974926f20c2615d515f2013144457974c4ce7e264a027886202b134feda6d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7290fa3e69af9c628367b1afbd44e3c5b0c378a3a95256bc1a860ee4d5550bb9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed5aab66b2fa1f77497e229ee84fb98af719067df65f7548ed8b90cc7c90634f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c51bfcf059513eb3da5ee3e3cf99a9d8ed23a77a8ef0e4d1a88bdf3d0562748(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsManagedZoneDnssecConfigDefaultKeySpecs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9fe5653a535c7f74c0cc8d48ae650dc7a924005b28a7fc44a67e2cfadbeae28(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b97f78cda891231928f31cf621cc4effd1046a03bb1c542076458c4c8c2edc46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d2bdc3022194c768b561b851be789c54d22d7f168a62736c75af8f725e31be5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caaed901fa594bf801684d1625b994a9a1a443c31de1e1528bef8278c70a4195(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20134ecea3e51961ecaacf804d4b6fd3d144316a03489c12405892df19ebc754(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7230c564c815311d663fad547b40b8c41438a3d52c6c6910ce0480f9e44726a6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsManagedZoneDnssecConfigDefaultKeySpecs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c32657c0300ff5ea84b819ebd2bba523f52ba416df819bc525d25381345831e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6b8f7bb5551368f379c6a96222325bcd0de906da32ec526badf6714ebee6811(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DnsManagedZoneDnssecConfigDefaultKeySpecs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2d54201cc0d6c1ef29ae96fcb89ae471cc95a019d22ee6b15b4568d73c80e35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f4207e5f75eeac30dea9b5573643f6666297402f58627418c7bf5c4272667ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6db300620150f310a5e3c0c4e06005b903e579d16ed0f7fed3d707297b418e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab9e9afe733e593338f015722851d94a3273a10833eb59f35b4e197562b77df3(
    value: typing.Optional[DnsManagedZoneDnssecConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f124430e7ef0dcf69b273c0b0e708bb6ba2fa9ea55652d57fb2eea7605eaa78d(
    *,
    target_name_servers: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DnsManagedZoneForwardingConfigTargetNameServers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b54ff33e275c0e7d9497d2af8d39e1f646c8e149ea2081d18d79840ae79f3fbb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__515e11322e3f370c69744d9867ff8a5903d3ed214a3d9ca7a6e12012707e4815(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DnsManagedZoneForwardingConfigTargetNameServers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55894e2da55461ed78c5f9630152ccd3e5d148c92a595a921505f59a65bae209(
    value: typing.Optional[DnsManagedZoneForwardingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e84e52b2e964cfb854c1bb4217b98a5238ae6706e8b2e0a5f6d98785b821b94(
    *,
    domain_name: typing.Optional[builtins.str] = None,
    forwarding_path: typing.Optional[builtins.str] = None,
    ipv4_address: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc2a2271d3702faa2e2397767dd3f8fdd727d63d7414912e526b1a9ece8b1e73(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0515c95a72b45c4af8b375afbb6a20f3cef3d8aa05212b60412d0640aefe356b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91759fa6610c573694bc48ec170e89ab96807849431ed029a1af6973d50127ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__515fc1c7d55227fe3e8d783c9bf29022c4f889d1bd81e730f125cdcdaa9a7555(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3618ea26a6744044792607b8f3ed66cd81bcb48fd04639ddb63175498ae971a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b29202d95673896103ae46380412bc6ff6badfc36be9ffdcb079043f186d7118(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsManagedZoneForwardingConfigTargetNameServers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29623ad39025035f4d35935ed7872dc04dc97173baf580e9993aa131f3c9dced(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__367073ca9e69f465dcb4e2091540f5d4445564e08a2a158004f2488add066e2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c2926127c0bb0d88a1b0dbe0fb099c093b94fbe2a20ff4c8e3f55bb6e3505c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cda5a5b03d5478a29f4e1268f8a1335eabaf2a83b8d73e358ef080b89ab9b17b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__991de7f82baf633b9a8109cf518adddfc74dd16603dd9cac4ecb2d9891a200e4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsManagedZoneForwardingConfigTargetNameServers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09ae4f38a76cdf4b02f28bebd45b4eec52ce2fa5d7c5cb12b89f4725bcbd112b(
    *,
    target_network: typing.Union[DnsManagedZonePeeringConfigTargetNetwork, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ce46561a60f8c1f27c7d7851f1868d53bf54c9783e9025d98ce4dd74c0f41f4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61d89c23404231585a7464c039b92d201ff5af082898b14097aa9a1329463e18(
    value: typing.Optional[DnsManagedZonePeeringConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8665a2078d9e19e765c2921558c91c2069ff907d60e0d097d6627f821a2171c8(
    *,
    network_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b769689b32ec0d69f02e3558162c507ba12c9d776fa1f0a5ff52fb8e61f329a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21b8a234fcb2319fe6363d967b26e5ebd7258bb52796965709f4475561680083(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e91a6410f541696ebae773762670ce12d587894cddb8eba4c0af9e2a1e0aa7f5(
    value: typing.Optional[DnsManagedZonePeeringConfigTargetNetwork],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0fba69ff2bdb5d816ce2d21c0dc6b5bb357c6e55ca28e43436797195838549e(
    *,
    gke_clusters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DnsManagedZonePrivateVisibilityConfigGkeClusters, typing.Dict[builtins.str, typing.Any]]]]] = None,
    networks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DnsManagedZonePrivateVisibilityConfigNetworks, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bef682efd048dfec5d04994f4030aef2c2bdac4a619429a8725642a58cf1725(
    *,
    gke_cluster_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90abe1c10a33bc02fd625e96d56eeba0adabe0146a954483471ab37492e776f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70e32be64eb4bc28fbfc19197822e4ba62698429781506f0fd087aafb2de5102(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7f2e0fddd1c9c7875e180e910421b106d0d9e878dc8d9fa082b1f92b9072c87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42660910dfd6b94b473949cd8518c621c0e23b9b5de44cfae16d7e32087d68fe(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dfbfaf555c13bccbc280eedd304af010d475c80143f459aa0f8b645d155e228(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccfd29ab5e73c54600acccb5fb76f52a5aef1714355cb9a833d1d7cab0fd1727(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsManagedZonePrivateVisibilityConfigGkeClusters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0b73dfa5d6ce7b01f5a6a2efcabc74506fd76b89810e5e584fa00dadb75cb2e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__639fb816d966e53c883ec24697986b7c95448f8209d6e0ccdc1b558faa378da9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be72ab82b3f89109377ad703097942702f035746dec0d05d718d1c44d4368563(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsManagedZonePrivateVisibilityConfigGkeClusters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a9a120e344dbf07eb1d18c5c4dfbb4074d6a4089edf27f64c9afbe4d894a159(
    *,
    network_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1e34086bc1e12c79b731955898662f3641f3c0e0de2b27c892c1ade8c4da3ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d95467639ffb51d03d71fe0fed464efcea90e811caae624e4f4f29b9b6cdefc1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3ad04a0d138e59510e3f3e453efed38a0b5f8ddde2945a30d229ec2b34c242d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c6fec4eda87b2070f5d033aee2104b620d6e7d5574ce4eab3e79e4ae8d97106(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fcacfc7457a6b5b9d1d5146cde7dba09ccc00da135c7962786cef986e220742(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b225a91539349f8d520d33877ca42e805977dfc9a63411fa5c53f4622a30a2a7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsManagedZonePrivateVisibilityConfigNetworks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2402c915b57e12113d71a511335e3b2c199528be49c9940f70f0b184b92739b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__370307af38940383cb3ddce96bbaf44ddadcb2c68bf9e438be7614f093491b47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__198e44ff2195e46b88dd5e7cda2ee8df517e01ded2058b5a2abbd70af3ad0be0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsManagedZonePrivateVisibilityConfigNetworks]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f39850ed6f4f946063c283b5acf00a097fa89d5061ddad72d461d1bf65f4837(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bf879b93c43ba2d8d89c4d04c64bcf9e556557aa09db4809ad1b5238cd7568d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DnsManagedZonePrivateVisibilityConfigGkeClusters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29302558352ebef2404fa4e0edc11ce42233f74d167f97bbfd09be5e01ec8664(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DnsManagedZonePrivateVisibilityConfigNetworks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4a75c243e82e001252c365107f7168282918058f25fa21326244bc645beda9c(
    value: typing.Optional[DnsManagedZonePrivateVisibilityConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abcbe8485d22ee9a4813510670107810d06d19da9c282d62d25e3435606f9896(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69f7e76177a9f14b7c84afd09e3972058e7ee2ff04ca49557d60868e4f6472fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ecf744b12104cb5108f58601149bb66ba34c47115282c934f85e3e57c36ebe8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ae1e3a389f775fab2ee40401dcd76fc6407c55e1e6fa1e070c1d443cc9fbb93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf8511e308201dfabbf89c43a35a0dec9767b8199f6cfcd0b00dbbac4163f817(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f186a61233a70efdb2f61cd683c6c26ef12758df3e115a66d8d83eb91bd61c7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsManagedZoneTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
