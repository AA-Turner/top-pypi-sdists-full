r'''
# `google_alloydb_instance`

Refer to the Terraform Registry for docs: [`google_alloydb_instance`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance).
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


class AlloydbInstance(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbInstance.AlloydbInstance",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance google_alloydb_instance}.'''

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
        client_connection_config: typing.Optional[typing.Union["AlloydbInstanceClientConnectionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        database_flags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        display_name: typing.Optional[builtins.str] = None,
        gce_zone: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        machine_config: typing.Optional[typing.Union["AlloydbInstanceMachineConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        network_config: typing.Optional[typing.Union["AlloydbInstanceNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        psc_instance_config: typing.Optional[typing.Union["AlloydbInstancePscInstanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        query_insights_config: typing.Optional[typing.Union["AlloydbInstanceQueryInsightsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        read_pool_config: typing.Optional[typing.Union["AlloydbInstanceReadPoolConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["AlloydbInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance google_alloydb_instance} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cluster: Identifies the alloydb cluster. Must be in the format 'projects/{project}/locations/{location}/clusters/{cluster_id}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#cluster AlloydbInstance#cluster}
        :param instance_id: The ID of the alloydb instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#instance_id AlloydbInstance#instance_id}
        :param instance_type: The type of the instance. If the instance type is READ_POOL, provide the associated PRIMARY/SECONDARY instance in the 'depends_on' meta-data attribute. If the instance type is SECONDARY, point to the cluster_type of the associated secondary cluster instead of mentioning SECONDARY. Example: {instance_type = google_alloydb_cluster.<secondary_cluster_name>.cluster_type} instead of {instance_type = SECONDARY} If the instance type is SECONDARY, the terraform delete instance operation does not delete the secondary instance but abandons it instead. Use deletion_policy = "FORCE" in the associated secondary cluster and delete the cluster forcefully to delete the secondary cluster as well its associated secondary instance. Users can undo the delete secondary instance action by importing the deleted secondary instance by calling terraform import. Possible values: ["PRIMARY", "READ_POOL", "SECONDARY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#instance_type AlloydbInstance#instance_type}
        :param activation_policy: 'Specifies whether an instance needs to spin up. Once the instance is active, the activation policy can be updated to the 'NEVER' to stop the instance. Likewise, the activation policy can be updated to 'ALWAYS' to start the instance. There are restrictions around when an instance can/cannot be activated (for example, a read pool instance should be stopped before stopping primary etc.). Please refer to the API documentation for more details. Possible values are: 'ACTIVATION_POLICY_UNSPECIFIED', 'ALWAYS', 'NEVER'.' Possible values: ["ACTIVATION_POLICY_UNSPECIFIED", "ALWAYS", "NEVER"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#activation_policy AlloydbInstance#activation_policy}
        :param annotations: Annotations to allow client tools to store small amount of arbitrary data. This is distinct from labels. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#annotations AlloydbInstance#annotations}
        :param availability_type: 'Availability type of an Instance. Defaults to REGIONAL for both primary and read instances. Note that primary and read instances can have different availability types. Primary instances can be either ZONAL or REGIONAL. Read Pool instances can also be either ZONAL or REGIONAL. Read pools of size 1 can only have zonal availability. Read pools with a node count of 2 or more can have regional availability (nodes are present in 2 or more zones in a region). Possible values are: 'AVAILABILITY_TYPE_UNSPECIFIED', 'ZONAL', 'REGIONAL'.' Possible values: ["AVAILABILITY_TYPE_UNSPECIFIED", "ZONAL", "REGIONAL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#availability_type AlloydbInstance#availability_type}
        :param client_connection_config: client_connection_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#client_connection_config AlloydbInstance#client_connection_config}
        :param database_flags: Database flags. Set at instance level. * They are copied from primary instance on read instance creation. * Read instances can set new or override existing flags that are relevant for reads, e.g. for enabling columnar cache on a read instance. Flags set on read instance may or may not be present on primary. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#database_flags AlloydbInstance#database_flags}
        :param display_name: User-settable and human-readable display name for the Instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#display_name AlloydbInstance#display_name}
        :param gce_zone: The Compute Engine zone that the instance should serve from, per https://cloud.google.com/compute/docs/regions-zones This can ONLY be specified for ZONAL instances. If present for a REGIONAL instance, an error will be thrown. If this is absent for a ZONAL instance, instance is created in a random zone with available capacity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#gce_zone AlloydbInstance#gce_zone}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#id AlloydbInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: User-defined labels for the alloydb instance. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#labels AlloydbInstance#labels}
        :param machine_config: machine_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#machine_config AlloydbInstance#machine_config}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#network_config AlloydbInstance#network_config}
        :param psc_instance_config: psc_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#psc_instance_config AlloydbInstance#psc_instance_config}
        :param query_insights_config: query_insights_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#query_insights_config AlloydbInstance#query_insights_config}
        :param read_pool_config: read_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#read_pool_config AlloydbInstance#read_pool_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#timeouts AlloydbInstance#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f765b873890bbf96433922dc1fea912d0f8d2ec8f3688afc26caab7e8fd9c0aa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AlloydbInstanceConfig(
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
        '''Generates CDKTF code for importing a AlloydbInstance resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AlloydbInstance to import.
        :param import_from_id: The id of the existing AlloydbInstance that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AlloydbInstance to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d454a858279d54fbe39535893d0c5306da4d01321e151b87cae12309fe9889b)
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
        ssl_config: typing.Optional[typing.Union["AlloydbInstanceClientConnectionConfigSslConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param require_connectors: Configuration to enforce connectors only (ex: AuthProxy) connections to the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#require_connectors AlloydbInstance#require_connectors}
        :param ssl_config: ssl_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#ssl_config AlloydbInstance#ssl_config}
        '''
        value = AlloydbInstanceClientConnectionConfig(
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
        :param cpu_count: The number of CPU's in the VM instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#cpu_count AlloydbInstance#cpu_count}
        :param machine_type: Machine type of the VM instance. E.g. "n2-highmem-4", "n2-highmem-8", "c4a-highmem-4-lssd". 'cpu_count' must match the number of vCPUs in the machine type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#machine_type AlloydbInstance#machine_type}
        '''
        value = AlloydbInstanceMachineConfig(
            cpu_count=cpu_count, machine_type=machine_type
        )

        return typing.cast(None, jsii.invoke(self, "putMachineConfig", [value]))

    @jsii.member(jsii_name="putNetworkConfig")
    def put_network_config(
        self,
        *,
        allocated_ip_range_override: typing.Optional[builtins.str] = None,
        authorized_external_networks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AlloydbInstanceNetworkConfigAuthorizedExternalNetworks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        enable_outbound_public_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_public_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param allocated_ip_range_override: Name of the allocated IP range for the private IP AlloyDB instance, for example: "google-managed-services-default". If set, the instance IPs will be created from this allocated range and will override the IP range used by the parent cluster. The range name must comply with RFC 1035. Specifically, the name must be 1-63 characters long and match the regular expression `a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#allocated_ip_range_override AlloydbInstance#allocated_ip_range_override}
        :param authorized_external_networks: authorized_external_networks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#authorized_external_networks AlloydbInstance#authorized_external_networks}
        :param enable_outbound_public_ip: Enabling outbound public ip for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#enable_outbound_public_ip AlloydbInstance#enable_outbound_public_ip}
        :param enable_public_ip: Enabling public ip for the instance. If a user wishes to disable this, please also clear the list of the authorized external networks set on the same instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#enable_public_ip AlloydbInstance#enable_public_ip}
        '''
        value = AlloydbInstanceNetworkConfig(
            allocated_ip_range_override=allocated_ip_range_override,
            authorized_external_networks=authorized_external_networks,
            enable_outbound_public_ip=enable_outbound_public_ip,
            enable_public_ip=enable_public_ip,
        )

        return typing.cast(None, jsii.invoke(self, "putNetworkConfig", [value]))

    @jsii.member(jsii_name="putPscInstanceConfig")
    def put_psc_instance_config(
        self,
        *,
        allowed_consumer_projects: typing.Optional[typing.Sequence[builtins.str]] = None,
        psc_auto_connections: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AlloydbInstancePscInstanceConfigPscAutoConnections", typing.Dict[builtins.str, typing.Any]]]]] = None,
        psc_interface_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AlloydbInstancePscInstanceConfigPscInterfaceConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param allowed_consumer_projects: List of consumer projects that are allowed to create PSC endpoints to service-attachments to this instance. These should be specified as project numbers only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#allowed_consumer_projects AlloydbInstance#allowed_consumer_projects}
        :param psc_auto_connections: psc_auto_connections block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#psc_auto_connections AlloydbInstance#psc_auto_connections}
        :param psc_interface_configs: psc_interface_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#psc_interface_configs AlloydbInstance#psc_interface_configs}
        '''
        value = AlloydbInstancePscInstanceConfig(
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
        :param query_plans_per_minute: Number of query execution plans captured by Insights per minute for all queries combined. The default value is 5. Any integer between 0 and 20 is considered valid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#query_plans_per_minute AlloydbInstance#query_plans_per_minute}
        :param query_string_length: Query string length. The default value is 1024. Any integer between 256 and 4500 is considered valid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#query_string_length AlloydbInstance#query_string_length}
        :param record_application_tags: Record application tags for an instance. This flag is turned "on" by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#record_application_tags AlloydbInstance#record_application_tags}
        :param record_client_address: Record client address for an instance. Client address is PII information. This flag is turned "on" by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#record_client_address AlloydbInstance#record_client_address}
        '''
        value = AlloydbInstanceQueryInsightsConfig(
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
        :param node_count: Read capacity, i.e. number of nodes in a read pool instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#node_count AlloydbInstance#node_count}
        '''
        value = AlloydbInstanceReadPoolConfig(node_count=node_count)

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#create AlloydbInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#delete AlloydbInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#update AlloydbInstance#update}.
        '''
        value = AlloydbInstanceTimeouts(create=create, delete=delete, update=update)

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
    ) -> "AlloydbInstanceClientConnectionConfigOutputReference":
        return typing.cast("AlloydbInstanceClientConnectionConfigOutputReference", jsii.get(self, "clientConnectionConfig"))

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
    def machine_config(self) -> "AlloydbInstanceMachineConfigOutputReference":
        return typing.cast("AlloydbInstanceMachineConfigOutputReference", jsii.get(self, "machineConfig"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="networkConfig")
    def network_config(self) -> "AlloydbInstanceNetworkConfigOutputReference":
        return typing.cast("AlloydbInstanceNetworkConfigOutputReference", jsii.get(self, "networkConfig"))

    @builtins.property
    @jsii.member(jsii_name="outboundPublicIpAddresses")
    def outbound_public_ip_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "outboundPublicIpAddresses"))

    @builtins.property
    @jsii.member(jsii_name="pscInstanceConfig")
    def psc_instance_config(self) -> "AlloydbInstancePscInstanceConfigOutputReference":
        return typing.cast("AlloydbInstancePscInstanceConfigOutputReference", jsii.get(self, "pscInstanceConfig"))

    @builtins.property
    @jsii.member(jsii_name="publicIpAddress")
    def public_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicIpAddress"))

    @builtins.property
    @jsii.member(jsii_name="queryInsightsConfig")
    def query_insights_config(
        self,
    ) -> "AlloydbInstanceQueryInsightsConfigOutputReference":
        return typing.cast("AlloydbInstanceQueryInsightsConfigOutputReference", jsii.get(self, "queryInsightsConfig"))

    @builtins.property
    @jsii.member(jsii_name="readPoolConfig")
    def read_pool_config(self) -> "AlloydbInstanceReadPoolConfigOutputReference":
        return typing.cast("AlloydbInstanceReadPoolConfigOutputReference", jsii.get(self, "readPoolConfig"))

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
    def timeouts(self) -> "AlloydbInstanceTimeoutsOutputReference":
        return typing.cast("AlloydbInstanceTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["AlloydbInstanceClientConnectionConfig"]:
        return typing.cast(typing.Optional["AlloydbInstanceClientConnectionConfig"], jsii.get(self, "clientConnectionConfigInput"))

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
    def machine_config_input(self) -> typing.Optional["AlloydbInstanceMachineConfig"]:
        return typing.cast(typing.Optional["AlloydbInstanceMachineConfig"], jsii.get(self, "machineConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="networkConfigInput")
    def network_config_input(self) -> typing.Optional["AlloydbInstanceNetworkConfig"]:
        return typing.cast(typing.Optional["AlloydbInstanceNetworkConfig"], jsii.get(self, "networkConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="pscInstanceConfigInput")
    def psc_instance_config_input(
        self,
    ) -> typing.Optional["AlloydbInstancePscInstanceConfig"]:
        return typing.cast(typing.Optional["AlloydbInstancePscInstanceConfig"], jsii.get(self, "pscInstanceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInsightsConfigInput")
    def query_insights_config_input(
        self,
    ) -> typing.Optional["AlloydbInstanceQueryInsightsConfig"]:
        return typing.cast(typing.Optional["AlloydbInstanceQueryInsightsConfig"], jsii.get(self, "queryInsightsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="readPoolConfigInput")
    def read_pool_config_input(
        self,
    ) -> typing.Optional["AlloydbInstanceReadPoolConfig"]:
        return typing.cast(typing.Optional["AlloydbInstanceReadPoolConfig"], jsii.get(self, "readPoolConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AlloydbInstanceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AlloydbInstanceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="activationPolicy")
    def activation_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "activationPolicy"))

    @activation_policy.setter
    def activation_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcbd91aa833e3ff387bfb0362b0e275b81f9e5eb2e38bcb5e2d6c906db033e51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "activationPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fa1cb9979915aca6a7c4aeb57518b12a5796b6145a5a64a20ba7fde6e597550)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="availabilityType")
    def availability_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityType"))

    @availability_type.setter
    def availability_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__158158519d9a8a65f38719221803f22b0703d7bf76e9846762986111669a41d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cluster"))

    @cluster.setter
    def cluster(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c4285c5b746dd6b49221842687902a1fd16d86c5f3323aa1f9e75c04444ffc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cluster", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="databaseFlags")
    def database_flags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "databaseFlags"))

    @database_flags.setter
    def database_flags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69172a3afd4ec3ebb8d1e95baa8c35287c8e0a2d8aff61d978256916dbb9e08b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseFlags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03f69c08f4e371a59795390d38974db812ca5132568dcf7976bed28c0b7761d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gceZone")
    def gce_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gceZone"))

    @gce_zone.setter
    def gce_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__024692bb7172b732c32dabc7eac5e3e61c8080298ee96e5e59153d60827c2031)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gceZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69feb04cc37565f93b1e2458d4a895c9f64325b499b629c6f52332caa6d88db0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceId"))

    @instance_id.setter
    def instance_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__433ab37fe37b6a6f75557ec95ffd95c27cf82fd7cb300c5d18713c16ee888395)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0213d387b77d2f90108f9dfee31e87e4c0440368736dbabfbad6df49074010a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5277e02c8c1938057186ca3fe735c81944512c81f6a0d17e69f4c9a464d2fceb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.alloydbInstance.AlloydbInstanceClientConnectionConfig",
    jsii_struct_bases=[],
    name_mapping={
        "require_connectors": "requireConnectors",
        "ssl_config": "sslConfig",
    },
)
class AlloydbInstanceClientConnectionConfig:
    def __init__(
        self,
        *,
        require_connectors: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ssl_config: typing.Optional[typing.Union["AlloydbInstanceClientConnectionConfigSslConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param require_connectors: Configuration to enforce connectors only (ex: AuthProxy) connections to the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#require_connectors AlloydbInstance#require_connectors}
        :param ssl_config: ssl_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#ssl_config AlloydbInstance#ssl_config}
        '''
        if isinstance(ssl_config, dict):
            ssl_config = AlloydbInstanceClientConnectionConfigSslConfig(**ssl_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8cf4e7fd9312883106f38e965b6f54060f7ce32b2043d9968ca7d86c2e2b487)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#require_connectors AlloydbInstance#require_connectors}
        '''
        result = self._values.get("require_connectors")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ssl_config(
        self,
    ) -> typing.Optional["AlloydbInstanceClientConnectionConfigSslConfig"]:
        '''ssl_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#ssl_config AlloydbInstance#ssl_config}
        '''
        result = self._values.get("ssl_config")
        return typing.cast(typing.Optional["AlloydbInstanceClientConnectionConfigSslConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlloydbInstanceClientConnectionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlloydbInstanceClientConnectionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbInstance.AlloydbInstanceClientConnectionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f45f3fa540237ab457caad04b0826ce46338ae701b6b66d01f418530a29922cb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSslConfig")
    def put_ssl_config(self, *, ssl_mode: typing.Optional[builtins.str] = None) -> None:
        '''
        :param ssl_mode: SSL mode. Specifies client-server SSL/TLS connection behavior. Possible values: ["ENCRYPTED_ONLY", "ALLOW_UNENCRYPTED_AND_ENCRYPTED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#ssl_mode AlloydbInstance#ssl_mode}
        '''
        value = AlloydbInstanceClientConnectionConfigSslConfig(ssl_mode=ssl_mode)

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
    ) -> "AlloydbInstanceClientConnectionConfigSslConfigOutputReference":
        return typing.cast("AlloydbInstanceClientConnectionConfigSslConfigOutputReference", jsii.get(self, "sslConfig"))

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
    ) -> typing.Optional["AlloydbInstanceClientConnectionConfigSslConfig"]:
        return typing.cast(typing.Optional["AlloydbInstanceClientConnectionConfigSslConfig"], jsii.get(self, "sslConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__59cc790ab7c9a199a2d86467a57beb13493cbc0f5ef7dca7ab336db703bfd9f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireConnectors", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AlloydbInstanceClientConnectionConfig]:
        return typing.cast(typing.Optional[AlloydbInstanceClientConnectionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AlloydbInstanceClientConnectionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f5028740603fe89465277e145850b53f386ff7f7661ccc34890ec0840e23298)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.alloydbInstance.AlloydbInstanceClientConnectionConfigSslConfig",
    jsii_struct_bases=[],
    name_mapping={"ssl_mode": "sslMode"},
)
class AlloydbInstanceClientConnectionConfigSslConfig:
    def __init__(self, *, ssl_mode: typing.Optional[builtins.str] = None) -> None:
        '''
        :param ssl_mode: SSL mode. Specifies client-server SSL/TLS connection behavior. Possible values: ["ENCRYPTED_ONLY", "ALLOW_UNENCRYPTED_AND_ENCRYPTED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#ssl_mode AlloydbInstance#ssl_mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9509e0196f1879b9e4a4d1b9fd98dec123341426d77f54b5a080035ad36328ec)
            check_type(argname="argument ssl_mode", value=ssl_mode, expected_type=type_hints["ssl_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ssl_mode is not None:
            self._values["ssl_mode"] = ssl_mode

    @builtins.property
    def ssl_mode(self) -> typing.Optional[builtins.str]:
        '''SSL mode. Specifies client-server SSL/TLS connection behavior. Possible values: ["ENCRYPTED_ONLY", "ALLOW_UNENCRYPTED_AND_ENCRYPTED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#ssl_mode AlloydbInstance#ssl_mode}
        '''
        result = self._values.get("ssl_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlloydbInstanceClientConnectionConfigSslConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlloydbInstanceClientConnectionConfigSslConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbInstance.AlloydbInstanceClientConnectionConfigSslConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb5606c62ff21f7a076ea481599006d5aa15e8f13e9bfb156730daed4279af9b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1fe5cac698c5296141623e85a90745a2cf570a9b320ab954a8e37b37296d5eda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AlloydbInstanceClientConnectionConfigSslConfig]:
        return typing.cast(typing.Optional[AlloydbInstanceClientConnectionConfigSslConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AlloydbInstanceClientConnectionConfigSslConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76e1119e35a4d448d087a370283b9cecd1a465b23f29327f3bf20bc0265b861c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.alloydbInstance.AlloydbInstanceConfig",
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
        "psc_instance_config": "pscInstanceConfig",
        "query_insights_config": "queryInsightsConfig",
        "read_pool_config": "readPoolConfig",
        "timeouts": "timeouts",
    },
)
class AlloydbInstanceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        client_connection_config: typing.Optional[typing.Union[AlloydbInstanceClientConnectionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        database_flags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        display_name: typing.Optional[builtins.str] = None,
        gce_zone: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        machine_config: typing.Optional[typing.Union["AlloydbInstanceMachineConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        network_config: typing.Optional[typing.Union["AlloydbInstanceNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        psc_instance_config: typing.Optional[typing.Union["AlloydbInstancePscInstanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        query_insights_config: typing.Optional[typing.Union["AlloydbInstanceQueryInsightsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        read_pool_config: typing.Optional[typing.Union["AlloydbInstanceReadPoolConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["AlloydbInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cluster: Identifies the alloydb cluster. Must be in the format 'projects/{project}/locations/{location}/clusters/{cluster_id}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#cluster AlloydbInstance#cluster}
        :param instance_id: The ID of the alloydb instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#instance_id AlloydbInstance#instance_id}
        :param instance_type: The type of the instance. If the instance type is READ_POOL, provide the associated PRIMARY/SECONDARY instance in the 'depends_on' meta-data attribute. If the instance type is SECONDARY, point to the cluster_type of the associated secondary cluster instead of mentioning SECONDARY. Example: {instance_type = google_alloydb_cluster.<secondary_cluster_name>.cluster_type} instead of {instance_type = SECONDARY} If the instance type is SECONDARY, the terraform delete instance operation does not delete the secondary instance but abandons it instead. Use deletion_policy = "FORCE" in the associated secondary cluster and delete the cluster forcefully to delete the secondary cluster as well its associated secondary instance. Users can undo the delete secondary instance action by importing the deleted secondary instance by calling terraform import. Possible values: ["PRIMARY", "READ_POOL", "SECONDARY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#instance_type AlloydbInstance#instance_type}
        :param activation_policy: 'Specifies whether an instance needs to spin up. Once the instance is active, the activation policy can be updated to the 'NEVER' to stop the instance. Likewise, the activation policy can be updated to 'ALWAYS' to start the instance. There are restrictions around when an instance can/cannot be activated (for example, a read pool instance should be stopped before stopping primary etc.). Please refer to the API documentation for more details. Possible values are: 'ACTIVATION_POLICY_UNSPECIFIED', 'ALWAYS', 'NEVER'.' Possible values: ["ACTIVATION_POLICY_UNSPECIFIED", "ALWAYS", "NEVER"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#activation_policy AlloydbInstance#activation_policy}
        :param annotations: Annotations to allow client tools to store small amount of arbitrary data. This is distinct from labels. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#annotations AlloydbInstance#annotations}
        :param availability_type: 'Availability type of an Instance. Defaults to REGIONAL for both primary and read instances. Note that primary and read instances can have different availability types. Primary instances can be either ZONAL or REGIONAL. Read Pool instances can also be either ZONAL or REGIONAL. Read pools of size 1 can only have zonal availability. Read pools with a node count of 2 or more can have regional availability (nodes are present in 2 or more zones in a region). Possible values are: 'AVAILABILITY_TYPE_UNSPECIFIED', 'ZONAL', 'REGIONAL'.' Possible values: ["AVAILABILITY_TYPE_UNSPECIFIED", "ZONAL", "REGIONAL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#availability_type AlloydbInstance#availability_type}
        :param client_connection_config: client_connection_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#client_connection_config AlloydbInstance#client_connection_config}
        :param database_flags: Database flags. Set at instance level. * They are copied from primary instance on read instance creation. * Read instances can set new or override existing flags that are relevant for reads, e.g. for enabling columnar cache on a read instance. Flags set on read instance may or may not be present on primary. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#database_flags AlloydbInstance#database_flags}
        :param display_name: User-settable and human-readable display name for the Instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#display_name AlloydbInstance#display_name}
        :param gce_zone: The Compute Engine zone that the instance should serve from, per https://cloud.google.com/compute/docs/regions-zones This can ONLY be specified for ZONAL instances. If present for a REGIONAL instance, an error will be thrown. If this is absent for a ZONAL instance, instance is created in a random zone with available capacity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#gce_zone AlloydbInstance#gce_zone}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#id AlloydbInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: User-defined labels for the alloydb instance. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#labels AlloydbInstance#labels}
        :param machine_config: machine_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#machine_config AlloydbInstance#machine_config}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#network_config AlloydbInstance#network_config}
        :param psc_instance_config: psc_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#psc_instance_config AlloydbInstance#psc_instance_config}
        :param query_insights_config: query_insights_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#query_insights_config AlloydbInstance#query_insights_config}
        :param read_pool_config: read_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#read_pool_config AlloydbInstance#read_pool_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#timeouts AlloydbInstance#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(client_connection_config, dict):
            client_connection_config = AlloydbInstanceClientConnectionConfig(**client_connection_config)
        if isinstance(machine_config, dict):
            machine_config = AlloydbInstanceMachineConfig(**machine_config)
        if isinstance(network_config, dict):
            network_config = AlloydbInstanceNetworkConfig(**network_config)
        if isinstance(psc_instance_config, dict):
            psc_instance_config = AlloydbInstancePscInstanceConfig(**psc_instance_config)
        if isinstance(query_insights_config, dict):
            query_insights_config = AlloydbInstanceQueryInsightsConfig(**query_insights_config)
        if isinstance(read_pool_config, dict):
            read_pool_config = AlloydbInstanceReadPoolConfig(**read_pool_config)
        if isinstance(timeouts, dict):
            timeouts = AlloydbInstanceTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1513728bf9a692ea14e578c6e8e3ebe350a5703568d9faa6685c56af4afcaf1)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#cluster AlloydbInstance#cluster}
        '''
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def instance_id(self) -> builtins.str:
        '''The ID of the alloydb instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#instance_id AlloydbInstance#instance_id}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#instance_type AlloydbInstance#instance_type}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#activation_policy AlloydbInstance#activation_policy}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#annotations AlloydbInstance#annotations}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#availability_type AlloydbInstance#availability_type}
        '''
        result = self._values.get("availability_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_connection_config(
        self,
    ) -> typing.Optional[AlloydbInstanceClientConnectionConfig]:
        '''client_connection_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#client_connection_config AlloydbInstance#client_connection_config}
        '''
        result = self._values.get("client_connection_config")
        return typing.cast(typing.Optional[AlloydbInstanceClientConnectionConfig], result)

    @builtins.property
    def database_flags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Database flags.

        Set at instance level. * They are copied from primary instance on read instance creation. * Read instances can set new or override existing flags that are relevant for reads, e.g. for enabling columnar cache on a read instance. Flags set on read instance may or may not be present on primary.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#database_flags AlloydbInstance#database_flags}
        '''
        result = self._values.get("database_flags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''User-settable and human-readable display name for the Instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#display_name AlloydbInstance#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gce_zone(self) -> typing.Optional[builtins.str]:
        '''The Compute Engine zone that the instance should serve from, per https://cloud.google.com/compute/docs/regions-zones This can ONLY be specified for ZONAL instances. If present for a REGIONAL instance, an error will be thrown. If this is absent for a ZONAL instance, instance is created in a random zone with available capacity.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#gce_zone AlloydbInstance#gce_zone}
        '''
        result = self._values.get("gce_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#id AlloydbInstance#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#labels AlloydbInstance#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def machine_config(self) -> typing.Optional["AlloydbInstanceMachineConfig"]:
        '''machine_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#machine_config AlloydbInstance#machine_config}
        '''
        result = self._values.get("machine_config")
        return typing.cast(typing.Optional["AlloydbInstanceMachineConfig"], result)

    @builtins.property
    def network_config(self) -> typing.Optional["AlloydbInstanceNetworkConfig"]:
        '''network_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#network_config AlloydbInstance#network_config}
        '''
        result = self._values.get("network_config")
        return typing.cast(typing.Optional["AlloydbInstanceNetworkConfig"], result)

    @builtins.property
    def psc_instance_config(
        self,
    ) -> typing.Optional["AlloydbInstancePscInstanceConfig"]:
        '''psc_instance_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#psc_instance_config AlloydbInstance#psc_instance_config}
        '''
        result = self._values.get("psc_instance_config")
        return typing.cast(typing.Optional["AlloydbInstancePscInstanceConfig"], result)

    @builtins.property
    def query_insights_config(
        self,
    ) -> typing.Optional["AlloydbInstanceQueryInsightsConfig"]:
        '''query_insights_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#query_insights_config AlloydbInstance#query_insights_config}
        '''
        result = self._values.get("query_insights_config")
        return typing.cast(typing.Optional["AlloydbInstanceQueryInsightsConfig"], result)

    @builtins.property
    def read_pool_config(self) -> typing.Optional["AlloydbInstanceReadPoolConfig"]:
        '''read_pool_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#read_pool_config AlloydbInstance#read_pool_config}
        '''
        result = self._values.get("read_pool_config")
        return typing.cast(typing.Optional["AlloydbInstanceReadPoolConfig"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["AlloydbInstanceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#timeouts AlloydbInstance#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["AlloydbInstanceTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlloydbInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.alloydbInstance.AlloydbInstanceMachineConfig",
    jsii_struct_bases=[],
    name_mapping={"cpu_count": "cpuCount", "machine_type": "machineType"},
)
class AlloydbInstanceMachineConfig:
    def __init__(
        self,
        *,
        cpu_count: typing.Optional[jsii.Number] = None,
        machine_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cpu_count: The number of CPU's in the VM instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#cpu_count AlloydbInstance#cpu_count}
        :param machine_type: Machine type of the VM instance. E.g. "n2-highmem-4", "n2-highmem-8", "c4a-highmem-4-lssd". 'cpu_count' must match the number of vCPUs in the machine type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#machine_type AlloydbInstance#machine_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae1c69322f6ed0426aaab238f3d6fe1f33698bd608cd1b6534450a776dc51bff)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#cpu_count AlloydbInstance#cpu_count}
        '''
        result = self._values.get("cpu_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def machine_type(self) -> typing.Optional[builtins.str]:
        '''Machine type of the VM instance. E.g. "n2-highmem-4", "n2-highmem-8", "c4a-highmem-4-lssd". 'cpu_count' must match the number of vCPUs in the machine type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#machine_type AlloydbInstance#machine_type}
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlloydbInstanceMachineConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlloydbInstanceMachineConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbInstance.AlloydbInstanceMachineConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6339a3d89e0aecd8dda776b93a80b321f950a484556e4d01594e51837d60162)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a73e48c2e41ed071faf47c52884932f4bb7b8df932fdcf4e7395f28e4feb33db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a074af488c75eeaddc22652fc84ca4936518e72b46fc56a96e273b7dcb1792c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AlloydbInstanceMachineConfig]:
        return typing.cast(typing.Optional[AlloydbInstanceMachineConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AlloydbInstanceMachineConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b49f69a9f7a02d3d4fc15faefa62a4fbe7a3cf1ccf6ce27dfa4ef3830ee6608d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.alloydbInstance.AlloydbInstanceNetworkConfig",
    jsii_struct_bases=[],
    name_mapping={
        "allocated_ip_range_override": "allocatedIpRangeOverride",
        "authorized_external_networks": "authorizedExternalNetworks",
        "enable_outbound_public_ip": "enableOutboundPublicIp",
        "enable_public_ip": "enablePublicIp",
    },
)
class AlloydbInstanceNetworkConfig:
    def __init__(
        self,
        *,
        allocated_ip_range_override: typing.Optional[builtins.str] = None,
        authorized_external_networks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AlloydbInstanceNetworkConfigAuthorizedExternalNetworks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        enable_outbound_public_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_public_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param allocated_ip_range_override: Name of the allocated IP range for the private IP AlloyDB instance, for example: "google-managed-services-default". If set, the instance IPs will be created from this allocated range and will override the IP range used by the parent cluster. The range name must comply with RFC 1035. Specifically, the name must be 1-63 characters long and match the regular expression `a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#allocated_ip_range_override AlloydbInstance#allocated_ip_range_override}
        :param authorized_external_networks: authorized_external_networks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#authorized_external_networks AlloydbInstance#authorized_external_networks}
        :param enable_outbound_public_ip: Enabling outbound public ip for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#enable_outbound_public_ip AlloydbInstance#enable_outbound_public_ip}
        :param enable_public_ip: Enabling public ip for the instance. If a user wishes to disable this, please also clear the list of the authorized external networks set on the same instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#enable_public_ip AlloydbInstance#enable_public_ip}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6eecabd9d2c04d20ddd9d7322d2e3278a6a5aaa482f391eb25d644abf1681f11)
            check_type(argname="argument allocated_ip_range_override", value=allocated_ip_range_override, expected_type=type_hints["allocated_ip_range_override"])
            check_type(argname="argument authorized_external_networks", value=authorized_external_networks, expected_type=type_hints["authorized_external_networks"])
            check_type(argname="argument enable_outbound_public_ip", value=enable_outbound_public_ip, expected_type=type_hints["enable_outbound_public_ip"])
            check_type(argname="argument enable_public_ip", value=enable_public_ip, expected_type=type_hints["enable_public_ip"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allocated_ip_range_override is not None:
            self._values["allocated_ip_range_override"] = allocated_ip_range_override
        if authorized_external_networks is not None:
            self._values["authorized_external_networks"] = authorized_external_networks
        if enable_outbound_public_ip is not None:
            self._values["enable_outbound_public_ip"] = enable_outbound_public_ip
        if enable_public_ip is not None:
            self._values["enable_public_ip"] = enable_public_ip

    @builtins.property
    def allocated_ip_range_override(self) -> typing.Optional[builtins.str]:
        '''Name of the allocated IP range for the private IP AlloyDB instance, for example: "google-managed-services-default".

        If set, the instance IPs will be created from this allocated range and will override the IP range used by the parent cluster.
        The range name must comply with RFC 1035. Specifically, the name must be 1-63 characters long and match the regular expression `a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#allocated_ip_range_override AlloydbInstance#allocated_ip_range_override}
        '''
        result = self._values.get("allocated_ip_range_override")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authorized_external_networks(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AlloydbInstanceNetworkConfigAuthorizedExternalNetworks"]]]:
        '''authorized_external_networks block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#authorized_external_networks AlloydbInstance#authorized_external_networks}
        '''
        result = self._values.get("authorized_external_networks")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AlloydbInstanceNetworkConfigAuthorizedExternalNetworks"]]], result)

    @builtins.property
    def enable_outbound_public_ip(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enabling outbound public ip for the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#enable_outbound_public_ip AlloydbInstance#enable_outbound_public_ip}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#enable_public_ip AlloydbInstance#enable_public_ip}
        '''
        result = self._values.get("enable_public_ip")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlloydbInstanceNetworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.alloydbInstance.AlloydbInstanceNetworkConfigAuthorizedExternalNetworks",
    jsii_struct_bases=[],
    name_mapping={"cidr_range": "cidrRange"},
)
class AlloydbInstanceNetworkConfigAuthorizedExternalNetworks:
    def __init__(self, *, cidr_range: typing.Optional[builtins.str] = None) -> None:
        '''
        :param cidr_range: CIDR range for one authorized network of the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#cidr_range AlloydbInstance#cidr_range}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3784bfe776a85fa93558af5d9a850a6d96b5e3a19e8929aacbc1e7fe2be7bb0)
            check_type(argname="argument cidr_range", value=cidr_range, expected_type=type_hints["cidr_range"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cidr_range is not None:
            self._values["cidr_range"] = cidr_range

    @builtins.property
    def cidr_range(self) -> typing.Optional[builtins.str]:
        '''CIDR range for one authorized network of the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#cidr_range AlloydbInstance#cidr_range}
        '''
        result = self._values.get("cidr_range")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlloydbInstanceNetworkConfigAuthorizedExternalNetworks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlloydbInstanceNetworkConfigAuthorizedExternalNetworksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbInstance.AlloydbInstanceNetworkConfigAuthorizedExternalNetworksList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8aed019e5283472c93ff082b0f11341ed76d73382622f6371ac5490164875de9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AlloydbInstanceNetworkConfigAuthorizedExternalNetworksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f19b72da21f8e7c8e9417197574fd6e38dabf502c5f15de25f93dfefa2195cbc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AlloydbInstanceNetworkConfigAuthorizedExternalNetworksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__192c29b627674d0274b93ee83081b810983d1b91e1b6a209c8fefb2d101c6605)
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
            type_hints = typing.get_type_hints(_typecheckingstub__353ac5f9aed9fa57cedcc26aa66bc26dac683f55eb3a8c797702b7df92d01892)
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
            type_hints = typing.get_type_hints(_typecheckingstub__847b66deab62f32a029d23c88deda974c8ab5ed73d896d6e70af4bc1527173a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AlloydbInstanceNetworkConfigAuthorizedExternalNetworks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AlloydbInstanceNetworkConfigAuthorizedExternalNetworks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AlloydbInstanceNetworkConfigAuthorizedExternalNetworks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0347d674562f47c8b2d9ad6d57916b8e43c1b38354b67aa78fffe565dda2688)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AlloydbInstanceNetworkConfigAuthorizedExternalNetworksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbInstance.AlloydbInstanceNetworkConfigAuthorizedExternalNetworksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e79fca9d3e9b7a5cf151dd2d57d273d760ec37c78a9df537a1d56dca6cdd70d4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b6caacef85cf55a2c3d1dde8034169f0f28a79de619a4a93949dede0606bbc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cidrRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlloydbInstanceNetworkConfigAuthorizedExternalNetworks]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlloydbInstanceNetworkConfigAuthorizedExternalNetworks]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlloydbInstanceNetworkConfigAuthorizedExternalNetworks]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44122d1a2b1185165339d32ece78917b02ed2df48517e89078f6bd5d65ab5a8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AlloydbInstanceNetworkConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbInstance.AlloydbInstanceNetworkConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6557aea470173be0ee74c5d53a80cfbbf4a48450debd4b8ab11fb37d2597f2ac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAuthorizedExternalNetworks")
    def put_authorized_external_networks(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AlloydbInstanceNetworkConfigAuthorizedExternalNetworks, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1432945e93ad9dfb53e0d27e6fd450dba70b4e06483c8cc1b1b1e63d3c8fd43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAuthorizedExternalNetworks", [value]))

    @jsii.member(jsii_name="resetAllocatedIpRangeOverride")
    def reset_allocated_ip_range_override(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllocatedIpRangeOverride", []))

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
    ) -> AlloydbInstanceNetworkConfigAuthorizedExternalNetworksList:
        return typing.cast(AlloydbInstanceNetworkConfigAuthorizedExternalNetworksList, jsii.get(self, "authorizedExternalNetworks"))

    @builtins.property
    @jsii.member(jsii_name="allocatedIpRangeOverrideInput")
    def allocated_ip_range_override_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "allocatedIpRangeOverrideInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizedExternalNetworksInput")
    def authorized_external_networks_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AlloydbInstanceNetworkConfigAuthorizedExternalNetworks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AlloydbInstanceNetworkConfigAuthorizedExternalNetworks]]], jsii.get(self, "authorizedExternalNetworksInput"))

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
    @jsii.member(jsii_name="allocatedIpRangeOverride")
    def allocated_ip_range_override(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "allocatedIpRangeOverride"))

    @allocated_ip_range_override.setter
    def allocated_ip_range_override(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__318561c5b7fb47e6466452c5ad51f7fb09a5d24caaf10c8562661fec52f06400)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allocatedIpRangeOverride", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__d9fc1a7c0d3bd776af4fc8f5185c2793f7edd817a0c418b9f3d91b0f95dc4777)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ec8146c7152b49cd1ae7fb8926f7e46bf60e1d3f41d38648970534713ec52bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enablePublicIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AlloydbInstanceNetworkConfig]:
        return typing.cast(typing.Optional[AlloydbInstanceNetworkConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AlloydbInstanceNetworkConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__922492357c21ad1176212bc39725d910c1fef2127b9f4a692ef39ea302e0c600)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.alloydbInstance.AlloydbInstancePscInstanceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_consumer_projects": "allowedConsumerProjects",
        "psc_auto_connections": "pscAutoConnections",
        "psc_interface_configs": "pscInterfaceConfigs",
    },
)
class AlloydbInstancePscInstanceConfig:
    def __init__(
        self,
        *,
        allowed_consumer_projects: typing.Optional[typing.Sequence[builtins.str]] = None,
        psc_auto_connections: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AlloydbInstancePscInstanceConfigPscAutoConnections", typing.Dict[builtins.str, typing.Any]]]]] = None,
        psc_interface_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AlloydbInstancePscInstanceConfigPscInterfaceConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param allowed_consumer_projects: List of consumer projects that are allowed to create PSC endpoints to service-attachments to this instance. These should be specified as project numbers only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#allowed_consumer_projects AlloydbInstance#allowed_consumer_projects}
        :param psc_auto_connections: psc_auto_connections block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#psc_auto_connections AlloydbInstance#psc_auto_connections}
        :param psc_interface_configs: psc_interface_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#psc_interface_configs AlloydbInstance#psc_interface_configs}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed01939214ec7982de1702bb73956902464e28a8c57942d8700db33826bd15b0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#allowed_consumer_projects AlloydbInstance#allowed_consumer_projects}
        '''
        result = self._values.get("allowed_consumer_projects")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def psc_auto_connections(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AlloydbInstancePscInstanceConfigPscAutoConnections"]]]:
        '''psc_auto_connections block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#psc_auto_connections AlloydbInstance#psc_auto_connections}
        '''
        result = self._values.get("psc_auto_connections")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AlloydbInstancePscInstanceConfigPscAutoConnections"]]], result)

    @builtins.property
    def psc_interface_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AlloydbInstancePscInstanceConfigPscInterfaceConfigs"]]]:
        '''psc_interface_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#psc_interface_configs AlloydbInstance#psc_interface_configs}
        '''
        result = self._values.get("psc_interface_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AlloydbInstancePscInstanceConfigPscInterfaceConfigs"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlloydbInstancePscInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlloydbInstancePscInstanceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbInstance.AlloydbInstancePscInstanceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__66cabee8086cfff6312cd2acb396083f5376701e8fc44ef3b3644fb53adbeace)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPscAutoConnections")
    def put_psc_auto_connections(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AlloydbInstancePscInstanceConfigPscAutoConnections", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a004420241717cbaea176e50a2f9dd3a3f4b373b91b6704f7e7a8e06f6cef39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPscAutoConnections", [value]))

    @jsii.member(jsii_name="putPscInterfaceConfigs")
    def put_psc_interface_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AlloydbInstancePscInstanceConfigPscInterfaceConfigs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9050edb31663e07f92acad137800e71a77bef37c2f1dae17d5e437e1a8bfcb33)
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
    ) -> "AlloydbInstancePscInstanceConfigPscAutoConnectionsList":
        return typing.cast("AlloydbInstancePscInstanceConfigPscAutoConnectionsList", jsii.get(self, "pscAutoConnections"))

    @builtins.property
    @jsii.member(jsii_name="pscDnsName")
    def psc_dns_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pscDnsName"))

    @builtins.property
    @jsii.member(jsii_name="pscInterfaceConfigs")
    def psc_interface_configs(
        self,
    ) -> "AlloydbInstancePscInstanceConfigPscInterfaceConfigsList":
        return typing.cast("AlloydbInstancePscInstanceConfigPscInterfaceConfigsList", jsii.get(self, "pscInterfaceConfigs"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AlloydbInstancePscInstanceConfigPscAutoConnections"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AlloydbInstancePscInstanceConfigPscAutoConnections"]]], jsii.get(self, "pscAutoConnectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="pscInterfaceConfigsInput")
    def psc_interface_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AlloydbInstancePscInstanceConfigPscInterfaceConfigs"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AlloydbInstancePscInstanceConfigPscInterfaceConfigs"]]], jsii.get(self, "pscInterfaceConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedConsumerProjects")
    def allowed_consumer_projects(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedConsumerProjects"))

    @allowed_consumer_projects.setter
    def allowed_consumer_projects(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75943cfab2ffea034237a64a7cc65f1b4f9d6e04bed087cced9852ad801db81a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedConsumerProjects", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AlloydbInstancePscInstanceConfig]:
        return typing.cast(typing.Optional[AlloydbInstancePscInstanceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AlloydbInstancePscInstanceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5968fe42e8749bf702f5e39c8668d3a1ef40f4a50037354372a6ecb9a57823eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.alloydbInstance.AlloydbInstancePscInstanceConfigPscAutoConnections",
    jsii_struct_bases=[],
    name_mapping={
        "consumer_network": "consumerNetwork",
        "consumer_project": "consumerProject",
    },
)
class AlloydbInstancePscInstanceConfigPscAutoConnections:
    def __init__(
        self,
        *,
        consumer_network: typing.Optional[builtins.str] = None,
        consumer_project: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param consumer_network: The consumer network for the PSC service automation, example: "projects/vpc-host-project/global/networks/default". The consumer network might be hosted a different project than the consumer project. The API expects the consumer project specified to be the project ID (and not the project number) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#consumer_network AlloydbInstance#consumer_network}
        :param consumer_project: The consumer project to which the PSC service automation endpoint will be created. The API expects the consumer project to be the project ID( and not the project number). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#consumer_project AlloydbInstance#consumer_project}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cab12810f4611fd34c372738888694d8b2321eaf8a5df8b4b8537241315c4d54)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#consumer_network AlloydbInstance#consumer_network}
        '''
        result = self._values.get("consumer_network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def consumer_project(self) -> typing.Optional[builtins.str]:
        '''The consumer project to which the PSC service automation endpoint will be created.

        The API expects the consumer project to be the project ID(
        and not the project number).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#consumer_project AlloydbInstance#consumer_project}
        '''
        result = self._values.get("consumer_project")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlloydbInstancePscInstanceConfigPscAutoConnections(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlloydbInstancePscInstanceConfigPscAutoConnectionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbInstance.AlloydbInstancePscInstanceConfigPscAutoConnectionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98ce8f280ec60b4fd289e7d3317cf8f5a72efe15709382539b5fc0b89d8c44aa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AlloydbInstancePscInstanceConfigPscAutoConnectionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c27898a098ffcffae543345be98294f00896a7fd8387c6f12ad8b31204bd2d5c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AlloydbInstancePscInstanceConfigPscAutoConnectionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f37640c5d28c5e91606d17109aceca4eb14174ea31fb32e899ba5a397bcec918)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2473528ec53df4a4c8304fba8062d02649cce2ccb3b87da7c6ab1634fe7c0526)
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
            type_hints = typing.get_type_hints(_typecheckingstub__80d1ab6fd9b6b5e4341c46361e88fe9e3c3d1eaf1f882b09532eb6aad0d18886)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AlloydbInstancePscInstanceConfigPscAutoConnections]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AlloydbInstancePscInstanceConfigPscAutoConnections]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AlloydbInstancePscInstanceConfigPscAutoConnections]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4df3f29b02b9638ed66b1f05be2f4e70090a1a251664d636ae2c58c9741d3219)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AlloydbInstancePscInstanceConfigPscAutoConnectionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbInstance.AlloydbInstancePscInstanceConfigPscAutoConnectionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3fd1fd48b9b01f7e129154e203bc6a7ac2ecda7b11fa7706afc8d55fa808a01f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__96458f55fbc9839019de64cdfa1675115777eb3020029d5fc13fd211810b0d12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerNetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="consumerProject")
    def consumer_project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerProject"))

    @consumer_project.setter
    def consumer_project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98e39d20df1215eac1a6cc742b8d9b61a698397118624063dfa37ebe273be8d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerProject", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlloydbInstancePscInstanceConfigPscAutoConnections]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlloydbInstancePscInstanceConfigPscAutoConnections]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlloydbInstancePscInstanceConfigPscAutoConnections]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bf28ffa1c1cade4b27e16989121f6e31ba91b36c2428acc2af12600f2e420a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.alloydbInstance.AlloydbInstancePscInstanceConfigPscInterfaceConfigs",
    jsii_struct_bases=[],
    name_mapping={"network_attachment_resource": "networkAttachmentResource"},
)
class AlloydbInstancePscInstanceConfigPscInterfaceConfigs:
    def __init__(
        self,
        *,
        network_attachment_resource: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param network_attachment_resource: The network attachment resource created in the consumer project to which the PSC interface will be linked. This is of the format: "projects/${CONSUMER_PROJECT}/regions/${REGION}/networkAttachments/${NETWORK_ATTACHMENT_NAME}". The network attachment must be in the same region as the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#network_attachment_resource AlloydbInstance#network_attachment_resource}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7f9d6b9349983c71632c804c0d44a52b4d10d40076e1f08ee9c44f3f5f02511)
            check_type(argname="argument network_attachment_resource", value=network_attachment_resource, expected_type=type_hints["network_attachment_resource"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if network_attachment_resource is not None:
            self._values["network_attachment_resource"] = network_attachment_resource

    @builtins.property
    def network_attachment_resource(self) -> typing.Optional[builtins.str]:
        '''The network attachment resource created in the consumer project to which the PSC interface will be linked.

        This is of the format: "projects/${CONSUMER_PROJECT}/regions/${REGION}/networkAttachments/${NETWORK_ATTACHMENT_NAME}".
        The network attachment must be in the same region as the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#network_attachment_resource AlloydbInstance#network_attachment_resource}
        '''
        result = self._values.get("network_attachment_resource")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlloydbInstancePscInstanceConfigPscInterfaceConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlloydbInstancePscInstanceConfigPscInterfaceConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbInstance.AlloydbInstancePscInstanceConfigPscInterfaceConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c464a41188ee4de2e2b0d0599b658652c21d576b948daab5ff6ff6be36e6bef7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AlloydbInstancePscInstanceConfigPscInterfaceConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0bb38b8677d579681c15c9ffb6192779f34141d58deae2b9b1f6acf52926da7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AlloydbInstancePscInstanceConfigPscInterfaceConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79080c0ed944188c78941a0fbd86de7ffa8804f4a621c8dbb2db90446f18aa8f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__40fd665e3343cfe22fba39daf224932715d0fb081a184289dcdfd640a5621a3a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__efbde442ed9a33ef70a7d5b4f68e4d594d4bb9003a4282fe0cec4001799dd564)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AlloydbInstancePscInstanceConfigPscInterfaceConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AlloydbInstancePscInstanceConfigPscInterfaceConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AlloydbInstancePscInstanceConfigPscInterfaceConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a1e2b436f82f8d32290cf84d98fb71d1b76dc22c8c0f5d07739a1787bdde48b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AlloydbInstancePscInstanceConfigPscInterfaceConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbInstance.AlloydbInstancePscInstanceConfigPscInterfaceConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eaca7f72b3eab7e8b9aee8f190d07d58c4c540bdb7c7416c7fd521411476c2a7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c991ba6ddbe69636a548663c1dc969f65cd8188b4a0aff3e68aac71b3208ab64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkAttachmentResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlloydbInstancePscInstanceConfigPscInterfaceConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlloydbInstancePscInstanceConfigPscInterfaceConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlloydbInstancePscInstanceConfigPscInterfaceConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83867f37475c48b67b49064a490edf15b7fe0105a12d085cf2360f9b0c395dfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.alloydbInstance.AlloydbInstanceQueryInsightsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "query_plans_per_minute": "queryPlansPerMinute",
        "query_string_length": "queryStringLength",
        "record_application_tags": "recordApplicationTags",
        "record_client_address": "recordClientAddress",
    },
)
class AlloydbInstanceQueryInsightsConfig:
    def __init__(
        self,
        *,
        query_plans_per_minute: typing.Optional[jsii.Number] = None,
        query_string_length: typing.Optional[jsii.Number] = None,
        record_application_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        record_client_address: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param query_plans_per_minute: Number of query execution plans captured by Insights per minute for all queries combined. The default value is 5. Any integer between 0 and 20 is considered valid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#query_plans_per_minute AlloydbInstance#query_plans_per_minute}
        :param query_string_length: Query string length. The default value is 1024. Any integer between 256 and 4500 is considered valid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#query_string_length AlloydbInstance#query_string_length}
        :param record_application_tags: Record application tags for an instance. This flag is turned "on" by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#record_application_tags AlloydbInstance#record_application_tags}
        :param record_client_address: Record client address for an instance. Client address is PII information. This flag is turned "on" by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#record_client_address AlloydbInstance#record_client_address}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d686258b4296fd9a11b228dfe1b794eee03b038e7d0d9e8375e0acd583b5e1f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#query_plans_per_minute AlloydbInstance#query_plans_per_minute}
        '''
        result = self._values.get("query_plans_per_minute")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def query_string_length(self) -> typing.Optional[jsii.Number]:
        '''Query string length. The default value is 1024. Any integer between 256 and 4500 is considered valid.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#query_string_length AlloydbInstance#query_string_length}
        '''
        result = self._values.get("query_string_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def record_application_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Record application tags for an instance. This flag is turned "on" by default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#record_application_tags AlloydbInstance#record_application_tags}
        '''
        result = self._values.get("record_application_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def record_client_address(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Record client address for an instance. Client address is PII information. This flag is turned "on" by default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#record_client_address AlloydbInstance#record_client_address}
        '''
        result = self._values.get("record_client_address")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlloydbInstanceQueryInsightsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlloydbInstanceQueryInsightsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbInstance.AlloydbInstanceQueryInsightsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c3081d80b5ac08445d9e276af8b24ec751a115ced26fa32ed501647df359ed2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdc2465597128c53ed48b45d8e804dc3c8c5f446817cf58627e74746d302c749)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryPlansPerMinute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryStringLength")
    def query_string_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "queryStringLength"))

    @query_string_length.setter
    def query_string_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b8e0d10d517a751a5e22e8db495c766b4b70570c31baf7ce30a0106c9c27809)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8268d229a554e88fde1336ac3c2cb167b77417013e27c1c647b5f287224f1876)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3242ac241e5195487a9a12ca8ae575c6192cbc9bc7f971c4bbed53d6bce766f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recordClientAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AlloydbInstanceQueryInsightsConfig]:
        return typing.cast(typing.Optional[AlloydbInstanceQueryInsightsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AlloydbInstanceQueryInsightsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca12cbb111540303c875c4559a422153cf7c73f3e6bb6201f881ba29f139069d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.alloydbInstance.AlloydbInstanceReadPoolConfig",
    jsii_struct_bases=[],
    name_mapping={"node_count": "nodeCount"},
)
class AlloydbInstanceReadPoolConfig:
    def __init__(self, *, node_count: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param node_count: Read capacity, i.e. number of nodes in a read pool instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#node_count AlloydbInstance#node_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0120a17d019867a39bdd1b37caa4ef3d6a7460620cc4588de9d2820ae166113a)
            check_type(argname="argument node_count", value=node_count, expected_type=type_hints["node_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if node_count is not None:
            self._values["node_count"] = node_count

    @builtins.property
    def node_count(self) -> typing.Optional[jsii.Number]:
        '''Read capacity, i.e. number of nodes in a read pool instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#node_count AlloydbInstance#node_count}
        '''
        result = self._values.get("node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlloydbInstanceReadPoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlloydbInstanceReadPoolConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbInstance.AlloydbInstanceReadPoolConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e556805238a67471d3893e5fabd42872956bcc68346527e15a946ed38ea27f2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__943318cc25fb6c6992d481fdae72284609c691c58f76ded639cbccc4eddb93fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AlloydbInstanceReadPoolConfig]:
        return typing.cast(typing.Optional[AlloydbInstanceReadPoolConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AlloydbInstanceReadPoolConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6158543947f4bc9fb14030f6c3aaeba07c43666ce7eccae912e026c2bf388738)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.alloydbInstance.AlloydbInstanceTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class AlloydbInstanceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#create AlloydbInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#delete AlloydbInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#update AlloydbInstance#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92852fd79f1a1c5827f4e08118e4b8d1230621d12ab5bd3224b75cd3a0aaedcf)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#create AlloydbInstance#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#delete AlloydbInstance#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_instance#update AlloydbInstance#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlloydbInstanceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlloydbInstanceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbInstance.AlloydbInstanceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af5cb81b3713f5486b0336541822b32c4dc250b959e4d0761a8ece4d1424ab7b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c95905f4e90d8f66e9d258da3dd09b81de67433dfda03e0b62f593f3bd3be278)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb9ef26d489259d7ed73010fb95d0e8fc45a13cd5be617b6a48a9313552f080a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca4553895f681f42dbf738f23a4e7a1f384184393c04956dbaee1f6706db8e21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlloydbInstanceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlloydbInstanceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlloydbInstanceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc17f01754fc0647c4f612b32f9e93a7061cac0a49fbf4f69e833d262c586c39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AlloydbInstance",
    "AlloydbInstanceClientConnectionConfig",
    "AlloydbInstanceClientConnectionConfigOutputReference",
    "AlloydbInstanceClientConnectionConfigSslConfig",
    "AlloydbInstanceClientConnectionConfigSslConfigOutputReference",
    "AlloydbInstanceConfig",
    "AlloydbInstanceMachineConfig",
    "AlloydbInstanceMachineConfigOutputReference",
    "AlloydbInstanceNetworkConfig",
    "AlloydbInstanceNetworkConfigAuthorizedExternalNetworks",
    "AlloydbInstanceNetworkConfigAuthorizedExternalNetworksList",
    "AlloydbInstanceNetworkConfigAuthorizedExternalNetworksOutputReference",
    "AlloydbInstanceNetworkConfigOutputReference",
    "AlloydbInstancePscInstanceConfig",
    "AlloydbInstancePscInstanceConfigOutputReference",
    "AlloydbInstancePscInstanceConfigPscAutoConnections",
    "AlloydbInstancePscInstanceConfigPscAutoConnectionsList",
    "AlloydbInstancePscInstanceConfigPscAutoConnectionsOutputReference",
    "AlloydbInstancePscInstanceConfigPscInterfaceConfigs",
    "AlloydbInstancePscInstanceConfigPscInterfaceConfigsList",
    "AlloydbInstancePscInstanceConfigPscInterfaceConfigsOutputReference",
    "AlloydbInstanceQueryInsightsConfig",
    "AlloydbInstanceQueryInsightsConfigOutputReference",
    "AlloydbInstanceReadPoolConfig",
    "AlloydbInstanceReadPoolConfigOutputReference",
    "AlloydbInstanceTimeouts",
    "AlloydbInstanceTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__f765b873890bbf96433922dc1fea912d0f8d2ec8f3688afc26caab7e8fd9c0aa(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    cluster: builtins.str,
    instance_id: builtins.str,
    instance_type: builtins.str,
    activation_policy: typing.Optional[builtins.str] = None,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    availability_type: typing.Optional[builtins.str] = None,
    client_connection_config: typing.Optional[typing.Union[AlloydbInstanceClientConnectionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    database_flags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    display_name: typing.Optional[builtins.str] = None,
    gce_zone: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    machine_config: typing.Optional[typing.Union[AlloydbInstanceMachineConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    network_config: typing.Optional[typing.Union[AlloydbInstanceNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    psc_instance_config: typing.Optional[typing.Union[AlloydbInstancePscInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    query_insights_config: typing.Optional[typing.Union[AlloydbInstanceQueryInsightsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    read_pool_config: typing.Optional[typing.Union[AlloydbInstanceReadPoolConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[AlloydbInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__2d454a858279d54fbe39535893d0c5306da4d01321e151b87cae12309fe9889b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcbd91aa833e3ff387bfb0362b0e275b81f9e5eb2e38bcb5e2d6c906db033e51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fa1cb9979915aca6a7c4aeb57518b12a5796b6145a5a64a20ba7fde6e597550(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__158158519d9a8a65f38719221803f22b0703d7bf76e9846762986111669a41d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c4285c5b746dd6b49221842687902a1fd16d86c5f3323aa1f9e75c04444ffc4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69172a3afd4ec3ebb8d1e95baa8c35287c8e0a2d8aff61d978256916dbb9e08b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03f69c08f4e371a59795390d38974db812ca5132568dcf7976bed28c0b7761d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__024692bb7172b732c32dabc7eac5e3e61c8080298ee96e5e59153d60827c2031(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69feb04cc37565f93b1e2458d4a895c9f64325b499b629c6f52332caa6d88db0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__433ab37fe37b6a6f75557ec95ffd95c27cf82fd7cb300c5d18713c16ee888395(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0213d387b77d2f90108f9dfee31e87e4c0440368736dbabfbad6df49074010a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5277e02c8c1938057186ca3fe735c81944512c81f6a0d17e69f4c9a464d2fceb(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8cf4e7fd9312883106f38e965b6f54060f7ce32b2043d9968ca7d86c2e2b487(
    *,
    require_connectors: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ssl_config: typing.Optional[typing.Union[AlloydbInstanceClientConnectionConfigSslConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f45f3fa540237ab457caad04b0826ce46338ae701b6b66d01f418530a29922cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59cc790ab7c9a199a2d86467a57beb13493cbc0f5ef7dca7ab336db703bfd9f5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f5028740603fe89465277e145850b53f386ff7f7661ccc34890ec0840e23298(
    value: typing.Optional[AlloydbInstanceClientConnectionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9509e0196f1879b9e4a4d1b9fd98dec123341426d77f54b5a080035ad36328ec(
    *,
    ssl_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb5606c62ff21f7a076ea481599006d5aa15e8f13e9bfb156730daed4279af9b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fe5cac698c5296141623e85a90745a2cf570a9b320ab954a8e37b37296d5eda(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76e1119e35a4d448d087a370283b9cecd1a465b23f29327f3bf20bc0265b861c(
    value: typing.Optional[AlloydbInstanceClientConnectionConfigSslConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1513728bf9a692ea14e578c6e8e3ebe350a5703568d9faa6685c56af4afcaf1(
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
    client_connection_config: typing.Optional[typing.Union[AlloydbInstanceClientConnectionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    database_flags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    display_name: typing.Optional[builtins.str] = None,
    gce_zone: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    machine_config: typing.Optional[typing.Union[AlloydbInstanceMachineConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    network_config: typing.Optional[typing.Union[AlloydbInstanceNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    psc_instance_config: typing.Optional[typing.Union[AlloydbInstancePscInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    query_insights_config: typing.Optional[typing.Union[AlloydbInstanceQueryInsightsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    read_pool_config: typing.Optional[typing.Union[AlloydbInstanceReadPoolConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[AlloydbInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae1c69322f6ed0426aaab238f3d6fe1f33698bd608cd1b6534450a776dc51bff(
    *,
    cpu_count: typing.Optional[jsii.Number] = None,
    machine_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6339a3d89e0aecd8dda776b93a80b321f950a484556e4d01594e51837d60162(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a73e48c2e41ed071faf47c52884932f4bb7b8df932fdcf4e7395f28e4feb33db(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a074af488c75eeaddc22652fc84ca4936518e72b46fc56a96e273b7dcb1792c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b49f69a9f7a02d3d4fc15faefa62a4fbe7a3cf1ccf6ce27dfa4ef3830ee6608d(
    value: typing.Optional[AlloydbInstanceMachineConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eecabd9d2c04d20ddd9d7322d2e3278a6a5aaa482f391eb25d644abf1681f11(
    *,
    allocated_ip_range_override: typing.Optional[builtins.str] = None,
    authorized_external_networks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AlloydbInstanceNetworkConfigAuthorizedExternalNetworks, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enable_outbound_public_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_public_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3784bfe776a85fa93558af5d9a850a6d96b5e3a19e8929aacbc1e7fe2be7bb0(
    *,
    cidr_range: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aed019e5283472c93ff082b0f11341ed76d73382622f6371ac5490164875de9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f19b72da21f8e7c8e9417197574fd6e38dabf502c5f15de25f93dfefa2195cbc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__192c29b627674d0274b93ee83081b810983d1b91e1b6a209c8fefb2d101c6605(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__353ac5f9aed9fa57cedcc26aa66bc26dac683f55eb3a8c797702b7df92d01892(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__847b66deab62f32a029d23c88deda974c8ab5ed73d896d6e70af4bc1527173a8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0347d674562f47c8b2d9ad6d57916b8e43c1b38354b67aa78fffe565dda2688(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AlloydbInstanceNetworkConfigAuthorizedExternalNetworks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e79fca9d3e9b7a5cf151dd2d57d273d760ec37c78a9df537a1d56dca6cdd70d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b6caacef85cf55a2c3d1dde8034169f0f28a79de619a4a93949dede0606bbc4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44122d1a2b1185165339d32ece78917b02ed2df48517e89078f6bd5d65ab5a8a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlloydbInstanceNetworkConfigAuthorizedExternalNetworks]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6557aea470173be0ee74c5d53a80cfbbf4a48450debd4b8ab11fb37d2597f2ac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1432945e93ad9dfb53e0d27e6fd450dba70b4e06483c8cc1b1b1e63d3c8fd43(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AlloydbInstanceNetworkConfigAuthorizedExternalNetworks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__318561c5b7fb47e6466452c5ad51f7fb09a5d24caaf10c8562661fec52f06400(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9fc1a7c0d3bd776af4fc8f5185c2793f7edd817a0c418b9f3d91b0f95dc4777(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ec8146c7152b49cd1ae7fb8926f7e46bf60e1d3f41d38648970534713ec52bd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__922492357c21ad1176212bc39725d910c1fef2127b9f4a692ef39ea302e0c600(
    value: typing.Optional[AlloydbInstanceNetworkConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed01939214ec7982de1702bb73956902464e28a8c57942d8700db33826bd15b0(
    *,
    allowed_consumer_projects: typing.Optional[typing.Sequence[builtins.str]] = None,
    psc_auto_connections: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AlloydbInstancePscInstanceConfigPscAutoConnections, typing.Dict[builtins.str, typing.Any]]]]] = None,
    psc_interface_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AlloydbInstancePscInstanceConfigPscInterfaceConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66cabee8086cfff6312cd2acb396083f5376701e8fc44ef3b3644fb53adbeace(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a004420241717cbaea176e50a2f9dd3a3f4b373b91b6704f7e7a8e06f6cef39(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AlloydbInstancePscInstanceConfigPscAutoConnections, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9050edb31663e07f92acad137800e71a77bef37c2f1dae17d5e437e1a8bfcb33(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AlloydbInstancePscInstanceConfigPscInterfaceConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75943cfab2ffea034237a64a7cc65f1b4f9d6e04bed087cced9852ad801db81a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5968fe42e8749bf702f5e39c8668d3a1ef40f4a50037354372a6ecb9a57823eb(
    value: typing.Optional[AlloydbInstancePscInstanceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cab12810f4611fd34c372738888694d8b2321eaf8a5df8b4b8537241315c4d54(
    *,
    consumer_network: typing.Optional[builtins.str] = None,
    consumer_project: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98ce8f280ec60b4fd289e7d3317cf8f5a72efe15709382539b5fc0b89d8c44aa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c27898a098ffcffae543345be98294f00896a7fd8387c6f12ad8b31204bd2d5c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f37640c5d28c5e91606d17109aceca4eb14174ea31fb32e899ba5a397bcec918(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2473528ec53df4a4c8304fba8062d02649cce2ccb3b87da7c6ab1634fe7c0526(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80d1ab6fd9b6b5e4341c46361e88fe9e3c3d1eaf1f882b09532eb6aad0d18886(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4df3f29b02b9638ed66b1f05be2f4e70090a1a251664d636ae2c58c9741d3219(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AlloydbInstancePscInstanceConfigPscAutoConnections]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fd1fd48b9b01f7e129154e203bc6a7ac2ecda7b11fa7706afc8d55fa808a01f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96458f55fbc9839019de64cdfa1675115777eb3020029d5fc13fd211810b0d12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98e39d20df1215eac1a6cc742b8d9b61a698397118624063dfa37ebe273be8d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bf28ffa1c1cade4b27e16989121f6e31ba91b36c2428acc2af12600f2e420a5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlloydbInstancePscInstanceConfigPscAutoConnections]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7f9d6b9349983c71632c804c0d44a52b4d10d40076e1f08ee9c44f3f5f02511(
    *,
    network_attachment_resource: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c464a41188ee4de2e2b0d0599b658652c21d576b948daab5ff6ff6be36e6bef7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0bb38b8677d579681c15c9ffb6192779f34141d58deae2b9b1f6acf52926da7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79080c0ed944188c78941a0fbd86de7ffa8804f4a621c8dbb2db90446f18aa8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40fd665e3343cfe22fba39daf224932715d0fb081a184289dcdfd640a5621a3a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efbde442ed9a33ef70a7d5b4f68e4d594d4bb9003a4282fe0cec4001799dd564(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a1e2b436f82f8d32290cf84d98fb71d1b76dc22c8c0f5d07739a1787bdde48b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AlloydbInstancePscInstanceConfigPscInterfaceConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaca7f72b3eab7e8b9aee8f190d07d58c4c540bdb7c7416c7fd521411476c2a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c991ba6ddbe69636a548663c1dc969f65cd8188b4a0aff3e68aac71b3208ab64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83867f37475c48b67b49064a490edf15b7fe0105a12d085cf2360f9b0c395dfd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlloydbInstancePscInstanceConfigPscInterfaceConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d686258b4296fd9a11b228dfe1b794eee03b038e7d0d9e8375e0acd583b5e1f(
    *,
    query_plans_per_minute: typing.Optional[jsii.Number] = None,
    query_string_length: typing.Optional[jsii.Number] = None,
    record_application_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    record_client_address: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c3081d80b5ac08445d9e276af8b24ec751a115ced26fa32ed501647df359ed2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdc2465597128c53ed48b45d8e804dc3c8c5f446817cf58627e74746d302c749(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b8e0d10d517a751a5e22e8db495c766b4b70570c31baf7ce30a0106c9c27809(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8268d229a554e88fde1336ac3c2cb167b77417013e27c1c647b5f287224f1876(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3242ac241e5195487a9a12ca8ae575c6192cbc9bc7f971c4bbed53d6bce766f6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca12cbb111540303c875c4559a422153cf7c73f3e6bb6201f881ba29f139069d(
    value: typing.Optional[AlloydbInstanceQueryInsightsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0120a17d019867a39bdd1b37caa4ef3d6a7460620cc4588de9d2820ae166113a(
    *,
    node_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e556805238a67471d3893e5fabd42872956bcc68346527e15a946ed38ea27f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__943318cc25fb6c6992d481fdae72284609c691c58f76ded639cbccc4eddb93fd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6158543947f4bc9fb14030f6c3aaeba07c43666ce7eccae912e026c2bf388738(
    value: typing.Optional[AlloydbInstanceReadPoolConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92852fd79f1a1c5827f4e08118e4b8d1230621d12ab5bd3224b75cd3a0aaedcf(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af5cb81b3713f5486b0336541822b32c4dc250b959e4d0761a8ece4d1424ab7b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c95905f4e90d8f66e9d258da3dd09b81de67433dfda03e0b62f593f3bd3be278(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb9ef26d489259d7ed73010fb95d0e8fc45a13cd5be617b6a48a9313552f080a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca4553895f681f42dbf738f23a4e7a1f384184393c04956dbaee1f6706db8e21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc17f01754fc0647c4f612b32f9e93a7061cac0a49fbf4f69e833d262c586c39(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlloydbInstanceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
