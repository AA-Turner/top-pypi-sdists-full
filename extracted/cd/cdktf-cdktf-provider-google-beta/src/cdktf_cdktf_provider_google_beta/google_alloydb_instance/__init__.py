r'''
# `google_alloydb_instance`

Refer to the Terraform Registry for docs: [`google_alloydb_instance`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance).
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


class GoogleAlloydbInstance(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbInstance.GoogleAlloydbInstance",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance google_alloydb_instance}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        cluster: builtins.str,
        instance_id: builtins.str,
        instance_type: builtins.str,
        activation_policy: typing.Optional[builtins.str] = None,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        availability_type: typing.Optional[builtins.str] = None,
        client_connection_config: typing.Optional[typing.Union["GoogleAlloydbInstanceClientConnectionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        database_flags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        display_name: typing.Optional[builtins.str] = None,
        gce_zone: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        machine_config: typing.Optional[typing.Union["GoogleAlloydbInstanceMachineConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        network_config: typing.Optional[typing.Union["GoogleAlloydbInstanceNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        observability_config: typing.Optional[typing.Union["GoogleAlloydbInstanceObservabilityConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        psc_instance_config: typing.Optional[typing.Union["GoogleAlloydbInstancePscInstanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        query_insights_config: typing.Optional[typing.Union["GoogleAlloydbInstanceQueryInsightsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        read_pool_config: typing.Optional[typing.Union["GoogleAlloydbInstanceReadPoolConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleAlloydbInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance google_alloydb_instance} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cluster: Identifies the alloydb cluster. Must be in the format 'projects/{project}/locations/{location}/clusters/{cluster_id}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#cluster GoogleAlloydbInstance#cluster}
        :param instance_id: The ID of the alloydb instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#instance_id GoogleAlloydbInstance#instance_id}
        :param instance_type: The type of the instance. If the instance type is READ_POOL, provide the associated PRIMARY/SECONDARY instance in the 'depends_on' meta-data attribute. If the instance type is SECONDARY, point to the cluster_type of the associated secondary cluster instead of mentioning SECONDARY. Example: {instance_type = google_alloydb_cluster.<secondary_cluster_name>.cluster_type} instead of {instance_type = SECONDARY} If the instance type is SECONDARY, the terraform delete instance operation does not delete the secondary instance but abandons it instead. Use deletion_policy = "FORCE" in the associated secondary cluster and delete the cluster forcefully to delete the secondary cluster as well its associated secondary instance. Users can undo the delete secondary instance action by importing the deleted secondary instance by calling terraform import. Possible values: ["PRIMARY", "READ_POOL", "SECONDARY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#instance_type GoogleAlloydbInstance#instance_type}
        :param activation_policy: 'Specifies whether an instance needs to spin up. Once the instance is active, the activation policy can be updated to the 'NEVER' to stop the instance. Likewise, the activation policy can be updated to 'ALWAYS' to start the instance. There are restrictions around when an instance can/cannot be activated (for example, a read pool instance should be stopped before stopping primary etc.). Please refer to the API documentation for more details. Possible values are: 'ACTIVATION_POLICY_UNSPECIFIED', 'ALWAYS', 'NEVER'.' Possible values: ["ACTIVATION_POLICY_UNSPECIFIED", "ALWAYS", "NEVER"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#activation_policy GoogleAlloydbInstance#activation_policy}
        :param annotations: Annotations to allow client tools to store small amount of arbitrary data. This is distinct from labels. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#annotations GoogleAlloydbInstance#annotations}
        :param availability_type: 'Availability type of an Instance. Defaults to REGIONAL for both primary and read instances. Note that primary and read instances can have different availability types. Primary instances can be either ZONAL or REGIONAL. Read Pool instances can also be either ZONAL or REGIONAL. Read pools of size 1 can only have zonal availability. Read pools with a node count of 2 or more can have regional availability (nodes are present in 2 or more zones in a region). Possible values are: 'AVAILABILITY_TYPE_UNSPECIFIED', 'ZONAL', 'REGIONAL'.' Possible values: ["AVAILABILITY_TYPE_UNSPECIFIED", "ZONAL", "REGIONAL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#availability_type GoogleAlloydbInstance#availability_type}
        :param client_connection_config: client_connection_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#client_connection_config GoogleAlloydbInstance#client_connection_config}
        :param database_flags: Database flags. Set at instance level. * They are copied from primary instance on read instance creation. * Read instances can set new or override existing flags that are relevant for reads, e.g. for enabling columnar cache on a read instance. Flags set on read instance may or may not be present on primary. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#database_flags GoogleAlloydbInstance#database_flags}
        :param display_name: User-settable and human-readable display name for the Instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#display_name GoogleAlloydbInstance#display_name}
        :param gce_zone: The Compute Engine zone that the instance should serve from, per https://cloud.google.com/compute/docs/regions-zones This can ONLY be specified for ZONAL instances. If present for a REGIONAL instance, an error will be thrown. If this is absent for a ZONAL instance, instance is created in a random zone with available capacity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#gce_zone GoogleAlloydbInstance#gce_zone}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#id GoogleAlloydbInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: User-defined labels for the alloydb instance. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#labels GoogleAlloydbInstance#labels}
        :param machine_config: machine_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#machine_config GoogleAlloydbInstance#machine_config}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#network_config GoogleAlloydbInstance#network_config}
        :param observability_config: observability_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#observability_config GoogleAlloydbInstance#observability_config}
        :param psc_instance_config: psc_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#psc_instance_config GoogleAlloydbInstance#psc_instance_config}
        :param query_insights_config: query_insights_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#query_insights_config GoogleAlloydbInstance#query_insights_config}
        :param read_pool_config: read_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#read_pool_config GoogleAlloydbInstance#read_pool_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#timeouts GoogleAlloydbInstance#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1a8431f1d79d47e80010c2b9e53867967d8a627e304fb135900b1ca4857761b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleAlloydbInstanceConfig(
            cluster=cluster,
            instance_id=instance_id,
            instance_type=instance_type,
            activation_policy=activation_policy,
            annotations=annotations,
            availability_type=availability_type,
            client_connection_config=client_connection_config,
            database_flags=database_flags,
            display_name=display_name,
            gce_zone=gce_zone,
            id=id,
            labels=labels,
            machine_config=machine_config,
            network_config=network_config,
            observability_config=observability_config,
            psc_instance_config=psc_instance_config,
            query_insights_config=query_insights_config,
            read_pool_config=read_pool_config,
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
        '''Generates CDKTF code for importing a GoogleAlloydbInstance resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleAlloydbInstance to import.
        :param import_from_id: The id of the existing GoogleAlloydbInstance that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleAlloydbInstance to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbc7d192f4f7254b9f89b99606c6177b6547f96720c1ca0a7b0dae57543e6474)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putClientConnectionConfig")
    def put_client_connection_config(
        self,
        *,
        require_connectors: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ssl_config: typing.Optional[typing.Union["GoogleAlloydbInstanceClientConnectionConfigSslConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param require_connectors: Configuration to enforce connectors only (ex: AuthProxy) connections to the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#require_connectors GoogleAlloydbInstance#require_connectors}
        :param ssl_config: ssl_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#ssl_config GoogleAlloydbInstance#ssl_config}
        '''
        value = GoogleAlloydbInstanceClientConnectionConfig(
            require_connectors=require_connectors, ssl_config=ssl_config
        )

        return typing.cast(None, jsii.invoke(self, "putClientConnectionConfig", [value]))

    @jsii.member(jsii_name="putMachineConfig")
    def put_machine_config(
        self,
        *,
        cpu_count: typing.Optional[jsii.Number] = None,
        machine_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cpu_count: The number of CPU's in the VM instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#cpu_count GoogleAlloydbInstance#cpu_count}
        :param machine_type: Machine type of the VM instance. E.g. "n2-highmem-4", "n2-highmem-8", "c4a-highmem-4-lssd". 'cpu_count' must match the number of vCPUs in the machine type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#machine_type GoogleAlloydbInstance#machine_type}
        '''
        value = GoogleAlloydbInstanceMachineConfig(
            cpu_count=cpu_count, machine_type=machine_type
        )

        return typing.cast(None, jsii.invoke(self, "putMachineConfig", [value]))

    @jsii.member(jsii_name="putNetworkConfig")
    def put_network_config(
        self,
        *,
        authorized_external_networks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAlloydbInstanceNetworkConfigAuthorizedExternalNetworks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        enable_outbound_public_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_public_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param authorized_external_networks: authorized_external_networks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#authorized_external_networks GoogleAlloydbInstance#authorized_external_networks}
        :param enable_outbound_public_ip: Enabling outbound public ip for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#enable_outbound_public_ip GoogleAlloydbInstance#enable_outbound_public_ip}
        :param enable_public_ip: Enabling public ip for the instance. If a user wishes to disable this, please also clear the list of the authorized external networks set on the same instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#enable_public_ip GoogleAlloydbInstance#enable_public_ip}
        '''
        value = GoogleAlloydbInstanceNetworkConfig(
            authorized_external_networks=authorized_external_networks,
            enable_outbound_public_ip=enable_outbound_public_ip,
            enable_public_ip=enable_public_ip,
        )

        return typing.cast(None, jsii.invoke(self, "putNetworkConfig", [value]))

    @jsii.member(jsii_name="putObservabilityConfig")
    def put_observability_config(
        self,
        *,
        assistive_experiences_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_query_string_length: typing.Optional[jsii.Number] = None,
        preserve_comments: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        query_plans_per_minute: typing.Optional[jsii.Number] = None,
        record_application_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        track_active_queries: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        track_wait_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        track_wait_event_types: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param assistive_experiences_enabled: Whether assistive experiences are enabled for this AlloyDB instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#assistive_experiences_enabled GoogleAlloydbInstance#assistive_experiences_enabled}
        :param enabled: Observability feature status for an instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#enabled GoogleAlloydbInstance#enabled}
        :param max_query_string_length: Query string length. The default value is 10240. Any integer between 1024 and 100000 is considered valid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#max_query_string_length GoogleAlloydbInstance#max_query_string_length}
        :param preserve_comments: Preserve comments in the query string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#preserve_comments GoogleAlloydbInstance#preserve_comments}
        :param query_plans_per_minute: Number of query execution plans captured by Insights per minute for all queries combined. The default value is 5. Any integer between 0 and 200 is considered valid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#query_plans_per_minute GoogleAlloydbInstance#query_plans_per_minute}
        :param record_application_tags: Record application tags for an instance. This flag is turned "on" by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#record_application_tags GoogleAlloydbInstance#record_application_tags}
        :param track_active_queries: Track actively running queries. If not set, default value is "off". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#track_active_queries GoogleAlloydbInstance#track_active_queries}
        :param track_wait_events: Record wait events during query execution for an instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#track_wait_events GoogleAlloydbInstance#track_wait_events}
        :param track_wait_event_types: Record wait event types during query execution for an instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#track_wait_event_types GoogleAlloydbInstance#track_wait_event_types}
        '''
        value = GoogleAlloydbInstanceObservabilityConfig(
            assistive_experiences_enabled=assistive_experiences_enabled,
            enabled=enabled,
            max_query_string_length=max_query_string_length,
            preserve_comments=preserve_comments,
            query_plans_per_minute=query_plans_per_minute,
            record_application_tags=record_application_tags,
            track_active_queries=track_active_queries,
            track_wait_events=track_wait_events,
            track_wait_event_types=track_wait_event_types,
        )

        return typing.cast(None, jsii.invoke(self, "putObservabilityConfig", [value]))

    @jsii.member(jsii_name="putPscInstanceConfig")
    def put_psc_instance_config(
        self,
        *,
        allowed_consumer_projects: typing.Optional[typing.Sequence[builtins.str]] = None,
        psc_auto_connections: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAlloydbInstancePscInstanceConfigPscAutoConnections", typing.Dict[builtins.str, typing.Any]]]]] = None,
        psc_interface_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAlloydbInstancePscInstanceConfigPscInterfaceConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param allowed_consumer_projects: List of consumer projects that are allowed to create PSC endpoints to service-attachments to this instance. These should be specified as project numbers only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#allowed_consumer_projects GoogleAlloydbInstance#allowed_consumer_projects}
        :param psc_auto_connections: psc_auto_connections block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#psc_auto_connections GoogleAlloydbInstance#psc_auto_connections}
        :param psc_interface_configs: psc_interface_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#psc_interface_configs GoogleAlloydbInstance#psc_interface_configs}
        '''
        value = GoogleAlloydbInstancePscInstanceConfig(
            allowed_consumer_projects=allowed_consumer_projects,
            psc_auto_connections=psc_auto_connections,
            psc_interface_configs=psc_interface_configs,
        )

        return typing.cast(None, jsii.invoke(self, "putPscInstanceConfig", [value]))

    @jsii.member(jsii_name="putQueryInsightsConfig")
    def put_query_insights_config(
        self,
        *,
        query_plans_per_minute: typing.Optional[jsii.Number] = None,
        query_string_length: typing.Optional[jsii.Number] = None,
        record_application_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        record_client_address: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param query_plans_per_minute: Number of query execution plans captured by Insights per minute for all queries combined. The default value is 5. Any integer between 0 and 20 is considered valid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#query_plans_per_minute GoogleAlloydbInstance#query_plans_per_minute}
        :param query_string_length: Query string length. The default value is 1024. Any integer between 256 and 4500 is considered valid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#query_string_length GoogleAlloydbInstance#query_string_length}
        :param record_application_tags: Record application tags for an instance. This flag is turned "on" by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#record_application_tags GoogleAlloydbInstance#record_application_tags}
        :param record_client_address: Record client address for an instance. Client address is PII information. This flag is turned "on" by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#record_client_address GoogleAlloydbInstance#record_client_address}
        '''
        value = GoogleAlloydbInstanceQueryInsightsConfig(
            query_plans_per_minute=query_plans_per_minute,
            query_string_length=query_string_length,
            record_application_tags=record_application_tags,
            record_client_address=record_client_address,
        )

        return typing.cast(None, jsii.invoke(self, "putQueryInsightsConfig", [value]))

    @jsii.member(jsii_name="putReadPoolConfig")
    def put_read_pool_config(
        self,
        *,
        node_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param node_count: Read capacity, i.e. number of nodes in a read pool instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#node_count GoogleAlloydbInstance#node_count}
        '''
        value = GoogleAlloydbInstanceReadPoolConfig(node_count=node_count)

        return typing.cast(None, jsii.invoke(self, "putReadPoolConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#create GoogleAlloydbInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#delete GoogleAlloydbInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#update GoogleAlloydbInstance#update}.
        '''
        value = GoogleAlloydbInstanceTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetActivationPolicy")
    def reset_activation_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActivationPolicy", []))

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetAvailabilityType")
    def reset_availability_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailabilityType", []))

    @jsii.member(jsii_name="resetClientConnectionConfig")
    def reset_client_connection_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientConnectionConfig", []))

    @jsii.member(jsii_name="resetDatabaseFlags")
    def reset_database_flags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabaseFlags", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetGceZone")
    def reset_gce_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGceZone", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMachineConfig")
    def reset_machine_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMachineConfig", []))

    @jsii.member(jsii_name="resetNetworkConfig")
    def reset_network_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkConfig", []))

    @jsii.member(jsii_name="resetObservabilityConfig")
    def reset_observability_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObservabilityConfig", []))

    @jsii.member(jsii_name="resetPscInstanceConfig")
    def reset_psc_instance_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPscInstanceConfig", []))

    @jsii.member(jsii_name="resetQueryInsightsConfig")
    def reset_query_insights_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryInsightsConfig", []))

    @jsii.member(jsii_name="resetReadPoolConfig")
    def reset_read_pool_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadPoolConfig", []))

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
    @jsii.member(jsii_name="clientConnectionConfig")
    def client_connection_config(
        self,
    ) -> "GoogleAlloydbInstanceClientConnectionConfigOutputReference":
        return typing.cast("GoogleAlloydbInstanceClientConnectionConfigOutputReference", jsii.get(self, "clientConnectionConfig"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="effectiveAnnotations")
    def effective_annotations(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveAnnotations"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @builtins.property
    @jsii.member(jsii_name="machineConfig")
    def machine_config(self) -> "GoogleAlloydbInstanceMachineConfigOutputReference":
        return typing.cast("GoogleAlloydbInstanceMachineConfigOutputReference", jsii.get(self, "machineConfig"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="networkConfig")
    def network_config(self) -> "GoogleAlloydbInstanceNetworkConfigOutputReference":
        return typing.cast("GoogleAlloydbInstanceNetworkConfigOutputReference", jsii.get(self, "networkConfig"))

    @builtins.property
    @jsii.member(jsii_name="observabilityConfig")
    def observability_config(
        self,
    ) -> "GoogleAlloydbInstanceObservabilityConfigOutputReference":
        return typing.cast("GoogleAlloydbInstanceObservabilityConfigOutputReference", jsii.get(self, "observabilityConfig"))

    @builtins.property
    @jsii.member(jsii_name="outboundPublicIpAddresses")
    def outbound_public_ip_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "outboundPublicIpAddresses"))

    @builtins.property
    @jsii.member(jsii_name="pscInstanceConfig")
    def psc_instance_config(
        self,
    ) -> "GoogleAlloydbInstancePscInstanceConfigOutputReference":
        return typing.cast("GoogleAlloydbInstancePscInstanceConfigOutputReference", jsii.get(self, "pscInstanceConfig"))

    @builtins.property
    @jsii.member(jsii_name="publicIpAddress")
    def public_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicIpAddress"))

    @builtins.property
    @jsii.member(jsii_name="queryInsightsConfig")
    def query_insights_config(
        self,
    ) -> "GoogleAlloydbInstanceQueryInsightsConfigOutputReference":
        return typing.cast("GoogleAlloydbInstanceQueryInsightsConfigOutputReference", jsii.get(self, "queryInsightsConfig"))

    @builtins.property
    @jsii.member(jsii_name="readPoolConfig")
    def read_pool_config(self) -> "GoogleAlloydbInstanceReadPoolConfigOutputReference":
        return typing.cast("GoogleAlloydbInstanceReadPoolConfigOutputReference", jsii.get(self, "readPoolConfig"))

    @builtins.property
    @jsii.member(jsii_name="reconciling")
    def reconciling(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "reconciling"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleAlloydbInstanceTimeoutsOutputReference":
        return typing.cast("GoogleAlloydbInstanceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="activationPolicyInput")
    def activation_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "activationPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="annotationsInput")
    def annotations_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "annotationsInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityTypeInput")
    def availability_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="clientConnectionConfigInput")
    def client_connection_config_input(
        self,
    ) -> typing.Optional["GoogleAlloydbInstanceClientConnectionConfig"]:
        return typing.cast(typing.Optional["GoogleAlloydbInstanceClientConnectionConfig"], jsii.get(self, "clientConnectionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterInput")
    def cluster_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseFlagsInput")
    def database_flags_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "databaseFlagsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="gceZoneInput")
    def gce_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gceZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceIdInput")
    def instance_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceTypeInput")
    def instance_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="machineConfigInput")
    def machine_config_input(
        self,
    ) -> typing.Optional["GoogleAlloydbInstanceMachineConfig"]:
        return typing.cast(typing.Optional["GoogleAlloydbInstanceMachineConfig"], jsii.get(self, "machineConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="networkConfigInput")
    def network_config_input(
        self,
    ) -> typing.Optional["GoogleAlloydbInstanceNetworkConfig"]:
        return typing.cast(typing.Optional["GoogleAlloydbInstanceNetworkConfig"], jsii.get(self, "networkConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="observabilityConfigInput")
    def observability_config_input(
        self,
    ) -> typing.Optional["GoogleAlloydbInstanceObservabilityConfig"]:
        return typing.cast(typing.Optional["GoogleAlloydbInstanceObservabilityConfig"], jsii.get(self, "observabilityConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="pscInstanceConfigInput")
    def psc_instance_config_input(
        self,
    ) -> typing.Optional["GoogleAlloydbInstancePscInstanceConfig"]:
        return typing.cast(typing.Optional["GoogleAlloydbInstancePscInstanceConfig"], jsii.get(self, "pscInstanceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInsightsConfigInput")
    def query_insights_config_input(
        self,
    ) -> typing.Optional["GoogleAlloydbInstanceQueryInsightsConfig"]:
        return typing.cast(typing.Optional["GoogleAlloydbInstanceQueryInsightsConfig"], jsii.get(self, "queryInsightsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="readPoolConfigInput")
    def read_pool_config_input(
        self,
    ) -> typing.Optional["GoogleAlloydbInstanceReadPoolConfig"]:
        return typing.cast(typing.Optional["GoogleAlloydbInstanceReadPoolConfig"], jsii.get(self, "readPoolConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleAlloydbInstanceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleAlloydbInstanceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="activationPolicy")
    def activation_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "activationPolicy"))

    @activation_policy.setter
    def activation_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5e4a33bcbbc2afcb5ab2ffc8af3690cabee5beec2a779df4545d010e077f669)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "activationPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdab180eaebb1c20b875be169c7e8648b426ed754372e9cfe26285577a8bca30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="availabilityType")
    def availability_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityType"))

    @availability_type.setter
    def availability_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb7c4a1b5134998988212626aca3e30c1b95606af98eb8bd91d10f568aeade0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cluster"))

    @cluster.setter
    def cluster(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f08ba00a79dcff56d4d664c133361d8fc254c102899ca8c4c5e29db0e40a3b27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cluster", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="databaseFlags")
    def database_flags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "databaseFlags"))

    @database_flags.setter
    def database_flags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c54f0db0cb92cb4c0e3d62914cbbf5f27f3c6637e9d0a5135b3a5edb9d137375)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseFlags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a957771901bb0839e17eaf8cbd6190be2d97cbd9920df8fdd8b0a945a234471)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gceZone")
    def gce_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gceZone"))

    @gce_zone.setter
    def gce_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55265f40907fc506324ea24fa52420cf92398df06940f3248e284c468cd03750)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gceZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__543413efe49247d5ffe58801c3d657c79df3dc29ab77558e44a2ab5f18c4efad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceId"))

    @instance_id.setter
    def instance_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bb6a49a6236f7a2bb4d3dab0a02fd604f607fff761efd5c96f39d7f6edec1f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1663d3fb5610fe563ef3ad9c7307d7fef618c9850a6c308c1e5b8097bcf0b808)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7c79e218ea78840812781d8548a1554508101185ffbb8484df72b459e45cb13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAlloydbInstance.GoogleAlloydbInstanceClientConnectionConfig",
    jsii_struct_bases=[],
    name_mapping={
        "require_connectors": "requireConnectors",
        "ssl_config": "sslConfig",
    },
)
class GoogleAlloydbInstanceClientConnectionConfig:
    def __init__(
        self,
        *,
        require_connectors: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ssl_config: typing.Optional[typing.Union["GoogleAlloydbInstanceClientConnectionConfigSslConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param require_connectors: Configuration to enforce connectors only (ex: AuthProxy) connections to the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#require_connectors GoogleAlloydbInstance#require_connectors}
        :param ssl_config: ssl_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#ssl_config GoogleAlloydbInstance#ssl_config}
        '''
        if isinstance(ssl_config, dict):
            ssl_config = GoogleAlloydbInstanceClientConnectionConfigSslConfig(**ssl_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74b291b2a8343ac1b9980a3799af3f81040b3a480b90457aba41631ea840d0a4)
            check_type(argname="argument require_connectors", value=require_connectors, expected_type=type_hints["require_connectors"])
            check_type(argname="argument ssl_config", value=ssl_config, expected_type=type_hints["ssl_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if require_connectors is not None:
            self._values["require_connectors"] = require_connectors
        if ssl_config is not None:
            self._values["ssl_config"] = ssl_config

    @builtins.property
    def require_connectors(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Configuration to enforce connectors only (ex: AuthProxy) connections to the database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#require_connectors GoogleAlloydbInstance#require_connectors}
        '''
        result = self._values.get("require_connectors")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ssl_config(
        self,
    ) -> typing.Optional["GoogleAlloydbInstanceClientConnectionConfigSslConfig"]:
        '''ssl_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#ssl_config GoogleAlloydbInstance#ssl_config}
        '''
        result = self._values.get("ssl_config")
        return typing.cast(typing.Optional["GoogleAlloydbInstanceClientConnectionConfigSslConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAlloydbInstanceClientConnectionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAlloydbInstanceClientConnectionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbInstance.GoogleAlloydbInstanceClientConnectionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__03679b9ea60512ebdf9a23acff73e3e0c517b47e6fb75bb641a72eba35d5568c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSslConfig")
    def put_ssl_config(self, *, ssl_mode: typing.Optional[builtins.str] = None) -> None:
        '''
        :param ssl_mode: SSL mode. Specifies client-server SSL/TLS connection behavior. Possible values: ["ENCRYPTED_ONLY", "ALLOW_UNENCRYPTED_AND_ENCRYPTED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#ssl_mode GoogleAlloydbInstance#ssl_mode}
        '''
        value = GoogleAlloydbInstanceClientConnectionConfigSslConfig(ssl_mode=ssl_mode)

        return typing.cast(None, jsii.invoke(self, "putSslConfig", [value]))

    @jsii.member(jsii_name="resetRequireConnectors")
    def reset_require_connectors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireConnectors", []))

    @jsii.member(jsii_name="resetSslConfig")
    def reset_ssl_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslConfig", []))

    @builtins.property
    @jsii.member(jsii_name="sslConfig")
    def ssl_config(
        self,
    ) -> "GoogleAlloydbInstanceClientConnectionConfigSslConfigOutputReference":
        return typing.cast("GoogleAlloydbInstanceClientConnectionConfigSslConfigOutputReference", jsii.get(self, "sslConfig"))

    @builtins.property
    @jsii.member(jsii_name="requireConnectorsInput")
    def require_connectors_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireConnectorsInput"))

    @builtins.property
    @jsii.member(jsii_name="sslConfigInput")
    def ssl_config_input(
        self,
    ) -> typing.Optional["GoogleAlloydbInstanceClientConnectionConfigSslConfig"]:
        return typing.cast(typing.Optional["GoogleAlloydbInstanceClientConnectionConfigSslConfig"], jsii.get(self, "sslConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="requireConnectors")
    def require_connectors(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireConnectors"))

    @require_connectors.setter
    def require_connectors(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e29b3ae62ba89a6d22ea69f925b18a76463521ddf7bfc9f589a0ec99f258fca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireConnectors", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAlloydbInstanceClientConnectionConfig]:
        return typing.cast(typing.Optional[GoogleAlloydbInstanceClientConnectionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAlloydbInstanceClientConnectionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5b090238c0a360562fba87c63f3e8a694eb92f8c4f6fbc5be25714ac32e14bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAlloydbInstance.GoogleAlloydbInstanceClientConnectionConfigSslConfig",
    jsii_struct_bases=[],
    name_mapping={"ssl_mode": "sslMode"},
)
class GoogleAlloydbInstanceClientConnectionConfigSslConfig:
    def __init__(self, *, ssl_mode: typing.Optional[builtins.str] = None) -> None:
        '''
        :param ssl_mode: SSL mode. Specifies client-server SSL/TLS connection behavior. Possible values: ["ENCRYPTED_ONLY", "ALLOW_UNENCRYPTED_AND_ENCRYPTED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#ssl_mode GoogleAlloydbInstance#ssl_mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd3d37f257ac035dc1104c98fb2a5a4c2f762965ececce88f0b8630dff8f326f)
            check_type(argname="argument ssl_mode", value=ssl_mode, expected_type=type_hints["ssl_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ssl_mode is not None:
            self._values["ssl_mode"] = ssl_mode

    @builtins.property
    def ssl_mode(self) -> typing.Optional[builtins.str]:
        '''SSL mode. Specifies client-server SSL/TLS connection behavior. Possible values: ["ENCRYPTED_ONLY", "ALLOW_UNENCRYPTED_AND_ENCRYPTED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#ssl_mode GoogleAlloydbInstance#ssl_mode}
        '''
        result = self._values.get("ssl_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAlloydbInstanceClientConnectionConfigSslConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAlloydbInstanceClientConnectionConfigSslConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbInstance.GoogleAlloydbInstanceClientConnectionConfigSslConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__11571136aebdcdc377611a4a5b0c6e91f0dde2584d9466827b1282631588a5a2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSslMode")
    def reset_ssl_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslMode", []))

    @builtins.property
    @jsii.member(jsii_name="sslModeInput")
    def ssl_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslModeInput"))

    @builtins.property
    @jsii.member(jsii_name="sslMode")
    def ssl_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslMode"))

    @ssl_mode.setter
    def ssl_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3775061a1765432c10f132ac1cc73a5e5c28921a4de64630e73effd5fa0a373)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAlloydbInstanceClientConnectionConfigSslConfig]:
        return typing.cast(typing.Optional[GoogleAlloydbInstanceClientConnectionConfigSslConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAlloydbInstanceClientConnectionConfigSslConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c33318f80056f4545f1eaa76a3889958bd0438c5a226def5b6bba674affa0d28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAlloydbInstance.GoogleAlloydbInstanceConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "cluster": "cluster",
        "instance_id": "instanceId",
        "instance_type": "instanceType",
        "activation_policy": "activationPolicy",
        "annotations": "annotations",
        "availability_type": "availabilityType",
        "client_connection_config": "clientConnectionConfig",
        "database_flags": "databaseFlags",
        "display_name": "displayName",
        "gce_zone": "gceZone",
        "id": "id",
        "labels": "labels",
        "machine_config": "machineConfig",
        "network_config": "networkConfig",
        "observability_config": "observabilityConfig",
        "psc_instance_config": "pscInstanceConfig",
        "query_insights_config": "queryInsightsConfig",
        "read_pool_config": "readPoolConfig",
        "timeouts": "timeouts",
    },
)
class GoogleAlloydbInstanceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        cluster: builtins.str,
        instance_id: builtins.str,
        instance_type: builtins.str,
        activation_policy: typing.Optional[builtins.str] = None,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        availability_type: typing.Optional[builtins.str] = None,
        client_connection_config: typing.Optional[typing.Union[GoogleAlloydbInstanceClientConnectionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        database_flags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        display_name: typing.Optional[builtins.str] = None,
        gce_zone: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        machine_config: typing.Optional[typing.Union["GoogleAlloydbInstanceMachineConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        network_config: typing.Optional[typing.Union["GoogleAlloydbInstanceNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        observability_config: typing.Optional[typing.Union["GoogleAlloydbInstanceObservabilityConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        psc_instance_config: typing.Optional[typing.Union["GoogleAlloydbInstancePscInstanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        query_insights_config: typing.Optional[typing.Union["GoogleAlloydbInstanceQueryInsightsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        read_pool_config: typing.Optional[typing.Union["GoogleAlloydbInstanceReadPoolConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleAlloydbInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cluster: Identifies the alloydb cluster. Must be in the format 'projects/{project}/locations/{location}/clusters/{cluster_id}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#cluster GoogleAlloydbInstance#cluster}
        :param instance_id: The ID of the alloydb instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#instance_id GoogleAlloydbInstance#instance_id}
        :param instance_type: The type of the instance. If the instance type is READ_POOL, provide the associated PRIMARY/SECONDARY instance in the 'depends_on' meta-data attribute. If the instance type is SECONDARY, point to the cluster_type of the associated secondary cluster instead of mentioning SECONDARY. Example: {instance_type = google_alloydb_cluster.<secondary_cluster_name>.cluster_type} instead of {instance_type = SECONDARY} If the instance type is SECONDARY, the terraform delete instance operation does not delete the secondary instance but abandons it instead. Use deletion_policy = "FORCE" in the associated secondary cluster and delete the cluster forcefully to delete the secondary cluster as well its associated secondary instance. Users can undo the delete secondary instance action by importing the deleted secondary instance by calling terraform import. Possible values: ["PRIMARY", "READ_POOL", "SECONDARY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#instance_type GoogleAlloydbInstance#instance_type}
        :param activation_policy: 'Specifies whether an instance needs to spin up. Once the instance is active, the activation policy can be updated to the 'NEVER' to stop the instance. Likewise, the activation policy can be updated to 'ALWAYS' to start the instance. There are restrictions around when an instance can/cannot be activated (for example, a read pool instance should be stopped before stopping primary etc.). Please refer to the API documentation for more details. Possible values are: 'ACTIVATION_POLICY_UNSPECIFIED', 'ALWAYS', 'NEVER'.' Possible values: ["ACTIVATION_POLICY_UNSPECIFIED", "ALWAYS", "NEVER"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#activation_policy GoogleAlloydbInstance#activation_policy}
        :param annotations: Annotations to allow client tools to store small amount of arbitrary data. This is distinct from labels. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#annotations GoogleAlloydbInstance#annotations}
        :param availability_type: 'Availability type of an Instance. Defaults to REGIONAL for both primary and read instances. Note that primary and read instances can have different availability types. Primary instances can be either ZONAL or REGIONAL. Read Pool instances can also be either ZONAL or REGIONAL. Read pools of size 1 can only have zonal availability. Read pools with a node count of 2 or more can have regional availability (nodes are present in 2 or more zones in a region). Possible values are: 'AVAILABILITY_TYPE_UNSPECIFIED', 'ZONAL', 'REGIONAL'.' Possible values: ["AVAILABILITY_TYPE_UNSPECIFIED", "ZONAL", "REGIONAL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#availability_type GoogleAlloydbInstance#availability_type}
        :param client_connection_config: client_connection_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#client_connection_config GoogleAlloydbInstance#client_connection_config}
        :param database_flags: Database flags. Set at instance level. * They are copied from primary instance on read instance creation. * Read instances can set new or override existing flags that are relevant for reads, e.g. for enabling columnar cache on a read instance. Flags set on read instance may or may not be present on primary. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#database_flags GoogleAlloydbInstance#database_flags}
        :param display_name: User-settable and human-readable display name for the Instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#display_name GoogleAlloydbInstance#display_name}
        :param gce_zone: The Compute Engine zone that the instance should serve from, per https://cloud.google.com/compute/docs/regions-zones This can ONLY be specified for ZONAL instances. If present for a REGIONAL instance, an error will be thrown. If this is absent for a ZONAL instance, instance is created in a random zone with available capacity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#gce_zone GoogleAlloydbInstance#gce_zone}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#id GoogleAlloydbInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: User-defined labels for the alloydb instance. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#labels GoogleAlloydbInstance#labels}
        :param machine_config: machine_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#machine_config GoogleAlloydbInstance#machine_config}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#network_config GoogleAlloydbInstance#network_config}
        :param observability_config: observability_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#observability_config GoogleAlloydbInstance#observability_config}
        :param psc_instance_config: psc_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#psc_instance_config GoogleAlloydbInstance#psc_instance_config}
        :param query_insights_config: query_insights_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#query_insights_config GoogleAlloydbInstance#query_insights_config}
        :param read_pool_config: read_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#read_pool_config GoogleAlloydbInstance#read_pool_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#timeouts GoogleAlloydbInstance#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(client_connection_config, dict):
            client_connection_config = GoogleAlloydbInstanceClientConnectionConfig(**client_connection_config)
        if isinstance(machine_config, dict):
            machine_config = GoogleAlloydbInstanceMachineConfig(**machine_config)
        if isinstance(network_config, dict):
            network_config = GoogleAlloydbInstanceNetworkConfig(**network_config)
        if isinstance(observability_config, dict):
            observability_config = GoogleAlloydbInstanceObservabilityConfig(**observability_config)
        if isinstance(psc_instance_config, dict):
            psc_instance_config = GoogleAlloydbInstancePscInstanceConfig(**psc_instance_config)
        if isinstance(query_insights_config, dict):
            query_insights_config = GoogleAlloydbInstanceQueryInsightsConfig(**query_insights_config)
        if isinstance(read_pool_config, dict):
            read_pool_config = GoogleAlloydbInstanceReadPoolConfig(**read_pool_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleAlloydbInstanceTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e23660ca52ff717fea25350d3a179cb982cdf51741ea2be6bbd11692a311bf2)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument activation_policy", value=activation_policy, expected_type=type_hints["activation_policy"])
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument availability_type", value=availability_type, expected_type=type_hints["availability_type"])
            check_type(argname="argument client_connection_config", value=client_connection_config, expected_type=type_hints["client_connection_config"])
            check_type(argname="argument database_flags", value=database_flags, expected_type=type_hints["database_flags"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument gce_zone", value=gce_zone, expected_type=type_hints["gce_zone"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument machine_config", value=machine_config, expected_type=type_hints["machine_config"])
            check_type(argname="argument network_config", value=network_config, expected_type=type_hints["network_config"])
            check_type(argname="argument observability_config", value=observability_config, expected_type=type_hints["observability_config"])
            check_type(argname="argument psc_instance_config", value=psc_instance_config, expected_type=type_hints["psc_instance_config"])
            check_type(argname="argument query_insights_config", value=query_insights_config, expected_type=type_hints["query_insights_config"])
            check_type(argname="argument read_pool_config", value=read_pool_config, expected_type=type_hints["read_pool_config"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster": cluster,
            "instance_id": instance_id,
            "instance_type": instance_type,
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
        if activation_policy is not None:
            self._values["activation_policy"] = activation_policy
        if annotations is not None:
            self._values["annotations"] = annotations
        if availability_type is not None:
            self._values["availability_type"] = availability_type
        if client_connection_config is not None:
            self._values["client_connection_config"] = client_connection_config
        if database_flags is not None:
            self._values["database_flags"] = database_flags
        if display_name is not None:
            self._values["display_name"] = display_name
        if gce_zone is not None:
            self._values["gce_zone"] = gce_zone
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if machine_config is not None:
            self._values["machine_config"] = machine_config
        if network_config is not None:
            self._values["network_config"] = network_config
        if observability_config is not None:
            self._values["observability_config"] = observability_config
        if psc_instance_config is not None:
            self._values["psc_instance_config"] = psc_instance_config
        if query_insights_config is not None:
            self._values["query_insights_config"] = query_insights_config
        if read_pool_config is not None:
            self._values["read_pool_config"] = read_pool_config
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
    def cluster(self) -> builtins.str:
        '''Identifies the alloydb cluster. Must be in the format 'projects/{project}/locations/{location}/clusters/{cluster_id}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#cluster GoogleAlloydbInstance#cluster}
        '''
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def instance_id(self) -> builtins.str:
        '''The ID of the alloydb instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#instance_id GoogleAlloydbInstance#instance_id}
        '''
        result = self._values.get("instance_id")
        assert result is not None, "Required property 'instance_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def instance_type(self) -> builtins.str:
        '''The type of the instance.

        If the instance type is READ_POOL, provide the associated PRIMARY/SECONDARY instance in the 'depends_on' meta-data attribute.
        If the instance type is SECONDARY, point to the cluster_type of the associated secondary cluster instead of mentioning SECONDARY.
        Example: {instance_type = google_alloydb_cluster.<secondary_cluster_name>.cluster_type} instead of {instance_type = SECONDARY}
        If the instance type is SECONDARY, the terraform delete instance operation does not delete the secondary instance but abandons it instead.
        Use deletion_policy = "FORCE" in the associated secondary cluster and delete the cluster forcefully to delete the secondary cluster as well its associated secondary instance.
        Users can undo the delete secondary instance action by importing the deleted secondary instance by calling terraform import. Possible values: ["PRIMARY", "READ_POOL", "SECONDARY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#instance_type GoogleAlloydbInstance#instance_type}
        '''
        result = self._values.get("instance_type")
        assert result is not None, "Required property 'instance_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def activation_policy(self) -> typing.Optional[builtins.str]:
        ''''Specifies whether an instance needs to spin up.

        Once the instance is
        active, the activation policy can be updated to the 'NEVER' to stop the
        instance. Likewise, the activation policy can be updated to 'ALWAYS' to
        start the instance.
        There are restrictions around when an instance can/cannot be activated (for
        example, a read pool instance should be stopped before stopping primary
        etc.). Please refer to the API documentation for more details.
        Possible values are: 'ACTIVATION_POLICY_UNSPECIFIED', 'ALWAYS', 'NEVER'.' Possible values: ["ACTIVATION_POLICY_UNSPECIFIED", "ALWAYS", "NEVER"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#activation_policy GoogleAlloydbInstance#activation_policy}
        '''
        result = self._values.get("activation_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Annotations to allow client tools to store small amount of arbitrary data. This is distinct from labels.

        **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration.
        Please refer to the field 'effective_annotations' for all of the annotations present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#annotations GoogleAlloydbInstance#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def availability_type(self) -> typing.Optional[builtins.str]:
        ''''Availability type of an Instance.

        Defaults to REGIONAL for both primary and read instances.
        Note that primary and read instances can have different availability types.
        Primary instances can be either ZONAL or REGIONAL. Read Pool instances can also be either ZONAL or REGIONAL.
        Read pools of size 1 can only have zonal availability. Read pools with a node count of 2 or more
        can have regional availability (nodes are present in 2 or more zones in a region).
        Possible values are: 'AVAILABILITY_TYPE_UNSPECIFIED', 'ZONAL', 'REGIONAL'.' Possible values: ["AVAILABILITY_TYPE_UNSPECIFIED", "ZONAL", "REGIONAL"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#availability_type GoogleAlloydbInstance#availability_type}
        '''
        result = self._values.get("availability_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_connection_config(
        self,
    ) -> typing.Optional[GoogleAlloydbInstanceClientConnectionConfig]:
        '''client_connection_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#client_connection_config GoogleAlloydbInstance#client_connection_config}
        '''
        result = self._values.get("client_connection_config")
        return typing.cast(typing.Optional[GoogleAlloydbInstanceClientConnectionConfig], result)

    @builtins.property
    def database_flags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Database flags.

        Set at instance level. * They are copied from primary instance on read instance creation. * Read instances can set new or override existing flags that are relevant for reads, e.g. for enabling columnar cache on a read instance. Flags set on read instance may or may not be present on primary.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#database_flags GoogleAlloydbInstance#database_flags}
        '''
        result = self._values.get("database_flags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''User-settable and human-readable display name for the Instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#display_name GoogleAlloydbInstance#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gce_zone(self) -> typing.Optional[builtins.str]:
        '''The Compute Engine zone that the instance should serve from, per https://cloud.google.com/compute/docs/regions-zones This can ONLY be specified for ZONAL instances. If present for a REGIONAL instance, an error will be thrown. If this is absent for a ZONAL instance, instance is created in a random zone with available capacity.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#gce_zone GoogleAlloydbInstance#gce_zone}
        '''
        result = self._values.get("gce_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#id GoogleAlloydbInstance#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''User-defined labels for the alloydb instance.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#labels GoogleAlloydbInstance#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def machine_config(self) -> typing.Optional["GoogleAlloydbInstanceMachineConfig"]:
        '''machine_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#machine_config GoogleAlloydbInstance#machine_config}
        '''
        result = self._values.get("machine_config")
        return typing.cast(typing.Optional["GoogleAlloydbInstanceMachineConfig"], result)

    @builtins.property
    def network_config(self) -> typing.Optional["GoogleAlloydbInstanceNetworkConfig"]:
        '''network_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#network_config GoogleAlloydbInstance#network_config}
        '''
        result = self._values.get("network_config")
        return typing.cast(typing.Optional["GoogleAlloydbInstanceNetworkConfig"], result)

    @builtins.property
    def observability_config(
        self,
    ) -> typing.Optional["GoogleAlloydbInstanceObservabilityConfig"]:
        '''observability_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#observability_config GoogleAlloydbInstance#observability_config}
        '''
        result = self._values.get("observability_config")
        return typing.cast(typing.Optional["GoogleAlloydbInstanceObservabilityConfig"], result)

    @builtins.property
    def psc_instance_config(
        self,
    ) -> typing.Optional["GoogleAlloydbInstancePscInstanceConfig"]:
        '''psc_instance_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#psc_instance_config GoogleAlloydbInstance#psc_instance_config}
        '''
        result = self._values.get("psc_instance_config")
        return typing.cast(typing.Optional["GoogleAlloydbInstancePscInstanceConfig"], result)

    @builtins.property
    def query_insights_config(
        self,
    ) -> typing.Optional["GoogleAlloydbInstanceQueryInsightsConfig"]:
        '''query_insights_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#query_insights_config GoogleAlloydbInstance#query_insights_config}
        '''
        result = self._values.get("query_insights_config")
        return typing.cast(typing.Optional["GoogleAlloydbInstanceQueryInsightsConfig"], result)

    @builtins.property
    def read_pool_config(
        self,
    ) -> typing.Optional["GoogleAlloydbInstanceReadPoolConfig"]:
        '''read_pool_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#read_pool_config GoogleAlloydbInstance#read_pool_config}
        '''
        result = self._values.get("read_pool_config")
        return typing.cast(typing.Optional["GoogleAlloydbInstanceReadPoolConfig"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleAlloydbInstanceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#timeouts GoogleAlloydbInstance#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleAlloydbInstanceTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAlloydbInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAlloydbInstance.GoogleAlloydbInstanceMachineConfig",
    jsii_struct_bases=[],
    name_mapping={"cpu_count": "cpuCount", "machine_type": "machineType"},
)
class GoogleAlloydbInstanceMachineConfig:
    def __init__(
        self,
        *,
        cpu_count: typing.Optional[jsii.Number] = None,
        machine_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cpu_count: The number of CPU's in the VM instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#cpu_count GoogleAlloydbInstance#cpu_count}
        :param machine_type: Machine type of the VM instance. E.g. "n2-highmem-4", "n2-highmem-8", "c4a-highmem-4-lssd". 'cpu_count' must match the number of vCPUs in the machine type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#machine_type GoogleAlloydbInstance#machine_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9537c0a0af16ef03bf3dacc7325bf7dda5b115b7544e166410a1aab5bfbc33b)
            check_type(argname="argument cpu_count", value=cpu_count, expected_type=type_hints["cpu_count"])
            check_type(argname="argument machine_type", value=machine_type, expected_type=type_hints["machine_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cpu_count is not None:
            self._values["cpu_count"] = cpu_count
        if machine_type is not None:
            self._values["machine_type"] = machine_type

    @builtins.property
    def cpu_count(self) -> typing.Optional[jsii.Number]:
        '''The number of CPU's in the VM instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#cpu_count GoogleAlloydbInstance#cpu_count}
        '''
        result = self._values.get("cpu_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def machine_type(self) -> typing.Optional[builtins.str]:
        '''Machine type of the VM instance. E.g. "n2-highmem-4", "n2-highmem-8", "c4a-highmem-4-lssd". 'cpu_count' must match the number of vCPUs in the machine type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#machine_type GoogleAlloydbInstance#machine_type}
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAlloydbInstanceMachineConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAlloydbInstanceMachineConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbInstance.GoogleAlloydbInstanceMachineConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc032ccfb3144912de416f2c55f4778e88853b731ec88d2babd8bf37267719b1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCpuCount")
    def reset_cpu_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuCount", []))

    @jsii.member(jsii_name="resetMachineType")
    def reset_machine_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMachineType", []))

    @builtins.property
    @jsii.member(jsii_name="cpuCountInput")
    def cpu_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuCountInput"))

    @builtins.property
    @jsii.member(jsii_name="machineTypeInput")
    def machine_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "machineTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuCount")
    def cpu_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuCount"))

    @cpu_count.setter
    def cpu_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fdc9724adf0c6e9c3140fb814e75331c37c1402f91a57054fcbcda1528c099a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54c030f74fc5a4160ad92cdc3f20c844530828332d443c2b8cff511044e704ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleAlloydbInstanceMachineConfig]:
        return typing.cast(typing.Optional[GoogleAlloydbInstanceMachineConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAlloydbInstanceMachineConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1772b8992f40c2963e7f532f3615c655c7ca05f04b859e843398b56e3a44c609)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAlloydbInstance.GoogleAlloydbInstanceNetworkConfig",
    jsii_struct_bases=[],
    name_mapping={
        "authorized_external_networks": "authorizedExternalNetworks",
        "enable_outbound_public_ip": "enableOutboundPublicIp",
        "enable_public_ip": "enablePublicIp",
    },
)
class GoogleAlloydbInstanceNetworkConfig:
    def __init__(
        self,
        *,
        authorized_external_networks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAlloydbInstanceNetworkConfigAuthorizedExternalNetworks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        enable_outbound_public_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_public_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param authorized_external_networks: authorized_external_networks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#authorized_external_networks GoogleAlloydbInstance#authorized_external_networks}
        :param enable_outbound_public_ip: Enabling outbound public ip for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#enable_outbound_public_ip GoogleAlloydbInstance#enable_outbound_public_ip}
        :param enable_public_ip: Enabling public ip for the instance. If a user wishes to disable this, please also clear the list of the authorized external networks set on the same instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#enable_public_ip GoogleAlloydbInstance#enable_public_ip}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95ba701575725b5bcb679fb88d22e218c26b7fddfdd7eb34473e7512d88c4fdd)
            check_type(argname="argument authorized_external_networks", value=authorized_external_networks, expected_type=type_hints["authorized_external_networks"])
            check_type(argname="argument enable_outbound_public_ip", value=enable_outbound_public_ip, expected_type=type_hints["enable_outbound_public_ip"])
            check_type(argname="argument enable_public_ip", value=enable_public_ip, expected_type=type_hints["enable_public_ip"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if authorized_external_networks is not None:
            self._values["authorized_external_networks"] = authorized_external_networks
        if enable_outbound_public_ip is not None:
            self._values["enable_outbound_public_ip"] = enable_outbound_public_ip
        if enable_public_ip is not None:
            self._values["enable_public_ip"] = enable_public_ip

    @builtins.property
    def authorized_external_networks(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAlloydbInstanceNetworkConfigAuthorizedExternalNetworks"]]]:
        '''authorized_external_networks block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#authorized_external_networks GoogleAlloydbInstance#authorized_external_networks}
        '''
        result = self._values.get("authorized_external_networks")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAlloydbInstanceNetworkConfigAuthorizedExternalNetworks"]]], result)

    @builtins.property
    def enable_outbound_public_ip(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enabling outbound public ip for the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#enable_outbound_public_ip GoogleAlloydbInstance#enable_outbound_public_ip}
        '''
        result = self._values.get("enable_outbound_public_ip")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_public_ip(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enabling public ip for the instance.

        If a user wishes to disable this,
        please also clear the list of the authorized external networks set on
        the same instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#enable_public_ip GoogleAlloydbInstance#enable_public_ip}
        '''
        result = self._values.get("enable_public_ip")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAlloydbInstanceNetworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAlloydbInstance.GoogleAlloydbInstanceNetworkConfigAuthorizedExternalNetworks",
    jsii_struct_bases=[],
    name_mapping={"cidr_range": "cidrRange"},
)
class GoogleAlloydbInstanceNetworkConfigAuthorizedExternalNetworks:
    def __init__(self, *, cidr_range: typing.Optional[builtins.str] = None) -> None:
        '''
        :param cidr_range: CIDR range for one authorized network of the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#cidr_range GoogleAlloydbInstance#cidr_range}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31866c78d8cbfa4bc86266921265a321b6754579dfa0e97e90858ec28b4c7ba5)
            check_type(argname="argument cidr_range", value=cidr_range, expected_type=type_hints["cidr_range"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cidr_range is not None:
            self._values["cidr_range"] = cidr_range

    @builtins.property
    def cidr_range(self) -> typing.Optional[builtins.str]:
        '''CIDR range for one authorized network of the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#cidr_range GoogleAlloydbInstance#cidr_range}
        '''
        result = self._values.get("cidr_range")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAlloydbInstanceNetworkConfigAuthorizedExternalNetworks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAlloydbInstanceNetworkConfigAuthorizedExternalNetworksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbInstance.GoogleAlloydbInstanceNetworkConfigAuthorizedExternalNetworksList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9e4f2ef1d40937bf6dd364bcde0b1edb7000d7a32b844b0895415f1147e8a07)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleAlloydbInstanceNetworkConfigAuthorizedExternalNetworksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc4d50e64f450f3d2037e5ac9d46215dafb098a154e4cf8bfcd7f856e7a08993)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleAlloydbInstanceNetworkConfigAuthorizedExternalNetworksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7205140e3121b726dc99e1df54351954fcd82171b0315dcdbddaf1a7f914e4fa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5f990ff49bd26044026593a9b59a5e983cc22157b40b44ebd08142f0931cd7f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__be97b816f718fa171a83081c005bb5fd3f0f061dfc08a1f05b62a043ef84d219)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAlloydbInstanceNetworkConfigAuthorizedExternalNetworks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAlloydbInstanceNetworkConfigAuthorizedExternalNetworks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAlloydbInstanceNetworkConfigAuthorizedExternalNetworks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beca0c7c3f9e6dbc1a8a81464586b1582fb0e560256d092401b7e9003b90854e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAlloydbInstanceNetworkConfigAuthorizedExternalNetworksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbInstance.GoogleAlloydbInstanceNetworkConfigAuthorizedExternalNetworksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bffdb78661bce067af4c814fdc19f141bc462210f200e9684d83ead65a0051b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCidrRange")
    def reset_cidr_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCidrRange", []))

    @builtins.property
    @jsii.member(jsii_name="cidrRangeInput")
    def cidr_range_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cidrRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="cidrRange")
    def cidr_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cidrRange"))

    @cidr_range.setter
    def cidr_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acb2fb96b67055938afb5ac9f41e02eb2cde1b1e586b3fa72426179353db66c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cidrRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAlloydbInstanceNetworkConfigAuthorizedExternalNetworks]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAlloydbInstanceNetworkConfigAuthorizedExternalNetworks]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAlloydbInstanceNetworkConfigAuthorizedExternalNetworks]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__827d06412dc6d43d25c7c1f9a76f181092820198e9ff1f60d826b50049bf0139)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAlloydbInstanceNetworkConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbInstance.GoogleAlloydbInstanceNetworkConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__580c58a0880caa3268aa859d0ae12bc998e4123d932bbd7958231b8018805273)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAuthorizedExternalNetworks")
    def put_authorized_external_networks(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAlloydbInstanceNetworkConfigAuthorizedExternalNetworks, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c69280aeae9cc560bebd405c7a6b2ea5095ee488fb73a94166a26dedca26e658)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAuthorizedExternalNetworks", [value]))

    @jsii.member(jsii_name="resetAuthorizedExternalNetworks")
    def reset_authorized_external_networks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthorizedExternalNetworks", []))

    @jsii.member(jsii_name="resetEnableOutboundPublicIp")
    def reset_enable_outbound_public_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableOutboundPublicIp", []))

    @jsii.member(jsii_name="resetEnablePublicIp")
    def reset_enable_public_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnablePublicIp", []))

    @builtins.property
    @jsii.member(jsii_name="authorizedExternalNetworks")
    def authorized_external_networks(
        self,
    ) -> GoogleAlloydbInstanceNetworkConfigAuthorizedExternalNetworksList:
        return typing.cast(GoogleAlloydbInstanceNetworkConfigAuthorizedExternalNetworksList, jsii.get(self, "authorizedExternalNetworks"))

    @builtins.property
    @jsii.member(jsii_name="authorizedExternalNetworksInput")
    def authorized_external_networks_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAlloydbInstanceNetworkConfigAuthorizedExternalNetworks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAlloydbInstanceNetworkConfigAuthorizedExternalNetworks]]], jsii.get(self, "authorizedExternalNetworksInput"))

    @builtins.property
    @jsii.member(jsii_name="enableOutboundPublicIpInput")
    def enable_outbound_public_ip_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableOutboundPublicIpInput"))

    @builtins.property
    @jsii.member(jsii_name="enablePublicIpInput")
    def enable_public_ip_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enablePublicIpInput"))

    @builtins.property
    @jsii.member(jsii_name="enableOutboundPublicIp")
    def enable_outbound_public_ip(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableOutboundPublicIp"))

    @enable_outbound_public_ip.setter
    def enable_outbound_public_ip(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e955f6f55b497abd6373ceca1c5bb327af217cd59d8a03d1e4120dd45456763)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableOutboundPublicIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enablePublicIp")
    def enable_public_ip(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enablePublicIp"))

    @enable_public_ip.setter
    def enable_public_ip(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4984252002cc5b2ab3b9562f60c134fb5cb565cfbbfb5dd2c69a2298d1f52b40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enablePublicIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleAlloydbInstanceNetworkConfig]:
        return typing.cast(typing.Optional[GoogleAlloydbInstanceNetworkConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAlloydbInstanceNetworkConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d83193c16949decde2d7051371c23dbb23ada7da35861bf3c5e451f80a60e1c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAlloydbInstance.GoogleAlloydbInstanceObservabilityConfig",
    jsii_struct_bases=[],
    name_mapping={
        "assistive_experiences_enabled": "assistiveExperiencesEnabled",
        "enabled": "enabled",
        "max_query_string_length": "maxQueryStringLength",
        "preserve_comments": "preserveComments",
        "query_plans_per_minute": "queryPlansPerMinute",
        "record_application_tags": "recordApplicationTags",
        "track_active_queries": "trackActiveQueries",
        "track_wait_events": "trackWaitEvents",
        "track_wait_event_types": "trackWaitEventTypes",
    },
)
class GoogleAlloydbInstanceObservabilityConfig:
    def __init__(
        self,
        *,
        assistive_experiences_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_query_string_length: typing.Optional[jsii.Number] = None,
        preserve_comments: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        query_plans_per_minute: typing.Optional[jsii.Number] = None,
        record_application_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        track_active_queries: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        track_wait_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        track_wait_event_types: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param assistive_experiences_enabled: Whether assistive experiences are enabled for this AlloyDB instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#assistive_experiences_enabled GoogleAlloydbInstance#assistive_experiences_enabled}
        :param enabled: Observability feature status for an instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#enabled GoogleAlloydbInstance#enabled}
        :param max_query_string_length: Query string length. The default value is 10240. Any integer between 1024 and 100000 is considered valid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#max_query_string_length GoogleAlloydbInstance#max_query_string_length}
        :param preserve_comments: Preserve comments in the query string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#preserve_comments GoogleAlloydbInstance#preserve_comments}
        :param query_plans_per_minute: Number of query execution plans captured by Insights per minute for all queries combined. The default value is 5. Any integer between 0 and 200 is considered valid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#query_plans_per_minute GoogleAlloydbInstance#query_plans_per_minute}
        :param record_application_tags: Record application tags for an instance. This flag is turned "on" by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#record_application_tags GoogleAlloydbInstance#record_application_tags}
        :param track_active_queries: Track actively running queries. If not set, default value is "off". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#track_active_queries GoogleAlloydbInstance#track_active_queries}
        :param track_wait_events: Record wait events during query execution for an instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#track_wait_events GoogleAlloydbInstance#track_wait_events}
        :param track_wait_event_types: Record wait event types during query execution for an instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#track_wait_event_types GoogleAlloydbInstance#track_wait_event_types}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7053f6bd762a7b257def7dd7a14d9103b13aceed02fab1037ca35f4ec5e7a61a)
            check_type(argname="argument assistive_experiences_enabled", value=assistive_experiences_enabled, expected_type=type_hints["assistive_experiences_enabled"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument max_query_string_length", value=max_query_string_length, expected_type=type_hints["max_query_string_length"])
            check_type(argname="argument preserve_comments", value=preserve_comments, expected_type=type_hints["preserve_comments"])
            check_type(argname="argument query_plans_per_minute", value=query_plans_per_minute, expected_type=type_hints["query_plans_per_minute"])
            check_type(argname="argument record_application_tags", value=record_application_tags, expected_type=type_hints["record_application_tags"])
            check_type(argname="argument track_active_queries", value=track_active_queries, expected_type=type_hints["track_active_queries"])
            check_type(argname="argument track_wait_events", value=track_wait_events, expected_type=type_hints["track_wait_events"])
            check_type(argname="argument track_wait_event_types", value=track_wait_event_types, expected_type=type_hints["track_wait_event_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if assistive_experiences_enabled is not None:
            self._values["assistive_experiences_enabled"] = assistive_experiences_enabled
        if enabled is not None:
            self._values["enabled"] = enabled
        if max_query_string_length is not None:
            self._values["max_query_string_length"] = max_query_string_length
        if preserve_comments is not None:
            self._values["preserve_comments"] = preserve_comments
        if query_plans_per_minute is not None:
            self._values["query_plans_per_minute"] = query_plans_per_minute
        if record_application_tags is not None:
            self._values["record_application_tags"] = record_application_tags
        if track_active_queries is not None:
            self._values["track_active_queries"] = track_active_queries
        if track_wait_events is not None:
            self._values["track_wait_events"] = track_wait_events
        if track_wait_event_types is not None:
            self._values["track_wait_event_types"] = track_wait_event_types

    @builtins.property
    def assistive_experiences_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether assistive experiences are enabled for this AlloyDB instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#assistive_experiences_enabled GoogleAlloydbInstance#assistive_experiences_enabled}
        '''
        result = self._values.get("assistive_experiences_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Observability feature status for an instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#enabled GoogleAlloydbInstance#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def max_query_string_length(self) -> typing.Optional[jsii.Number]:
        '''Query string length. The default value is 10240. Any integer between 1024 and 100000 is considered valid.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#max_query_string_length GoogleAlloydbInstance#max_query_string_length}
        '''
        result = self._values.get("max_query_string_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def preserve_comments(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Preserve comments in the query string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#preserve_comments GoogleAlloydbInstance#preserve_comments}
        '''
        result = self._values.get("preserve_comments")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def query_plans_per_minute(self) -> typing.Optional[jsii.Number]:
        '''Number of query execution plans captured by Insights per minute for all queries combined.

        The default value is 5. Any integer between 0 and 200 is considered valid.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#query_plans_per_minute GoogleAlloydbInstance#query_plans_per_minute}
        '''
        result = self._values.get("query_plans_per_minute")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def record_application_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Record application tags for an instance. This flag is turned "on" by default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#record_application_tags GoogleAlloydbInstance#record_application_tags}
        '''
        result = self._values.get("record_application_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def track_active_queries(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Track actively running queries. If not set, default value is "off".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#track_active_queries GoogleAlloydbInstance#track_active_queries}
        '''
        result = self._values.get("track_active_queries")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def track_wait_events(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Record wait events during query execution for an instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#track_wait_events GoogleAlloydbInstance#track_wait_events}
        '''
        result = self._values.get("track_wait_events")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def track_wait_event_types(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Record wait event types during query execution for an instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#track_wait_event_types GoogleAlloydbInstance#track_wait_event_types}
        '''
        result = self._values.get("track_wait_event_types")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAlloydbInstanceObservabilityConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAlloydbInstanceObservabilityConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbInstance.GoogleAlloydbInstanceObservabilityConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5ede40969ccc0a6cbf4f2d74cb7646b4235e604ad2317fea64f14e20c24eb2b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAssistiveExperiencesEnabled")
    def reset_assistive_experiences_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssistiveExperiencesEnabled", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetMaxQueryStringLength")
    def reset_max_query_string_length(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxQueryStringLength", []))

    @jsii.member(jsii_name="resetPreserveComments")
    def reset_preserve_comments(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreserveComments", []))

    @jsii.member(jsii_name="resetQueryPlansPerMinute")
    def reset_query_plans_per_minute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryPlansPerMinute", []))

    @jsii.member(jsii_name="resetRecordApplicationTags")
    def reset_record_application_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecordApplicationTags", []))

    @jsii.member(jsii_name="resetTrackActiveQueries")
    def reset_track_active_queries(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrackActiveQueries", []))

    @jsii.member(jsii_name="resetTrackWaitEvents")
    def reset_track_wait_events(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrackWaitEvents", []))

    @jsii.member(jsii_name="resetTrackWaitEventTypes")
    def reset_track_wait_event_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrackWaitEventTypes", []))

    @builtins.property
    @jsii.member(jsii_name="assistiveExperiencesEnabledInput")
    def assistive_experiences_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "assistiveExperiencesEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="maxQueryStringLengthInput")
    def max_query_string_length_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxQueryStringLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="preserveCommentsInput")
    def preserve_comments_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "preserveCommentsInput"))

    @builtins.property
    @jsii.member(jsii_name="queryPlansPerMinuteInput")
    def query_plans_per_minute_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "queryPlansPerMinuteInput"))

    @builtins.property
    @jsii.member(jsii_name="recordApplicationTagsInput")
    def record_application_tags_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "recordApplicationTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="trackActiveQueriesInput")
    def track_active_queries_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "trackActiveQueriesInput"))

    @builtins.property
    @jsii.member(jsii_name="trackWaitEventsInput")
    def track_wait_events_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "trackWaitEventsInput"))

    @builtins.property
    @jsii.member(jsii_name="trackWaitEventTypesInput")
    def track_wait_event_types_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "trackWaitEventTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="assistiveExperiencesEnabled")
    def assistive_experiences_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "assistiveExperiencesEnabled"))

    @assistive_experiences_enabled.setter
    def assistive_experiences_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__671e61f06879a304d589d4b03c63ecc83ff06ac24648dc9b03145674dc741757)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assistiveExperiencesEnabled", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__208b7c02aa1a8814742b066a44c1ea70fc705aef14c1afef5b96c4ebb6d0b40d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxQueryStringLength")
    def max_query_string_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxQueryStringLength"))

    @max_query_string_length.setter
    def max_query_string_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f6c5e1eaf09225cf39b5d127ad6e6bdeb7d665add19a5a3213ae6771437fa46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxQueryStringLength", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preserveComments")
    def preserve_comments(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "preserveComments"))

    @preserve_comments.setter
    def preserve_comments(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f801c085b0914dcf14643c7cb0b26233a04f86ec58d992ae0981cb524b72a1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preserveComments", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryPlansPerMinute")
    def query_plans_per_minute(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "queryPlansPerMinute"))

    @query_plans_per_minute.setter
    def query_plans_per_minute(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad99b86cffb9bda151f7dddda82c68b8a16fc6b6b08cecb6880f8e5eaef46590)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryPlansPerMinute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recordApplicationTags")
    def record_application_tags(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "recordApplicationTags"))

    @record_application_tags.setter
    def record_application_tags(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edbf77ade398a178ff5ee1778ffbb4623141ea1558eac9b92948b9810ed53c7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recordApplicationTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trackActiveQueries")
    def track_active_queries(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "trackActiveQueries"))

    @track_active_queries.setter
    def track_active_queries(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acf713ff2b05e65fae67754fe146ba3a3bf58bd8f14a413cd374efc8d46ee9c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trackActiveQueries", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trackWaitEvents")
    def track_wait_events(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "trackWaitEvents"))

    @track_wait_events.setter
    def track_wait_events(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05acc400a24a485c8cdbfb0f0a4a94d9428cb9aeff75ba8464fb0a53c2f20be6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trackWaitEvents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trackWaitEventTypes")
    def track_wait_event_types(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "trackWaitEventTypes"))

    @track_wait_event_types.setter
    def track_wait_event_types(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cacb4e11807e3429e0a4d868ecc34e374b5ff5ecdcd7deaf4bd7f631fccf095)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trackWaitEventTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAlloydbInstanceObservabilityConfig]:
        return typing.cast(typing.Optional[GoogleAlloydbInstanceObservabilityConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAlloydbInstanceObservabilityConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__591aa9ef25a29a5f1aa58d6bf93d649ec6cd9c53efaf5e70914108422afa5a6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAlloydbInstance.GoogleAlloydbInstancePscInstanceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_consumer_projects": "allowedConsumerProjects",
        "psc_auto_connections": "pscAutoConnections",
        "psc_interface_configs": "pscInterfaceConfigs",
    },
)
class GoogleAlloydbInstancePscInstanceConfig:
    def __init__(
        self,
        *,
        allowed_consumer_projects: typing.Optional[typing.Sequence[builtins.str]] = None,
        psc_auto_connections: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAlloydbInstancePscInstanceConfigPscAutoConnections", typing.Dict[builtins.str, typing.Any]]]]] = None,
        psc_interface_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAlloydbInstancePscInstanceConfigPscInterfaceConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param allowed_consumer_projects: List of consumer projects that are allowed to create PSC endpoints to service-attachments to this instance. These should be specified as project numbers only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#allowed_consumer_projects GoogleAlloydbInstance#allowed_consumer_projects}
        :param psc_auto_connections: psc_auto_connections block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#psc_auto_connections GoogleAlloydbInstance#psc_auto_connections}
        :param psc_interface_configs: psc_interface_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#psc_interface_configs GoogleAlloydbInstance#psc_interface_configs}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce7f5e4bfcc8efd56ade83b8b41910954f264f03d8694aea4a0d3717fdf2c45a)
            check_type(argname="argument allowed_consumer_projects", value=allowed_consumer_projects, expected_type=type_hints["allowed_consumer_projects"])
            check_type(argname="argument psc_auto_connections", value=psc_auto_connections, expected_type=type_hints["psc_auto_connections"])
            check_type(argname="argument psc_interface_configs", value=psc_interface_configs, expected_type=type_hints["psc_interface_configs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_consumer_projects is not None:
            self._values["allowed_consumer_projects"] = allowed_consumer_projects
        if psc_auto_connections is not None:
            self._values["psc_auto_connections"] = psc_auto_connections
        if psc_interface_configs is not None:
            self._values["psc_interface_configs"] = psc_interface_configs

    @builtins.property
    def allowed_consumer_projects(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of consumer projects that are allowed to create PSC endpoints to service-attachments to this instance.

        These should be specified as project numbers only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#allowed_consumer_projects GoogleAlloydbInstance#allowed_consumer_projects}
        '''
        result = self._values.get("allowed_consumer_projects")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def psc_auto_connections(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAlloydbInstancePscInstanceConfigPscAutoConnections"]]]:
        '''psc_auto_connections block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#psc_auto_connections GoogleAlloydbInstance#psc_auto_connections}
        '''
        result = self._values.get("psc_auto_connections")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAlloydbInstancePscInstanceConfigPscAutoConnections"]]], result)

    @builtins.property
    def psc_interface_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAlloydbInstancePscInstanceConfigPscInterfaceConfigs"]]]:
        '''psc_interface_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#psc_interface_configs GoogleAlloydbInstance#psc_interface_configs}
        '''
        result = self._values.get("psc_interface_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAlloydbInstancePscInstanceConfigPscInterfaceConfigs"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAlloydbInstancePscInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAlloydbInstancePscInstanceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbInstance.GoogleAlloydbInstancePscInstanceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a859987946d6ee2ea48238c2e276bd2effc589e95524e06a716915c73332a91f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPscAutoConnections")
    def put_psc_auto_connections(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAlloydbInstancePscInstanceConfigPscAutoConnections", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__976342474d181b1f089b5034c1c17cfab7f5611325cf034f3af7d4a2e5537202)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPscAutoConnections", [value]))

    @jsii.member(jsii_name="putPscInterfaceConfigs")
    def put_psc_interface_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAlloydbInstancePscInstanceConfigPscInterfaceConfigs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7805bd6ea814e23d349dff23efcb4e78f4fad6594618a023bd7a19ae8c2cce4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPscInterfaceConfigs", [value]))

    @jsii.member(jsii_name="resetAllowedConsumerProjects")
    def reset_allowed_consumer_projects(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedConsumerProjects", []))

    @jsii.member(jsii_name="resetPscAutoConnections")
    def reset_psc_auto_connections(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPscAutoConnections", []))

    @jsii.member(jsii_name="resetPscInterfaceConfigs")
    def reset_psc_interface_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPscInterfaceConfigs", []))

    @builtins.property
    @jsii.member(jsii_name="pscAutoConnections")
    def psc_auto_connections(
        self,
    ) -> "GoogleAlloydbInstancePscInstanceConfigPscAutoConnectionsList":
        return typing.cast("GoogleAlloydbInstancePscInstanceConfigPscAutoConnectionsList", jsii.get(self, "pscAutoConnections"))

    @builtins.property
    @jsii.member(jsii_name="pscDnsName")
    def psc_dns_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pscDnsName"))

    @builtins.property
    @jsii.member(jsii_name="pscInterfaceConfigs")
    def psc_interface_configs(
        self,
    ) -> "GoogleAlloydbInstancePscInstanceConfigPscInterfaceConfigsList":
        return typing.cast("GoogleAlloydbInstancePscInstanceConfigPscInterfaceConfigsList", jsii.get(self, "pscInterfaceConfigs"))

    @builtins.property
    @jsii.member(jsii_name="serviceAttachmentLink")
    def service_attachment_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAttachmentLink"))

    @builtins.property
    @jsii.member(jsii_name="allowedConsumerProjectsInput")
    def allowed_consumer_projects_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedConsumerProjectsInput"))

    @builtins.property
    @jsii.member(jsii_name="pscAutoConnectionsInput")
    def psc_auto_connections_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAlloydbInstancePscInstanceConfigPscAutoConnections"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAlloydbInstancePscInstanceConfigPscAutoConnections"]]], jsii.get(self, "pscAutoConnectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="pscInterfaceConfigsInput")
    def psc_interface_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAlloydbInstancePscInstanceConfigPscInterfaceConfigs"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAlloydbInstancePscInstanceConfigPscInterfaceConfigs"]]], jsii.get(self, "pscInterfaceConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedConsumerProjects")
    def allowed_consumer_projects(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedConsumerProjects"))

    @allowed_consumer_projects.setter
    def allowed_consumer_projects(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7486dfa9f081a6ab2e935e85623caf2d668c109aa3d6169df0a194ea15a738f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedConsumerProjects", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleAlloydbInstancePscInstanceConfig]:
        return typing.cast(typing.Optional[GoogleAlloydbInstancePscInstanceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAlloydbInstancePscInstanceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2793795b32205008ce798c44c92b168c97666641fcff9fe2a83c542feb29ae63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAlloydbInstance.GoogleAlloydbInstancePscInstanceConfigPscAutoConnections",
    jsii_struct_bases=[],
    name_mapping={
        "consumer_network": "consumerNetwork",
        "consumer_project": "consumerProject",
    },
)
class GoogleAlloydbInstancePscInstanceConfigPscAutoConnections:
    def __init__(
        self,
        *,
        consumer_network: typing.Optional[builtins.str] = None,
        consumer_project: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param consumer_network: The consumer network for the PSC service automation, example: "projects/vpc-host-project/global/networks/default". The consumer network might be hosted a different project than the consumer project. The API expects the consumer project specified to be the project ID (and not the project number) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#consumer_network GoogleAlloydbInstance#consumer_network}
        :param consumer_project: The consumer project to which the PSC service automation endpoint will be created. The API expects the consumer project to be the project ID( and not the project number). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#consumer_project GoogleAlloydbInstance#consumer_project}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d52125e8b3df1354f787c663a6762833c32ee0762583179d609e7b0132f881ef)
            check_type(argname="argument consumer_network", value=consumer_network, expected_type=type_hints["consumer_network"])
            check_type(argname="argument consumer_project", value=consumer_project, expected_type=type_hints["consumer_project"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if consumer_network is not None:
            self._values["consumer_network"] = consumer_network
        if consumer_project is not None:
            self._values["consumer_project"] = consumer_project

    @builtins.property
    def consumer_network(self) -> typing.Optional[builtins.str]:
        '''The consumer network for the PSC service automation, example: "projects/vpc-host-project/global/networks/default".

        The consumer network might be hosted a different project than the
        consumer project. The API expects the consumer project specified to be
        the project ID (and not the project number)

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#consumer_network GoogleAlloydbInstance#consumer_network}
        '''
        result = self._values.get("consumer_network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def consumer_project(self) -> typing.Optional[builtins.str]:
        '''The consumer project to which the PSC service automation endpoint will be created.

        The API expects the consumer project to be the project ID(
        and not the project number).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#consumer_project GoogleAlloydbInstance#consumer_project}
        '''
        result = self._values.get("consumer_project")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAlloydbInstancePscInstanceConfigPscAutoConnections(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAlloydbInstancePscInstanceConfigPscAutoConnectionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbInstance.GoogleAlloydbInstancePscInstanceConfigPscAutoConnectionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__66a55500f00ae59ca9b632453e17c69caf6859c0523dcb70234841a5c873c4aa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleAlloydbInstancePscInstanceConfigPscAutoConnectionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3b96188730102246012c2e96580e04d603c2c880d67fcbd51969eb90f4dbe43)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleAlloydbInstancePscInstanceConfigPscAutoConnectionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__998640784446d9d76666c885668afd309097c00d7fd4a17d5acb3dc461abc7fc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9a9a6d4adf7f90bf9c1e384e59c89c32f700c4c74fab1deffdde2a583162436)
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
            type_hints = typing.get_type_hints(_typecheckingstub__84ba739a76068a4b7ba5f8735771cbdb066ca0201590da30481e4317801017a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAlloydbInstancePscInstanceConfigPscAutoConnections]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAlloydbInstancePscInstanceConfigPscAutoConnections]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAlloydbInstancePscInstanceConfigPscAutoConnections]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__526413e7e896243cf5de7409f7cce4790f301ae0b5d150aeb259cf0ccbd836ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAlloydbInstancePscInstanceConfigPscAutoConnectionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbInstance.GoogleAlloydbInstancePscInstanceConfigPscAutoConnectionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2546dbcd101a5d009e31a616f643adec047791879c37043f14a0e093cd9fa638)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetConsumerNetwork")
    def reset_consumer_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsumerNetwork", []))

    @jsii.member(jsii_name="resetConsumerProject")
    def reset_consumer_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsumerProject", []))

    @builtins.property
    @jsii.member(jsii_name="consumerNetworkStatus")
    def consumer_network_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerNetworkStatus"))

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="consumerNetworkInput")
    def consumer_network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "consumerNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="consumerProjectInput")
    def consumer_project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "consumerProjectInput"))

    @builtins.property
    @jsii.member(jsii_name="consumerNetwork")
    def consumer_network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerNetwork"))

    @consumer_network.setter
    def consumer_network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3399e1e438d30bd3dc73d34c416e9f04e4e5b32f0ac13a7b81fd6f9c81e14e0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerNetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="consumerProject")
    def consumer_project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerProject"))

    @consumer_project.setter
    def consumer_project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a6bd2aecb77a0e353c0faca52cf692972ed3be8976d12191565974f19467346)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerProject", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAlloydbInstancePscInstanceConfigPscAutoConnections]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAlloydbInstancePscInstanceConfigPscAutoConnections]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAlloydbInstancePscInstanceConfigPscAutoConnections]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e00bb5a535cba054c39ab348df151433680e10c6ff5a501a8f92f5101a38770)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAlloydbInstance.GoogleAlloydbInstancePscInstanceConfigPscInterfaceConfigs",
    jsii_struct_bases=[],
    name_mapping={"network_attachment_resource": "networkAttachmentResource"},
)
class GoogleAlloydbInstancePscInstanceConfigPscInterfaceConfigs:
    def __init__(
        self,
        *,
        network_attachment_resource: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param network_attachment_resource: The network attachment resource created in the consumer project to which the PSC interface will be linked. This is of the format: "projects/${CONSUMER_PROJECT}/regions/${REGION}/networkAttachments/${NETWORK_ATTACHMENT_NAME}". The network attachment must be in the same region as the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#network_attachment_resource GoogleAlloydbInstance#network_attachment_resource}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bf10e7753596bfe7c85902425e48085c109b94a23c137bd90874532c1ff74f4)
            check_type(argname="argument network_attachment_resource", value=network_attachment_resource, expected_type=type_hints["network_attachment_resource"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if network_attachment_resource is not None:
            self._values["network_attachment_resource"] = network_attachment_resource

    @builtins.property
    def network_attachment_resource(self) -> typing.Optional[builtins.str]:
        '''The network attachment resource created in the consumer project to which the PSC interface will be linked.

        This is of the format: "projects/${CONSUMER_PROJECT}/regions/${REGION}/networkAttachments/${NETWORK_ATTACHMENT_NAME}".
        The network attachment must be in the same region as the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#network_attachment_resource GoogleAlloydbInstance#network_attachment_resource}
        '''
        result = self._values.get("network_attachment_resource")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAlloydbInstancePscInstanceConfigPscInterfaceConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAlloydbInstancePscInstanceConfigPscInterfaceConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbInstance.GoogleAlloydbInstancePscInstanceConfigPscInterfaceConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__893b58dab52b0efbc5a6308e6d74c430edb7db3d441e99246c80050e994ef057)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleAlloydbInstancePscInstanceConfigPscInterfaceConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f13a2ce85aa63bac4e595a24f92a124f357e1a2ce0d1c68434431ae7c4e7956)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleAlloydbInstancePscInstanceConfigPscInterfaceConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9f48a76c1c0020db0e698d0071e3912fcecc25ed9959a0264e49dce4e6b611c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7d8e615f40a5b5e97151f2cf65beffd84749583677f784ccd9df2ce79f39ef9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__80a61b35ba5adf76db520f44d38c753ebb3f99b4c8041e257c7c6d2a3ed5fca5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAlloydbInstancePscInstanceConfigPscInterfaceConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAlloydbInstancePscInstanceConfigPscInterfaceConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAlloydbInstancePscInstanceConfigPscInterfaceConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c91a5e1533d923ae66fd24b256056291a35db24be05bc77ef53c61d4ad38519b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAlloydbInstancePscInstanceConfigPscInterfaceConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbInstance.GoogleAlloydbInstancePscInstanceConfigPscInterfaceConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__01778ae17a6108c2270d3050e63f4531321489327081b780f3424b60aa4618cd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetNetworkAttachmentResource")
    def reset_network_attachment_resource(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkAttachmentResource", []))

    @builtins.property
    @jsii.member(jsii_name="networkAttachmentResourceInput")
    def network_attachment_resource_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkAttachmentResourceInput"))

    @builtins.property
    @jsii.member(jsii_name="networkAttachmentResource")
    def network_attachment_resource(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkAttachmentResource"))

    @network_attachment_resource.setter
    def network_attachment_resource(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79c419bb3275be835a424dfc54cf8e6db3399907151e5358273ab24080b45282)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkAttachmentResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAlloydbInstancePscInstanceConfigPscInterfaceConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAlloydbInstancePscInstanceConfigPscInterfaceConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAlloydbInstancePscInstanceConfigPscInterfaceConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4ae1d30fd1e1d51d2e006c4351c400a901431826a6760cff202a524ff864201)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAlloydbInstance.GoogleAlloydbInstanceQueryInsightsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "query_plans_per_minute": "queryPlansPerMinute",
        "query_string_length": "queryStringLength",
        "record_application_tags": "recordApplicationTags",
        "record_client_address": "recordClientAddress",
    },
)
class GoogleAlloydbInstanceQueryInsightsConfig:
    def __init__(
        self,
        *,
        query_plans_per_minute: typing.Optional[jsii.Number] = None,
        query_string_length: typing.Optional[jsii.Number] = None,
        record_application_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        record_client_address: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param query_plans_per_minute: Number of query execution plans captured by Insights per minute for all queries combined. The default value is 5. Any integer between 0 and 20 is considered valid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#query_plans_per_minute GoogleAlloydbInstance#query_plans_per_minute}
        :param query_string_length: Query string length. The default value is 1024. Any integer between 256 and 4500 is considered valid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#query_string_length GoogleAlloydbInstance#query_string_length}
        :param record_application_tags: Record application tags for an instance. This flag is turned "on" by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#record_application_tags GoogleAlloydbInstance#record_application_tags}
        :param record_client_address: Record client address for an instance. Client address is PII information. This flag is turned "on" by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#record_client_address GoogleAlloydbInstance#record_client_address}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__710b165618d517ef923959f6303f3dd016049f421ae8623ae3e051a9b01b6d67)
            check_type(argname="argument query_plans_per_minute", value=query_plans_per_minute, expected_type=type_hints["query_plans_per_minute"])
            check_type(argname="argument query_string_length", value=query_string_length, expected_type=type_hints["query_string_length"])
            check_type(argname="argument record_application_tags", value=record_application_tags, expected_type=type_hints["record_application_tags"])
            check_type(argname="argument record_client_address", value=record_client_address, expected_type=type_hints["record_client_address"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if query_plans_per_minute is not None:
            self._values["query_plans_per_minute"] = query_plans_per_minute
        if query_string_length is not None:
            self._values["query_string_length"] = query_string_length
        if record_application_tags is not None:
            self._values["record_application_tags"] = record_application_tags
        if record_client_address is not None:
            self._values["record_client_address"] = record_client_address

    @builtins.property
    def query_plans_per_minute(self) -> typing.Optional[jsii.Number]:
        '''Number of query execution plans captured by Insights per minute for all queries combined.

        The default value is 5. Any integer between 0 and 20 is considered valid.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#query_plans_per_minute GoogleAlloydbInstance#query_plans_per_minute}
        '''
        result = self._values.get("query_plans_per_minute")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def query_string_length(self) -> typing.Optional[jsii.Number]:
        '''Query string length. The default value is 1024. Any integer between 256 and 4500 is considered valid.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#query_string_length GoogleAlloydbInstance#query_string_length}
        '''
        result = self._values.get("query_string_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def record_application_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Record application tags for an instance. This flag is turned "on" by default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#record_application_tags GoogleAlloydbInstance#record_application_tags}
        '''
        result = self._values.get("record_application_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def record_client_address(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Record client address for an instance. Client address is PII information. This flag is turned "on" by default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#record_client_address GoogleAlloydbInstance#record_client_address}
        '''
        result = self._values.get("record_client_address")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAlloydbInstanceQueryInsightsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAlloydbInstanceQueryInsightsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbInstance.GoogleAlloydbInstanceQueryInsightsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb4ef087ab595cab0119fedfd542fbfdc7dfb202824d6af8e786eb18f65714a9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetQueryPlansPerMinute")
    def reset_query_plans_per_minute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryPlansPerMinute", []))

    @jsii.member(jsii_name="resetQueryStringLength")
    def reset_query_string_length(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryStringLength", []))

    @jsii.member(jsii_name="resetRecordApplicationTags")
    def reset_record_application_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecordApplicationTags", []))

    @jsii.member(jsii_name="resetRecordClientAddress")
    def reset_record_client_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecordClientAddress", []))

    @builtins.property
    @jsii.member(jsii_name="queryPlansPerMinuteInput")
    def query_plans_per_minute_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "queryPlansPerMinuteInput"))

    @builtins.property
    @jsii.member(jsii_name="queryStringLengthInput")
    def query_string_length_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "queryStringLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="recordApplicationTagsInput")
    def record_application_tags_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "recordApplicationTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="recordClientAddressInput")
    def record_client_address_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "recordClientAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="queryPlansPerMinute")
    def query_plans_per_minute(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "queryPlansPerMinute"))

    @query_plans_per_minute.setter
    def query_plans_per_minute(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb7377fdc877caf149df27db0179e89d9955b406a242b332056718cba31ccc01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryPlansPerMinute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryStringLength")
    def query_string_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "queryStringLength"))

    @query_string_length.setter
    def query_string_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2284d2210110b36df84c52da8cb17808cea32612c3853f54d007d5f3762ab75b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryStringLength", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recordApplicationTags")
    def record_application_tags(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "recordApplicationTags"))

    @record_application_tags.setter
    def record_application_tags(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f0b0942c5b2e6b28901cc6e253495aebd416c69d12f2654bd36a8824ba0d124)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recordApplicationTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recordClientAddress")
    def record_client_address(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "recordClientAddress"))

    @record_client_address.setter
    def record_client_address(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__436c1f4ec637f2e7868b34ca765cffb9edf1d7838b49a639c586c7076638839a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recordClientAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAlloydbInstanceQueryInsightsConfig]:
        return typing.cast(typing.Optional[GoogleAlloydbInstanceQueryInsightsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAlloydbInstanceQueryInsightsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21fae2f5314ad4b48343ee1d7e46ef8bda73df4a8a13a2f5bc22573a58fb40cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAlloydbInstance.GoogleAlloydbInstanceReadPoolConfig",
    jsii_struct_bases=[],
    name_mapping={"node_count": "nodeCount"},
)
class GoogleAlloydbInstanceReadPoolConfig:
    def __init__(self, *, node_count: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param node_count: Read capacity, i.e. number of nodes in a read pool instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#node_count GoogleAlloydbInstance#node_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__878e5906de16621dda5e762ce9d6f4dd7204f5f868865ad6200def611a50ba1d)
            check_type(argname="argument node_count", value=node_count, expected_type=type_hints["node_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if node_count is not None:
            self._values["node_count"] = node_count

    @builtins.property
    def node_count(self) -> typing.Optional[jsii.Number]:
        '''Read capacity, i.e. number of nodes in a read pool instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#node_count GoogleAlloydbInstance#node_count}
        '''
        result = self._values.get("node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAlloydbInstanceReadPoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAlloydbInstanceReadPoolConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbInstance.GoogleAlloydbInstanceReadPoolConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7201da290f68bd1ccfdaa3294ed2b706f2d239da12875881dab017b37897a61a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNodeCount")
    def reset_node_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeCount", []))

    @builtins.property
    @jsii.member(jsii_name="nodeCountInput")
    def node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeCount")
    def node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nodeCount"))

    @node_count.setter
    def node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__421792949c8a8cc8d9c4e95dcedfe2b5050655f60bbbbac7050f05aaa0ed1db6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleAlloydbInstanceReadPoolConfig]:
        return typing.cast(typing.Optional[GoogleAlloydbInstanceReadPoolConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAlloydbInstanceReadPoolConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__727107bed190d759199456103286709317c0f38fd900aea32c4e9fe158c76aa4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAlloydbInstance.GoogleAlloydbInstanceTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleAlloydbInstanceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#create GoogleAlloydbInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#delete GoogleAlloydbInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#update GoogleAlloydbInstance#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1187d566df0a175307b0339f6c2b3d4e94baf2e7b20f66d6af3799793b068b36)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#create GoogleAlloydbInstance#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#delete GoogleAlloydbInstance#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_instance#update GoogleAlloydbInstance#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAlloydbInstanceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAlloydbInstanceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbInstance.GoogleAlloydbInstanceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__03db0bfea0fa86d8d6db9ae48907747327a202c95942d83531f5f4f887e15901)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e92644d4ea88215c47dd24642794396145c3917bb74b1935d6215f46a9b2dbca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ed97b89952e6db6ccee5d87e973a4bb66786ffb83bdbd81f0dcc70c717fd5bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63331ed7d43fa769a907d5d442ec02ac76fe164bf01baf0f5fbfeea916f900fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAlloydbInstanceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAlloydbInstanceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAlloydbInstanceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85bb9565d49ab88aa7d1dbe5533e39c0e72c0439902e8e9ef0dcff55ce278368)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleAlloydbInstance",
    "GoogleAlloydbInstanceClientConnectionConfig",
    "GoogleAlloydbInstanceClientConnectionConfigOutputReference",
    "GoogleAlloydbInstanceClientConnectionConfigSslConfig",
    "GoogleAlloydbInstanceClientConnectionConfigSslConfigOutputReference",
    "GoogleAlloydbInstanceConfig",
    "GoogleAlloydbInstanceMachineConfig",
    "GoogleAlloydbInstanceMachineConfigOutputReference",
    "GoogleAlloydbInstanceNetworkConfig",
    "GoogleAlloydbInstanceNetworkConfigAuthorizedExternalNetworks",
    "GoogleAlloydbInstanceNetworkConfigAuthorizedExternalNetworksList",
    "GoogleAlloydbInstanceNetworkConfigAuthorizedExternalNetworksOutputReference",
    "GoogleAlloydbInstanceNetworkConfigOutputReference",
    "GoogleAlloydbInstanceObservabilityConfig",
    "GoogleAlloydbInstanceObservabilityConfigOutputReference",
    "GoogleAlloydbInstancePscInstanceConfig",
    "GoogleAlloydbInstancePscInstanceConfigOutputReference",
    "GoogleAlloydbInstancePscInstanceConfigPscAutoConnections",
    "GoogleAlloydbInstancePscInstanceConfigPscAutoConnectionsList",
    "GoogleAlloydbInstancePscInstanceConfigPscAutoConnectionsOutputReference",
    "GoogleAlloydbInstancePscInstanceConfigPscInterfaceConfigs",
    "GoogleAlloydbInstancePscInstanceConfigPscInterfaceConfigsList",
    "GoogleAlloydbInstancePscInstanceConfigPscInterfaceConfigsOutputReference",
    "GoogleAlloydbInstanceQueryInsightsConfig",
    "GoogleAlloydbInstanceQueryInsightsConfigOutputReference",
    "GoogleAlloydbInstanceReadPoolConfig",
    "GoogleAlloydbInstanceReadPoolConfigOutputReference",
    "GoogleAlloydbInstanceTimeouts",
    "GoogleAlloydbInstanceTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__d1a8431f1d79d47e80010c2b9e53867967d8a627e304fb135900b1ca4857761b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    cluster: builtins.str,
    instance_id: builtins.str,
    instance_type: builtins.str,
    activation_policy: typing.Optional[builtins.str] = None,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    availability_type: typing.Optional[builtins.str] = None,
    client_connection_config: typing.Optional[typing.Union[GoogleAlloydbInstanceClientConnectionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    database_flags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    display_name: typing.Optional[builtins.str] = None,
    gce_zone: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    machine_config: typing.Optional[typing.Union[GoogleAlloydbInstanceMachineConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    network_config: typing.Optional[typing.Union[GoogleAlloydbInstanceNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    observability_config: typing.Optional[typing.Union[GoogleAlloydbInstanceObservabilityConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    psc_instance_config: typing.Optional[typing.Union[GoogleAlloydbInstancePscInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    query_insights_config: typing.Optional[typing.Union[GoogleAlloydbInstanceQueryInsightsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    read_pool_config: typing.Optional[typing.Union[GoogleAlloydbInstanceReadPoolConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleAlloydbInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__cbc7d192f4f7254b9f89b99606c6177b6547f96720c1ca0a7b0dae57543e6474(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5e4a33bcbbc2afcb5ab2ffc8af3690cabee5beec2a779df4545d010e077f669(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdab180eaebb1c20b875be169c7e8648b426ed754372e9cfe26285577a8bca30(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb7c4a1b5134998988212626aca3e30c1b95606af98eb8bd91d10f568aeade0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f08ba00a79dcff56d4d664c133361d8fc254c102899ca8c4c5e29db0e40a3b27(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c54f0db0cb92cb4c0e3d62914cbbf5f27f3c6637e9d0a5135b3a5edb9d137375(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a957771901bb0839e17eaf8cbd6190be2d97cbd9920df8fdd8b0a945a234471(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55265f40907fc506324ea24fa52420cf92398df06940f3248e284c468cd03750(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__543413efe49247d5ffe58801c3d657c79df3dc29ab77558e44a2ab5f18c4efad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bb6a49a6236f7a2bb4d3dab0a02fd604f607fff761efd5c96f39d7f6edec1f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1663d3fb5610fe563ef3ad9c7307d7fef618c9850a6c308c1e5b8097bcf0b808(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7c79e218ea78840812781d8548a1554508101185ffbb8484df72b459e45cb13(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74b291b2a8343ac1b9980a3799af3f81040b3a480b90457aba41631ea840d0a4(
    *,
    require_connectors: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ssl_config: typing.Optional[typing.Union[GoogleAlloydbInstanceClientConnectionConfigSslConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03679b9ea60512ebdf9a23acff73e3e0c517b47e6fb75bb641a72eba35d5568c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e29b3ae62ba89a6d22ea69f925b18a76463521ddf7bfc9f589a0ec99f258fca(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5b090238c0a360562fba87c63f3e8a694eb92f8c4f6fbc5be25714ac32e14bf(
    value: typing.Optional[GoogleAlloydbInstanceClientConnectionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd3d37f257ac035dc1104c98fb2a5a4c2f762965ececce88f0b8630dff8f326f(
    *,
    ssl_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11571136aebdcdc377611a4a5b0c6e91f0dde2584d9466827b1282631588a5a2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3775061a1765432c10f132ac1cc73a5e5c28921a4de64630e73effd5fa0a373(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c33318f80056f4545f1eaa76a3889958bd0438c5a226def5b6bba674affa0d28(
    value: typing.Optional[GoogleAlloydbInstanceClientConnectionConfigSslConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e23660ca52ff717fea25350d3a179cb982cdf51741ea2be6bbd11692a311bf2(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cluster: builtins.str,
    instance_id: builtins.str,
    instance_type: builtins.str,
    activation_policy: typing.Optional[builtins.str] = None,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    availability_type: typing.Optional[builtins.str] = None,
    client_connection_config: typing.Optional[typing.Union[GoogleAlloydbInstanceClientConnectionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    database_flags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    display_name: typing.Optional[builtins.str] = None,
    gce_zone: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    machine_config: typing.Optional[typing.Union[GoogleAlloydbInstanceMachineConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    network_config: typing.Optional[typing.Union[GoogleAlloydbInstanceNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    observability_config: typing.Optional[typing.Union[GoogleAlloydbInstanceObservabilityConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    psc_instance_config: typing.Optional[typing.Union[GoogleAlloydbInstancePscInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    query_insights_config: typing.Optional[typing.Union[GoogleAlloydbInstanceQueryInsightsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    read_pool_config: typing.Optional[typing.Union[GoogleAlloydbInstanceReadPoolConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleAlloydbInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9537c0a0af16ef03bf3dacc7325bf7dda5b115b7544e166410a1aab5bfbc33b(
    *,
    cpu_count: typing.Optional[jsii.Number] = None,
    machine_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc032ccfb3144912de416f2c55f4778e88853b731ec88d2babd8bf37267719b1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fdc9724adf0c6e9c3140fb814e75331c37c1402f91a57054fcbcda1528c099a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54c030f74fc5a4160ad92cdc3f20c844530828332d443c2b8cff511044e704ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1772b8992f40c2963e7f532f3615c655c7ca05f04b859e843398b56e3a44c609(
    value: typing.Optional[GoogleAlloydbInstanceMachineConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95ba701575725b5bcb679fb88d22e218c26b7fddfdd7eb34473e7512d88c4fdd(
    *,
    authorized_external_networks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAlloydbInstanceNetworkConfigAuthorizedExternalNetworks, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enable_outbound_public_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_public_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31866c78d8cbfa4bc86266921265a321b6754579dfa0e97e90858ec28b4c7ba5(
    *,
    cidr_range: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9e4f2ef1d40937bf6dd364bcde0b1edb7000d7a32b844b0895415f1147e8a07(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc4d50e64f450f3d2037e5ac9d46215dafb098a154e4cf8bfcd7f856e7a08993(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7205140e3121b726dc99e1df54351954fcd82171b0315dcdbddaf1a7f914e4fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5f990ff49bd26044026593a9b59a5e983cc22157b40b44ebd08142f0931cd7f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be97b816f718fa171a83081c005bb5fd3f0f061dfc08a1f05b62a043ef84d219(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beca0c7c3f9e6dbc1a8a81464586b1582fb0e560256d092401b7e9003b90854e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAlloydbInstanceNetworkConfigAuthorizedExternalNetworks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bffdb78661bce067af4c814fdc19f141bc462210f200e9684d83ead65a0051b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acb2fb96b67055938afb5ac9f41e02eb2cde1b1e586b3fa72426179353db66c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__827d06412dc6d43d25c7c1f9a76f181092820198e9ff1f60d826b50049bf0139(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAlloydbInstanceNetworkConfigAuthorizedExternalNetworks]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__580c58a0880caa3268aa859d0ae12bc998e4123d932bbd7958231b8018805273(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c69280aeae9cc560bebd405c7a6b2ea5095ee488fb73a94166a26dedca26e658(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAlloydbInstanceNetworkConfigAuthorizedExternalNetworks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e955f6f55b497abd6373ceca1c5bb327af217cd59d8a03d1e4120dd45456763(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4984252002cc5b2ab3b9562f60c134fb5cb565cfbbfb5dd2c69a2298d1f52b40(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d83193c16949decde2d7051371c23dbb23ada7da35861bf3c5e451f80a60e1c3(
    value: typing.Optional[GoogleAlloydbInstanceNetworkConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7053f6bd762a7b257def7dd7a14d9103b13aceed02fab1037ca35f4ec5e7a61a(
    *,
    assistive_experiences_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    max_query_string_length: typing.Optional[jsii.Number] = None,
    preserve_comments: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    query_plans_per_minute: typing.Optional[jsii.Number] = None,
    record_application_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    track_active_queries: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    track_wait_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    track_wait_event_types: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5ede40969ccc0a6cbf4f2d74cb7646b4235e604ad2317fea64f14e20c24eb2b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__671e61f06879a304d589d4b03c63ecc83ff06ac24648dc9b03145674dc741757(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__208b7c02aa1a8814742b066a44c1ea70fc705aef14c1afef5b96c4ebb6d0b40d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f6c5e1eaf09225cf39b5d127ad6e6bdeb7d665add19a5a3213ae6771437fa46(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f801c085b0914dcf14643c7cb0b26233a04f86ec58d992ae0981cb524b72a1a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad99b86cffb9bda151f7dddda82c68b8a16fc6b6b08cecb6880f8e5eaef46590(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edbf77ade398a178ff5ee1778ffbb4623141ea1558eac9b92948b9810ed53c7b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acf713ff2b05e65fae67754fe146ba3a3bf58bd8f14a413cd374efc8d46ee9c1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05acc400a24a485c8cdbfb0f0a4a94d9428cb9aeff75ba8464fb0a53c2f20be6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cacb4e11807e3429e0a4d868ecc34e374b5ff5ecdcd7deaf4bd7f631fccf095(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__591aa9ef25a29a5f1aa58d6bf93d649ec6cd9c53efaf5e70914108422afa5a6a(
    value: typing.Optional[GoogleAlloydbInstanceObservabilityConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce7f5e4bfcc8efd56ade83b8b41910954f264f03d8694aea4a0d3717fdf2c45a(
    *,
    allowed_consumer_projects: typing.Optional[typing.Sequence[builtins.str]] = None,
    psc_auto_connections: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAlloydbInstancePscInstanceConfigPscAutoConnections, typing.Dict[builtins.str, typing.Any]]]]] = None,
    psc_interface_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAlloydbInstancePscInstanceConfigPscInterfaceConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a859987946d6ee2ea48238c2e276bd2effc589e95524e06a716915c73332a91f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__976342474d181b1f089b5034c1c17cfab7f5611325cf034f3af7d4a2e5537202(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAlloydbInstancePscInstanceConfigPscAutoConnections, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7805bd6ea814e23d349dff23efcb4e78f4fad6594618a023bd7a19ae8c2cce4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAlloydbInstancePscInstanceConfigPscInterfaceConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7486dfa9f081a6ab2e935e85623caf2d668c109aa3d6169df0a194ea15a738f0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2793795b32205008ce798c44c92b168c97666641fcff9fe2a83c542feb29ae63(
    value: typing.Optional[GoogleAlloydbInstancePscInstanceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d52125e8b3df1354f787c663a6762833c32ee0762583179d609e7b0132f881ef(
    *,
    consumer_network: typing.Optional[builtins.str] = None,
    consumer_project: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66a55500f00ae59ca9b632453e17c69caf6859c0523dcb70234841a5c873c4aa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3b96188730102246012c2e96580e04d603c2c880d67fcbd51969eb90f4dbe43(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__998640784446d9d76666c885668afd309097c00d7fd4a17d5acb3dc461abc7fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9a9a6d4adf7f90bf9c1e384e59c89c32f700c4c74fab1deffdde2a583162436(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84ba739a76068a4b7ba5f8735771cbdb066ca0201590da30481e4317801017a1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__526413e7e896243cf5de7409f7cce4790f301ae0b5d150aeb259cf0ccbd836ba(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAlloydbInstancePscInstanceConfigPscAutoConnections]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2546dbcd101a5d009e31a616f643adec047791879c37043f14a0e093cd9fa638(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3399e1e438d30bd3dc73d34c416e9f04e4e5b32f0ac13a7b81fd6f9c81e14e0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a6bd2aecb77a0e353c0faca52cf692972ed3be8976d12191565974f19467346(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e00bb5a535cba054c39ab348df151433680e10c6ff5a501a8f92f5101a38770(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAlloydbInstancePscInstanceConfigPscAutoConnections]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bf10e7753596bfe7c85902425e48085c109b94a23c137bd90874532c1ff74f4(
    *,
    network_attachment_resource: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__893b58dab52b0efbc5a6308e6d74c430edb7db3d441e99246c80050e994ef057(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f13a2ce85aa63bac4e595a24f92a124f357e1a2ce0d1c68434431ae7c4e7956(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9f48a76c1c0020db0e698d0071e3912fcecc25ed9959a0264e49dce4e6b611c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7d8e615f40a5b5e97151f2cf65beffd84749583677f784ccd9df2ce79f39ef9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80a61b35ba5adf76db520f44d38c753ebb3f99b4c8041e257c7c6d2a3ed5fca5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c91a5e1533d923ae66fd24b256056291a35db24be05bc77ef53c61d4ad38519b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAlloydbInstancePscInstanceConfigPscInterfaceConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01778ae17a6108c2270d3050e63f4531321489327081b780f3424b60aa4618cd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79c419bb3275be835a424dfc54cf8e6db3399907151e5358273ab24080b45282(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4ae1d30fd1e1d51d2e006c4351c400a901431826a6760cff202a524ff864201(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAlloydbInstancePscInstanceConfigPscInterfaceConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__710b165618d517ef923959f6303f3dd016049f421ae8623ae3e051a9b01b6d67(
    *,
    query_plans_per_minute: typing.Optional[jsii.Number] = None,
    query_string_length: typing.Optional[jsii.Number] = None,
    record_application_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    record_client_address: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb4ef087ab595cab0119fedfd542fbfdc7dfb202824d6af8e786eb18f65714a9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb7377fdc877caf149df27db0179e89d9955b406a242b332056718cba31ccc01(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2284d2210110b36df84c52da8cb17808cea32612c3853f54d007d5f3762ab75b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f0b0942c5b2e6b28901cc6e253495aebd416c69d12f2654bd36a8824ba0d124(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__436c1f4ec637f2e7868b34ca765cffb9edf1d7838b49a639c586c7076638839a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21fae2f5314ad4b48343ee1d7e46ef8bda73df4a8a13a2f5bc22573a58fb40cd(
    value: typing.Optional[GoogleAlloydbInstanceQueryInsightsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__878e5906de16621dda5e762ce9d6f4dd7204f5f868865ad6200def611a50ba1d(
    *,
    node_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7201da290f68bd1ccfdaa3294ed2b706f2d239da12875881dab017b37897a61a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__421792949c8a8cc8d9c4e95dcedfe2b5050655f60bbbbac7050f05aaa0ed1db6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__727107bed190d759199456103286709317c0f38fd900aea32c4e9fe158c76aa4(
    value: typing.Optional[GoogleAlloydbInstanceReadPoolConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1187d566df0a175307b0339f6c2b3d4e94baf2e7b20f66d6af3799793b068b36(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03db0bfea0fa86d8d6db9ae48907747327a202c95942d83531f5f4f887e15901(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e92644d4ea88215c47dd24642794396145c3917bb74b1935d6215f46a9b2dbca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ed97b89952e6db6ccee5d87e973a4bb66786ffb83bdbd81f0dcc70c717fd5bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63331ed7d43fa769a907d5d442ec02ac76fe164bf01baf0f5fbfeea916f900fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85bb9565d49ab88aa7d1dbe5533e39c0e72c0439902e8e9ef0dcff55ce278368(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAlloydbInstanceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
