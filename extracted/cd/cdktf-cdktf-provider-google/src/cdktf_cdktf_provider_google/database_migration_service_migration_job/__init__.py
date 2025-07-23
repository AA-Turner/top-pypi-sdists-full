r'''
# `google_database_migration_service_migration_job`

Refer to the Terraform Registry for docs: [`google_database_migration_service_migration_job`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job).
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


class DatabaseMigrationServiceMigrationJob(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.databaseMigrationServiceMigrationJob.DatabaseMigrationServiceMigrationJob",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job google_database_migration_service_migration_job}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        destination: builtins.str,
        migration_job_id: builtins.str,
        source: builtins.str,
        type: builtins.str,
        display_name: typing.Optional[builtins.str] = None,
        dump_flags: typing.Optional[typing.Union["DatabaseMigrationServiceMigrationJobDumpFlags", typing.Dict[builtins.str, typing.Any]]] = None,
        dump_path: typing.Optional[builtins.str] = None,
        dump_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        performance_config: typing.Optional[typing.Union["DatabaseMigrationServiceMigrationJobPerformanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        reverse_ssh_connectivity: typing.Optional[typing.Union["DatabaseMigrationServiceMigrationJobReverseSshConnectivity", typing.Dict[builtins.str, typing.Any]]] = None,
        static_ip_connectivity: typing.Optional[typing.Union["DatabaseMigrationServiceMigrationJobStaticIpConnectivity", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["DatabaseMigrationServiceMigrationJobTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_peering_connectivity: typing.Optional[typing.Union["DatabaseMigrationServiceMigrationJobVpcPeeringConnectivity", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job google_database_migration_service_migration_job} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param destination: The name of the destination connection profile resource in the form of projects/{project}/locations/{location}/connectionProfiles/{destinationConnectionProfile}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#destination DatabaseMigrationServiceMigrationJob#destination}
        :param migration_job_id: The ID of the migration job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#migration_job_id DatabaseMigrationServiceMigrationJob#migration_job_id}
        :param source: The name of the source connection profile resource in the form of projects/{project}/locations/{location}/connectionProfiles/{sourceConnectionProfile}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#source DatabaseMigrationServiceMigrationJob#source}
        :param type: The type of the migration job. Possible values: ["ONE_TIME", "CONTINUOUS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#type DatabaseMigrationServiceMigrationJob#type}
        :param display_name: The migration job display name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#display_name DatabaseMigrationServiceMigrationJob#display_name}
        :param dump_flags: dump_flags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#dump_flags DatabaseMigrationServiceMigrationJob#dump_flags}
        :param dump_path: The path to the dump file in Google Cloud Storage, in the format: (gs://[BUCKET_NAME]/[OBJECT_NAME]). This field and the "dump_flags" field are mutually exclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#dump_path DatabaseMigrationServiceMigrationJob#dump_path}
        :param dump_type: The type of the data dump. Supported for MySQL to CloudSQL for MySQL migrations only. Possible values: ["LOGICAL", "PHYSICAL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#dump_type DatabaseMigrationServiceMigrationJob#dump_type}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#id DatabaseMigrationServiceMigrationJob#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The resource labels for migration job to use to annotate any related underlying resources such as Compute Engine VMs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#labels DatabaseMigrationServiceMigrationJob#labels}
        :param location: The location where the migration job should reside. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#location DatabaseMigrationServiceMigrationJob#location}
        :param performance_config: performance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#performance_config DatabaseMigrationServiceMigrationJob#performance_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#project DatabaseMigrationServiceMigrationJob#project}.
        :param reverse_ssh_connectivity: reverse_ssh_connectivity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#reverse_ssh_connectivity DatabaseMigrationServiceMigrationJob#reverse_ssh_connectivity}
        :param static_ip_connectivity: static_ip_connectivity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#static_ip_connectivity DatabaseMigrationServiceMigrationJob#static_ip_connectivity}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#timeouts DatabaseMigrationServiceMigrationJob#timeouts}
        :param vpc_peering_connectivity: vpc_peering_connectivity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#vpc_peering_connectivity DatabaseMigrationServiceMigrationJob#vpc_peering_connectivity}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__053da1f8f4d53afb658336ff30a0a630019af8c123c923b88bdc7aa4c399b6e5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DatabaseMigrationServiceMigrationJobConfig(
            destination=destination,
            migration_job_id=migration_job_id,
            source=source,
            type=type,
            display_name=display_name,
            dump_flags=dump_flags,
            dump_path=dump_path,
            dump_type=dump_type,
            id=id,
            labels=labels,
            location=location,
            performance_config=performance_config,
            project=project,
            reverse_ssh_connectivity=reverse_ssh_connectivity,
            static_ip_connectivity=static_ip_connectivity,
            timeouts=timeouts,
            vpc_peering_connectivity=vpc_peering_connectivity,
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
        '''Generates CDKTF code for importing a DatabaseMigrationServiceMigrationJob resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DatabaseMigrationServiceMigrationJob to import.
        :param import_from_id: The id of the existing DatabaseMigrationServiceMigrationJob that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DatabaseMigrationServiceMigrationJob to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ed180d53fe4075daa30981e16fd9c7bcff0c539ffcd0a8291d08fe90e77e223)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDumpFlags")
    def put_dump_flags(
        self,
        *,
        dump_flags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseMigrationServiceMigrationJobDumpFlagsDumpFlags", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param dump_flags: dump_flags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#dump_flags DatabaseMigrationServiceMigrationJob#dump_flags}
        '''
        value = DatabaseMigrationServiceMigrationJobDumpFlags(dump_flags=dump_flags)

        return typing.cast(None, jsii.invoke(self, "putDumpFlags", [value]))

    @jsii.member(jsii_name="putPerformanceConfig")
    def put_performance_config(
        self,
        *,
        dump_parallel_level: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dump_parallel_level: Initial dump parallelism level. Possible values: ["MIN", "OPTIMAL", "MAX"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#dump_parallel_level DatabaseMigrationServiceMigrationJob#dump_parallel_level}
        '''
        value = DatabaseMigrationServiceMigrationJobPerformanceConfig(
            dump_parallel_level=dump_parallel_level
        )

        return typing.cast(None, jsii.invoke(self, "putPerformanceConfig", [value]))

    @jsii.member(jsii_name="putReverseSshConnectivity")
    def put_reverse_ssh_connectivity(
        self,
        *,
        vm: typing.Optional[builtins.str] = None,
        vm_ip: typing.Optional[builtins.str] = None,
        vm_port: typing.Optional[jsii.Number] = None,
        vpc: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param vm: The name of the virtual machine (Compute Engine) used as the bastion server for the SSH tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#vm DatabaseMigrationServiceMigrationJob#vm}
        :param vm_ip: The IP of the virtual machine (Compute Engine) used as the bastion server for the SSH tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#vm_ip DatabaseMigrationServiceMigrationJob#vm_ip}
        :param vm_port: The forwarding port of the virtual machine (Compute Engine) used as the bastion server for the SSH tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#vm_port DatabaseMigrationServiceMigrationJob#vm_port}
        :param vpc: The name of the VPC to peer with the Cloud SQL private network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#vpc DatabaseMigrationServiceMigrationJob#vpc}
        '''
        value = DatabaseMigrationServiceMigrationJobReverseSshConnectivity(
            vm=vm, vm_ip=vm_ip, vm_port=vm_port, vpc=vpc
        )

        return typing.cast(None, jsii.invoke(self, "putReverseSshConnectivity", [value]))

    @jsii.member(jsii_name="putStaticIpConnectivity")
    def put_static_ip_connectivity(self) -> None:
        value = DatabaseMigrationServiceMigrationJobStaticIpConnectivity()

        return typing.cast(None, jsii.invoke(self, "putStaticIpConnectivity", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#create DatabaseMigrationServiceMigrationJob#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#delete DatabaseMigrationServiceMigrationJob#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#update DatabaseMigrationServiceMigrationJob#update}.
        '''
        value = DatabaseMigrationServiceMigrationJobTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putVpcPeeringConnectivity")
    def put_vpc_peering_connectivity(
        self,
        *,
        vpc: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param vpc: The name of the VPC network to peer with the Cloud SQL private network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#vpc DatabaseMigrationServiceMigrationJob#vpc}
        '''
        value = DatabaseMigrationServiceMigrationJobVpcPeeringConnectivity(vpc=vpc)

        return typing.cast(None, jsii.invoke(self, "putVpcPeeringConnectivity", [value]))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetDumpFlags")
    def reset_dump_flags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDumpFlags", []))

    @jsii.member(jsii_name="resetDumpPath")
    def reset_dump_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDumpPath", []))

    @jsii.member(jsii_name="resetDumpType")
    def reset_dump_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDumpType", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetPerformanceConfig")
    def reset_performance_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPerformanceConfig", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetReverseSshConnectivity")
    def reset_reverse_ssh_connectivity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReverseSshConnectivity", []))

    @jsii.member(jsii_name="resetStaticIpConnectivity")
    def reset_static_ip_connectivity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStaticIpConnectivity", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVpcPeeringConnectivity")
    def reset_vpc_peering_connectivity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcPeeringConnectivity", []))

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
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="dumpFlags")
    def dump_flags(
        self,
    ) -> "DatabaseMigrationServiceMigrationJobDumpFlagsOutputReference":
        return typing.cast("DatabaseMigrationServiceMigrationJobDumpFlagsOutputReference", jsii.get(self, "dumpFlags"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="error")
    def error(self) -> "DatabaseMigrationServiceMigrationJobErrorList":
        return typing.cast("DatabaseMigrationServiceMigrationJobErrorList", jsii.get(self, "error"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="performanceConfig")
    def performance_config(
        self,
    ) -> "DatabaseMigrationServiceMigrationJobPerformanceConfigOutputReference":
        return typing.cast("DatabaseMigrationServiceMigrationJobPerformanceConfigOutputReference", jsii.get(self, "performanceConfig"))

    @builtins.property
    @jsii.member(jsii_name="phase")
    def phase(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "phase"))

    @builtins.property
    @jsii.member(jsii_name="reverseSshConnectivity")
    def reverse_ssh_connectivity(
        self,
    ) -> "DatabaseMigrationServiceMigrationJobReverseSshConnectivityOutputReference":
        return typing.cast("DatabaseMigrationServiceMigrationJobReverseSshConnectivityOutputReference", jsii.get(self, "reverseSshConnectivity"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="staticIpConnectivity")
    def static_ip_connectivity(
        self,
    ) -> "DatabaseMigrationServiceMigrationJobStaticIpConnectivityOutputReference":
        return typing.cast("DatabaseMigrationServiceMigrationJobStaticIpConnectivityOutputReference", jsii.get(self, "staticIpConnectivity"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DatabaseMigrationServiceMigrationJobTimeoutsOutputReference":
        return typing.cast("DatabaseMigrationServiceMigrationJobTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="vpcPeeringConnectivity")
    def vpc_peering_connectivity(
        self,
    ) -> "DatabaseMigrationServiceMigrationJobVpcPeeringConnectivityOutputReference":
        return typing.cast("DatabaseMigrationServiceMigrationJobVpcPeeringConnectivityOutputReference", jsii.get(self, "vpcPeeringConnectivity"))

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="dumpFlagsInput")
    def dump_flags_input(
        self,
    ) -> typing.Optional["DatabaseMigrationServiceMigrationJobDumpFlags"]:
        return typing.cast(typing.Optional["DatabaseMigrationServiceMigrationJobDumpFlags"], jsii.get(self, "dumpFlagsInput"))

    @builtins.property
    @jsii.member(jsii_name="dumpPathInput")
    def dump_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dumpPathInput"))

    @builtins.property
    @jsii.member(jsii_name="dumpTypeInput")
    def dump_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dumpTypeInput"))

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
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="migrationJobIdInput")
    def migration_job_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "migrationJobIdInput"))

    @builtins.property
    @jsii.member(jsii_name="performanceConfigInput")
    def performance_config_input(
        self,
    ) -> typing.Optional["DatabaseMigrationServiceMigrationJobPerformanceConfig"]:
        return typing.cast(typing.Optional["DatabaseMigrationServiceMigrationJobPerformanceConfig"], jsii.get(self, "performanceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="reverseSshConnectivityInput")
    def reverse_ssh_connectivity_input(
        self,
    ) -> typing.Optional["DatabaseMigrationServiceMigrationJobReverseSshConnectivity"]:
        return typing.cast(typing.Optional["DatabaseMigrationServiceMigrationJobReverseSshConnectivity"], jsii.get(self, "reverseSshConnectivityInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="staticIpConnectivityInput")
    def static_ip_connectivity_input(
        self,
    ) -> typing.Optional["DatabaseMigrationServiceMigrationJobStaticIpConnectivity"]:
        return typing.cast(typing.Optional["DatabaseMigrationServiceMigrationJobStaticIpConnectivity"], jsii.get(self, "staticIpConnectivityInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DatabaseMigrationServiceMigrationJobTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DatabaseMigrationServiceMigrationJobTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcPeeringConnectivityInput")
    def vpc_peering_connectivity_input(
        self,
    ) -> typing.Optional["DatabaseMigrationServiceMigrationJobVpcPeeringConnectivity"]:
        return typing.cast(typing.Optional["DatabaseMigrationServiceMigrationJobVpcPeeringConnectivity"], jsii.get(self, "vpcPeeringConnectivityInput"))

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destination"))

    @destination.setter
    def destination(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eab8886a68043c9b8a4b73008d6c6133bbef722f6925951154673123038301b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60e521f88f083189a8251199abe0e90aa7e6270f76394931d9797d7cbe195d6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dumpPath")
    def dump_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dumpPath"))

    @dump_path.setter
    def dump_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e8fa56bccb106c245b89ea17b9c2bcca187ca9037ba9f328d2cb62a69f7f398)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dumpPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dumpType")
    def dump_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dumpType"))

    @dump_type.setter
    def dump_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f86479f6195bee3240513b49a47a3761655542322b71d00723e4fdb7cb452fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dumpType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__621fd589779ff13febf46fd7a68c64aa7497e43f16ad12c85949b3b3339cf3aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c7b572a58162be65a7d12c83db3273bc2426f069db985b1b17a0a457e20f4ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c8b8a032949f743958b2eb37f63702b724ba5f719540267c8c457eddb687fb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="migrationJobId")
    def migration_job_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "migrationJobId"))

    @migration_job_id.setter
    def migration_job_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f78ee9c2fd72740ea74ef41133de56d5318a0af37eafee7e89f81b04c0d6c228)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "migrationJobId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f11a0563e3618889326784a010c54f441a4230e4810266da89b2a957af2df35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__388eadbb07c71ae51413669224f6fb96fc70e7a17c95848a024de19f031812e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f553604bb06b486c85f31a190320457c95f609466a9e9487bc84abf37935071f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.databaseMigrationServiceMigrationJob.DatabaseMigrationServiceMigrationJobConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "destination": "destination",
        "migration_job_id": "migrationJobId",
        "source": "source",
        "type": "type",
        "display_name": "displayName",
        "dump_flags": "dumpFlags",
        "dump_path": "dumpPath",
        "dump_type": "dumpType",
        "id": "id",
        "labels": "labels",
        "location": "location",
        "performance_config": "performanceConfig",
        "project": "project",
        "reverse_ssh_connectivity": "reverseSshConnectivity",
        "static_ip_connectivity": "staticIpConnectivity",
        "timeouts": "timeouts",
        "vpc_peering_connectivity": "vpcPeeringConnectivity",
    },
)
class DatabaseMigrationServiceMigrationJobConfig(
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
        destination: builtins.str,
        migration_job_id: builtins.str,
        source: builtins.str,
        type: builtins.str,
        display_name: typing.Optional[builtins.str] = None,
        dump_flags: typing.Optional[typing.Union["DatabaseMigrationServiceMigrationJobDumpFlags", typing.Dict[builtins.str, typing.Any]]] = None,
        dump_path: typing.Optional[builtins.str] = None,
        dump_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        performance_config: typing.Optional[typing.Union["DatabaseMigrationServiceMigrationJobPerformanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        reverse_ssh_connectivity: typing.Optional[typing.Union["DatabaseMigrationServiceMigrationJobReverseSshConnectivity", typing.Dict[builtins.str, typing.Any]]] = None,
        static_ip_connectivity: typing.Optional[typing.Union["DatabaseMigrationServiceMigrationJobStaticIpConnectivity", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["DatabaseMigrationServiceMigrationJobTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_peering_connectivity: typing.Optional[typing.Union["DatabaseMigrationServiceMigrationJobVpcPeeringConnectivity", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param destination: The name of the destination connection profile resource in the form of projects/{project}/locations/{location}/connectionProfiles/{destinationConnectionProfile}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#destination DatabaseMigrationServiceMigrationJob#destination}
        :param migration_job_id: The ID of the migration job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#migration_job_id DatabaseMigrationServiceMigrationJob#migration_job_id}
        :param source: The name of the source connection profile resource in the form of projects/{project}/locations/{location}/connectionProfiles/{sourceConnectionProfile}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#source DatabaseMigrationServiceMigrationJob#source}
        :param type: The type of the migration job. Possible values: ["ONE_TIME", "CONTINUOUS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#type DatabaseMigrationServiceMigrationJob#type}
        :param display_name: The migration job display name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#display_name DatabaseMigrationServiceMigrationJob#display_name}
        :param dump_flags: dump_flags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#dump_flags DatabaseMigrationServiceMigrationJob#dump_flags}
        :param dump_path: The path to the dump file in Google Cloud Storage, in the format: (gs://[BUCKET_NAME]/[OBJECT_NAME]). This field and the "dump_flags" field are mutually exclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#dump_path DatabaseMigrationServiceMigrationJob#dump_path}
        :param dump_type: The type of the data dump. Supported for MySQL to CloudSQL for MySQL migrations only. Possible values: ["LOGICAL", "PHYSICAL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#dump_type DatabaseMigrationServiceMigrationJob#dump_type}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#id DatabaseMigrationServiceMigrationJob#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The resource labels for migration job to use to annotate any related underlying resources such as Compute Engine VMs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#labels DatabaseMigrationServiceMigrationJob#labels}
        :param location: The location where the migration job should reside. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#location DatabaseMigrationServiceMigrationJob#location}
        :param performance_config: performance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#performance_config DatabaseMigrationServiceMigrationJob#performance_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#project DatabaseMigrationServiceMigrationJob#project}.
        :param reverse_ssh_connectivity: reverse_ssh_connectivity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#reverse_ssh_connectivity DatabaseMigrationServiceMigrationJob#reverse_ssh_connectivity}
        :param static_ip_connectivity: static_ip_connectivity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#static_ip_connectivity DatabaseMigrationServiceMigrationJob#static_ip_connectivity}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#timeouts DatabaseMigrationServiceMigrationJob#timeouts}
        :param vpc_peering_connectivity: vpc_peering_connectivity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#vpc_peering_connectivity DatabaseMigrationServiceMigrationJob#vpc_peering_connectivity}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(dump_flags, dict):
            dump_flags = DatabaseMigrationServiceMigrationJobDumpFlags(**dump_flags)
        if isinstance(performance_config, dict):
            performance_config = DatabaseMigrationServiceMigrationJobPerformanceConfig(**performance_config)
        if isinstance(reverse_ssh_connectivity, dict):
            reverse_ssh_connectivity = DatabaseMigrationServiceMigrationJobReverseSshConnectivity(**reverse_ssh_connectivity)
        if isinstance(static_ip_connectivity, dict):
            static_ip_connectivity = DatabaseMigrationServiceMigrationJobStaticIpConnectivity(**static_ip_connectivity)
        if isinstance(timeouts, dict):
            timeouts = DatabaseMigrationServiceMigrationJobTimeouts(**timeouts)
        if isinstance(vpc_peering_connectivity, dict):
            vpc_peering_connectivity = DatabaseMigrationServiceMigrationJobVpcPeeringConnectivity(**vpc_peering_connectivity)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7470698f11c2d90169475413ca058a75c743b19faa1fdb22552b5bc313f32d6f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument migration_job_id", value=migration_job_id, expected_type=type_hints["migration_job_id"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument dump_flags", value=dump_flags, expected_type=type_hints["dump_flags"])
            check_type(argname="argument dump_path", value=dump_path, expected_type=type_hints["dump_path"])
            check_type(argname="argument dump_type", value=dump_type, expected_type=type_hints["dump_type"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument performance_config", value=performance_config, expected_type=type_hints["performance_config"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument reverse_ssh_connectivity", value=reverse_ssh_connectivity, expected_type=type_hints["reverse_ssh_connectivity"])
            check_type(argname="argument static_ip_connectivity", value=static_ip_connectivity, expected_type=type_hints["static_ip_connectivity"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument vpc_peering_connectivity", value=vpc_peering_connectivity, expected_type=type_hints["vpc_peering_connectivity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination": destination,
            "migration_job_id": migration_job_id,
            "source": source,
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
        if display_name is not None:
            self._values["display_name"] = display_name
        if dump_flags is not None:
            self._values["dump_flags"] = dump_flags
        if dump_path is not None:
            self._values["dump_path"] = dump_path
        if dump_type is not None:
            self._values["dump_type"] = dump_type
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if location is not None:
            self._values["location"] = location
        if performance_config is not None:
            self._values["performance_config"] = performance_config
        if project is not None:
            self._values["project"] = project
        if reverse_ssh_connectivity is not None:
            self._values["reverse_ssh_connectivity"] = reverse_ssh_connectivity
        if static_ip_connectivity is not None:
            self._values["static_ip_connectivity"] = static_ip_connectivity
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if vpc_peering_connectivity is not None:
            self._values["vpc_peering_connectivity"] = vpc_peering_connectivity

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
    def destination(self) -> builtins.str:
        '''The name of the destination connection profile resource in the form of projects/{project}/locations/{location}/connectionProfiles/{destinationConnectionProfile}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#destination DatabaseMigrationServiceMigrationJob#destination}
        '''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def migration_job_id(self) -> builtins.str:
        '''The ID of the migration job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#migration_job_id DatabaseMigrationServiceMigrationJob#migration_job_id}
        '''
        result = self._values.get("migration_job_id")
        assert result is not None, "Required property 'migration_job_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source(self) -> builtins.str:
        '''The name of the source connection profile resource in the form of projects/{project}/locations/{location}/connectionProfiles/{sourceConnectionProfile}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#source DatabaseMigrationServiceMigrationJob#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of the migration job. Possible values: ["ONE_TIME", "CONTINUOUS"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#type DatabaseMigrationServiceMigrationJob#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The migration job display name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#display_name DatabaseMigrationServiceMigrationJob#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dump_flags(
        self,
    ) -> typing.Optional["DatabaseMigrationServiceMigrationJobDumpFlags"]:
        '''dump_flags block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#dump_flags DatabaseMigrationServiceMigrationJob#dump_flags}
        '''
        result = self._values.get("dump_flags")
        return typing.cast(typing.Optional["DatabaseMigrationServiceMigrationJobDumpFlags"], result)

    @builtins.property
    def dump_path(self) -> typing.Optional[builtins.str]:
        '''The path to the dump file in Google Cloud Storage, in the format: (gs://[BUCKET_NAME]/[OBJECT_NAME]).

        This field and the "dump_flags" field are mutually exclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#dump_path DatabaseMigrationServiceMigrationJob#dump_path}
        '''
        result = self._values.get("dump_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dump_type(self) -> typing.Optional[builtins.str]:
        '''The type of the data dump. Supported for MySQL to CloudSQL for MySQL migrations only. Possible values: ["LOGICAL", "PHYSICAL"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#dump_type DatabaseMigrationServiceMigrationJob#dump_type}
        '''
        result = self._values.get("dump_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#id DatabaseMigrationServiceMigrationJob#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The resource labels for migration job to use to annotate any related underlying resources such as Compute Engine VMs.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#labels DatabaseMigrationServiceMigrationJob#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The location where the migration job should reside.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#location DatabaseMigrationServiceMigrationJob#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def performance_config(
        self,
    ) -> typing.Optional["DatabaseMigrationServiceMigrationJobPerformanceConfig"]:
        '''performance_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#performance_config DatabaseMigrationServiceMigrationJob#performance_config}
        '''
        result = self._values.get("performance_config")
        return typing.cast(typing.Optional["DatabaseMigrationServiceMigrationJobPerformanceConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#project DatabaseMigrationServiceMigrationJob#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reverse_ssh_connectivity(
        self,
    ) -> typing.Optional["DatabaseMigrationServiceMigrationJobReverseSshConnectivity"]:
        '''reverse_ssh_connectivity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#reverse_ssh_connectivity DatabaseMigrationServiceMigrationJob#reverse_ssh_connectivity}
        '''
        result = self._values.get("reverse_ssh_connectivity")
        return typing.cast(typing.Optional["DatabaseMigrationServiceMigrationJobReverseSshConnectivity"], result)

    @builtins.property
    def static_ip_connectivity(
        self,
    ) -> typing.Optional["DatabaseMigrationServiceMigrationJobStaticIpConnectivity"]:
        '''static_ip_connectivity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#static_ip_connectivity DatabaseMigrationServiceMigrationJob#static_ip_connectivity}
        '''
        result = self._values.get("static_ip_connectivity")
        return typing.cast(typing.Optional["DatabaseMigrationServiceMigrationJobStaticIpConnectivity"], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["DatabaseMigrationServiceMigrationJobTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#timeouts DatabaseMigrationServiceMigrationJob#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DatabaseMigrationServiceMigrationJobTimeouts"], result)

    @builtins.property
    def vpc_peering_connectivity(
        self,
    ) -> typing.Optional["DatabaseMigrationServiceMigrationJobVpcPeeringConnectivity"]:
        '''vpc_peering_connectivity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#vpc_peering_connectivity DatabaseMigrationServiceMigrationJob#vpc_peering_connectivity}
        '''
        result = self._values.get("vpc_peering_connectivity")
        return typing.cast(typing.Optional["DatabaseMigrationServiceMigrationJobVpcPeeringConnectivity"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseMigrationServiceMigrationJobConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.databaseMigrationServiceMigrationJob.DatabaseMigrationServiceMigrationJobDumpFlags",
    jsii_struct_bases=[],
    name_mapping={"dump_flags": "dumpFlags"},
)
class DatabaseMigrationServiceMigrationJobDumpFlags:
    def __init__(
        self,
        *,
        dump_flags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseMigrationServiceMigrationJobDumpFlagsDumpFlags", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param dump_flags: dump_flags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#dump_flags DatabaseMigrationServiceMigrationJob#dump_flags}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37c171612646792f83ac0e489aea4bc81867271abefcf1cd0e499e9de086703b)
            check_type(argname="argument dump_flags", value=dump_flags, expected_type=type_hints["dump_flags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dump_flags is not None:
            self._values["dump_flags"] = dump_flags

    @builtins.property
    def dump_flags(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseMigrationServiceMigrationJobDumpFlagsDumpFlags"]]]:
        '''dump_flags block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#dump_flags DatabaseMigrationServiceMigrationJob#dump_flags}
        '''
        result = self._values.get("dump_flags")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseMigrationServiceMigrationJobDumpFlagsDumpFlags"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseMigrationServiceMigrationJobDumpFlags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.databaseMigrationServiceMigrationJob.DatabaseMigrationServiceMigrationJobDumpFlagsDumpFlags",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class DatabaseMigrationServiceMigrationJobDumpFlagsDumpFlags:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name of the flag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#name DatabaseMigrationServiceMigrationJob#name}
        :param value: The vale of the flag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#value DatabaseMigrationServiceMigrationJob#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b40dd2a9a75640db507bc46dc1b73afa88a399bea7729ddb42091bba4a841623)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the flag.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#name DatabaseMigrationServiceMigrationJob#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The vale of the flag.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#value DatabaseMigrationServiceMigrationJob#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseMigrationServiceMigrationJobDumpFlagsDumpFlags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabaseMigrationServiceMigrationJobDumpFlagsDumpFlagsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.databaseMigrationServiceMigrationJob.DatabaseMigrationServiceMigrationJobDumpFlagsDumpFlagsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec6dcd9c2df9f94522f7a300c51b6290315116fc0e610bb607d1b292856e478f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DatabaseMigrationServiceMigrationJobDumpFlagsDumpFlagsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa75d54cd34b26d1547da3d071fbf852b1910cb5cb9c39ba8c396439d0d45809)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatabaseMigrationServiceMigrationJobDumpFlagsDumpFlagsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__270376b6bfd9862aebb219714c02c345433834c73ace2ed3c58ce1d11b07f7dc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e47c75dd37bb45dd0c8802f9fa24d8bc33e783d25147e5d9e85069cdfd2c6514)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f034ea4f9727a6c723cb687c1d2f40ebb00cdd740a9b6552a670ae39756c3f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseMigrationServiceMigrationJobDumpFlagsDumpFlags]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseMigrationServiceMigrationJobDumpFlagsDumpFlags]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseMigrationServiceMigrationJobDumpFlagsDumpFlags]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f417a410b6216e093767b7dc2f61be736df6e10bd4d22474a954b537a968991)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DatabaseMigrationServiceMigrationJobDumpFlagsDumpFlagsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.databaseMigrationServiceMigrationJob.DatabaseMigrationServiceMigrationJobDumpFlagsDumpFlagsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0c7b00989c7f07bd134b1527f561aa557064ec56118cb418539f1f9ec2887af)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03ee76545693c8712f4749bae8b2f3c191cfc0109126e6708e9d20302933ae0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__198bb17e9ddb455848cb8d0d8a9dc2f7731be4cbfcfcafe4f0e7eae00630248f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseMigrationServiceMigrationJobDumpFlagsDumpFlags]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseMigrationServiceMigrationJobDumpFlagsDumpFlags]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseMigrationServiceMigrationJobDumpFlagsDumpFlags]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2503414db05af0ea5b5e139d1518a8640ee9eb33b5659887c0d2e7cc3086ed9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DatabaseMigrationServiceMigrationJobDumpFlagsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.databaseMigrationServiceMigrationJob.DatabaseMigrationServiceMigrationJobDumpFlagsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee0f3a979ae4a105e0376a313f02d40d28ec6bd0755b39c5b2108c4f62cea23f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDumpFlags")
    def put_dump_flags(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseMigrationServiceMigrationJobDumpFlagsDumpFlags, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da9e93b6450f28e10f3598093ff84a31a5cdef5d1c288fde11edd9c1623e8136)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDumpFlags", [value]))

    @jsii.member(jsii_name="resetDumpFlags")
    def reset_dump_flags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDumpFlags", []))

    @builtins.property
    @jsii.member(jsii_name="dumpFlags")
    def dump_flags(self) -> DatabaseMigrationServiceMigrationJobDumpFlagsDumpFlagsList:
        return typing.cast(DatabaseMigrationServiceMigrationJobDumpFlagsDumpFlagsList, jsii.get(self, "dumpFlags"))

    @builtins.property
    @jsii.member(jsii_name="dumpFlagsInput")
    def dump_flags_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseMigrationServiceMigrationJobDumpFlagsDumpFlags]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseMigrationServiceMigrationJobDumpFlagsDumpFlags]]], jsii.get(self, "dumpFlagsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatabaseMigrationServiceMigrationJobDumpFlags]:
        return typing.cast(typing.Optional[DatabaseMigrationServiceMigrationJobDumpFlags], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatabaseMigrationServiceMigrationJobDumpFlags],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10bdef07a9db060d5fda5a13075397c2a7b4ac6018678f9dfbdd5761666d2c7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.databaseMigrationServiceMigrationJob.DatabaseMigrationServiceMigrationJobError",
    jsii_struct_bases=[],
    name_mapping={},
)
class DatabaseMigrationServiceMigrationJobError:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseMigrationServiceMigrationJobError(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabaseMigrationServiceMigrationJobErrorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.databaseMigrationServiceMigrationJob.DatabaseMigrationServiceMigrationJobErrorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__248e9d97f8a67bb5ec8ceb4c90f378c2d45e33ca67549bd4cb5b7fe8cdf320d7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DatabaseMigrationServiceMigrationJobErrorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4a7769766040d25e1ee532329bb370755e6f2311d2861e8aeaa34c9b389649d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatabaseMigrationServiceMigrationJobErrorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab5e7b6269d4560a0d19826cf94180cbd04803bac6838f98fc31c23f6b9d7558)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f823e351ff84ca3ef9077a5d4322787559448a06cfe0cd05f3e871985ad4cd45)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d71dffda3f804b109e5b54975fbc59e11846a1c91af54e8232aae9d120b73168)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DatabaseMigrationServiceMigrationJobErrorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.databaseMigrationServiceMigrationJob.DatabaseMigrationServiceMigrationJobErrorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__959d848302b90f7b3e4ccb75035c75aefa8a0c7d114039996ff43c2b620d6db3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="code")
    def code(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "code"))

    @builtins.property
    @jsii.member(jsii_name="details")
    def details(self) -> _cdktf_9a9027ec.StringMapList:
        return typing.cast(_cdktf_9a9027ec.StringMapList, jsii.get(self, "details"))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatabaseMigrationServiceMigrationJobError]:
        return typing.cast(typing.Optional[DatabaseMigrationServiceMigrationJobError], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatabaseMigrationServiceMigrationJobError],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8d22189ffd431e8da1a967dbd193a84bfdd6926aeeb6f71b3c018870eab1bf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.databaseMigrationServiceMigrationJob.DatabaseMigrationServiceMigrationJobPerformanceConfig",
    jsii_struct_bases=[],
    name_mapping={"dump_parallel_level": "dumpParallelLevel"},
)
class DatabaseMigrationServiceMigrationJobPerformanceConfig:
    def __init__(
        self,
        *,
        dump_parallel_level: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dump_parallel_level: Initial dump parallelism level. Possible values: ["MIN", "OPTIMAL", "MAX"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#dump_parallel_level DatabaseMigrationServiceMigrationJob#dump_parallel_level}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__230652fa8a4481f8929f273e7b439dfba50b61fe0f607c3743b30bb2eba39176)
            check_type(argname="argument dump_parallel_level", value=dump_parallel_level, expected_type=type_hints["dump_parallel_level"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dump_parallel_level is not None:
            self._values["dump_parallel_level"] = dump_parallel_level

    @builtins.property
    def dump_parallel_level(self) -> typing.Optional[builtins.str]:
        '''Initial dump parallelism level. Possible values: ["MIN", "OPTIMAL", "MAX"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#dump_parallel_level DatabaseMigrationServiceMigrationJob#dump_parallel_level}
        '''
        result = self._values.get("dump_parallel_level")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseMigrationServiceMigrationJobPerformanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabaseMigrationServiceMigrationJobPerformanceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.databaseMigrationServiceMigrationJob.DatabaseMigrationServiceMigrationJobPerformanceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__695da165626928757a7d3ae3282c82dd31f2787dd9625902d71559f86fd630de)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDumpParallelLevel")
    def reset_dump_parallel_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDumpParallelLevel", []))

    @builtins.property
    @jsii.member(jsii_name="dumpParallelLevelInput")
    def dump_parallel_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dumpParallelLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="dumpParallelLevel")
    def dump_parallel_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dumpParallelLevel"))

    @dump_parallel_level.setter
    def dump_parallel_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0d50a26f2b414c46481e979a8d9ca994dd353ceac3f2965f84ce1a0b3943597)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dumpParallelLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatabaseMigrationServiceMigrationJobPerformanceConfig]:
        return typing.cast(typing.Optional[DatabaseMigrationServiceMigrationJobPerformanceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatabaseMigrationServiceMigrationJobPerformanceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38be8d6ab9262664d0255592bb12f4cb1b60db67280171e0337145641868a4e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.databaseMigrationServiceMigrationJob.DatabaseMigrationServiceMigrationJobReverseSshConnectivity",
    jsii_struct_bases=[],
    name_mapping={"vm": "vm", "vm_ip": "vmIp", "vm_port": "vmPort", "vpc": "vpc"},
)
class DatabaseMigrationServiceMigrationJobReverseSshConnectivity:
    def __init__(
        self,
        *,
        vm: typing.Optional[builtins.str] = None,
        vm_ip: typing.Optional[builtins.str] = None,
        vm_port: typing.Optional[jsii.Number] = None,
        vpc: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param vm: The name of the virtual machine (Compute Engine) used as the bastion server for the SSH tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#vm DatabaseMigrationServiceMigrationJob#vm}
        :param vm_ip: The IP of the virtual machine (Compute Engine) used as the bastion server for the SSH tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#vm_ip DatabaseMigrationServiceMigrationJob#vm_ip}
        :param vm_port: The forwarding port of the virtual machine (Compute Engine) used as the bastion server for the SSH tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#vm_port DatabaseMigrationServiceMigrationJob#vm_port}
        :param vpc: The name of the VPC to peer with the Cloud SQL private network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#vpc DatabaseMigrationServiceMigrationJob#vpc}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acc4c7c0358e6b62981809912f3c42fcaff033d78dee0e49770121d6828f5846)
            check_type(argname="argument vm", value=vm, expected_type=type_hints["vm"])
            check_type(argname="argument vm_ip", value=vm_ip, expected_type=type_hints["vm_ip"])
            check_type(argname="argument vm_port", value=vm_port, expected_type=type_hints["vm_port"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if vm is not None:
            self._values["vm"] = vm
        if vm_ip is not None:
            self._values["vm_ip"] = vm_ip
        if vm_port is not None:
            self._values["vm_port"] = vm_port
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def vm(self) -> typing.Optional[builtins.str]:
        '''The name of the virtual machine (Compute Engine) used as the bastion server for the SSH tunnel.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#vm DatabaseMigrationServiceMigrationJob#vm}
        '''
        result = self._values.get("vm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vm_ip(self) -> typing.Optional[builtins.str]:
        '''The IP of the virtual machine (Compute Engine) used as the bastion server for the SSH tunnel.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#vm_ip DatabaseMigrationServiceMigrationJob#vm_ip}
        '''
        result = self._values.get("vm_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vm_port(self) -> typing.Optional[jsii.Number]:
        '''The forwarding port of the virtual machine (Compute Engine) used as the bastion server for the SSH tunnel.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#vm_port DatabaseMigrationServiceMigrationJob#vm_port}
        '''
        result = self._values.get("vm_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vpc(self) -> typing.Optional[builtins.str]:
        '''The name of the VPC to peer with the Cloud SQL private network.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#vpc DatabaseMigrationServiceMigrationJob#vpc}
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseMigrationServiceMigrationJobReverseSshConnectivity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabaseMigrationServiceMigrationJobReverseSshConnectivityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.databaseMigrationServiceMigrationJob.DatabaseMigrationServiceMigrationJobReverseSshConnectivityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce288961c6a19ab8b11abc94f892d6532a6c39cf8b11e81186ba8a15f62dbfc3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetVm")
    def reset_vm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVm", []))

    @jsii.member(jsii_name="resetVmIp")
    def reset_vm_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVmIp", []))

    @jsii.member(jsii_name="resetVmPort")
    def reset_vm_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVmPort", []))

    @jsii.member(jsii_name="resetVpc")
    def reset_vpc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpc", []))

    @builtins.property
    @jsii.member(jsii_name="vmInput")
    def vm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vmInput"))

    @builtins.property
    @jsii.member(jsii_name="vmIpInput")
    def vm_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vmIpInput"))

    @builtins.property
    @jsii.member(jsii_name="vmPortInput")
    def vm_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "vmPortInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcInput")
    def vpc_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcInput"))

    @builtins.property
    @jsii.member(jsii_name="vm")
    def vm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vm"))

    @vm.setter
    def vm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4fbc08c68505944d7efbbb6b72d90844b2e79cd662c87d0b5305d9fefdfbf25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmIp")
    def vm_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmIp"))

    @vm_ip.setter
    def vm_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db8314f2d0a9b0660c54462acbbcd040d8c7f448fa6b90dbcdf86283004d3237)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmPort")
    def vm_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "vmPort"))

    @vm_port.setter
    def vm_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cec9fe785abd66e2ed35d10ee58231ce1a4d1c2483ed88a20a6cd9b55be8b927)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpc"))

    @vpc.setter
    def vpc(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee984da1d0f2760e1883bf9d58e7d6de36dccecdfa2be24d12068daf206a527a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpc", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatabaseMigrationServiceMigrationJobReverseSshConnectivity]:
        return typing.cast(typing.Optional[DatabaseMigrationServiceMigrationJobReverseSshConnectivity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatabaseMigrationServiceMigrationJobReverseSshConnectivity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a49f34693e67503299cd20cae523df42db698bcec9dc4c782435fa59fa8a4b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.databaseMigrationServiceMigrationJob.DatabaseMigrationServiceMigrationJobStaticIpConnectivity",
    jsii_struct_bases=[],
    name_mapping={},
)
class DatabaseMigrationServiceMigrationJobStaticIpConnectivity:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseMigrationServiceMigrationJobStaticIpConnectivity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabaseMigrationServiceMigrationJobStaticIpConnectivityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.databaseMigrationServiceMigrationJob.DatabaseMigrationServiceMigrationJobStaticIpConnectivityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__91ee657dbc9a78a9ea029fd01017034212351f4342ab18ae0441eebb552fea65)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatabaseMigrationServiceMigrationJobStaticIpConnectivity]:
        return typing.cast(typing.Optional[DatabaseMigrationServiceMigrationJobStaticIpConnectivity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatabaseMigrationServiceMigrationJobStaticIpConnectivity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c831a5ea8b6d30618cb28c4ca774e6263854a704ede218531f792c745a81925d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.databaseMigrationServiceMigrationJob.DatabaseMigrationServiceMigrationJobTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DatabaseMigrationServiceMigrationJobTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#create DatabaseMigrationServiceMigrationJob#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#delete DatabaseMigrationServiceMigrationJob#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#update DatabaseMigrationServiceMigrationJob#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc817e0b7cfbef7ef6b2762c5d5d615486b4972c784999a5c04344c209948629)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#create DatabaseMigrationServiceMigrationJob#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#delete DatabaseMigrationServiceMigrationJob#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#update DatabaseMigrationServiceMigrationJob#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseMigrationServiceMigrationJobTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabaseMigrationServiceMigrationJobTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.databaseMigrationServiceMigrationJob.DatabaseMigrationServiceMigrationJobTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c4e6e19ea918d29b8351594412c08fb75362e4284c06655a81266db47e60739)
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
            type_hints = typing.get_type_hints(_typecheckingstub__15852912fd2eecf25dd2f2f33d6a067ae1a00209ce9362d5d1dea1f35540a4c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0177969bdd1bfb625330fbca6accbb5192f2de51b354fdcf2b41509b553bc17a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10b6c5dab92f061bc64939ba8df9813bdad1f30b496027c4a0566009dd231b1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseMigrationServiceMigrationJobTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseMigrationServiceMigrationJobTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseMigrationServiceMigrationJobTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99a972c4f3feb47e9d955621bd142db14445bf64729e5abcb08a27d33406b279)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.databaseMigrationServiceMigrationJob.DatabaseMigrationServiceMigrationJobVpcPeeringConnectivity",
    jsii_struct_bases=[],
    name_mapping={"vpc": "vpc"},
)
class DatabaseMigrationServiceMigrationJobVpcPeeringConnectivity:
    def __init__(self, *, vpc: typing.Optional[builtins.str] = None) -> None:
        '''
        :param vpc: The name of the VPC network to peer with the Cloud SQL private network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#vpc DatabaseMigrationServiceMigrationJob#vpc}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10968b78b09d84b09840093ccf8bc4c76e368fabddb2bca9ad359a5749b811fb)
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def vpc(self) -> typing.Optional[builtins.str]:
        '''The name of the VPC network to peer with the Cloud SQL private network.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_migration_job#vpc DatabaseMigrationServiceMigrationJob#vpc}
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseMigrationServiceMigrationJobVpcPeeringConnectivity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabaseMigrationServiceMigrationJobVpcPeeringConnectivityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.databaseMigrationServiceMigrationJob.DatabaseMigrationServiceMigrationJobVpcPeeringConnectivityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__445b192af48d7238ae3e542291f5f9e18b0d57b30d92677d5bc49537d0ef6838)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetVpc")
    def reset_vpc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpc", []))

    @builtins.property
    @jsii.member(jsii_name="vpcInput")
    def vpc_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcInput"))

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpc"))

    @vpc.setter
    def vpc(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70b740fa642ce7ee33eb9c479cb3c78180786c8edbf356f84552e97b48fc3e2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpc", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatabaseMigrationServiceMigrationJobVpcPeeringConnectivity]:
        return typing.cast(typing.Optional[DatabaseMigrationServiceMigrationJobVpcPeeringConnectivity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatabaseMigrationServiceMigrationJobVpcPeeringConnectivity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63d0b37685b7f185cabc3cc9889a22d2124e4ee06cf2392608bb3f7aa88ef45c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DatabaseMigrationServiceMigrationJob",
    "DatabaseMigrationServiceMigrationJobConfig",
    "DatabaseMigrationServiceMigrationJobDumpFlags",
    "DatabaseMigrationServiceMigrationJobDumpFlagsDumpFlags",
    "DatabaseMigrationServiceMigrationJobDumpFlagsDumpFlagsList",
    "DatabaseMigrationServiceMigrationJobDumpFlagsDumpFlagsOutputReference",
    "DatabaseMigrationServiceMigrationJobDumpFlagsOutputReference",
    "DatabaseMigrationServiceMigrationJobError",
    "DatabaseMigrationServiceMigrationJobErrorList",
    "DatabaseMigrationServiceMigrationJobErrorOutputReference",
    "DatabaseMigrationServiceMigrationJobPerformanceConfig",
    "DatabaseMigrationServiceMigrationJobPerformanceConfigOutputReference",
    "DatabaseMigrationServiceMigrationJobReverseSshConnectivity",
    "DatabaseMigrationServiceMigrationJobReverseSshConnectivityOutputReference",
    "DatabaseMigrationServiceMigrationJobStaticIpConnectivity",
    "DatabaseMigrationServiceMigrationJobStaticIpConnectivityOutputReference",
    "DatabaseMigrationServiceMigrationJobTimeouts",
    "DatabaseMigrationServiceMigrationJobTimeoutsOutputReference",
    "DatabaseMigrationServiceMigrationJobVpcPeeringConnectivity",
    "DatabaseMigrationServiceMigrationJobVpcPeeringConnectivityOutputReference",
]

publication.publish()

def _typecheckingstub__053da1f8f4d53afb658336ff30a0a630019af8c123c923b88bdc7aa4c399b6e5(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    destination: builtins.str,
    migration_job_id: builtins.str,
    source: builtins.str,
    type: builtins.str,
    display_name: typing.Optional[builtins.str] = None,
    dump_flags: typing.Optional[typing.Union[DatabaseMigrationServiceMigrationJobDumpFlags, typing.Dict[builtins.str, typing.Any]]] = None,
    dump_path: typing.Optional[builtins.str] = None,
    dump_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    performance_config: typing.Optional[typing.Union[DatabaseMigrationServiceMigrationJobPerformanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    reverse_ssh_connectivity: typing.Optional[typing.Union[DatabaseMigrationServiceMigrationJobReverseSshConnectivity, typing.Dict[builtins.str, typing.Any]]] = None,
    static_ip_connectivity: typing.Optional[typing.Union[DatabaseMigrationServiceMigrationJobStaticIpConnectivity, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[DatabaseMigrationServiceMigrationJobTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc_peering_connectivity: typing.Optional[typing.Union[DatabaseMigrationServiceMigrationJobVpcPeeringConnectivity, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__1ed180d53fe4075daa30981e16fd9c7bcff0c539ffcd0a8291d08fe90e77e223(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eab8886a68043c9b8a4b73008d6c6133bbef722f6925951154673123038301b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60e521f88f083189a8251199abe0e90aa7e6270f76394931d9797d7cbe195d6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e8fa56bccb106c245b89ea17b9c2bcca187ca9037ba9f328d2cb62a69f7f398(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f86479f6195bee3240513b49a47a3761655542322b71d00723e4fdb7cb452fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__621fd589779ff13febf46fd7a68c64aa7497e43f16ad12c85949b3b3339cf3aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c7b572a58162be65a7d12c83db3273bc2426f069db985b1b17a0a457e20f4ed(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c8b8a032949f743958b2eb37f63702b724ba5f719540267c8c457eddb687fb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f78ee9c2fd72740ea74ef41133de56d5318a0af37eafee7e89f81b04c0d6c228(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f11a0563e3618889326784a010c54f441a4230e4810266da89b2a957af2df35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__388eadbb07c71ae51413669224f6fb96fc70e7a17c95848a024de19f031812e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f553604bb06b486c85f31a190320457c95f609466a9e9487bc84abf37935071f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7470698f11c2d90169475413ca058a75c743b19faa1fdb22552b5bc313f32d6f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    destination: builtins.str,
    migration_job_id: builtins.str,
    source: builtins.str,
    type: builtins.str,
    display_name: typing.Optional[builtins.str] = None,
    dump_flags: typing.Optional[typing.Union[DatabaseMigrationServiceMigrationJobDumpFlags, typing.Dict[builtins.str, typing.Any]]] = None,
    dump_path: typing.Optional[builtins.str] = None,
    dump_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    performance_config: typing.Optional[typing.Union[DatabaseMigrationServiceMigrationJobPerformanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    reverse_ssh_connectivity: typing.Optional[typing.Union[DatabaseMigrationServiceMigrationJobReverseSshConnectivity, typing.Dict[builtins.str, typing.Any]]] = None,
    static_ip_connectivity: typing.Optional[typing.Union[DatabaseMigrationServiceMigrationJobStaticIpConnectivity, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[DatabaseMigrationServiceMigrationJobTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc_peering_connectivity: typing.Optional[typing.Union[DatabaseMigrationServiceMigrationJobVpcPeeringConnectivity, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37c171612646792f83ac0e489aea4bc81867271abefcf1cd0e499e9de086703b(
    *,
    dump_flags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseMigrationServiceMigrationJobDumpFlagsDumpFlags, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b40dd2a9a75640db507bc46dc1b73afa88a399bea7729ddb42091bba4a841623(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec6dcd9c2df9f94522f7a300c51b6290315116fc0e610bb607d1b292856e478f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa75d54cd34b26d1547da3d071fbf852b1910cb5cb9c39ba8c396439d0d45809(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__270376b6bfd9862aebb219714c02c345433834c73ace2ed3c58ce1d11b07f7dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e47c75dd37bb45dd0c8802f9fa24d8bc33e783d25147e5d9e85069cdfd2c6514(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f034ea4f9727a6c723cb687c1d2f40ebb00cdd740a9b6552a670ae39756c3f7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f417a410b6216e093767b7dc2f61be736df6e10bd4d22474a954b537a968991(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseMigrationServiceMigrationJobDumpFlagsDumpFlags]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0c7b00989c7f07bd134b1527f561aa557064ec56118cb418539f1f9ec2887af(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03ee76545693c8712f4749bae8b2f3c191cfc0109126e6708e9d20302933ae0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__198bb17e9ddb455848cb8d0d8a9dc2f7731be4cbfcfcafe4f0e7eae00630248f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2503414db05af0ea5b5e139d1518a8640ee9eb33b5659887c0d2e7cc3086ed9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseMigrationServiceMigrationJobDumpFlagsDumpFlags]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee0f3a979ae4a105e0376a313f02d40d28ec6bd0755b39c5b2108c4f62cea23f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da9e93b6450f28e10f3598093ff84a31a5cdef5d1c288fde11edd9c1623e8136(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseMigrationServiceMigrationJobDumpFlagsDumpFlags, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10bdef07a9db060d5fda5a13075397c2a7b4ac6018678f9dfbdd5761666d2c7f(
    value: typing.Optional[DatabaseMigrationServiceMigrationJobDumpFlags],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__248e9d97f8a67bb5ec8ceb4c90f378c2d45e33ca67549bd4cb5b7fe8cdf320d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4a7769766040d25e1ee532329bb370755e6f2311d2861e8aeaa34c9b389649d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab5e7b6269d4560a0d19826cf94180cbd04803bac6838f98fc31c23f6b9d7558(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f823e351ff84ca3ef9077a5d4322787559448a06cfe0cd05f3e871985ad4cd45(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d71dffda3f804b109e5b54975fbc59e11846a1c91af54e8232aae9d120b73168(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__959d848302b90f7b3e4ccb75035c75aefa8a0c7d114039996ff43c2b620d6db3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8d22189ffd431e8da1a967dbd193a84bfdd6926aeeb6f71b3c018870eab1bf2(
    value: typing.Optional[DatabaseMigrationServiceMigrationJobError],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__230652fa8a4481f8929f273e7b439dfba50b61fe0f607c3743b30bb2eba39176(
    *,
    dump_parallel_level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__695da165626928757a7d3ae3282c82dd31f2787dd9625902d71559f86fd630de(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0d50a26f2b414c46481e979a8d9ca994dd353ceac3f2965f84ce1a0b3943597(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38be8d6ab9262664d0255592bb12f4cb1b60db67280171e0337145641868a4e5(
    value: typing.Optional[DatabaseMigrationServiceMigrationJobPerformanceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acc4c7c0358e6b62981809912f3c42fcaff033d78dee0e49770121d6828f5846(
    *,
    vm: typing.Optional[builtins.str] = None,
    vm_ip: typing.Optional[builtins.str] = None,
    vm_port: typing.Optional[jsii.Number] = None,
    vpc: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce288961c6a19ab8b11abc94f892d6532a6c39cf8b11e81186ba8a15f62dbfc3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4fbc08c68505944d7efbbb6b72d90844b2e79cd662c87d0b5305d9fefdfbf25(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db8314f2d0a9b0660c54462acbbcd040d8c7f448fa6b90dbcdf86283004d3237(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cec9fe785abd66e2ed35d10ee58231ce1a4d1c2483ed88a20a6cd9b55be8b927(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee984da1d0f2760e1883bf9d58e7d6de36dccecdfa2be24d12068daf206a527a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a49f34693e67503299cd20cae523df42db698bcec9dc4c782435fa59fa8a4b6(
    value: typing.Optional[DatabaseMigrationServiceMigrationJobReverseSshConnectivity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91ee657dbc9a78a9ea029fd01017034212351f4342ab18ae0441eebb552fea65(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c831a5ea8b6d30618cb28c4ca774e6263854a704ede218531f792c745a81925d(
    value: typing.Optional[DatabaseMigrationServiceMigrationJobStaticIpConnectivity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc817e0b7cfbef7ef6b2762c5d5d615486b4972c784999a5c04344c209948629(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c4e6e19ea918d29b8351594412c08fb75362e4284c06655a81266db47e60739(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15852912fd2eecf25dd2f2f33d6a067ae1a00209ce9362d5d1dea1f35540a4c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0177969bdd1bfb625330fbca6accbb5192f2de51b354fdcf2b41509b553bc17a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10b6c5dab92f061bc64939ba8df9813bdad1f30b496027c4a0566009dd231b1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99a972c4f3feb47e9d955621bd142db14445bf64729e5abcb08a27d33406b279(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseMigrationServiceMigrationJobTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10968b78b09d84b09840093ccf8bc4c76e368fabddb2bca9ad359a5749b811fb(
    *,
    vpc: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__445b192af48d7238ae3e542291f5f9e18b0d57b30d92677d5bc49537d0ef6838(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70b740fa642ce7ee33eb9c479cb3c78180786c8edbf356f84552e97b48fc3e2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63d0b37685b7f185cabc3cc9889a22d2124e4ee06cf2392608bb3f7aa88ef45c(
    value: typing.Optional[DatabaseMigrationServiceMigrationJobVpcPeeringConnectivity],
) -> None:
    """Type checking stubs"""
    pass
