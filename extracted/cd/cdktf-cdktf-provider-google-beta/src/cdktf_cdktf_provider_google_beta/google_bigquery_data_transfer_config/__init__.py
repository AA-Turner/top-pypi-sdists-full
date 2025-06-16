r'''
# `google_bigquery_data_transfer_config`

Refer to the Terraform Registry for docs: [`google_bigquery_data_transfer_config`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config).
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


class GoogleBigqueryDataTransferConfig(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryDataTransferConfig.GoogleBigqueryDataTransferConfig",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config google_bigquery_data_transfer_config}.'''

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
        email_preferences: typing.Optional[typing.Union["GoogleBigqueryDataTransferConfigEmailPreferences", typing.Dict[builtins.str, typing.Any]]] = None,
        encryption_configuration: typing.Optional[typing.Union["GoogleBigqueryDataTransferConfigEncryptionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        notification_pubsub_topic: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[builtins.str] = None,
        schedule_options: typing.Optional[typing.Union["GoogleBigqueryDataTransferConfigScheduleOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        sensitive_params: typing.Optional[typing.Union["GoogleBigqueryDataTransferConfigSensitiveParams", typing.Dict[builtins.str, typing.Any]]] = None,
        service_account_name: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleBigqueryDataTransferConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config google_bigquery_data_transfer_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param data_source_id: The data source id. Cannot be changed once the transfer config is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#data_source_id GoogleBigqueryDataTransferConfig#data_source_id}
        :param display_name: The user specified display name for the transfer config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#display_name GoogleBigqueryDataTransferConfig#display_name}
        :param params: Parameters specific to each data source. For more information see the bq tab in the 'Setting up a data transfer' section for each data source. For example the parameters for Cloud Storage transfers are listed here: https://cloud.google.com/bigquery-transfer/docs/cloud-storage-transfer#bq **NOTE** : If you are attempting to update a parameter that cannot be updated (due to api limitations) `please force recreation of the resource <https://www.terraform.io/cli/state/taint#forcing-re-creation-of-resources>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#params GoogleBigqueryDataTransferConfig#params}
        :param data_refresh_window_days: The number of days to look back to automatically refresh the data. For example, if dataRefreshWindowDays = 10, then every day BigQuery reingests data for [today-10, today-1], rather than ingesting data for just [today-1]. Only valid if the data source supports the feature. Set the value to 0 to use the default value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#data_refresh_window_days GoogleBigqueryDataTransferConfig#data_refresh_window_days}
        :param destination_dataset_id: The BigQuery target dataset id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#destination_dataset_id GoogleBigqueryDataTransferConfig#destination_dataset_id}
        :param disabled: When set to true, no runs are scheduled for a given transfer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#disabled GoogleBigqueryDataTransferConfig#disabled}
        :param email_preferences: email_preferences block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#email_preferences GoogleBigqueryDataTransferConfig#email_preferences}
        :param encryption_configuration: encryption_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#encryption_configuration GoogleBigqueryDataTransferConfig#encryption_configuration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#id GoogleBigqueryDataTransferConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param location: The geographic location where the transfer config should reside. Examples: US, EU, asia-northeast1. The default value is US. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#location GoogleBigqueryDataTransferConfig#location}
        :param notification_pubsub_topic: Pub/Sub topic where notifications will be sent after transfer runs associated with this transfer config finish. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#notification_pubsub_topic GoogleBigqueryDataTransferConfig#notification_pubsub_topic}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#project GoogleBigqueryDataTransferConfig#project}.
        :param schedule: Data transfer schedule. If the data source does not support a custom schedule, this should be empty. If it is empty, the default value for the data source will be used. The specified times are in UTC. Examples of valid format: 1st,3rd monday of month 15:30, every wed,fri of jan, jun 13:15, and first sunday of quarter 00:00. See more explanation about the format here: https://cloud.google.com/appengine/docs/flexible/python/scheduling-jobs-with-cron-yaml#the_schedule_format NOTE: The minimum interval time between recurring transfers depends on the data source; refer to the documentation for your data source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#schedule GoogleBigqueryDataTransferConfig#schedule}
        :param schedule_options: schedule_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#schedule_options GoogleBigqueryDataTransferConfig#schedule_options}
        :param sensitive_params: sensitive_params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#sensitive_params GoogleBigqueryDataTransferConfig#sensitive_params}
        :param service_account_name: Service account email. If this field is set, transfer config will be created with this service account credentials. It requires that requesting user calling this API has permissions to act as this service account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#service_account_name GoogleBigqueryDataTransferConfig#service_account_name}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#timeouts GoogleBigqueryDataTransferConfig#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96c9a18993faefa00341827ce472cf592d269a47cf2a70e2892113e13f4efeab)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleBigqueryDataTransferConfigConfig(
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
        '''Generates CDKTF code for importing a GoogleBigqueryDataTransferConfig resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleBigqueryDataTransferConfig to import.
        :param import_from_id: The id of the existing GoogleBigqueryDataTransferConfig that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleBigqueryDataTransferConfig to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8cad4a81a27f571e221dff2b2e51210bc8264d2a00d44f5cc0b5661ac4cdd6b)
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
        :param enable_failure_email: If true, email notifications will be sent on transfer run failures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#enable_failure_email GoogleBigqueryDataTransferConfig#enable_failure_email}
        '''
        value = GoogleBigqueryDataTransferConfigEmailPreferences(
            enable_failure_email=enable_failure_email
        )

        return typing.cast(None, jsii.invoke(self, "putEmailPreferences", [value]))

    @jsii.member(jsii_name="putEncryptionConfiguration")
    def put_encryption_configuration(self, *, kms_key_name: builtins.str) -> None:
        '''
        :param kms_key_name: The name of the KMS key used for encrypting BigQuery data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#kms_key_name GoogleBigqueryDataTransferConfig#kms_key_name}
        '''
        value = GoogleBigqueryDataTransferConfigEncryptionConfiguration(
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
        :param disable_auto_scheduling: If true, automatic scheduling of data transfer runs for this configuration will be disabled. The runs can be started on ad-hoc basis using transferConfigs.startManualRuns API. When automatic scheduling is disabled, the TransferConfig.schedule field will be ignored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#disable_auto_scheduling GoogleBigqueryDataTransferConfig#disable_auto_scheduling}
        :param end_time: Defines time to stop scheduling transfer runs. A transfer run cannot be scheduled at or after the end time. The end time can be changed at any moment. The time when a data transfer can be triggered manually is not limited by this option. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#end_time GoogleBigqueryDataTransferConfig#end_time}
        :param start_time: Specifies time to start scheduling transfer runs. The first run will be scheduled at or after the start time according to a recurrence pattern defined in the schedule string. The start time can be changed at any moment. The time when a data transfer can be triggered manually is not limited by this option. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#start_time GoogleBigqueryDataTransferConfig#start_time}
        '''
        value = GoogleBigqueryDataTransferConfigScheduleOptions(
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
        :param secret_access_key: The Secret Access Key of the AWS account transferring data from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#secret_access_key GoogleBigqueryDataTransferConfig#secret_access_key}
        :param secret_access_key_wo: The Secret Access Key of the AWS account transferring data from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#secret_access_key_wo GoogleBigqueryDataTransferConfig#secret_access_key_wo}
        :param secret_access_key_wo_version: The version of the sensitive params - used to trigger updates of the write-only params. For more info see `updating write-only attributes </docs/providers/google/guides/using_write_only_attributes.html#updating-write-only-attributes>`_ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#secret_access_key_wo_version GoogleBigqueryDataTransferConfig#secret_access_key_wo_version}
        '''
        value = GoogleBigqueryDataTransferConfigSensitiveParams(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#create GoogleBigqueryDataTransferConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#delete GoogleBigqueryDataTransferConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#update GoogleBigqueryDataTransferConfig#update}.
        '''
        value = GoogleBigqueryDataTransferConfigTimeouts(
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
    ) -> "GoogleBigqueryDataTransferConfigEmailPreferencesOutputReference":
        return typing.cast("GoogleBigqueryDataTransferConfigEmailPreferencesOutputReference", jsii.get(self, "emailPreferences"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfiguration")
    def encryption_configuration(
        self,
    ) -> "GoogleBigqueryDataTransferConfigEncryptionConfigurationOutputReference":
        return typing.cast("GoogleBigqueryDataTransferConfigEncryptionConfigurationOutputReference", jsii.get(self, "encryptionConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="scheduleOptions")
    def schedule_options(
        self,
    ) -> "GoogleBigqueryDataTransferConfigScheduleOptionsOutputReference":
        return typing.cast("GoogleBigqueryDataTransferConfigScheduleOptionsOutputReference", jsii.get(self, "scheduleOptions"))

    @builtins.property
    @jsii.member(jsii_name="sensitiveParams")
    def sensitive_params(
        self,
    ) -> "GoogleBigqueryDataTransferConfigSensitiveParamsOutputReference":
        return typing.cast("GoogleBigqueryDataTransferConfigSensitiveParamsOutputReference", jsii.get(self, "sensitiveParams"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleBigqueryDataTransferConfigTimeoutsOutputReference":
        return typing.cast("GoogleBigqueryDataTransferConfigTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["GoogleBigqueryDataTransferConfigEmailPreferences"]:
        return typing.cast(typing.Optional["GoogleBigqueryDataTransferConfigEmailPreferences"], jsii.get(self, "emailPreferencesInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfigurationInput")
    def encryption_configuration_input(
        self,
    ) -> typing.Optional["GoogleBigqueryDataTransferConfigEncryptionConfiguration"]:
        return typing.cast(typing.Optional["GoogleBigqueryDataTransferConfigEncryptionConfiguration"], jsii.get(self, "encryptionConfigurationInput"))

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
    ) -> typing.Optional["GoogleBigqueryDataTransferConfigScheduleOptions"]:
        return typing.cast(typing.Optional["GoogleBigqueryDataTransferConfigScheduleOptions"], jsii.get(self, "scheduleOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="sensitiveParamsInput")
    def sensitive_params_input(
        self,
    ) -> typing.Optional["GoogleBigqueryDataTransferConfigSensitiveParams"]:
        return typing.cast(typing.Optional["GoogleBigqueryDataTransferConfigSensitiveParams"], jsii.get(self, "sensitiveParamsInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountNameInput")
    def service_account_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountNameInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleBigqueryDataTransferConfigTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleBigqueryDataTransferConfigTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="dataRefreshWindowDays")
    def data_refresh_window_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dataRefreshWindowDays"))

    @data_refresh_window_days.setter
    def data_refresh_window_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4d25349eec5ef3d3fb250b64ba80970f2457fd8841556685fbfd0f967a246d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataRefreshWindowDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataSourceId")
    def data_source_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataSourceId"))

    @data_source_id.setter
    def data_source_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d81a46963fbb6d6c4fb30cd693632b163f4ad2e7c94309aa2973a3f091c1bf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataSourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destinationDatasetId")
    def destination_dataset_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationDatasetId"))

    @destination_dataset_id.setter
    def destination_dataset_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fa7999c9dcbfb64156c8c6ce48666224ef868ad46e72f39890105f1cec070cf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c48bfd68b34a8fc148e538848ab46a89bae0a0f59e418aa522873fdd27c2d6c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c19b7a9007984abb5608feba35c1cbefaacec490f60bf026b3bf195b638389f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12922f76af29b4ec1748af4ca0532413f01a28a464d8ae31581b1dd6c76d172c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7dd905b2ea7ab4c52d44b0ffbe466af14ae75a5f423bf96192dd5e25021ed10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notificationPubsubTopic")
    def notification_pubsub_topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notificationPubsubTopic"))

    @notification_pubsub_topic.setter
    def notification_pubsub_topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2963cd872182aa5122ea41f54e88f5b7adfe487e0d78ab4fc794ca3a4a413e79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationPubsubTopic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="params")
    def params(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "params"))

    @params.setter
    def params(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e688aa1315a507877d6bca28b3c5552241c10ea8717ffc533aaf46eee00126ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "params", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd746026852e9c9fcaf68a0e03256f4c301b20d879cc8678884a22c08c184ce3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schedule"))

    @schedule.setter
    def schedule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efe276dc53e8e48e86c31fd7538702cb9ff111e3f08aba3fcfaff883fb40dd81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccountName")
    def service_account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccountName"))

    @service_account_name.setter
    def service_account_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__908f237e8382cdf3308d73ead3a58203b93d3cf699d3a05cc2761c4220b9fa81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountName", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryDataTransferConfig.GoogleBigqueryDataTransferConfigConfig",
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
class GoogleBigqueryDataTransferConfigConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        email_preferences: typing.Optional[typing.Union["GoogleBigqueryDataTransferConfigEmailPreferences", typing.Dict[builtins.str, typing.Any]]] = None,
        encryption_configuration: typing.Optional[typing.Union["GoogleBigqueryDataTransferConfigEncryptionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        notification_pubsub_topic: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[builtins.str] = None,
        schedule_options: typing.Optional[typing.Union["GoogleBigqueryDataTransferConfigScheduleOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        sensitive_params: typing.Optional[typing.Union["GoogleBigqueryDataTransferConfigSensitiveParams", typing.Dict[builtins.str, typing.Any]]] = None,
        service_account_name: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleBigqueryDataTransferConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param data_source_id: The data source id. Cannot be changed once the transfer config is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#data_source_id GoogleBigqueryDataTransferConfig#data_source_id}
        :param display_name: The user specified display name for the transfer config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#display_name GoogleBigqueryDataTransferConfig#display_name}
        :param params: Parameters specific to each data source. For more information see the bq tab in the 'Setting up a data transfer' section for each data source. For example the parameters for Cloud Storage transfers are listed here: https://cloud.google.com/bigquery-transfer/docs/cloud-storage-transfer#bq **NOTE** : If you are attempting to update a parameter that cannot be updated (due to api limitations) `please force recreation of the resource <https://www.terraform.io/cli/state/taint#forcing-re-creation-of-resources>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#params GoogleBigqueryDataTransferConfig#params}
        :param data_refresh_window_days: The number of days to look back to automatically refresh the data. For example, if dataRefreshWindowDays = 10, then every day BigQuery reingests data for [today-10, today-1], rather than ingesting data for just [today-1]. Only valid if the data source supports the feature. Set the value to 0 to use the default value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#data_refresh_window_days GoogleBigqueryDataTransferConfig#data_refresh_window_days}
        :param destination_dataset_id: The BigQuery target dataset id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#destination_dataset_id GoogleBigqueryDataTransferConfig#destination_dataset_id}
        :param disabled: When set to true, no runs are scheduled for a given transfer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#disabled GoogleBigqueryDataTransferConfig#disabled}
        :param email_preferences: email_preferences block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#email_preferences GoogleBigqueryDataTransferConfig#email_preferences}
        :param encryption_configuration: encryption_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#encryption_configuration GoogleBigqueryDataTransferConfig#encryption_configuration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#id GoogleBigqueryDataTransferConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param location: The geographic location where the transfer config should reside. Examples: US, EU, asia-northeast1. The default value is US. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#location GoogleBigqueryDataTransferConfig#location}
        :param notification_pubsub_topic: Pub/Sub topic where notifications will be sent after transfer runs associated with this transfer config finish. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#notification_pubsub_topic GoogleBigqueryDataTransferConfig#notification_pubsub_topic}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#project GoogleBigqueryDataTransferConfig#project}.
        :param schedule: Data transfer schedule. If the data source does not support a custom schedule, this should be empty. If it is empty, the default value for the data source will be used. The specified times are in UTC. Examples of valid format: 1st,3rd monday of month 15:30, every wed,fri of jan, jun 13:15, and first sunday of quarter 00:00. See more explanation about the format here: https://cloud.google.com/appengine/docs/flexible/python/scheduling-jobs-with-cron-yaml#the_schedule_format NOTE: The minimum interval time between recurring transfers depends on the data source; refer to the documentation for your data source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#schedule GoogleBigqueryDataTransferConfig#schedule}
        :param schedule_options: schedule_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#schedule_options GoogleBigqueryDataTransferConfig#schedule_options}
        :param sensitive_params: sensitive_params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#sensitive_params GoogleBigqueryDataTransferConfig#sensitive_params}
        :param service_account_name: Service account email. If this field is set, transfer config will be created with this service account credentials. It requires that requesting user calling this API has permissions to act as this service account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#service_account_name GoogleBigqueryDataTransferConfig#service_account_name}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#timeouts GoogleBigqueryDataTransferConfig#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(email_preferences, dict):
            email_preferences = GoogleBigqueryDataTransferConfigEmailPreferences(**email_preferences)
        if isinstance(encryption_configuration, dict):
            encryption_configuration = GoogleBigqueryDataTransferConfigEncryptionConfiguration(**encryption_configuration)
        if isinstance(schedule_options, dict):
            schedule_options = GoogleBigqueryDataTransferConfigScheduleOptions(**schedule_options)
        if isinstance(sensitive_params, dict):
            sensitive_params = GoogleBigqueryDataTransferConfigSensitiveParams(**sensitive_params)
        if isinstance(timeouts, dict):
            timeouts = GoogleBigqueryDataTransferConfigTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91ed7e31fda5c5b9d14d01f57e77bc505a5897abc578619759abbd16d26c3a92)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#data_source_id GoogleBigqueryDataTransferConfig#data_source_id}
        '''
        result = self._values.get("data_source_id")
        assert result is not None, "Required property 'data_source_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''The user specified display name for the transfer config.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#display_name GoogleBigqueryDataTransferConfig#display_name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#params GoogleBigqueryDataTransferConfig#params}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#data_refresh_window_days GoogleBigqueryDataTransferConfig#data_refresh_window_days}
        '''
        result = self._values.get("data_refresh_window_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def destination_dataset_id(self) -> typing.Optional[builtins.str]:
        '''The BigQuery target dataset id.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#destination_dataset_id GoogleBigqueryDataTransferConfig#destination_dataset_id}
        '''
        result = self._values.get("destination_dataset_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When set to true, no runs are scheduled for a given transfer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#disabled GoogleBigqueryDataTransferConfig#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def email_preferences(
        self,
    ) -> typing.Optional["GoogleBigqueryDataTransferConfigEmailPreferences"]:
        '''email_preferences block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#email_preferences GoogleBigqueryDataTransferConfig#email_preferences}
        '''
        result = self._values.get("email_preferences")
        return typing.cast(typing.Optional["GoogleBigqueryDataTransferConfigEmailPreferences"], result)

    @builtins.property
    def encryption_configuration(
        self,
    ) -> typing.Optional["GoogleBigqueryDataTransferConfigEncryptionConfiguration"]:
        '''encryption_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#encryption_configuration GoogleBigqueryDataTransferConfig#encryption_configuration}
        '''
        result = self._values.get("encryption_configuration")
        return typing.cast(typing.Optional["GoogleBigqueryDataTransferConfigEncryptionConfiguration"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#id GoogleBigqueryDataTransferConfig#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The geographic location where the transfer config should reside. Examples: US, EU, asia-northeast1. The default value is US.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#location GoogleBigqueryDataTransferConfig#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_pubsub_topic(self) -> typing.Optional[builtins.str]:
        '''Pub/Sub topic where notifications will be sent after transfer runs associated with this transfer config finish.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#notification_pubsub_topic GoogleBigqueryDataTransferConfig#notification_pubsub_topic}
        '''
        result = self._values.get("notification_pubsub_topic")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#project GoogleBigqueryDataTransferConfig#project}.'''
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#schedule GoogleBigqueryDataTransferConfig#schedule}
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule_options(
        self,
    ) -> typing.Optional["GoogleBigqueryDataTransferConfigScheduleOptions"]:
        '''schedule_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#schedule_options GoogleBigqueryDataTransferConfig#schedule_options}
        '''
        result = self._values.get("schedule_options")
        return typing.cast(typing.Optional["GoogleBigqueryDataTransferConfigScheduleOptions"], result)

    @builtins.property
    def sensitive_params(
        self,
    ) -> typing.Optional["GoogleBigqueryDataTransferConfigSensitiveParams"]:
        '''sensitive_params block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#sensitive_params GoogleBigqueryDataTransferConfig#sensitive_params}
        '''
        result = self._values.get("sensitive_params")
        return typing.cast(typing.Optional["GoogleBigqueryDataTransferConfigSensitiveParams"], result)

    @builtins.property
    def service_account_name(self) -> typing.Optional[builtins.str]:
        '''Service account email.

        If this field is set, transfer config will
        be created with this service account credentials. It requires that
        requesting user calling this API has permissions to act as this service account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#service_account_name GoogleBigqueryDataTransferConfig#service_account_name}
        '''
        result = self._values.get("service_account_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleBigqueryDataTransferConfigTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#timeouts GoogleBigqueryDataTransferConfig#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleBigqueryDataTransferConfigTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryDataTransferConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryDataTransferConfig.GoogleBigqueryDataTransferConfigEmailPreferences",
    jsii_struct_bases=[],
    name_mapping={"enable_failure_email": "enableFailureEmail"},
)
class GoogleBigqueryDataTransferConfigEmailPreferences:
    def __init__(
        self,
        *,
        enable_failure_email: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enable_failure_email: If true, email notifications will be sent on transfer run failures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#enable_failure_email GoogleBigqueryDataTransferConfig#enable_failure_email}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51c4d29944340b4f4e7300f32fb1046b1f428c978398572e7abd932d32830958)
            check_type(argname="argument enable_failure_email", value=enable_failure_email, expected_type=type_hints["enable_failure_email"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enable_failure_email": enable_failure_email,
        }

    @builtins.property
    def enable_failure_email(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''If true, email notifications will be sent on transfer run failures.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#enable_failure_email GoogleBigqueryDataTransferConfig#enable_failure_email}
        '''
        result = self._values.get("enable_failure_email")
        assert result is not None, "Required property 'enable_failure_email' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryDataTransferConfigEmailPreferences(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBigqueryDataTransferConfigEmailPreferencesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryDataTransferConfig.GoogleBigqueryDataTransferConfigEmailPreferencesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8786ae5f4e9ac62499530f6c1804e99bc424302eeca8aa01261a6a7fd1dabe07)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e2e669a0253864d2e9d471be815105d45ba62d41874d1fc4a6770e788815651)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableFailureEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleBigqueryDataTransferConfigEmailPreferences]:
        return typing.cast(typing.Optional[GoogleBigqueryDataTransferConfigEmailPreferences], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBigqueryDataTransferConfigEmailPreferences],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e579b2c87b200567fa9548d4bc5ce360208e72f96a6886c927a178bed04963cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryDataTransferConfig.GoogleBigqueryDataTransferConfigEncryptionConfiguration",
    jsii_struct_bases=[],
    name_mapping={"kms_key_name": "kmsKeyName"},
)
class GoogleBigqueryDataTransferConfigEncryptionConfiguration:
    def __init__(self, *, kms_key_name: builtins.str) -> None:
        '''
        :param kms_key_name: The name of the KMS key used for encrypting BigQuery data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#kms_key_name GoogleBigqueryDataTransferConfig#kms_key_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__122d1265005075544e912836b452566dbb0f848fbb74429bc57a36ccc9165abf)
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kms_key_name": kms_key_name,
        }

    @builtins.property
    def kms_key_name(self) -> builtins.str:
        '''The name of the KMS key used for encrypting BigQuery data.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#kms_key_name GoogleBigqueryDataTransferConfig#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        assert result is not None, "Required property 'kms_key_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryDataTransferConfigEncryptionConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBigqueryDataTransferConfigEncryptionConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryDataTransferConfig.GoogleBigqueryDataTransferConfigEncryptionConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff73f86befd0b15f36796ab98f0ee00fe65cabd5c24c7bc517be845983e4d3de)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a5be1eb88aaa42677b60bf41a1e69c8b3464f16835126069e9d524447218d29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleBigqueryDataTransferConfigEncryptionConfiguration]:
        return typing.cast(typing.Optional[GoogleBigqueryDataTransferConfigEncryptionConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBigqueryDataTransferConfigEncryptionConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d6d16379f46946ff9fe7251a4cb5f259ee74aed7e8e76c2bf37add188f57ab9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryDataTransferConfig.GoogleBigqueryDataTransferConfigScheduleOptions",
    jsii_struct_bases=[],
    name_mapping={
        "disable_auto_scheduling": "disableAutoScheduling",
        "end_time": "endTime",
        "start_time": "startTime",
    },
)
class GoogleBigqueryDataTransferConfigScheduleOptions:
    def __init__(
        self,
        *,
        disable_auto_scheduling: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        end_time: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disable_auto_scheduling: If true, automatic scheduling of data transfer runs for this configuration will be disabled. The runs can be started on ad-hoc basis using transferConfigs.startManualRuns API. When automatic scheduling is disabled, the TransferConfig.schedule field will be ignored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#disable_auto_scheduling GoogleBigqueryDataTransferConfig#disable_auto_scheduling}
        :param end_time: Defines time to stop scheduling transfer runs. A transfer run cannot be scheduled at or after the end time. The end time can be changed at any moment. The time when a data transfer can be triggered manually is not limited by this option. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#end_time GoogleBigqueryDataTransferConfig#end_time}
        :param start_time: Specifies time to start scheduling transfer runs. The first run will be scheduled at or after the start time according to a recurrence pattern defined in the schedule string. The start time can be changed at any moment. The time when a data transfer can be triggered manually is not limited by this option. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#start_time GoogleBigqueryDataTransferConfig#start_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__413302374f8c2148e650badb8d6b6cce2d7357b1a13bfaddd7108a34a784752a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#disable_auto_scheduling GoogleBigqueryDataTransferConfig#disable_auto_scheduling}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#end_time GoogleBigqueryDataTransferConfig#end_time}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#start_time GoogleBigqueryDataTransferConfig#start_time}
        '''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryDataTransferConfigScheduleOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBigqueryDataTransferConfigScheduleOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryDataTransferConfig.GoogleBigqueryDataTransferConfigScheduleOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__89cc8b7fe08e0985b052b8325985c5ec4dc27f1d6d5b122ec0210eb6034aaf3c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf9fa32dc91fa2a1ec3eb7493ae90f9cdad22efaea8680227486dcecc828e069)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableAutoScheduling", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTime"))

    @end_time.setter
    def end_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d29773553e33273b740812b670ac3251eea8055ae97f3326561384bffa844aad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__533b3c850048c3409885c8cc25e60400c242ea171dcab02ec9ff428454915ea9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleBigqueryDataTransferConfigScheduleOptions]:
        return typing.cast(typing.Optional[GoogleBigqueryDataTransferConfigScheduleOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBigqueryDataTransferConfigScheduleOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11837402a284cc2d8715a6b6b786b789f1e9b158ece9756c1257d14f55eecd73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryDataTransferConfig.GoogleBigqueryDataTransferConfigSensitiveParams",
    jsii_struct_bases=[],
    name_mapping={
        "secret_access_key": "secretAccessKey",
        "secret_access_key_wo": "secretAccessKeyWo",
        "secret_access_key_wo_version": "secretAccessKeyWoVersion",
    },
)
class GoogleBigqueryDataTransferConfigSensitiveParams:
    def __init__(
        self,
        *,
        secret_access_key: typing.Optional[builtins.str] = None,
        secret_access_key_wo: typing.Optional[builtins.str] = None,
        secret_access_key_wo_version: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param secret_access_key: The Secret Access Key of the AWS account transferring data from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#secret_access_key GoogleBigqueryDataTransferConfig#secret_access_key}
        :param secret_access_key_wo: The Secret Access Key of the AWS account transferring data from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#secret_access_key_wo GoogleBigqueryDataTransferConfig#secret_access_key_wo}
        :param secret_access_key_wo_version: The version of the sensitive params - used to trigger updates of the write-only params. For more info see `updating write-only attributes </docs/providers/google/guides/using_write_only_attributes.html#updating-write-only-attributes>`_ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#secret_access_key_wo_version GoogleBigqueryDataTransferConfig#secret_access_key_wo_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39a3f2df39855fd24038978e575aa8b8daa9f8db53b4e3a62a2a7b4fcc4cd444)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#secret_access_key GoogleBigqueryDataTransferConfig#secret_access_key}
        '''
        result = self._values.get("secret_access_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_access_key_wo(self) -> typing.Optional[builtins.str]:
        '''The Secret Access Key of the AWS account transferring data from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#secret_access_key_wo GoogleBigqueryDataTransferConfig#secret_access_key_wo}
        '''
        result = self._values.get("secret_access_key_wo")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_access_key_wo_version(self) -> typing.Optional[jsii.Number]:
        '''The version of the sensitive params - used to trigger updates of the write-only params.

        For more info see `updating write-only attributes </docs/providers/google/guides/using_write_only_attributes.html#updating-write-only-attributes>`_

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#secret_access_key_wo_version GoogleBigqueryDataTransferConfig#secret_access_key_wo_version}
        '''
        result = self._values.get("secret_access_key_wo_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryDataTransferConfigSensitiveParams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBigqueryDataTransferConfigSensitiveParamsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryDataTransferConfig.GoogleBigqueryDataTransferConfigSensitiveParamsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2e4afa192c5d5f80658eef1151347ed68a8143153d04958fbac8598d6239b02)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f8e21457f7c44e4b842138f4bc2fcf0e90f8bdbb32b5f78500c2bf423c82a28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretAccessKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretAccessKeyWo")
    def secret_access_key_wo(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretAccessKeyWo"))

    @secret_access_key_wo.setter
    def secret_access_key_wo(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4883105913245f07251383ca5fed9a610aa4c5b57d2f0c6006a92112369e292a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretAccessKeyWo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretAccessKeyWoVersion")
    def secret_access_key_wo_version(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "secretAccessKeyWoVersion"))

    @secret_access_key_wo_version.setter
    def secret_access_key_wo_version(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99e405da38c6a912a8b50dd0db0dba6245481746116d7cd3ca32c9c4c0b95979)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretAccessKeyWoVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleBigqueryDataTransferConfigSensitiveParams]:
        return typing.cast(typing.Optional[GoogleBigqueryDataTransferConfigSensitiveParams], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBigqueryDataTransferConfigSensitiveParams],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1ee4aac71a7ce4355c85d0cd39cad941137e4c94d3660a7a3ffacc136cfe0b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryDataTransferConfig.GoogleBigqueryDataTransferConfigTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleBigqueryDataTransferConfigTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#create GoogleBigqueryDataTransferConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#delete GoogleBigqueryDataTransferConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#update GoogleBigqueryDataTransferConfig#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b835650ef263f259ce9a268bbe0704a6cf8ffd7dff54553c479f9ca8b38ee2ff)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#create GoogleBigqueryDataTransferConfig#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#delete GoogleBigqueryDataTransferConfig#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_data_transfer_config#update GoogleBigqueryDataTransferConfig#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryDataTransferConfigTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBigqueryDataTransferConfigTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryDataTransferConfig.GoogleBigqueryDataTransferConfigTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e84fdaa07b7e92f8c30003b555d2d3a375d5f210d29d809221994a93a6882498)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0419400fcca18e4811a950f712cd4899bd0c0d434f5e718256173c27ee7c3b12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb4d1fd28692c6ad4719a1768506949a0ae036ac064d7918c54edf6b2620a6b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1181ae2719f83b005b317b1c1bff2e931b8cdbe88b115988e4c5faad3e82f1bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBigqueryDataTransferConfigTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBigqueryDataTransferConfigTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBigqueryDataTransferConfigTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d3a7d3b7a9bc6eb3846f14df53fa8e85517f245963f9f371445fb9bda21b512)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleBigqueryDataTransferConfig",
    "GoogleBigqueryDataTransferConfigConfig",
    "GoogleBigqueryDataTransferConfigEmailPreferences",
    "GoogleBigqueryDataTransferConfigEmailPreferencesOutputReference",
    "GoogleBigqueryDataTransferConfigEncryptionConfiguration",
    "GoogleBigqueryDataTransferConfigEncryptionConfigurationOutputReference",
    "GoogleBigqueryDataTransferConfigScheduleOptions",
    "GoogleBigqueryDataTransferConfigScheduleOptionsOutputReference",
    "GoogleBigqueryDataTransferConfigSensitiveParams",
    "GoogleBigqueryDataTransferConfigSensitiveParamsOutputReference",
    "GoogleBigqueryDataTransferConfigTimeouts",
    "GoogleBigqueryDataTransferConfigTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__96c9a18993faefa00341827ce472cf592d269a47cf2a70e2892113e13f4efeab(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    data_source_id: builtins.str,
    display_name: builtins.str,
    params: typing.Mapping[builtins.str, builtins.str],
    data_refresh_window_days: typing.Optional[jsii.Number] = None,
    destination_dataset_id: typing.Optional[builtins.str] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    email_preferences: typing.Optional[typing.Union[GoogleBigqueryDataTransferConfigEmailPreferences, typing.Dict[builtins.str, typing.Any]]] = None,
    encryption_configuration: typing.Optional[typing.Union[GoogleBigqueryDataTransferConfigEncryptionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    notification_pubsub_topic: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[builtins.str] = None,
    schedule_options: typing.Optional[typing.Union[GoogleBigqueryDataTransferConfigScheduleOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    sensitive_params: typing.Optional[typing.Union[GoogleBigqueryDataTransferConfigSensitiveParams, typing.Dict[builtins.str, typing.Any]]] = None,
    service_account_name: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleBigqueryDataTransferConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__a8cad4a81a27f571e221dff2b2e51210bc8264d2a00d44f5cc0b5661ac4cdd6b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4d25349eec5ef3d3fb250b64ba80970f2457fd8841556685fbfd0f967a246d1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d81a46963fbb6d6c4fb30cd693632b163f4ad2e7c94309aa2973a3f091c1bf0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fa7999c9dcbfb64156c8c6ce48666224ef868ad46e72f39890105f1cec070cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c48bfd68b34a8fc148e538848ab46a89bae0a0f59e418aa522873fdd27c2d6c0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c19b7a9007984abb5608feba35c1cbefaacec490f60bf026b3bf195b638389f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12922f76af29b4ec1748af4ca0532413f01a28a464d8ae31581b1dd6c76d172c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7dd905b2ea7ab4c52d44b0ffbe466af14ae75a5f423bf96192dd5e25021ed10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2963cd872182aa5122ea41f54e88f5b7adfe487e0d78ab4fc794ca3a4a413e79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e688aa1315a507877d6bca28b3c5552241c10ea8717ffc533aaf46eee00126ce(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd746026852e9c9fcaf68a0e03256f4c301b20d879cc8678884a22c08c184ce3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efe276dc53e8e48e86c31fd7538702cb9ff111e3f08aba3fcfaff883fb40dd81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__908f237e8382cdf3308d73ead3a58203b93d3cf699d3a05cc2761c4220b9fa81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91ed7e31fda5c5b9d14d01f57e77bc505a5897abc578619759abbd16d26c3a92(
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
    email_preferences: typing.Optional[typing.Union[GoogleBigqueryDataTransferConfigEmailPreferences, typing.Dict[builtins.str, typing.Any]]] = None,
    encryption_configuration: typing.Optional[typing.Union[GoogleBigqueryDataTransferConfigEncryptionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    notification_pubsub_topic: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[builtins.str] = None,
    schedule_options: typing.Optional[typing.Union[GoogleBigqueryDataTransferConfigScheduleOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    sensitive_params: typing.Optional[typing.Union[GoogleBigqueryDataTransferConfigSensitiveParams, typing.Dict[builtins.str, typing.Any]]] = None,
    service_account_name: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleBigqueryDataTransferConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51c4d29944340b4f4e7300f32fb1046b1f428c978398572e7abd932d32830958(
    *,
    enable_failure_email: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8786ae5f4e9ac62499530f6c1804e99bc424302eeca8aa01261a6a7fd1dabe07(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e2e669a0253864d2e9d471be815105d45ba62d41874d1fc4a6770e788815651(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e579b2c87b200567fa9548d4bc5ce360208e72f96a6886c927a178bed04963cd(
    value: typing.Optional[GoogleBigqueryDataTransferConfigEmailPreferences],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__122d1265005075544e912836b452566dbb0f848fbb74429bc57a36ccc9165abf(
    *,
    kms_key_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff73f86befd0b15f36796ab98f0ee00fe65cabd5c24c7bc517be845983e4d3de(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a5be1eb88aaa42677b60bf41a1e69c8b3464f16835126069e9d524447218d29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d6d16379f46946ff9fe7251a4cb5f259ee74aed7e8e76c2bf37add188f57ab9(
    value: typing.Optional[GoogleBigqueryDataTransferConfigEncryptionConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__413302374f8c2148e650badb8d6b6cce2d7357b1a13bfaddd7108a34a784752a(
    *,
    disable_auto_scheduling: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    end_time: typing.Optional[builtins.str] = None,
    start_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89cc8b7fe08e0985b052b8325985c5ec4dc27f1d6d5b122ec0210eb6034aaf3c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf9fa32dc91fa2a1ec3eb7493ae90f9cdad22efaea8680227486dcecc828e069(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d29773553e33273b740812b670ac3251eea8055ae97f3326561384bffa844aad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__533b3c850048c3409885c8cc25e60400c242ea171dcab02ec9ff428454915ea9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11837402a284cc2d8715a6b6b786b789f1e9b158ece9756c1257d14f55eecd73(
    value: typing.Optional[GoogleBigqueryDataTransferConfigScheduleOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39a3f2df39855fd24038978e575aa8b8daa9f8db53b4e3a62a2a7b4fcc4cd444(
    *,
    secret_access_key: typing.Optional[builtins.str] = None,
    secret_access_key_wo: typing.Optional[builtins.str] = None,
    secret_access_key_wo_version: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2e4afa192c5d5f80658eef1151347ed68a8143153d04958fbac8598d6239b02(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f8e21457f7c44e4b842138f4bc2fcf0e90f8bdbb32b5f78500c2bf423c82a28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4883105913245f07251383ca5fed9a610aa4c5b57d2f0c6006a92112369e292a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99e405da38c6a912a8b50dd0db0dba6245481746116d7cd3ca32c9c4c0b95979(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1ee4aac71a7ce4355c85d0cd39cad941137e4c94d3660a7a3ffacc136cfe0b9(
    value: typing.Optional[GoogleBigqueryDataTransferConfigSensitiveParams],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b835650ef263f259ce9a268bbe0704a6cf8ffd7dff54553c479f9ca8b38ee2ff(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e84fdaa07b7e92f8c30003b555d2d3a375d5f210d29d809221994a93a6882498(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0419400fcca18e4811a950f712cd4899bd0c0d434f5e718256173c27ee7c3b12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb4d1fd28692c6ad4719a1768506949a0ae036ac064d7918c54edf6b2620a6b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1181ae2719f83b005b317b1c1bff2e931b8cdbe88b115988e4c5faad3e82f1bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d3a7d3b7a9bc6eb3846f14df53fa8e85517f245963f9f371445fb9bda21b512(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBigqueryDataTransferConfigTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
