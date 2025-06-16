r'''
# `google_dns_managed_zone`

Refer to the Terraform Registry for docs: [`google_dns_managed_zone`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone).
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


class GoogleDnsManagedZone(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDnsManagedZone.GoogleDnsManagedZone",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone google_dns_managed_zone}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        dns_name: builtins.str,
        name: builtins.str,
        cloud_logging_config: typing.Optional[typing.Union["GoogleDnsManagedZoneCloudLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        dnssec_config: typing.Optional[typing.Union["GoogleDnsManagedZoneDnssecConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        forwarding_config: typing.Optional[typing.Union["GoogleDnsManagedZoneForwardingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        peering_config: typing.Optional[typing.Union["GoogleDnsManagedZonePeeringConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        private_visibility_config: typing.Optional[typing.Union["GoogleDnsManagedZonePrivateVisibilityConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        reverse_lookup: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        service_directory_config: typing.Optional[typing.Union["GoogleDnsManagedZoneServiceDirectoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleDnsManagedZoneTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        visibility: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone google_dns_managed_zone} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param dns_name: The DNS name of this managed zone, for instance "example.com.". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#dns_name GoogleDnsManagedZone#dns_name}
        :param name: User assigned name for this resource. Must be unique within the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#name GoogleDnsManagedZone#name}
        :param cloud_logging_config: cloud_logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#cloud_logging_config GoogleDnsManagedZone#cloud_logging_config}
        :param description: A textual description field. Defaults to 'Managed by Terraform'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#description GoogleDnsManagedZone#description}
        :param dnssec_config: dnssec_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#dnssec_config GoogleDnsManagedZone#dnssec_config}
        :param force_destroy: Set this true to delete all records in the zone. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#force_destroy GoogleDnsManagedZone#force_destroy}
        :param forwarding_config: forwarding_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#forwarding_config GoogleDnsManagedZone#forwarding_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#id GoogleDnsManagedZone#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: A set of key/value label pairs to assign to this ManagedZone. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#labels GoogleDnsManagedZone#labels}
        :param peering_config: peering_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#peering_config GoogleDnsManagedZone#peering_config}
        :param private_visibility_config: private_visibility_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#private_visibility_config GoogleDnsManagedZone#private_visibility_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#project GoogleDnsManagedZone#project}.
        :param reverse_lookup: Specifies if this is a managed reverse lookup zone. If true, Cloud DNS will resolve reverse lookup queries using automatically configured records for VPC resources. This only applies to networks listed under 'private_visibility_config'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#reverse_lookup GoogleDnsManagedZone#reverse_lookup}
        :param service_directory_config: service_directory_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#service_directory_config GoogleDnsManagedZone#service_directory_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#timeouts GoogleDnsManagedZone#timeouts}
        :param visibility: The zone's visibility: public zones are exposed to the Internet, while private zones are visible only to Virtual Private Cloud resources. Default value: "public" Possible values: ["private", "public"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#visibility GoogleDnsManagedZone#visibility}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e849893a42b459947f8e4ba50c4772fff8eed75fe0ca02debfbce4d3384b5ba)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleDnsManagedZoneConfig(
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
            reverse_lookup=reverse_lookup,
            service_directory_config=service_directory_config,
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
        '''Generates CDKTF code for importing a GoogleDnsManagedZone resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleDnsManagedZone to import.
        :param import_from_id: The id of the existing GoogleDnsManagedZone that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleDnsManagedZone to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1ce2c54a75f6bfa27ca4219bb397741ef63ae12ba6e6032fb67145c5055d203)
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
        :param enable_logging: If set, enable query logging for this ManagedZone. False by default, making logging opt-in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#enable_logging GoogleDnsManagedZone#enable_logging}
        '''
        value = GoogleDnsManagedZoneCloudLoggingConfig(enable_logging=enable_logging)

        return typing.cast(None, jsii.invoke(self, "putCloudLoggingConfig", [value]))

    @jsii.member(jsii_name="putDnssecConfig")
    def put_dnssec_config(
        self,
        *,
        default_key_specs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDnsManagedZoneDnssecConfigDefaultKeySpecs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        kind: typing.Optional[builtins.str] = None,
        non_existence: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param default_key_specs: default_key_specs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#default_key_specs GoogleDnsManagedZone#default_key_specs}
        :param kind: Identifies what kind of resource this is. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#kind GoogleDnsManagedZone#kind}
        :param non_existence: Specifies the mechanism used to provide authenticated denial-of-existence responses. non_existence can only be updated when the state is 'off'. Possible values: ["nsec", "nsec3"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#non_existence GoogleDnsManagedZone#non_existence}
        :param state: Specifies whether DNSSEC is enabled, and what mode it is in Possible values: ["off", "on", "transfer"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#state GoogleDnsManagedZone#state}
        '''
        value = GoogleDnsManagedZoneDnssecConfig(
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
        target_name_servers: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDnsManagedZoneForwardingConfigTargetNameServers", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param target_name_servers: target_name_servers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#target_name_servers GoogleDnsManagedZone#target_name_servers}
        '''
        value = GoogleDnsManagedZoneForwardingConfig(
            target_name_servers=target_name_servers
        )

        return typing.cast(None, jsii.invoke(self, "putForwardingConfig", [value]))

    @jsii.member(jsii_name="putPeeringConfig")
    def put_peering_config(
        self,
        *,
        target_network: typing.Union["GoogleDnsManagedZonePeeringConfigTargetNetwork", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param target_network: target_network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#target_network GoogleDnsManagedZone#target_network}
        '''
        value = GoogleDnsManagedZonePeeringConfig(target_network=target_network)

        return typing.cast(None, jsii.invoke(self, "putPeeringConfig", [value]))

    @jsii.member(jsii_name="putPrivateVisibilityConfig")
    def put_private_visibility_config(
        self,
        *,
        gke_clusters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDnsManagedZonePrivateVisibilityConfigGkeClusters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        networks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDnsManagedZonePrivateVisibilityConfigNetworks", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param gke_clusters: gke_clusters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#gke_clusters GoogleDnsManagedZone#gke_clusters}
        :param networks: networks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#networks GoogleDnsManagedZone#networks}
        '''
        value = GoogleDnsManagedZonePrivateVisibilityConfig(
            gke_clusters=gke_clusters, networks=networks
        )

        return typing.cast(None, jsii.invoke(self, "putPrivateVisibilityConfig", [value]))

    @jsii.member(jsii_name="putServiceDirectoryConfig")
    def put_service_directory_config(
        self,
        *,
        namespace: typing.Union["GoogleDnsManagedZoneServiceDirectoryConfigNamespace", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param namespace: namespace block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#namespace GoogleDnsManagedZone#namespace}
        '''
        value = GoogleDnsManagedZoneServiceDirectoryConfig(namespace=namespace)

        return typing.cast(None, jsii.invoke(self, "putServiceDirectoryConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#create GoogleDnsManagedZone#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#delete GoogleDnsManagedZone#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#update GoogleDnsManagedZone#update}.
        '''
        value = GoogleDnsManagedZoneTimeouts(
            create=create, delete=delete, update=update
        )

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

    @jsii.member(jsii_name="resetReverseLookup")
    def reset_reverse_lookup(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReverseLookup", []))

    @jsii.member(jsii_name="resetServiceDirectoryConfig")
    def reset_service_directory_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceDirectoryConfig", []))

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
    def cloud_logging_config(
        self,
    ) -> "GoogleDnsManagedZoneCloudLoggingConfigOutputReference":
        return typing.cast("GoogleDnsManagedZoneCloudLoggingConfigOutputReference", jsii.get(self, "cloudLoggingConfig"))

    @builtins.property
    @jsii.member(jsii_name="creationTime")
    def creation_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationTime"))

    @builtins.property
    @jsii.member(jsii_name="dnssecConfig")
    def dnssec_config(self) -> "GoogleDnsManagedZoneDnssecConfigOutputReference":
        return typing.cast("GoogleDnsManagedZoneDnssecConfigOutputReference", jsii.get(self, "dnssecConfig"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="forwardingConfig")
    def forwarding_config(
        self,
    ) -> "GoogleDnsManagedZoneForwardingConfigOutputReference":
        return typing.cast("GoogleDnsManagedZoneForwardingConfigOutputReference", jsii.get(self, "forwardingConfig"))

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
    def peering_config(self) -> "GoogleDnsManagedZonePeeringConfigOutputReference":
        return typing.cast("GoogleDnsManagedZonePeeringConfigOutputReference", jsii.get(self, "peeringConfig"))

    @builtins.property
    @jsii.member(jsii_name="privateVisibilityConfig")
    def private_visibility_config(
        self,
    ) -> "GoogleDnsManagedZonePrivateVisibilityConfigOutputReference":
        return typing.cast("GoogleDnsManagedZonePrivateVisibilityConfigOutputReference", jsii.get(self, "privateVisibilityConfig"))

    @builtins.property
    @jsii.member(jsii_name="serviceDirectoryConfig")
    def service_directory_config(
        self,
    ) -> "GoogleDnsManagedZoneServiceDirectoryConfigOutputReference":
        return typing.cast("GoogleDnsManagedZoneServiceDirectoryConfigOutputReference", jsii.get(self, "serviceDirectoryConfig"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleDnsManagedZoneTimeoutsOutputReference":
        return typing.cast("GoogleDnsManagedZoneTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="cloudLoggingConfigInput")
    def cloud_logging_config_input(
        self,
    ) -> typing.Optional["GoogleDnsManagedZoneCloudLoggingConfig"]:
        return typing.cast(typing.Optional["GoogleDnsManagedZoneCloudLoggingConfig"], jsii.get(self, "cloudLoggingConfigInput"))

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
    def dnssec_config_input(
        self,
    ) -> typing.Optional["GoogleDnsManagedZoneDnssecConfig"]:
        return typing.cast(typing.Optional["GoogleDnsManagedZoneDnssecConfig"], jsii.get(self, "dnssecConfigInput"))

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
    ) -> typing.Optional["GoogleDnsManagedZoneForwardingConfig"]:
        return typing.cast(typing.Optional["GoogleDnsManagedZoneForwardingConfig"], jsii.get(self, "forwardingConfigInput"))

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
    def peering_config_input(
        self,
    ) -> typing.Optional["GoogleDnsManagedZonePeeringConfig"]:
        return typing.cast(typing.Optional["GoogleDnsManagedZonePeeringConfig"], jsii.get(self, "peeringConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="privateVisibilityConfigInput")
    def private_visibility_config_input(
        self,
    ) -> typing.Optional["GoogleDnsManagedZonePrivateVisibilityConfig"]:
        return typing.cast(typing.Optional["GoogleDnsManagedZonePrivateVisibilityConfig"], jsii.get(self, "privateVisibilityConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="reverseLookupInput")
    def reverse_lookup_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "reverseLookupInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceDirectoryConfigInput")
    def service_directory_config_input(
        self,
    ) -> typing.Optional["GoogleDnsManagedZoneServiceDirectoryConfig"]:
        return typing.cast(typing.Optional["GoogleDnsManagedZoneServiceDirectoryConfig"], jsii.get(self, "serviceDirectoryConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDnsManagedZoneTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDnsManagedZoneTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__ef94fed5516974f2270782dd74204bb105940f6ce62d33e8ede2a453e8e15eee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dnsName")
    def dns_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dnsName"))

    @dns_name.setter
    def dns_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83aed7fd932d02e5783b710ae2c4ca8888db256cd53309b518eda2049f1c9478)
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
            type_hints = typing.get_type_hints(_typecheckingstub__df4f61898944a1525fd2f7a4351cc238a5f3d5791cd8886c13d2d870019157ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceDestroy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__127695f8a14fd654a611c1621f19731ac861a19118752f6bf76945d00d9ac447)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a721384bdcbd4be229595edde1d5b6d0cc3776067a8027893782527be059f6e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4c047f08b2e5e811e9cd42e3f48a9716b89af1bc8d823c23ad3c01a26f103f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c2daacaf0bf9804e25011e00cec736b987994f7ee417bd78cbdcc754938f392)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reverseLookup")
    def reverse_lookup(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "reverseLookup"))

    @reverse_lookup.setter
    def reverse_lookup(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae6af8e49822af324ee6fb64dd050e942d81989cdbc3ef9c6c1a37b57306ac23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reverseLookup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="visibility")
    def visibility(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "visibility"))

    @visibility.setter
    def visibility(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f3749f19dabe2b8b96e695a441f79b22ccbfea11a5d6a9d8e1528461b6940db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "visibility", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDnsManagedZone.GoogleDnsManagedZoneCloudLoggingConfig",
    jsii_struct_bases=[],
    name_mapping={"enable_logging": "enableLogging"},
)
class GoogleDnsManagedZoneCloudLoggingConfig:
    def __init__(
        self,
        *,
        enable_logging: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enable_logging: If set, enable query logging for this ManagedZone. False by default, making logging opt-in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#enable_logging GoogleDnsManagedZone#enable_logging}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25ebc66a92ea715c15d0a3733f79c0dadd75440a0341b17b1ec6dc41db82b3ca)
            check_type(argname="argument enable_logging", value=enable_logging, expected_type=type_hints["enable_logging"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enable_logging": enable_logging,
        }

    @builtins.property
    def enable_logging(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''If set, enable query logging for this ManagedZone. False by default, making logging opt-in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#enable_logging GoogleDnsManagedZone#enable_logging}
        '''
        result = self._values.get("enable_logging")
        assert result is not None, "Required property 'enable_logging' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDnsManagedZoneCloudLoggingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDnsManagedZoneCloudLoggingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDnsManagedZone.GoogleDnsManagedZoneCloudLoggingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__436ce9675a607a19a4365383cc562b9dc0d88af6cf74e1fbb8be1cfa9dff9094)
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
            type_hints = typing.get_type_hints(_typecheckingstub__095c24c1ace1f1af0171f96a769e1f83d7d53f0ed7ca7e17bb11b5dbb04fc20d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableLogging", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleDnsManagedZoneCloudLoggingConfig]:
        return typing.cast(typing.Optional[GoogleDnsManagedZoneCloudLoggingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDnsManagedZoneCloudLoggingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__518c4580cf458638e4b77e378cbef498f520f92640892776306d6bd444b6ff1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDnsManagedZone.GoogleDnsManagedZoneConfig",
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
        "reverse_lookup": "reverseLookup",
        "service_directory_config": "serviceDirectoryConfig",
        "timeouts": "timeouts",
        "visibility": "visibility",
    },
)
class GoogleDnsManagedZoneConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        cloud_logging_config: typing.Optional[typing.Union[GoogleDnsManagedZoneCloudLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        dnssec_config: typing.Optional[typing.Union["GoogleDnsManagedZoneDnssecConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        forwarding_config: typing.Optional[typing.Union["GoogleDnsManagedZoneForwardingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        peering_config: typing.Optional[typing.Union["GoogleDnsManagedZonePeeringConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        private_visibility_config: typing.Optional[typing.Union["GoogleDnsManagedZonePrivateVisibilityConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        reverse_lookup: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        service_directory_config: typing.Optional[typing.Union["GoogleDnsManagedZoneServiceDirectoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleDnsManagedZoneTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param dns_name: The DNS name of this managed zone, for instance "example.com.". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#dns_name GoogleDnsManagedZone#dns_name}
        :param name: User assigned name for this resource. Must be unique within the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#name GoogleDnsManagedZone#name}
        :param cloud_logging_config: cloud_logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#cloud_logging_config GoogleDnsManagedZone#cloud_logging_config}
        :param description: A textual description field. Defaults to 'Managed by Terraform'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#description GoogleDnsManagedZone#description}
        :param dnssec_config: dnssec_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#dnssec_config GoogleDnsManagedZone#dnssec_config}
        :param force_destroy: Set this true to delete all records in the zone. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#force_destroy GoogleDnsManagedZone#force_destroy}
        :param forwarding_config: forwarding_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#forwarding_config GoogleDnsManagedZone#forwarding_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#id GoogleDnsManagedZone#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: A set of key/value label pairs to assign to this ManagedZone. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#labels GoogleDnsManagedZone#labels}
        :param peering_config: peering_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#peering_config GoogleDnsManagedZone#peering_config}
        :param private_visibility_config: private_visibility_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#private_visibility_config GoogleDnsManagedZone#private_visibility_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#project GoogleDnsManagedZone#project}.
        :param reverse_lookup: Specifies if this is a managed reverse lookup zone. If true, Cloud DNS will resolve reverse lookup queries using automatically configured records for VPC resources. This only applies to networks listed under 'private_visibility_config'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#reverse_lookup GoogleDnsManagedZone#reverse_lookup}
        :param service_directory_config: service_directory_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#service_directory_config GoogleDnsManagedZone#service_directory_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#timeouts GoogleDnsManagedZone#timeouts}
        :param visibility: The zone's visibility: public zones are exposed to the Internet, while private zones are visible only to Virtual Private Cloud resources. Default value: "public" Possible values: ["private", "public"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#visibility GoogleDnsManagedZone#visibility}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(cloud_logging_config, dict):
            cloud_logging_config = GoogleDnsManagedZoneCloudLoggingConfig(**cloud_logging_config)
        if isinstance(dnssec_config, dict):
            dnssec_config = GoogleDnsManagedZoneDnssecConfig(**dnssec_config)
        if isinstance(forwarding_config, dict):
            forwarding_config = GoogleDnsManagedZoneForwardingConfig(**forwarding_config)
        if isinstance(peering_config, dict):
            peering_config = GoogleDnsManagedZonePeeringConfig(**peering_config)
        if isinstance(private_visibility_config, dict):
            private_visibility_config = GoogleDnsManagedZonePrivateVisibilityConfig(**private_visibility_config)
        if isinstance(service_directory_config, dict):
            service_directory_config = GoogleDnsManagedZoneServiceDirectoryConfig(**service_directory_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleDnsManagedZoneTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32f399915ba8d780a6cd7066d120de314f6482224e0482b0e6c0a82cbe491099)
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
            check_type(argname="argument reverse_lookup", value=reverse_lookup, expected_type=type_hints["reverse_lookup"])
            check_type(argname="argument service_directory_config", value=service_directory_config, expected_type=type_hints["service_directory_config"])
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
        if reverse_lookup is not None:
            self._values["reverse_lookup"] = reverse_lookup
        if service_directory_config is not None:
            self._values["service_directory_config"] = service_directory_config
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#dns_name GoogleDnsManagedZone#dns_name}
        '''
        result = self._values.get("dns_name")
        assert result is not None, "Required property 'dns_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''User assigned name for this resource. Must be unique within the project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#name GoogleDnsManagedZone#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cloud_logging_config(
        self,
    ) -> typing.Optional[GoogleDnsManagedZoneCloudLoggingConfig]:
        '''cloud_logging_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#cloud_logging_config GoogleDnsManagedZone#cloud_logging_config}
        '''
        result = self._values.get("cloud_logging_config")
        return typing.cast(typing.Optional[GoogleDnsManagedZoneCloudLoggingConfig], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A textual description field. Defaults to 'Managed by Terraform'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#description GoogleDnsManagedZone#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dnssec_config(self) -> typing.Optional["GoogleDnsManagedZoneDnssecConfig"]:
        '''dnssec_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#dnssec_config GoogleDnsManagedZone#dnssec_config}
        '''
        result = self._values.get("dnssec_config")
        return typing.cast(typing.Optional["GoogleDnsManagedZoneDnssecConfig"], result)

    @builtins.property
    def force_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set this true to delete all records in the zone.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#force_destroy GoogleDnsManagedZone#force_destroy}
        '''
        result = self._values.get("force_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def forwarding_config(
        self,
    ) -> typing.Optional["GoogleDnsManagedZoneForwardingConfig"]:
        '''forwarding_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#forwarding_config GoogleDnsManagedZone#forwarding_config}
        '''
        result = self._values.get("forwarding_config")
        return typing.cast(typing.Optional["GoogleDnsManagedZoneForwardingConfig"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#id GoogleDnsManagedZone#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#labels GoogleDnsManagedZone#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def peering_config(self) -> typing.Optional["GoogleDnsManagedZonePeeringConfig"]:
        '''peering_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#peering_config GoogleDnsManagedZone#peering_config}
        '''
        result = self._values.get("peering_config")
        return typing.cast(typing.Optional["GoogleDnsManagedZonePeeringConfig"], result)

    @builtins.property
    def private_visibility_config(
        self,
    ) -> typing.Optional["GoogleDnsManagedZonePrivateVisibilityConfig"]:
        '''private_visibility_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#private_visibility_config GoogleDnsManagedZone#private_visibility_config}
        '''
        result = self._values.get("private_visibility_config")
        return typing.cast(typing.Optional["GoogleDnsManagedZonePrivateVisibilityConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#project GoogleDnsManagedZone#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reverse_lookup(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies if this is a managed reverse lookup zone.

        If true, Cloud DNS will resolve reverse
        lookup queries using automatically configured records for VPC resources. This only applies
        to networks listed under 'private_visibility_config'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#reverse_lookup GoogleDnsManagedZone#reverse_lookup}
        '''
        result = self._values.get("reverse_lookup")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def service_directory_config(
        self,
    ) -> typing.Optional["GoogleDnsManagedZoneServiceDirectoryConfig"]:
        '''service_directory_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#service_directory_config GoogleDnsManagedZone#service_directory_config}
        '''
        result = self._values.get("service_directory_config")
        return typing.cast(typing.Optional["GoogleDnsManagedZoneServiceDirectoryConfig"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleDnsManagedZoneTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#timeouts GoogleDnsManagedZone#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleDnsManagedZoneTimeouts"], result)

    @builtins.property
    def visibility(self) -> typing.Optional[builtins.str]:
        '''The zone's visibility: public zones are exposed to the Internet, while private zones are visible only to Virtual Private Cloud resources.

        Default value: "public" Possible values: ["private", "public"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#visibility GoogleDnsManagedZone#visibility}
        '''
        result = self._values.get("visibility")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDnsManagedZoneConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDnsManagedZone.GoogleDnsManagedZoneDnssecConfig",
    jsii_struct_bases=[],
    name_mapping={
        "default_key_specs": "defaultKeySpecs",
        "kind": "kind",
        "non_existence": "nonExistence",
        "state": "state",
    },
)
class GoogleDnsManagedZoneDnssecConfig:
    def __init__(
        self,
        *,
        default_key_specs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDnsManagedZoneDnssecConfigDefaultKeySpecs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        kind: typing.Optional[builtins.str] = None,
        non_existence: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param default_key_specs: default_key_specs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#default_key_specs GoogleDnsManagedZone#default_key_specs}
        :param kind: Identifies what kind of resource this is. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#kind GoogleDnsManagedZone#kind}
        :param non_existence: Specifies the mechanism used to provide authenticated denial-of-existence responses. non_existence can only be updated when the state is 'off'. Possible values: ["nsec", "nsec3"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#non_existence GoogleDnsManagedZone#non_existence}
        :param state: Specifies whether DNSSEC is enabled, and what mode it is in Possible values: ["off", "on", "transfer"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#state GoogleDnsManagedZone#state}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ce1b156062f1590a6d5ccf244e9a4f9a05c48a63c5dd2421e8be2d860310b1e)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDnsManagedZoneDnssecConfigDefaultKeySpecs"]]]:
        '''default_key_specs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#default_key_specs GoogleDnsManagedZone#default_key_specs}
        '''
        result = self._values.get("default_key_specs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDnsManagedZoneDnssecConfigDefaultKeySpecs"]]], result)

    @builtins.property
    def kind(self) -> typing.Optional[builtins.str]:
        '''Identifies what kind of resource this is.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#kind GoogleDnsManagedZone#kind}
        '''
        result = self._values.get("kind")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def non_existence(self) -> typing.Optional[builtins.str]:
        '''Specifies the mechanism used to provide authenticated denial-of-existence responses.

        non_existence can only be updated when the state is 'off'. Possible values: ["nsec", "nsec3"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#non_existence GoogleDnsManagedZone#non_existence}
        '''
        result = self._values.get("non_existence")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''Specifies whether DNSSEC is enabled, and what mode it is in Possible values: ["off", "on", "transfer"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#state GoogleDnsManagedZone#state}
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDnsManagedZoneDnssecConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDnsManagedZone.GoogleDnsManagedZoneDnssecConfigDefaultKeySpecs",
    jsii_struct_bases=[],
    name_mapping={
        "algorithm": "algorithm",
        "key_length": "keyLength",
        "key_type": "keyType",
        "kind": "kind",
    },
)
class GoogleDnsManagedZoneDnssecConfigDefaultKeySpecs:
    def __init__(
        self,
        *,
        algorithm: typing.Optional[builtins.str] = None,
        key_length: typing.Optional[jsii.Number] = None,
        key_type: typing.Optional[builtins.str] = None,
        kind: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param algorithm: String mnemonic specifying the DNSSEC algorithm of this key Possible values: ["ecdsap256sha256", "ecdsap384sha384", "rsasha1", "rsasha256", "rsasha512"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#algorithm GoogleDnsManagedZone#algorithm}
        :param key_length: Length of the keys in bits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#key_length GoogleDnsManagedZone#key_length}
        :param key_type: Specifies whether this is a key signing key (KSK) or a zone signing key (ZSK). Key signing keys have the Secure Entry Point flag set and, when active, will only be used to sign resource record sets of type DNSKEY. Zone signing keys do not have the Secure Entry Point flag set and will be used to sign all other types of resource record sets. Possible values: ["keySigning", "zoneSigning"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#key_type GoogleDnsManagedZone#key_type}
        :param kind: Identifies what kind of resource this is. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#kind GoogleDnsManagedZone#kind}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__340f22ac60983540ab48e30c17858b145bed260e01fb2e6dda6f1cc1da852b4f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#algorithm GoogleDnsManagedZone#algorithm}
        '''
        result = self._values.get("algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_length(self) -> typing.Optional[jsii.Number]:
        '''Length of the keys in bits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#key_length GoogleDnsManagedZone#key_length}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#key_type GoogleDnsManagedZone#key_type}
        '''
        result = self._values.get("key_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kind(self) -> typing.Optional[builtins.str]:
        '''Identifies what kind of resource this is.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#kind GoogleDnsManagedZone#kind}
        '''
        result = self._values.get("kind")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDnsManagedZoneDnssecConfigDefaultKeySpecs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDnsManagedZoneDnssecConfigDefaultKeySpecsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDnsManagedZone.GoogleDnsManagedZoneDnssecConfigDefaultKeySpecsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6add8f7242c2f39c23ccbcfc5e7de670962472c0eab42bec6be0645b1296c78b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDnsManagedZoneDnssecConfigDefaultKeySpecsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2b5efec9517a066d56ab2175769b93f8cd55d1de490d5bd831328196f7ea936)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDnsManagedZoneDnssecConfigDefaultKeySpecsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b59378c45039f102e3c4b0e171d48753446567fc714438cc168f29118aad1bf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b7cf2cf948d815fe1bff7021d04267b870e54b58d66513cf65112f1f7beac6a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0260af7120aeb95d1e2e1daf4989c72409ff8ea75f5493e1dd0884c58a5aca50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsManagedZoneDnssecConfigDefaultKeySpecs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsManagedZoneDnssecConfigDefaultKeySpecs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsManagedZoneDnssecConfigDefaultKeySpecs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c85457bcd38d373f7dec0ab6cabefd6183aa1a68b707f6068202aba72feae429)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDnsManagedZoneDnssecConfigDefaultKeySpecsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDnsManagedZone.GoogleDnsManagedZoneDnssecConfigDefaultKeySpecsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e6a0c8574ae0ae2e42d412482adb9bb5eb02039ff2b034aa6ff91ce59addbb1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a80429d1907b6674eb5b0ab66bd25b225497264440b30ffdb6113e56ada4138)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "algorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyLength")
    def key_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "keyLength"))

    @key_length.setter
    def key_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cea61e302e9b93dcf8ce28533b1d5a8b34f81ee7c52bce7f9cfc99f5133dc7dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyLength", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyType")
    def key_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyType"))

    @key_type.setter
    def key_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ff9db8b42de530110caebaaeaad3e6fb2b16a1510160d3148e0e06fed76289f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kind"))

    @kind.setter
    def kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d60cf03b37d31e2cbc543f83aa912d0ff0aac3d7f138d14ac0c68673ddf27fb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsManagedZoneDnssecConfigDefaultKeySpecs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsManagedZoneDnssecConfigDefaultKeySpecs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsManagedZoneDnssecConfigDefaultKeySpecs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dd2cfe71cd3920eec88cfc04f5eef6c39483cd7edbb35c3920e94dfd9d8c754)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDnsManagedZoneDnssecConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDnsManagedZone.GoogleDnsManagedZoneDnssecConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e1c191f3c23e97c6937b3828a6e7b23b9a7e8ecad9febcceb7542f7e8ab5b13)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDefaultKeySpecs")
    def put_default_key_specs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDnsManagedZoneDnssecConfigDefaultKeySpecs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c69dd32fce7977ff1b720edb5de43899f7595214cd8db06820ea29d2410e2e4f)
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
    def default_key_specs(self) -> GoogleDnsManagedZoneDnssecConfigDefaultKeySpecsList:
        return typing.cast(GoogleDnsManagedZoneDnssecConfigDefaultKeySpecsList, jsii.get(self, "defaultKeySpecs"))

    @builtins.property
    @jsii.member(jsii_name="defaultKeySpecsInput")
    def default_key_specs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsManagedZoneDnssecConfigDefaultKeySpecs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsManagedZoneDnssecConfigDefaultKeySpecs]]], jsii.get(self, "defaultKeySpecsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__21ea340d6fc47b2f55c4ff76fd1a381c75fb23f5c306c0c5c84f41aebab940e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nonExistence")
    def non_existence(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nonExistence"))

    @non_existence.setter
    def non_existence(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff3c2257f3d749f1431f932c9dadab0a3d5aa8b9ea61403372a61264e0c7fb8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nonExistence", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8072a43bf93a47eb01305b278cd28643402ac16eaa1c55739d75c440c51411e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleDnsManagedZoneDnssecConfig]:
        return typing.cast(typing.Optional[GoogleDnsManagedZoneDnssecConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDnsManagedZoneDnssecConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__527a4ced5ccabb12e73c952362f248bcc2e33600c864ee6b1bef278722d21cc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDnsManagedZone.GoogleDnsManagedZoneForwardingConfig",
    jsii_struct_bases=[],
    name_mapping={"target_name_servers": "targetNameServers"},
)
class GoogleDnsManagedZoneForwardingConfig:
    def __init__(
        self,
        *,
        target_name_servers: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDnsManagedZoneForwardingConfigTargetNameServers", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param target_name_servers: target_name_servers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#target_name_servers GoogleDnsManagedZone#target_name_servers}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c2a4752fdb677fbd12c6014ef1145070527b987d1c4ba05c74a131aac9961cf)
            check_type(argname="argument target_name_servers", value=target_name_servers, expected_type=type_hints["target_name_servers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target_name_servers": target_name_servers,
        }

    @builtins.property
    def target_name_servers(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDnsManagedZoneForwardingConfigTargetNameServers"]]:
        '''target_name_servers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#target_name_servers GoogleDnsManagedZone#target_name_servers}
        '''
        result = self._values.get("target_name_servers")
        assert result is not None, "Required property 'target_name_servers' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDnsManagedZoneForwardingConfigTargetNameServers"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDnsManagedZoneForwardingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDnsManagedZoneForwardingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDnsManagedZone.GoogleDnsManagedZoneForwardingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b1b90e2fec1ace3d9113da6ef8ab0e8c488dbb25419f80b43bf0e9e21aa5495)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTargetNameServers")
    def put_target_name_servers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDnsManagedZoneForwardingConfigTargetNameServers", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38a5a1bfe3f9ae89b147941ce53ad85649b1cde24226cc80a52ce35f1c150d6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTargetNameServers", [value]))

    @builtins.property
    @jsii.member(jsii_name="targetNameServers")
    def target_name_servers(
        self,
    ) -> "GoogleDnsManagedZoneForwardingConfigTargetNameServersList":
        return typing.cast("GoogleDnsManagedZoneForwardingConfigTargetNameServersList", jsii.get(self, "targetNameServers"))

    @builtins.property
    @jsii.member(jsii_name="targetNameServersInput")
    def target_name_servers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDnsManagedZoneForwardingConfigTargetNameServers"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDnsManagedZoneForwardingConfigTargetNameServers"]]], jsii.get(self, "targetNameServersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleDnsManagedZoneForwardingConfig]:
        return typing.cast(typing.Optional[GoogleDnsManagedZoneForwardingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDnsManagedZoneForwardingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8210404a41302a84352fa19f1951e030aeb6c887cb85bd28813ab1f31496d48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDnsManagedZone.GoogleDnsManagedZoneForwardingConfigTargetNameServers",
    jsii_struct_bases=[],
    name_mapping={
        "domain_name": "domainName",
        "forwarding_path": "forwardingPath",
        "ipv4_address": "ipv4Address",
    },
)
class GoogleDnsManagedZoneForwardingConfigTargetNameServers:
    def __init__(
        self,
        *,
        domain_name: typing.Optional[builtins.str] = None,
        forwarding_path: typing.Optional[builtins.str] = None,
        ipv4_address: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param domain_name: Fully qualified domain name for the forwarding target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#domain_name GoogleDnsManagedZone#domain_name}
        :param forwarding_path: Forwarding path for this TargetNameServer. If unset or 'default' Cloud DNS will make forwarding decision based on address ranges, i.e. RFC1918 addresses go to the VPC, Non-RFC1918 addresses go to the Internet. When set to 'private', Cloud DNS will always send queries through VPC for this target Possible values: ["default", "private"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#forwarding_path GoogleDnsManagedZone#forwarding_path}
        :param ipv4_address: IPv4 address of a target name server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#ipv4_address GoogleDnsManagedZone#ipv4_address}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d03e8eefa168147486a7a6b58000328f999965b5563db210a34136866dd448b9)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#domain_name GoogleDnsManagedZone#domain_name}
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def forwarding_path(self) -> typing.Optional[builtins.str]:
        '''Forwarding path for this TargetNameServer.

        If unset or 'default' Cloud DNS will make forwarding
        decision based on address ranges, i.e. RFC1918 addresses go to the VPC, Non-RFC1918 addresses go
        to the Internet. When set to 'private', Cloud DNS will always send queries through VPC for this target Possible values: ["default", "private"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#forwarding_path GoogleDnsManagedZone#forwarding_path}
        '''
        result = self._values.get("forwarding_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ipv4_address(self) -> typing.Optional[builtins.str]:
        '''IPv4 address of a target name server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#ipv4_address GoogleDnsManagedZone#ipv4_address}
        '''
        result = self._values.get("ipv4_address")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDnsManagedZoneForwardingConfigTargetNameServers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDnsManagedZoneForwardingConfigTargetNameServersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDnsManagedZone.GoogleDnsManagedZoneForwardingConfigTargetNameServersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0779bb29eee93bd45a5498032b7b28c6c900e867dbaac10262fcb48b6da85c65)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDnsManagedZoneForwardingConfigTargetNameServersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b74085e7374698920674468d7f9900bad1093ed7febfcfed576ffbe50b53f5b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDnsManagedZoneForwardingConfigTargetNameServersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__334264b8a75d0d4af3c363db5de942d543ca16abc915c00638e99eb1bbf68fe6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b89ba36de7525052d93e97627fb898acb921fdb6c6e30011b6b0a3dae92b873)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5eccef2e61b19531f03378e31d695c9b957a064ed32ee938ebdf7d6b63b05bc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsManagedZoneForwardingConfigTargetNameServers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsManagedZoneForwardingConfigTargetNameServers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsManagedZoneForwardingConfigTargetNameServers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b94339d586bea22927f42a2d33c88d32c0b617d3adc93bdaf271f8e27b178950)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDnsManagedZoneForwardingConfigTargetNameServersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDnsManagedZone.GoogleDnsManagedZoneForwardingConfigTargetNameServersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d3f96ce270c9024dc2162c31233facfd270a69b6beb55350b9f877ed5019ecf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__07134a576995bc6bb1fd04c2dd31e1e5fbbbaab7047224a9357bb506b8fc2739)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forwardingPath")
    def forwarding_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "forwardingPath"))

    @forwarding_path.setter
    def forwarding_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__210e81f2df674fcdd44fc41bc6d46ae009c92046e53cfcc8157d9dab2a5b6f84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forwardingPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipv4Address")
    def ipv4_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv4Address"))

    @ipv4_address.setter
    def ipv4_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aee54ee00895cb3e037f6bad85e66d9754e9cff8558ff7a4896d52e011bf6e60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv4Address", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsManagedZoneForwardingConfigTargetNameServers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsManagedZoneForwardingConfigTargetNameServers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsManagedZoneForwardingConfigTargetNameServers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__346aa0c5ba7cbba3b0f72abb4097a4958b92f84d0038ddb7eb7bc2b761d32032)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDnsManagedZone.GoogleDnsManagedZonePeeringConfig",
    jsii_struct_bases=[],
    name_mapping={"target_network": "targetNetwork"},
)
class GoogleDnsManagedZonePeeringConfig:
    def __init__(
        self,
        *,
        target_network: typing.Union["GoogleDnsManagedZonePeeringConfigTargetNetwork", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param target_network: target_network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#target_network GoogleDnsManagedZone#target_network}
        '''
        if isinstance(target_network, dict):
            target_network = GoogleDnsManagedZonePeeringConfigTargetNetwork(**target_network)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77a8edcada893d28f47c92fbba870915f51dcecfdd7f3ebd291aae07f6036623)
            check_type(argname="argument target_network", value=target_network, expected_type=type_hints["target_network"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target_network": target_network,
        }

    @builtins.property
    def target_network(self) -> "GoogleDnsManagedZonePeeringConfigTargetNetwork":
        '''target_network block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#target_network GoogleDnsManagedZone#target_network}
        '''
        result = self._values.get("target_network")
        assert result is not None, "Required property 'target_network' is missing"
        return typing.cast("GoogleDnsManagedZonePeeringConfigTargetNetwork", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDnsManagedZonePeeringConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDnsManagedZonePeeringConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDnsManagedZone.GoogleDnsManagedZonePeeringConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a442433964edef2bd18a107f0912395a12c4b9fe64ca2c7a37cd0a9b4fbd023a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTargetNetwork")
    def put_target_network(self, *, network_url: builtins.str) -> None:
        '''
        :param network_url: The id or fully qualified URL of the VPC network to forward queries to. This should be formatted like 'projects/{project}/global/networks/{network}' or 'https://www.googleapis.com/compute/v1/projects/{project}/global/networks/{network}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#network_url GoogleDnsManagedZone#network_url}
        '''
        value = GoogleDnsManagedZonePeeringConfigTargetNetwork(network_url=network_url)

        return typing.cast(None, jsii.invoke(self, "putTargetNetwork", [value]))

    @builtins.property
    @jsii.member(jsii_name="targetNetwork")
    def target_network(
        self,
    ) -> "GoogleDnsManagedZonePeeringConfigTargetNetworkOutputReference":
        return typing.cast("GoogleDnsManagedZonePeeringConfigTargetNetworkOutputReference", jsii.get(self, "targetNetwork"))

    @builtins.property
    @jsii.member(jsii_name="targetNetworkInput")
    def target_network_input(
        self,
    ) -> typing.Optional["GoogleDnsManagedZonePeeringConfigTargetNetwork"]:
        return typing.cast(typing.Optional["GoogleDnsManagedZonePeeringConfigTargetNetwork"], jsii.get(self, "targetNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleDnsManagedZonePeeringConfig]:
        return typing.cast(typing.Optional[GoogleDnsManagedZonePeeringConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDnsManagedZonePeeringConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7815ad7ba3b35d695f7122b6a6f3cf50aeb083f5f274a308b68c6c7b032aeee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDnsManagedZone.GoogleDnsManagedZonePeeringConfigTargetNetwork",
    jsii_struct_bases=[],
    name_mapping={"network_url": "networkUrl"},
)
class GoogleDnsManagedZonePeeringConfigTargetNetwork:
    def __init__(self, *, network_url: builtins.str) -> None:
        '''
        :param network_url: The id or fully qualified URL of the VPC network to forward queries to. This should be formatted like 'projects/{project}/global/networks/{network}' or 'https://www.googleapis.com/compute/v1/projects/{project}/global/networks/{network}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#network_url GoogleDnsManagedZone#network_url}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74af5806609044ffbc24bda5452373fd4c4aac26152f8a75a21c50f15b4879d2)
            check_type(argname="argument network_url", value=network_url, expected_type=type_hints["network_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "network_url": network_url,
        }

    @builtins.property
    def network_url(self) -> builtins.str:
        '''The id or fully qualified URL of the VPC network to forward queries to.

        This should be formatted like 'projects/{project}/global/networks/{network}' or
        'https://www.googleapis.com/compute/v1/projects/{project}/global/networks/{network}'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#network_url GoogleDnsManagedZone#network_url}
        '''
        result = self._values.get("network_url")
        assert result is not None, "Required property 'network_url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDnsManagedZonePeeringConfigTargetNetwork(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDnsManagedZonePeeringConfigTargetNetworkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDnsManagedZone.GoogleDnsManagedZonePeeringConfigTargetNetworkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ec2f4c56eb197b232e9710154c86b6510a4b392e6ca8f0f0be622fcc4d55be8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__80a80cf0a84e0c7a61a108c4f2130c85dc1509190ae98aa86fa5d8be58c61dd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDnsManagedZonePeeringConfigTargetNetwork]:
        return typing.cast(typing.Optional[GoogleDnsManagedZonePeeringConfigTargetNetwork], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDnsManagedZonePeeringConfigTargetNetwork],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae9dda24667551bdad2caf59f6890c450ef79f24f5d8a9ec3c12c7452e059641)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDnsManagedZone.GoogleDnsManagedZonePrivateVisibilityConfig",
    jsii_struct_bases=[],
    name_mapping={"gke_clusters": "gkeClusters", "networks": "networks"},
)
class GoogleDnsManagedZonePrivateVisibilityConfig:
    def __init__(
        self,
        *,
        gke_clusters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDnsManagedZonePrivateVisibilityConfigGkeClusters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        networks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDnsManagedZonePrivateVisibilityConfigNetworks", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param gke_clusters: gke_clusters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#gke_clusters GoogleDnsManagedZone#gke_clusters}
        :param networks: networks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#networks GoogleDnsManagedZone#networks}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a9a81d709cf11a5f0853e9c3f6f01769817fb70f91cf294468a3826fadac3be)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDnsManagedZonePrivateVisibilityConfigGkeClusters"]]]:
        '''gke_clusters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#gke_clusters GoogleDnsManagedZone#gke_clusters}
        '''
        result = self._values.get("gke_clusters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDnsManagedZonePrivateVisibilityConfigGkeClusters"]]], result)

    @builtins.property
    def networks(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDnsManagedZonePrivateVisibilityConfigNetworks"]]]:
        '''networks block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#networks GoogleDnsManagedZone#networks}
        '''
        result = self._values.get("networks")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDnsManagedZonePrivateVisibilityConfigNetworks"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDnsManagedZonePrivateVisibilityConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDnsManagedZone.GoogleDnsManagedZonePrivateVisibilityConfigGkeClusters",
    jsii_struct_bases=[],
    name_mapping={"gke_cluster_name": "gkeClusterName"},
)
class GoogleDnsManagedZonePrivateVisibilityConfigGkeClusters:
    def __init__(self, *, gke_cluster_name: builtins.str) -> None:
        '''
        :param gke_cluster_name: The resource name of the cluster to bind this ManagedZone to. This should be specified in the format like 'projects/* /locations/* /clusters/*' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#gke_cluster_name GoogleDnsManagedZone#gke_cluster_name} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba2cc4f65032054b0bf4cb4534a0aefdaced54884a89e76524c17264db59b378)
            check_type(argname="argument gke_cluster_name", value=gke_cluster_name, expected_type=type_hints["gke_cluster_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "gke_cluster_name": gke_cluster_name,
        }

    @builtins.property
    def gke_cluster_name(self) -> builtins.str:
        '''The resource name of the cluster to bind this ManagedZone to.

        This should be specified in the format like
        'projects/* /locations/* /clusters/*'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#gke_cluster_name GoogleDnsManagedZone#gke_cluster_name}

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
        return "GoogleDnsManagedZonePrivateVisibilityConfigGkeClusters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDnsManagedZonePrivateVisibilityConfigGkeClustersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDnsManagedZone.GoogleDnsManagedZonePrivateVisibilityConfigGkeClustersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__55f3c72937006afdba9080dc0d15c85759df9dcf20024fd5e9222ad8f74431ad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDnsManagedZonePrivateVisibilityConfigGkeClustersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab44d9cb012111d734254e437cd7503071ff01faac3ec1a67a17263e4494039f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDnsManagedZonePrivateVisibilityConfigGkeClustersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0fdc5f417aad56f927ec433076b359a5d84c75d4c275c15e8b4755b76b8cf66)
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
            type_hints = typing.get_type_hints(_typecheckingstub__852c4d1ba66d6362b6d5da4fc4d580aee044dd83600947d7b2ef70057d48fc83)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f5b1f2b943ea2248e4c32cd226fa2db5c389c75f1f93db543a0cc5aa581aaba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsManagedZonePrivateVisibilityConfigGkeClusters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsManagedZonePrivateVisibilityConfigGkeClusters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsManagedZonePrivateVisibilityConfigGkeClusters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9268b4e47bdde006d9a44f785b4cd4c47cad5a6bef0155ae13cf850482e3a80a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDnsManagedZonePrivateVisibilityConfigGkeClustersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDnsManagedZone.GoogleDnsManagedZonePrivateVisibilityConfigGkeClustersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e69336e8f7285885110650a7aaaaa976751e15da14f37d4412e05631c99b5d15)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc13eec62eb7640af0819b16481223ed3e0300085c622c0f893ec810cc301dac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gkeClusterName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsManagedZonePrivateVisibilityConfigGkeClusters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsManagedZonePrivateVisibilityConfigGkeClusters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsManagedZonePrivateVisibilityConfigGkeClusters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a392dddd8107dc69b5f7665cf138086ea5a9b505d20849d6ebf83bc0e7d70bca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDnsManagedZone.GoogleDnsManagedZonePrivateVisibilityConfigNetworks",
    jsii_struct_bases=[],
    name_mapping={"network_url": "networkUrl"},
)
class GoogleDnsManagedZonePrivateVisibilityConfigNetworks:
    def __init__(self, *, network_url: builtins.str) -> None:
        '''
        :param network_url: The id or fully qualified URL of the VPC network to bind to. This should be formatted like 'projects/{project}/global/networks/{network}' or 'https://www.googleapis.com/compute/v1/projects/{project}/global/networks/{network}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#network_url GoogleDnsManagedZone#network_url}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45fdee9bd870ef9cbd43610891411bf89bb2079557616488148a0f89d3723489)
            check_type(argname="argument network_url", value=network_url, expected_type=type_hints["network_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "network_url": network_url,
        }

    @builtins.property
    def network_url(self) -> builtins.str:
        '''The id or fully qualified URL of the VPC network to bind to. This should be formatted like 'projects/{project}/global/networks/{network}' or 'https://www.googleapis.com/compute/v1/projects/{project}/global/networks/{network}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#network_url GoogleDnsManagedZone#network_url}
        '''
        result = self._values.get("network_url")
        assert result is not None, "Required property 'network_url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDnsManagedZonePrivateVisibilityConfigNetworks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDnsManagedZonePrivateVisibilityConfigNetworksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDnsManagedZone.GoogleDnsManagedZonePrivateVisibilityConfigNetworksList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3c08a4b9ecafad7d3cc1e78d801de86d14482198138f4fe116459f75787af99)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDnsManagedZonePrivateVisibilityConfigNetworksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d7ba8f2bab23d259b4aa02c43c6d7860e7d95248459708520ec292a98f9b251)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDnsManagedZonePrivateVisibilityConfigNetworksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a15928f5876ac4e13184d7c2c04a0d6f5ba0de4f298a22275ca5658d07997a20)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f85991fee2a39ea883981323f6601e447d1385ac809802cf75504b8c3c30a016)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb68b1e7531280bc86d6b8f5d06aa39d206a5606fe98bce59a84c960595a85a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsManagedZonePrivateVisibilityConfigNetworks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsManagedZonePrivateVisibilityConfigNetworks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsManagedZonePrivateVisibilityConfigNetworks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8ef632c04af63ee1da73d644da98f1bfa25124218a4f7f974e9947f72331548)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDnsManagedZonePrivateVisibilityConfigNetworksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDnsManagedZone.GoogleDnsManagedZonePrivateVisibilityConfigNetworksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1fd6c5829d7e67de1b87264c9e3fd4e73d15e84826333f1548304cc367d12d14)
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
            type_hints = typing.get_type_hints(_typecheckingstub__02c58b52e390a77ae9a3d27232e10b65860d7a40c11194e5e7530868b23c7a53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsManagedZonePrivateVisibilityConfigNetworks]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsManagedZonePrivateVisibilityConfigNetworks]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsManagedZonePrivateVisibilityConfigNetworks]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c265e53e604f4d3fe16524e7ad9972243f48cbb5a65cf65e9053ff2c5c6157df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDnsManagedZonePrivateVisibilityConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDnsManagedZone.GoogleDnsManagedZonePrivateVisibilityConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca64982dfb6fa1279001b070aacfb01e2b7bc0840da8ba7eb87b110857049663)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGkeClusters")
    def put_gke_clusters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDnsManagedZonePrivateVisibilityConfigGkeClusters, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__824548de9b8f353debdc46e270af26678dbbe8feeb41b48ce9d4086a1e7d6a6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGkeClusters", [value]))

    @jsii.member(jsii_name="putNetworks")
    def put_networks(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDnsManagedZonePrivateVisibilityConfigNetworks, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b56bf8df254f2e94f0fb70dd930f90bf39a0f5111ad0dbbe1fefc7048a25a072)
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
    def gke_clusters(
        self,
    ) -> GoogleDnsManagedZonePrivateVisibilityConfigGkeClustersList:
        return typing.cast(GoogleDnsManagedZonePrivateVisibilityConfigGkeClustersList, jsii.get(self, "gkeClusters"))

    @builtins.property
    @jsii.member(jsii_name="networks")
    def networks(self) -> GoogleDnsManagedZonePrivateVisibilityConfigNetworksList:
        return typing.cast(GoogleDnsManagedZonePrivateVisibilityConfigNetworksList, jsii.get(self, "networks"))

    @builtins.property
    @jsii.member(jsii_name="gkeClustersInput")
    def gke_clusters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsManagedZonePrivateVisibilityConfigGkeClusters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsManagedZonePrivateVisibilityConfigGkeClusters]]], jsii.get(self, "gkeClustersInput"))

    @builtins.property
    @jsii.member(jsii_name="networksInput")
    def networks_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsManagedZonePrivateVisibilityConfigNetworks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsManagedZonePrivateVisibilityConfigNetworks]]], jsii.get(self, "networksInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDnsManagedZonePrivateVisibilityConfig]:
        return typing.cast(typing.Optional[GoogleDnsManagedZonePrivateVisibilityConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDnsManagedZonePrivateVisibilityConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fa658e7be2765b677b64bae46884b70f058d18d0a99cc7b053ee2467005f300)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDnsManagedZone.GoogleDnsManagedZoneServiceDirectoryConfig",
    jsii_struct_bases=[],
    name_mapping={"namespace": "namespace"},
)
class GoogleDnsManagedZoneServiceDirectoryConfig:
    def __init__(
        self,
        *,
        namespace: typing.Union["GoogleDnsManagedZoneServiceDirectoryConfigNamespace", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param namespace: namespace block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#namespace GoogleDnsManagedZone#namespace}
        '''
        if isinstance(namespace, dict):
            namespace = GoogleDnsManagedZoneServiceDirectoryConfigNamespace(**namespace)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09b73bdfd19bd1d37ba00e86681c202ea8dcd4a51161bfaf37d686d78f748131)
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "namespace": namespace,
        }

    @builtins.property
    def namespace(self) -> "GoogleDnsManagedZoneServiceDirectoryConfigNamespace":
        '''namespace block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#namespace GoogleDnsManagedZone#namespace}
        '''
        result = self._values.get("namespace")
        assert result is not None, "Required property 'namespace' is missing"
        return typing.cast("GoogleDnsManagedZoneServiceDirectoryConfigNamespace", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDnsManagedZoneServiceDirectoryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDnsManagedZone.GoogleDnsManagedZoneServiceDirectoryConfigNamespace",
    jsii_struct_bases=[],
    name_mapping={"namespace_url": "namespaceUrl"},
)
class GoogleDnsManagedZoneServiceDirectoryConfigNamespace:
    def __init__(self, *, namespace_url: builtins.str) -> None:
        '''
        :param namespace_url: The fully qualified or partial URL of the service directory namespace that should be associated with the zone. This should be formatted like 'https://servicedirectory.googleapis.com/v1/projects/{project}/locations/{location}/namespaces/{namespace_id}' or simply 'projects/{project}/locations/{location}/namespaces/{namespace_id}' Ignored for 'public' visibility zones. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#namespace_url GoogleDnsManagedZone#namespace_url}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff52773fe29370c03cf93bf2aec301fd04d704982a124336902745172da148dd)
            check_type(argname="argument namespace_url", value=namespace_url, expected_type=type_hints["namespace_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "namespace_url": namespace_url,
        }

    @builtins.property
    def namespace_url(self) -> builtins.str:
        '''The fully qualified or partial URL of the service directory namespace that should be associated with the zone.

        This should be formatted like
        'https://servicedirectory.googleapis.com/v1/projects/{project}/locations/{location}/namespaces/{namespace_id}'
        or simply 'projects/{project}/locations/{location}/namespaces/{namespace_id}'
        Ignored for 'public' visibility zones.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#namespace_url GoogleDnsManagedZone#namespace_url}
        '''
        result = self._values.get("namespace_url")
        assert result is not None, "Required property 'namespace_url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDnsManagedZoneServiceDirectoryConfigNamespace(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDnsManagedZoneServiceDirectoryConfigNamespaceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDnsManagedZone.GoogleDnsManagedZoneServiceDirectoryConfigNamespaceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a363c8e3ffeb940b7c31d4930f439fe36754da0b854375bb02d0cf289ef702d5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="namespaceUrlInput")
    def namespace_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceUrl")
    def namespace_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespaceUrl"))

    @namespace_url.setter
    def namespace_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee4230029b9263ed19a287c16834e43ffd1b3360b4c2dbc26a9e782d672cf374)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespaceUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDnsManagedZoneServiceDirectoryConfigNamespace]:
        return typing.cast(typing.Optional[GoogleDnsManagedZoneServiceDirectoryConfigNamespace], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDnsManagedZoneServiceDirectoryConfigNamespace],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a104134c456f48a9f4ad8d1c5b116a914d198d59214024a75ecf989d8da557c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDnsManagedZoneServiceDirectoryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDnsManagedZone.GoogleDnsManagedZoneServiceDirectoryConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__77bf7491974fa3b15da82cd5797712833b1513e0dda19349ec52ece94c794a26)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNamespace")
    def put_namespace(self, *, namespace_url: builtins.str) -> None:
        '''
        :param namespace_url: The fully qualified or partial URL of the service directory namespace that should be associated with the zone. This should be formatted like 'https://servicedirectory.googleapis.com/v1/projects/{project}/locations/{location}/namespaces/{namespace_id}' or simply 'projects/{project}/locations/{location}/namespaces/{namespace_id}' Ignored for 'public' visibility zones. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#namespace_url GoogleDnsManagedZone#namespace_url}
        '''
        value = GoogleDnsManagedZoneServiceDirectoryConfigNamespace(
            namespace_url=namespace_url
        )

        return typing.cast(None, jsii.invoke(self, "putNamespace", [value]))

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(
        self,
    ) -> GoogleDnsManagedZoneServiceDirectoryConfigNamespaceOutputReference:
        return typing.cast(GoogleDnsManagedZoneServiceDirectoryConfigNamespaceOutputReference, jsii.get(self, "namespace"))

    @builtins.property
    @jsii.member(jsii_name="namespaceInput")
    def namespace_input(
        self,
    ) -> typing.Optional[GoogleDnsManagedZoneServiceDirectoryConfigNamespace]:
        return typing.cast(typing.Optional[GoogleDnsManagedZoneServiceDirectoryConfigNamespace], jsii.get(self, "namespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDnsManagedZoneServiceDirectoryConfig]:
        return typing.cast(typing.Optional[GoogleDnsManagedZoneServiceDirectoryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDnsManagedZoneServiceDirectoryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb9b22934893e67b5bba8d268dcb28e622569b692878dbe3932f6d008b71d38d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDnsManagedZone.GoogleDnsManagedZoneTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleDnsManagedZoneTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#create GoogleDnsManagedZone#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#delete GoogleDnsManagedZone#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#update GoogleDnsManagedZone#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c77e6c19f53a75d982d3d1c60c67f233cd8f5a4f9283a036f47a9a60230de41)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#create GoogleDnsManagedZone#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#delete GoogleDnsManagedZone#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_managed_zone#update GoogleDnsManagedZone#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDnsManagedZoneTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDnsManagedZoneTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDnsManagedZone.GoogleDnsManagedZoneTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__672ed4fe327ad4c50b725640b1a1acdef29ee696f0dc827d9612bafce7d11dea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f830882cd132eb9fd6fcba7d3d2050d11343fb674a01efaf71dfab7c6b32ce0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9305eeb97fdd09ede19683992b5501d6d115748548791bae0f4d6fa4765fe581)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3b6b8795adfbe999be100b8311bd0ce5d12aca6e4d84fd9d88721e90ec6bbfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsManagedZoneTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsManagedZoneTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsManagedZoneTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71645e0ce3700c3e0f14c2aa6bcb7873a5addd7c936e0f51f38f9b860edf7ccb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleDnsManagedZone",
    "GoogleDnsManagedZoneCloudLoggingConfig",
    "GoogleDnsManagedZoneCloudLoggingConfigOutputReference",
    "GoogleDnsManagedZoneConfig",
    "GoogleDnsManagedZoneDnssecConfig",
    "GoogleDnsManagedZoneDnssecConfigDefaultKeySpecs",
    "GoogleDnsManagedZoneDnssecConfigDefaultKeySpecsList",
    "GoogleDnsManagedZoneDnssecConfigDefaultKeySpecsOutputReference",
    "GoogleDnsManagedZoneDnssecConfigOutputReference",
    "GoogleDnsManagedZoneForwardingConfig",
    "GoogleDnsManagedZoneForwardingConfigOutputReference",
    "GoogleDnsManagedZoneForwardingConfigTargetNameServers",
    "GoogleDnsManagedZoneForwardingConfigTargetNameServersList",
    "GoogleDnsManagedZoneForwardingConfigTargetNameServersOutputReference",
    "GoogleDnsManagedZonePeeringConfig",
    "GoogleDnsManagedZonePeeringConfigOutputReference",
    "GoogleDnsManagedZonePeeringConfigTargetNetwork",
    "GoogleDnsManagedZonePeeringConfigTargetNetworkOutputReference",
    "GoogleDnsManagedZonePrivateVisibilityConfig",
    "GoogleDnsManagedZonePrivateVisibilityConfigGkeClusters",
    "GoogleDnsManagedZonePrivateVisibilityConfigGkeClustersList",
    "GoogleDnsManagedZonePrivateVisibilityConfigGkeClustersOutputReference",
    "GoogleDnsManagedZonePrivateVisibilityConfigNetworks",
    "GoogleDnsManagedZonePrivateVisibilityConfigNetworksList",
    "GoogleDnsManagedZonePrivateVisibilityConfigNetworksOutputReference",
    "GoogleDnsManagedZonePrivateVisibilityConfigOutputReference",
    "GoogleDnsManagedZoneServiceDirectoryConfig",
    "GoogleDnsManagedZoneServiceDirectoryConfigNamespace",
    "GoogleDnsManagedZoneServiceDirectoryConfigNamespaceOutputReference",
    "GoogleDnsManagedZoneServiceDirectoryConfigOutputReference",
    "GoogleDnsManagedZoneTimeouts",
    "GoogleDnsManagedZoneTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__0e849893a42b459947f8e4ba50c4772fff8eed75fe0ca02debfbce4d3384b5ba(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    dns_name: builtins.str,
    name: builtins.str,
    cloud_logging_config: typing.Optional[typing.Union[GoogleDnsManagedZoneCloudLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    dnssec_config: typing.Optional[typing.Union[GoogleDnsManagedZoneDnssecConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    forwarding_config: typing.Optional[typing.Union[GoogleDnsManagedZoneForwardingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    peering_config: typing.Optional[typing.Union[GoogleDnsManagedZonePeeringConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    private_visibility_config: typing.Optional[typing.Union[GoogleDnsManagedZonePrivateVisibilityConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    reverse_lookup: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    service_directory_config: typing.Optional[typing.Union[GoogleDnsManagedZoneServiceDirectoryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleDnsManagedZoneTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__f1ce2c54a75f6bfa27ca4219bb397741ef63ae12ba6e6032fb67145c5055d203(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef94fed5516974f2270782dd74204bb105940f6ce62d33e8ede2a453e8e15eee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83aed7fd932d02e5783b710ae2c4ca8888db256cd53309b518eda2049f1c9478(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df4f61898944a1525fd2f7a4351cc238a5f3d5791cd8886c13d2d870019157ea(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__127695f8a14fd654a611c1621f19731ac861a19118752f6bf76945d00d9ac447(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a721384bdcbd4be229595edde1d5b6d0cc3776067a8027893782527be059f6e4(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4c047f08b2e5e811e9cd42e3f48a9716b89af1bc8d823c23ad3c01a26f103f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c2daacaf0bf9804e25011e00cec736b987994f7ee417bd78cbdcc754938f392(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae6af8e49822af324ee6fb64dd050e942d81989cdbc3ef9c6c1a37b57306ac23(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f3749f19dabe2b8b96e695a441f79b22ccbfea11a5d6a9d8e1528461b6940db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25ebc66a92ea715c15d0a3733f79c0dadd75440a0341b17b1ec6dc41db82b3ca(
    *,
    enable_logging: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__436ce9675a607a19a4365383cc562b9dc0d88af6cf74e1fbb8be1cfa9dff9094(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__095c24c1ace1f1af0171f96a769e1f83d7d53f0ed7ca7e17bb11b5dbb04fc20d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__518c4580cf458638e4b77e378cbef498f520f92640892776306d6bd444b6ff1c(
    value: typing.Optional[GoogleDnsManagedZoneCloudLoggingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32f399915ba8d780a6cd7066d120de314f6482224e0482b0e6c0a82cbe491099(
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
    cloud_logging_config: typing.Optional[typing.Union[GoogleDnsManagedZoneCloudLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    dnssec_config: typing.Optional[typing.Union[GoogleDnsManagedZoneDnssecConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    forwarding_config: typing.Optional[typing.Union[GoogleDnsManagedZoneForwardingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    peering_config: typing.Optional[typing.Union[GoogleDnsManagedZonePeeringConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    private_visibility_config: typing.Optional[typing.Union[GoogleDnsManagedZonePrivateVisibilityConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    reverse_lookup: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    service_directory_config: typing.Optional[typing.Union[GoogleDnsManagedZoneServiceDirectoryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleDnsManagedZoneTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    visibility: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ce1b156062f1590a6d5ccf244e9a4f9a05c48a63c5dd2421e8be2d860310b1e(
    *,
    default_key_specs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDnsManagedZoneDnssecConfigDefaultKeySpecs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    kind: typing.Optional[builtins.str] = None,
    non_existence: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__340f22ac60983540ab48e30c17858b145bed260e01fb2e6dda6f1cc1da852b4f(
    *,
    algorithm: typing.Optional[builtins.str] = None,
    key_length: typing.Optional[jsii.Number] = None,
    key_type: typing.Optional[builtins.str] = None,
    kind: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6add8f7242c2f39c23ccbcfc5e7de670962472c0eab42bec6be0645b1296c78b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2b5efec9517a066d56ab2175769b93f8cd55d1de490d5bd831328196f7ea936(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b59378c45039f102e3c4b0e171d48753446567fc714438cc168f29118aad1bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b7cf2cf948d815fe1bff7021d04267b870e54b58d66513cf65112f1f7beac6a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0260af7120aeb95d1e2e1daf4989c72409ff8ea75f5493e1dd0884c58a5aca50(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c85457bcd38d373f7dec0ab6cabefd6183aa1a68b707f6068202aba72feae429(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsManagedZoneDnssecConfigDefaultKeySpecs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e6a0c8574ae0ae2e42d412482adb9bb5eb02039ff2b034aa6ff91ce59addbb1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a80429d1907b6674eb5b0ab66bd25b225497264440b30ffdb6113e56ada4138(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cea61e302e9b93dcf8ce28533b1d5a8b34f81ee7c52bce7f9cfc99f5133dc7dd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ff9db8b42de530110caebaaeaad3e6fb2b16a1510160d3148e0e06fed76289f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d60cf03b37d31e2cbc543f83aa912d0ff0aac3d7f138d14ac0c68673ddf27fb2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dd2cfe71cd3920eec88cfc04f5eef6c39483cd7edbb35c3920e94dfd9d8c754(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsManagedZoneDnssecConfigDefaultKeySpecs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e1c191f3c23e97c6937b3828a6e7b23b9a7e8ecad9febcceb7542f7e8ab5b13(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c69dd32fce7977ff1b720edb5de43899f7595214cd8db06820ea29d2410e2e4f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDnsManagedZoneDnssecConfigDefaultKeySpecs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21ea340d6fc47b2f55c4ff76fd1a381c75fb23f5c306c0c5c84f41aebab940e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff3c2257f3d749f1431f932c9dadab0a3d5aa8b9ea61403372a61264e0c7fb8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8072a43bf93a47eb01305b278cd28643402ac16eaa1c55739d75c440c51411e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__527a4ced5ccabb12e73c952362f248bcc2e33600c864ee6b1bef278722d21cc4(
    value: typing.Optional[GoogleDnsManagedZoneDnssecConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c2a4752fdb677fbd12c6014ef1145070527b987d1c4ba05c74a131aac9961cf(
    *,
    target_name_servers: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDnsManagedZoneForwardingConfigTargetNameServers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b1b90e2fec1ace3d9113da6ef8ab0e8c488dbb25419f80b43bf0e9e21aa5495(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38a5a1bfe3f9ae89b147941ce53ad85649b1cde24226cc80a52ce35f1c150d6a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDnsManagedZoneForwardingConfigTargetNameServers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8210404a41302a84352fa19f1951e030aeb6c887cb85bd28813ab1f31496d48(
    value: typing.Optional[GoogleDnsManagedZoneForwardingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d03e8eefa168147486a7a6b58000328f999965b5563db210a34136866dd448b9(
    *,
    domain_name: typing.Optional[builtins.str] = None,
    forwarding_path: typing.Optional[builtins.str] = None,
    ipv4_address: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0779bb29eee93bd45a5498032b7b28c6c900e867dbaac10262fcb48b6da85c65(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b74085e7374698920674468d7f9900bad1093ed7febfcfed576ffbe50b53f5b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__334264b8a75d0d4af3c363db5de942d543ca16abc915c00638e99eb1bbf68fe6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b89ba36de7525052d93e97627fb898acb921fdb6c6e30011b6b0a3dae92b873(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eccef2e61b19531f03378e31d695c9b957a064ed32ee938ebdf7d6b63b05bc8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b94339d586bea22927f42a2d33c88d32c0b617d3adc93bdaf271f8e27b178950(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsManagedZoneForwardingConfigTargetNameServers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d3f96ce270c9024dc2162c31233facfd270a69b6beb55350b9f877ed5019ecf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07134a576995bc6bb1fd04c2dd31e1e5fbbbaab7047224a9357bb506b8fc2739(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__210e81f2df674fcdd44fc41bc6d46ae009c92046e53cfcc8157d9dab2a5b6f84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aee54ee00895cb3e037f6bad85e66d9754e9cff8558ff7a4896d52e011bf6e60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__346aa0c5ba7cbba3b0f72abb4097a4958b92f84d0038ddb7eb7bc2b761d32032(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsManagedZoneForwardingConfigTargetNameServers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77a8edcada893d28f47c92fbba870915f51dcecfdd7f3ebd291aae07f6036623(
    *,
    target_network: typing.Union[GoogleDnsManagedZonePeeringConfigTargetNetwork, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a442433964edef2bd18a107f0912395a12c4b9fe64ca2c7a37cd0a9b4fbd023a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7815ad7ba3b35d695f7122b6a6f3cf50aeb083f5f274a308b68c6c7b032aeee(
    value: typing.Optional[GoogleDnsManagedZonePeeringConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74af5806609044ffbc24bda5452373fd4c4aac26152f8a75a21c50f15b4879d2(
    *,
    network_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ec2f4c56eb197b232e9710154c86b6510a4b392e6ca8f0f0be622fcc4d55be8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80a80cf0a84e0c7a61a108c4f2130c85dc1509190ae98aa86fa5d8be58c61dd8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae9dda24667551bdad2caf59f6890c450ef79f24f5d8a9ec3c12c7452e059641(
    value: typing.Optional[GoogleDnsManagedZonePeeringConfigTargetNetwork],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a9a81d709cf11a5f0853e9c3f6f01769817fb70f91cf294468a3826fadac3be(
    *,
    gke_clusters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDnsManagedZonePrivateVisibilityConfigGkeClusters, typing.Dict[builtins.str, typing.Any]]]]] = None,
    networks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDnsManagedZonePrivateVisibilityConfigNetworks, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba2cc4f65032054b0bf4cb4534a0aefdaced54884a89e76524c17264db59b378(
    *,
    gke_cluster_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55f3c72937006afdba9080dc0d15c85759df9dcf20024fd5e9222ad8f74431ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab44d9cb012111d734254e437cd7503071ff01faac3ec1a67a17263e4494039f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0fdc5f417aad56f927ec433076b359a5d84c75d4c275c15e8b4755b76b8cf66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__852c4d1ba66d6362b6d5da4fc4d580aee044dd83600947d7b2ef70057d48fc83(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f5b1f2b943ea2248e4c32cd226fa2db5c389c75f1f93db543a0cc5aa581aaba(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9268b4e47bdde006d9a44f785b4cd4c47cad5a6bef0155ae13cf850482e3a80a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsManagedZonePrivateVisibilityConfigGkeClusters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e69336e8f7285885110650a7aaaaa976751e15da14f37d4412e05631c99b5d15(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc13eec62eb7640af0819b16481223ed3e0300085c622c0f893ec810cc301dac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a392dddd8107dc69b5f7665cf138086ea5a9b505d20849d6ebf83bc0e7d70bca(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsManagedZonePrivateVisibilityConfigGkeClusters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45fdee9bd870ef9cbd43610891411bf89bb2079557616488148a0f89d3723489(
    *,
    network_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3c08a4b9ecafad7d3cc1e78d801de86d14482198138f4fe116459f75787af99(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d7ba8f2bab23d259b4aa02c43c6d7860e7d95248459708520ec292a98f9b251(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a15928f5876ac4e13184d7c2c04a0d6f5ba0de4f298a22275ca5658d07997a20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f85991fee2a39ea883981323f6601e447d1385ac809802cf75504b8c3c30a016(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb68b1e7531280bc86d6b8f5d06aa39d206a5606fe98bce59a84c960595a85a9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8ef632c04af63ee1da73d644da98f1bfa25124218a4f7f974e9947f72331548(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsManagedZonePrivateVisibilityConfigNetworks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fd6c5829d7e67de1b87264c9e3fd4e73d15e84826333f1548304cc367d12d14(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02c58b52e390a77ae9a3d27232e10b65860d7a40c11194e5e7530868b23c7a53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c265e53e604f4d3fe16524e7ad9972243f48cbb5a65cf65e9053ff2c5c6157df(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsManagedZonePrivateVisibilityConfigNetworks]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca64982dfb6fa1279001b070aacfb01e2b7bc0840da8ba7eb87b110857049663(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__824548de9b8f353debdc46e270af26678dbbe8feeb41b48ce9d4086a1e7d6a6f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDnsManagedZonePrivateVisibilityConfigGkeClusters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b56bf8df254f2e94f0fb70dd930f90bf39a0f5111ad0dbbe1fefc7048a25a072(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDnsManagedZonePrivateVisibilityConfigNetworks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fa658e7be2765b677b64bae46884b70f058d18d0a99cc7b053ee2467005f300(
    value: typing.Optional[GoogleDnsManagedZonePrivateVisibilityConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09b73bdfd19bd1d37ba00e86681c202ea8dcd4a51161bfaf37d686d78f748131(
    *,
    namespace: typing.Union[GoogleDnsManagedZoneServiceDirectoryConfigNamespace, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff52773fe29370c03cf93bf2aec301fd04d704982a124336902745172da148dd(
    *,
    namespace_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a363c8e3ffeb940b7c31d4930f439fe36754da0b854375bb02d0cf289ef702d5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee4230029b9263ed19a287c16834e43ffd1b3360b4c2dbc26a9e782d672cf374(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a104134c456f48a9f4ad8d1c5b116a914d198d59214024a75ecf989d8da557c6(
    value: typing.Optional[GoogleDnsManagedZoneServiceDirectoryConfigNamespace],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77bf7491974fa3b15da82cd5797712833b1513e0dda19349ec52ece94c794a26(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb9b22934893e67b5bba8d268dcb28e622569b692878dbe3932f6d008b71d38d(
    value: typing.Optional[GoogleDnsManagedZoneServiceDirectoryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c77e6c19f53a75d982d3d1c60c67f233cd8f5a4f9283a036f47a9a60230de41(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__672ed4fe327ad4c50b725640b1a1acdef29ee696f0dc827d9612bafce7d11dea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f830882cd132eb9fd6fcba7d3d2050d11343fb674a01efaf71dfab7c6b32ce0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9305eeb97fdd09ede19683992b5501d6d115748548791bae0f4d6fa4765fe581(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3b6b8795adfbe999be100b8311bd0ce5d12aca6e4d84fd9d88721e90ec6bbfb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71645e0ce3700c3e0f14c2aa6bcb7873a5addd7c936e0f51f38f9b860edf7ccb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsManagedZoneTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
