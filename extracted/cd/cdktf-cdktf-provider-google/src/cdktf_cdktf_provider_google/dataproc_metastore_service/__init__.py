r'''
# `google_dataproc_metastore_service`

Refer to the Terraform Registry for docs: [`google_dataproc_metastore_service`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service).
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


class DataprocMetastoreService(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocMetastoreService.DataprocMetastoreService",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service google_dataproc_metastore_service}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        service_id: builtins.str,
        database_type: typing.Optional[builtins.str] = None,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_config: typing.Optional[typing.Union["DataprocMetastoreServiceEncryptionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        hive_metastore_config: typing.Optional[typing.Union["DataprocMetastoreServiceHiveMetastoreConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        maintenance_window: typing.Optional[typing.Union["DataprocMetastoreServiceMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]] = None,
        metadata_integration: typing.Optional[typing.Union["DataprocMetastoreServiceMetadataIntegration", typing.Dict[builtins.str, typing.Any]]] = None,
        network: typing.Optional[builtins.str] = None,
        network_config: typing.Optional[typing.Union["DataprocMetastoreServiceNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        port: typing.Optional[jsii.Number] = None,
        project: typing.Optional[builtins.str] = None,
        release_channel: typing.Optional[builtins.str] = None,
        scaling_config: typing.Optional[typing.Union["DataprocMetastoreServiceScalingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        scheduled_backup: typing.Optional[typing.Union["DataprocMetastoreServiceScheduledBackup", typing.Dict[builtins.str, typing.Any]]] = None,
        telemetry_config: typing.Optional[typing.Union["DataprocMetastoreServiceTelemetryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tier: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataprocMetastoreServiceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service google_dataproc_metastore_service} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param service_id: The ID of the metastore service. The id must contain only letters (a-z, A-Z), numbers (0-9), underscores (_), and hyphens (-). Cannot begin or end with underscore or hyphen. Must consist of between 3 and 63 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#service_id DataprocMetastoreService#service_id}
        :param database_type: The database type that the Metastore service stores its data. Default value: "MYSQL" Possible values: ["MYSQL", "SPANNER"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#database_type DataprocMetastoreService#database_type}
        :param deletion_protection: Indicates if the dataproc metastore should be protected against accidental deletions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#deletion_protection DataprocMetastoreService#deletion_protection}
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#encryption_config DataprocMetastoreService#encryption_config}
        :param hive_metastore_config: hive_metastore_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#hive_metastore_config DataprocMetastoreService#hive_metastore_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#id DataprocMetastoreService#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: User-defined labels for the metastore service. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#labels DataprocMetastoreService#labels}
        :param location: The location where the metastore service should reside. The default value is 'global'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#location DataprocMetastoreService#location}
        :param maintenance_window: maintenance_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#maintenance_window DataprocMetastoreService#maintenance_window}
        :param metadata_integration: metadata_integration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#metadata_integration DataprocMetastoreService#metadata_integration}
        :param network: The relative resource name of the VPC network on which the instance can be accessed. It is specified in the following form: "projects/{projectNumber}/global/networks/{network_id}". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#network DataprocMetastoreService#network}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#network_config DataprocMetastoreService#network_config}
        :param port: The TCP port at which the metastore service is reached. Default: 9083. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#port DataprocMetastoreService#port}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#project DataprocMetastoreService#project}.
        :param release_channel: The release channel of the service. If unspecified, defaults to 'STABLE'. Default value: "STABLE" Possible values: ["CANARY", "STABLE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#release_channel DataprocMetastoreService#release_channel}
        :param scaling_config: scaling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#scaling_config DataprocMetastoreService#scaling_config}
        :param scheduled_backup: scheduled_backup block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#scheduled_backup DataprocMetastoreService#scheduled_backup}
        :param telemetry_config: telemetry_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#telemetry_config DataprocMetastoreService#telemetry_config}
        :param tier: The tier of the service. Possible values: ["DEVELOPER", "ENTERPRISE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#tier DataprocMetastoreService#tier}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#timeouts DataprocMetastoreService#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c6c30b2fa325592281e66943d0efae5eeb701cdb951f4d4700e37d87e84d0dc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataprocMetastoreServiceConfig(
            service_id=service_id,
            database_type=database_type,
            deletion_protection=deletion_protection,
            encryption_config=encryption_config,
            hive_metastore_config=hive_metastore_config,
            id=id,
            labels=labels,
            location=location,
            maintenance_window=maintenance_window,
            metadata_integration=metadata_integration,
            network=network,
            network_config=network_config,
            port=port,
            project=project,
            release_channel=release_channel,
            scaling_config=scaling_config,
            scheduled_backup=scheduled_backup,
            telemetry_config=telemetry_config,
            tier=tier,
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
        '''Generates CDKTF code for importing a DataprocMetastoreService resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataprocMetastoreService to import.
        :param import_from_id: The id of the existing DataprocMetastoreService that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataprocMetastoreService to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__711ae53107df0130c2924e2539a842e90e32d7326c8c7196edc518a6a415f216)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEncryptionConfig")
    def put_encryption_config(self, *, kms_key: builtins.str) -> None:
        '''
        :param kms_key: The fully qualified customer provided Cloud KMS key name to use for customer data encryption. Use the following format: 'projects/([^/]+)/locations/([^/]+)/keyRings/([^/]+)/cryptoKeys/([^/]+)'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#kms_key DataprocMetastoreService#kms_key}
        '''
        value = DataprocMetastoreServiceEncryptionConfig(kms_key=kms_key)

        return typing.cast(None, jsii.invoke(self, "putEncryptionConfig", [value]))

    @jsii.member(jsii_name="putHiveMetastoreConfig")
    def put_hive_metastore_config(
        self,
        *,
        version: builtins.str,
        auxiliary_versions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        config_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        endpoint_protocol: typing.Optional[builtins.str] = None,
        kerberos_config: typing.Optional[typing.Union["DataprocMetastoreServiceHiveMetastoreConfigKerberosConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param version: The Hive metastore schema version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#version DataprocMetastoreService#version}
        :param auxiliary_versions: auxiliary_versions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#auxiliary_versions DataprocMetastoreService#auxiliary_versions}
        :param config_overrides: A mapping of Hive metastore configuration key-value pairs to apply to the Hive metastore (configured in hive-site.xml). The mappings override system defaults (some keys cannot be overridden). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#config_overrides DataprocMetastoreService#config_overrides}
        :param endpoint_protocol: The protocol to use for the metastore service endpoint. If unspecified, defaults to 'THRIFT'. Default value: "THRIFT" Possible values: ["THRIFT", "GRPC"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#endpoint_protocol DataprocMetastoreService#endpoint_protocol}
        :param kerberos_config: kerberos_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#kerberos_config DataprocMetastoreService#kerberos_config}
        '''
        value = DataprocMetastoreServiceHiveMetastoreConfig(
            version=version,
            auxiliary_versions=auxiliary_versions,
            config_overrides=config_overrides,
            endpoint_protocol=endpoint_protocol,
            kerberos_config=kerberos_config,
        )

        return typing.cast(None, jsii.invoke(self, "putHiveMetastoreConfig", [value]))

    @jsii.member(jsii_name="putMaintenanceWindow")
    def put_maintenance_window(
        self,
        *,
        day_of_week: builtins.str,
        hour_of_day: jsii.Number,
    ) -> None:
        '''
        :param day_of_week: The day of week, when the window starts. Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#day_of_week DataprocMetastoreService#day_of_week}
        :param hour_of_day: The hour of day (0-23) when the window starts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#hour_of_day DataprocMetastoreService#hour_of_day}
        '''
        value = DataprocMetastoreServiceMaintenanceWindow(
            day_of_week=day_of_week, hour_of_day=hour_of_day
        )

        return typing.cast(None, jsii.invoke(self, "putMaintenanceWindow", [value]))

    @jsii.member(jsii_name="putMetadataIntegration")
    def put_metadata_integration(
        self,
        *,
        data_catalog_config: typing.Union["DataprocMetastoreServiceMetadataIntegrationDataCatalogConfig", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param data_catalog_config: data_catalog_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#data_catalog_config DataprocMetastoreService#data_catalog_config}
        '''
        value = DataprocMetastoreServiceMetadataIntegration(
            data_catalog_config=data_catalog_config
        )

        return typing.cast(None, jsii.invoke(self, "putMetadataIntegration", [value]))

    @jsii.member(jsii_name="putNetworkConfig")
    def put_network_config(
        self,
        *,
        consumers: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataprocMetastoreServiceNetworkConfigConsumers", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param consumers: consumers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#consumers DataprocMetastoreService#consumers}
        '''
        value = DataprocMetastoreServiceNetworkConfig(consumers=consumers)

        return typing.cast(None, jsii.invoke(self, "putNetworkConfig", [value]))

    @jsii.member(jsii_name="putScalingConfig")
    def put_scaling_config(
        self,
        *,
        autoscaling_config: typing.Optional[typing.Union["DataprocMetastoreServiceScalingConfigAutoscalingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        instance_size: typing.Optional[builtins.str] = None,
        scaling_factor: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param autoscaling_config: autoscaling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#autoscaling_config DataprocMetastoreService#autoscaling_config}
        :param instance_size: Metastore instance sizes. Possible values: ["EXTRA_SMALL", "SMALL", "MEDIUM", "LARGE", "EXTRA_LARGE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#instance_size DataprocMetastoreService#instance_size}
        :param scaling_factor: Scaling factor, in increments of 0.1 for values less than 1.0, and increments of 1.0 for values greater than 1.0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#scaling_factor DataprocMetastoreService#scaling_factor}
        '''
        value = DataprocMetastoreServiceScalingConfig(
            autoscaling_config=autoscaling_config,
            instance_size=instance_size,
            scaling_factor=scaling_factor,
        )

        return typing.cast(None, jsii.invoke(self, "putScalingConfig", [value]))

    @jsii.member(jsii_name="putScheduledBackup")
    def put_scheduled_backup(
        self,
        *,
        backup_location: builtins.str,
        cron_schedule: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        time_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param backup_location: A Cloud Storage URI of a folder, in the format gs://<bucket_name>/<path_inside_bucket>. A sub-folder <backup_folder> containing backup files will be stored below it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#backup_location DataprocMetastoreService#backup_location}
        :param cron_schedule: The scheduled interval in Cron format, see https://en.wikipedia.org/wiki/Cron The default is empty: scheduled backup is not enabled. Must be specified to enable scheduled backups. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#cron_schedule DataprocMetastoreService#cron_schedule}
        :param enabled: Defines whether the scheduled backup is enabled. The default value is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#enabled DataprocMetastoreService#enabled}
        :param time_zone: Specifies the time zone to be used when interpreting cronSchedule. Must be a time zone name from the time zone database (https://en.wikipedia.org/wiki/List_of_tz_database_time_zones), e.g. America/Los_Angeles or Africa/Abidjan. If left unspecified, the default is UTC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#time_zone DataprocMetastoreService#time_zone}
        '''
        value = DataprocMetastoreServiceScheduledBackup(
            backup_location=backup_location,
            cron_schedule=cron_schedule,
            enabled=enabled,
            time_zone=time_zone,
        )

        return typing.cast(None, jsii.invoke(self, "putScheduledBackup", [value]))

    @jsii.member(jsii_name="putTelemetryConfig")
    def put_telemetry_config(
        self,
        *,
        log_format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param log_format: The output format of the Dataproc Metastore service's logs. Default value: "JSON" Possible values: ["LEGACY", "JSON"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#log_format DataprocMetastoreService#log_format}
        '''
        value = DataprocMetastoreServiceTelemetryConfig(log_format=log_format)

        return typing.cast(None, jsii.invoke(self, "putTelemetryConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#create DataprocMetastoreService#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#delete DataprocMetastoreService#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#update DataprocMetastoreService#update}.
        '''
        value = DataprocMetastoreServiceTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDatabaseType")
    def reset_database_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabaseType", []))

    @jsii.member(jsii_name="resetDeletionProtection")
    def reset_deletion_protection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeletionProtection", []))

    @jsii.member(jsii_name="resetEncryptionConfig")
    def reset_encryption_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionConfig", []))

    @jsii.member(jsii_name="resetHiveMetastoreConfig")
    def reset_hive_metastore_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHiveMetastoreConfig", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetMaintenanceWindow")
    def reset_maintenance_window(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintenanceWindow", []))

    @jsii.member(jsii_name="resetMetadataIntegration")
    def reset_metadata_integration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadataIntegration", []))

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @jsii.member(jsii_name="resetNetworkConfig")
    def reset_network_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkConfig", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetReleaseChannel")
    def reset_release_channel(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReleaseChannel", []))

    @jsii.member(jsii_name="resetScalingConfig")
    def reset_scaling_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScalingConfig", []))

    @jsii.member(jsii_name="resetScheduledBackup")
    def reset_scheduled_backup(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheduledBackup", []))

    @jsii.member(jsii_name="resetTelemetryConfig")
    def reset_telemetry_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTelemetryConfig", []))

    @jsii.member(jsii_name="resetTier")
    def reset_tier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTier", []))

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
    @jsii.member(jsii_name="artifactGcsUri")
    def artifact_gcs_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "artifactGcsUri"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfig")
    def encryption_config(
        self,
    ) -> "DataprocMetastoreServiceEncryptionConfigOutputReference":
        return typing.cast("DataprocMetastoreServiceEncryptionConfigOutputReference", jsii.get(self, "encryptionConfig"))

    @builtins.property
    @jsii.member(jsii_name="endpointUri")
    def endpoint_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpointUri"))

    @builtins.property
    @jsii.member(jsii_name="hiveMetastoreConfig")
    def hive_metastore_config(
        self,
    ) -> "DataprocMetastoreServiceHiveMetastoreConfigOutputReference":
        return typing.cast("DataprocMetastoreServiceHiveMetastoreConfigOutputReference", jsii.get(self, "hiveMetastoreConfig"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindow")
    def maintenance_window(
        self,
    ) -> "DataprocMetastoreServiceMaintenanceWindowOutputReference":
        return typing.cast("DataprocMetastoreServiceMaintenanceWindowOutputReference", jsii.get(self, "maintenanceWindow"))

    @builtins.property
    @jsii.member(jsii_name="metadataIntegration")
    def metadata_integration(
        self,
    ) -> "DataprocMetastoreServiceMetadataIntegrationOutputReference":
        return typing.cast("DataprocMetastoreServiceMetadataIntegrationOutputReference", jsii.get(self, "metadataIntegration"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="networkConfig")
    def network_config(self) -> "DataprocMetastoreServiceNetworkConfigOutputReference":
        return typing.cast("DataprocMetastoreServiceNetworkConfigOutputReference", jsii.get(self, "networkConfig"))

    @builtins.property
    @jsii.member(jsii_name="scalingConfig")
    def scaling_config(self) -> "DataprocMetastoreServiceScalingConfigOutputReference":
        return typing.cast("DataprocMetastoreServiceScalingConfigOutputReference", jsii.get(self, "scalingConfig"))

    @builtins.property
    @jsii.member(jsii_name="scheduledBackup")
    def scheduled_backup(
        self,
    ) -> "DataprocMetastoreServiceScheduledBackupOutputReference":
        return typing.cast("DataprocMetastoreServiceScheduledBackupOutputReference", jsii.get(self, "scheduledBackup"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="stateMessage")
    def state_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stateMessage"))

    @builtins.property
    @jsii.member(jsii_name="telemetryConfig")
    def telemetry_config(
        self,
    ) -> "DataprocMetastoreServiceTelemetryConfigOutputReference":
        return typing.cast("DataprocMetastoreServiceTelemetryConfigOutputReference", jsii.get(self, "telemetryConfig"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DataprocMetastoreServiceTimeoutsOutputReference":
        return typing.cast("DataprocMetastoreServiceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="databaseTypeInput")
    def database_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="deletionProtectionInput")
    def deletion_protection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deletionProtectionInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfigInput")
    def encryption_config_input(
        self,
    ) -> typing.Optional["DataprocMetastoreServiceEncryptionConfig"]:
        return typing.cast(typing.Optional["DataprocMetastoreServiceEncryptionConfig"], jsii.get(self, "encryptionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="hiveMetastoreConfigInput")
    def hive_metastore_config_input(
        self,
    ) -> typing.Optional["DataprocMetastoreServiceHiveMetastoreConfig"]:
        return typing.cast(typing.Optional["DataprocMetastoreServiceHiveMetastoreConfig"], jsii.get(self, "hiveMetastoreConfigInput"))

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
    @jsii.member(jsii_name="maintenanceWindowInput")
    def maintenance_window_input(
        self,
    ) -> typing.Optional["DataprocMetastoreServiceMaintenanceWindow"]:
        return typing.cast(typing.Optional["DataprocMetastoreServiceMaintenanceWindow"], jsii.get(self, "maintenanceWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataIntegrationInput")
    def metadata_integration_input(
        self,
    ) -> typing.Optional["DataprocMetastoreServiceMetadataIntegration"]:
        return typing.cast(typing.Optional["DataprocMetastoreServiceMetadataIntegration"], jsii.get(self, "metadataIntegrationInput"))

    @builtins.property
    @jsii.member(jsii_name="networkConfigInput")
    def network_config_input(
        self,
    ) -> typing.Optional["DataprocMetastoreServiceNetworkConfig"]:
        return typing.cast(typing.Optional["DataprocMetastoreServiceNetworkConfig"], jsii.get(self, "networkConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="releaseChannelInput")
    def release_channel_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "releaseChannelInput"))

    @builtins.property
    @jsii.member(jsii_name="scalingConfigInput")
    def scaling_config_input(
        self,
    ) -> typing.Optional["DataprocMetastoreServiceScalingConfig"]:
        return typing.cast(typing.Optional["DataprocMetastoreServiceScalingConfig"], jsii.get(self, "scalingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduledBackupInput")
    def scheduled_backup_input(
        self,
    ) -> typing.Optional["DataprocMetastoreServiceScheduledBackup"]:
        return typing.cast(typing.Optional["DataprocMetastoreServiceScheduledBackup"], jsii.get(self, "scheduledBackupInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceIdInput")
    def service_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="telemetryConfigInput")
    def telemetry_config_input(
        self,
    ) -> typing.Optional["DataprocMetastoreServiceTelemetryConfig"]:
        return typing.cast(typing.Optional["DataprocMetastoreServiceTelemetryConfig"], jsii.get(self, "telemetryConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="tierInput")
    def tier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tierInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataprocMetastoreServiceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataprocMetastoreServiceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseType")
    def database_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseType"))

    @database_type.setter
    def database_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56a79e3b07585328bbc438e2c4c548249e166a5035c53d046b346a01ff788260)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deletionProtection")
    def deletion_protection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deletionProtection"))

    @deletion_protection.setter
    def deletion_protection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b60bf737d4f1abffb5fef22c34fe9ee92ce8e16d81d541619bae083a842c62d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionProtection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5eb4c13993b1799f1fdf8b0ba0acae174cfae5fb325e82dfe44dd78ad93055b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__036a99424d82c3e0a86a0965622e7d5e18b5ec36220e5e81525615ceb0110453)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f792684130a2b65c87f46247d89fd3cc81a68cedb61897e1bf7d12d97e30de6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c226d3655e00cfd24e367355ea0009321c36584159b00c6a13779aaeed316c42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__085cd89fe09e0afb8a33f5816fc7d139c79fead911567d3c83b47550d35678aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26821518ec36a687d2b673f782161fbee1dba726f75aef7774b2b70aba3efc90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="releaseChannel")
    def release_channel(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "releaseChannel"))

    @release_channel.setter
    def release_channel(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b22ecadf46f20a8f6ea11636da2a416026732eb663f5929f5c1c405bd48194e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "releaseChannel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceId")
    def service_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceId"))

    @service_id.setter
    def service_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__365a5a3c4025235aa79721eeaac216401f6bc18ee61c5fb4a1ef18216a26b365)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tier")
    def tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tier"))

    @tier.setter
    def tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9a701a373949e892312c24628201e43a9c960d0b9ed5617cd48070fce0ec70e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tier", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocMetastoreService.DataprocMetastoreServiceConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "service_id": "serviceId",
        "database_type": "databaseType",
        "deletion_protection": "deletionProtection",
        "encryption_config": "encryptionConfig",
        "hive_metastore_config": "hiveMetastoreConfig",
        "id": "id",
        "labels": "labels",
        "location": "location",
        "maintenance_window": "maintenanceWindow",
        "metadata_integration": "metadataIntegration",
        "network": "network",
        "network_config": "networkConfig",
        "port": "port",
        "project": "project",
        "release_channel": "releaseChannel",
        "scaling_config": "scalingConfig",
        "scheduled_backup": "scheduledBackup",
        "telemetry_config": "telemetryConfig",
        "tier": "tier",
        "timeouts": "timeouts",
    },
)
class DataprocMetastoreServiceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        service_id: builtins.str,
        database_type: typing.Optional[builtins.str] = None,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_config: typing.Optional[typing.Union["DataprocMetastoreServiceEncryptionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        hive_metastore_config: typing.Optional[typing.Union["DataprocMetastoreServiceHiveMetastoreConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        maintenance_window: typing.Optional[typing.Union["DataprocMetastoreServiceMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]] = None,
        metadata_integration: typing.Optional[typing.Union["DataprocMetastoreServiceMetadataIntegration", typing.Dict[builtins.str, typing.Any]]] = None,
        network: typing.Optional[builtins.str] = None,
        network_config: typing.Optional[typing.Union["DataprocMetastoreServiceNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        port: typing.Optional[jsii.Number] = None,
        project: typing.Optional[builtins.str] = None,
        release_channel: typing.Optional[builtins.str] = None,
        scaling_config: typing.Optional[typing.Union["DataprocMetastoreServiceScalingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        scheduled_backup: typing.Optional[typing.Union["DataprocMetastoreServiceScheduledBackup", typing.Dict[builtins.str, typing.Any]]] = None,
        telemetry_config: typing.Optional[typing.Union["DataprocMetastoreServiceTelemetryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tier: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataprocMetastoreServiceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param service_id: The ID of the metastore service. The id must contain only letters (a-z, A-Z), numbers (0-9), underscores (_), and hyphens (-). Cannot begin or end with underscore or hyphen. Must consist of between 3 and 63 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#service_id DataprocMetastoreService#service_id}
        :param database_type: The database type that the Metastore service stores its data. Default value: "MYSQL" Possible values: ["MYSQL", "SPANNER"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#database_type DataprocMetastoreService#database_type}
        :param deletion_protection: Indicates if the dataproc metastore should be protected against accidental deletions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#deletion_protection DataprocMetastoreService#deletion_protection}
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#encryption_config DataprocMetastoreService#encryption_config}
        :param hive_metastore_config: hive_metastore_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#hive_metastore_config DataprocMetastoreService#hive_metastore_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#id DataprocMetastoreService#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: User-defined labels for the metastore service. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#labels DataprocMetastoreService#labels}
        :param location: The location where the metastore service should reside. The default value is 'global'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#location DataprocMetastoreService#location}
        :param maintenance_window: maintenance_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#maintenance_window DataprocMetastoreService#maintenance_window}
        :param metadata_integration: metadata_integration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#metadata_integration DataprocMetastoreService#metadata_integration}
        :param network: The relative resource name of the VPC network on which the instance can be accessed. It is specified in the following form: "projects/{projectNumber}/global/networks/{network_id}". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#network DataprocMetastoreService#network}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#network_config DataprocMetastoreService#network_config}
        :param port: The TCP port at which the metastore service is reached. Default: 9083. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#port DataprocMetastoreService#port}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#project DataprocMetastoreService#project}.
        :param release_channel: The release channel of the service. If unspecified, defaults to 'STABLE'. Default value: "STABLE" Possible values: ["CANARY", "STABLE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#release_channel DataprocMetastoreService#release_channel}
        :param scaling_config: scaling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#scaling_config DataprocMetastoreService#scaling_config}
        :param scheduled_backup: scheduled_backup block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#scheduled_backup DataprocMetastoreService#scheduled_backup}
        :param telemetry_config: telemetry_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#telemetry_config DataprocMetastoreService#telemetry_config}
        :param tier: The tier of the service. Possible values: ["DEVELOPER", "ENTERPRISE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#tier DataprocMetastoreService#tier}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#timeouts DataprocMetastoreService#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(encryption_config, dict):
            encryption_config = DataprocMetastoreServiceEncryptionConfig(**encryption_config)
        if isinstance(hive_metastore_config, dict):
            hive_metastore_config = DataprocMetastoreServiceHiveMetastoreConfig(**hive_metastore_config)
        if isinstance(maintenance_window, dict):
            maintenance_window = DataprocMetastoreServiceMaintenanceWindow(**maintenance_window)
        if isinstance(metadata_integration, dict):
            metadata_integration = DataprocMetastoreServiceMetadataIntegration(**metadata_integration)
        if isinstance(network_config, dict):
            network_config = DataprocMetastoreServiceNetworkConfig(**network_config)
        if isinstance(scaling_config, dict):
            scaling_config = DataprocMetastoreServiceScalingConfig(**scaling_config)
        if isinstance(scheduled_backup, dict):
            scheduled_backup = DataprocMetastoreServiceScheduledBackup(**scheduled_backup)
        if isinstance(telemetry_config, dict):
            telemetry_config = DataprocMetastoreServiceTelemetryConfig(**telemetry_config)
        if isinstance(timeouts, dict):
            timeouts = DataprocMetastoreServiceTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01caaf7ef1f994e7ed6c5f31e31d0acda26cbf540bc791d39bf49116046fa9a1)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument service_id", value=service_id, expected_type=type_hints["service_id"])
            check_type(argname="argument database_type", value=database_type, expected_type=type_hints["database_type"])
            check_type(argname="argument deletion_protection", value=deletion_protection, expected_type=type_hints["deletion_protection"])
            check_type(argname="argument encryption_config", value=encryption_config, expected_type=type_hints["encryption_config"])
            check_type(argname="argument hive_metastore_config", value=hive_metastore_config, expected_type=type_hints["hive_metastore_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument maintenance_window", value=maintenance_window, expected_type=type_hints["maintenance_window"])
            check_type(argname="argument metadata_integration", value=metadata_integration, expected_type=type_hints["metadata_integration"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument network_config", value=network_config, expected_type=type_hints["network_config"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument release_channel", value=release_channel, expected_type=type_hints["release_channel"])
            check_type(argname="argument scaling_config", value=scaling_config, expected_type=type_hints["scaling_config"])
            check_type(argname="argument scheduled_backup", value=scheduled_backup, expected_type=type_hints["scheduled_backup"])
            check_type(argname="argument telemetry_config", value=telemetry_config, expected_type=type_hints["telemetry_config"])
            check_type(argname="argument tier", value=tier, expected_type=type_hints["tier"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service_id": service_id,
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
        if database_type is not None:
            self._values["database_type"] = database_type
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if encryption_config is not None:
            self._values["encryption_config"] = encryption_config
        if hive_metastore_config is not None:
            self._values["hive_metastore_config"] = hive_metastore_config
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if location is not None:
            self._values["location"] = location
        if maintenance_window is not None:
            self._values["maintenance_window"] = maintenance_window
        if metadata_integration is not None:
            self._values["metadata_integration"] = metadata_integration
        if network is not None:
            self._values["network"] = network
        if network_config is not None:
            self._values["network_config"] = network_config
        if port is not None:
            self._values["port"] = port
        if project is not None:
            self._values["project"] = project
        if release_channel is not None:
            self._values["release_channel"] = release_channel
        if scaling_config is not None:
            self._values["scaling_config"] = scaling_config
        if scheduled_backup is not None:
            self._values["scheduled_backup"] = scheduled_backup
        if telemetry_config is not None:
            self._values["telemetry_config"] = telemetry_config
        if tier is not None:
            self._values["tier"] = tier
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
    def service_id(self) -> builtins.str:
        '''The ID of the metastore service.

        The id must contain only letters (a-z, A-Z), numbers (0-9), underscores (_),
        and hyphens (-). Cannot begin or end with underscore or hyphen. Must consist of between
        3 and 63 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#service_id DataprocMetastoreService#service_id}
        '''
        result = self._values.get("service_id")
        assert result is not None, "Required property 'service_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def database_type(self) -> typing.Optional[builtins.str]:
        '''The database type that the Metastore service stores its data. Default value: "MYSQL" Possible values: ["MYSQL", "SPANNER"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#database_type DataprocMetastoreService#database_type}
        '''
        result = self._values.get("database_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deletion_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates if the dataproc metastore should be protected against accidental deletions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#deletion_protection DataprocMetastoreService#deletion_protection}
        '''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encryption_config(
        self,
    ) -> typing.Optional["DataprocMetastoreServiceEncryptionConfig"]:
        '''encryption_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#encryption_config DataprocMetastoreService#encryption_config}
        '''
        result = self._values.get("encryption_config")
        return typing.cast(typing.Optional["DataprocMetastoreServiceEncryptionConfig"], result)

    @builtins.property
    def hive_metastore_config(
        self,
    ) -> typing.Optional["DataprocMetastoreServiceHiveMetastoreConfig"]:
        '''hive_metastore_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#hive_metastore_config DataprocMetastoreService#hive_metastore_config}
        '''
        result = self._values.get("hive_metastore_config")
        return typing.cast(typing.Optional["DataprocMetastoreServiceHiveMetastoreConfig"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#id DataprocMetastoreService#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''User-defined labels for the metastore service.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#labels DataprocMetastoreService#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The location where the metastore service should reside. The default value is 'global'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#location DataprocMetastoreService#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintenance_window(
        self,
    ) -> typing.Optional["DataprocMetastoreServiceMaintenanceWindow"]:
        '''maintenance_window block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#maintenance_window DataprocMetastoreService#maintenance_window}
        '''
        result = self._values.get("maintenance_window")
        return typing.cast(typing.Optional["DataprocMetastoreServiceMaintenanceWindow"], result)

    @builtins.property
    def metadata_integration(
        self,
    ) -> typing.Optional["DataprocMetastoreServiceMetadataIntegration"]:
        '''metadata_integration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#metadata_integration DataprocMetastoreService#metadata_integration}
        '''
        result = self._values.get("metadata_integration")
        return typing.cast(typing.Optional["DataprocMetastoreServiceMetadataIntegration"], result)

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''The relative resource name of the VPC network on which the instance can be accessed.

        It is specified in the following form:

        "projects/{projectNumber}/global/networks/{network_id}".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#network DataprocMetastoreService#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_config(
        self,
    ) -> typing.Optional["DataprocMetastoreServiceNetworkConfig"]:
        '''network_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#network_config DataprocMetastoreService#network_config}
        '''
        result = self._values.get("network_config")
        return typing.cast(typing.Optional["DataprocMetastoreServiceNetworkConfig"], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The TCP port at which the metastore service is reached. Default: 9083.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#port DataprocMetastoreService#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#project DataprocMetastoreService#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def release_channel(self) -> typing.Optional[builtins.str]:
        '''The release channel of the service. If unspecified, defaults to 'STABLE'. Default value: "STABLE" Possible values: ["CANARY", "STABLE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#release_channel DataprocMetastoreService#release_channel}
        '''
        result = self._values.get("release_channel")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scaling_config(
        self,
    ) -> typing.Optional["DataprocMetastoreServiceScalingConfig"]:
        '''scaling_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#scaling_config DataprocMetastoreService#scaling_config}
        '''
        result = self._values.get("scaling_config")
        return typing.cast(typing.Optional["DataprocMetastoreServiceScalingConfig"], result)

    @builtins.property
    def scheduled_backup(
        self,
    ) -> typing.Optional["DataprocMetastoreServiceScheduledBackup"]:
        '''scheduled_backup block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#scheduled_backup DataprocMetastoreService#scheduled_backup}
        '''
        result = self._values.get("scheduled_backup")
        return typing.cast(typing.Optional["DataprocMetastoreServiceScheduledBackup"], result)

    @builtins.property
    def telemetry_config(
        self,
    ) -> typing.Optional["DataprocMetastoreServiceTelemetryConfig"]:
        '''telemetry_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#telemetry_config DataprocMetastoreService#telemetry_config}
        '''
        result = self._values.get("telemetry_config")
        return typing.cast(typing.Optional["DataprocMetastoreServiceTelemetryConfig"], result)

    @builtins.property
    def tier(self) -> typing.Optional[builtins.str]:
        '''The tier of the service. Possible values: ["DEVELOPER", "ENTERPRISE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#tier DataprocMetastoreService#tier}
        '''
        result = self._values.get("tier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DataprocMetastoreServiceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#timeouts DataprocMetastoreService#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DataprocMetastoreServiceTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocMetastoreServiceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocMetastoreService.DataprocMetastoreServiceEncryptionConfig",
    jsii_struct_bases=[],
    name_mapping={"kms_key": "kmsKey"},
)
class DataprocMetastoreServiceEncryptionConfig:
    def __init__(self, *, kms_key: builtins.str) -> None:
        '''
        :param kms_key: The fully qualified customer provided Cloud KMS key name to use for customer data encryption. Use the following format: 'projects/([^/]+)/locations/([^/]+)/keyRings/([^/]+)/cryptoKeys/([^/]+)'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#kms_key DataprocMetastoreService#kms_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d336eab06ad120c0fb7be7f82d516a8d670f81cd7afcfabfd9400962df3a3c2)
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kms_key": kms_key,
        }

    @builtins.property
    def kms_key(self) -> builtins.str:
        '''The fully qualified customer provided Cloud KMS key name to use for customer data encryption. Use the following format: 'projects/([^/]+)/locations/([^/]+)/keyRings/([^/]+)/cryptoKeys/([^/]+)'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#kms_key DataprocMetastoreService#kms_key}
        '''
        result = self._values.get("kms_key")
        assert result is not None, "Required property 'kms_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocMetastoreServiceEncryptionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocMetastoreServiceEncryptionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocMetastoreService.DataprocMetastoreServiceEncryptionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__be097f849d309ea8f78b601c1ee0e72513528e06937f66d902925fa8ced7b410)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="kmsKeyInput")
    def kms_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKey"))

    @kms_key.setter
    def kms_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0edb0bede55de9d86f482dd2e04580e6a3bd131c94e9fd58f96e6024cb7cf79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocMetastoreServiceEncryptionConfig]:
        return typing.cast(typing.Optional[DataprocMetastoreServiceEncryptionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocMetastoreServiceEncryptionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eae6cd602572895e0663edb8350d5004da1e725ef48af79d28fc7ff901cc313)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocMetastoreService.DataprocMetastoreServiceHiveMetastoreConfig",
    jsii_struct_bases=[],
    name_mapping={
        "version": "version",
        "auxiliary_versions": "auxiliaryVersions",
        "config_overrides": "configOverrides",
        "endpoint_protocol": "endpointProtocol",
        "kerberos_config": "kerberosConfig",
    },
)
class DataprocMetastoreServiceHiveMetastoreConfig:
    def __init__(
        self,
        *,
        version: builtins.str,
        auxiliary_versions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        config_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        endpoint_protocol: typing.Optional[builtins.str] = None,
        kerberos_config: typing.Optional[typing.Union["DataprocMetastoreServiceHiveMetastoreConfigKerberosConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param version: The Hive metastore schema version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#version DataprocMetastoreService#version}
        :param auxiliary_versions: auxiliary_versions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#auxiliary_versions DataprocMetastoreService#auxiliary_versions}
        :param config_overrides: A mapping of Hive metastore configuration key-value pairs to apply to the Hive metastore (configured in hive-site.xml). The mappings override system defaults (some keys cannot be overridden). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#config_overrides DataprocMetastoreService#config_overrides}
        :param endpoint_protocol: The protocol to use for the metastore service endpoint. If unspecified, defaults to 'THRIFT'. Default value: "THRIFT" Possible values: ["THRIFT", "GRPC"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#endpoint_protocol DataprocMetastoreService#endpoint_protocol}
        :param kerberos_config: kerberos_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#kerberos_config DataprocMetastoreService#kerberos_config}
        '''
        if isinstance(kerberos_config, dict):
            kerberos_config = DataprocMetastoreServiceHiveMetastoreConfigKerberosConfig(**kerberos_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e1b0242e6cc7888aa52d62efd9615db1a9417c9b095a978a585d563d6d762d3)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument auxiliary_versions", value=auxiliary_versions, expected_type=type_hints["auxiliary_versions"])
            check_type(argname="argument config_overrides", value=config_overrides, expected_type=type_hints["config_overrides"])
            check_type(argname="argument endpoint_protocol", value=endpoint_protocol, expected_type=type_hints["endpoint_protocol"])
            check_type(argname="argument kerberos_config", value=kerberos_config, expected_type=type_hints["kerberos_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "version": version,
        }
        if auxiliary_versions is not None:
            self._values["auxiliary_versions"] = auxiliary_versions
        if config_overrides is not None:
            self._values["config_overrides"] = config_overrides
        if endpoint_protocol is not None:
            self._values["endpoint_protocol"] = endpoint_protocol
        if kerberos_config is not None:
            self._values["kerberos_config"] = kerberos_config

    @builtins.property
    def version(self) -> builtins.str:
        '''The Hive metastore schema version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#version DataprocMetastoreService#version}
        '''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auxiliary_versions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersions"]]]:
        '''auxiliary_versions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#auxiliary_versions DataprocMetastoreService#auxiliary_versions}
        '''
        result = self._values.get("auxiliary_versions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersions"]]], result)

    @builtins.property
    def config_overrides(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A mapping of Hive metastore configuration key-value pairs to apply to the Hive metastore (configured in hive-site.xml). The mappings override system defaults (some keys cannot be overridden).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#config_overrides DataprocMetastoreService#config_overrides}
        '''
        result = self._values.get("config_overrides")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def endpoint_protocol(self) -> typing.Optional[builtins.str]:
        '''The protocol to use for the metastore service endpoint.

        If unspecified, defaults to 'THRIFT'. Default value: "THRIFT" Possible values: ["THRIFT", "GRPC"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#endpoint_protocol DataprocMetastoreService#endpoint_protocol}
        '''
        result = self._values.get("endpoint_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kerberos_config(
        self,
    ) -> typing.Optional["DataprocMetastoreServiceHiveMetastoreConfigKerberosConfig"]:
        '''kerberos_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#kerberos_config DataprocMetastoreService#kerberos_config}
        '''
        result = self._values.get("kerberos_config")
        return typing.cast(typing.Optional["DataprocMetastoreServiceHiveMetastoreConfigKerberosConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocMetastoreServiceHiveMetastoreConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocMetastoreService.DataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersions",
    jsii_struct_bases=[],
    name_mapping={
        "key": "key",
        "version": "version",
        "config_overrides": "configOverrides",
    },
)
class DataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersions:
    def __init__(
        self,
        *,
        key: builtins.str,
        version: builtins.str,
        config_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#key DataprocMetastoreService#key}.
        :param version: The Hive metastore version of the auxiliary service. It must be less than the primary Hive metastore service's version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#version DataprocMetastoreService#version}
        :param config_overrides: A mapping of Hive metastore configuration key-value pairs to apply to the auxiliary Hive metastore (configured in hive-site.xml) in addition to the primary version's overrides. If keys are present in both the auxiliary version's overrides and the primary version's overrides, the value from the auxiliary version's overrides takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#config_overrides DataprocMetastoreService#config_overrides}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67ab7f8c4561dce41958922f1ef0440ea4c27dd07f315aa85014cd2f6dc0e53d)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument config_overrides", value=config_overrides, expected_type=type_hints["config_overrides"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "version": version,
        }
        if config_overrides is not None:
            self._values["config_overrides"] = config_overrides

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#key DataprocMetastoreService#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''The Hive metastore version of the auxiliary service. It must be less than the primary Hive metastore service's version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#version DataprocMetastoreService#version}
        '''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def config_overrides(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A mapping of Hive metastore configuration key-value pairs to apply to the auxiliary Hive metastore (configured in hive-site.xml) in addition to the primary version's overrides. If keys are present in both the auxiliary version's overrides and the primary version's overrides, the value from the auxiliary version's overrides takes precedence.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#config_overrides DataprocMetastoreService#config_overrides}
        '''
        result = self._values.get("config_overrides")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocMetastoreService.DataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4da1f66e5237a2338d58f403ce7ed8787328890cf92e9526d574225ff281cb3f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69837f975a040667b3231e3c9b5dd86cecba3f2de772aeab18394c9c26544fe3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__412fcdbf7f1710c7fbdf38ca49f524d83af11688a43fba85c630e40631241ecd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f620570b31d600f6192a6415b389103daa45f12a72513a9142c3053a7f149786)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7fef756029ac0c7ad78fbfff9fe2ef9d4eea958a0fc6b9ef2bcc9f3c77c5064)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__436dac4b0405692ed009fc6c1912c666bd8369dd218845b274cd5cd8174bfc60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocMetastoreService.DataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3a8385105940b361717080bb2953abc381ef771116017b24fe16353be821e5a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetConfigOverrides")
    def reset_config_overrides(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfigOverrides", []))

    @builtins.property
    @jsii.member(jsii_name="configOverridesInput")
    def config_overrides_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "configOverridesInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="configOverrides")
    def config_overrides(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "configOverrides"))

    @config_overrides.setter
    def config_overrides(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89e318ba4c8f75e42e397367f91110926ce5e2cfd036d44e79654dcdbb44a711)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configOverrides", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be41f8c823fd602eea5afd24b0bc24647fe434c0624604a78e4a51c1445261d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c3081559186163b3dff1a1e86bcd4bad8b00381391975d6addca7fd9d6090cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3406b03c1b6e042807ae80755a3a3b61dfa3874a31abef9fcddd359f334eca0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocMetastoreService.DataprocMetastoreServiceHiveMetastoreConfigKerberosConfig",
    jsii_struct_bases=[],
    name_mapping={
        "keytab": "keytab",
        "krb5_config_gcs_uri": "krb5ConfigGcsUri",
        "principal": "principal",
    },
)
class DataprocMetastoreServiceHiveMetastoreConfigKerberosConfig:
    def __init__(
        self,
        *,
        keytab: typing.Union["DataprocMetastoreServiceHiveMetastoreConfigKerberosConfigKeytab", typing.Dict[builtins.str, typing.Any]],
        krb5_config_gcs_uri: builtins.str,
        principal: builtins.str,
    ) -> None:
        '''
        :param keytab: keytab block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#keytab DataprocMetastoreService#keytab}
        :param krb5_config_gcs_uri: A Cloud Storage URI that specifies the path to a krb5.conf file. It is of the form gs://{bucket_name}/path/to/krb5.conf, although the file does not need to be named krb5.conf explicitly. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#krb5_config_gcs_uri DataprocMetastoreService#krb5_config_gcs_uri}
        :param principal: A Kerberos principal that exists in the both the keytab the KDC to authenticate as. A typical principal is of the form "primary/instance@REALM", but there is no exact format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#principal DataprocMetastoreService#principal}
        '''
        if isinstance(keytab, dict):
            keytab = DataprocMetastoreServiceHiveMetastoreConfigKerberosConfigKeytab(**keytab)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01f68992e7773d044fce5127bf11fd231005f8f878036aabbc99912776caf743)
            check_type(argname="argument keytab", value=keytab, expected_type=type_hints["keytab"])
            check_type(argname="argument krb5_config_gcs_uri", value=krb5_config_gcs_uri, expected_type=type_hints["krb5_config_gcs_uri"])
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "keytab": keytab,
            "krb5_config_gcs_uri": krb5_config_gcs_uri,
            "principal": principal,
        }

    @builtins.property
    def keytab(
        self,
    ) -> "DataprocMetastoreServiceHiveMetastoreConfigKerberosConfigKeytab":
        '''keytab block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#keytab DataprocMetastoreService#keytab}
        '''
        result = self._values.get("keytab")
        assert result is not None, "Required property 'keytab' is missing"
        return typing.cast("DataprocMetastoreServiceHiveMetastoreConfigKerberosConfigKeytab", result)

    @builtins.property
    def krb5_config_gcs_uri(self) -> builtins.str:
        '''A Cloud Storage URI that specifies the path to a krb5.conf file. It is of the form gs://{bucket_name}/path/to/krb5.conf, although the file does not need to be named krb5.conf explicitly.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#krb5_config_gcs_uri DataprocMetastoreService#krb5_config_gcs_uri}
        '''
        result = self._values.get("krb5_config_gcs_uri")
        assert result is not None, "Required property 'krb5_config_gcs_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def principal(self) -> builtins.str:
        '''A Kerberos principal that exists in the both the keytab the KDC to authenticate as.

        A typical principal is of the form "primary/instance@REALM", but there is no exact format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#principal DataprocMetastoreService#principal}
        '''
        result = self._values.get("principal")
        assert result is not None, "Required property 'principal' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocMetastoreServiceHiveMetastoreConfigKerberosConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocMetastoreService.DataprocMetastoreServiceHiveMetastoreConfigKerberosConfigKeytab",
    jsii_struct_bases=[],
    name_mapping={"cloud_secret": "cloudSecret"},
)
class DataprocMetastoreServiceHiveMetastoreConfigKerberosConfigKeytab:
    def __init__(self, *, cloud_secret: builtins.str) -> None:
        '''
        :param cloud_secret: The relative resource name of a Secret Manager secret version, in the following form:. "projects/{projectNumber}/secrets/{secret_id}/versions/{version_id}". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#cloud_secret DataprocMetastoreService#cloud_secret}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba58ab8776add2656543da21fee71a9429b74a88fee210a8ae9f6f7c881c58bb)
            check_type(argname="argument cloud_secret", value=cloud_secret, expected_type=type_hints["cloud_secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cloud_secret": cloud_secret,
        }

    @builtins.property
    def cloud_secret(self) -> builtins.str:
        '''The relative resource name of a Secret Manager secret version, in the following form:.

        "projects/{projectNumber}/secrets/{secret_id}/versions/{version_id}".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#cloud_secret DataprocMetastoreService#cloud_secret}
        '''
        result = self._values.get("cloud_secret")
        assert result is not None, "Required property 'cloud_secret' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocMetastoreServiceHiveMetastoreConfigKerberosConfigKeytab(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocMetastoreServiceHiveMetastoreConfigKerberosConfigKeytabOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocMetastoreService.DataprocMetastoreServiceHiveMetastoreConfigKerberosConfigKeytabOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a78d50dc12776cdc206c393d08beb7adc0f661703f05a4ab185b45d037605c6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="cloudSecretInput")
    def cloud_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudSecret")
    def cloud_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudSecret"))

    @cloud_secret.setter
    def cloud_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87af15ec001985bbde22095ce133ded406e993dd991bd937d25bed3d6deac4c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocMetastoreServiceHiveMetastoreConfigKerberosConfigKeytab]:
        return typing.cast(typing.Optional[DataprocMetastoreServiceHiveMetastoreConfigKerberosConfigKeytab], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocMetastoreServiceHiveMetastoreConfigKerberosConfigKeytab],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbd1a37ed2c50599966877eabadb494f8b0cae934726ee0952975fced7db2e68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataprocMetastoreServiceHiveMetastoreConfigKerberosConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocMetastoreService.DataprocMetastoreServiceHiveMetastoreConfigKerberosConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b2ed886bfdeca65edaca9f037ac172f81611e7fab8d1a1e2f8cb9a18f1bf95a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putKeytab")
    def put_keytab(self, *, cloud_secret: builtins.str) -> None:
        '''
        :param cloud_secret: The relative resource name of a Secret Manager secret version, in the following form:. "projects/{projectNumber}/secrets/{secret_id}/versions/{version_id}". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#cloud_secret DataprocMetastoreService#cloud_secret}
        '''
        value = DataprocMetastoreServiceHiveMetastoreConfigKerberosConfigKeytab(
            cloud_secret=cloud_secret
        )

        return typing.cast(None, jsii.invoke(self, "putKeytab", [value]))

    @builtins.property
    @jsii.member(jsii_name="keytab")
    def keytab(
        self,
    ) -> DataprocMetastoreServiceHiveMetastoreConfigKerberosConfigKeytabOutputReference:
        return typing.cast(DataprocMetastoreServiceHiveMetastoreConfigKerberosConfigKeytabOutputReference, jsii.get(self, "keytab"))

    @builtins.property
    @jsii.member(jsii_name="keytabInput")
    def keytab_input(
        self,
    ) -> typing.Optional[DataprocMetastoreServiceHiveMetastoreConfigKerberosConfigKeytab]:
        return typing.cast(typing.Optional[DataprocMetastoreServiceHiveMetastoreConfigKerberosConfigKeytab], jsii.get(self, "keytabInput"))

    @builtins.property
    @jsii.member(jsii_name="krb5ConfigGcsUriInput")
    def krb5_config_gcs_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "krb5ConfigGcsUriInput"))

    @builtins.property
    @jsii.member(jsii_name="principalInput")
    def principal_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "principalInput"))

    @builtins.property
    @jsii.member(jsii_name="krb5ConfigGcsUri")
    def krb5_config_gcs_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "krb5ConfigGcsUri"))

    @krb5_config_gcs_uri.setter
    def krb5_config_gcs_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67154394df902fd2bc8291c60f6fe1a2fe8250137e66547e5f2adf3100f2b4c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "krb5ConfigGcsUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="principal")
    def principal(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "principal"))

    @principal.setter
    def principal(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7861945876207533fb0d30c090d7de627a0a40c76c0f9d7161c2c3c8ca7b9323)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "principal", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocMetastoreServiceHiveMetastoreConfigKerberosConfig]:
        return typing.cast(typing.Optional[DataprocMetastoreServiceHiveMetastoreConfigKerberosConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocMetastoreServiceHiveMetastoreConfigKerberosConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__273372d176acc28db5c1b5a68a9614eef41f039a36f4b758aa4340762c718f4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataprocMetastoreServiceHiveMetastoreConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocMetastoreService.DataprocMetastoreServiceHiveMetastoreConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1e446c286735a1665fc8ed7e1f111a74e8010807d34b3561219fc5f2609f6d5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAuxiliaryVersions")
    def put_auxiliary_versions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6018107f80d6a457f8551b25a8f37c6479730fefbc8111cad3f3f0d8608ce7ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAuxiliaryVersions", [value]))

    @jsii.member(jsii_name="putKerberosConfig")
    def put_kerberos_config(
        self,
        *,
        keytab: typing.Union[DataprocMetastoreServiceHiveMetastoreConfigKerberosConfigKeytab, typing.Dict[builtins.str, typing.Any]],
        krb5_config_gcs_uri: builtins.str,
        principal: builtins.str,
    ) -> None:
        '''
        :param keytab: keytab block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#keytab DataprocMetastoreService#keytab}
        :param krb5_config_gcs_uri: A Cloud Storage URI that specifies the path to a krb5.conf file. It is of the form gs://{bucket_name}/path/to/krb5.conf, although the file does not need to be named krb5.conf explicitly. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#krb5_config_gcs_uri DataprocMetastoreService#krb5_config_gcs_uri}
        :param principal: A Kerberos principal that exists in the both the keytab the KDC to authenticate as. A typical principal is of the form "primary/instance@REALM", but there is no exact format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#principal DataprocMetastoreService#principal}
        '''
        value = DataprocMetastoreServiceHiveMetastoreConfigKerberosConfig(
            keytab=keytab, krb5_config_gcs_uri=krb5_config_gcs_uri, principal=principal
        )

        return typing.cast(None, jsii.invoke(self, "putKerberosConfig", [value]))

    @jsii.member(jsii_name="resetAuxiliaryVersions")
    def reset_auxiliary_versions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuxiliaryVersions", []))

    @jsii.member(jsii_name="resetConfigOverrides")
    def reset_config_overrides(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfigOverrides", []))

    @jsii.member(jsii_name="resetEndpointProtocol")
    def reset_endpoint_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpointProtocol", []))

    @jsii.member(jsii_name="resetKerberosConfig")
    def reset_kerberos_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKerberosConfig", []))

    @builtins.property
    @jsii.member(jsii_name="auxiliaryVersions")
    def auxiliary_versions(
        self,
    ) -> DataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersionsList:
        return typing.cast(DataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersionsList, jsii.get(self, "auxiliaryVersions"))

    @builtins.property
    @jsii.member(jsii_name="kerberosConfig")
    def kerberos_config(
        self,
    ) -> DataprocMetastoreServiceHiveMetastoreConfigKerberosConfigOutputReference:
        return typing.cast(DataprocMetastoreServiceHiveMetastoreConfigKerberosConfigOutputReference, jsii.get(self, "kerberosConfig"))

    @builtins.property
    @jsii.member(jsii_name="auxiliaryVersionsInput")
    def auxiliary_versions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersions]]], jsii.get(self, "auxiliaryVersionsInput"))

    @builtins.property
    @jsii.member(jsii_name="configOverridesInput")
    def config_overrides_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "configOverridesInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointProtocolInput")
    def endpoint_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="kerberosConfigInput")
    def kerberos_config_input(
        self,
    ) -> typing.Optional[DataprocMetastoreServiceHiveMetastoreConfigKerberosConfig]:
        return typing.cast(typing.Optional[DataprocMetastoreServiceHiveMetastoreConfigKerberosConfig], jsii.get(self, "kerberosConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="configOverrides")
    def config_overrides(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "configOverrides"))

    @config_overrides.setter
    def config_overrides(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76250e088fc3f8f5fafa73b6c241fd7f5a04591cec4488e4dadc544d2df21f18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configOverrides", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endpointProtocol")
    def endpoint_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpointProtocol"))

    @endpoint_protocol.setter
    def endpoint_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb41b31425a78dd42854112e95411776768b22e62820f44d5e01568dc50bd940)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61529528962844ed4224eb84be8a712f6e99649e2d00c38a6ed4c6735b59ea56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocMetastoreServiceHiveMetastoreConfig]:
        return typing.cast(typing.Optional[DataprocMetastoreServiceHiveMetastoreConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocMetastoreServiceHiveMetastoreConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dbc76bde9c1759d3c56d4b1d0e42cf2091a98263485c994136e94ca58a7ae05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocMetastoreService.DataprocMetastoreServiceMaintenanceWindow",
    jsii_struct_bases=[],
    name_mapping={"day_of_week": "dayOfWeek", "hour_of_day": "hourOfDay"},
)
class DataprocMetastoreServiceMaintenanceWindow:
    def __init__(self, *, day_of_week: builtins.str, hour_of_day: jsii.Number) -> None:
        '''
        :param day_of_week: The day of week, when the window starts. Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#day_of_week DataprocMetastoreService#day_of_week}
        :param hour_of_day: The hour of day (0-23) when the window starts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#hour_of_day DataprocMetastoreService#hour_of_day}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37c544e5fde22a515907b412d11472d793008ae89880d48cdb98e1a6ce066ced)
            check_type(argname="argument day_of_week", value=day_of_week, expected_type=type_hints["day_of_week"])
            check_type(argname="argument hour_of_day", value=hour_of_day, expected_type=type_hints["hour_of_day"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "day_of_week": day_of_week,
            "hour_of_day": hour_of_day,
        }

    @builtins.property
    def day_of_week(self) -> builtins.str:
        '''The day of week, when the window starts. Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#day_of_week DataprocMetastoreService#day_of_week}
        '''
        result = self._values.get("day_of_week")
        assert result is not None, "Required property 'day_of_week' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hour_of_day(self) -> jsii.Number:
        '''The hour of day (0-23) when the window starts.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#hour_of_day DataprocMetastoreService#hour_of_day}
        '''
        result = self._values.get("hour_of_day")
        assert result is not None, "Required property 'hour_of_day' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocMetastoreServiceMaintenanceWindow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocMetastoreServiceMaintenanceWindowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocMetastoreService.DataprocMetastoreServiceMaintenanceWindowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d171bbc78de196dc060f85e1cad82085e5373e0a8827c96febd4a1efc1cd090)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="dayOfWeekInput")
    def day_of_week_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dayOfWeekInput"))

    @builtins.property
    @jsii.member(jsii_name="hourOfDayInput")
    def hour_of_day_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hourOfDayInput"))

    @builtins.property
    @jsii.member(jsii_name="dayOfWeek")
    def day_of_week(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dayOfWeek"))

    @day_of_week.setter
    def day_of_week(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__603051864a6dd185e33c74f4e2e554fb023a6e1243e1cc82f053c3d8d3124469)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dayOfWeek", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hourOfDay")
    def hour_of_day(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hourOfDay"))

    @hour_of_day.setter
    def hour_of_day(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__263627d5caa87b46db5a99a1e0add63e3f200228a2a79ed757b230ac126b090a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hourOfDay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocMetastoreServiceMaintenanceWindow]:
        return typing.cast(typing.Optional[DataprocMetastoreServiceMaintenanceWindow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocMetastoreServiceMaintenanceWindow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__517b85764561e09db3bf91b07eb19d9342cd96bc20631eb69d65354cbfc584ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocMetastoreService.DataprocMetastoreServiceMetadataIntegration",
    jsii_struct_bases=[],
    name_mapping={"data_catalog_config": "dataCatalogConfig"},
)
class DataprocMetastoreServiceMetadataIntegration:
    def __init__(
        self,
        *,
        data_catalog_config: typing.Union["DataprocMetastoreServiceMetadataIntegrationDataCatalogConfig", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param data_catalog_config: data_catalog_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#data_catalog_config DataprocMetastoreService#data_catalog_config}
        '''
        if isinstance(data_catalog_config, dict):
            data_catalog_config = DataprocMetastoreServiceMetadataIntegrationDataCatalogConfig(**data_catalog_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__944a1616f4c9de07a7370cbf2b92d899266f66fbc41442b1a17754a204f17310)
            check_type(argname="argument data_catalog_config", value=data_catalog_config, expected_type=type_hints["data_catalog_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_catalog_config": data_catalog_config,
        }

    @builtins.property
    def data_catalog_config(
        self,
    ) -> "DataprocMetastoreServiceMetadataIntegrationDataCatalogConfig":
        '''data_catalog_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#data_catalog_config DataprocMetastoreService#data_catalog_config}
        '''
        result = self._values.get("data_catalog_config")
        assert result is not None, "Required property 'data_catalog_config' is missing"
        return typing.cast("DataprocMetastoreServiceMetadataIntegrationDataCatalogConfig", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocMetastoreServiceMetadataIntegration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocMetastoreService.DataprocMetastoreServiceMetadataIntegrationDataCatalogConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class DataprocMetastoreServiceMetadataIntegrationDataCatalogConfig:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Defines whether the metastore metadata should be synced to Data Catalog. The default value is to disable syncing metastore metadata to Data Catalog. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#enabled DataprocMetastoreService#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__645ad1901e7fe0baf1f9cb74274228e829268a353a519abe757c0d7a12f96786)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Defines whether the metastore metadata should be synced to Data Catalog.

        The default value is to disable syncing metastore metadata to Data Catalog.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#enabled DataprocMetastoreService#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocMetastoreServiceMetadataIntegrationDataCatalogConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocMetastoreServiceMetadataIntegrationDataCatalogConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocMetastoreService.DataprocMetastoreServiceMetadataIntegrationDataCatalogConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__97d7e4bda7ecc45c27793366e2c707aae62bd24575fa77e59add1d4ce8c77379)
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
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e7219c02f0dc0ba5793cb9cf1a646d43c161cc460ac6ef27d37bf9393a4ca45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocMetastoreServiceMetadataIntegrationDataCatalogConfig]:
        return typing.cast(typing.Optional[DataprocMetastoreServiceMetadataIntegrationDataCatalogConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocMetastoreServiceMetadataIntegrationDataCatalogConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c98ee2ad30e6ea8bc3caa62ad20e6918f18f87c497fb4299ceeca8d513c1ff38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataprocMetastoreServiceMetadataIntegrationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocMetastoreService.DataprocMetastoreServiceMetadataIntegrationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3caf0afe4817838290b19d8fc54626ff5d168ceb5040bffd52956b2a8d29049)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDataCatalogConfig")
    def put_data_catalog_config(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Defines whether the metastore metadata should be synced to Data Catalog. The default value is to disable syncing metastore metadata to Data Catalog. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#enabled DataprocMetastoreService#enabled}
        '''
        value = DataprocMetastoreServiceMetadataIntegrationDataCatalogConfig(
            enabled=enabled
        )

        return typing.cast(None, jsii.invoke(self, "putDataCatalogConfig", [value]))

    @builtins.property
    @jsii.member(jsii_name="dataCatalogConfig")
    def data_catalog_config(
        self,
    ) -> DataprocMetastoreServiceMetadataIntegrationDataCatalogConfigOutputReference:
        return typing.cast(DataprocMetastoreServiceMetadataIntegrationDataCatalogConfigOutputReference, jsii.get(self, "dataCatalogConfig"))

    @builtins.property
    @jsii.member(jsii_name="dataCatalogConfigInput")
    def data_catalog_config_input(
        self,
    ) -> typing.Optional[DataprocMetastoreServiceMetadataIntegrationDataCatalogConfig]:
        return typing.cast(typing.Optional[DataprocMetastoreServiceMetadataIntegrationDataCatalogConfig], jsii.get(self, "dataCatalogConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocMetastoreServiceMetadataIntegration]:
        return typing.cast(typing.Optional[DataprocMetastoreServiceMetadataIntegration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocMetastoreServiceMetadataIntegration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a11b9cc0aa729e3cecdd070356411d8ce9fa80b0f4191b0ada4c5bd2a2747a7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocMetastoreService.DataprocMetastoreServiceNetworkConfig",
    jsii_struct_bases=[],
    name_mapping={"consumers": "consumers"},
)
class DataprocMetastoreServiceNetworkConfig:
    def __init__(
        self,
        *,
        consumers: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataprocMetastoreServiceNetworkConfigConsumers", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param consumers: consumers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#consumers DataprocMetastoreService#consumers}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35ec65f5d9d0fad4d8c7434d85c8ad05c1c8af765624d1cba1ba5c7c9251d92f)
            check_type(argname="argument consumers", value=consumers, expected_type=type_hints["consumers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "consumers": consumers,
        }

    @builtins.property
    def consumers(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataprocMetastoreServiceNetworkConfigConsumers"]]:
        '''consumers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#consumers DataprocMetastoreService#consumers}
        '''
        result = self._values.get("consumers")
        assert result is not None, "Required property 'consumers' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataprocMetastoreServiceNetworkConfigConsumers"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocMetastoreServiceNetworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocMetastoreService.DataprocMetastoreServiceNetworkConfigConsumers",
    jsii_struct_bases=[],
    name_mapping={"subnetwork": "subnetwork"},
)
class DataprocMetastoreServiceNetworkConfigConsumers:
    def __init__(self, *, subnetwork: builtins.str) -> None:
        '''
        :param subnetwork: The subnetwork of the customer project from which an IP address is reserved and used as the Dataproc Metastore service's endpoint. It is accessible to hosts in the subnet and to all hosts in a subnet in the same region and same network. There must be at least one IP address available in the subnet's primary range. The subnet is specified in the following form: 'projects/{projectNumber}/regions/{region_id}/subnetworks/{subnetwork_id} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#subnetwork DataprocMetastoreService#subnetwork}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5c7b785655c488a57bc98d4a8ce258382c67f949e6d590edb936d1ee3650f4e)
            check_type(argname="argument subnetwork", value=subnetwork, expected_type=type_hints["subnetwork"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subnetwork": subnetwork,
        }

    @builtins.property
    def subnetwork(self) -> builtins.str:
        '''The subnetwork of the customer project from which an IP address is reserved and used as the Dataproc Metastore service's endpoint.

        It is accessible to hosts in the subnet and to all hosts in a subnet in the same region and same network.
        There must be at least one IP address available in the subnet's primary range. The subnet is specified in the following form:
        'projects/{projectNumber}/regions/{region_id}/subnetworks/{subnetwork_id}

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#subnetwork DataprocMetastoreService#subnetwork}
        '''
        result = self._values.get("subnetwork")
        assert result is not None, "Required property 'subnetwork' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocMetastoreServiceNetworkConfigConsumers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocMetastoreServiceNetworkConfigConsumersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocMetastoreService.DataprocMetastoreServiceNetworkConfigConsumersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c43dada6af8841b1cf431898ab976146bfdb624dca47684aa3feb3d3f868f032)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataprocMetastoreServiceNetworkConfigConsumersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27f670900a9f60e43bc4967c79cafd253eb214bfd24f289be7b22ddd7dcbd5a1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataprocMetastoreServiceNetworkConfigConsumersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abfaeb86eb373a9d53ba643a2999090dbf04074bdec9d8ee96e2fe5d218b1719)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b9a54d131623e87b65739c7c4775bac6c4eb39305f9a59dd05084edc4e572d2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ab4ba6c4250d441859c6cf7a0a48e8e09b31587bc61846a931fb6b97ab314c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocMetastoreServiceNetworkConfigConsumers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocMetastoreServiceNetworkConfigConsumers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocMetastoreServiceNetworkConfigConsumers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2032d6986f313eb4cdc93baf2cae22e6efac7d978817cb65799074b05152afbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataprocMetastoreServiceNetworkConfigConsumersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocMetastoreService.DataprocMetastoreServiceNetworkConfigConsumersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2c64386a63a9acf36c7cd080b9bac3a84750c5da3958a3f4b6ab4d2353e4ad0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="endpointUri")
    def endpoint_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpointUri"))

    @builtins.property
    @jsii.member(jsii_name="subnetworkInput")
    def subnetwork_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetwork")
    def subnetwork(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetwork"))

    @subnetwork.setter
    def subnetwork(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__194988a679b4f55240396e08eba64fd86ad22931ccd852b9d9e143d6527b443d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocMetastoreServiceNetworkConfigConsumers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocMetastoreServiceNetworkConfigConsumers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocMetastoreServiceNetworkConfigConsumers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__300418f8347dc08a1751db46603645575a0c1c683e958058ebec49be570ef394)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataprocMetastoreServiceNetworkConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocMetastoreService.DataprocMetastoreServiceNetworkConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0eb2eb4c4fe5c5ce85553a673db61896dfc0b220e45ac826a23d6eea48ff5d94)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConsumers")
    def put_consumers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataprocMetastoreServiceNetworkConfigConsumers, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bc55508cd865831a4c905ef02e146b6404e9b4a0b66f127ac68e87c80424535)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConsumers", [value]))

    @builtins.property
    @jsii.member(jsii_name="consumers")
    def consumers(self) -> DataprocMetastoreServiceNetworkConfigConsumersList:
        return typing.cast(DataprocMetastoreServiceNetworkConfigConsumersList, jsii.get(self, "consumers"))

    @builtins.property
    @jsii.member(jsii_name="consumersInput")
    def consumers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocMetastoreServiceNetworkConfigConsumers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocMetastoreServiceNetworkConfigConsumers]]], jsii.get(self, "consumersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataprocMetastoreServiceNetworkConfig]:
        return typing.cast(typing.Optional[DataprocMetastoreServiceNetworkConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocMetastoreServiceNetworkConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__852c6101e2cd2ff20c35b013d4fc303b7aeccbd973935b52c3918d23918b2df0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocMetastoreService.DataprocMetastoreServiceScalingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "autoscaling_config": "autoscalingConfig",
        "instance_size": "instanceSize",
        "scaling_factor": "scalingFactor",
    },
)
class DataprocMetastoreServiceScalingConfig:
    def __init__(
        self,
        *,
        autoscaling_config: typing.Optional[typing.Union["DataprocMetastoreServiceScalingConfigAutoscalingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        instance_size: typing.Optional[builtins.str] = None,
        scaling_factor: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param autoscaling_config: autoscaling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#autoscaling_config DataprocMetastoreService#autoscaling_config}
        :param instance_size: Metastore instance sizes. Possible values: ["EXTRA_SMALL", "SMALL", "MEDIUM", "LARGE", "EXTRA_LARGE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#instance_size DataprocMetastoreService#instance_size}
        :param scaling_factor: Scaling factor, in increments of 0.1 for values less than 1.0, and increments of 1.0 for values greater than 1.0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#scaling_factor DataprocMetastoreService#scaling_factor}
        '''
        if isinstance(autoscaling_config, dict):
            autoscaling_config = DataprocMetastoreServiceScalingConfigAutoscalingConfig(**autoscaling_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43710df38faebed6fcc8600dc5c389c030636f1c4575943d5e040d4fbd165a95)
            check_type(argname="argument autoscaling_config", value=autoscaling_config, expected_type=type_hints["autoscaling_config"])
            check_type(argname="argument instance_size", value=instance_size, expected_type=type_hints["instance_size"])
            check_type(argname="argument scaling_factor", value=scaling_factor, expected_type=type_hints["scaling_factor"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if autoscaling_config is not None:
            self._values["autoscaling_config"] = autoscaling_config
        if instance_size is not None:
            self._values["instance_size"] = instance_size
        if scaling_factor is not None:
            self._values["scaling_factor"] = scaling_factor

    @builtins.property
    def autoscaling_config(
        self,
    ) -> typing.Optional["DataprocMetastoreServiceScalingConfigAutoscalingConfig"]:
        '''autoscaling_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#autoscaling_config DataprocMetastoreService#autoscaling_config}
        '''
        result = self._values.get("autoscaling_config")
        return typing.cast(typing.Optional["DataprocMetastoreServiceScalingConfigAutoscalingConfig"], result)

    @builtins.property
    def instance_size(self) -> typing.Optional[builtins.str]:
        '''Metastore instance sizes. Possible values: ["EXTRA_SMALL", "SMALL", "MEDIUM", "LARGE", "EXTRA_LARGE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#instance_size DataprocMetastoreService#instance_size}
        '''
        result = self._values.get("instance_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scaling_factor(self) -> typing.Optional[jsii.Number]:
        '''Scaling factor, in increments of 0.1 for values less than 1.0, and increments of 1.0 for values greater than 1.0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#scaling_factor DataprocMetastoreService#scaling_factor}
        '''
        result = self._values.get("scaling_factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocMetastoreServiceScalingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocMetastoreService.DataprocMetastoreServiceScalingConfigAutoscalingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "autoscaling_enabled": "autoscalingEnabled",
        "limit_config": "limitConfig",
    },
)
class DataprocMetastoreServiceScalingConfigAutoscalingConfig:
    def __init__(
        self,
        *,
        autoscaling_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        limit_config: typing.Optional[typing.Union["DataprocMetastoreServiceScalingConfigAutoscalingConfigLimitConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param autoscaling_enabled: Defines whether autoscaling is enabled. The default value is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#autoscaling_enabled DataprocMetastoreService#autoscaling_enabled}
        :param limit_config: limit_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#limit_config DataprocMetastoreService#limit_config}
        '''
        if isinstance(limit_config, dict):
            limit_config = DataprocMetastoreServiceScalingConfigAutoscalingConfigLimitConfig(**limit_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e9a36c69cd450e230eeebdbe6583bb1077f42bdb4f01bd9955bad510c802581)
            check_type(argname="argument autoscaling_enabled", value=autoscaling_enabled, expected_type=type_hints["autoscaling_enabled"])
            check_type(argname="argument limit_config", value=limit_config, expected_type=type_hints["limit_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if autoscaling_enabled is not None:
            self._values["autoscaling_enabled"] = autoscaling_enabled
        if limit_config is not None:
            self._values["limit_config"] = limit_config

    @builtins.property
    def autoscaling_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defines whether autoscaling is enabled. The default value is false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#autoscaling_enabled DataprocMetastoreService#autoscaling_enabled}
        '''
        result = self._values.get("autoscaling_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def limit_config(
        self,
    ) -> typing.Optional["DataprocMetastoreServiceScalingConfigAutoscalingConfigLimitConfig"]:
        '''limit_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#limit_config DataprocMetastoreService#limit_config}
        '''
        result = self._values.get("limit_config")
        return typing.cast(typing.Optional["DataprocMetastoreServiceScalingConfigAutoscalingConfigLimitConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocMetastoreServiceScalingConfigAutoscalingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocMetastoreService.DataprocMetastoreServiceScalingConfigAutoscalingConfigLimitConfig",
    jsii_struct_bases=[],
    name_mapping={
        "max_scaling_factor": "maxScalingFactor",
        "min_scaling_factor": "minScalingFactor",
    },
)
class DataprocMetastoreServiceScalingConfigAutoscalingConfigLimitConfig:
    def __init__(
        self,
        *,
        max_scaling_factor: typing.Optional[jsii.Number] = None,
        min_scaling_factor: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_scaling_factor: The maximum scaling factor that the service will autoscale to. The default value is 6.0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#max_scaling_factor DataprocMetastoreService#max_scaling_factor}
        :param min_scaling_factor: The minimum scaling factor that the service will autoscale to. The default value is 0.1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#min_scaling_factor DataprocMetastoreService#min_scaling_factor}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9137a36d4c570d9984a8f69ebae4862c8147d83cb181c69dd00c7a9621dfaf54)
            check_type(argname="argument max_scaling_factor", value=max_scaling_factor, expected_type=type_hints["max_scaling_factor"])
            check_type(argname="argument min_scaling_factor", value=min_scaling_factor, expected_type=type_hints["min_scaling_factor"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_scaling_factor is not None:
            self._values["max_scaling_factor"] = max_scaling_factor
        if min_scaling_factor is not None:
            self._values["min_scaling_factor"] = min_scaling_factor

    @builtins.property
    def max_scaling_factor(self) -> typing.Optional[jsii.Number]:
        '''The maximum scaling factor that the service will autoscale to. The default value is 6.0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#max_scaling_factor DataprocMetastoreService#max_scaling_factor}
        '''
        result = self._values.get("max_scaling_factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_scaling_factor(self) -> typing.Optional[jsii.Number]:
        '''The minimum scaling factor that the service will autoscale to. The default value is 0.1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#min_scaling_factor DataprocMetastoreService#min_scaling_factor}
        '''
        result = self._values.get("min_scaling_factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocMetastoreServiceScalingConfigAutoscalingConfigLimitConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocMetastoreServiceScalingConfigAutoscalingConfigLimitConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocMetastoreService.DataprocMetastoreServiceScalingConfigAutoscalingConfigLimitConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea61e385aa867aaef1fbb55bdfc05cf0eb2f365e65d0980161df7af0e98f26d9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxScalingFactor")
    def reset_max_scaling_factor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxScalingFactor", []))

    @jsii.member(jsii_name="resetMinScalingFactor")
    def reset_min_scaling_factor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinScalingFactor", []))

    @builtins.property
    @jsii.member(jsii_name="maxScalingFactorInput")
    def max_scaling_factor_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxScalingFactorInput"))

    @builtins.property
    @jsii.member(jsii_name="minScalingFactorInput")
    def min_scaling_factor_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minScalingFactorInput"))

    @builtins.property
    @jsii.member(jsii_name="maxScalingFactor")
    def max_scaling_factor(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxScalingFactor"))

    @max_scaling_factor.setter
    def max_scaling_factor(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8704c63db4fc9aa14874703cba1fd15126b8eef875e0ae99f973298064232266)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxScalingFactor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minScalingFactor")
    def min_scaling_factor(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minScalingFactor"))

    @min_scaling_factor.setter
    def min_scaling_factor(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c858c34407ec855df9ec322f077ef3119901b78d7da86f4a0d338b4e7954b5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minScalingFactor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocMetastoreServiceScalingConfigAutoscalingConfigLimitConfig]:
        return typing.cast(typing.Optional[DataprocMetastoreServiceScalingConfigAutoscalingConfigLimitConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocMetastoreServiceScalingConfigAutoscalingConfigLimitConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31aad35291ca2d6466e4dce40ecf62b6ea193c98775e93b432702d78cdeab533)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataprocMetastoreServiceScalingConfigAutoscalingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocMetastoreService.DataprocMetastoreServiceScalingConfigAutoscalingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5030fc9913da0cf37476fcd7c4bf6e07c8e4179a7a988c09738818316d37e869)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLimitConfig")
    def put_limit_config(
        self,
        *,
        max_scaling_factor: typing.Optional[jsii.Number] = None,
        min_scaling_factor: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_scaling_factor: The maximum scaling factor that the service will autoscale to. The default value is 6.0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#max_scaling_factor DataprocMetastoreService#max_scaling_factor}
        :param min_scaling_factor: The minimum scaling factor that the service will autoscale to. The default value is 0.1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#min_scaling_factor DataprocMetastoreService#min_scaling_factor}
        '''
        value = DataprocMetastoreServiceScalingConfigAutoscalingConfigLimitConfig(
            max_scaling_factor=max_scaling_factor,
            min_scaling_factor=min_scaling_factor,
        )

        return typing.cast(None, jsii.invoke(self, "putLimitConfig", [value]))

    @jsii.member(jsii_name="resetAutoscalingEnabled")
    def reset_autoscaling_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoscalingEnabled", []))

    @jsii.member(jsii_name="resetLimitConfig")
    def reset_limit_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLimitConfig", []))

    @builtins.property
    @jsii.member(jsii_name="autoscalingFactor")
    def autoscaling_factor(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "autoscalingFactor"))

    @builtins.property
    @jsii.member(jsii_name="limitConfig")
    def limit_config(
        self,
    ) -> DataprocMetastoreServiceScalingConfigAutoscalingConfigLimitConfigOutputReference:
        return typing.cast(DataprocMetastoreServiceScalingConfigAutoscalingConfigLimitConfigOutputReference, jsii.get(self, "limitConfig"))

    @builtins.property
    @jsii.member(jsii_name="autoscalingEnabledInput")
    def autoscaling_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoscalingEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="limitConfigInput")
    def limit_config_input(
        self,
    ) -> typing.Optional[DataprocMetastoreServiceScalingConfigAutoscalingConfigLimitConfig]:
        return typing.cast(typing.Optional[DataprocMetastoreServiceScalingConfigAutoscalingConfigLimitConfig], jsii.get(self, "limitConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="autoscalingEnabled")
    def autoscaling_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoscalingEnabled"))

    @autoscaling_enabled.setter
    def autoscaling_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91671ec1e8c084e475760b0aa7e42259a7b58f64dc45142a3320233637af16a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoscalingEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocMetastoreServiceScalingConfigAutoscalingConfig]:
        return typing.cast(typing.Optional[DataprocMetastoreServiceScalingConfigAutoscalingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocMetastoreServiceScalingConfigAutoscalingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a48042d2cfa04db8a7904902863beae0e20c48cdd48e97023d357de8ca70e64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataprocMetastoreServiceScalingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocMetastoreService.DataprocMetastoreServiceScalingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a90edb527d51d447146b94571aec81668f0caa01db3e950721608aff7860e49)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAutoscalingConfig")
    def put_autoscaling_config(
        self,
        *,
        autoscaling_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        limit_config: typing.Optional[typing.Union[DataprocMetastoreServiceScalingConfigAutoscalingConfigLimitConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param autoscaling_enabled: Defines whether autoscaling is enabled. The default value is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#autoscaling_enabled DataprocMetastoreService#autoscaling_enabled}
        :param limit_config: limit_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#limit_config DataprocMetastoreService#limit_config}
        '''
        value = DataprocMetastoreServiceScalingConfigAutoscalingConfig(
            autoscaling_enabled=autoscaling_enabled, limit_config=limit_config
        )

        return typing.cast(None, jsii.invoke(self, "putAutoscalingConfig", [value]))

    @jsii.member(jsii_name="resetAutoscalingConfig")
    def reset_autoscaling_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoscalingConfig", []))

    @jsii.member(jsii_name="resetInstanceSize")
    def reset_instance_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceSize", []))

    @jsii.member(jsii_name="resetScalingFactor")
    def reset_scaling_factor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScalingFactor", []))

    @builtins.property
    @jsii.member(jsii_name="autoscalingConfig")
    def autoscaling_config(
        self,
    ) -> DataprocMetastoreServiceScalingConfigAutoscalingConfigOutputReference:
        return typing.cast(DataprocMetastoreServiceScalingConfigAutoscalingConfigOutputReference, jsii.get(self, "autoscalingConfig"))

    @builtins.property
    @jsii.member(jsii_name="autoscalingConfigInput")
    def autoscaling_config_input(
        self,
    ) -> typing.Optional[DataprocMetastoreServiceScalingConfigAutoscalingConfig]:
        return typing.cast(typing.Optional[DataprocMetastoreServiceScalingConfigAutoscalingConfig], jsii.get(self, "autoscalingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceSizeInput")
    def instance_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="scalingFactorInput")
    def scaling_factor_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "scalingFactorInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceSize")
    def instance_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceSize"))

    @instance_size.setter
    def instance_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99af9388acb228a682fae930d46ecb58b298340c1352522ac5121a4a144f49d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scalingFactor")
    def scaling_factor(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scalingFactor"))

    @scaling_factor.setter
    def scaling_factor(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__362b513a7fd4e6bb0fd9b8f7e95a8db67a0375548eebd232cd4cc4c1e797e2be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scalingFactor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataprocMetastoreServiceScalingConfig]:
        return typing.cast(typing.Optional[DataprocMetastoreServiceScalingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocMetastoreServiceScalingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d2a59b1baa8cea93f1b2c82b52a6d56406280d151aae57ca88b67429a6b8e19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocMetastoreService.DataprocMetastoreServiceScheduledBackup",
    jsii_struct_bases=[],
    name_mapping={
        "backup_location": "backupLocation",
        "cron_schedule": "cronSchedule",
        "enabled": "enabled",
        "time_zone": "timeZone",
    },
)
class DataprocMetastoreServiceScheduledBackup:
    def __init__(
        self,
        *,
        backup_location: builtins.str,
        cron_schedule: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        time_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param backup_location: A Cloud Storage URI of a folder, in the format gs://<bucket_name>/<path_inside_bucket>. A sub-folder <backup_folder> containing backup files will be stored below it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#backup_location DataprocMetastoreService#backup_location}
        :param cron_schedule: The scheduled interval in Cron format, see https://en.wikipedia.org/wiki/Cron The default is empty: scheduled backup is not enabled. Must be specified to enable scheduled backups. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#cron_schedule DataprocMetastoreService#cron_schedule}
        :param enabled: Defines whether the scheduled backup is enabled. The default value is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#enabled DataprocMetastoreService#enabled}
        :param time_zone: Specifies the time zone to be used when interpreting cronSchedule. Must be a time zone name from the time zone database (https://en.wikipedia.org/wiki/List_of_tz_database_time_zones), e.g. America/Los_Angeles or Africa/Abidjan. If left unspecified, the default is UTC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#time_zone DataprocMetastoreService#time_zone}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30be24ee6f2109c14b5c4358621727f65ef941241cf01aaf1e04600e1a60d271)
            check_type(argname="argument backup_location", value=backup_location, expected_type=type_hints["backup_location"])
            check_type(argname="argument cron_schedule", value=cron_schedule, expected_type=type_hints["cron_schedule"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "backup_location": backup_location,
        }
        if cron_schedule is not None:
            self._values["cron_schedule"] = cron_schedule
        if enabled is not None:
            self._values["enabled"] = enabled
        if time_zone is not None:
            self._values["time_zone"] = time_zone

    @builtins.property
    def backup_location(self) -> builtins.str:
        '''A Cloud Storage URI of a folder, in the format gs://<bucket_name>/<path_inside_bucket>.

        A sub-folder <backup_folder> containing backup files will be stored below it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#backup_location DataprocMetastoreService#backup_location}
        '''
        result = self._values.get("backup_location")
        assert result is not None, "Required property 'backup_location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cron_schedule(self) -> typing.Optional[builtins.str]:
        '''The scheduled interval in Cron format, see https://en.wikipedia.org/wiki/Cron The default is empty: scheduled backup is not enabled. Must be specified to enable scheduled backups.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#cron_schedule DataprocMetastoreService#cron_schedule}
        '''
        result = self._values.get("cron_schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defines whether the scheduled backup is enabled. The default value is false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#enabled DataprocMetastoreService#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def time_zone(self) -> typing.Optional[builtins.str]:
        '''Specifies the time zone to be used when interpreting cronSchedule.

        Must be a time zone name from the time zone database (https://en.wikipedia.org/wiki/List_of_tz_database_time_zones), e.g. America/Los_Angeles or Africa/Abidjan. If left unspecified, the default is UTC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#time_zone DataprocMetastoreService#time_zone}
        '''
        result = self._values.get("time_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocMetastoreServiceScheduledBackup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocMetastoreServiceScheduledBackupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocMetastoreService.DataprocMetastoreServiceScheduledBackupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b93390c9036326d3357b9ad0e1929d5a2533d712c0cddc0c852f95f035ba75eb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCronSchedule")
    def reset_cron_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCronSchedule", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetTimeZone")
    def reset_time_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeZone", []))

    @builtins.property
    @jsii.member(jsii_name="backupLocationInput")
    def backup_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "backupLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="cronScheduleInput")
    def cron_schedule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cronScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZoneInput")
    def time_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="backupLocation")
    def backup_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backupLocation"))

    @backup_location.setter
    def backup_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7b91af692388e662ac63c995cee33fdf0de64625250183d3b858613fb5435a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cronSchedule")
    def cron_schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cronSchedule"))

    @cron_schedule.setter
    def cron_schedule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__310eed8c2486ece570eb1928e2e3ddde0563c586e5f175d8dceceff07d46a7ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cronSchedule", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__571ea9ae485900347cd022eeb7479fff7ca0ee6a9faf4bc35d12fb242ff2acd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4069de1959865adc4922192e73fd65f4a80865c5058b502daae331c3a3b19c4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocMetastoreServiceScheduledBackup]:
        return typing.cast(typing.Optional[DataprocMetastoreServiceScheduledBackup], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocMetastoreServiceScheduledBackup],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c74f971c647d54d0cd189b67aea5a42313879266dee767405d38a8581eef8359)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocMetastoreService.DataprocMetastoreServiceTelemetryConfig",
    jsii_struct_bases=[],
    name_mapping={"log_format": "logFormat"},
)
class DataprocMetastoreServiceTelemetryConfig:
    def __init__(self, *, log_format: typing.Optional[builtins.str] = None) -> None:
        '''
        :param log_format: The output format of the Dataproc Metastore service's logs. Default value: "JSON" Possible values: ["LEGACY", "JSON"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#log_format DataprocMetastoreService#log_format}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a8e19e2f2beb7474a06daf6cf9bd04afeeabdfe15928aae793359a84ddab4b8)
            check_type(argname="argument log_format", value=log_format, expected_type=type_hints["log_format"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if log_format is not None:
            self._values["log_format"] = log_format

    @builtins.property
    def log_format(self) -> typing.Optional[builtins.str]:
        '''The output format of the Dataproc Metastore service's logs. Default value: "JSON" Possible values: ["LEGACY", "JSON"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#log_format DataprocMetastoreService#log_format}
        '''
        result = self._values.get("log_format")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocMetastoreServiceTelemetryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocMetastoreServiceTelemetryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocMetastoreService.DataprocMetastoreServiceTelemetryConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c8c3b83a1dde817c21228813f611142d06a90952ab7ef3df82142c738824905)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLogFormat")
    def reset_log_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogFormat", []))

    @builtins.property
    @jsii.member(jsii_name="logFormatInput")
    def log_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="logFormat")
    def log_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logFormat"))

    @log_format.setter
    def log_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bda1bd531dae4b5e09136537ce006d5665e7eb841346fdcde790052a7d9d1dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocMetastoreServiceTelemetryConfig]:
        return typing.cast(typing.Optional[DataprocMetastoreServiceTelemetryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocMetastoreServiceTelemetryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a006700f5e01c1a145cf596df0752da74615fcb301ec2fb7ce8be24d55bf3b5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocMetastoreService.DataprocMetastoreServiceTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DataprocMetastoreServiceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#create DataprocMetastoreService#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#delete DataprocMetastoreService#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#update DataprocMetastoreService#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9285b472124affce09f75e837f2c52f6593c4be802ce6f385e9e56a8b62c646)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#create DataprocMetastoreService#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#delete DataprocMetastoreService#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_metastore_service#update DataprocMetastoreService#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocMetastoreServiceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocMetastoreServiceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocMetastoreService.DataprocMetastoreServiceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d934fd5a4982d8b91661a4b315bf03af65ceb20587449606d95b45bfc7ba3f8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf922aa497c9cdbefe04bdfd195f53256c8cfe6b0f20cbf1f876c158fda35fd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a576e252395d23403d6b49d3e8fddc7d85081617861135b171c36115984ad296)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc4f8d6e45c9829d146d46ab7666407324eb870dd633b05c0f9cce9b589eadc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocMetastoreServiceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocMetastoreServiceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocMetastoreServiceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__317a5496033bfb2324f0b3c801f15de585974e81bc66cd4dfaef4e03c157efc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataprocMetastoreService",
    "DataprocMetastoreServiceConfig",
    "DataprocMetastoreServiceEncryptionConfig",
    "DataprocMetastoreServiceEncryptionConfigOutputReference",
    "DataprocMetastoreServiceHiveMetastoreConfig",
    "DataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersions",
    "DataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersionsList",
    "DataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersionsOutputReference",
    "DataprocMetastoreServiceHiveMetastoreConfigKerberosConfig",
    "DataprocMetastoreServiceHiveMetastoreConfigKerberosConfigKeytab",
    "DataprocMetastoreServiceHiveMetastoreConfigKerberosConfigKeytabOutputReference",
    "DataprocMetastoreServiceHiveMetastoreConfigKerberosConfigOutputReference",
    "DataprocMetastoreServiceHiveMetastoreConfigOutputReference",
    "DataprocMetastoreServiceMaintenanceWindow",
    "DataprocMetastoreServiceMaintenanceWindowOutputReference",
    "DataprocMetastoreServiceMetadataIntegration",
    "DataprocMetastoreServiceMetadataIntegrationDataCatalogConfig",
    "DataprocMetastoreServiceMetadataIntegrationDataCatalogConfigOutputReference",
    "DataprocMetastoreServiceMetadataIntegrationOutputReference",
    "DataprocMetastoreServiceNetworkConfig",
    "DataprocMetastoreServiceNetworkConfigConsumers",
    "DataprocMetastoreServiceNetworkConfigConsumersList",
    "DataprocMetastoreServiceNetworkConfigConsumersOutputReference",
    "DataprocMetastoreServiceNetworkConfigOutputReference",
    "DataprocMetastoreServiceScalingConfig",
    "DataprocMetastoreServiceScalingConfigAutoscalingConfig",
    "DataprocMetastoreServiceScalingConfigAutoscalingConfigLimitConfig",
    "DataprocMetastoreServiceScalingConfigAutoscalingConfigLimitConfigOutputReference",
    "DataprocMetastoreServiceScalingConfigAutoscalingConfigOutputReference",
    "DataprocMetastoreServiceScalingConfigOutputReference",
    "DataprocMetastoreServiceScheduledBackup",
    "DataprocMetastoreServiceScheduledBackupOutputReference",
    "DataprocMetastoreServiceTelemetryConfig",
    "DataprocMetastoreServiceTelemetryConfigOutputReference",
    "DataprocMetastoreServiceTimeouts",
    "DataprocMetastoreServiceTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__0c6c30b2fa325592281e66943d0efae5eeb701cdb951f4d4700e37d87e84d0dc(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    service_id: builtins.str,
    database_type: typing.Optional[builtins.str] = None,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encryption_config: typing.Optional[typing.Union[DataprocMetastoreServiceEncryptionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    hive_metastore_config: typing.Optional[typing.Union[DataprocMetastoreServiceHiveMetastoreConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    maintenance_window: typing.Optional[typing.Union[DataprocMetastoreServiceMaintenanceWindow, typing.Dict[builtins.str, typing.Any]]] = None,
    metadata_integration: typing.Optional[typing.Union[DataprocMetastoreServiceMetadataIntegration, typing.Dict[builtins.str, typing.Any]]] = None,
    network: typing.Optional[builtins.str] = None,
    network_config: typing.Optional[typing.Union[DataprocMetastoreServiceNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    port: typing.Optional[jsii.Number] = None,
    project: typing.Optional[builtins.str] = None,
    release_channel: typing.Optional[builtins.str] = None,
    scaling_config: typing.Optional[typing.Union[DataprocMetastoreServiceScalingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    scheduled_backup: typing.Optional[typing.Union[DataprocMetastoreServiceScheduledBackup, typing.Dict[builtins.str, typing.Any]]] = None,
    telemetry_config: typing.Optional[typing.Union[DataprocMetastoreServiceTelemetryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    tier: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataprocMetastoreServiceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__711ae53107df0130c2924e2539a842e90e32d7326c8c7196edc518a6a415f216(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56a79e3b07585328bbc438e2c4c548249e166a5035c53d046b346a01ff788260(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b60bf737d4f1abffb5fef22c34fe9ee92ce8e16d81d541619bae083a842c62d1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5eb4c13993b1799f1fdf8b0ba0acae174cfae5fb325e82dfe44dd78ad93055b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__036a99424d82c3e0a86a0965622e7d5e18b5ec36220e5e81525615ceb0110453(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f792684130a2b65c87f46247d89fd3cc81a68cedb61897e1bf7d12d97e30de6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c226d3655e00cfd24e367355ea0009321c36584159b00c6a13779aaeed316c42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__085cd89fe09e0afb8a33f5816fc7d139c79fead911567d3c83b47550d35678aa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26821518ec36a687d2b673f782161fbee1dba726f75aef7774b2b70aba3efc90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b22ecadf46f20a8f6ea11636da2a416026732eb663f5929f5c1c405bd48194e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__365a5a3c4025235aa79721eeaac216401f6bc18ee61c5fb4a1ef18216a26b365(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9a701a373949e892312c24628201e43a9c960d0b9ed5617cd48070fce0ec70e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01caaf7ef1f994e7ed6c5f31e31d0acda26cbf540bc791d39bf49116046fa9a1(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_id: builtins.str,
    database_type: typing.Optional[builtins.str] = None,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encryption_config: typing.Optional[typing.Union[DataprocMetastoreServiceEncryptionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    hive_metastore_config: typing.Optional[typing.Union[DataprocMetastoreServiceHiveMetastoreConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    maintenance_window: typing.Optional[typing.Union[DataprocMetastoreServiceMaintenanceWindow, typing.Dict[builtins.str, typing.Any]]] = None,
    metadata_integration: typing.Optional[typing.Union[DataprocMetastoreServiceMetadataIntegration, typing.Dict[builtins.str, typing.Any]]] = None,
    network: typing.Optional[builtins.str] = None,
    network_config: typing.Optional[typing.Union[DataprocMetastoreServiceNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    port: typing.Optional[jsii.Number] = None,
    project: typing.Optional[builtins.str] = None,
    release_channel: typing.Optional[builtins.str] = None,
    scaling_config: typing.Optional[typing.Union[DataprocMetastoreServiceScalingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    scheduled_backup: typing.Optional[typing.Union[DataprocMetastoreServiceScheduledBackup, typing.Dict[builtins.str, typing.Any]]] = None,
    telemetry_config: typing.Optional[typing.Union[DataprocMetastoreServiceTelemetryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    tier: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataprocMetastoreServiceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d336eab06ad120c0fb7be7f82d516a8d670f81cd7afcfabfd9400962df3a3c2(
    *,
    kms_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be097f849d309ea8f78b601c1ee0e72513528e06937f66d902925fa8ced7b410(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0edb0bede55de9d86f482dd2e04580e6a3bd131c94e9fd58f96e6024cb7cf79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eae6cd602572895e0663edb8350d5004da1e725ef48af79d28fc7ff901cc313(
    value: typing.Optional[DataprocMetastoreServiceEncryptionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e1b0242e6cc7888aa52d62efd9615db1a9417c9b095a978a585d563d6d762d3(
    *,
    version: builtins.str,
    auxiliary_versions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    config_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    endpoint_protocol: typing.Optional[builtins.str] = None,
    kerberos_config: typing.Optional[typing.Union[DataprocMetastoreServiceHiveMetastoreConfigKerberosConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67ab7f8c4561dce41958922f1ef0440ea4c27dd07f315aa85014cd2f6dc0e53d(
    *,
    key: builtins.str,
    version: builtins.str,
    config_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4da1f66e5237a2338d58f403ce7ed8787328890cf92e9526d574225ff281cb3f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69837f975a040667b3231e3c9b5dd86cecba3f2de772aeab18394c9c26544fe3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__412fcdbf7f1710c7fbdf38ca49f524d83af11688a43fba85c630e40631241ecd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f620570b31d600f6192a6415b389103daa45f12a72513a9142c3053a7f149786(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7fef756029ac0c7ad78fbfff9fe2ef9d4eea958a0fc6b9ef2bcc9f3c77c5064(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__436dac4b0405692ed009fc6c1912c666bd8369dd218845b274cd5cd8174bfc60(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3a8385105940b361717080bb2953abc381ef771116017b24fe16353be821e5a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89e318ba4c8f75e42e397367f91110926ce5e2cfd036d44e79654dcdbb44a711(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be41f8c823fd602eea5afd24b0bc24647fe434c0624604a78e4a51c1445261d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c3081559186163b3dff1a1e86bcd4bad8b00381391975d6addca7fd9d6090cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3406b03c1b6e042807ae80755a3a3b61dfa3874a31abef9fcddd359f334eca0c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01f68992e7773d044fce5127bf11fd231005f8f878036aabbc99912776caf743(
    *,
    keytab: typing.Union[DataprocMetastoreServiceHiveMetastoreConfigKerberosConfigKeytab, typing.Dict[builtins.str, typing.Any]],
    krb5_config_gcs_uri: builtins.str,
    principal: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba58ab8776add2656543da21fee71a9429b74a88fee210a8ae9f6f7c881c58bb(
    *,
    cloud_secret: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a78d50dc12776cdc206c393d08beb7adc0f661703f05a4ab185b45d037605c6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87af15ec001985bbde22095ce133ded406e993dd991bd937d25bed3d6deac4c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbd1a37ed2c50599966877eabadb494f8b0cae934726ee0952975fced7db2e68(
    value: typing.Optional[DataprocMetastoreServiceHiveMetastoreConfigKerberosConfigKeytab],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b2ed886bfdeca65edaca9f037ac172f81611e7fab8d1a1e2f8cb9a18f1bf95a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67154394df902fd2bc8291c60f6fe1a2fe8250137e66547e5f2adf3100f2b4c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7861945876207533fb0d30c090d7de627a0a40c76c0f9d7161c2c3c8ca7b9323(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__273372d176acc28db5c1b5a68a9614eef41f039a36f4b758aa4340762c718f4e(
    value: typing.Optional[DataprocMetastoreServiceHiveMetastoreConfigKerberosConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1e446c286735a1665fc8ed7e1f111a74e8010807d34b3561219fc5f2609f6d5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6018107f80d6a457f8551b25a8f37c6479730fefbc8111cad3f3f0d8608ce7ed(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76250e088fc3f8f5fafa73b6c241fd7f5a04591cec4488e4dadc544d2df21f18(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb41b31425a78dd42854112e95411776768b22e62820f44d5e01568dc50bd940(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61529528962844ed4224eb84be8a712f6e99649e2d00c38a6ed4c6735b59ea56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dbc76bde9c1759d3c56d4b1d0e42cf2091a98263485c994136e94ca58a7ae05(
    value: typing.Optional[DataprocMetastoreServiceHiveMetastoreConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37c544e5fde22a515907b412d11472d793008ae89880d48cdb98e1a6ce066ced(
    *,
    day_of_week: builtins.str,
    hour_of_day: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d171bbc78de196dc060f85e1cad82085e5373e0a8827c96febd4a1efc1cd090(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__603051864a6dd185e33c74f4e2e554fb023a6e1243e1cc82f053c3d8d3124469(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__263627d5caa87b46db5a99a1e0add63e3f200228a2a79ed757b230ac126b090a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__517b85764561e09db3bf91b07eb19d9342cd96bc20631eb69d65354cbfc584ee(
    value: typing.Optional[DataprocMetastoreServiceMaintenanceWindow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__944a1616f4c9de07a7370cbf2b92d899266f66fbc41442b1a17754a204f17310(
    *,
    data_catalog_config: typing.Union[DataprocMetastoreServiceMetadataIntegrationDataCatalogConfig, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__645ad1901e7fe0baf1f9cb74274228e829268a353a519abe757c0d7a12f96786(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97d7e4bda7ecc45c27793366e2c707aae62bd24575fa77e59add1d4ce8c77379(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e7219c02f0dc0ba5793cb9cf1a646d43c161cc460ac6ef27d37bf9393a4ca45(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c98ee2ad30e6ea8bc3caa62ad20e6918f18f87c497fb4299ceeca8d513c1ff38(
    value: typing.Optional[DataprocMetastoreServiceMetadataIntegrationDataCatalogConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3caf0afe4817838290b19d8fc54626ff5d168ceb5040bffd52956b2a8d29049(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a11b9cc0aa729e3cecdd070356411d8ce9fa80b0f4191b0ada4c5bd2a2747a7b(
    value: typing.Optional[DataprocMetastoreServiceMetadataIntegration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35ec65f5d9d0fad4d8c7434d85c8ad05c1c8af765624d1cba1ba5c7c9251d92f(
    *,
    consumers: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataprocMetastoreServiceNetworkConfigConsumers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5c7b785655c488a57bc98d4a8ce258382c67f949e6d590edb936d1ee3650f4e(
    *,
    subnetwork: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c43dada6af8841b1cf431898ab976146bfdb624dca47684aa3feb3d3f868f032(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27f670900a9f60e43bc4967c79cafd253eb214bfd24f289be7b22ddd7dcbd5a1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abfaeb86eb373a9d53ba643a2999090dbf04074bdec9d8ee96e2fe5d218b1719(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b9a54d131623e87b65739c7c4775bac6c4eb39305f9a59dd05084edc4e572d2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ab4ba6c4250d441859c6cf7a0a48e8e09b31587bc61846a931fb6b97ab314c6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2032d6986f313eb4cdc93baf2cae22e6efac7d978817cb65799074b05152afbe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocMetastoreServiceNetworkConfigConsumers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2c64386a63a9acf36c7cd080b9bac3a84750c5da3958a3f4b6ab4d2353e4ad0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__194988a679b4f55240396e08eba64fd86ad22931ccd852b9d9e143d6527b443d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__300418f8347dc08a1751db46603645575a0c1c683e958058ebec49be570ef394(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocMetastoreServiceNetworkConfigConsumers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eb2eb4c4fe5c5ce85553a673db61896dfc0b220e45ac826a23d6eea48ff5d94(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bc55508cd865831a4c905ef02e146b6404e9b4a0b66f127ac68e87c80424535(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataprocMetastoreServiceNetworkConfigConsumers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__852c6101e2cd2ff20c35b013d4fc303b7aeccbd973935b52c3918d23918b2df0(
    value: typing.Optional[DataprocMetastoreServiceNetworkConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43710df38faebed6fcc8600dc5c389c030636f1c4575943d5e040d4fbd165a95(
    *,
    autoscaling_config: typing.Optional[typing.Union[DataprocMetastoreServiceScalingConfigAutoscalingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    instance_size: typing.Optional[builtins.str] = None,
    scaling_factor: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e9a36c69cd450e230eeebdbe6583bb1077f42bdb4f01bd9955bad510c802581(
    *,
    autoscaling_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    limit_config: typing.Optional[typing.Union[DataprocMetastoreServiceScalingConfigAutoscalingConfigLimitConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9137a36d4c570d9984a8f69ebae4862c8147d83cb181c69dd00c7a9621dfaf54(
    *,
    max_scaling_factor: typing.Optional[jsii.Number] = None,
    min_scaling_factor: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea61e385aa867aaef1fbb55bdfc05cf0eb2f365e65d0980161df7af0e98f26d9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8704c63db4fc9aa14874703cba1fd15126b8eef875e0ae99f973298064232266(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c858c34407ec855df9ec322f077ef3119901b78d7da86f4a0d338b4e7954b5a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31aad35291ca2d6466e4dce40ecf62b6ea193c98775e93b432702d78cdeab533(
    value: typing.Optional[DataprocMetastoreServiceScalingConfigAutoscalingConfigLimitConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5030fc9913da0cf37476fcd7c4bf6e07c8e4179a7a988c09738818316d37e869(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91671ec1e8c084e475760b0aa7e42259a7b58f64dc45142a3320233637af16a1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a48042d2cfa04db8a7904902863beae0e20c48cdd48e97023d357de8ca70e64(
    value: typing.Optional[DataprocMetastoreServiceScalingConfigAutoscalingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a90edb527d51d447146b94571aec81668f0caa01db3e950721608aff7860e49(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99af9388acb228a682fae930d46ecb58b298340c1352522ac5121a4a144f49d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__362b513a7fd4e6bb0fd9b8f7e95a8db67a0375548eebd232cd4cc4c1e797e2be(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d2a59b1baa8cea93f1b2c82b52a6d56406280d151aae57ca88b67429a6b8e19(
    value: typing.Optional[DataprocMetastoreServiceScalingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30be24ee6f2109c14b5c4358621727f65ef941241cf01aaf1e04600e1a60d271(
    *,
    backup_location: builtins.str,
    cron_schedule: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    time_zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b93390c9036326d3357b9ad0e1929d5a2533d712c0cddc0c852f95f035ba75eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7b91af692388e662ac63c995cee33fdf0de64625250183d3b858613fb5435a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__310eed8c2486ece570eb1928e2e3ddde0563c586e5f175d8dceceff07d46a7ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__571ea9ae485900347cd022eeb7479fff7ca0ee6a9faf4bc35d12fb242ff2acd5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4069de1959865adc4922192e73fd65f4a80865c5058b502daae331c3a3b19c4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c74f971c647d54d0cd189b67aea5a42313879266dee767405d38a8581eef8359(
    value: typing.Optional[DataprocMetastoreServiceScheduledBackup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a8e19e2f2beb7474a06daf6cf9bd04afeeabdfe15928aae793359a84ddab4b8(
    *,
    log_format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c8c3b83a1dde817c21228813f611142d06a90952ab7ef3df82142c738824905(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bda1bd531dae4b5e09136537ce006d5665e7eb841346fdcde790052a7d9d1dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a006700f5e01c1a145cf596df0752da74615fcb301ec2fb7ce8be24d55bf3b5a(
    value: typing.Optional[DataprocMetastoreServiceTelemetryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9285b472124affce09f75e837f2c52f6593c4be802ce6f385e9e56a8b62c646(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d934fd5a4982d8b91661a4b315bf03af65ceb20587449606d95b45bfc7ba3f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf922aa497c9cdbefe04bdfd195f53256c8cfe6b0f20cbf1f876c158fda35fd4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a576e252395d23403d6b49d3e8fddc7d85081617861135b171c36115984ad296(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc4f8d6e45c9829d146d46ab7666407324eb870dd633b05c0f9cce9b589eadc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__317a5496033bfb2324f0b3c801f15de585974e81bc66cd4dfaef4e03c157efc0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocMetastoreServiceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
