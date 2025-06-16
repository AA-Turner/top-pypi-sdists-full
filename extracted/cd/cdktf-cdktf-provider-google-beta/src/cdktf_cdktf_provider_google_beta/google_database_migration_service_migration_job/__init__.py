r'''
# `google_database_migration_service_migration_job`

Refer to the Terraform Registry for docs: [`google_database_migration_service_migration_job`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job).
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


class GoogleDatabaseMigrationServiceMigrationJob(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceMigrationJob.GoogleDatabaseMigrationServiceMigrationJob",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job google_database_migration_service_migration_job}.'''

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
        dump_flags: typing.Optional[typing.Union["GoogleDatabaseMigrationServiceMigrationJobDumpFlags", typing.Dict[builtins.str, typing.Any]]] = None,
        dump_path: typing.Optional[builtins.str] = None,
        dump_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        performance_config: typing.Optional[typing.Union["GoogleDatabaseMigrationServiceMigrationJobPerformanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        reverse_ssh_connectivity: typing.Optional[typing.Union["GoogleDatabaseMigrationServiceMigrationJobReverseSshConnectivity", typing.Dict[builtins.str, typing.Any]]] = None,
        static_ip_connectivity: typing.Optional[typing.Union["GoogleDatabaseMigrationServiceMigrationJobStaticIpConnectivity", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleDatabaseMigrationServiceMigrationJobTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_peering_connectivity: typing.Optional[typing.Union["GoogleDatabaseMigrationServiceMigrationJobVpcPeeringConnectivity", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job google_database_migration_service_migration_job} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param destination: The name of the destination connection profile resource in the form of projects/{project}/locations/{location}/connectionProfiles/{destinationConnectionProfile}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#destination GoogleDatabaseMigrationServiceMigrationJob#destination}
        :param migration_job_id: The ID of the migration job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#migration_job_id GoogleDatabaseMigrationServiceMigrationJob#migration_job_id}
        :param source: The name of the source connection profile resource in the form of projects/{project}/locations/{location}/connectionProfiles/{sourceConnectionProfile}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#source GoogleDatabaseMigrationServiceMigrationJob#source}
        :param type: The type of the migration job. Possible values: ["ONE_TIME", "CONTINUOUS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#type GoogleDatabaseMigrationServiceMigrationJob#type}
        :param display_name: The migration job display name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#display_name GoogleDatabaseMigrationServiceMigrationJob#display_name}
        :param dump_flags: dump_flags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#dump_flags GoogleDatabaseMigrationServiceMigrationJob#dump_flags}
        :param dump_path: The path to the dump file in Google Cloud Storage, in the format: (gs://[BUCKET_NAME]/[OBJECT_NAME]). This field and the "dump_flags" field are mutually exclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#dump_path GoogleDatabaseMigrationServiceMigrationJob#dump_path}
        :param dump_type: The type of the data dump. Supported for MySQL to CloudSQL for MySQL migrations only. Possible values: ["LOGICAL", "PHYSICAL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#dump_type GoogleDatabaseMigrationServiceMigrationJob#dump_type}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#id GoogleDatabaseMigrationServiceMigrationJob#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The resource labels for migration job to use to annotate any related underlying resources such as Compute Engine VMs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#labels GoogleDatabaseMigrationServiceMigrationJob#labels}
        :param location: The location where the migration job should reside. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#location GoogleDatabaseMigrationServiceMigrationJob#location}
        :param performance_config: performance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#performance_config GoogleDatabaseMigrationServiceMigrationJob#performance_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#project GoogleDatabaseMigrationServiceMigrationJob#project}.
        :param reverse_ssh_connectivity: reverse_ssh_connectivity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#reverse_ssh_connectivity GoogleDatabaseMigrationServiceMigrationJob#reverse_ssh_connectivity}
        :param static_ip_connectivity: static_ip_connectivity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#static_ip_connectivity GoogleDatabaseMigrationServiceMigrationJob#static_ip_connectivity}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#timeouts GoogleDatabaseMigrationServiceMigrationJob#timeouts}
        :param vpc_peering_connectivity: vpc_peering_connectivity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#vpc_peering_connectivity GoogleDatabaseMigrationServiceMigrationJob#vpc_peering_connectivity}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9095370a9146c7d2acaccbbfad850cdf8cf7ea4ebce607a59d052a3e174acb43)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleDatabaseMigrationServiceMigrationJobConfig(
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
        '''Generates CDKTF code for importing a GoogleDatabaseMigrationServiceMigrationJob resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleDatabaseMigrationServiceMigrationJob to import.
        :param import_from_id: The id of the existing GoogleDatabaseMigrationServiceMigrationJob that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleDatabaseMigrationServiceMigrationJob to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fac205e15023ec56f6f725bbb3b390672070478298a3ca0312a6377bd2c1140)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDumpFlags")
    def put_dump_flags(
        self,
        *,
        dump_flags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDatabaseMigrationServiceMigrationJobDumpFlagsDumpFlags", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param dump_flags: dump_flags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#dump_flags GoogleDatabaseMigrationServiceMigrationJob#dump_flags}
        '''
        value = GoogleDatabaseMigrationServiceMigrationJobDumpFlags(
            dump_flags=dump_flags
        )

        return typing.cast(None, jsii.invoke(self, "putDumpFlags", [value]))

    @jsii.member(jsii_name="putPerformanceConfig")
    def put_performance_config(
        self,
        *,
        dump_parallel_level: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dump_parallel_level: Initial dump parallelism level. Possible values: ["MIN", "OPTIMAL", "MAX"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#dump_parallel_level GoogleDatabaseMigrationServiceMigrationJob#dump_parallel_level}
        '''
        value = GoogleDatabaseMigrationServiceMigrationJobPerformanceConfig(
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
        :param vm: The name of the virtual machine (Compute Engine) used as the bastion server for the SSH tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#vm GoogleDatabaseMigrationServiceMigrationJob#vm}
        :param vm_ip: The IP of the virtual machine (Compute Engine) used as the bastion server for the SSH tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#vm_ip GoogleDatabaseMigrationServiceMigrationJob#vm_ip}
        :param vm_port: The forwarding port of the virtual machine (Compute Engine) used as the bastion server for the SSH tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#vm_port GoogleDatabaseMigrationServiceMigrationJob#vm_port}
        :param vpc: The name of the VPC to peer with the Cloud SQL private network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#vpc GoogleDatabaseMigrationServiceMigrationJob#vpc}
        '''
        value = GoogleDatabaseMigrationServiceMigrationJobReverseSshConnectivity(
            vm=vm, vm_ip=vm_ip, vm_port=vm_port, vpc=vpc
        )

        return typing.cast(None, jsii.invoke(self, "putReverseSshConnectivity", [value]))

    @jsii.member(jsii_name="putStaticIpConnectivity")
    def put_static_ip_connectivity(self) -> None:
        value = GoogleDatabaseMigrationServiceMigrationJobStaticIpConnectivity()

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#create GoogleDatabaseMigrationServiceMigrationJob#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#delete GoogleDatabaseMigrationServiceMigrationJob#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#update GoogleDatabaseMigrationServiceMigrationJob#update}.
        '''
        value = GoogleDatabaseMigrationServiceMigrationJobTimeouts(
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
        :param vpc: The name of the VPC network to peer with the Cloud SQL private network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#vpc GoogleDatabaseMigrationServiceMigrationJob#vpc}
        '''
        value = GoogleDatabaseMigrationServiceMigrationJobVpcPeeringConnectivity(
            vpc=vpc
        )

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
    ) -> "GoogleDatabaseMigrationServiceMigrationJobDumpFlagsOutputReference":
        return typing.cast("GoogleDatabaseMigrationServiceMigrationJobDumpFlagsOutputReference", jsii.get(self, "dumpFlags"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="error")
    def error(self) -> "GoogleDatabaseMigrationServiceMigrationJobErrorList":
        return typing.cast("GoogleDatabaseMigrationServiceMigrationJobErrorList", jsii.get(self, "error"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="performanceConfig")
    def performance_config(
        self,
    ) -> "GoogleDatabaseMigrationServiceMigrationJobPerformanceConfigOutputReference":
        return typing.cast("GoogleDatabaseMigrationServiceMigrationJobPerformanceConfigOutputReference", jsii.get(self, "performanceConfig"))

    @builtins.property
    @jsii.member(jsii_name="phase")
    def phase(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "phase"))

    @builtins.property
    @jsii.member(jsii_name="reverseSshConnectivity")
    def reverse_ssh_connectivity(
        self,
    ) -> "GoogleDatabaseMigrationServiceMigrationJobReverseSshConnectivityOutputReference":
        return typing.cast("GoogleDatabaseMigrationServiceMigrationJobReverseSshConnectivityOutputReference", jsii.get(self, "reverseSshConnectivity"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="staticIpConnectivity")
    def static_ip_connectivity(
        self,
    ) -> "GoogleDatabaseMigrationServiceMigrationJobStaticIpConnectivityOutputReference":
        return typing.cast("GoogleDatabaseMigrationServiceMigrationJobStaticIpConnectivityOutputReference", jsii.get(self, "staticIpConnectivity"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "GoogleDatabaseMigrationServiceMigrationJobTimeoutsOutputReference":
        return typing.cast("GoogleDatabaseMigrationServiceMigrationJobTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="vpcPeeringConnectivity")
    def vpc_peering_connectivity(
        self,
    ) -> "GoogleDatabaseMigrationServiceMigrationJobVpcPeeringConnectivityOutputReference":
        return typing.cast("GoogleDatabaseMigrationServiceMigrationJobVpcPeeringConnectivityOutputReference", jsii.get(self, "vpcPeeringConnectivity"))

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
    ) -> typing.Optional["GoogleDatabaseMigrationServiceMigrationJobDumpFlags"]:
        return typing.cast(typing.Optional["GoogleDatabaseMigrationServiceMigrationJobDumpFlags"], jsii.get(self, "dumpFlagsInput"))

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
    ) -> typing.Optional["GoogleDatabaseMigrationServiceMigrationJobPerformanceConfig"]:
        return typing.cast(typing.Optional["GoogleDatabaseMigrationServiceMigrationJobPerformanceConfig"], jsii.get(self, "performanceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="reverseSshConnectivityInput")
    def reverse_ssh_connectivity_input(
        self,
    ) -> typing.Optional["GoogleDatabaseMigrationServiceMigrationJobReverseSshConnectivity"]:
        return typing.cast(typing.Optional["GoogleDatabaseMigrationServiceMigrationJobReverseSshConnectivity"], jsii.get(self, "reverseSshConnectivityInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="staticIpConnectivityInput")
    def static_ip_connectivity_input(
        self,
    ) -> typing.Optional["GoogleDatabaseMigrationServiceMigrationJobStaticIpConnectivity"]:
        return typing.cast(typing.Optional["GoogleDatabaseMigrationServiceMigrationJobStaticIpConnectivity"], jsii.get(self, "staticIpConnectivityInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDatabaseMigrationServiceMigrationJobTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDatabaseMigrationServiceMigrationJobTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcPeeringConnectivityInput")
    def vpc_peering_connectivity_input(
        self,
    ) -> typing.Optional["GoogleDatabaseMigrationServiceMigrationJobVpcPeeringConnectivity"]:
        return typing.cast(typing.Optional["GoogleDatabaseMigrationServiceMigrationJobVpcPeeringConnectivity"], jsii.get(self, "vpcPeeringConnectivityInput"))

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destination"))

    @destination.setter
    def destination(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03e943cf6afc75e055c99737a000e326543658ad409c4ac9aec7fe7d68b19176)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e140536e62d6912f086ac8a9e3ebae8ed1798792ae8e603d85449a3741311b90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dumpPath")
    def dump_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dumpPath"))

    @dump_path.setter
    def dump_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5ee69b566483bfb6de98a52596edade830b49ff07c53944e4eeb5753a660444)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dumpPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dumpType")
    def dump_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dumpType"))

    @dump_type.setter
    def dump_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26348a8f8f45abe84678096476bbd454f93e9f494bd2bd56e980cc151315286d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dumpType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d8ebc9cb3c2679307d6f0e50ab5e5574b93a351a7cd92d60757baefd3eb7535)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d442459951ff0ba0822d8539e0ccdef63ea567ff00f8d2e7b4189347cc98b04c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e01dd08ca07cb728b327a8ca689a94b8a39f782c1e740acd31d30b799153c9c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="migrationJobId")
    def migration_job_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "migrationJobId"))

    @migration_job_id.setter
    def migration_job_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b6e4c1cdfab2176d606734b3f32fe907ac0701f5d14ca73813dfd868f116f40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "migrationJobId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1071564883cfccc52a24e2448ebcabd7a2dd970d681c46b9338ae8de637dcca5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acc32c12720661315d10d31b9b2c9f8be11310974aef95639ae5e358390b3b9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76e8cd8ae0c0c4d878bb6f3698d67d8f7941a10ee74c95e8c2caaafde615a813)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceMigrationJob.GoogleDatabaseMigrationServiceMigrationJobConfig",
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
class GoogleDatabaseMigrationServiceMigrationJobConfig(
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
        dump_flags: typing.Optional[typing.Union["GoogleDatabaseMigrationServiceMigrationJobDumpFlags", typing.Dict[builtins.str, typing.Any]]] = None,
        dump_path: typing.Optional[builtins.str] = None,
        dump_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        performance_config: typing.Optional[typing.Union["GoogleDatabaseMigrationServiceMigrationJobPerformanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        reverse_ssh_connectivity: typing.Optional[typing.Union["GoogleDatabaseMigrationServiceMigrationJobReverseSshConnectivity", typing.Dict[builtins.str, typing.Any]]] = None,
        static_ip_connectivity: typing.Optional[typing.Union["GoogleDatabaseMigrationServiceMigrationJobStaticIpConnectivity", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleDatabaseMigrationServiceMigrationJobTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_peering_connectivity: typing.Optional[typing.Union["GoogleDatabaseMigrationServiceMigrationJobVpcPeeringConnectivity", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param destination: The name of the destination connection profile resource in the form of projects/{project}/locations/{location}/connectionProfiles/{destinationConnectionProfile}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#destination GoogleDatabaseMigrationServiceMigrationJob#destination}
        :param migration_job_id: The ID of the migration job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#migration_job_id GoogleDatabaseMigrationServiceMigrationJob#migration_job_id}
        :param source: The name of the source connection profile resource in the form of projects/{project}/locations/{location}/connectionProfiles/{sourceConnectionProfile}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#source GoogleDatabaseMigrationServiceMigrationJob#source}
        :param type: The type of the migration job. Possible values: ["ONE_TIME", "CONTINUOUS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#type GoogleDatabaseMigrationServiceMigrationJob#type}
        :param display_name: The migration job display name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#display_name GoogleDatabaseMigrationServiceMigrationJob#display_name}
        :param dump_flags: dump_flags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#dump_flags GoogleDatabaseMigrationServiceMigrationJob#dump_flags}
        :param dump_path: The path to the dump file in Google Cloud Storage, in the format: (gs://[BUCKET_NAME]/[OBJECT_NAME]). This field and the "dump_flags" field are mutually exclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#dump_path GoogleDatabaseMigrationServiceMigrationJob#dump_path}
        :param dump_type: The type of the data dump. Supported for MySQL to CloudSQL for MySQL migrations only. Possible values: ["LOGICAL", "PHYSICAL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#dump_type GoogleDatabaseMigrationServiceMigrationJob#dump_type}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#id GoogleDatabaseMigrationServiceMigrationJob#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The resource labels for migration job to use to annotate any related underlying resources such as Compute Engine VMs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#labels GoogleDatabaseMigrationServiceMigrationJob#labels}
        :param location: The location where the migration job should reside. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#location GoogleDatabaseMigrationServiceMigrationJob#location}
        :param performance_config: performance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#performance_config GoogleDatabaseMigrationServiceMigrationJob#performance_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#project GoogleDatabaseMigrationServiceMigrationJob#project}.
        :param reverse_ssh_connectivity: reverse_ssh_connectivity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#reverse_ssh_connectivity GoogleDatabaseMigrationServiceMigrationJob#reverse_ssh_connectivity}
        :param static_ip_connectivity: static_ip_connectivity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#static_ip_connectivity GoogleDatabaseMigrationServiceMigrationJob#static_ip_connectivity}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#timeouts GoogleDatabaseMigrationServiceMigrationJob#timeouts}
        :param vpc_peering_connectivity: vpc_peering_connectivity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#vpc_peering_connectivity GoogleDatabaseMigrationServiceMigrationJob#vpc_peering_connectivity}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(dump_flags, dict):
            dump_flags = GoogleDatabaseMigrationServiceMigrationJobDumpFlags(**dump_flags)
        if isinstance(performance_config, dict):
            performance_config = GoogleDatabaseMigrationServiceMigrationJobPerformanceConfig(**performance_config)
        if isinstance(reverse_ssh_connectivity, dict):
            reverse_ssh_connectivity = GoogleDatabaseMigrationServiceMigrationJobReverseSshConnectivity(**reverse_ssh_connectivity)
        if isinstance(static_ip_connectivity, dict):
            static_ip_connectivity = GoogleDatabaseMigrationServiceMigrationJobStaticIpConnectivity(**static_ip_connectivity)
        if isinstance(timeouts, dict):
            timeouts = GoogleDatabaseMigrationServiceMigrationJobTimeouts(**timeouts)
        if isinstance(vpc_peering_connectivity, dict):
            vpc_peering_connectivity = GoogleDatabaseMigrationServiceMigrationJobVpcPeeringConnectivity(**vpc_peering_connectivity)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fe569e65986014381d002b563b2146c7d162a8d31855d087928c4b215283cab)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#destination GoogleDatabaseMigrationServiceMigrationJob#destination}
        '''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def migration_job_id(self) -> builtins.str:
        '''The ID of the migration job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#migration_job_id GoogleDatabaseMigrationServiceMigrationJob#migration_job_id}
        '''
        result = self._values.get("migration_job_id")
        assert result is not None, "Required property 'migration_job_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source(self) -> builtins.str:
        '''The name of the source connection profile resource in the form of projects/{project}/locations/{location}/connectionProfiles/{sourceConnectionProfile}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#source GoogleDatabaseMigrationServiceMigrationJob#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of the migration job. Possible values: ["ONE_TIME", "CONTINUOUS"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#type GoogleDatabaseMigrationServiceMigrationJob#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The migration job display name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#display_name GoogleDatabaseMigrationServiceMigrationJob#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dump_flags(
        self,
    ) -> typing.Optional["GoogleDatabaseMigrationServiceMigrationJobDumpFlags"]:
        '''dump_flags block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#dump_flags GoogleDatabaseMigrationServiceMigrationJob#dump_flags}
        '''
        result = self._values.get("dump_flags")
        return typing.cast(typing.Optional["GoogleDatabaseMigrationServiceMigrationJobDumpFlags"], result)

    @builtins.property
    def dump_path(self) -> typing.Optional[builtins.str]:
        '''The path to the dump file in Google Cloud Storage, in the format: (gs://[BUCKET_NAME]/[OBJECT_NAME]).

        This field and the "dump_flags" field are mutually exclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#dump_path GoogleDatabaseMigrationServiceMigrationJob#dump_path}
        '''
        result = self._values.get("dump_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dump_type(self) -> typing.Optional[builtins.str]:
        '''The type of the data dump. Supported for MySQL to CloudSQL for MySQL migrations only. Possible values: ["LOGICAL", "PHYSICAL"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#dump_type GoogleDatabaseMigrationServiceMigrationJob#dump_type}
        '''
        result = self._values.get("dump_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#id GoogleDatabaseMigrationServiceMigrationJob#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#labels GoogleDatabaseMigrationServiceMigrationJob#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The location where the migration job should reside.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#location GoogleDatabaseMigrationServiceMigrationJob#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def performance_config(
        self,
    ) -> typing.Optional["GoogleDatabaseMigrationServiceMigrationJobPerformanceConfig"]:
        '''performance_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#performance_config GoogleDatabaseMigrationServiceMigrationJob#performance_config}
        '''
        result = self._values.get("performance_config")
        return typing.cast(typing.Optional["GoogleDatabaseMigrationServiceMigrationJobPerformanceConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#project GoogleDatabaseMigrationServiceMigrationJob#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reverse_ssh_connectivity(
        self,
    ) -> typing.Optional["GoogleDatabaseMigrationServiceMigrationJobReverseSshConnectivity"]:
        '''reverse_ssh_connectivity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#reverse_ssh_connectivity GoogleDatabaseMigrationServiceMigrationJob#reverse_ssh_connectivity}
        '''
        result = self._values.get("reverse_ssh_connectivity")
        return typing.cast(typing.Optional["GoogleDatabaseMigrationServiceMigrationJobReverseSshConnectivity"], result)

    @builtins.property
    def static_ip_connectivity(
        self,
    ) -> typing.Optional["GoogleDatabaseMigrationServiceMigrationJobStaticIpConnectivity"]:
        '''static_ip_connectivity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#static_ip_connectivity GoogleDatabaseMigrationServiceMigrationJob#static_ip_connectivity}
        '''
        result = self._values.get("static_ip_connectivity")
        return typing.cast(typing.Optional["GoogleDatabaseMigrationServiceMigrationJobStaticIpConnectivity"], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleDatabaseMigrationServiceMigrationJobTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#timeouts GoogleDatabaseMigrationServiceMigrationJob#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleDatabaseMigrationServiceMigrationJobTimeouts"], result)

    @builtins.property
    def vpc_peering_connectivity(
        self,
    ) -> typing.Optional["GoogleDatabaseMigrationServiceMigrationJobVpcPeeringConnectivity"]:
        '''vpc_peering_connectivity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#vpc_peering_connectivity GoogleDatabaseMigrationServiceMigrationJob#vpc_peering_connectivity}
        '''
        result = self._values.get("vpc_peering_connectivity")
        return typing.cast(typing.Optional["GoogleDatabaseMigrationServiceMigrationJobVpcPeeringConnectivity"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDatabaseMigrationServiceMigrationJobConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceMigrationJob.GoogleDatabaseMigrationServiceMigrationJobDumpFlags",
    jsii_struct_bases=[],
    name_mapping={"dump_flags": "dumpFlags"},
)
class GoogleDatabaseMigrationServiceMigrationJobDumpFlags:
    def __init__(
        self,
        *,
        dump_flags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDatabaseMigrationServiceMigrationJobDumpFlagsDumpFlags", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param dump_flags: dump_flags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#dump_flags GoogleDatabaseMigrationServiceMigrationJob#dump_flags}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd8f92e276c073f794415a76ea10e81a0957c4467777f2e5cc6e3f756d963f39)
            check_type(argname="argument dump_flags", value=dump_flags, expected_type=type_hints["dump_flags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dump_flags is not None:
            self._values["dump_flags"] = dump_flags

    @builtins.property
    def dump_flags(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDatabaseMigrationServiceMigrationJobDumpFlagsDumpFlags"]]]:
        '''dump_flags block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#dump_flags GoogleDatabaseMigrationServiceMigrationJob#dump_flags}
        '''
        result = self._values.get("dump_flags")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDatabaseMigrationServiceMigrationJobDumpFlagsDumpFlags"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDatabaseMigrationServiceMigrationJobDumpFlags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceMigrationJob.GoogleDatabaseMigrationServiceMigrationJobDumpFlagsDumpFlags",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class GoogleDatabaseMigrationServiceMigrationJobDumpFlagsDumpFlags:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name of the flag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#name GoogleDatabaseMigrationServiceMigrationJob#name}
        :param value: The vale of the flag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#value GoogleDatabaseMigrationServiceMigrationJob#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf837975aefbe775d615fd52560a6fd8527e0528fdee8ea205b653f79a6a8620)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#name GoogleDatabaseMigrationServiceMigrationJob#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The vale of the flag.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#value GoogleDatabaseMigrationServiceMigrationJob#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDatabaseMigrationServiceMigrationJobDumpFlagsDumpFlags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDatabaseMigrationServiceMigrationJobDumpFlagsDumpFlagsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceMigrationJob.GoogleDatabaseMigrationServiceMigrationJobDumpFlagsDumpFlagsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5baa041c240079837a40236fea57cc6841a2a9747e5c7421d508199363d7746)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDatabaseMigrationServiceMigrationJobDumpFlagsDumpFlagsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13e0a9855b9cddd9c4df0c1dcf14ad14f136df4a25fabe5faab1519b3687dd26)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDatabaseMigrationServiceMigrationJobDumpFlagsDumpFlagsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30414a0f5c1baf15afcacb17cb0edd421d7f25401b719cf4923ce75c7bf2e358)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9bf08d1796aabdb223cf0ecf61888673f9e0e2a3cd6a292b2f53388cb664b34f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc73caab50e09cbf0dd9dd4e8c002b3a14cf8d7e8724021612ea4169f8b9d190)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDatabaseMigrationServiceMigrationJobDumpFlagsDumpFlags]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDatabaseMigrationServiceMigrationJobDumpFlagsDumpFlags]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDatabaseMigrationServiceMigrationJobDumpFlagsDumpFlags]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad530dd7cb62350ddbd6ab74fc913edd0db980cb6062f84e542dafe31bd2463b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDatabaseMigrationServiceMigrationJobDumpFlagsDumpFlagsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceMigrationJob.GoogleDatabaseMigrationServiceMigrationJobDumpFlagsDumpFlagsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5df031952b746d939ffda0b2b62f1fd9748808ba3c8b49a3d6dd0a02a1265d1e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6801bfdfcb9db8af5a2b50263ff14ab237e05f514c3f1f9be6313d455c01f1fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bce2dfdf1e541b4f0e581bdba135644308c3b78ee8bcd2538da0c4dc5933510a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDatabaseMigrationServiceMigrationJobDumpFlagsDumpFlags]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDatabaseMigrationServiceMigrationJobDumpFlagsDumpFlags]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDatabaseMigrationServiceMigrationJobDumpFlagsDumpFlags]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a69b72037c835077542a1e3812cb473eb1a62b0fb11e14e6b5f9da35ae8a253)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDatabaseMigrationServiceMigrationJobDumpFlagsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceMigrationJob.GoogleDatabaseMigrationServiceMigrationJobDumpFlagsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c1d6508d7643e62a2c116674373aed79b399f479454f23fddefbadf160a070e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDumpFlags")
    def put_dump_flags(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDatabaseMigrationServiceMigrationJobDumpFlagsDumpFlags, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f140649e2ad2aaa8e1490366bad8f60523b03344c6570f462640fd47125c6e84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDumpFlags", [value]))

    @jsii.member(jsii_name="resetDumpFlags")
    def reset_dump_flags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDumpFlags", []))

    @builtins.property
    @jsii.member(jsii_name="dumpFlags")
    def dump_flags(
        self,
    ) -> GoogleDatabaseMigrationServiceMigrationJobDumpFlagsDumpFlagsList:
        return typing.cast(GoogleDatabaseMigrationServiceMigrationJobDumpFlagsDumpFlagsList, jsii.get(self, "dumpFlags"))

    @builtins.property
    @jsii.member(jsii_name="dumpFlagsInput")
    def dump_flags_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDatabaseMigrationServiceMigrationJobDumpFlagsDumpFlags]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDatabaseMigrationServiceMigrationJobDumpFlagsDumpFlags]]], jsii.get(self, "dumpFlagsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDatabaseMigrationServiceMigrationJobDumpFlags]:
        return typing.cast(typing.Optional[GoogleDatabaseMigrationServiceMigrationJobDumpFlags], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDatabaseMigrationServiceMigrationJobDumpFlags],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40081de9905972e574f2b26393c90e55869e3c95df2d90faf09c1156a228ae4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceMigrationJob.GoogleDatabaseMigrationServiceMigrationJobError",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDatabaseMigrationServiceMigrationJobError:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDatabaseMigrationServiceMigrationJobError(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDatabaseMigrationServiceMigrationJobErrorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceMigrationJob.GoogleDatabaseMigrationServiceMigrationJobErrorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6837d016de895706d8b1a3a0d2fcfd32f21524cc26e2270fb938dc245e7cffa2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDatabaseMigrationServiceMigrationJobErrorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c5e204c7a60e3135f83369bcdf2292455f48b7468c7d0ad02249a5f8d67b4c8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDatabaseMigrationServiceMigrationJobErrorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c5d14268d3b931683a34c88d13fc5c8e5d5875f475a6f50dd24ad80db075326)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5eb313a344fd2b1b5d0333702d5a801381ed9d14772faa4968bcef858fa34cd9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd4a077ddb3d83e38a21552ebde9e2d3739da671dcaab67815d072196279a9a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleDatabaseMigrationServiceMigrationJobErrorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceMigrationJob.GoogleDatabaseMigrationServiceMigrationJobErrorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed6cd483719f214823b704fdeebaeff62cec57d604ac35e1dd4540cd4e9eeb35)
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
    ) -> typing.Optional[GoogleDatabaseMigrationServiceMigrationJobError]:
        return typing.cast(typing.Optional[GoogleDatabaseMigrationServiceMigrationJobError], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDatabaseMigrationServiceMigrationJobError],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3e166d1cfda7a8d5b41bb2e4286ec672defeedc54dc47c3d41bdb7b8f5e6667)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceMigrationJob.GoogleDatabaseMigrationServiceMigrationJobPerformanceConfig",
    jsii_struct_bases=[],
    name_mapping={"dump_parallel_level": "dumpParallelLevel"},
)
class GoogleDatabaseMigrationServiceMigrationJobPerformanceConfig:
    def __init__(
        self,
        *,
        dump_parallel_level: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dump_parallel_level: Initial dump parallelism level. Possible values: ["MIN", "OPTIMAL", "MAX"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#dump_parallel_level GoogleDatabaseMigrationServiceMigrationJob#dump_parallel_level}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cf34b5feb345097ed9f6434d7cc8074373bd15b9e77756e7307e1dfe917135d)
            check_type(argname="argument dump_parallel_level", value=dump_parallel_level, expected_type=type_hints["dump_parallel_level"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dump_parallel_level is not None:
            self._values["dump_parallel_level"] = dump_parallel_level

    @builtins.property
    def dump_parallel_level(self) -> typing.Optional[builtins.str]:
        '''Initial dump parallelism level. Possible values: ["MIN", "OPTIMAL", "MAX"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#dump_parallel_level GoogleDatabaseMigrationServiceMigrationJob#dump_parallel_level}
        '''
        result = self._values.get("dump_parallel_level")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDatabaseMigrationServiceMigrationJobPerformanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDatabaseMigrationServiceMigrationJobPerformanceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceMigrationJob.GoogleDatabaseMigrationServiceMigrationJobPerformanceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6c93fb9cacfe0538c9af425386caf45f4c2df3cf27bbce874de250bab978d1f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e729d3752eba1c6b2fd55cae896711f40fd211517e8d230426b25783db7170cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dumpParallelLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDatabaseMigrationServiceMigrationJobPerformanceConfig]:
        return typing.cast(typing.Optional[GoogleDatabaseMigrationServiceMigrationJobPerformanceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDatabaseMigrationServiceMigrationJobPerformanceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daa841d0e7a3e14b5051a7e8e1d1cef293906163b62e11c0430a46e2ca0cd397)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceMigrationJob.GoogleDatabaseMigrationServiceMigrationJobReverseSshConnectivity",
    jsii_struct_bases=[],
    name_mapping={"vm": "vm", "vm_ip": "vmIp", "vm_port": "vmPort", "vpc": "vpc"},
)
class GoogleDatabaseMigrationServiceMigrationJobReverseSshConnectivity:
    def __init__(
        self,
        *,
        vm: typing.Optional[builtins.str] = None,
        vm_ip: typing.Optional[builtins.str] = None,
        vm_port: typing.Optional[jsii.Number] = None,
        vpc: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param vm: The name of the virtual machine (Compute Engine) used as the bastion server for the SSH tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#vm GoogleDatabaseMigrationServiceMigrationJob#vm}
        :param vm_ip: The IP of the virtual machine (Compute Engine) used as the bastion server for the SSH tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#vm_ip GoogleDatabaseMigrationServiceMigrationJob#vm_ip}
        :param vm_port: The forwarding port of the virtual machine (Compute Engine) used as the bastion server for the SSH tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#vm_port GoogleDatabaseMigrationServiceMigrationJob#vm_port}
        :param vpc: The name of the VPC to peer with the Cloud SQL private network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#vpc GoogleDatabaseMigrationServiceMigrationJob#vpc}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d59d3cc6b4efdabbbb8c2f3b0201d009188d4c2e4259ec7c86dd96c5979be615)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#vm GoogleDatabaseMigrationServiceMigrationJob#vm}
        '''
        result = self._values.get("vm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vm_ip(self) -> typing.Optional[builtins.str]:
        '''The IP of the virtual machine (Compute Engine) used as the bastion server for the SSH tunnel.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#vm_ip GoogleDatabaseMigrationServiceMigrationJob#vm_ip}
        '''
        result = self._values.get("vm_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vm_port(self) -> typing.Optional[jsii.Number]:
        '''The forwarding port of the virtual machine (Compute Engine) used as the bastion server for the SSH tunnel.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#vm_port GoogleDatabaseMigrationServiceMigrationJob#vm_port}
        '''
        result = self._values.get("vm_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vpc(self) -> typing.Optional[builtins.str]:
        '''The name of the VPC to peer with the Cloud SQL private network.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#vpc GoogleDatabaseMigrationServiceMigrationJob#vpc}
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDatabaseMigrationServiceMigrationJobReverseSshConnectivity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDatabaseMigrationServiceMigrationJobReverseSshConnectivityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceMigrationJob.GoogleDatabaseMigrationServiceMigrationJobReverseSshConnectivityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b592995ff535adc93c6b1de2f7c6a09083297dccd3f4c9e499a205145b35c0f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4857c5b7f163b9876a0bc8b7971cad82f45df58d2f8ae38163e67740fab3d6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmIp")
    def vm_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmIp"))

    @vm_ip.setter
    def vm_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8544fddd37814a258d321eaeb093d649f3af7a6f2a08ece6f5be881ae43b6f46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmPort")
    def vm_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "vmPort"))

    @vm_port.setter
    def vm_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66a8d288395f53c32b16664f91d5a79f68eceba05897c032977decbacdbf27e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpc"))

    @vpc.setter
    def vpc(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c79e736e6ca865d2aa388abd37f2ea0bc724d473eb1c50dd9e796b4aa4c167a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpc", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDatabaseMigrationServiceMigrationJobReverseSshConnectivity]:
        return typing.cast(typing.Optional[GoogleDatabaseMigrationServiceMigrationJobReverseSshConnectivity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDatabaseMigrationServiceMigrationJobReverseSshConnectivity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbaf1afee266f824a09564b44d1da8dfbb49e0f2327d18f0a5b5cddc017c9bb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceMigrationJob.GoogleDatabaseMigrationServiceMigrationJobStaticIpConnectivity",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDatabaseMigrationServiceMigrationJobStaticIpConnectivity:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDatabaseMigrationServiceMigrationJobStaticIpConnectivity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDatabaseMigrationServiceMigrationJobStaticIpConnectivityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceMigrationJob.GoogleDatabaseMigrationServiceMigrationJobStaticIpConnectivityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__994fe9714ada1612f8d3ea1d4237aa306e9f9e4e3e5cae3eb43c019a2524c9df)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDatabaseMigrationServiceMigrationJobStaticIpConnectivity]:
        return typing.cast(typing.Optional[GoogleDatabaseMigrationServiceMigrationJobStaticIpConnectivity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDatabaseMigrationServiceMigrationJobStaticIpConnectivity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08e6ebeafe7ebfc635a1a21dc51d606b914001ee307d0e16674498e94a1faf7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceMigrationJob.GoogleDatabaseMigrationServiceMigrationJobTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleDatabaseMigrationServiceMigrationJobTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#create GoogleDatabaseMigrationServiceMigrationJob#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#delete GoogleDatabaseMigrationServiceMigrationJob#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#update GoogleDatabaseMigrationServiceMigrationJob#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73b892fb79f0e59d1e745114ea4d3ea01d4d56c8e9eaecdf948c37ee723b523a)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#create GoogleDatabaseMigrationServiceMigrationJob#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#delete GoogleDatabaseMigrationServiceMigrationJob#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#update GoogleDatabaseMigrationServiceMigrationJob#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDatabaseMigrationServiceMigrationJobTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDatabaseMigrationServiceMigrationJobTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceMigrationJob.GoogleDatabaseMigrationServiceMigrationJobTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__02bc0c85467e66f18add55c2ffd8e59a0f6f127f2e4dfc774ada30ffab6f7724)
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
            type_hints = typing.get_type_hints(_typecheckingstub__19680df60312622b86e715b09c28ae224cdc34c543135bd20445716d78787344)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b4c302c440e55e0a250cf2cafaec7fecbc1ca2aebcfe7e68a49a4ff79267c6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8957731bb779dd52ca47a852630073fb611c510c0db2ec55292b2ae3f9d07d5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDatabaseMigrationServiceMigrationJobTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDatabaseMigrationServiceMigrationJobTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDatabaseMigrationServiceMigrationJobTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24635faa1f7f71379a26eb64c65ad1fb5427f3642ec50615352f95381c58dc3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceMigrationJob.GoogleDatabaseMigrationServiceMigrationJobVpcPeeringConnectivity",
    jsii_struct_bases=[],
    name_mapping={"vpc": "vpc"},
)
class GoogleDatabaseMigrationServiceMigrationJobVpcPeeringConnectivity:
    def __init__(self, *, vpc: typing.Optional[builtins.str] = None) -> None:
        '''
        :param vpc: The name of the VPC network to peer with the Cloud SQL private network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#vpc GoogleDatabaseMigrationServiceMigrationJob#vpc}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d395200e423fbec1f1efdc981413f19e6d5a6057c818921b0e64651d7c372e7f)
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def vpc(self) -> typing.Optional[builtins.str]:
        '''The name of the VPC network to peer with the Cloud SQL private network.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_migration_job#vpc GoogleDatabaseMigrationServiceMigrationJob#vpc}
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDatabaseMigrationServiceMigrationJobVpcPeeringConnectivity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDatabaseMigrationServiceMigrationJobVpcPeeringConnectivityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceMigrationJob.GoogleDatabaseMigrationServiceMigrationJobVpcPeeringConnectivityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fba5777aa7f0ce9e66a91a5fbb8cef41a05acd3d9eaf78ed146b85166ef0cd1c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe1ccfa2e80bc6a33cc54ffb795e099913df35da99eab738c024bd05cf74bb02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpc", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDatabaseMigrationServiceMigrationJobVpcPeeringConnectivity]:
        return typing.cast(typing.Optional[GoogleDatabaseMigrationServiceMigrationJobVpcPeeringConnectivity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDatabaseMigrationServiceMigrationJobVpcPeeringConnectivity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1e1ef8d4c7c180060c70fffd2dc9f9776d32216ac23f63a09f1c25ae3f7f50f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleDatabaseMigrationServiceMigrationJob",
    "GoogleDatabaseMigrationServiceMigrationJobConfig",
    "GoogleDatabaseMigrationServiceMigrationJobDumpFlags",
    "GoogleDatabaseMigrationServiceMigrationJobDumpFlagsDumpFlags",
    "GoogleDatabaseMigrationServiceMigrationJobDumpFlagsDumpFlagsList",
    "GoogleDatabaseMigrationServiceMigrationJobDumpFlagsDumpFlagsOutputReference",
    "GoogleDatabaseMigrationServiceMigrationJobDumpFlagsOutputReference",
    "GoogleDatabaseMigrationServiceMigrationJobError",
    "GoogleDatabaseMigrationServiceMigrationJobErrorList",
    "GoogleDatabaseMigrationServiceMigrationJobErrorOutputReference",
    "GoogleDatabaseMigrationServiceMigrationJobPerformanceConfig",
    "GoogleDatabaseMigrationServiceMigrationJobPerformanceConfigOutputReference",
    "GoogleDatabaseMigrationServiceMigrationJobReverseSshConnectivity",
    "GoogleDatabaseMigrationServiceMigrationJobReverseSshConnectivityOutputReference",
    "GoogleDatabaseMigrationServiceMigrationJobStaticIpConnectivity",
    "GoogleDatabaseMigrationServiceMigrationJobStaticIpConnectivityOutputReference",
    "GoogleDatabaseMigrationServiceMigrationJobTimeouts",
    "GoogleDatabaseMigrationServiceMigrationJobTimeoutsOutputReference",
    "GoogleDatabaseMigrationServiceMigrationJobVpcPeeringConnectivity",
    "GoogleDatabaseMigrationServiceMigrationJobVpcPeeringConnectivityOutputReference",
]

publication.publish()

def _typecheckingstub__9095370a9146c7d2acaccbbfad850cdf8cf7ea4ebce607a59d052a3e174acb43(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    destination: builtins.str,
    migration_job_id: builtins.str,
    source: builtins.str,
    type: builtins.str,
    display_name: typing.Optional[builtins.str] = None,
    dump_flags: typing.Optional[typing.Union[GoogleDatabaseMigrationServiceMigrationJobDumpFlags, typing.Dict[builtins.str, typing.Any]]] = None,
    dump_path: typing.Optional[builtins.str] = None,
    dump_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    performance_config: typing.Optional[typing.Union[GoogleDatabaseMigrationServiceMigrationJobPerformanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    reverse_ssh_connectivity: typing.Optional[typing.Union[GoogleDatabaseMigrationServiceMigrationJobReverseSshConnectivity, typing.Dict[builtins.str, typing.Any]]] = None,
    static_ip_connectivity: typing.Optional[typing.Union[GoogleDatabaseMigrationServiceMigrationJobStaticIpConnectivity, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleDatabaseMigrationServiceMigrationJobTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc_peering_connectivity: typing.Optional[typing.Union[GoogleDatabaseMigrationServiceMigrationJobVpcPeeringConnectivity, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__0fac205e15023ec56f6f725bbb3b390672070478298a3ca0312a6377bd2c1140(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03e943cf6afc75e055c99737a000e326543658ad409c4ac9aec7fe7d68b19176(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e140536e62d6912f086ac8a9e3ebae8ed1798792ae8e603d85449a3741311b90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5ee69b566483bfb6de98a52596edade830b49ff07c53944e4eeb5753a660444(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26348a8f8f45abe84678096476bbd454f93e9f494bd2bd56e980cc151315286d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d8ebc9cb3c2679307d6f0e50ab5e5574b93a351a7cd92d60757baefd3eb7535(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d442459951ff0ba0822d8539e0ccdef63ea567ff00f8d2e7b4189347cc98b04c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e01dd08ca07cb728b327a8ca689a94b8a39f782c1e740acd31d30b799153c9c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b6e4c1cdfab2176d606734b3f32fe907ac0701f5d14ca73813dfd868f116f40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1071564883cfccc52a24e2448ebcabd7a2dd970d681c46b9338ae8de637dcca5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acc32c12720661315d10d31b9b2c9f8be11310974aef95639ae5e358390b3b9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76e8cd8ae0c0c4d878bb6f3698d67d8f7941a10ee74c95e8c2caaafde615a813(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fe569e65986014381d002b563b2146c7d162a8d31855d087928c4b215283cab(
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
    dump_flags: typing.Optional[typing.Union[GoogleDatabaseMigrationServiceMigrationJobDumpFlags, typing.Dict[builtins.str, typing.Any]]] = None,
    dump_path: typing.Optional[builtins.str] = None,
    dump_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    performance_config: typing.Optional[typing.Union[GoogleDatabaseMigrationServiceMigrationJobPerformanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    reverse_ssh_connectivity: typing.Optional[typing.Union[GoogleDatabaseMigrationServiceMigrationJobReverseSshConnectivity, typing.Dict[builtins.str, typing.Any]]] = None,
    static_ip_connectivity: typing.Optional[typing.Union[GoogleDatabaseMigrationServiceMigrationJobStaticIpConnectivity, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleDatabaseMigrationServiceMigrationJobTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc_peering_connectivity: typing.Optional[typing.Union[GoogleDatabaseMigrationServiceMigrationJobVpcPeeringConnectivity, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd8f92e276c073f794415a76ea10e81a0957c4467777f2e5cc6e3f756d963f39(
    *,
    dump_flags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDatabaseMigrationServiceMigrationJobDumpFlagsDumpFlags, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf837975aefbe775d615fd52560a6fd8527e0528fdee8ea205b653f79a6a8620(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5baa041c240079837a40236fea57cc6841a2a9747e5c7421d508199363d7746(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13e0a9855b9cddd9c4df0c1dcf14ad14f136df4a25fabe5faab1519b3687dd26(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30414a0f5c1baf15afcacb17cb0edd421d7f25401b719cf4923ce75c7bf2e358(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bf08d1796aabdb223cf0ecf61888673f9e0e2a3cd6a292b2f53388cb664b34f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc73caab50e09cbf0dd9dd4e8c002b3a14cf8d7e8724021612ea4169f8b9d190(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad530dd7cb62350ddbd6ab74fc913edd0db980cb6062f84e542dafe31bd2463b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDatabaseMigrationServiceMigrationJobDumpFlagsDumpFlags]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5df031952b746d939ffda0b2b62f1fd9748808ba3c8b49a3d6dd0a02a1265d1e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6801bfdfcb9db8af5a2b50263ff14ab237e05f514c3f1f9be6313d455c01f1fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bce2dfdf1e541b4f0e581bdba135644308c3b78ee8bcd2538da0c4dc5933510a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a69b72037c835077542a1e3812cb473eb1a62b0fb11e14e6b5f9da35ae8a253(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDatabaseMigrationServiceMigrationJobDumpFlagsDumpFlags]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c1d6508d7643e62a2c116674373aed79b399f479454f23fddefbadf160a070e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f140649e2ad2aaa8e1490366bad8f60523b03344c6570f462640fd47125c6e84(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDatabaseMigrationServiceMigrationJobDumpFlagsDumpFlags, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40081de9905972e574f2b26393c90e55869e3c95df2d90faf09c1156a228ae4b(
    value: typing.Optional[GoogleDatabaseMigrationServiceMigrationJobDumpFlags],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6837d016de895706d8b1a3a0d2fcfd32f21524cc26e2270fb938dc245e7cffa2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c5e204c7a60e3135f83369bcdf2292455f48b7468c7d0ad02249a5f8d67b4c8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c5d14268d3b931683a34c88d13fc5c8e5d5875f475a6f50dd24ad80db075326(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eb313a344fd2b1b5d0333702d5a801381ed9d14772faa4968bcef858fa34cd9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd4a077ddb3d83e38a21552ebde9e2d3739da671dcaab67815d072196279a9a5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed6cd483719f214823b704fdeebaeff62cec57d604ac35e1dd4540cd4e9eeb35(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3e166d1cfda7a8d5b41bb2e4286ec672defeedc54dc47c3d41bdb7b8f5e6667(
    value: typing.Optional[GoogleDatabaseMigrationServiceMigrationJobError],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cf34b5feb345097ed9f6434d7cc8074373bd15b9e77756e7307e1dfe917135d(
    *,
    dump_parallel_level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6c93fb9cacfe0538c9af425386caf45f4c2df3cf27bbce874de250bab978d1f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e729d3752eba1c6b2fd55cae896711f40fd211517e8d230426b25783db7170cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daa841d0e7a3e14b5051a7e8e1d1cef293906163b62e11c0430a46e2ca0cd397(
    value: typing.Optional[GoogleDatabaseMigrationServiceMigrationJobPerformanceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d59d3cc6b4efdabbbb8c2f3b0201d009188d4c2e4259ec7c86dd96c5979be615(
    *,
    vm: typing.Optional[builtins.str] = None,
    vm_ip: typing.Optional[builtins.str] = None,
    vm_port: typing.Optional[jsii.Number] = None,
    vpc: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b592995ff535adc93c6b1de2f7c6a09083297dccd3f4c9e499a205145b35c0f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4857c5b7f163b9876a0bc8b7971cad82f45df58d2f8ae38163e67740fab3d6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8544fddd37814a258d321eaeb093d649f3af7a6f2a08ece6f5be881ae43b6f46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66a8d288395f53c32b16664f91d5a79f68eceba05897c032977decbacdbf27e3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c79e736e6ca865d2aa388abd37f2ea0bc724d473eb1c50dd9e796b4aa4c167a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbaf1afee266f824a09564b44d1da8dfbb49e0f2327d18f0a5b5cddc017c9bb4(
    value: typing.Optional[GoogleDatabaseMigrationServiceMigrationJobReverseSshConnectivity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__994fe9714ada1612f8d3ea1d4237aa306e9f9e4e3e5cae3eb43c019a2524c9df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08e6ebeafe7ebfc635a1a21dc51d606b914001ee307d0e16674498e94a1faf7b(
    value: typing.Optional[GoogleDatabaseMigrationServiceMigrationJobStaticIpConnectivity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73b892fb79f0e59d1e745114ea4d3ea01d4d56c8e9eaecdf948c37ee723b523a(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02bc0c85467e66f18add55c2ffd8e59a0f6f127f2e4dfc774ada30ffab6f7724(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19680df60312622b86e715b09c28ae224cdc34c543135bd20445716d78787344(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b4c302c440e55e0a250cf2cafaec7fecbc1ca2aebcfe7e68a49a4ff79267c6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8957731bb779dd52ca47a852630073fb611c510c0db2ec55292b2ae3f9d07d5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24635faa1f7f71379a26eb64c65ad1fb5427f3642ec50615352f95381c58dc3a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDatabaseMigrationServiceMigrationJobTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d395200e423fbec1f1efdc981413f19e6d5a6057c818921b0e64651d7c372e7f(
    *,
    vpc: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fba5777aa7f0ce9e66a91a5fbb8cef41a05acd3d9eaf78ed146b85166ef0cd1c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe1ccfa2e80bc6a33cc54ffb795e099913df35da99eab738c024bd05cf74bb02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1e1ef8d4c7c180060c70fffd2dc9f9776d32216ac23f63a09f1c25ae3f7f50f(
    value: typing.Optional[GoogleDatabaseMigrationServiceMigrationJobVpcPeeringConnectivity],
) -> None:
    """Type checking stubs"""
    pass
