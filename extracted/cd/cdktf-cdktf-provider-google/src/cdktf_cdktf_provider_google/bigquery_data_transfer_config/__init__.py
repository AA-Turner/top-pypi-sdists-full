r'''
# `google_bigquery_data_transfer_config`

Refer to the Terraform Registry for docs: [`google_bigquery_data_transfer_config`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config).
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


class BigqueryDataTransferConfig(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryDataTransferConfig.BigqueryDataTransferConfig",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config google_bigquery_data_transfer_config}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        data_source_id: builtins.str,
        display_name: builtins.str,
        params: typing.Mapping[builtins.str, builtins.str],
        data_refresh_window_days: typing.Optional[jsii.Number] = None,
        destination_dataset_id: typing.Optional[builtins.str] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        email_preferences: typing.Optional[typing.Union["BigqueryDataTransferConfigEmailPreferences", typing.Dict[builtins.str, typing.Any]]] = None,
        encryption_configuration: typing.Optional[typing.Union["BigqueryDataTransferConfigEncryptionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        notification_pubsub_topic: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[builtins.str] = None,
        schedule_options: typing.Optional[typing.Union["BigqueryDataTransferConfigScheduleOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        sensitive_params: typing.Optional[typing.Union["BigqueryDataTransferConfigSensitiveParams", typing.Dict[builtins.str, typing.Any]]] = None,
        service_account_name: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["BigqueryDataTransferConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config google_bigquery_data_transfer_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param data_source_id: The data source id. Cannot be changed once the transfer config is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#data_source_id BigqueryDataTransferConfig#data_source_id}
        :param display_name: The user specified display name for the transfer config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#display_name BigqueryDataTransferConfig#display_name}
        :param params: Parameters specific to each data source. For more information see the bq tab in the 'Setting up a data transfer' section for each data source. For example the parameters for Cloud Storage transfers are listed here: https://cloud.google.com/bigquery-transfer/docs/cloud-storage-transfer#bq **NOTE** : If you are attempting to update a parameter that cannot be updated (due to api limitations) `please force recreation of the resource <https://www.terraform.io/cli/state/taint#forcing-re-creation-of-resources>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#params BigqueryDataTransferConfig#params}
        :param data_refresh_window_days: The number of days to look back to automatically refresh the data. For example, if dataRefreshWindowDays = 10, then every day BigQuery reingests data for [today-10, today-1], rather than ingesting data for just [today-1]. Only valid if the data source supports the feature. Set the value to 0 to use the default value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#data_refresh_window_days BigqueryDataTransferConfig#data_refresh_window_days}
        :param destination_dataset_id: The BigQuery target dataset id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#destination_dataset_id BigqueryDataTransferConfig#destination_dataset_id}
        :param disabled: When set to true, no runs are scheduled for a given transfer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#disabled BigqueryDataTransferConfig#disabled}
        :param email_preferences: email_preferences block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#email_preferences BigqueryDataTransferConfig#email_preferences}
        :param encryption_configuration: encryption_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#encryption_configuration BigqueryDataTransferConfig#encryption_configuration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#id BigqueryDataTransferConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param location: The geographic location where the transfer config should reside. Examples: US, EU, asia-northeast1. The default value is US. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#location BigqueryDataTransferConfig#location}
        :param notification_pubsub_topic: Pub/Sub topic where notifications will be sent after transfer runs associated with this transfer config finish. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#notification_pubsub_topic BigqueryDataTransferConfig#notification_pubsub_topic}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#project BigqueryDataTransferConfig#project}.
        :param schedule: Data transfer schedule. If the data source does not support a custom schedule, this should be empty. If it is empty, the default value for the data source will be used. The specified times are in UTC. Examples of valid format: 1st,3rd monday of month 15:30, every wed,fri of jan, jun 13:15, and first sunday of quarter 00:00. See more explanation about the format here: https://cloud.google.com/appengine/docs/flexible/python/scheduling-jobs-with-cron-yaml#the_schedule_format NOTE: The minimum interval time between recurring transfers depends on the data source; refer to the documentation for your data source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#schedule BigqueryDataTransferConfig#schedule}
        :param schedule_options: schedule_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#schedule_options BigqueryDataTransferConfig#schedule_options}
        :param sensitive_params: sensitive_params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#sensitive_params BigqueryDataTransferConfig#sensitive_params}
        :param service_account_name: Service account email. If this field is set, transfer config will be created with this service account credentials. It requires that requesting user calling this API has permissions to act as this service account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#service_account_name BigqueryDataTransferConfig#service_account_name}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#timeouts BigqueryDataTransferConfig#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ce5c5f72d7da49fee4b30f16a923322c87c24e3f10abe6f6aaf4de011d3dd4e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = BigqueryDataTransferConfigConfig(
            data_source_id=data_source_id,
            display_name=display_name,
            params=params,
            data_refresh_window_days=data_refresh_window_days,
            destination_dataset_id=destination_dataset_id,
            disabled=disabled,
            email_preferences=email_preferences,
            encryption_configuration=encryption_configuration,
            id=id,
            location=location,
            notification_pubsub_topic=notification_pubsub_topic,
            project=project,
            schedule=schedule,
            schedule_options=schedule_options,
            sensitive_params=sensitive_params,
            service_account_name=service_account_name,
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
        '''Generates CDKTF code for importing a BigqueryDataTransferConfig resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the BigqueryDataTransferConfig to import.
        :param import_from_id: The id of the existing BigqueryDataTransferConfig that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the BigqueryDataTransferConfig to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__061b2c860ae4419df30312a4e535cab10a1ad180f1c5818509a95b8a6c53e520)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEmailPreferences")
    def put_email_preferences(
        self,
        *,
        enable_failure_email: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enable_failure_email: If true, email notifications will be sent on transfer run failures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#enable_failure_email BigqueryDataTransferConfig#enable_failure_email}
        '''
        value = BigqueryDataTransferConfigEmailPreferences(
            enable_failure_email=enable_failure_email
        )

        return typing.cast(None, jsii.invoke(self, "putEmailPreferences", [value]))

    @jsii.member(jsii_name="putEncryptionConfiguration")
    def put_encryption_configuration(self, *, kms_key_name: builtins.str) -> None:
        '''
        :param kms_key_name: The name of the KMS key used for encrypting BigQuery data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#kms_key_name BigqueryDataTransferConfig#kms_key_name}
        '''
        value = BigqueryDataTransferConfigEncryptionConfiguration(
            kms_key_name=kms_key_name
        )

        return typing.cast(None, jsii.invoke(self, "putEncryptionConfiguration", [value]))

    @jsii.member(jsii_name="putScheduleOptions")
    def put_schedule_options(
        self,
        *,
        disable_auto_scheduling: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        end_time: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disable_auto_scheduling: If true, automatic scheduling of data transfer runs for this configuration will be disabled. The runs can be started on ad-hoc basis using transferConfigs.startManualRuns API. When automatic scheduling is disabled, the TransferConfig.schedule field will be ignored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#disable_auto_scheduling BigqueryDataTransferConfig#disable_auto_scheduling}
        :param end_time: Defines time to stop scheduling transfer runs. A transfer run cannot be scheduled at or after the end time. The end time can be changed at any moment. The time when a data transfer can be triggered manually is not limited by this option. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#end_time BigqueryDataTransferConfig#end_time}
        :param start_time: Specifies time to start scheduling transfer runs. The first run will be scheduled at or after the start time according to a recurrence pattern defined in the schedule string. The start time can be changed at any moment. The time when a data transfer can be triggered manually is not limited by this option. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#start_time BigqueryDataTransferConfig#start_time}
        '''
        value = BigqueryDataTransferConfigScheduleOptions(
            disable_auto_scheduling=disable_auto_scheduling,
            end_time=end_time,
            start_time=start_time,
        )

        return typing.cast(None, jsii.invoke(self, "putScheduleOptions", [value]))

    @jsii.member(jsii_name="putSensitiveParams")
    def put_sensitive_params(
        self,
        *,
        secret_access_key: typing.Optional[builtins.str] = None,
        secret_access_key_wo: typing.Optional[builtins.str] = None,
        secret_access_key_wo_version: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param secret_access_key: The Secret Access Key of the AWS account transferring data from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#secret_access_key BigqueryDataTransferConfig#secret_access_key}
        :param secret_access_key_wo: The Secret Access Key of the AWS account transferring data from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#secret_access_key_wo BigqueryDataTransferConfig#secret_access_key_wo}
        :param secret_access_key_wo_version: The version of the sensitive params - used to trigger updates of the write-only params. For more info see `updating write-only attributes </docs/providers/google/guides/using_write_only_attributes.html#updating-write-only-attributes>`_ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#secret_access_key_wo_version BigqueryDataTransferConfig#secret_access_key_wo_version}
        '''
        value = BigqueryDataTransferConfigSensitiveParams(
            secret_access_key=secret_access_key,
            secret_access_key_wo=secret_access_key_wo,
            secret_access_key_wo_version=secret_access_key_wo_version,
        )

        return typing.cast(None, jsii.invoke(self, "putSensitiveParams", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#create BigqueryDataTransferConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#delete BigqueryDataTransferConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#update BigqueryDataTransferConfig#update}.
        '''
        value = BigqueryDataTransferConfigTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDataRefreshWindowDays")
    def reset_data_refresh_window_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataRefreshWindowDays", []))

    @jsii.member(jsii_name="resetDestinationDatasetId")
    def reset_destination_dataset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationDatasetId", []))

    @jsii.member(jsii_name="resetDisabled")
    def reset_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisabled", []))

    @jsii.member(jsii_name="resetEmailPreferences")
    def reset_email_preferences(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailPreferences", []))

    @jsii.member(jsii_name="resetEncryptionConfiguration")
    def reset_encryption_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionConfiguration", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetNotificationPubsubTopic")
    def reset_notification_pubsub_topic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotificationPubsubTopic", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetSchedule")
    def reset_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchedule", []))

    @jsii.member(jsii_name="resetScheduleOptions")
    def reset_schedule_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheduleOptions", []))

    @jsii.member(jsii_name="resetSensitiveParams")
    def reset_sensitive_params(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSensitiveParams", []))

    @jsii.member(jsii_name="resetServiceAccountName")
    def reset_service_account_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccountName", []))

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
    @jsii.member(jsii_name="emailPreferences")
    def email_preferences(
        self,
    ) -> "BigqueryDataTransferConfigEmailPreferencesOutputReference":
        return typing.cast("BigqueryDataTransferConfigEmailPreferencesOutputReference", jsii.get(self, "emailPreferences"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfiguration")
    def encryption_configuration(
        self,
    ) -> "BigqueryDataTransferConfigEncryptionConfigurationOutputReference":
        return typing.cast("BigqueryDataTransferConfigEncryptionConfigurationOutputReference", jsii.get(self, "encryptionConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="scheduleOptions")
    def schedule_options(
        self,
    ) -> "BigqueryDataTransferConfigScheduleOptionsOutputReference":
        return typing.cast("BigqueryDataTransferConfigScheduleOptionsOutputReference", jsii.get(self, "scheduleOptions"))

    @builtins.property
    @jsii.member(jsii_name="sensitiveParams")
    def sensitive_params(
        self,
    ) -> "BigqueryDataTransferConfigSensitiveParamsOutputReference":
        return typing.cast("BigqueryDataTransferConfigSensitiveParamsOutputReference", jsii.get(self, "sensitiveParams"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "BigqueryDataTransferConfigTimeoutsOutputReference":
        return typing.cast("BigqueryDataTransferConfigTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="dataRefreshWindowDaysInput")
    def data_refresh_window_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dataRefreshWindowDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceIdInput")
    def data_source_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataSourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationDatasetIdInput")
    def destination_dataset_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationDatasetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="disabledInput")
    def disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disabledInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="emailPreferencesInput")
    def email_preferences_input(
        self,
    ) -> typing.Optional["BigqueryDataTransferConfigEmailPreferences"]:
        return typing.cast(typing.Optional["BigqueryDataTransferConfigEmailPreferences"], jsii.get(self, "emailPreferencesInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfigurationInput")
    def encryption_configuration_input(
        self,
    ) -> typing.Optional["BigqueryDataTransferConfigEncryptionConfiguration"]:
        return typing.cast(typing.Optional["BigqueryDataTransferConfigEncryptionConfiguration"], jsii.get(self, "encryptionConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationPubsubTopicInput")
    def notification_pubsub_topic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notificationPubsubTopicInput"))

    @builtins.property
    @jsii.member(jsii_name="paramsInput")
    def params_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "paramsInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleOptionsInput")
    def schedule_options_input(
        self,
    ) -> typing.Optional["BigqueryDataTransferConfigScheduleOptions"]:
        return typing.cast(typing.Optional["BigqueryDataTransferConfigScheduleOptions"], jsii.get(self, "scheduleOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="sensitiveParamsInput")
    def sensitive_params_input(
        self,
    ) -> typing.Optional["BigqueryDataTransferConfigSensitiveParams"]:
        return typing.cast(typing.Optional["BigqueryDataTransferConfigSensitiveParams"], jsii.get(self, "sensitiveParamsInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountNameInput")
    def service_account_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountNameInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BigqueryDataTransferConfigTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BigqueryDataTransferConfigTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="dataRefreshWindowDays")
    def data_refresh_window_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dataRefreshWindowDays"))

    @data_refresh_window_days.setter
    def data_refresh_window_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f2e7d6fc029bddff272b87a7c742ee880737944ae1a65329b5711d955b16a7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataRefreshWindowDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataSourceId")
    def data_source_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataSourceId"))

    @data_source_id.setter
    def data_source_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ff11e2885c25d012bc91f7ae7acd0f150b5fbf90a575a5c9ee8b69ed96caa3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataSourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destinationDatasetId")
    def destination_dataset_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationDatasetId"))

    @destination_dataset_id.setter
    def destination_dataset_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39b74f8a00f0a2298a1af34748f2a9278a72844539e9fa2b195d70dd086f6d69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationDatasetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disabled")
    def disabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disabled"))

    @disabled.setter
    def disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04ebab6a9fe044e2736ecb179185f757522e9e7f6037350fc5d3e79a0ae66d69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fd825eb23d30629ae27d1378506d0fa6d7bb1585f804326ba3b33fb1c197559)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__448ee582f7fb5394fe3038e029c0987073c0a4a56cc7ab599c8a7b477adcc51d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__527f7969c82b06cb1d9cfd86bfe5138ac0fd7603d9982a180b852a191cd73559)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notificationPubsubTopic")
    def notification_pubsub_topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notificationPubsubTopic"))

    @notification_pubsub_topic.setter
    def notification_pubsub_topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac52df80c117d81f734290b9d519f01e30cfe65bdb15c580c720c5bc171550e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationPubsubTopic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="params")
    def params(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "params"))

    @params.setter
    def params(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90430baf4a12816ce63c5fb48138ea273d878f09108237c7d06df5b0aac9ab77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "params", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aa0ecd2e379279b4bcf330838cc0f3527fad04b121a4efc1773c9f1d8fa8f1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schedule"))

    @schedule.setter
    def schedule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d8628cc88f9c612c5add3df4592579d5afd04441d7993c4d13e9f766b37eb78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccountName")
    def service_account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccountName"))

    @service_account_name.setter
    def service_account_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f066231e520c91912f47abe966e8269599a81b280d33a3cdf0364bd1573e66b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountName", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryDataTransferConfig.BigqueryDataTransferConfigConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "data_source_id": "dataSourceId",
        "display_name": "displayName",
        "params": "params",
        "data_refresh_window_days": "dataRefreshWindowDays",
        "destination_dataset_id": "destinationDatasetId",
        "disabled": "disabled",
        "email_preferences": "emailPreferences",
        "encryption_configuration": "encryptionConfiguration",
        "id": "id",
        "location": "location",
        "notification_pubsub_topic": "notificationPubsubTopic",
        "project": "project",
        "schedule": "schedule",
        "schedule_options": "scheduleOptions",
        "sensitive_params": "sensitiveParams",
        "service_account_name": "serviceAccountName",
        "timeouts": "timeouts",
    },
)
class BigqueryDataTransferConfigConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        data_source_id: builtins.str,
        display_name: builtins.str,
        params: typing.Mapping[builtins.str, builtins.str],
        data_refresh_window_days: typing.Optional[jsii.Number] = None,
        destination_dataset_id: typing.Optional[builtins.str] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        email_preferences: typing.Optional[typing.Union["BigqueryDataTransferConfigEmailPreferences", typing.Dict[builtins.str, typing.Any]]] = None,
        encryption_configuration: typing.Optional[typing.Union["BigqueryDataTransferConfigEncryptionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        notification_pubsub_topic: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[builtins.str] = None,
        schedule_options: typing.Optional[typing.Union["BigqueryDataTransferConfigScheduleOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        sensitive_params: typing.Optional[typing.Union["BigqueryDataTransferConfigSensitiveParams", typing.Dict[builtins.str, typing.Any]]] = None,
        service_account_name: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["BigqueryDataTransferConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param data_source_id: The data source id. Cannot be changed once the transfer config is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#data_source_id BigqueryDataTransferConfig#data_source_id}
        :param display_name: The user specified display name for the transfer config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#display_name BigqueryDataTransferConfig#display_name}
        :param params: Parameters specific to each data source. For more information see the bq tab in the 'Setting up a data transfer' section for each data source. For example the parameters for Cloud Storage transfers are listed here: https://cloud.google.com/bigquery-transfer/docs/cloud-storage-transfer#bq **NOTE** : If you are attempting to update a parameter that cannot be updated (due to api limitations) `please force recreation of the resource <https://www.terraform.io/cli/state/taint#forcing-re-creation-of-resources>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#params BigqueryDataTransferConfig#params}
        :param data_refresh_window_days: The number of days to look back to automatically refresh the data. For example, if dataRefreshWindowDays = 10, then every day BigQuery reingests data for [today-10, today-1], rather than ingesting data for just [today-1]. Only valid if the data source supports the feature. Set the value to 0 to use the default value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#data_refresh_window_days BigqueryDataTransferConfig#data_refresh_window_days}
        :param destination_dataset_id: The BigQuery target dataset id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#destination_dataset_id BigqueryDataTransferConfig#destination_dataset_id}
        :param disabled: When set to true, no runs are scheduled for a given transfer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#disabled BigqueryDataTransferConfig#disabled}
        :param email_preferences: email_preferences block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#email_preferences BigqueryDataTransferConfig#email_preferences}
        :param encryption_configuration: encryption_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#encryption_configuration BigqueryDataTransferConfig#encryption_configuration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#id BigqueryDataTransferConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param location: The geographic location where the transfer config should reside. Examples: US, EU, asia-northeast1. The default value is US. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#location BigqueryDataTransferConfig#location}
        :param notification_pubsub_topic: Pub/Sub topic where notifications will be sent after transfer runs associated with this transfer config finish. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#notification_pubsub_topic BigqueryDataTransferConfig#notification_pubsub_topic}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#project BigqueryDataTransferConfig#project}.
        :param schedule: Data transfer schedule. If the data source does not support a custom schedule, this should be empty. If it is empty, the default value for the data source will be used. The specified times are in UTC. Examples of valid format: 1st,3rd monday of month 15:30, every wed,fri of jan, jun 13:15, and first sunday of quarter 00:00. See more explanation about the format here: https://cloud.google.com/appengine/docs/flexible/python/scheduling-jobs-with-cron-yaml#the_schedule_format NOTE: The minimum interval time between recurring transfers depends on the data source; refer to the documentation for your data source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#schedule BigqueryDataTransferConfig#schedule}
        :param schedule_options: schedule_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#schedule_options BigqueryDataTransferConfig#schedule_options}
        :param sensitive_params: sensitive_params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#sensitive_params BigqueryDataTransferConfig#sensitive_params}
        :param service_account_name: Service account email. If this field is set, transfer config will be created with this service account credentials. It requires that requesting user calling this API has permissions to act as this service account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#service_account_name BigqueryDataTransferConfig#service_account_name}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#timeouts BigqueryDataTransferConfig#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(email_preferences, dict):
            email_preferences = BigqueryDataTransferConfigEmailPreferences(**email_preferences)
        if isinstance(encryption_configuration, dict):
            encryption_configuration = BigqueryDataTransferConfigEncryptionConfiguration(**encryption_configuration)
        if isinstance(schedule_options, dict):
            schedule_options = BigqueryDataTransferConfigScheduleOptions(**schedule_options)
        if isinstance(sensitive_params, dict):
            sensitive_params = BigqueryDataTransferConfigSensitiveParams(**sensitive_params)
        if isinstance(timeouts, dict):
            timeouts = BigqueryDataTransferConfigTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ffb0e22d8c4adea91922889705a0be32220f7f6cbf6d2d7f815b82286c0db3f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument data_source_id", value=data_source_id, expected_type=type_hints["data_source_id"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument params", value=params, expected_type=type_hints["params"])
            check_type(argname="argument data_refresh_window_days", value=data_refresh_window_days, expected_type=type_hints["data_refresh_window_days"])
            check_type(argname="argument destination_dataset_id", value=destination_dataset_id, expected_type=type_hints["destination_dataset_id"])
            check_type(argname="argument disabled", value=disabled, expected_type=type_hints["disabled"])
            check_type(argname="argument email_preferences", value=email_preferences, expected_type=type_hints["email_preferences"])
            check_type(argname="argument encryption_configuration", value=encryption_configuration, expected_type=type_hints["encryption_configuration"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument notification_pubsub_topic", value=notification_pubsub_topic, expected_type=type_hints["notification_pubsub_topic"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument schedule_options", value=schedule_options, expected_type=type_hints["schedule_options"])
            check_type(argname="argument sensitive_params", value=sensitive_params, expected_type=type_hints["sensitive_params"])
            check_type(argname="argument service_account_name", value=service_account_name, expected_type=type_hints["service_account_name"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_source_id": data_source_id,
            "display_name": display_name,
            "params": params,
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
        if data_refresh_window_days is not None:
            self._values["data_refresh_window_days"] = data_refresh_window_days
        if destination_dataset_id is not None:
            self._values["destination_dataset_id"] = destination_dataset_id
        if disabled is not None:
            self._values["disabled"] = disabled
        if email_preferences is not None:
            self._values["email_preferences"] = email_preferences
        if encryption_configuration is not None:
            self._values["encryption_configuration"] = encryption_configuration
        if id is not None:
            self._values["id"] = id
        if location is not None:
            self._values["location"] = location
        if notification_pubsub_topic is not None:
            self._values["notification_pubsub_topic"] = notification_pubsub_topic
        if project is not None:
            self._values["project"] = project
        if schedule is not None:
            self._values["schedule"] = schedule
        if schedule_options is not None:
            self._values["schedule_options"] = schedule_options
        if sensitive_params is not None:
            self._values["sensitive_params"] = sensitive_params
        if service_account_name is not None:
            self._values["service_account_name"] = service_account_name
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
    def data_source_id(self) -> builtins.str:
        '''The data source id. Cannot be changed once the transfer config is created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#data_source_id BigqueryDataTransferConfig#data_source_id}
        '''
        result = self._values.get("data_source_id")
        assert result is not None, "Required property 'data_source_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''The user specified display name for the transfer config.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#display_name BigqueryDataTransferConfig#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def params(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''Parameters specific to each data source.

        For more information see the bq tab in the 'Setting up a data transfer'
        section for each data source. For example the parameters for Cloud Storage transfers are listed here:
        https://cloud.google.com/bigquery-transfer/docs/cloud-storage-transfer#bq

        **NOTE** : If you are attempting to update a parameter that cannot be updated (due to api limitations) `please force recreation of the resource <https://www.terraform.io/cli/state/taint#forcing-re-creation-of-resources>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#params BigqueryDataTransferConfig#params}
        '''
        result = self._values.get("params")
        assert result is not None, "Required property 'params' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    @builtins.property
    def data_refresh_window_days(self) -> typing.Optional[jsii.Number]:
        '''The number of days to look back to automatically refresh the data.

        For example, if dataRefreshWindowDays = 10, then every day BigQuery
        reingests data for [today-10, today-1], rather than ingesting data for
        just [today-1]. Only valid if the data source supports the feature.
        Set the value to 0 to use the default value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#data_refresh_window_days BigqueryDataTransferConfig#data_refresh_window_days}
        '''
        result = self._values.get("data_refresh_window_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def destination_dataset_id(self) -> typing.Optional[builtins.str]:
        '''The BigQuery target dataset id.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#destination_dataset_id BigqueryDataTransferConfig#destination_dataset_id}
        '''
        result = self._values.get("destination_dataset_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When set to true, no runs are scheduled for a given transfer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#disabled BigqueryDataTransferConfig#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def email_preferences(
        self,
    ) -> typing.Optional["BigqueryDataTransferConfigEmailPreferences"]:
        '''email_preferences block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#email_preferences BigqueryDataTransferConfig#email_preferences}
        '''
        result = self._values.get("email_preferences")
        return typing.cast(typing.Optional["BigqueryDataTransferConfigEmailPreferences"], result)

    @builtins.property
    def encryption_configuration(
        self,
    ) -> typing.Optional["BigqueryDataTransferConfigEncryptionConfiguration"]:
        '''encryption_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#encryption_configuration BigqueryDataTransferConfig#encryption_configuration}
        '''
        result = self._values.get("encryption_configuration")
        return typing.cast(typing.Optional["BigqueryDataTransferConfigEncryptionConfiguration"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#id BigqueryDataTransferConfig#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The geographic location where the transfer config should reside. Examples: US, EU, asia-northeast1. The default value is US.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#location BigqueryDataTransferConfig#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_pubsub_topic(self) -> typing.Optional[builtins.str]:
        '''Pub/Sub topic where notifications will be sent after transfer runs associated with this transfer config finish.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#notification_pubsub_topic BigqueryDataTransferConfig#notification_pubsub_topic}
        '''
        result = self._values.get("notification_pubsub_topic")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#project BigqueryDataTransferConfig#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule(self) -> typing.Optional[builtins.str]:
        '''Data transfer schedule.

        If the data source does not support a custom
        schedule, this should be empty. If it is empty, the default value for
        the data source will be used. The specified times are in UTC. Examples
        of valid format: 1st,3rd monday of month 15:30, every wed,fri of jan,
        jun 13:15, and first sunday of quarter 00:00. See more explanation
        about the format here:
        https://cloud.google.com/appengine/docs/flexible/python/scheduling-jobs-with-cron-yaml#the_schedule_format
        NOTE: The minimum interval time between recurring transfers depends
        on the data source; refer to the documentation for your data source.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#schedule BigqueryDataTransferConfig#schedule}
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule_options(
        self,
    ) -> typing.Optional["BigqueryDataTransferConfigScheduleOptions"]:
        '''schedule_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#schedule_options BigqueryDataTransferConfig#schedule_options}
        '''
        result = self._values.get("schedule_options")
        return typing.cast(typing.Optional["BigqueryDataTransferConfigScheduleOptions"], result)

    @builtins.property
    def sensitive_params(
        self,
    ) -> typing.Optional["BigqueryDataTransferConfigSensitiveParams"]:
        '''sensitive_params block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#sensitive_params BigqueryDataTransferConfig#sensitive_params}
        '''
        result = self._values.get("sensitive_params")
        return typing.cast(typing.Optional["BigqueryDataTransferConfigSensitiveParams"], result)

    @builtins.property
    def service_account_name(self) -> typing.Optional[builtins.str]:
        '''Service account email.

        If this field is set, transfer config will
        be created with this service account credentials. It requires that
        requesting user calling this API has permissions to act as this service account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#service_account_name BigqueryDataTransferConfig#service_account_name}
        '''
        result = self._values.get("service_account_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["BigqueryDataTransferConfigTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#timeouts BigqueryDataTransferConfig#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["BigqueryDataTransferConfigTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryDataTransferConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryDataTransferConfig.BigqueryDataTransferConfigEmailPreferences",
    jsii_struct_bases=[],
    name_mapping={"enable_failure_email": "enableFailureEmail"},
)
class BigqueryDataTransferConfigEmailPreferences:
    def __init__(
        self,
        *,
        enable_failure_email: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enable_failure_email: If true, email notifications will be sent on transfer run failures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#enable_failure_email BigqueryDataTransferConfig#enable_failure_email}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20f0eb2dc01087dc23a5e3067f3dec27cac24001117fc324571ebc18af7e2c56)
            check_type(argname="argument enable_failure_email", value=enable_failure_email, expected_type=type_hints["enable_failure_email"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enable_failure_email": enable_failure_email,
        }

    @builtins.property
    def enable_failure_email(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''If true, email notifications will be sent on transfer run failures.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#enable_failure_email BigqueryDataTransferConfig#enable_failure_email}
        '''
        result = self._values.get("enable_failure_email")
        assert result is not None, "Required property 'enable_failure_email' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryDataTransferConfigEmailPreferences(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryDataTransferConfigEmailPreferencesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryDataTransferConfig.BigqueryDataTransferConfigEmailPreferencesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2d6f201549467267f29432aa59e8e8e39227873982e05d24ff2ea903c6e6ba5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="enableFailureEmailInput")
    def enable_failure_email_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableFailureEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="enableFailureEmail")
    def enable_failure_email(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableFailureEmail"))

    @enable_failure_email.setter
    def enable_failure_email(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49cc43a71a7a64ff401bf8dfb443b187931146ac05ae5c9e271afb50401ed788)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableFailureEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BigqueryDataTransferConfigEmailPreferences]:
        return typing.cast(typing.Optional[BigqueryDataTransferConfigEmailPreferences], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryDataTransferConfigEmailPreferences],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__859c528078ecefdc50487be112b7dd04345658e5ec11ba962a4341e6eeb1a300)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryDataTransferConfig.BigqueryDataTransferConfigEncryptionConfiguration",
    jsii_struct_bases=[],
    name_mapping={"kms_key_name": "kmsKeyName"},
)
class BigqueryDataTransferConfigEncryptionConfiguration:
    def __init__(self, *, kms_key_name: builtins.str) -> None:
        '''
        :param kms_key_name: The name of the KMS key used for encrypting BigQuery data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#kms_key_name BigqueryDataTransferConfig#kms_key_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fef28bb292bc36fdc3e1b0a5033c692933c0cb16dac67bb74c93727a5320a57f)
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kms_key_name": kms_key_name,
        }

    @builtins.property
    def kms_key_name(self) -> builtins.str:
        '''The name of the KMS key used for encrypting BigQuery data.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#kms_key_name BigqueryDataTransferConfig#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        assert result is not None, "Required property 'kms_key_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryDataTransferConfigEncryptionConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryDataTransferConfigEncryptionConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryDataTransferConfig.BigqueryDataTransferConfigEncryptionConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bb5f832e9c275cfcdbf02169563f58688073cef6e49012a3742d5b7e87ece55)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="kmsKeyNameInput")
    def kms_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__233bdc72a3c0986620a4a10c990066e8ac5f90a37882d1ce80112a1c1838a1f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BigqueryDataTransferConfigEncryptionConfiguration]:
        return typing.cast(typing.Optional[BigqueryDataTransferConfigEncryptionConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryDataTransferConfigEncryptionConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__947e389f327e2fcfd3e7e9a1e2ff68b93db8d442fd807a2779f848bcc462b736)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryDataTransferConfig.BigqueryDataTransferConfigScheduleOptions",
    jsii_struct_bases=[],
    name_mapping={
        "disable_auto_scheduling": "disableAutoScheduling",
        "end_time": "endTime",
        "start_time": "startTime",
    },
)
class BigqueryDataTransferConfigScheduleOptions:
    def __init__(
        self,
        *,
        disable_auto_scheduling: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        end_time: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disable_auto_scheduling: If true, automatic scheduling of data transfer runs for this configuration will be disabled. The runs can be started on ad-hoc basis using transferConfigs.startManualRuns API. When automatic scheduling is disabled, the TransferConfig.schedule field will be ignored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#disable_auto_scheduling BigqueryDataTransferConfig#disable_auto_scheduling}
        :param end_time: Defines time to stop scheduling transfer runs. A transfer run cannot be scheduled at or after the end time. The end time can be changed at any moment. The time when a data transfer can be triggered manually is not limited by this option. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#end_time BigqueryDataTransferConfig#end_time}
        :param start_time: Specifies time to start scheduling transfer runs. The first run will be scheduled at or after the start time according to a recurrence pattern defined in the schedule string. The start time can be changed at any moment. The time when a data transfer can be triggered manually is not limited by this option. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#start_time BigqueryDataTransferConfig#start_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13f79c62d2c3aaa5dc82238fa7b3bd835543155f4b1621109bc0c46bc34fe6fb)
            check_type(argname="argument disable_auto_scheduling", value=disable_auto_scheduling, expected_type=type_hints["disable_auto_scheduling"])
            check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disable_auto_scheduling is not None:
            self._values["disable_auto_scheduling"] = disable_auto_scheduling
        if end_time is not None:
            self._values["end_time"] = end_time
        if start_time is not None:
            self._values["start_time"] = start_time

    @builtins.property
    def disable_auto_scheduling(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, automatic scheduling of data transfer runs for this configuration will be disabled.

        The runs can be started on ad-hoc
        basis using transferConfigs.startManualRuns API. When automatic
        scheduling is disabled, the TransferConfig.schedule field will
        be ignored.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#disable_auto_scheduling BigqueryDataTransferConfig#disable_auto_scheduling}
        '''
        result = self._values.get("disable_auto_scheduling")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def end_time(self) -> typing.Optional[builtins.str]:
        '''Defines time to stop scheduling transfer runs.

        A transfer run cannot be
        scheduled at or after the end time. The end time can be changed at any
        moment. The time when a data transfer can be triggered manually is not
        limited by this option.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#end_time BigqueryDataTransferConfig#end_time}
        '''
        result = self._values.get("end_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        '''Specifies time to start scheduling transfer runs.

        The first run will be
        scheduled at or after the start time according to a recurrence pattern
        defined in the schedule string. The start time can be changed at any
        moment. The time when a data transfer can be triggered manually is not
        limited by this option.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#start_time BigqueryDataTransferConfig#start_time}
        '''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryDataTransferConfigScheduleOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryDataTransferConfigScheduleOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryDataTransferConfig.BigqueryDataTransferConfigScheduleOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__994b55521e07c795a3be105ed4c2d342854ff109eb7beb4ed3b023e8735662ce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDisableAutoScheduling")
    def reset_disable_auto_scheduling(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableAutoScheduling", []))

    @jsii.member(jsii_name="resetEndTime")
    def reset_end_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndTime", []))

    @jsii.member(jsii_name="resetStartTime")
    def reset_start_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartTime", []))

    @builtins.property
    @jsii.member(jsii_name="disableAutoSchedulingInput")
    def disable_auto_scheduling_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableAutoSchedulingInput"))

    @builtins.property
    @jsii.member(jsii_name="endTimeInput")
    def end_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="disableAutoScheduling")
    def disable_auto_scheduling(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableAutoScheduling"))

    @disable_auto_scheduling.setter
    def disable_auto_scheduling(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92649db922ce627c5ed610b65f58146c8b0d08e9cd216b24d3239b16fbcd8b79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableAutoScheduling", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTime"))

    @end_time.setter
    def end_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c85fbe72e143286214077352cb8d9c3a216ba394eedfbb65d07cb391cb71d14f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__334114df0296e9ca9fe2e96f6ec4d86f75adeb42a0e736322091f6bd5fccfd24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BigqueryDataTransferConfigScheduleOptions]:
        return typing.cast(typing.Optional[BigqueryDataTransferConfigScheduleOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryDataTransferConfigScheduleOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27e012c4fd64115735a4d7f2188b99f9abbdd4201ff889c30c32a7c6ce1b297e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryDataTransferConfig.BigqueryDataTransferConfigSensitiveParams",
    jsii_struct_bases=[],
    name_mapping={
        "secret_access_key": "secretAccessKey",
        "secret_access_key_wo": "secretAccessKeyWo",
        "secret_access_key_wo_version": "secretAccessKeyWoVersion",
    },
)
class BigqueryDataTransferConfigSensitiveParams:
    def __init__(
        self,
        *,
        secret_access_key: typing.Optional[builtins.str] = None,
        secret_access_key_wo: typing.Optional[builtins.str] = None,
        secret_access_key_wo_version: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param secret_access_key: The Secret Access Key of the AWS account transferring data from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#secret_access_key BigqueryDataTransferConfig#secret_access_key}
        :param secret_access_key_wo: The Secret Access Key of the AWS account transferring data from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#secret_access_key_wo BigqueryDataTransferConfig#secret_access_key_wo}
        :param secret_access_key_wo_version: The version of the sensitive params - used to trigger updates of the write-only params. For more info see `updating write-only attributes </docs/providers/google/guides/using_write_only_attributes.html#updating-write-only-attributes>`_ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#secret_access_key_wo_version BigqueryDataTransferConfig#secret_access_key_wo_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d11d7103971e3dc6e76809789a18de81f6b0bb38a9453871ba518d788e153e04)
            check_type(argname="argument secret_access_key", value=secret_access_key, expected_type=type_hints["secret_access_key"])
            check_type(argname="argument secret_access_key_wo", value=secret_access_key_wo, expected_type=type_hints["secret_access_key_wo"])
            check_type(argname="argument secret_access_key_wo_version", value=secret_access_key_wo_version, expected_type=type_hints["secret_access_key_wo_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if secret_access_key is not None:
            self._values["secret_access_key"] = secret_access_key
        if secret_access_key_wo is not None:
            self._values["secret_access_key_wo"] = secret_access_key_wo
        if secret_access_key_wo_version is not None:
            self._values["secret_access_key_wo_version"] = secret_access_key_wo_version

    @builtins.property
    def secret_access_key(self) -> typing.Optional[builtins.str]:
        '''The Secret Access Key of the AWS account transferring data from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#secret_access_key BigqueryDataTransferConfig#secret_access_key}
        '''
        result = self._values.get("secret_access_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_access_key_wo(self) -> typing.Optional[builtins.str]:
        '''The Secret Access Key of the AWS account transferring data from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#secret_access_key_wo BigqueryDataTransferConfig#secret_access_key_wo}
        '''
        result = self._values.get("secret_access_key_wo")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_access_key_wo_version(self) -> typing.Optional[jsii.Number]:
        '''The version of the sensitive params - used to trigger updates of the write-only params.

        For more info see `updating write-only attributes </docs/providers/google/guides/using_write_only_attributes.html#updating-write-only-attributes>`_

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#secret_access_key_wo_version BigqueryDataTransferConfig#secret_access_key_wo_version}
        '''
        result = self._values.get("secret_access_key_wo_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryDataTransferConfigSensitiveParams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryDataTransferConfigSensitiveParamsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryDataTransferConfig.BigqueryDataTransferConfigSensitiveParamsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9517484e7bc2c064f77d38df8f9b343e5d6506ce826cf66743d7ccb9098ce992)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSecretAccessKey")
    def reset_secret_access_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretAccessKey", []))

    @jsii.member(jsii_name="resetSecretAccessKeyWo")
    def reset_secret_access_key_wo(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretAccessKeyWo", []))

    @jsii.member(jsii_name="resetSecretAccessKeyWoVersion")
    def reset_secret_access_key_wo_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretAccessKeyWoVersion", []))

    @builtins.property
    @jsii.member(jsii_name="secretAccessKeyInput")
    def secret_access_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretAccessKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="secretAccessKeyWoInput")
    def secret_access_key_wo_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretAccessKeyWoInput"))

    @builtins.property
    @jsii.member(jsii_name="secretAccessKeyWoVersionInput")
    def secret_access_key_wo_version_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "secretAccessKeyWoVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="secretAccessKey")
    def secret_access_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretAccessKey"))

    @secret_access_key.setter
    def secret_access_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b077f64484b20ec1d29d52d81e63662167b965806ca735f94252e537d6860d36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretAccessKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretAccessKeyWo")
    def secret_access_key_wo(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretAccessKeyWo"))

    @secret_access_key_wo.setter
    def secret_access_key_wo(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba114477ae2c9f3bdc0b3984b61462f0e60b39c11b54c3bf675fcb467d78d90c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretAccessKeyWo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretAccessKeyWoVersion")
    def secret_access_key_wo_version(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "secretAccessKeyWoVersion"))

    @secret_access_key_wo_version.setter
    def secret_access_key_wo_version(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01cace08d03652cf79b82b3375973e8605002b3caba43283a02c5a38af84a2bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretAccessKeyWoVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BigqueryDataTransferConfigSensitiveParams]:
        return typing.cast(typing.Optional[BigqueryDataTransferConfigSensitiveParams], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryDataTransferConfigSensitiveParams],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e597a1ce3e7798e331fff389280450aa15a38ff97fefe0e9d81c9fb4feaa7513)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryDataTransferConfig.BigqueryDataTransferConfigTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class BigqueryDataTransferConfigTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#create BigqueryDataTransferConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#delete BigqueryDataTransferConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#update BigqueryDataTransferConfig#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4b19f6bc25e3b3bf664d2a36165dd4c20087761ca8e1e631fafa06f4f41614a)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#create BigqueryDataTransferConfig#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#delete BigqueryDataTransferConfig#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_data_transfer_config#update BigqueryDataTransferConfig#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryDataTransferConfigTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryDataTransferConfigTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryDataTransferConfig.BigqueryDataTransferConfigTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1254ec22a3aafa941c4bf39040f120da9c03389257df54c00ffdcd398687c62c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7743e7f893bfc041ea424229076e73d5a17a86f51070d8001bbeaa9fee0ce3d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72b7315db04f4d4dcbe7e8ea548203f90bb17c5e9829f3066ffabb24820f0ee7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dd552ea93d227eb0744ebb37712dad998c61ab9c6afb76f68c49fa2f9db8840)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryDataTransferConfigTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryDataTransferConfigTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryDataTransferConfigTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b9e00eb54b8c643e2fecaaf8454621d6d30cab14c4510a396c242626e0d03bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "BigqueryDataTransferConfig",
    "BigqueryDataTransferConfigConfig",
    "BigqueryDataTransferConfigEmailPreferences",
    "BigqueryDataTransferConfigEmailPreferencesOutputReference",
    "BigqueryDataTransferConfigEncryptionConfiguration",
    "BigqueryDataTransferConfigEncryptionConfigurationOutputReference",
    "BigqueryDataTransferConfigScheduleOptions",
    "BigqueryDataTransferConfigScheduleOptionsOutputReference",
    "BigqueryDataTransferConfigSensitiveParams",
    "BigqueryDataTransferConfigSensitiveParamsOutputReference",
    "BigqueryDataTransferConfigTimeouts",
    "BigqueryDataTransferConfigTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__9ce5c5f72d7da49fee4b30f16a923322c87c24e3f10abe6f6aaf4de011d3dd4e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    data_source_id: builtins.str,
    display_name: builtins.str,
    params: typing.Mapping[builtins.str, builtins.str],
    data_refresh_window_days: typing.Optional[jsii.Number] = None,
    destination_dataset_id: typing.Optional[builtins.str] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    email_preferences: typing.Optional[typing.Union[BigqueryDataTransferConfigEmailPreferences, typing.Dict[builtins.str, typing.Any]]] = None,
    encryption_configuration: typing.Optional[typing.Union[BigqueryDataTransferConfigEncryptionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    notification_pubsub_topic: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[builtins.str] = None,
    schedule_options: typing.Optional[typing.Union[BigqueryDataTransferConfigScheduleOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    sensitive_params: typing.Optional[typing.Union[BigqueryDataTransferConfigSensitiveParams, typing.Dict[builtins.str, typing.Any]]] = None,
    service_account_name: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[BigqueryDataTransferConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__061b2c860ae4419df30312a4e535cab10a1ad180f1c5818509a95b8a6c53e520(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f2e7d6fc029bddff272b87a7c742ee880737944ae1a65329b5711d955b16a7b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ff11e2885c25d012bc91f7ae7acd0f150b5fbf90a575a5c9ee8b69ed96caa3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39b74f8a00f0a2298a1af34748f2a9278a72844539e9fa2b195d70dd086f6d69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04ebab6a9fe044e2736ecb179185f757522e9e7f6037350fc5d3e79a0ae66d69(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fd825eb23d30629ae27d1378506d0fa6d7bb1585f804326ba3b33fb1c197559(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__448ee582f7fb5394fe3038e029c0987073c0a4a56cc7ab599c8a7b477adcc51d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__527f7969c82b06cb1d9cfd86bfe5138ac0fd7603d9982a180b852a191cd73559(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac52df80c117d81f734290b9d519f01e30cfe65bdb15c580c720c5bc171550e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90430baf4a12816ce63c5fb48138ea273d878f09108237c7d06df5b0aac9ab77(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aa0ecd2e379279b4bcf330838cc0f3527fad04b121a4efc1773c9f1d8fa8f1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d8628cc88f9c612c5add3df4592579d5afd04441d7993c4d13e9f766b37eb78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f066231e520c91912f47abe966e8269599a81b280d33a3cdf0364bd1573e66b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ffb0e22d8c4adea91922889705a0be32220f7f6cbf6d2d7f815b82286c0db3f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    data_source_id: builtins.str,
    display_name: builtins.str,
    params: typing.Mapping[builtins.str, builtins.str],
    data_refresh_window_days: typing.Optional[jsii.Number] = None,
    destination_dataset_id: typing.Optional[builtins.str] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    email_preferences: typing.Optional[typing.Union[BigqueryDataTransferConfigEmailPreferences, typing.Dict[builtins.str, typing.Any]]] = None,
    encryption_configuration: typing.Optional[typing.Union[BigqueryDataTransferConfigEncryptionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    notification_pubsub_topic: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[builtins.str] = None,
    schedule_options: typing.Optional[typing.Union[BigqueryDataTransferConfigScheduleOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    sensitive_params: typing.Optional[typing.Union[BigqueryDataTransferConfigSensitiveParams, typing.Dict[builtins.str, typing.Any]]] = None,
    service_account_name: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[BigqueryDataTransferConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20f0eb2dc01087dc23a5e3067f3dec27cac24001117fc324571ebc18af7e2c56(
    *,
    enable_failure_email: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2d6f201549467267f29432aa59e8e8e39227873982e05d24ff2ea903c6e6ba5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49cc43a71a7a64ff401bf8dfb443b187931146ac05ae5c9e271afb50401ed788(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__859c528078ecefdc50487be112b7dd04345658e5ec11ba962a4341e6eeb1a300(
    value: typing.Optional[BigqueryDataTransferConfigEmailPreferences],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fef28bb292bc36fdc3e1b0a5033c692933c0cb16dac67bb74c93727a5320a57f(
    *,
    kms_key_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bb5f832e9c275cfcdbf02169563f58688073cef6e49012a3742d5b7e87ece55(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__233bdc72a3c0986620a4a10c990066e8ac5f90a37882d1ce80112a1c1838a1f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__947e389f327e2fcfd3e7e9a1e2ff68b93db8d442fd807a2779f848bcc462b736(
    value: typing.Optional[BigqueryDataTransferConfigEncryptionConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13f79c62d2c3aaa5dc82238fa7b3bd835543155f4b1621109bc0c46bc34fe6fb(
    *,
    disable_auto_scheduling: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    end_time: typing.Optional[builtins.str] = None,
    start_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__994b55521e07c795a3be105ed4c2d342854ff109eb7beb4ed3b023e8735662ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92649db922ce627c5ed610b65f58146c8b0d08e9cd216b24d3239b16fbcd8b79(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c85fbe72e143286214077352cb8d9c3a216ba394eedfbb65d07cb391cb71d14f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__334114df0296e9ca9fe2e96f6ec4d86f75adeb42a0e736322091f6bd5fccfd24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27e012c4fd64115735a4d7f2188b99f9abbdd4201ff889c30c32a7c6ce1b297e(
    value: typing.Optional[BigqueryDataTransferConfigScheduleOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d11d7103971e3dc6e76809789a18de81f6b0bb38a9453871ba518d788e153e04(
    *,
    secret_access_key: typing.Optional[builtins.str] = None,
    secret_access_key_wo: typing.Optional[builtins.str] = None,
    secret_access_key_wo_version: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9517484e7bc2c064f77d38df8f9b343e5d6506ce826cf66743d7ccb9098ce992(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b077f64484b20ec1d29d52d81e63662167b965806ca735f94252e537d6860d36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba114477ae2c9f3bdc0b3984b61462f0e60b39c11b54c3bf675fcb467d78d90c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01cace08d03652cf79b82b3375973e8605002b3caba43283a02c5a38af84a2bf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e597a1ce3e7798e331fff389280450aa15a38ff97fefe0e9d81c9fb4feaa7513(
    value: typing.Optional[BigqueryDataTransferConfigSensitiveParams],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4b19f6bc25e3b3bf664d2a36165dd4c20087761ca8e1e631fafa06f4f41614a(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1254ec22a3aafa941c4bf39040f120da9c03389257df54c00ffdcd398687c62c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7743e7f893bfc041ea424229076e73d5a17a86f51070d8001bbeaa9fee0ce3d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72b7315db04f4d4dcbe7e8ea548203f90bb17c5e9829f3066ffabb24820f0ee7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dd552ea93d227eb0744ebb37712dad998c61ab9c6afb76f68c49fa2f9db8840(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b9e00eb54b8c643e2fecaaf8454621d6d30cab14c4510a396c242626e0d03bb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryDataTransferConfigTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
