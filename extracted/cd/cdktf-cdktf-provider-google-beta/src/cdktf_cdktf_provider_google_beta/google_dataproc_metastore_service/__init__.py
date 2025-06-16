r'''
# `google_dataproc_metastore_service`

Refer to the Terraform Registry for docs: [`google_dataproc_metastore_service`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service).
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


class GoogleDataprocMetastoreService(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocMetastoreService.GoogleDataprocMetastoreService",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service google_dataproc_metastore_service}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        service_id: builtins.str,
        database_type: typing.Optional[builtins.str] = None,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_config: typing.Optional[typing.Union["GoogleDataprocMetastoreServiceEncryptionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        hive_metastore_config: typing.Optional[typing.Union["GoogleDataprocMetastoreServiceHiveMetastoreConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        maintenance_window: typing.Optional[typing.Union["GoogleDataprocMetastoreServiceMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]] = None,
        metadata_integration: typing.Optional[typing.Union["GoogleDataprocMetastoreServiceMetadataIntegration", typing.Dict[builtins.str, typing.Any]]] = None,
        network: typing.Optional[builtins.str] = None,
        network_config: typing.Optional[typing.Union["GoogleDataprocMetastoreServiceNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        port: typing.Optional[jsii.Number] = None,
        project: typing.Optional[builtins.str] = None,
        release_channel: typing.Optional[builtins.str] = None,
        scaling_config: typing.Optional[typing.Union["GoogleDataprocMetastoreServiceScalingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        scheduled_backup: typing.Optional[typing.Union["GoogleDataprocMetastoreServiceScheduledBackup", typing.Dict[builtins.str, typing.Any]]] = None,
        telemetry_config: typing.Optional[typing.Union["GoogleDataprocMetastoreServiceTelemetryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tier: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDataprocMetastoreServiceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service google_dataproc_metastore_service} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param service_id: The ID of the metastore service. The id must contain only letters (a-z, A-Z), numbers (0-9), underscores (_), and hyphens (-). Cannot begin or end with underscore or hyphen. Must consist of between 3 and 63 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#service_id GoogleDataprocMetastoreService#service_id}
        :param database_type: The database type that the Metastore service stores its data. Default value: "MYSQL" Possible values: ["MYSQL", "SPANNER"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#database_type GoogleDataprocMetastoreService#database_type}
        :param deletion_protection: Indicates if the dataproc metastore should be protected against accidental deletions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#deletion_protection GoogleDataprocMetastoreService#deletion_protection}
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#encryption_config GoogleDataprocMetastoreService#encryption_config}
        :param hive_metastore_config: hive_metastore_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#hive_metastore_config GoogleDataprocMetastoreService#hive_metastore_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#id GoogleDataprocMetastoreService#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: User-defined labels for the metastore service. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#labels GoogleDataprocMetastoreService#labels}
        :param location: The location where the metastore service should reside. The default value is 'global'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#location GoogleDataprocMetastoreService#location}
        :param maintenance_window: maintenance_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#maintenance_window GoogleDataprocMetastoreService#maintenance_window}
        :param metadata_integration: metadata_integration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#metadata_integration GoogleDataprocMetastoreService#metadata_integration}
        :param network: The relative resource name of the VPC network on which the instance can be accessed. It is specified in the following form: "projects/{projectNumber}/global/networks/{network_id}". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#network GoogleDataprocMetastoreService#network}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#network_config GoogleDataprocMetastoreService#network_config}
        :param port: The TCP port at which the metastore service is reached. Default: 9083. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#port GoogleDataprocMetastoreService#port}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#project GoogleDataprocMetastoreService#project}.
        :param release_channel: The release channel of the service. If unspecified, defaults to 'STABLE'. Default value: "STABLE" Possible values: ["CANARY", "STABLE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#release_channel GoogleDataprocMetastoreService#release_channel}
        :param scaling_config: scaling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#scaling_config GoogleDataprocMetastoreService#scaling_config}
        :param scheduled_backup: scheduled_backup block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#scheduled_backup GoogleDataprocMetastoreService#scheduled_backup}
        :param telemetry_config: telemetry_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#telemetry_config GoogleDataprocMetastoreService#telemetry_config}
        :param tier: The tier of the service. Possible values: ["DEVELOPER", "ENTERPRISE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#tier GoogleDataprocMetastoreService#tier}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#timeouts GoogleDataprocMetastoreService#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9cf4bc6d38963afb60304c9411f5694a66e81db8e88c3f76d5caec80a3a1a89)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleDataprocMetastoreServiceConfig(
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
        '''Generates CDKTF code for importing a GoogleDataprocMetastoreService resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleDataprocMetastoreService to import.
        :param import_from_id: The id of the existing GoogleDataprocMetastoreService that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleDataprocMetastoreService to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd9e3592af3e1d660bc3690fb3a77ea2fd83ab59864b45a8e25f5d5ec94a416e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEncryptionConfig")
    def put_encryption_config(self, *, kms_key: builtins.str) -> None:
        '''
        :param kms_key: The fully qualified customer provided Cloud KMS key name to use for customer data encryption. Use the following format: 'projects/([^/]+)/locations/([^/]+)/keyRings/([^/]+)/cryptoKeys/([^/]+)'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#kms_key GoogleDataprocMetastoreService#kms_key}
        '''
        value = GoogleDataprocMetastoreServiceEncryptionConfig(kms_key=kms_key)

        return typing.cast(None, jsii.invoke(self, "putEncryptionConfig", [value]))

    @jsii.member(jsii_name="putHiveMetastoreConfig")
    def put_hive_metastore_config(
        self,
        *,
        version: builtins.str,
        auxiliary_versions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        config_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        endpoint_protocol: typing.Optional[builtins.str] = None,
        kerberos_config: typing.Optional[typing.Union["GoogleDataprocMetastoreServiceHiveMetastoreConfigKerberosConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param version: The Hive metastore schema version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#version GoogleDataprocMetastoreService#version}
        :param auxiliary_versions: auxiliary_versions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#auxiliary_versions GoogleDataprocMetastoreService#auxiliary_versions}
        :param config_overrides: A mapping of Hive metastore configuration key-value pairs to apply to the Hive metastore (configured in hive-site.xml). The mappings override system defaults (some keys cannot be overridden). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#config_overrides GoogleDataprocMetastoreService#config_overrides}
        :param endpoint_protocol: The protocol to use for the metastore service endpoint. If unspecified, defaults to 'THRIFT'. Default value: "THRIFT" Possible values: ["THRIFT", "GRPC"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#endpoint_protocol GoogleDataprocMetastoreService#endpoint_protocol}
        :param kerberos_config: kerberos_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#kerberos_config GoogleDataprocMetastoreService#kerberos_config}
        '''
        value = GoogleDataprocMetastoreServiceHiveMetastoreConfig(
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
        :param day_of_week: The day of week, when the window starts. Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#day_of_week GoogleDataprocMetastoreService#day_of_week}
        :param hour_of_day: The hour of day (0-23) when the window starts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#hour_of_day GoogleDataprocMetastoreService#hour_of_day}
        '''
        value = GoogleDataprocMetastoreServiceMaintenanceWindow(
            day_of_week=day_of_week, hour_of_day=hour_of_day
        )

        return typing.cast(None, jsii.invoke(self, "putMaintenanceWindow", [value]))

    @jsii.member(jsii_name="putMetadataIntegration")
    def put_metadata_integration(
        self,
        *,
        data_catalog_config: typing.Union["GoogleDataprocMetastoreServiceMetadataIntegrationDataCatalogConfig", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param data_catalog_config: data_catalog_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#data_catalog_config GoogleDataprocMetastoreService#data_catalog_config}
        '''
        value = GoogleDataprocMetastoreServiceMetadataIntegration(
            data_catalog_config=data_catalog_config
        )

        return typing.cast(None, jsii.invoke(self, "putMetadataIntegration", [value]))

    @jsii.member(jsii_name="putNetworkConfig")
    def put_network_config(
        self,
        *,
        consumers: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataprocMetastoreServiceNetworkConfigConsumers", typing.Dict[builtins.str, typing.Any]]]],
        custom_routes_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param consumers: consumers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#consumers GoogleDataprocMetastoreService#consumers}
        :param custom_routes_enabled: Enables custom routes to be imported and exported for the Dataproc Metastore service's peered VPC network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#custom_routes_enabled GoogleDataprocMetastoreService#custom_routes_enabled}
        '''
        value = GoogleDataprocMetastoreServiceNetworkConfig(
            consumers=consumers, custom_routes_enabled=custom_routes_enabled
        )

        return typing.cast(None, jsii.invoke(self, "putNetworkConfig", [value]))

    @jsii.member(jsii_name="putScalingConfig")
    def put_scaling_config(
        self,
        *,
        autoscaling_config: typing.Optional[typing.Union["GoogleDataprocMetastoreServiceScalingConfigAutoscalingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        instance_size: typing.Optional[builtins.str] = None,
        scaling_factor: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param autoscaling_config: autoscaling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#autoscaling_config GoogleDataprocMetastoreService#autoscaling_config}
        :param instance_size: Metastore instance sizes. Possible values: ["EXTRA_SMALL", "SMALL", "MEDIUM", "LARGE", "EXTRA_LARGE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#instance_size GoogleDataprocMetastoreService#instance_size}
        :param scaling_factor: Scaling factor, in increments of 0.1 for values less than 1.0, and increments of 1.0 for values greater than 1.0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#scaling_factor GoogleDataprocMetastoreService#scaling_factor}
        '''
        value = GoogleDataprocMetastoreServiceScalingConfig(
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
        :param backup_location: A Cloud Storage URI of a folder, in the format gs://<bucket_name>/<path_inside_bucket>. A sub-folder <backup_folder> containing backup files will be stored below it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#backup_location GoogleDataprocMetastoreService#backup_location}
        :param cron_schedule: The scheduled interval in Cron format, see https://en.wikipedia.org/wiki/Cron The default is empty: scheduled backup is not enabled. Must be specified to enable scheduled backups. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#cron_schedule GoogleDataprocMetastoreService#cron_schedule}
        :param enabled: Defines whether the scheduled backup is enabled. The default value is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#enabled GoogleDataprocMetastoreService#enabled}
        :param time_zone: Specifies the time zone to be used when interpreting cronSchedule. Must be a time zone name from the time zone database (https://en.wikipedia.org/wiki/List_of_tz_database_time_zones), e.g. America/Los_Angeles or Africa/Abidjan. If left unspecified, the default is UTC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#time_zone GoogleDataprocMetastoreService#time_zone}
        '''
        value = GoogleDataprocMetastoreServiceScheduledBackup(
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
        :param log_format: The output format of the Dataproc Metastore service's logs. Default value: "JSON" Possible values: ["LEGACY", "JSON"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#log_format GoogleDataprocMetastoreService#log_format}
        '''
        value = GoogleDataprocMetastoreServiceTelemetryConfig(log_format=log_format)

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#create GoogleDataprocMetastoreService#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#delete GoogleDataprocMetastoreService#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#update GoogleDataprocMetastoreService#update}.
        '''
        value = GoogleDataprocMetastoreServiceTimeouts(
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
    ) -> "GoogleDataprocMetastoreServiceEncryptionConfigOutputReference":
        return typing.cast("GoogleDataprocMetastoreServiceEncryptionConfigOutputReference", jsii.get(self, "encryptionConfig"))

    @builtins.property
    @jsii.member(jsii_name="endpointUri")
    def endpoint_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpointUri"))

    @builtins.property
    @jsii.member(jsii_name="hiveMetastoreConfig")
    def hive_metastore_config(
        self,
    ) -> "GoogleDataprocMetastoreServiceHiveMetastoreConfigOutputReference":
        return typing.cast("GoogleDataprocMetastoreServiceHiveMetastoreConfigOutputReference", jsii.get(self, "hiveMetastoreConfig"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindow")
    def maintenance_window(
        self,
    ) -> "GoogleDataprocMetastoreServiceMaintenanceWindowOutputReference":
        return typing.cast("GoogleDataprocMetastoreServiceMaintenanceWindowOutputReference", jsii.get(self, "maintenanceWindow"))

    @builtins.property
    @jsii.member(jsii_name="metadataIntegration")
    def metadata_integration(
        self,
    ) -> "GoogleDataprocMetastoreServiceMetadataIntegrationOutputReference":
        return typing.cast("GoogleDataprocMetastoreServiceMetadataIntegrationOutputReference", jsii.get(self, "metadataIntegration"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="networkConfig")
    def network_config(
        self,
    ) -> "GoogleDataprocMetastoreServiceNetworkConfigOutputReference":
        return typing.cast("GoogleDataprocMetastoreServiceNetworkConfigOutputReference", jsii.get(self, "networkConfig"))

    @builtins.property
    @jsii.member(jsii_name="scalingConfig")
    def scaling_config(
        self,
    ) -> "GoogleDataprocMetastoreServiceScalingConfigOutputReference":
        return typing.cast("GoogleDataprocMetastoreServiceScalingConfigOutputReference", jsii.get(self, "scalingConfig"))

    @builtins.property
    @jsii.member(jsii_name="scheduledBackup")
    def scheduled_backup(
        self,
    ) -> "GoogleDataprocMetastoreServiceScheduledBackupOutputReference":
        return typing.cast("GoogleDataprocMetastoreServiceScheduledBackupOutputReference", jsii.get(self, "scheduledBackup"))

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
    ) -> "GoogleDataprocMetastoreServiceTelemetryConfigOutputReference":
        return typing.cast("GoogleDataprocMetastoreServiceTelemetryConfigOutputReference", jsii.get(self, "telemetryConfig"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleDataprocMetastoreServiceTimeoutsOutputReference":
        return typing.cast("GoogleDataprocMetastoreServiceTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["GoogleDataprocMetastoreServiceEncryptionConfig"]:
        return typing.cast(typing.Optional["GoogleDataprocMetastoreServiceEncryptionConfig"], jsii.get(self, "encryptionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="hiveMetastoreConfigInput")
    def hive_metastore_config_input(
        self,
    ) -> typing.Optional["GoogleDataprocMetastoreServiceHiveMetastoreConfig"]:
        return typing.cast(typing.Optional["GoogleDataprocMetastoreServiceHiveMetastoreConfig"], jsii.get(self, "hiveMetastoreConfigInput"))

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
    ) -> typing.Optional["GoogleDataprocMetastoreServiceMaintenanceWindow"]:
        return typing.cast(typing.Optional["GoogleDataprocMetastoreServiceMaintenanceWindow"], jsii.get(self, "maintenanceWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataIntegrationInput")
    def metadata_integration_input(
        self,
    ) -> typing.Optional["GoogleDataprocMetastoreServiceMetadataIntegration"]:
        return typing.cast(typing.Optional["GoogleDataprocMetastoreServiceMetadataIntegration"], jsii.get(self, "metadataIntegrationInput"))

    @builtins.property
    @jsii.member(jsii_name="networkConfigInput")
    def network_config_input(
        self,
    ) -> typing.Optional["GoogleDataprocMetastoreServiceNetworkConfig"]:
        return typing.cast(typing.Optional["GoogleDataprocMetastoreServiceNetworkConfig"], jsii.get(self, "networkConfigInput"))

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
    ) -> typing.Optional["GoogleDataprocMetastoreServiceScalingConfig"]:
        return typing.cast(typing.Optional["GoogleDataprocMetastoreServiceScalingConfig"], jsii.get(self, "scalingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduledBackupInput")
    def scheduled_backup_input(
        self,
    ) -> typing.Optional["GoogleDataprocMetastoreServiceScheduledBackup"]:
        return typing.cast(typing.Optional["GoogleDataprocMetastoreServiceScheduledBackup"], jsii.get(self, "scheduledBackupInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceIdInput")
    def service_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="telemetryConfigInput")
    def telemetry_config_input(
        self,
    ) -> typing.Optional["GoogleDataprocMetastoreServiceTelemetryConfig"]:
        return typing.cast(typing.Optional["GoogleDataprocMetastoreServiceTelemetryConfig"], jsii.get(self, "telemetryConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="tierInput")
    def tier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tierInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDataprocMetastoreServiceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDataprocMetastoreServiceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseType")
    def database_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseType"))

    @database_type.setter
    def database_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e55f4275643f970cb8a7a565cac8e3eb498f0289720fd59922e02a67c6f2398e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d58b4bdbfb01aeff98fc888a191ba07d59640fd1a7adf17d6e1b80d4335a7882)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionProtection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b93a6154de450b9fb1aab719f682e037cfe1b2e4f02824bf948a01cdc37f92e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc6ae48d1d4be72a989a6d725a02cfc7099caa38ce7a1b63130752f4e9aa214d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52bcca49e1a4d94704efa4c01b6d36f8e83b18177480fa7cd8a6dc58d9892932)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04c4f53d3d9e938e1d51f2ad32302dfa47f83f4b3d3ba4c64ab3f28599cdae85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae736363f85d332443370768686f30149344c80dc9aff3d329240dab5b635dbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4b72d9a8289133cc75fb6d529115cac7a8a30227b1422013dbfcdc043d1bfc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="releaseChannel")
    def release_channel(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "releaseChannel"))

    @release_channel.setter
    def release_channel(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4b7673c4d02349c2078dabd1106e674efbb651238290cf7d3be3909f7c4ff29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "releaseChannel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceId")
    def service_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceId"))

    @service_id.setter
    def service_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08f824fce2eda36205851a26081e3c8edbce6d19c42f6477ab8cae76d7e66136)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tier")
    def tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tier"))

    @tier.setter
    def tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e763de31a4578f796d9a9ac0a62ae992b7a0ee9a5e7599813f7a05a4c76f1a93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tier", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocMetastoreService.GoogleDataprocMetastoreServiceConfig",
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
class GoogleDataprocMetastoreServiceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        encryption_config: typing.Optional[typing.Union["GoogleDataprocMetastoreServiceEncryptionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        hive_metastore_config: typing.Optional[typing.Union["GoogleDataprocMetastoreServiceHiveMetastoreConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        maintenance_window: typing.Optional[typing.Union["GoogleDataprocMetastoreServiceMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]] = None,
        metadata_integration: typing.Optional[typing.Union["GoogleDataprocMetastoreServiceMetadataIntegration", typing.Dict[builtins.str, typing.Any]]] = None,
        network: typing.Optional[builtins.str] = None,
        network_config: typing.Optional[typing.Union["GoogleDataprocMetastoreServiceNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        port: typing.Optional[jsii.Number] = None,
        project: typing.Optional[builtins.str] = None,
        release_channel: typing.Optional[builtins.str] = None,
        scaling_config: typing.Optional[typing.Union["GoogleDataprocMetastoreServiceScalingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        scheduled_backup: typing.Optional[typing.Union["GoogleDataprocMetastoreServiceScheduledBackup", typing.Dict[builtins.str, typing.Any]]] = None,
        telemetry_config: typing.Optional[typing.Union["GoogleDataprocMetastoreServiceTelemetryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tier: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDataprocMetastoreServiceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param service_id: The ID of the metastore service. The id must contain only letters (a-z, A-Z), numbers (0-9), underscores (_), and hyphens (-). Cannot begin or end with underscore or hyphen. Must consist of between 3 and 63 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#service_id GoogleDataprocMetastoreService#service_id}
        :param database_type: The database type that the Metastore service stores its data. Default value: "MYSQL" Possible values: ["MYSQL", "SPANNER"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#database_type GoogleDataprocMetastoreService#database_type}
        :param deletion_protection: Indicates if the dataproc metastore should be protected against accidental deletions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#deletion_protection GoogleDataprocMetastoreService#deletion_protection}
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#encryption_config GoogleDataprocMetastoreService#encryption_config}
        :param hive_metastore_config: hive_metastore_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#hive_metastore_config GoogleDataprocMetastoreService#hive_metastore_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#id GoogleDataprocMetastoreService#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: User-defined labels for the metastore service. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#labels GoogleDataprocMetastoreService#labels}
        :param location: The location where the metastore service should reside. The default value is 'global'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#location GoogleDataprocMetastoreService#location}
        :param maintenance_window: maintenance_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#maintenance_window GoogleDataprocMetastoreService#maintenance_window}
        :param metadata_integration: metadata_integration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#metadata_integration GoogleDataprocMetastoreService#metadata_integration}
        :param network: The relative resource name of the VPC network on which the instance can be accessed. It is specified in the following form: "projects/{projectNumber}/global/networks/{network_id}". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#network GoogleDataprocMetastoreService#network}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#network_config GoogleDataprocMetastoreService#network_config}
        :param port: The TCP port at which the metastore service is reached. Default: 9083. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#port GoogleDataprocMetastoreService#port}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#project GoogleDataprocMetastoreService#project}.
        :param release_channel: The release channel of the service. If unspecified, defaults to 'STABLE'. Default value: "STABLE" Possible values: ["CANARY", "STABLE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#release_channel GoogleDataprocMetastoreService#release_channel}
        :param scaling_config: scaling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#scaling_config GoogleDataprocMetastoreService#scaling_config}
        :param scheduled_backup: scheduled_backup block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#scheduled_backup GoogleDataprocMetastoreService#scheduled_backup}
        :param telemetry_config: telemetry_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#telemetry_config GoogleDataprocMetastoreService#telemetry_config}
        :param tier: The tier of the service. Possible values: ["DEVELOPER", "ENTERPRISE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#tier GoogleDataprocMetastoreService#tier}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#timeouts GoogleDataprocMetastoreService#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(encryption_config, dict):
            encryption_config = GoogleDataprocMetastoreServiceEncryptionConfig(**encryption_config)
        if isinstance(hive_metastore_config, dict):
            hive_metastore_config = GoogleDataprocMetastoreServiceHiveMetastoreConfig(**hive_metastore_config)
        if isinstance(maintenance_window, dict):
            maintenance_window = GoogleDataprocMetastoreServiceMaintenanceWindow(**maintenance_window)
        if isinstance(metadata_integration, dict):
            metadata_integration = GoogleDataprocMetastoreServiceMetadataIntegration(**metadata_integration)
        if isinstance(network_config, dict):
            network_config = GoogleDataprocMetastoreServiceNetworkConfig(**network_config)
        if isinstance(scaling_config, dict):
            scaling_config = GoogleDataprocMetastoreServiceScalingConfig(**scaling_config)
        if isinstance(scheduled_backup, dict):
            scheduled_backup = GoogleDataprocMetastoreServiceScheduledBackup(**scheduled_backup)
        if isinstance(telemetry_config, dict):
            telemetry_config = GoogleDataprocMetastoreServiceTelemetryConfig(**telemetry_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleDataprocMetastoreServiceTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f20cd5f9c16ba80af87f3c149ea683291ef09ac55c6b06ab8dc3b929477ec256)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#service_id GoogleDataprocMetastoreService#service_id}
        '''
        result = self._values.get("service_id")
        assert result is not None, "Required property 'service_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def database_type(self) -> typing.Optional[builtins.str]:
        '''The database type that the Metastore service stores its data. Default value: "MYSQL" Possible values: ["MYSQL", "SPANNER"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#database_type GoogleDataprocMetastoreService#database_type}
        '''
        result = self._values.get("database_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deletion_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates if the dataproc metastore should be protected against accidental deletions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#deletion_protection GoogleDataprocMetastoreService#deletion_protection}
        '''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encryption_config(
        self,
    ) -> typing.Optional["GoogleDataprocMetastoreServiceEncryptionConfig"]:
        '''encryption_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#encryption_config GoogleDataprocMetastoreService#encryption_config}
        '''
        result = self._values.get("encryption_config")
        return typing.cast(typing.Optional["GoogleDataprocMetastoreServiceEncryptionConfig"], result)

    @builtins.property
    def hive_metastore_config(
        self,
    ) -> typing.Optional["GoogleDataprocMetastoreServiceHiveMetastoreConfig"]:
        '''hive_metastore_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#hive_metastore_config GoogleDataprocMetastoreService#hive_metastore_config}
        '''
        result = self._values.get("hive_metastore_config")
        return typing.cast(typing.Optional["GoogleDataprocMetastoreServiceHiveMetastoreConfig"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#id GoogleDataprocMetastoreService#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#labels GoogleDataprocMetastoreService#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The location where the metastore service should reside. The default value is 'global'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#location GoogleDataprocMetastoreService#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintenance_window(
        self,
    ) -> typing.Optional["GoogleDataprocMetastoreServiceMaintenanceWindow"]:
        '''maintenance_window block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#maintenance_window GoogleDataprocMetastoreService#maintenance_window}
        '''
        result = self._values.get("maintenance_window")
        return typing.cast(typing.Optional["GoogleDataprocMetastoreServiceMaintenanceWindow"], result)

    @builtins.property
    def metadata_integration(
        self,
    ) -> typing.Optional["GoogleDataprocMetastoreServiceMetadataIntegration"]:
        '''metadata_integration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#metadata_integration GoogleDataprocMetastoreService#metadata_integration}
        '''
        result = self._values.get("metadata_integration")
        return typing.cast(typing.Optional["GoogleDataprocMetastoreServiceMetadataIntegration"], result)

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''The relative resource name of the VPC network on which the instance can be accessed.

        It is specified in the following form:

        "projects/{projectNumber}/global/networks/{network_id}".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#network GoogleDataprocMetastoreService#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_config(
        self,
    ) -> typing.Optional["GoogleDataprocMetastoreServiceNetworkConfig"]:
        '''network_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#network_config GoogleDataprocMetastoreService#network_config}
        '''
        result = self._values.get("network_config")
        return typing.cast(typing.Optional["GoogleDataprocMetastoreServiceNetworkConfig"], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The TCP port at which the metastore service is reached. Default: 9083.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#port GoogleDataprocMetastoreService#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#project GoogleDataprocMetastoreService#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def release_channel(self) -> typing.Optional[builtins.str]:
        '''The release channel of the service. If unspecified, defaults to 'STABLE'. Default value: "STABLE" Possible values: ["CANARY", "STABLE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#release_channel GoogleDataprocMetastoreService#release_channel}
        '''
        result = self._values.get("release_channel")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scaling_config(
        self,
    ) -> typing.Optional["GoogleDataprocMetastoreServiceScalingConfig"]:
        '''scaling_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#scaling_config GoogleDataprocMetastoreService#scaling_config}
        '''
        result = self._values.get("scaling_config")
        return typing.cast(typing.Optional["GoogleDataprocMetastoreServiceScalingConfig"], result)

    @builtins.property
    def scheduled_backup(
        self,
    ) -> typing.Optional["GoogleDataprocMetastoreServiceScheduledBackup"]:
        '''scheduled_backup block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#scheduled_backup GoogleDataprocMetastoreService#scheduled_backup}
        '''
        result = self._values.get("scheduled_backup")
        return typing.cast(typing.Optional["GoogleDataprocMetastoreServiceScheduledBackup"], result)

    @builtins.property
    def telemetry_config(
        self,
    ) -> typing.Optional["GoogleDataprocMetastoreServiceTelemetryConfig"]:
        '''telemetry_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#telemetry_config GoogleDataprocMetastoreService#telemetry_config}
        '''
        result = self._values.get("telemetry_config")
        return typing.cast(typing.Optional["GoogleDataprocMetastoreServiceTelemetryConfig"], result)

    @builtins.property
    def tier(self) -> typing.Optional[builtins.str]:
        '''The tier of the service. Possible values: ["DEVELOPER", "ENTERPRISE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#tier GoogleDataprocMetastoreService#tier}
        '''
        result = self._values.get("tier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleDataprocMetastoreServiceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#timeouts GoogleDataprocMetastoreService#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleDataprocMetastoreServiceTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocMetastoreServiceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocMetastoreService.GoogleDataprocMetastoreServiceEncryptionConfig",
    jsii_struct_bases=[],
    name_mapping={"kms_key": "kmsKey"},
)
class GoogleDataprocMetastoreServiceEncryptionConfig:
    def __init__(self, *, kms_key: builtins.str) -> None:
        '''
        :param kms_key: The fully qualified customer provided Cloud KMS key name to use for customer data encryption. Use the following format: 'projects/([^/]+)/locations/([^/]+)/keyRings/([^/]+)/cryptoKeys/([^/]+)'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#kms_key GoogleDataprocMetastoreService#kms_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a26b70aa101b3ff97ca3c0a7030f927d456a7cbaa1013f8a9b506b28afb98ec)
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kms_key": kms_key,
        }

    @builtins.property
    def kms_key(self) -> builtins.str:
        '''The fully qualified customer provided Cloud KMS key name to use for customer data encryption. Use the following format: 'projects/([^/]+)/locations/([^/]+)/keyRings/([^/]+)/cryptoKeys/([^/]+)'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#kms_key GoogleDataprocMetastoreService#kms_key}
        '''
        result = self._values.get("kms_key")
        assert result is not None, "Required property 'kms_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocMetastoreServiceEncryptionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocMetastoreServiceEncryptionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocMetastoreService.GoogleDataprocMetastoreServiceEncryptionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0e34d2ed8ae2b460a24593c51544e83453ac58cf4846760da1d4adf8a990558)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a29b8bdf5850d01f29a3ee9ee982b1b4477bf115ee5e11ae87ecceebd4596d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocMetastoreServiceEncryptionConfig]:
        return typing.cast(typing.Optional[GoogleDataprocMetastoreServiceEncryptionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocMetastoreServiceEncryptionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__410e86c87968ae81d4d9d121758ae47e2e80d544950a6e5d9c8a6244ecb5f6a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocMetastoreService.GoogleDataprocMetastoreServiceHiveMetastoreConfig",
    jsii_struct_bases=[],
    name_mapping={
        "version": "version",
        "auxiliary_versions": "auxiliaryVersions",
        "config_overrides": "configOverrides",
        "endpoint_protocol": "endpointProtocol",
        "kerberos_config": "kerberosConfig",
    },
)
class GoogleDataprocMetastoreServiceHiveMetastoreConfig:
    def __init__(
        self,
        *,
        version: builtins.str,
        auxiliary_versions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        config_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        endpoint_protocol: typing.Optional[builtins.str] = None,
        kerberos_config: typing.Optional[typing.Union["GoogleDataprocMetastoreServiceHiveMetastoreConfigKerberosConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param version: The Hive metastore schema version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#version GoogleDataprocMetastoreService#version}
        :param auxiliary_versions: auxiliary_versions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#auxiliary_versions GoogleDataprocMetastoreService#auxiliary_versions}
        :param config_overrides: A mapping of Hive metastore configuration key-value pairs to apply to the Hive metastore (configured in hive-site.xml). The mappings override system defaults (some keys cannot be overridden). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#config_overrides GoogleDataprocMetastoreService#config_overrides}
        :param endpoint_protocol: The protocol to use for the metastore service endpoint. If unspecified, defaults to 'THRIFT'. Default value: "THRIFT" Possible values: ["THRIFT", "GRPC"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#endpoint_protocol GoogleDataprocMetastoreService#endpoint_protocol}
        :param kerberos_config: kerberos_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#kerberos_config GoogleDataprocMetastoreService#kerberos_config}
        '''
        if isinstance(kerberos_config, dict):
            kerberos_config = GoogleDataprocMetastoreServiceHiveMetastoreConfigKerberosConfig(**kerberos_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36b385943e0f355e706f2739e016be4cb05c0bf6069e71bf01a6cd56ec7edd6b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#version GoogleDataprocMetastoreService#version}
        '''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auxiliary_versions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersions"]]]:
        '''auxiliary_versions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#auxiliary_versions GoogleDataprocMetastoreService#auxiliary_versions}
        '''
        result = self._values.get("auxiliary_versions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersions"]]], result)

    @builtins.property
    def config_overrides(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A mapping of Hive metastore configuration key-value pairs to apply to the Hive metastore (configured in hive-site.xml). The mappings override system defaults (some keys cannot be overridden).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#config_overrides GoogleDataprocMetastoreService#config_overrides}
        '''
        result = self._values.get("config_overrides")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def endpoint_protocol(self) -> typing.Optional[builtins.str]:
        '''The protocol to use for the metastore service endpoint.

        If unspecified, defaults to 'THRIFT'. Default value: "THRIFT" Possible values: ["THRIFT", "GRPC"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#endpoint_protocol GoogleDataprocMetastoreService#endpoint_protocol}
        '''
        result = self._values.get("endpoint_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kerberos_config(
        self,
    ) -> typing.Optional["GoogleDataprocMetastoreServiceHiveMetastoreConfigKerberosConfig"]:
        '''kerberos_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#kerberos_config GoogleDataprocMetastoreService#kerberos_config}
        '''
        result = self._values.get("kerberos_config")
        return typing.cast(typing.Optional["GoogleDataprocMetastoreServiceHiveMetastoreConfigKerberosConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocMetastoreServiceHiveMetastoreConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocMetastoreService.GoogleDataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersions",
    jsii_struct_bases=[],
    name_mapping={
        "key": "key",
        "version": "version",
        "config_overrides": "configOverrides",
    },
)
class GoogleDataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersions:
    def __init__(
        self,
        *,
        key: builtins.str,
        version: builtins.str,
        config_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#key GoogleDataprocMetastoreService#key}.
        :param version: The Hive metastore version of the auxiliary service. It must be less than the primary Hive metastore service's version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#version GoogleDataprocMetastoreService#version}
        :param config_overrides: A mapping of Hive metastore configuration key-value pairs to apply to the auxiliary Hive metastore (configured in hive-site.xml) in addition to the primary version's overrides. If keys are present in both the auxiliary version's overrides and the primary version's overrides, the value from the auxiliary version's overrides takes precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#config_overrides GoogleDataprocMetastoreService#config_overrides}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3f5bf16ee9a9d00b38237fa38bc237603a591284d0b9db9ca97e18f9e022d8b)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#key GoogleDataprocMetastoreService#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''The Hive metastore version of the auxiliary service. It must be less than the primary Hive metastore service's version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#version GoogleDataprocMetastoreService#version}
        '''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def config_overrides(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A mapping of Hive metastore configuration key-value pairs to apply to the auxiliary Hive metastore (configured in hive-site.xml) in addition to the primary version's overrides. If keys are present in both the auxiliary version's overrides and the primary version's overrides, the value from the auxiliary version's overrides takes precedence.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#config_overrides GoogleDataprocMetastoreService#config_overrides}
        '''
        result = self._values.get("config_overrides")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocMetastoreService.GoogleDataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d93007897ca78bcd38de8c07e1c3a50ca69fdf10ee5d5ef047b13267196e309d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b62f838ccb6cd6d45e13a3ced0259433b780c93f579ccd267f9f4033d69e846c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84ffe75124cc85cfaac6a8c057bee46cd9dbad0e5fa1bc9af25e977010f4781a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__00c8109bff285bc0c1cd6c3b9dceb7e6cb1a0981208d5b52d6ce6ac6f8e3081a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__549cd7ce9a04ee2501661f63741d963e7f08f752613bb945465372da6fe5dba9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__465f1d8025b0f68cddac22d71793c763f95ddbe4a4dacd15f43d86226c2dd0ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocMetastoreService.GoogleDataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd7067cfcba444cc23c82b086dc81761230d6875f5c55b910b518e75db69da7a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a83fe549e19ff4985232f000e3a9a52a2f4394e145d063734971595234b7deb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configOverrides", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2df057e3895c7691a4b1d05e2b49f94e650609ee3455c4bee6ac02d0b5685aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97b74e18cd37b087c03540f7fb903268e3059df7b211e150dfc2b8baec95e878)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e87f19555624d9c7632ff04870f5b1ce7c1672cbf4fb073743500338820e8b56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocMetastoreService.GoogleDataprocMetastoreServiceHiveMetastoreConfigKerberosConfig",
    jsii_struct_bases=[],
    name_mapping={
        "keytab": "keytab",
        "krb5_config_gcs_uri": "krb5ConfigGcsUri",
        "principal": "principal",
    },
)
class GoogleDataprocMetastoreServiceHiveMetastoreConfigKerberosConfig:
    def __init__(
        self,
        *,
        keytab: typing.Union["GoogleDataprocMetastoreServiceHiveMetastoreConfigKerberosConfigKeytab", typing.Dict[builtins.str, typing.Any]],
        krb5_config_gcs_uri: builtins.str,
        principal: builtins.str,
    ) -> None:
        '''
        :param keytab: keytab block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#keytab GoogleDataprocMetastoreService#keytab}
        :param krb5_config_gcs_uri: A Cloud Storage URI that specifies the path to a krb5.conf file. It is of the form gs://{bucket_name}/path/to/krb5.conf, although the file does not need to be named krb5.conf explicitly. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#krb5_config_gcs_uri GoogleDataprocMetastoreService#krb5_config_gcs_uri}
        :param principal: A Kerberos principal that exists in the both the keytab the KDC to authenticate as. A typical principal is of the form "primary/instance@REALM", but there is no exact format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#principal GoogleDataprocMetastoreService#principal}
        '''
        if isinstance(keytab, dict):
            keytab = GoogleDataprocMetastoreServiceHiveMetastoreConfigKerberosConfigKeytab(**keytab)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddd961c7b0f82c52246e615598ef0b5c1adf5305475f9876c353e29b6a005ee6)
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
    ) -> "GoogleDataprocMetastoreServiceHiveMetastoreConfigKerberosConfigKeytab":
        '''keytab block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#keytab GoogleDataprocMetastoreService#keytab}
        '''
        result = self._values.get("keytab")
        assert result is not None, "Required property 'keytab' is missing"
        return typing.cast("GoogleDataprocMetastoreServiceHiveMetastoreConfigKerberosConfigKeytab", result)

    @builtins.property
    def krb5_config_gcs_uri(self) -> builtins.str:
        '''A Cloud Storage URI that specifies the path to a krb5.conf file. It is of the form gs://{bucket_name}/path/to/krb5.conf, although the file does not need to be named krb5.conf explicitly.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#krb5_config_gcs_uri GoogleDataprocMetastoreService#krb5_config_gcs_uri}
        '''
        result = self._values.get("krb5_config_gcs_uri")
        assert result is not None, "Required property 'krb5_config_gcs_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def principal(self) -> builtins.str:
        '''A Kerberos principal that exists in the both the keytab the KDC to authenticate as.

        A typical principal is of the form "primary/instance@REALM", but there is no exact format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#principal GoogleDataprocMetastoreService#principal}
        '''
        result = self._values.get("principal")
        assert result is not None, "Required property 'principal' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocMetastoreServiceHiveMetastoreConfigKerberosConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocMetastoreService.GoogleDataprocMetastoreServiceHiveMetastoreConfigKerberosConfigKeytab",
    jsii_struct_bases=[],
    name_mapping={"cloud_secret": "cloudSecret"},
)
class GoogleDataprocMetastoreServiceHiveMetastoreConfigKerberosConfigKeytab:
    def __init__(self, *, cloud_secret: builtins.str) -> None:
        '''
        :param cloud_secret: The relative resource name of a Secret Manager secret version, in the following form:. "projects/{projectNumber}/secrets/{secret_id}/versions/{version_id}". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#cloud_secret GoogleDataprocMetastoreService#cloud_secret}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4908f18a51c487b9b8c14658167c6a15049817018e96e418febd27214b92451)
            check_type(argname="argument cloud_secret", value=cloud_secret, expected_type=type_hints["cloud_secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cloud_secret": cloud_secret,
        }

    @builtins.property
    def cloud_secret(self) -> builtins.str:
        '''The relative resource name of a Secret Manager secret version, in the following form:.

        "projects/{projectNumber}/secrets/{secret_id}/versions/{version_id}".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#cloud_secret GoogleDataprocMetastoreService#cloud_secret}
        '''
        result = self._values.get("cloud_secret")
        assert result is not None, "Required property 'cloud_secret' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocMetastoreServiceHiveMetastoreConfigKerberosConfigKeytab(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocMetastoreServiceHiveMetastoreConfigKerberosConfigKeytabOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocMetastoreService.GoogleDataprocMetastoreServiceHiveMetastoreConfigKerberosConfigKeytabOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__873274fe635d4b41279d628a4c687e85bfebf3c011a92c5b134448f4bf67b022)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a3e5cb13c916d2a66319f774cbb63cac37b47a25a60f4905f814dc63ae923c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocMetastoreServiceHiveMetastoreConfigKerberosConfigKeytab]:
        return typing.cast(typing.Optional[GoogleDataprocMetastoreServiceHiveMetastoreConfigKerberosConfigKeytab], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocMetastoreServiceHiveMetastoreConfigKerberosConfigKeytab],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb9f9b2ed9a71a7d208b84f7fe9c535231b4b14de9f862780be15782136162b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataprocMetastoreServiceHiveMetastoreConfigKerberosConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocMetastoreService.GoogleDataprocMetastoreServiceHiveMetastoreConfigKerberosConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a126d6714579c9cd01f8d516debcfa9b89ca03fd67b074e8b65b3f455f725277)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putKeytab")
    def put_keytab(self, *, cloud_secret: builtins.str) -> None:
        '''
        :param cloud_secret: The relative resource name of a Secret Manager secret version, in the following form:. "projects/{projectNumber}/secrets/{secret_id}/versions/{version_id}". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#cloud_secret GoogleDataprocMetastoreService#cloud_secret}
        '''
        value = GoogleDataprocMetastoreServiceHiveMetastoreConfigKerberosConfigKeytab(
            cloud_secret=cloud_secret
        )

        return typing.cast(None, jsii.invoke(self, "putKeytab", [value]))

    @builtins.property
    @jsii.member(jsii_name="keytab")
    def keytab(
        self,
    ) -> GoogleDataprocMetastoreServiceHiveMetastoreConfigKerberosConfigKeytabOutputReference:
        return typing.cast(GoogleDataprocMetastoreServiceHiveMetastoreConfigKerberosConfigKeytabOutputReference, jsii.get(self, "keytab"))

    @builtins.property
    @jsii.member(jsii_name="keytabInput")
    def keytab_input(
        self,
    ) -> typing.Optional[GoogleDataprocMetastoreServiceHiveMetastoreConfigKerberosConfigKeytab]:
        return typing.cast(typing.Optional[GoogleDataprocMetastoreServiceHiveMetastoreConfigKerberosConfigKeytab], jsii.get(self, "keytabInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__bef5ec44a4615dc5a00b07fa2f89ba101a340e815243ebc25164df57803f4756)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "krb5ConfigGcsUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="principal")
    def principal(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "principal"))

    @principal.setter
    def principal(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__307a68775a88497ef7c6b525e9ffa6c33cdebe2ab27e8c8b9660241c6a0ad68e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "principal", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocMetastoreServiceHiveMetastoreConfigKerberosConfig]:
        return typing.cast(typing.Optional[GoogleDataprocMetastoreServiceHiveMetastoreConfigKerberosConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocMetastoreServiceHiveMetastoreConfigKerberosConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f922d57325bdd9d5a32e63313b6aa4f6996a2ca11942f6116dd3f2eafb4152ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataprocMetastoreServiceHiveMetastoreConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocMetastoreService.GoogleDataprocMetastoreServiceHiveMetastoreConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f430bd2ec2735b1879cad752cf81455e6ec44fcb27990fa5dd11b745241d685)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAuxiliaryVersions")
    def put_auxiliary_versions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfee40a69069a6f94b4ffdbce1f40908ecc415e2ef19bf0568093e575dfdd9b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAuxiliaryVersions", [value]))

    @jsii.member(jsii_name="putKerberosConfig")
    def put_kerberos_config(
        self,
        *,
        keytab: typing.Union[GoogleDataprocMetastoreServiceHiveMetastoreConfigKerberosConfigKeytab, typing.Dict[builtins.str, typing.Any]],
        krb5_config_gcs_uri: builtins.str,
        principal: builtins.str,
    ) -> None:
        '''
        :param keytab: keytab block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#keytab GoogleDataprocMetastoreService#keytab}
        :param krb5_config_gcs_uri: A Cloud Storage URI that specifies the path to a krb5.conf file. It is of the form gs://{bucket_name}/path/to/krb5.conf, although the file does not need to be named krb5.conf explicitly. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#krb5_config_gcs_uri GoogleDataprocMetastoreService#krb5_config_gcs_uri}
        :param principal: A Kerberos principal that exists in the both the keytab the KDC to authenticate as. A typical principal is of the form "primary/instance@REALM", but there is no exact format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#principal GoogleDataprocMetastoreService#principal}
        '''
        value = GoogleDataprocMetastoreServiceHiveMetastoreConfigKerberosConfig(
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
    ) -> GoogleDataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersionsList:
        return typing.cast(GoogleDataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersionsList, jsii.get(self, "auxiliaryVersions"))

    @builtins.property
    @jsii.member(jsii_name="kerberosConfig")
    def kerberos_config(
        self,
    ) -> GoogleDataprocMetastoreServiceHiveMetastoreConfigKerberosConfigOutputReference:
        return typing.cast(GoogleDataprocMetastoreServiceHiveMetastoreConfigKerberosConfigOutputReference, jsii.get(self, "kerberosConfig"))

    @builtins.property
    @jsii.member(jsii_name="auxiliaryVersionsInput")
    def auxiliary_versions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersions]]], jsii.get(self, "auxiliaryVersionsInput"))

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
    ) -> typing.Optional[GoogleDataprocMetastoreServiceHiveMetastoreConfigKerberosConfig]:
        return typing.cast(typing.Optional[GoogleDataprocMetastoreServiceHiveMetastoreConfigKerberosConfig], jsii.get(self, "kerberosConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__1b68e7c6f611f80d326c8e2c7f08ae28d3e2ea2d4763912d002150f506c453e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configOverrides", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endpointProtocol")
    def endpoint_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpointProtocol"))

    @endpoint_protocol.setter
    def endpoint_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2a273e387ed18caa28f05b2b8892d05210c9c5ed25857e5ca18fe6c51b717f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__990c056ad90144268449f81642c0e0ed6c33a697fc04a7065662dce7425f4e23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocMetastoreServiceHiveMetastoreConfig]:
        return typing.cast(typing.Optional[GoogleDataprocMetastoreServiceHiveMetastoreConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocMetastoreServiceHiveMetastoreConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a8f93a46ec19699bc9f754e7fb36973d8b6f990cc4e248e7bbf07b15406b726)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocMetastoreService.GoogleDataprocMetastoreServiceMaintenanceWindow",
    jsii_struct_bases=[],
    name_mapping={"day_of_week": "dayOfWeek", "hour_of_day": "hourOfDay"},
)
class GoogleDataprocMetastoreServiceMaintenanceWindow:
    def __init__(self, *, day_of_week: builtins.str, hour_of_day: jsii.Number) -> None:
        '''
        :param day_of_week: The day of week, when the window starts. Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#day_of_week GoogleDataprocMetastoreService#day_of_week}
        :param hour_of_day: The hour of day (0-23) when the window starts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#hour_of_day GoogleDataprocMetastoreService#hour_of_day}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__484694657027df6e95142448cc7ebebc79f2b21f14fb805a5f02eca8732c6ec0)
            check_type(argname="argument day_of_week", value=day_of_week, expected_type=type_hints["day_of_week"])
            check_type(argname="argument hour_of_day", value=hour_of_day, expected_type=type_hints["hour_of_day"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "day_of_week": day_of_week,
            "hour_of_day": hour_of_day,
        }

    @builtins.property
    def day_of_week(self) -> builtins.str:
        '''The day of week, when the window starts. Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#day_of_week GoogleDataprocMetastoreService#day_of_week}
        '''
        result = self._values.get("day_of_week")
        assert result is not None, "Required property 'day_of_week' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hour_of_day(self) -> jsii.Number:
        '''The hour of day (0-23) when the window starts.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#hour_of_day GoogleDataprocMetastoreService#hour_of_day}
        '''
        result = self._values.get("hour_of_day")
        assert result is not None, "Required property 'hour_of_day' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocMetastoreServiceMaintenanceWindow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocMetastoreServiceMaintenanceWindowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocMetastoreService.GoogleDataprocMetastoreServiceMaintenanceWindowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8074b8411befe64df941411a75176d363d274fea0972cc1474a582e36bbcf77d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__41801eb838b6c3ea41f4fce13599555e654cd314767d83eecd4907729b58e63b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dayOfWeek", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hourOfDay")
    def hour_of_day(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hourOfDay"))

    @hour_of_day.setter
    def hour_of_day(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e63554921a85c9f9572849728e3599ea6640cdb8f46c4c6262bb66dfffd4166)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hourOfDay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocMetastoreServiceMaintenanceWindow]:
        return typing.cast(typing.Optional[GoogleDataprocMetastoreServiceMaintenanceWindow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocMetastoreServiceMaintenanceWindow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ccc24710ce2c8470398d5e7acb2298491cc57c2da7621a2969cbed880998eba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocMetastoreService.GoogleDataprocMetastoreServiceMetadataIntegration",
    jsii_struct_bases=[],
    name_mapping={"data_catalog_config": "dataCatalogConfig"},
)
class GoogleDataprocMetastoreServiceMetadataIntegration:
    def __init__(
        self,
        *,
        data_catalog_config: typing.Union["GoogleDataprocMetastoreServiceMetadataIntegrationDataCatalogConfig", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param data_catalog_config: data_catalog_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#data_catalog_config GoogleDataprocMetastoreService#data_catalog_config}
        '''
        if isinstance(data_catalog_config, dict):
            data_catalog_config = GoogleDataprocMetastoreServiceMetadataIntegrationDataCatalogConfig(**data_catalog_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__520a136aee43276d6020d3d8ffb335bdf64cb0f9ea4dba5da967ef5cc5087ca1)
            check_type(argname="argument data_catalog_config", value=data_catalog_config, expected_type=type_hints["data_catalog_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_catalog_config": data_catalog_config,
        }

    @builtins.property
    def data_catalog_config(
        self,
    ) -> "GoogleDataprocMetastoreServiceMetadataIntegrationDataCatalogConfig":
        '''data_catalog_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#data_catalog_config GoogleDataprocMetastoreService#data_catalog_config}
        '''
        result = self._values.get("data_catalog_config")
        assert result is not None, "Required property 'data_catalog_config' is missing"
        return typing.cast("GoogleDataprocMetastoreServiceMetadataIntegrationDataCatalogConfig", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocMetastoreServiceMetadataIntegration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocMetastoreService.GoogleDataprocMetastoreServiceMetadataIntegrationDataCatalogConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GoogleDataprocMetastoreServiceMetadataIntegrationDataCatalogConfig:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Defines whether the metastore metadata should be synced to Data Catalog. The default value is to disable syncing metastore metadata to Data Catalog. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#enabled GoogleDataprocMetastoreService#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0b925f708d252f0e7df94f052017f5c399ef63a125e5f3c172bb1753354318f)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Defines whether the metastore metadata should be synced to Data Catalog.

        The default value is to disable syncing metastore metadata to Data Catalog.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#enabled GoogleDataprocMetastoreService#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocMetastoreServiceMetadataIntegrationDataCatalogConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocMetastoreServiceMetadataIntegrationDataCatalogConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocMetastoreService.GoogleDataprocMetastoreServiceMetadataIntegrationDataCatalogConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ddee1dbe77f35b36a0bb97545fd96816d727b65dc259cd7adf5f6b0d15b72690)
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
            type_hints = typing.get_type_hints(_typecheckingstub__248861b9c731b5d938ae6183ff6a57191f61b511b26cf04d6c0dc64e421eb436)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocMetastoreServiceMetadataIntegrationDataCatalogConfig]:
        return typing.cast(typing.Optional[GoogleDataprocMetastoreServiceMetadataIntegrationDataCatalogConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocMetastoreServiceMetadataIntegrationDataCatalogConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26dfa3c27dd557217f9119064985e7a1b76657cb7048e91f41932c74bd02bc30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataprocMetastoreServiceMetadataIntegrationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocMetastoreService.GoogleDataprocMetastoreServiceMetadataIntegrationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ab46b515fb01d9519a6a8676d8b6af1b13354e726da3a9e1e077710e5946e71)
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
        :param enabled: Defines whether the metastore metadata should be synced to Data Catalog. The default value is to disable syncing metastore metadata to Data Catalog. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#enabled GoogleDataprocMetastoreService#enabled}
        '''
        value = GoogleDataprocMetastoreServiceMetadataIntegrationDataCatalogConfig(
            enabled=enabled
        )

        return typing.cast(None, jsii.invoke(self, "putDataCatalogConfig", [value]))

    @builtins.property
    @jsii.member(jsii_name="dataCatalogConfig")
    def data_catalog_config(
        self,
    ) -> GoogleDataprocMetastoreServiceMetadataIntegrationDataCatalogConfigOutputReference:
        return typing.cast(GoogleDataprocMetastoreServiceMetadataIntegrationDataCatalogConfigOutputReference, jsii.get(self, "dataCatalogConfig"))

    @builtins.property
    @jsii.member(jsii_name="dataCatalogConfigInput")
    def data_catalog_config_input(
        self,
    ) -> typing.Optional[GoogleDataprocMetastoreServiceMetadataIntegrationDataCatalogConfig]:
        return typing.cast(typing.Optional[GoogleDataprocMetastoreServiceMetadataIntegrationDataCatalogConfig], jsii.get(self, "dataCatalogConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocMetastoreServiceMetadataIntegration]:
        return typing.cast(typing.Optional[GoogleDataprocMetastoreServiceMetadataIntegration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocMetastoreServiceMetadataIntegration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca2cafcaa01420e953fb6ac9848a9767dd40e964b2365ea05a57c17ba49e071b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocMetastoreService.GoogleDataprocMetastoreServiceNetworkConfig",
    jsii_struct_bases=[],
    name_mapping={
        "consumers": "consumers",
        "custom_routes_enabled": "customRoutesEnabled",
    },
)
class GoogleDataprocMetastoreServiceNetworkConfig:
    def __init__(
        self,
        *,
        consumers: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataprocMetastoreServiceNetworkConfigConsumers", typing.Dict[builtins.str, typing.Any]]]],
        custom_routes_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param consumers: consumers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#consumers GoogleDataprocMetastoreService#consumers}
        :param custom_routes_enabled: Enables custom routes to be imported and exported for the Dataproc Metastore service's peered VPC network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#custom_routes_enabled GoogleDataprocMetastoreService#custom_routes_enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__715c11af667637bbabd13a8ea78c99d922b89582f4097c5786879e101f1e24f7)
            check_type(argname="argument consumers", value=consumers, expected_type=type_hints["consumers"])
            check_type(argname="argument custom_routes_enabled", value=custom_routes_enabled, expected_type=type_hints["custom_routes_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "consumers": consumers,
        }
        if custom_routes_enabled is not None:
            self._values["custom_routes_enabled"] = custom_routes_enabled

    @builtins.property
    def consumers(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataprocMetastoreServiceNetworkConfigConsumers"]]:
        '''consumers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#consumers GoogleDataprocMetastoreService#consumers}
        '''
        result = self._values.get("consumers")
        assert result is not None, "Required property 'consumers' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataprocMetastoreServiceNetworkConfigConsumers"]], result)

    @builtins.property
    def custom_routes_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables custom routes to be imported and exported for the Dataproc Metastore service's peered VPC network.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#custom_routes_enabled GoogleDataprocMetastoreService#custom_routes_enabled}
        '''
        result = self._values.get("custom_routes_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocMetastoreServiceNetworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocMetastoreService.GoogleDataprocMetastoreServiceNetworkConfigConsumers",
    jsii_struct_bases=[],
    name_mapping={"subnetwork": "subnetwork"},
)
class GoogleDataprocMetastoreServiceNetworkConfigConsumers:
    def __init__(self, *, subnetwork: builtins.str) -> None:
        '''
        :param subnetwork: The subnetwork of the customer project from which an IP address is reserved and used as the Dataproc Metastore service's endpoint. It is accessible to hosts in the subnet and to all hosts in a subnet in the same region and same network. There must be at least one IP address available in the subnet's primary range. The subnet is specified in the following form: 'projects/{projectNumber}/regions/{region_id}/subnetworks/{subnetwork_id} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#subnetwork GoogleDataprocMetastoreService#subnetwork}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c650e847eda4c4929b929ca79080c99544d951ecbb18abc2c3c76185bb0cf730)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#subnetwork GoogleDataprocMetastoreService#subnetwork}
        '''
        result = self._values.get("subnetwork")
        assert result is not None, "Required property 'subnetwork' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocMetastoreServiceNetworkConfigConsumers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocMetastoreServiceNetworkConfigConsumersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocMetastoreService.GoogleDataprocMetastoreServiceNetworkConfigConsumersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a981f5d563b1238692db67b2333f136e6f07f933d6be243d47bda5e8cc504de4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataprocMetastoreServiceNetworkConfigConsumersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fd279ae392ce5fac2729423cb0c18dcde30352e5bb812f44db4dc74305e092f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataprocMetastoreServiceNetworkConfigConsumersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d07296e24cac35951a4ae21d6e128c1c5d3dbc0b1a15333b3a8825fe4619bb67)
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
            type_hints = typing.get_type_hints(_typecheckingstub__48fdebbefab07bc870d1903ba22e3a80d10afc547539c61affd41ad606dad6ef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4c958bf76348fa3cf0e05f43c19eb54dcae64b78341654f7cf11f2dff716e03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocMetastoreServiceNetworkConfigConsumers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocMetastoreServiceNetworkConfigConsumers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocMetastoreServiceNetworkConfigConsumers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8026d5464fe48d03fe521392dbe0731addbdd6fa4f536f09f463f4a12ffcfe38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataprocMetastoreServiceNetworkConfigConsumersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocMetastoreService.GoogleDataprocMetastoreServiceNetworkConfigConsumersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e17cd90b4bfecfc55b245acaf20d8eb9971ad4ce99acfcc1ff49ec7b5290fa94)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2755c16066e5a11551584afadd2252124ab07e8b17dd07f104a712240c62279)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocMetastoreServiceNetworkConfigConsumers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocMetastoreServiceNetworkConfigConsumers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocMetastoreServiceNetworkConfigConsumers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5486c6d6b85982e082622db23ade26872cb3c8e589921bd4f7f13493d653741c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataprocMetastoreServiceNetworkConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocMetastoreService.GoogleDataprocMetastoreServiceNetworkConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__afd62df96f9ac3f5dd0ea1b4d0998f30c930beb6ce1b89d63ee7702223c77e1d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConsumers")
    def put_consumers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataprocMetastoreServiceNetworkConfigConsumers, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cd3173e2db7e04b8d72619f20bdde6cc29ff995b759e4a19ce4d6dca2c85bac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConsumers", [value]))

    @jsii.member(jsii_name="resetCustomRoutesEnabled")
    def reset_custom_routes_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomRoutesEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="consumers")
    def consumers(self) -> GoogleDataprocMetastoreServiceNetworkConfigConsumersList:
        return typing.cast(GoogleDataprocMetastoreServiceNetworkConfigConsumersList, jsii.get(self, "consumers"))

    @builtins.property
    @jsii.member(jsii_name="consumersInput")
    def consumers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocMetastoreServiceNetworkConfigConsumers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocMetastoreServiceNetworkConfigConsumers]]], jsii.get(self, "consumersInput"))

    @builtins.property
    @jsii.member(jsii_name="customRoutesEnabledInput")
    def custom_routes_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "customRoutesEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="customRoutesEnabled")
    def custom_routes_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "customRoutesEnabled"))

    @custom_routes_enabled.setter
    def custom_routes_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba70a490fcbae8446893ce4b5cfa8a57a4d6ce434104c14f1547caddd89d6db3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customRoutesEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocMetastoreServiceNetworkConfig]:
        return typing.cast(typing.Optional[GoogleDataprocMetastoreServiceNetworkConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocMetastoreServiceNetworkConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__609e9fb204f438f45984f3ea3d775004ad1d188903be06ea19b97cd65bfd0075)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocMetastoreService.GoogleDataprocMetastoreServiceScalingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "autoscaling_config": "autoscalingConfig",
        "instance_size": "instanceSize",
        "scaling_factor": "scalingFactor",
    },
)
class GoogleDataprocMetastoreServiceScalingConfig:
    def __init__(
        self,
        *,
        autoscaling_config: typing.Optional[typing.Union["GoogleDataprocMetastoreServiceScalingConfigAutoscalingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        instance_size: typing.Optional[builtins.str] = None,
        scaling_factor: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param autoscaling_config: autoscaling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#autoscaling_config GoogleDataprocMetastoreService#autoscaling_config}
        :param instance_size: Metastore instance sizes. Possible values: ["EXTRA_SMALL", "SMALL", "MEDIUM", "LARGE", "EXTRA_LARGE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#instance_size GoogleDataprocMetastoreService#instance_size}
        :param scaling_factor: Scaling factor, in increments of 0.1 for values less than 1.0, and increments of 1.0 for values greater than 1.0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#scaling_factor GoogleDataprocMetastoreService#scaling_factor}
        '''
        if isinstance(autoscaling_config, dict):
            autoscaling_config = GoogleDataprocMetastoreServiceScalingConfigAutoscalingConfig(**autoscaling_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__482acde6f03e1f2f31e18869f41396fd590fd1279f6f368c8cdce18600710831)
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
    ) -> typing.Optional["GoogleDataprocMetastoreServiceScalingConfigAutoscalingConfig"]:
        '''autoscaling_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#autoscaling_config GoogleDataprocMetastoreService#autoscaling_config}
        '''
        result = self._values.get("autoscaling_config")
        return typing.cast(typing.Optional["GoogleDataprocMetastoreServiceScalingConfigAutoscalingConfig"], result)

    @builtins.property
    def instance_size(self) -> typing.Optional[builtins.str]:
        '''Metastore instance sizes. Possible values: ["EXTRA_SMALL", "SMALL", "MEDIUM", "LARGE", "EXTRA_LARGE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#instance_size GoogleDataprocMetastoreService#instance_size}
        '''
        result = self._values.get("instance_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scaling_factor(self) -> typing.Optional[jsii.Number]:
        '''Scaling factor, in increments of 0.1 for values less than 1.0, and increments of 1.0 for values greater than 1.0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#scaling_factor GoogleDataprocMetastoreService#scaling_factor}
        '''
        result = self._values.get("scaling_factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocMetastoreServiceScalingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocMetastoreService.GoogleDataprocMetastoreServiceScalingConfigAutoscalingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "autoscaling_enabled": "autoscalingEnabled",
        "limit_config": "limitConfig",
    },
)
class GoogleDataprocMetastoreServiceScalingConfigAutoscalingConfig:
    def __init__(
        self,
        *,
        autoscaling_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        limit_config: typing.Optional[typing.Union["GoogleDataprocMetastoreServiceScalingConfigAutoscalingConfigLimitConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param autoscaling_enabled: Defines whether autoscaling is enabled. The default value is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#autoscaling_enabled GoogleDataprocMetastoreService#autoscaling_enabled}
        :param limit_config: limit_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#limit_config GoogleDataprocMetastoreService#limit_config}
        '''
        if isinstance(limit_config, dict):
            limit_config = GoogleDataprocMetastoreServiceScalingConfigAutoscalingConfigLimitConfig(**limit_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa57425d4a06bc4075f0890e9fd86e9b8c81daa3262143189fd96105a7716f56)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#autoscaling_enabled GoogleDataprocMetastoreService#autoscaling_enabled}
        '''
        result = self._values.get("autoscaling_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def limit_config(
        self,
    ) -> typing.Optional["GoogleDataprocMetastoreServiceScalingConfigAutoscalingConfigLimitConfig"]:
        '''limit_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#limit_config GoogleDataprocMetastoreService#limit_config}
        '''
        result = self._values.get("limit_config")
        return typing.cast(typing.Optional["GoogleDataprocMetastoreServiceScalingConfigAutoscalingConfigLimitConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocMetastoreServiceScalingConfigAutoscalingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocMetastoreService.GoogleDataprocMetastoreServiceScalingConfigAutoscalingConfigLimitConfig",
    jsii_struct_bases=[],
    name_mapping={
        "max_scaling_factor": "maxScalingFactor",
        "min_scaling_factor": "minScalingFactor",
    },
)
class GoogleDataprocMetastoreServiceScalingConfigAutoscalingConfigLimitConfig:
    def __init__(
        self,
        *,
        max_scaling_factor: typing.Optional[jsii.Number] = None,
        min_scaling_factor: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_scaling_factor: The maximum scaling factor that the service will autoscale to. The default value is 6.0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#max_scaling_factor GoogleDataprocMetastoreService#max_scaling_factor}
        :param min_scaling_factor: The minimum scaling factor that the service will autoscale to. The default value is 0.1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#min_scaling_factor GoogleDataprocMetastoreService#min_scaling_factor}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__086f3bb5a898890b808fd39f876b58ac2d0a8cc36b2fee5eabc4524004b0fb8b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#max_scaling_factor GoogleDataprocMetastoreService#max_scaling_factor}
        '''
        result = self._values.get("max_scaling_factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_scaling_factor(self) -> typing.Optional[jsii.Number]:
        '''The minimum scaling factor that the service will autoscale to. The default value is 0.1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#min_scaling_factor GoogleDataprocMetastoreService#min_scaling_factor}
        '''
        result = self._values.get("min_scaling_factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocMetastoreServiceScalingConfigAutoscalingConfigLimitConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocMetastoreServiceScalingConfigAutoscalingConfigLimitConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocMetastoreService.GoogleDataprocMetastoreServiceScalingConfigAutoscalingConfigLimitConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__418293b5a8820a1e361e2373e6b79dc90fcb39275c3b7cb129da518e22c6f45e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__de4b2475e3749cea6d32f38fd1aace8d913d94ba2a711e5baac5a6b622a5681f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxScalingFactor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minScalingFactor")
    def min_scaling_factor(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minScalingFactor"))

    @min_scaling_factor.setter
    def min_scaling_factor(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__986b3e14d3da9ffa95efd8915d866a26f7cc1d1b097c39c4b16d110f5926fe65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minScalingFactor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocMetastoreServiceScalingConfigAutoscalingConfigLimitConfig]:
        return typing.cast(typing.Optional[GoogleDataprocMetastoreServiceScalingConfigAutoscalingConfigLimitConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocMetastoreServiceScalingConfigAutoscalingConfigLimitConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68825e6173eef4cca20a41518816601087a13f2d345eadfb01934b6074502eec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataprocMetastoreServiceScalingConfigAutoscalingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocMetastoreService.GoogleDataprocMetastoreServiceScalingConfigAutoscalingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__039ac61584486ef53c99e0fb8cf9096fb1a5d32999eedafdfd2be074c6aacd02)
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
        :param max_scaling_factor: The maximum scaling factor that the service will autoscale to. The default value is 6.0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#max_scaling_factor GoogleDataprocMetastoreService#max_scaling_factor}
        :param min_scaling_factor: The minimum scaling factor that the service will autoscale to. The default value is 0.1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#min_scaling_factor GoogleDataprocMetastoreService#min_scaling_factor}
        '''
        value = GoogleDataprocMetastoreServiceScalingConfigAutoscalingConfigLimitConfig(
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
    ) -> GoogleDataprocMetastoreServiceScalingConfigAutoscalingConfigLimitConfigOutputReference:
        return typing.cast(GoogleDataprocMetastoreServiceScalingConfigAutoscalingConfigLimitConfigOutputReference, jsii.get(self, "limitConfig"))

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
    ) -> typing.Optional[GoogleDataprocMetastoreServiceScalingConfigAutoscalingConfigLimitConfig]:
        return typing.cast(typing.Optional[GoogleDataprocMetastoreServiceScalingConfigAutoscalingConfigLimitConfig], jsii.get(self, "limitConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__c708d49c5795e8d24befb08f75b42fa7cf4021f72d99b6e32e49d1947e9af3e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoscalingEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocMetastoreServiceScalingConfigAutoscalingConfig]:
        return typing.cast(typing.Optional[GoogleDataprocMetastoreServiceScalingConfigAutoscalingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocMetastoreServiceScalingConfigAutoscalingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4ccae37313ed4a5dd97de8039d0f9cf7c16279fa556cdb60de9dfa596393986)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataprocMetastoreServiceScalingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocMetastoreService.GoogleDataprocMetastoreServiceScalingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd4ee3b788885020c0c35e7d495034126579751566e40ae04705cd758b99beaa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAutoscalingConfig")
    def put_autoscaling_config(
        self,
        *,
        autoscaling_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        limit_config: typing.Optional[typing.Union[GoogleDataprocMetastoreServiceScalingConfigAutoscalingConfigLimitConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param autoscaling_enabled: Defines whether autoscaling is enabled. The default value is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#autoscaling_enabled GoogleDataprocMetastoreService#autoscaling_enabled}
        :param limit_config: limit_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#limit_config GoogleDataprocMetastoreService#limit_config}
        '''
        value = GoogleDataprocMetastoreServiceScalingConfigAutoscalingConfig(
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
    ) -> GoogleDataprocMetastoreServiceScalingConfigAutoscalingConfigOutputReference:
        return typing.cast(GoogleDataprocMetastoreServiceScalingConfigAutoscalingConfigOutputReference, jsii.get(self, "autoscalingConfig"))

    @builtins.property
    @jsii.member(jsii_name="autoscalingConfigInput")
    def autoscaling_config_input(
        self,
    ) -> typing.Optional[GoogleDataprocMetastoreServiceScalingConfigAutoscalingConfig]:
        return typing.cast(typing.Optional[GoogleDataprocMetastoreServiceScalingConfigAutoscalingConfig], jsii.get(self, "autoscalingConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__735daa7f72ea084832ec903897eb359da2f8c67c06d27098603f79f813b4aa1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scalingFactor")
    def scaling_factor(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scalingFactor"))

    @scaling_factor.setter
    def scaling_factor(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1572c7e604f29270a41cb7a2ce8250d4eaf73d58f2ef70d3eb4cc16ff13d7399)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scalingFactor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocMetastoreServiceScalingConfig]:
        return typing.cast(typing.Optional[GoogleDataprocMetastoreServiceScalingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocMetastoreServiceScalingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c632df4f1c1d97c324807c4b785d642029096a454d06cce582e20e307271c4c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocMetastoreService.GoogleDataprocMetastoreServiceScheduledBackup",
    jsii_struct_bases=[],
    name_mapping={
        "backup_location": "backupLocation",
        "cron_schedule": "cronSchedule",
        "enabled": "enabled",
        "time_zone": "timeZone",
    },
)
class GoogleDataprocMetastoreServiceScheduledBackup:
    def __init__(
        self,
        *,
        backup_location: builtins.str,
        cron_schedule: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        time_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param backup_location: A Cloud Storage URI of a folder, in the format gs://<bucket_name>/<path_inside_bucket>. A sub-folder <backup_folder> containing backup files will be stored below it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#backup_location GoogleDataprocMetastoreService#backup_location}
        :param cron_schedule: The scheduled interval in Cron format, see https://en.wikipedia.org/wiki/Cron The default is empty: scheduled backup is not enabled. Must be specified to enable scheduled backups. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#cron_schedule GoogleDataprocMetastoreService#cron_schedule}
        :param enabled: Defines whether the scheduled backup is enabled. The default value is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#enabled GoogleDataprocMetastoreService#enabled}
        :param time_zone: Specifies the time zone to be used when interpreting cronSchedule. Must be a time zone name from the time zone database (https://en.wikipedia.org/wiki/List_of_tz_database_time_zones), e.g. America/Los_Angeles or Africa/Abidjan. If left unspecified, the default is UTC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#time_zone GoogleDataprocMetastoreService#time_zone}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9ca7c18704e50afdc3398e64e6606b1382104602e9338a31b651ace94fc3a83)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#backup_location GoogleDataprocMetastoreService#backup_location}
        '''
        result = self._values.get("backup_location")
        assert result is not None, "Required property 'backup_location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cron_schedule(self) -> typing.Optional[builtins.str]:
        '''The scheduled interval in Cron format, see https://en.wikipedia.org/wiki/Cron The default is empty: scheduled backup is not enabled. Must be specified to enable scheduled backups.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#cron_schedule GoogleDataprocMetastoreService#cron_schedule}
        '''
        result = self._values.get("cron_schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defines whether the scheduled backup is enabled. The default value is false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#enabled GoogleDataprocMetastoreService#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def time_zone(self) -> typing.Optional[builtins.str]:
        '''Specifies the time zone to be used when interpreting cronSchedule.

        Must be a time zone name from the time zone database (https://en.wikipedia.org/wiki/List_of_tz_database_time_zones), e.g. America/Los_Angeles or Africa/Abidjan. If left unspecified, the default is UTC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#time_zone GoogleDataprocMetastoreService#time_zone}
        '''
        result = self._values.get("time_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocMetastoreServiceScheduledBackup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocMetastoreServiceScheduledBackupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocMetastoreService.GoogleDataprocMetastoreServiceScheduledBackupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae935739ff64c77f8533be2e857a287c5a0829bd22381fe5bab5d8edc3ed15d9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb5d2ca8d19d261849664c25124cf79def0c51c28c16dbe952e591dfc00d96a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cronSchedule")
    def cron_schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cronSchedule"))

    @cron_schedule.setter
    def cron_schedule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__104f366866df4d0bc6d67c91d12632fcd639f95499acf3ee35e096e13e87d7ef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e434ac47087f6b6108948719e98669c0ab17190d46cb48d59a7d328a950300c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__950d7f84557bd9d491b4d9e8e939fde83bc6367026ebc330acf20bf5af4236e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocMetastoreServiceScheduledBackup]:
        return typing.cast(typing.Optional[GoogleDataprocMetastoreServiceScheduledBackup], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocMetastoreServiceScheduledBackup],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86219b1c335d905b2ce5caa376880a5a8640d6b44666246b20510cbeaa1f2249)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocMetastoreService.GoogleDataprocMetastoreServiceTelemetryConfig",
    jsii_struct_bases=[],
    name_mapping={"log_format": "logFormat"},
)
class GoogleDataprocMetastoreServiceTelemetryConfig:
    def __init__(self, *, log_format: typing.Optional[builtins.str] = None) -> None:
        '''
        :param log_format: The output format of the Dataproc Metastore service's logs. Default value: "JSON" Possible values: ["LEGACY", "JSON"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#log_format GoogleDataprocMetastoreService#log_format}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d68847a9680009fa4132c7011c614d4c796f9ae85f4d8fa6b63b9bf1ead9d722)
            check_type(argname="argument log_format", value=log_format, expected_type=type_hints["log_format"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if log_format is not None:
            self._values["log_format"] = log_format

    @builtins.property
    def log_format(self) -> typing.Optional[builtins.str]:
        '''The output format of the Dataproc Metastore service's logs. Default value: "JSON" Possible values: ["LEGACY", "JSON"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#log_format GoogleDataprocMetastoreService#log_format}
        '''
        result = self._values.get("log_format")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocMetastoreServiceTelemetryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocMetastoreServiceTelemetryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocMetastoreService.GoogleDataprocMetastoreServiceTelemetryConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__678e1ba0cbcb0fbd7108534a97cd7b93848a44f303e5b09c900a9528bf57e515)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7194e82c4631fbcb44bdc74fde511aed59a3f0a0145f02dd17b051adf1caa2b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocMetastoreServiceTelemetryConfig]:
        return typing.cast(typing.Optional[GoogleDataprocMetastoreServiceTelemetryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocMetastoreServiceTelemetryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b354609fb7fc00483183b034367834e8611d3fa6dafabc975b08d67362ac43b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocMetastoreService.GoogleDataprocMetastoreServiceTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleDataprocMetastoreServiceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#create GoogleDataprocMetastoreService#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#delete GoogleDataprocMetastoreService#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#update GoogleDataprocMetastoreService#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__786d29cf86067242546b3b5ea859ed1843606df5f0a6a6e6b95cfbe01a13b3b7)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#create GoogleDataprocMetastoreService#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#delete GoogleDataprocMetastoreService#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_metastore_service#update GoogleDataprocMetastoreService#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocMetastoreServiceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocMetastoreServiceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocMetastoreService.GoogleDataprocMetastoreServiceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab6382eb7c1a0c61fd6457de85fd85a7a032a2c068c63391267ca390412424ae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__35dc2411c3ee2e47b7cd73b4d92aaeb907c6ccac92877fcbb46823e72a210f04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15d3faa5cccec7385f6040bd81154b4ce1a10403f70921f4e659021b382f9b95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7e9e3004d5b781d8cf11220e54aa6bca57c897de2afde0cd1204b8a4e80ed75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocMetastoreServiceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocMetastoreServiceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocMetastoreServiceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d72699f5cf06ccbd1487a26110a5035ed5cfc4b2fe1950103c4de383db0d134)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleDataprocMetastoreService",
    "GoogleDataprocMetastoreServiceConfig",
    "GoogleDataprocMetastoreServiceEncryptionConfig",
    "GoogleDataprocMetastoreServiceEncryptionConfigOutputReference",
    "GoogleDataprocMetastoreServiceHiveMetastoreConfig",
    "GoogleDataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersions",
    "GoogleDataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersionsList",
    "GoogleDataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersionsOutputReference",
    "GoogleDataprocMetastoreServiceHiveMetastoreConfigKerberosConfig",
    "GoogleDataprocMetastoreServiceHiveMetastoreConfigKerberosConfigKeytab",
    "GoogleDataprocMetastoreServiceHiveMetastoreConfigKerberosConfigKeytabOutputReference",
    "GoogleDataprocMetastoreServiceHiveMetastoreConfigKerberosConfigOutputReference",
    "GoogleDataprocMetastoreServiceHiveMetastoreConfigOutputReference",
    "GoogleDataprocMetastoreServiceMaintenanceWindow",
    "GoogleDataprocMetastoreServiceMaintenanceWindowOutputReference",
    "GoogleDataprocMetastoreServiceMetadataIntegration",
    "GoogleDataprocMetastoreServiceMetadataIntegrationDataCatalogConfig",
    "GoogleDataprocMetastoreServiceMetadataIntegrationDataCatalogConfigOutputReference",
    "GoogleDataprocMetastoreServiceMetadataIntegrationOutputReference",
    "GoogleDataprocMetastoreServiceNetworkConfig",
    "GoogleDataprocMetastoreServiceNetworkConfigConsumers",
    "GoogleDataprocMetastoreServiceNetworkConfigConsumersList",
    "GoogleDataprocMetastoreServiceNetworkConfigConsumersOutputReference",
    "GoogleDataprocMetastoreServiceNetworkConfigOutputReference",
    "GoogleDataprocMetastoreServiceScalingConfig",
    "GoogleDataprocMetastoreServiceScalingConfigAutoscalingConfig",
    "GoogleDataprocMetastoreServiceScalingConfigAutoscalingConfigLimitConfig",
    "GoogleDataprocMetastoreServiceScalingConfigAutoscalingConfigLimitConfigOutputReference",
    "GoogleDataprocMetastoreServiceScalingConfigAutoscalingConfigOutputReference",
    "GoogleDataprocMetastoreServiceScalingConfigOutputReference",
    "GoogleDataprocMetastoreServiceScheduledBackup",
    "GoogleDataprocMetastoreServiceScheduledBackupOutputReference",
    "GoogleDataprocMetastoreServiceTelemetryConfig",
    "GoogleDataprocMetastoreServiceTelemetryConfigOutputReference",
    "GoogleDataprocMetastoreServiceTimeouts",
    "GoogleDataprocMetastoreServiceTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__a9cf4bc6d38963afb60304c9411f5694a66e81db8e88c3f76d5caec80a3a1a89(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    service_id: builtins.str,
    database_type: typing.Optional[builtins.str] = None,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encryption_config: typing.Optional[typing.Union[GoogleDataprocMetastoreServiceEncryptionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    hive_metastore_config: typing.Optional[typing.Union[GoogleDataprocMetastoreServiceHiveMetastoreConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    maintenance_window: typing.Optional[typing.Union[GoogleDataprocMetastoreServiceMaintenanceWindow, typing.Dict[builtins.str, typing.Any]]] = None,
    metadata_integration: typing.Optional[typing.Union[GoogleDataprocMetastoreServiceMetadataIntegration, typing.Dict[builtins.str, typing.Any]]] = None,
    network: typing.Optional[builtins.str] = None,
    network_config: typing.Optional[typing.Union[GoogleDataprocMetastoreServiceNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    port: typing.Optional[jsii.Number] = None,
    project: typing.Optional[builtins.str] = None,
    release_channel: typing.Optional[builtins.str] = None,
    scaling_config: typing.Optional[typing.Union[GoogleDataprocMetastoreServiceScalingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    scheduled_backup: typing.Optional[typing.Union[GoogleDataprocMetastoreServiceScheduledBackup, typing.Dict[builtins.str, typing.Any]]] = None,
    telemetry_config: typing.Optional[typing.Union[GoogleDataprocMetastoreServiceTelemetryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    tier: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDataprocMetastoreServiceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__bd9e3592af3e1d660bc3690fb3a77ea2fd83ab59864b45a8e25f5d5ec94a416e(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e55f4275643f970cb8a7a565cac8e3eb498f0289720fd59922e02a67c6f2398e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d58b4bdbfb01aeff98fc888a191ba07d59640fd1a7adf17d6e1b80d4335a7882(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b93a6154de450b9fb1aab719f682e037cfe1b2e4f02824bf948a01cdc37f92e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc6ae48d1d4be72a989a6d725a02cfc7099caa38ce7a1b63130752f4e9aa214d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52bcca49e1a4d94704efa4c01b6d36f8e83b18177480fa7cd8a6dc58d9892932(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04c4f53d3d9e938e1d51f2ad32302dfa47f83f4b3d3ba4c64ab3f28599cdae85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae736363f85d332443370768686f30149344c80dc9aff3d329240dab5b635dbb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4b72d9a8289133cc75fb6d529115cac7a8a30227b1422013dbfcdc043d1bfc2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4b7673c4d02349c2078dabd1106e674efbb651238290cf7d3be3909f7c4ff29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08f824fce2eda36205851a26081e3c8edbce6d19c42f6477ab8cae76d7e66136(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e763de31a4578f796d9a9ac0a62ae992b7a0ee9a5e7599813f7a05a4c76f1a93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f20cd5f9c16ba80af87f3c149ea683291ef09ac55c6b06ab8dc3b929477ec256(
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
    encryption_config: typing.Optional[typing.Union[GoogleDataprocMetastoreServiceEncryptionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    hive_metastore_config: typing.Optional[typing.Union[GoogleDataprocMetastoreServiceHiveMetastoreConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    maintenance_window: typing.Optional[typing.Union[GoogleDataprocMetastoreServiceMaintenanceWindow, typing.Dict[builtins.str, typing.Any]]] = None,
    metadata_integration: typing.Optional[typing.Union[GoogleDataprocMetastoreServiceMetadataIntegration, typing.Dict[builtins.str, typing.Any]]] = None,
    network: typing.Optional[builtins.str] = None,
    network_config: typing.Optional[typing.Union[GoogleDataprocMetastoreServiceNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    port: typing.Optional[jsii.Number] = None,
    project: typing.Optional[builtins.str] = None,
    release_channel: typing.Optional[builtins.str] = None,
    scaling_config: typing.Optional[typing.Union[GoogleDataprocMetastoreServiceScalingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    scheduled_backup: typing.Optional[typing.Union[GoogleDataprocMetastoreServiceScheduledBackup, typing.Dict[builtins.str, typing.Any]]] = None,
    telemetry_config: typing.Optional[typing.Union[GoogleDataprocMetastoreServiceTelemetryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    tier: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDataprocMetastoreServiceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a26b70aa101b3ff97ca3c0a7030f927d456a7cbaa1013f8a9b506b28afb98ec(
    *,
    kms_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0e34d2ed8ae2b460a24593c51544e83453ac58cf4846760da1d4adf8a990558(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a29b8bdf5850d01f29a3ee9ee982b1b4477bf115ee5e11ae87ecceebd4596d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__410e86c87968ae81d4d9d121758ae47e2e80d544950a6e5d9c8a6244ecb5f6a1(
    value: typing.Optional[GoogleDataprocMetastoreServiceEncryptionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36b385943e0f355e706f2739e016be4cb05c0bf6069e71bf01a6cd56ec7edd6b(
    *,
    version: builtins.str,
    auxiliary_versions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    config_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    endpoint_protocol: typing.Optional[builtins.str] = None,
    kerberos_config: typing.Optional[typing.Union[GoogleDataprocMetastoreServiceHiveMetastoreConfigKerberosConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3f5bf16ee9a9d00b38237fa38bc237603a591284d0b9db9ca97e18f9e022d8b(
    *,
    key: builtins.str,
    version: builtins.str,
    config_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d93007897ca78bcd38de8c07e1c3a50ca69fdf10ee5d5ef047b13267196e309d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b62f838ccb6cd6d45e13a3ced0259433b780c93f579ccd267f9f4033d69e846c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84ffe75124cc85cfaac6a8c057bee46cd9dbad0e5fa1bc9af25e977010f4781a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00c8109bff285bc0c1cd6c3b9dceb7e6cb1a0981208d5b52d6ce6ac6f8e3081a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__549cd7ce9a04ee2501661f63741d963e7f08f752613bb945465372da6fe5dba9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__465f1d8025b0f68cddac22d71793c763f95ddbe4a4dacd15f43d86226c2dd0ce(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd7067cfcba444cc23c82b086dc81761230d6875f5c55b910b518e75db69da7a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a83fe549e19ff4985232f000e3a9a52a2f4394e145d063734971595234b7deb5(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2df057e3895c7691a4b1d05e2b49f94e650609ee3455c4bee6ac02d0b5685aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97b74e18cd37b087c03540f7fb903268e3059df7b211e150dfc2b8baec95e878(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e87f19555624d9c7632ff04870f5b1ce7c1672cbf4fb073743500338820e8b56(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddd961c7b0f82c52246e615598ef0b5c1adf5305475f9876c353e29b6a005ee6(
    *,
    keytab: typing.Union[GoogleDataprocMetastoreServiceHiveMetastoreConfigKerberosConfigKeytab, typing.Dict[builtins.str, typing.Any]],
    krb5_config_gcs_uri: builtins.str,
    principal: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4908f18a51c487b9b8c14658167c6a15049817018e96e418febd27214b92451(
    *,
    cloud_secret: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__873274fe635d4b41279d628a4c687e85bfebf3c011a92c5b134448f4bf67b022(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a3e5cb13c916d2a66319f774cbb63cac37b47a25a60f4905f814dc63ae923c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb9f9b2ed9a71a7d208b84f7fe9c535231b4b14de9f862780be15782136162b0(
    value: typing.Optional[GoogleDataprocMetastoreServiceHiveMetastoreConfigKerberosConfigKeytab],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a126d6714579c9cd01f8d516debcfa9b89ca03fd67b074e8b65b3f455f725277(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bef5ec44a4615dc5a00b07fa2f89ba101a340e815243ebc25164df57803f4756(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__307a68775a88497ef7c6b525e9ffa6c33cdebe2ab27e8c8b9660241c6a0ad68e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f922d57325bdd9d5a32e63313b6aa4f6996a2ca11942f6116dd3f2eafb4152ce(
    value: typing.Optional[GoogleDataprocMetastoreServiceHiveMetastoreConfigKerberosConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f430bd2ec2735b1879cad752cf81455e6ec44fcb27990fa5dd11b745241d685(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfee40a69069a6f94b4ffdbce1f40908ecc415e2ef19bf0568093e575dfdd9b9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataprocMetastoreServiceHiveMetastoreConfigAuxiliaryVersions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b68e7c6f611f80d326c8e2c7f08ae28d3e2ea2d4763912d002150f506c453e6(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2a273e387ed18caa28f05b2b8892d05210c9c5ed25857e5ca18fe6c51b717f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__990c056ad90144268449f81642c0e0ed6c33a697fc04a7065662dce7425f4e23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a8f93a46ec19699bc9f754e7fb36973d8b6f990cc4e248e7bbf07b15406b726(
    value: typing.Optional[GoogleDataprocMetastoreServiceHiveMetastoreConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__484694657027df6e95142448cc7ebebc79f2b21f14fb805a5f02eca8732c6ec0(
    *,
    day_of_week: builtins.str,
    hour_of_day: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8074b8411befe64df941411a75176d363d274fea0972cc1474a582e36bbcf77d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41801eb838b6c3ea41f4fce13599555e654cd314767d83eecd4907729b58e63b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e63554921a85c9f9572849728e3599ea6640cdb8f46c4c6262bb66dfffd4166(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ccc24710ce2c8470398d5e7acb2298491cc57c2da7621a2969cbed880998eba(
    value: typing.Optional[GoogleDataprocMetastoreServiceMaintenanceWindow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__520a136aee43276d6020d3d8ffb335bdf64cb0f9ea4dba5da967ef5cc5087ca1(
    *,
    data_catalog_config: typing.Union[GoogleDataprocMetastoreServiceMetadataIntegrationDataCatalogConfig, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0b925f708d252f0e7df94f052017f5c399ef63a125e5f3c172bb1753354318f(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddee1dbe77f35b36a0bb97545fd96816d727b65dc259cd7adf5f6b0d15b72690(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__248861b9c731b5d938ae6183ff6a57191f61b511b26cf04d6c0dc64e421eb436(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26dfa3c27dd557217f9119064985e7a1b76657cb7048e91f41932c74bd02bc30(
    value: typing.Optional[GoogleDataprocMetastoreServiceMetadataIntegrationDataCatalogConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ab46b515fb01d9519a6a8676d8b6af1b13354e726da3a9e1e077710e5946e71(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca2cafcaa01420e953fb6ac9848a9767dd40e964b2365ea05a57c17ba49e071b(
    value: typing.Optional[GoogleDataprocMetastoreServiceMetadataIntegration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__715c11af667637bbabd13a8ea78c99d922b89582f4097c5786879e101f1e24f7(
    *,
    consumers: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataprocMetastoreServiceNetworkConfigConsumers, typing.Dict[builtins.str, typing.Any]]]],
    custom_routes_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c650e847eda4c4929b929ca79080c99544d951ecbb18abc2c3c76185bb0cf730(
    *,
    subnetwork: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a981f5d563b1238692db67b2333f136e6f07f933d6be243d47bda5e8cc504de4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fd279ae392ce5fac2729423cb0c18dcde30352e5bb812f44db4dc74305e092f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d07296e24cac35951a4ae21d6e128c1c5d3dbc0b1a15333b3a8825fe4619bb67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48fdebbefab07bc870d1903ba22e3a80d10afc547539c61affd41ad606dad6ef(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4c958bf76348fa3cf0e05f43c19eb54dcae64b78341654f7cf11f2dff716e03(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8026d5464fe48d03fe521392dbe0731addbdd6fa4f536f09f463f4a12ffcfe38(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocMetastoreServiceNetworkConfigConsumers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e17cd90b4bfecfc55b245acaf20d8eb9971ad4ce99acfcc1ff49ec7b5290fa94(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2755c16066e5a11551584afadd2252124ab07e8b17dd07f104a712240c62279(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5486c6d6b85982e082622db23ade26872cb3c8e589921bd4f7f13493d653741c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocMetastoreServiceNetworkConfigConsumers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afd62df96f9ac3f5dd0ea1b4d0998f30c930beb6ce1b89d63ee7702223c77e1d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cd3173e2db7e04b8d72619f20bdde6cc29ff995b759e4a19ce4d6dca2c85bac(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataprocMetastoreServiceNetworkConfigConsumers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba70a490fcbae8446893ce4b5cfa8a57a4d6ce434104c14f1547caddd89d6db3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__609e9fb204f438f45984f3ea3d775004ad1d188903be06ea19b97cd65bfd0075(
    value: typing.Optional[GoogleDataprocMetastoreServiceNetworkConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__482acde6f03e1f2f31e18869f41396fd590fd1279f6f368c8cdce18600710831(
    *,
    autoscaling_config: typing.Optional[typing.Union[GoogleDataprocMetastoreServiceScalingConfigAutoscalingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    instance_size: typing.Optional[builtins.str] = None,
    scaling_factor: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa57425d4a06bc4075f0890e9fd86e9b8c81daa3262143189fd96105a7716f56(
    *,
    autoscaling_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    limit_config: typing.Optional[typing.Union[GoogleDataprocMetastoreServiceScalingConfigAutoscalingConfigLimitConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__086f3bb5a898890b808fd39f876b58ac2d0a8cc36b2fee5eabc4524004b0fb8b(
    *,
    max_scaling_factor: typing.Optional[jsii.Number] = None,
    min_scaling_factor: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__418293b5a8820a1e361e2373e6b79dc90fcb39275c3b7cb129da518e22c6f45e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de4b2475e3749cea6d32f38fd1aace8d913d94ba2a711e5baac5a6b622a5681f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__986b3e14d3da9ffa95efd8915d866a26f7cc1d1b097c39c4b16d110f5926fe65(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68825e6173eef4cca20a41518816601087a13f2d345eadfb01934b6074502eec(
    value: typing.Optional[GoogleDataprocMetastoreServiceScalingConfigAutoscalingConfigLimitConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__039ac61584486ef53c99e0fb8cf9096fb1a5d32999eedafdfd2be074c6aacd02(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c708d49c5795e8d24befb08f75b42fa7cf4021f72d99b6e32e49d1947e9af3e6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4ccae37313ed4a5dd97de8039d0f9cf7c16279fa556cdb60de9dfa596393986(
    value: typing.Optional[GoogleDataprocMetastoreServiceScalingConfigAutoscalingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd4ee3b788885020c0c35e7d495034126579751566e40ae04705cd758b99beaa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__735daa7f72ea084832ec903897eb359da2f8c67c06d27098603f79f813b4aa1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1572c7e604f29270a41cb7a2ce8250d4eaf73d58f2ef70d3eb4cc16ff13d7399(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c632df4f1c1d97c324807c4b785d642029096a454d06cce582e20e307271c4c9(
    value: typing.Optional[GoogleDataprocMetastoreServiceScalingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9ca7c18704e50afdc3398e64e6606b1382104602e9338a31b651ace94fc3a83(
    *,
    backup_location: builtins.str,
    cron_schedule: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    time_zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae935739ff64c77f8533be2e857a287c5a0829bd22381fe5bab5d8edc3ed15d9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb5d2ca8d19d261849664c25124cf79def0c51c28c16dbe952e591dfc00d96a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__104f366866df4d0bc6d67c91d12632fcd639f95499acf3ee35e096e13e87d7ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e434ac47087f6b6108948719e98669c0ab17190d46cb48d59a7d328a950300c7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__950d7f84557bd9d491b4d9e8e939fde83bc6367026ebc330acf20bf5af4236e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86219b1c335d905b2ce5caa376880a5a8640d6b44666246b20510cbeaa1f2249(
    value: typing.Optional[GoogleDataprocMetastoreServiceScheduledBackup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d68847a9680009fa4132c7011c614d4c796f9ae85f4d8fa6b63b9bf1ead9d722(
    *,
    log_format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__678e1ba0cbcb0fbd7108534a97cd7b93848a44f303e5b09c900a9528bf57e515(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7194e82c4631fbcb44bdc74fde511aed59a3f0a0145f02dd17b051adf1caa2b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b354609fb7fc00483183b034367834e8611d3fa6dafabc975b08d67362ac43b8(
    value: typing.Optional[GoogleDataprocMetastoreServiceTelemetryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__786d29cf86067242546b3b5ea859ed1843606df5f0a6a6e6b95cfbe01a13b3b7(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab6382eb7c1a0c61fd6457de85fd85a7a032a2c068c63391267ca390412424ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35dc2411c3ee2e47b7cd73b4d92aaeb907c6ccac92877fcbb46823e72a210f04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15d3faa5cccec7385f6040bd81154b4ce1a10403f70921f4e659021b382f9b95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7e9e3004d5b781d8cf11220e54aa6bca57c897de2afde0cd1204b8a4e80ed75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d72699f5cf06ccbd1487a26110a5035ed5cfc4b2fe1950103c4de383db0d134(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocMetastoreServiceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
