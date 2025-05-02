r'''
# `aws_storagegateway_gateway`

Refer to the Terraform Registry for docs: [`aws_storagegateway_gateway`](https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway).
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


class StoragegatewayGateway(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.storagegatewayGateway.StoragegatewayGateway",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway aws_storagegateway_gateway}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        gateway_name: builtins.str,
        gateway_timezone: builtins.str,
        activation_key: typing.Optional[builtins.str] = None,
        average_download_rate_limit_in_bits_per_sec: typing.Optional[jsii.Number] = None,
        average_upload_rate_limit_in_bits_per_sec: typing.Optional[jsii.Number] = None,
        cloudwatch_log_group_arn: typing.Optional[builtins.str] = None,
        gateway_ip_address: typing.Optional[builtins.str] = None,
        gateway_type: typing.Optional[builtins.str] = None,
        gateway_vpc_endpoint: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        maintenance_start_time: typing.Optional[typing.Union["StoragegatewayGatewayMaintenanceStartTime", typing.Dict[builtins.str, typing.Any]]] = None,
        medium_changer_type: typing.Optional[builtins.str] = None,
        smb_active_directory_settings: typing.Optional[typing.Union["StoragegatewayGatewaySmbActiveDirectorySettings", typing.Dict[builtins.str, typing.Any]]] = None,
        smb_file_share_visibility: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        smb_guest_password: typing.Optional[builtins.str] = None,
        smb_security_strategy: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tape_drive_type: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["StoragegatewayGatewayTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway aws_storagegateway_gateway} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param gateway_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#gateway_name StoragegatewayGateway#gateway_name}.
        :param gateway_timezone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#gateway_timezone StoragegatewayGateway#gateway_timezone}.
        :param activation_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#activation_key StoragegatewayGateway#activation_key}.
        :param average_download_rate_limit_in_bits_per_sec: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#average_download_rate_limit_in_bits_per_sec StoragegatewayGateway#average_download_rate_limit_in_bits_per_sec}.
        :param average_upload_rate_limit_in_bits_per_sec: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#average_upload_rate_limit_in_bits_per_sec StoragegatewayGateway#average_upload_rate_limit_in_bits_per_sec}.
        :param cloudwatch_log_group_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#cloudwatch_log_group_arn StoragegatewayGateway#cloudwatch_log_group_arn}.
        :param gateway_ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#gateway_ip_address StoragegatewayGateway#gateway_ip_address}.
        :param gateway_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#gateway_type StoragegatewayGateway#gateway_type}.
        :param gateway_vpc_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#gateway_vpc_endpoint StoragegatewayGateway#gateway_vpc_endpoint}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#id StoragegatewayGateway#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param maintenance_start_time: maintenance_start_time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#maintenance_start_time StoragegatewayGateway#maintenance_start_time}
        :param medium_changer_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#medium_changer_type StoragegatewayGateway#medium_changer_type}.
        :param smb_active_directory_settings: smb_active_directory_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#smb_active_directory_settings StoragegatewayGateway#smb_active_directory_settings}
        :param smb_file_share_visibility: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#smb_file_share_visibility StoragegatewayGateway#smb_file_share_visibility}.
        :param smb_guest_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#smb_guest_password StoragegatewayGateway#smb_guest_password}.
        :param smb_security_strategy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#smb_security_strategy StoragegatewayGateway#smb_security_strategy}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#tags StoragegatewayGateway#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#tags_all StoragegatewayGateway#tags_all}.
        :param tape_drive_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#tape_drive_type StoragegatewayGateway#tape_drive_type}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#timeouts StoragegatewayGateway#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__326691d0d89768066da3e4ff77f6ff8d1b09e56db170a6cc7087637358afae10)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = StoragegatewayGatewayConfig(
            gateway_name=gateway_name,
            gateway_timezone=gateway_timezone,
            activation_key=activation_key,
            average_download_rate_limit_in_bits_per_sec=average_download_rate_limit_in_bits_per_sec,
            average_upload_rate_limit_in_bits_per_sec=average_upload_rate_limit_in_bits_per_sec,
            cloudwatch_log_group_arn=cloudwatch_log_group_arn,
            gateway_ip_address=gateway_ip_address,
            gateway_type=gateway_type,
            gateway_vpc_endpoint=gateway_vpc_endpoint,
            id=id,
            maintenance_start_time=maintenance_start_time,
            medium_changer_type=medium_changer_type,
            smb_active_directory_settings=smb_active_directory_settings,
            smb_file_share_visibility=smb_file_share_visibility,
            smb_guest_password=smb_guest_password,
            smb_security_strategy=smb_security_strategy,
            tags=tags,
            tags_all=tags_all,
            tape_drive_type=tape_drive_type,
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
        '''Generates CDKTF code for importing a StoragegatewayGateway resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the StoragegatewayGateway to import.
        :param import_from_id: The id of the existing StoragegatewayGateway that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the StoragegatewayGateway to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dd9c918ca010c5ca1bac5c88ebff242aa3b3a94349689fcbbe9bd0684c9886b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putMaintenanceStartTime")
    def put_maintenance_start_time(
        self,
        *,
        hour_of_day: jsii.Number,
        day_of_month: typing.Optional[builtins.str] = None,
        day_of_week: typing.Optional[builtins.str] = None,
        minute_of_hour: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hour_of_day: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#hour_of_day StoragegatewayGateway#hour_of_day}.
        :param day_of_month: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#day_of_month StoragegatewayGateway#day_of_month}.
        :param day_of_week: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#day_of_week StoragegatewayGateway#day_of_week}.
        :param minute_of_hour: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#minute_of_hour StoragegatewayGateway#minute_of_hour}.
        '''
        value = StoragegatewayGatewayMaintenanceStartTime(
            hour_of_day=hour_of_day,
            day_of_month=day_of_month,
            day_of_week=day_of_week,
            minute_of_hour=minute_of_hour,
        )

        return typing.cast(None, jsii.invoke(self, "putMaintenanceStartTime", [value]))

    @jsii.member(jsii_name="putSmbActiveDirectorySettings")
    def put_smb_active_directory_settings(
        self,
        *,
        domain_name: builtins.str,
        password: builtins.str,
        username: builtins.str,
        domain_controllers: typing.Optional[typing.Sequence[builtins.str]] = None,
        organizational_unit: typing.Optional[builtins.str] = None,
        timeout_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param domain_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#domain_name StoragegatewayGateway#domain_name}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#password StoragegatewayGateway#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#username StoragegatewayGateway#username}.
        :param domain_controllers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#domain_controllers StoragegatewayGateway#domain_controllers}.
        :param organizational_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#organizational_unit StoragegatewayGateway#organizational_unit}.
        :param timeout_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#timeout_in_seconds StoragegatewayGateway#timeout_in_seconds}.
        '''
        value = StoragegatewayGatewaySmbActiveDirectorySettings(
            domain_name=domain_name,
            password=password,
            username=username,
            domain_controllers=domain_controllers,
            organizational_unit=organizational_unit,
            timeout_in_seconds=timeout_in_seconds,
        )

        return typing.cast(None, jsii.invoke(self, "putSmbActiveDirectorySettings", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(self, *, create: typing.Optional[builtins.str] = None) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#create StoragegatewayGateway#create}.
        '''
        value = StoragegatewayGatewayTimeouts(create=create)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetActivationKey")
    def reset_activation_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActivationKey", []))

    @jsii.member(jsii_name="resetAverageDownloadRateLimitInBitsPerSec")
    def reset_average_download_rate_limit_in_bits_per_sec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAverageDownloadRateLimitInBitsPerSec", []))

    @jsii.member(jsii_name="resetAverageUploadRateLimitInBitsPerSec")
    def reset_average_upload_rate_limit_in_bits_per_sec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAverageUploadRateLimitInBitsPerSec", []))

    @jsii.member(jsii_name="resetCloudwatchLogGroupArn")
    def reset_cloudwatch_log_group_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchLogGroupArn", []))

    @jsii.member(jsii_name="resetGatewayIpAddress")
    def reset_gateway_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGatewayIpAddress", []))

    @jsii.member(jsii_name="resetGatewayType")
    def reset_gateway_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGatewayType", []))

    @jsii.member(jsii_name="resetGatewayVpcEndpoint")
    def reset_gateway_vpc_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGatewayVpcEndpoint", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMaintenanceStartTime")
    def reset_maintenance_start_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintenanceStartTime", []))

    @jsii.member(jsii_name="resetMediumChangerType")
    def reset_medium_changer_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMediumChangerType", []))

    @jsii.member(jsii_name="resetSmbActiveDirectorySettings")
    def reset_smb_active_directory_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSmbActiveDirectorySettings", []))

    @jsii.member(jsii_name="resetSmbFileShareVisibility")
    def reset_smb_file_share_visibility(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSmbFileShareVisibility", []))

    @jsii.member(jsii_name="resetSmbGuestPassword")
    def reset_smb_guest_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSmbGuestPassword", []))

    @jsii.member(jsii_name="resetSmbSecurityStrategy")
    def reset_smb_security_strategy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSmbSecurityStrategy", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTapeDriveType")
    def reset_tape_drive_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTapeDriveType", []))

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
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="ec2InstanceId")
    def ec2_instance_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ec2InstanceId"))

    @builtins.property
    @jsii.member(jsii_name="endpointType")
    def endpoint_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpointType"))

    @builtins.property
    @jsii.member(jsii_name="gatewayId")
    def gateway_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gatewayId"))

    @builtins.property
    @jsii.member(jsii_name="gatewayNetworkInterface")
    def gateway_network_interface(
        self,
    ) -> "StoragegatewayGatewayGatewayNetworkInterfaceList":
        return typing.cast("StoragegatewayGatewayGatewayNetworkInterfaceList", jsii.get(self, "gatewayNetworkInterface"))

    @builtins.property
    @jsii.member(jsii_name="hostEnvironment")
    def host_environment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostEnvironment"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceStartTime")
    def maintenance_start_time(
        self,
    ) -> "StoragegatewayGatewayMaintenanceStartTimeOutputReference":
        return typing.cast("StoragegatewayGatewayMaintenanceStartTimeOutputReference", jsii.get(self, "maintenanceStartTime"))

    @builtins.property
    @jsii.member(jsii_name="smbActiveDirectorySettings")
    def smb_active_directory_settings(
        self,
    ) -> "StoragegatewayGatewaySmbActiveDirectorySettingsOutputReference":
        return typing.cast("StoragegatewayGatewaySmbActiveDirectorySettingsOutputReference", jsii.get(self, "smbActiveDirectorySettings"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "StoragegatewayGatewayTimeoutsOutputReference":
        return typing.cast("StoragegatewayGatewayTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="activationKeyInput")
    def activation_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "activationKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="averageDownloadRateLimitInBitsPerSecInput")
    def average_download_rate_limit_in_bits_per_sec_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "averageDownloadRateLimitInBitsPerSecInput"))

    @builtins.property
    @jsii.member(jsii_name="averageUploadRateLimitInBitsPerSecInput")
    def average_upload_rate_limit_in_bits_per_sec_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "averageUploadRateLimitInBitsPerSecInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLogGroupArnInput")
    def cloudwatch_log_group_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudwatchLogGroupArnInput"))

    @builtins.property
    @jsii.member(jsii_name="gatewayIpAddressInput")
    def gateway_ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gatewayIpAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="gatewayNameInput")
    def gateway_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gatewayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="gatewayTimezoneInput")
    def gateway_timezone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gatewayTimezoneInput"))

    @builtins.property
    @jsii.member(jsii_name="gatewayTypeInput")
    def gateway_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gatewayTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="gatewayVpcEndpointInput")
    def gateway_vpc_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gatewayVpcEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceStartTimeInput")
    def maintenance_start_time_input(
        self,
    ) -> typing.Optional["StoragegatewayGatewayMaintenanceStartTime"]:
        return typing.cast(typing.Optional["StoragegatewayGatewayMaintenanceStartTime"], jsii.get(self, "maintenanceStartTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="mediumChangerTypeInput")
    def medium_changer_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mediumChangerTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="smbActiveDirectorySettingsInput")
    def smb_active_directory_settings_input(
        self,
    ) -> typing.Optional["StoragegatewayGatewaySmbActiveDirectorySettings"]:
        return typing.cast(typing.Optional["StoragegatewayGatewaySmbActiveDirectorySettings"], jsii.get(self, "smbActiveDirectorySettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="smbFileShareVisibilityInput")
    def smb_file_share_visibility_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "smbFileShareVisibilityInput"))

    @builtins.property
    @jsii.member(jsii_name="smbGuestPasswordInput")
    def smb_guest_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "smbGuestPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="smbSecurityStrategyInput")
    def smb_security_strategy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "smbSecurityStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsAllInput")
    def tags_all_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsAllInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="tapeDriveTypeInput")
    def tape_drive_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tapeDriveTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "StoragegatewayGatewayTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "StoragegatewayGatewayTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="activationKey")
    def activation_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "activationKey"))

    @activation_key.setter
    def activation_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28143989496c2ebce0d2941428c711c744ca1cb43ae987cc20f7d6106c6273ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "activationKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="averageDownloadRateLimitInBitsPerSec")
    def average_download_rate_limit_in_bits_per_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "averageDownloadRateLimitInBitsPerSec"))

    @average_download_rate_limit_in_bits_per_sec.setter
    def average_download_rate_limit_in_bits_per_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__701f12ef3286b2c48574c30abe58321172f39b5ec55d480504a5d3283ae90605)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "averageDownloadRateLimitInBitsPerSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="averageUploadRateLimitInBitsPerSec")
    def average_upload_rate_limit_in_bits_per_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "averageUploadRateLimitInBitsPerSec"))

    @average_upload_rate_limit_in_bits_per_sec.setter
    def average_upload_rate_limit_in_bits_per_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf9d6e2eb8330b87125c2c32a67d295c498983b4c0123b23d9618470b6229315)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "averageUploadRateLimitInBitsPerSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLogGroupArn")
    def cloudwatch_log_group_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudwatchLogGroupArn"))

    @cloudwatch_log_group_arn.setter
    def cloudwatch_log_group_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4da7e88a97b1ab95d9329eaf7d0b2516d889628822f67ee28f20bbb82cfc3599)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudwatchLogGroupArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gatewayIpAddress")
    def gateway_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gatewayIpAddress"))

    @gateway_ip_address.setter
    def gateway_ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8738faaa935d8c1d152b810410ed4aee409a043e37d94fd55c3f136dec2ca21a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gatewayIpAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gatewayName")
    def gateway_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gatewayName"))

    @gateway_name.setter
    def gateway_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34e9ce5f33fb95b803724d629c52339be558f880e958e879b7cf8350f919619a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gatewayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gatewayTimezone")
    def gateway_timezone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gatewayTimezone"))

    @gateway_timezone.setter
    def gateway_timezone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ec4305a1a449f4e16127834bd578b2fd505ef2af8ffcbdfa79f40fab3717924)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gatewayTimezone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gatewayType")
    def gateway_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gatewayType"))

    @gateway_type.setter
    def gateway_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ee40551b66e251897332cb0de5483efe2bf861cb54f63ba054975f561abb60d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gatewayType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gatewayVpcEndpoint")
    def gateway_vpc_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gatewayVpcEndpoint"))

    @gateway_vpc_endpoint.setter
    def gateway_vpc_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1332adbb22e295fd2288f1d75afbab6f8fbb0b5dd6fc1d8218569395a1e68ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gatewayVpcEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__897eb64e34a687baedff661a6618e8615f2c77716e7d606585f4784f6d1468a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mediumChangerType")
    def medium_changer_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mediumChangerType"))

    @medium_changer_type.setter
    def medium_changer_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f17fe6571e38e23cbab8d7815265b9bfef6d3998c0b263ae7da843952e63c12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mediumChangerType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="smbFileShareVisibility")
    def smb_file_share_visibility(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "smbFileShareVisibility"))

    @smb_file_share_visibility.setter
    def smb_file_share_visibility(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54339fb1306a7bc66ab474e59978833a25a23e2ad27ca52868b9aa7d41b9fa69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "smbFileShareVisibility", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="smbGuestPassword")
    def smb_guest_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "smbGuestPassword"))

    @smb_guest_password.setter
    def smb_guest_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11055e595bd89c61bd31c21b2b6d24e12e5d1406c94714b5ba2345652c8100dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "smbGuestPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="smbSecurityStrategy")
    def smb_security_strategy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "smbSecurityStrategy"))

    @smb_security_strategy.setter
    def smb_security_strategy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dbd496f82c20c352db2e413f00806e25435f062578004445c1d7f943f850cb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "smbSecurityStrategy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c918159ed71ac63f22675f22a11e8efcdf3c279a61270fcc37adba4e2b5aa753)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daa0fa2ac812beefb781306345cf613a36728ec05f652a773ea64ad265e18ec1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tapeDriveType")
    def tape_drive_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tapeDriveType"))

    @tape_drive_type.setter
    def tape_drive_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c699b3e0d170e810da0e04e6739ae74b3f1d6699d1570159d0e70801e5cdf9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tapeDriveType", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.storagegatewayGateway.StoragegatewayGatewayConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "gateway_name": "gatewayName",
        "gateway_timezone": "gatewayTimezone",
        "activation_key": "activationKey",
        "average_download_rate_limit_in_bits_per_sec": "averageDownloadRateLimitInBitsPerSec",
        "average_upload_rate_limit_in_bits_per_sec": "averageUploadRateLimitInBitsPerSec",
        "cloudwatch_log_group_arn": "cloudwatchLogGroupArn",
        "gateway_ip_address": "gatewayIpAddress",
        "gateway_type": "gatewayType",
        "gateway_vpc_endpoint": "gatewayVpcEndpoint",
        "id": "id",
        "maintenance_start_time": "maintenanceStartTime",
        "medium_changer_type": "mediumChangerType",
        "smb_active_directory_settings": "smbActiveDirectorySettings",
        "smb_file_share_visibility": "smbFileShareVisibility",
        "smb_guest_password": "smbGuestPassword",
        "smb_security_strategy": "smbSecurityStrategy",
        "tags": "tags",
        "tags_all": "tagsAll",
        "tape_drive_type": "tapeDriveType",
        "timeouts": "timeouts",
    },
)
class StoragegatewayGatewayConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        gateway_name: builtins.str,
        gateway_timezone: builtins.str,
        activation_key: typing.Optional[builtins.str] = None,
        average_download_rate_limit_in_bits_per_sec: typing.Optional[jsii.Number] = None,
        average_upload_rate_limit_in_bits_per_sec: typing.Optional[jsii.Number] = None,
        cloudwatch_log_group_arn: typing.Optional[builtins.str] = None,
        gateway_ip_address: typing.Optional[builtins.str] = None,
        gateway_type: typing.Optional[builtins.str] = None,
        gateway_vpc_endpoint: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        maintenance_start_time: typing.Optional[typing.Union["StoragegatewayGatewayMaintenanceStartTime", typing.Dict[builtins.str, typing.Any]]] = None,
        medium_changer_type: typing.Optional[builtins.str] = None,
        smb_active_directory_settings: typing.Optional[typing.Union["StoragegatewayGatewaySmbActiveDirectorySettings", typing.Dict[builtins.str, typing.Any]]] = None,
        smb_file_share_visibility: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        smb_guest_password: typing.Optional[builtins.str] = None,
        smb_security_strategy: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tape_drive_type: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["StoragegatewayGatewayTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param gateway_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#gateway_name StoragegatewayGateway#gateway_name}.
        :param gateway_timezone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#gateway_timezone StoragegatewayGateway#gateway_timezone}.
        :param activation_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#activation_key StoragegatewayGateway#activation_key}.
        :param average_download_rate_limit_in_bits_per_sec: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#average_download_rate_limit_in_bits_per_sec StoragegatewayGateway#average_download_rate_limit_in_bits_per_sec}.
        :param average_upload_rate_limit_in_bits_per_sec: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#average_upload_rate_limit_in_bits_per_sec StoragegatewayGateway#average_upload_rate_limit_in_bits_per_sec}.
        :param cloudwatch_log_group_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#cloudwatch_log_group_arn StoragegatewayGateway#cloudwatch_log_group_arn}.
        :param gateway_ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#gateway_ip_address StoragegatewayGateway#gateway_ip_address}.
        :param gateway_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#gateway_type StoragegatewayGateway#gateway_type}.
        :param gateway_vpc_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#gateway_vpc_endpoint StoragegatewayGateway#gateway_vpc_endpoint}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#id StoragegatewayGateway#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param maintenance_start_time: maintenance_start_time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#maintenance_start_time StoragegatewayGateway#maintenance_start_time}
        :param medium_changer_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#medium_changer_type StoragegatewayGateway#medium_changer_type}.
        :param smb_active_directory_settings: smb_active_directory_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#smb_active_directory_settings StoragegatewayGateway#smb_active_directory_settings}
        :param smb_file_share_visibility: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#smb_file_share_visibility StoragegatewayGateway#smb_file_share_visibility}.
        :param smb_guest_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#smb_guest_password StoragegatewayGateway#smb_guest_password}.
        :param smb_security_strategy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#smb_security_strategy StoragegatewayGateway#smb_security_strategy}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#tags StoragegatewayGateway#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#tags_all StoragegatewayGateway#tags_all}.
        :param tape_drive_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#tape_drive_type StoragegatewayGateway#tape_drive_type}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#timeouts StoragegatewayGateway#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(maintenance_start_time, dict):
            maintenance_start_time = StoragegatewayGatewayMaintenanceStartTime(**maintenance_start_time)
        if isinstance(smb_active_directory_settings, dict):
            smb_active_directory_settings = StoragegatewayGatewaySmbActiveDirectorySettings(**smb_active_directory_settings)
        if isinstance(timeouts, dict):
            timeouts = StoragegatewayGatewayTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28d989eaf1a36acd1c91dc8f7c410ca1f46c1d16e54335d9308274315581f31c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument gateway_name", value=gateway_name, expected_type=type_hints["gateway_name"])
            check_type(argname="argument gateway_timezone", value=gateway_timezone, expected_type=type_hints["gateway_timezone"])
            check_type(argname="argument activation_key", value=activation_key, expected_type=type_hints["activation_key"])
            check_type(argname="argument average_download_rate_limit_in_bits_per_sec", value=average_download_rate_limit_in_bits_per_sec, expected_type=type_hints["average_download_rate_limit_in_bits_per_sec"])
            check_type(argname="argument average_upload_rate_limit_in_bits_per_sec", value=average_upload_rate_limit_in_bits_per_sec, expected_type=type_hints["average_upload_rate_limit_in_bits_per_sec"])
            check_type(argname="argument cloudwatch_log_group_arn", value=cloudwatch_log_group_arn, expected_type=type_hints["cloudwatch_log_group_arn"])
            check_type(argname="argument gateway_ip_address", value=gateway_ip_address, expected_type=type_hints["gateway_ip_address"])
            check_type(argname="argument gateway_type", value=gateway_type, expected_type=type_hints["gateway_type"])
            check_type(argname="argument gateway_vpc_endpoint", value=gateway_vpc_endpoint, expected_type=type_hints["gateway_vpc_endpoint"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument maintenance_start_time", value=maintenance_start_time, expected_type=type_hints["maintenance_start_time"])
            check_type(argname="argument medium_changer_type", value=medium_changer_type, expected_type=type_hints["medium_changer_type"])
            check_type(argname="argument smb_active_directory_settings", value=smb_active_directory_settings, expected_type=type_hints["smb_active_directory_settings"])
            check_type(argname="argument smb_file_share_visibility", value=smb_file_share_visibility, expected_type=type_hints["smb_file_share_visibility"])
            check_type(argname="argument smb_guest_password", value=smb_guest_password, expected_type=type_hints["smb_guest_password"])
            check_type(argname="argument smb_security_strategy", value=smb_security_strategy, expected_type=type_hints["smb_security_strategy"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument tape_drive_type", value=tape_drive_type, expected_type=type_hints["tape_drive_type"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "gateway_name": gateway_name,
            "gateway_timezone": gateway_timezone,
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
        if activation_key is not None:
            self._values["activation_key"] = activation_key
        if average_download_rate_limit_in_bits_per_sec is not None:
            self._values["average_download_rate_limit_in_bits_per_sec"] = average_download_rate_limit_in_bits_per_sec
        if average_upload_rate_limit_in_bits_per_sec is not None:
            self._values["average_upload_rate_limit_in_bits_per_sec"] = average_upload_rate_limit_in_bits_per_sec
        if cloudwatch_log_group_arn is not None:
            self._values["cloudwatch_log_group_arn"] = cloudwatch_log_group_arn
        if gateway_ip_address is not None:
            self._values["gateway_ip_address"] = gateway_ip_address
        if gateway_type is not None:
            self._values["gateway_type"] = gateway_type
        if gateway_vpc_endpoint is not None:
            self._values["gateway_vpc_endpoint"] = gateway_vpc_endpoint
        if id is not None:
            self._values["id"] = id
        if maintenance_start_time is not None:
            self._values["maintenance_start_time"] = maintenance_start_time
        if medium_changer_type is not None:
            self._values["medium_changer_type"] = medium_changer_type
        if smb_active_directory_settings is not None:
            self._values["smb_active_directory_settings"] = smb_active_directory_settings
        if smb_file_share_visibility is not None:
            self._values["smb_file_share_visibility"] = smb_file_share_visibility
        if smb_guest_password is not None:
            self._values["smb_guest_password"] = smb_guest_password
        if smb_security_strategy is not None:
            self._values["smb_security_strategy"] = smb_security_strategy
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if tape_drive_type is not None:
            self._values["tape_drive_type"] = tape_drive_type
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
    def gateway_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#gateway_name StoragegatewayGateway#gateway_name}.'''
        result = self._values.get("gateway_name")
        assert result is not None, "Required property 'gateway_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gateway_timezone(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#gateway_timezone StoragegatewayGateway#gateway_timezone}.'''
        result = self._values.get("gateway_timezone")
        assert result is not None, "Required property 'gateway_timezone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def activation_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#activation_key StoragegatewayGateway#activation_key}.'''
        result = self._values.get("activation_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def average_download_rate_limit_in_bits_per_sec(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#average_download_rate_limit_in_bits_per_sec StoragegatewayGateway#average_download_rate_limit_in_bits_per_sec}.'''
        result = self._values.get("average_download_rate_limit_in_bits_per_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def average_upload_rate_limit_in_bits_per_sec(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#average_upload_rate_limit_in_bits_per_sec StoragegatewayGateway#average_upload_rate_limit_in_bits_per_sec}.'''
        result = self._values.get("average_upload_rate_limit_in_bits_per_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cloudwatch_log_group_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#cloudwatch_log_group_arn StoragegatewayGateway#cloudwatch_log_group_arn}.'''
        result = self._values.get("cloudwatch_log_group_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gateway_ip_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#gateway_ip_address StoragegatewayGateway#gateway_ip_address}.'''
        result = self._values.get("gateway_ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gateway_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#gateway_type StoragegatewayGateway#gateway_type}.'''
        result = self._values.get("gateway_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gateway_vpc_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#gateway_vpc_endpoint StoragegatewayGateway#gateway_vpc_endpoint}.'''
        result = self._values.get("gateway_vpc_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#id StoragegatewayGateway#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintenance_start_time(
        self,
    ) -> typing.Optional["StoragegatewayGatewayMaintenanceStartTime"]:
        '''maintenance_start_time block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#maintenance_start_time StoragegatewayGateway#maintenance_start_time}
        '''
        result = self._values.get("maintenance_start_time")
        return typing.cast(typing.Optional["StoragegatewayGatewayMaintenanceStartTime"], result)

    @builtins.property
    def medium_changer_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#medium_changer_type StoragegatewayGateway#medium_changer_type}.'''
        result = self._values.get("medium_changer_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def smb_active_directory_settings(
        self,
    ) -> typing.Optional["StoragegatewayGatewaySmbActiveDirectorySettings"]:
        '''smb_active_directory_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#smb_active_directory_settings StoragegatewayGateway#smb_active_directory_settings}
        '''
        result = self._values.get("smb_active_directory_settings")
        return typing.cast(typing.Optional["StoragegatewayGatewaySmbActiveDirectorySettings"], result)

    @builtins.property
    def smb_file_share_visibility(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#smb_file_share_visibility StoragegatewayGateway#smb_file_share_visibility}.'''
        result = self._values.get("smb_file_share_visibility")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def smb_guest_password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#smb_guest_password StoragegatewayGateway#smb_guest_password}.'''
        result = self._values.get("smb_guest_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def smb_security_strategy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#smb_security_strategy StoragegatewayGateway#smb_security_strategy}.'''
        result = self._values.get("smb_security_strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#tags StoragegatewayGateway#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#tags_all StoragegatewayGateway#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tape_drive_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#tape_drive_type StoragegatewayGateway#tape_drive_type}.'''
        result = self._values.get("tape_drive_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["StoragegatewayGatewayTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#timeouts StoragegatewayGateway#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["StoragegatewayGatewayTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StoragegatewayGatewayConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.storagegatewayGateway.StoragegatewayGatewayGatewayNetworkInterface",
    jsii_struct_bases=[],
    name_mapping={},
)
class StoragegatewayGatewayGatewayNetworkInterface:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StoragegatewayGatewayGatewayNetworkInterface(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StoragegatewayGatewayGatewayNetworkInterfaceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.storagegatewayGateway.StoragegatewayGatewayGatewayNetworkInterfaceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__241c06fc5035f1ce49e94b659f9dd155d26c3e80e511159e6af30fec4b7bd99a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "StoragegatewayGatewayGatewayNetworkInterfaceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9946e24a0ce52790089bcb8955e00ddd2f43982767eb11345f46a79fa6b1d268)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("StoragegatewayGatewayGatewayNetworkInterfaceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a215d4ba0e1a7332902868fc9ebc3d6b08f3f8fe192eb1a1bbd6746129bf7cc1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b109ede8b3017033b3ec48faea099cb2b233b76785f6b2a2d4e92787eaa44a2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__225ab7bf892da0c595e0c50b6769659503a49f0c4fb87635e57d52cb3075a2d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class StoragegatewayGatewayGatewayNetworkInterfaceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.storagegatewayGateway.StoragegatewayGatewayGatewayNetworkInterfaceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f131fcde60d2a7ed48041c6a15ba81ae1e8e436e6f1fc7579d0fcd6ff70bcbb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="ipv4Address")
    def ipv4_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv4Address"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StoragegatewayGatewayGatewayNetworkInterface]:
        return typing.cast(typing.Optional[StoragegatewayGatewayGatewayNetworkInterface], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StoragegatewayGatewayGatewayNetworkInterface],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01a2f4ed22eb61521aa33646e2b4885af05d814a62d1b924b13f97c7cad687a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.storagegatewayGateway.StoragegatewayGatewayMaintenanceStartTime",
    jsii_struct_bases=[],
    name_mapping={
        "hour_of_day": "hourOfDay",
        "day_of_month": "dayOfMonth",
        "day_of_week": "dayOfWeek",
        "minute_of_hour": "minuteOfHour",
    },
)
class StoragegatewayGatewayMaintenanceStartTime:
    def __init__(
        self,
        *,
        hour_of_day: jsii.Number,
        day_of_month: typing.Optional[builtins.str] = None,
        day_of_week: typing.Optional[builtins.str] = None,
        minute_of_hour: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hour_of_day: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#hour_of_day StoragegatewayGateway#hour_of_day}.
        :param day_of_month: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#day_of_month StoragegatewayGateway#day_of_month}.
        :param day_of_week: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#day_of_week StoragegatewayGateway#day_of_week}.
        :param minute_of_hour: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#minute_of_hour StoragegatewayGateway#minute_of_hour}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75b5e634cdee21cee9b09b88791bf7d1c2937bc925d7658ec48bd8a0bf009269)
            check_type(argname="argument hour_of_day", value=hour_of_day, expected_type=type_hints["hour_of_day"])
            check_type(argname="argument day_of_month", value=day_of_month, expected_type=type_hints["day_of_month"])
            check_type(argname="argument day_of_week", value=day_of_week, expected_type=type_hints["day_of_week"])
            check_type(argname="argument minute_of_hour", value=minute_of_hour, expected_type=type_hints["minute_of_hour"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hour_of_day": hour_of_day,
        }
        if day_of_month is not None:
            self._values["day_of_month"] = day_of_month
        if day_of_week is not None:
            self._values["day_of_week"] = day_of_week
        if minute_of_hour is not None:
            self._values["minute_of_hour"] = minute_of_hour

    @builtins.property
    def hour_of_day(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#hour_of_day StoragegatewayGateway#hour_of_day}.'''
        result = self._values.get("hour_of_day")
        assert result is not None, "Required property 'hour_of_day' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def day_of_month(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#day_of_month StoragegatewayGateway#day_of_month}.'''
        result = self._values.get("day_of_month")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def day_of_week(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#day_of_week StoragegatewayGateway#day_of_week}.'''
        result = self._values.get("day_of_week")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def minute_of_hour(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#minute_of_hour StoragegatewayGateway#minute_of_hour}.'''
        result = self._values.get("minute_of_hour")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StoragegatewayGatewayMaintenanceStartTime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StoragegatewayGatewayMaintenanceStartTimeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.storagegatewayGateway.StoragegatewayGatewayMaintenanceStartTimeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f58db971410ddf4c0f539881d3e7e7d7ac42b9829d62f1367d6fca841add2cb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDayOfMonth")
    def reset_day_of_month(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDayOfMonth", []))

    @jsii.member(jsii_name="resetDayOfWeek")
    def reset_day_of_week(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDayOfWeek", []))

    @jsii.member(jsii_name="resetMinuteOfHour")
    def reset_minute_of_hour(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinuteOfHour", []))

    @builtins.property
    @jsii.member(jsii_name="dayOfMonthInput")
    def day_of_month_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dayOfMonthInput"))

    @builtins.property
    @jsii.member(jsii_name="dayOfWeekInput")
    def day_of_week_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dayOfWeekInput"))

    @builtins.property
    @jsii.member(jsii_name="hourOfDayInput")
    def hour_of_day_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hourOfDayInput"))

    @builtins.property
    @jsii.member(jsii_name="minuteOfHourInput")
    def minute_of_hour_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minuteOfHourInput"))

    @builtins.property
    @jsii.member(jsii_name="dayOfMonth")
    def day_of_month(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dayOfMonth"))

    @day_of_month.setter
    def day_of_month(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d42624394e46702e11aca8a2dc4a8b8b1033b2420def34796d3aa290cc9fb32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dayOfMonth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dayOfWeek")
    def day_of_week(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dayOfWeek"))

    @day_of_week.setter
    def day_of_week(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90b9b9a8b17449fe679acd57fef0878caac0aebc244d3cfc8e452f735c41d121)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dayOfWeek", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hourOfDay")
    def hour_of_day(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hourOfDay"))

    @hour_of_day.setter
    def hour_of_day(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b836336ee424cd70135f6ad80026cf9ed685d93871828a42762be93c550b674)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hourOfDay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minuteOfHour")
    def minute_of_hour(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minuteOfHour"))

    @minute_of_hour.setter
    def minute_of_hour(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__984401deba5771ce05d6b23433ea2a25ed5c6a0b62ceda9ac75d4a563315236a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minuteOfHour", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StoragegatewayGatewayMaintenanceStartTime]:
        return typing.cast(typing.Optional[StoragegatewayGatewayMaintenanceStartTime], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StoragegatewayGatewayMaintenanceStartTime],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22f363676adb89a17f7d98d18c08ed0a8f2564ce33c872ad02c850cc42ce35bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.storagegatewayGateway.StoragegatewayGatewaySmbActiveDirectorySettings",
    jsii_struct_bases=[],
    name_mapping={
        "domain_name": "domainName",
        "password": "password",
        "username": "username",
        "domain_controllers": "domainControllers",
        "organizational_unit": "organizationalUnit",
        "timeout_in_seconds": "timeoutInSeconds",
    },
)
class StoragegatewayGatewaySmbActiveDirectorySettings:
    def __init__(
        self,
        *,
        domain_name: builtins.str,
        password: builtins.str,
        username: builtins.str,
        domain_controllers: typing.Optional[typing.Sequence[builtins.str]] = None,
        organizational_unit: typing.Optional[builtins.str] = None,
        timeout_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param domain_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#domain_name StoragegatewayGateway#domain_name}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#password StoragegatewayGateway#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#username StoragegatewayGateway#username}.
        :param domain_controllers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#domain_controllers StoragegatewayGateway#domain_controllers}.
        :param organizational_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#organizational_unit StoragegatewayGateway#organizational_unit}.
        :param timeout_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#timeout_in_seconds StoragegatewayGateway#timeout_in_seconds}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97dd2aad11ba3b59ee5736ec2e1eee13a344867afa948d326af39a2c4306fda9)
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument domain_controllers", value=domain_controllers, expected_type=type_hints["domain_controllers"])
            check_type(argname="argument organizational_unit", value=organizational_unit, expected_type=type_hints["organizational_unit"])
            check_type(argname="argument timeout_in_seconds", value=timeout_in_seconds, expected_type=type_hints["timeout_in_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain_name": domain_name,
            "password": password,
            "username": username,
        }
        if domain_controllers is not None:
            self._values["domain_controllers"] = domain_controllers
        if organizational_unit is not None:
            self._values["organizational_unit"] = organizational_unit
        if timeout_in_seconds is not None:
            self._values["timeout_in_seconds"] = timeout_in_seconds

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#domain_name StoragegatewayGateway#domain_name}.'''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#password StoragegatewayGateway#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#username StoragegatewayGateway#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain_controllers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#domain_controllers StoragegatewayGateway#domain_controllers}.'''
        result = self._values.get("domain_controllers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def organizational_unit(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#organizational_unit StoragegatewayGateway#organizational_unit}.'''
        result = self._values.get("organizational_unit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#timeout_in_seconds StoragegatewayGateway#timeout_in_seconds}.'''
        result = self._values.get("timeout_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StoragegatewayGatewaySmbActiveDirectorySettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StoragegatewayGatewaySmbActiveDirectorySettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.storagegatewayGateway.StoragegatewayGatewaySmbActiveDirectorySettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5ce4c203832ba9bde464de928d28178cd12a04565fc055d2b20f5794c9aa821)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDomainControllers")
    def reset_domain_controllers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomainControllers", []))

    @jsii.member(jsii_name="resetOrganizationalUnit")
    def reset_organizational_unit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrganizationalUnit", []))

    @jsii.member(jsii_name="resetTimeoutInSeconds")
    def reset_timeout_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeoutInSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="activeDirectoryStatus")
    def active_directory_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "activeDirectoryStatus"))

    @builtins.property
    @jsii.member(jsii_name="domainControllersInput")
    def domain_controllers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "domainControllersInput"))

    @builtins.property
    @jsii.member(jsii_name="domainNameInput")
    def domain_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainNameInput"))

    @builtins.property
    @jsii.member(jsii_name="organizationalUnitInput")
    def organizational_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationalUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInSecondsInput")
    def timeout_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="domainControllers")
    def domain_controllers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "domainControllers"))

    @domain_controllers.setter
    def domain_controllers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75523504c6a5a6c47ec4ab5fb6aac0b7a8d4ff33163e92ae82358bdfccb8bda6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainControllers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @domain_name.setter
    def domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6acd28d3f0f92d7633dab632734e279107e5cf5789af188fa36ce08486ee0ef0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="organizationalUnit")
    def organizational_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organizationalUnit"))

    @organizational_unit.setter
    def organizational_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32aabe85d6ce923fdd604e99895c3f77b4fb7fea41bca3bd29c701846d7de51e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organizationalUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69f09ff9e88cda356ef6a87ce3da2f1162af36377342fc5b97dae6d833c9446f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutInSeconds")
    def timeout_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutInSeconds"))

    @timeout_in_seconds.setter
    def timeout_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b877651f0e98b90c7c084a4ca1ef230e7180289feb88dafc67c550a91afae46f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e3ee66c6bee34e09e2337b5c2a4471db6233733337aa54d1a0b79b35c823e6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StoragegatewayGatewaySmbActiveDirectorySettings]:
        return typing.cast(typing.Optional[StoragegatewayGatewaySmbActiveDirectorySettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StoragegatewayGatewaySmbActiveDirectorySettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52b4844c55ecd1f2bcf467e13c232d34bcd0aefd1fac2438efe26d6417e3cac3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.storagegatewayGateway.StoragegatewayGatewayTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create"},
)
class StoragegatewayGatewayTimeouts:
    def __init__(self, *, create: typing.Optional[builtins.str] = None) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#create StoragegatewayGateway#create}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__926baa1344db951a1689e32ad62084f5a9838947d3f5d1d74c79c2ffb41326ba)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/storagegateway_gateway#create StoragegatewayGateway#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StoragegatewayGatewayTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StoragegatewayGatewayTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.storagegatewayGateway.StoragegatewayGatewayTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3ab5baeb3b64bece7f1502d8d927d53d3323344f67747a7dc1864297cecfb3f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70bf8115e644f4ac35f9c18eb351a40e9f700508beeb946c643e017caa134e4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StoragegatewayGatewayTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StoragegatewayGatewayTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StoragegatewayGatewayTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__417a137764b7b2a120000494129f442d4fdeb40ac15fca528cc6d995608b6cd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "StoragegatewayGateway",
    "StoragegatewayGatewayConfig",
    "StoragegatewayGatewayGatewayNetworkInterface",
    "StoragegatewayGatewayGatewayNetworkInterfaceList",
    "StoragegatewayGatewayGatewayNetworkInterfaceOutputReference",
    "StoragegatewayGatewayMaintenanceStartTime",
    "StoragegatewayGatewayMaintenanceStartTimeOutputReference",
    "StoragegatewayGatewaySmbActiveDirectorySettings",
    "StoragegatewayGatewaySmbActiveDirectorySettingsOutputReference",
    "StoragegatewayGatewayTimeouts",
    "StoragegatewayGatewayTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__326691d0d89768066da3e4ff77f6ff8d1b09e56db170a6cc7087637358afae10(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    gateway_name: builtins.str,
    gateway_timezone: builtins.str,
    activation_key: typing.Optional[builtins.str] = None,
    average_download_rate_limit_in_bits_per_sec: typing.Optional[jsii.Number] = None,
    average_upload_rate_limit_in_bits_per_sec: typing.Optional[jsii.Number] = None,
    cloudwatch_log_group_arn: typing.Optional[builtins.str] = None,
    gateway_ip_address: typing.Optional[builtins.str] = None,
    gateway_type: typing.Optional[builtins.str] = None,
    gateway_vpc_endpoint: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    maintenance_start_time: typing.Optional[typing.Union[StoragegatewayGatewayMaintenanceStartTime, typing.Dict[builtins.str, typing.Any]]] = None,
    medium_changer_type: typing.Optional[builtins.str] = None,
    smb_active_directory_settings: typing.Optional[typing.Union[StoragegatewayGatewaySmbActiveDirectorySettings, typing.Dict[builtins.str, typing.Any]]] = None,
    smb_file_share_visibility: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    smb_guest_password: typing.Optional[builtins.str] = None,
    smb_security_strategy: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tape_drive_type: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[StoragegatewayGatewayTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__2dd9c918ca010c5ca1bac5c88ebff242aa3b3a94349689fcbbe9bd0684c9886b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28143989496c2ebce0d2941428c711c744ca1cb43ae987cc20f7d6106c6273ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__701f12ef3286b2c48574c30abe58321172f39b5ec55d480504a5d3283ae90605(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf9d6e2eb8330b87125c2c32a67d295c498983b4c0123b23d9618470b6229315(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4da7e88a97b1ab95d9329eaf7d0b2516d889628822f67ee28f20bbb82cfc3599(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8738faaa935d8c1d152b810410ed4aee409a043e37d94fd55c3f136dec2ca21a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34e9ce5f33fb95b803724d629c52339be558f880e958e879b7cf8350f919619a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ec4305a1a449f4e16127834bd578b2fd505ef2af8ffcbdfa79f40fab3717924(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ee40551b66e251897332cb0de5483efe2bf861cb54f63ba054975f561abb60d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1332adbb22e295fd2288f1d75afbab6f8fbb0b5dd6fc1d8218569395a1e68ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__897eb64e34a687baedff661a6618e8615f2c77716e7d606585f4784f6d1468a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f17fe6571e38e23cbab8d7815265b9bfef6d3998c0b263ae7da843952e63c12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54339fb1306a7bc66ab474e59978833a25a23e2ad27ca52868b9aa7d41b9fa69(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11055e595bd89c61bd31c21b2b6d24e12e5d1406c94714b5ba2345652c8100dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dbd496f82c20c352db2e413f00806e25435f062578004445c1d7f943f850cb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c918159ed71ac63f22675f22a11e8efcdf3c279a61270fcc37adba4e2b5aa753(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daa0fa2ac812beefb781306345cf613a36728ec05f652a773ea64ad265e18ec1(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c699b3e0d170e810da0e04e6739ae74b3f1d6699d1570159d0e70801e5cdf9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28d989eaf1a36acd1c91dc8f7c410ca1f46c1d16e54335d9308274315581f31c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    gateway_name: builtins.str,
    gateway_timezone: builtins.str,
    activation_key: typing.Optional[builtins.str] = None,
    average_download_rate_limit_in_bits_per_sec: typing.Optional[jsii.Number] = None,
    average_upload_rate_limit_in_bits_per_sec: typing.Optional[jsii.Number] = None,
    cloudwatch_log_group_arn: typing.Optional[builtins.str] = None,
    gateway_ip_address: typing.Optional[builtins.str] = None,
    gateway_type: typing.Optional[builtins.str] = None,
    gateway_vpc_endpoint: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    maintenance_start_time: typing.Optional[typing.Union[StoragegatewayGatewayMaintenanceStartTime, typing.Dict[builtins.str, typing.Any]]] = None,
    medium_changer_type: typing.Optional[builtins.str] = None,
    smb_active_directory_settings: typing.Optional[typing.Union[StoragegatewayGatewaySmbActiveDirectorySettings, typing.Dict[builtins.str, typing.Any]]] = None,
    smb_file_share_visibility: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    smb_guest_password: typing.Optional[builtins.str] = None,
    smb_security_strategy: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tape_drive_type: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[StoragegatewayGatewayTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__241c06fc5035f1ce49e94b659f9dd155d26c3e80e511159e6af30fec4b7bd99a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9946e24a0ce52790089bcb8955e00ddd2f43982767eb11345f46a79fa6b1d268(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a215d4ba0e1a7332902868fc9ebc3d6b08f3f8fe192eb1a1bbd6746129bf7cc1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b109ede8b3017033b3ec48faea099cb2b233b76785f6b2a2d4e92787eaa44a2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__225ab7bf892da0c595e0c50b6769659503a49f0c4fb87635e57d52cb3075a2d7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f131fcde60d2a7ed48041c6a15ba81ae1e8e436e6f1fc7579d0fcd6ff70bcbb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01a2f4ed22eb61521aa33646e2b4885af05d814a62d1b924b13f97c7cad687a5(
    value: typing.Optional[StoragegatewayGatewayGatewayNetworkInterface],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75b5e634cdee21cee9b09b88791bf7d1c2937bc925d7658ec48bd8a0bf009269(
    *,
    hour_of_day: jsii.Number,
    day_of_month: typing.Optional[builtins.str] = None,
    day_of_week: typing.Optional[builtins.str] = None,
    minute_of_hour: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f58db971410ddf4c0f539881d3e7e7d7ac42b9829d62f1367d6fca841add2cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d42624394e46702e11aca8a2dc4a8b8b1033b2420def34796d3aa290cc9fb32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90b9b9a8b17449fe679acd57fef0878caac0aebc244d3cfc8e452f735c41d121(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b836336ee424cd70135f6ad80026cf9ed685d93871828a42762be93c550b674(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__984401deba5771ce05d6b23433ea2a25ed5c6a0b62ceda9ac75d4a563315236a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22f363676adb89a17f7d98d18c08ed0a8f2564ce33c872ad02c850cc42ce35bc(
    value: typing.Optional[StoragegatewayGatewayMaintenanceStartTime],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97dd2aad11ba3b59ee5736ec2e1eee13a344867afa948d326af39a2c4306fda9(
    *,
    domain_name: builtins.str,
    password: builtins.str,
    username: builtins.str,
    domain_controllers: typing.Optional[typing.Sequence[builtins.str]] = None,
    organizational_unit: typing.Optional[builtins.str] = None,
    timeout_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5ce4c203832ba9bde464de928d28178cd12a04565fc055d2b20f5794c9aa821(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75523504c6a5a6c47ec4ab5fb6aac0b7a8d4ff33163e92ae82358bdfccb8bda6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6acd28d3f0f92d7633dab632734e279107e5cf5789af188fa36ce08486ee0ef0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32aabe85d6ce923fdd604e99895c3f77b4fb7fea41bca3bd29c701846d7de51e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69f09ff9e88cda356ef6a87ce3da2f1162af36377342fc5b97dae6d833c9446f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b877651f0e98b90c7c084a4ca1ef230e7180289feb88dafc67c550a91afae46f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e3ee66c6bee34e09e2337b5c2a4471db6233733337aa54d1a0b79b35c823e6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52b4844c55ecd1f2bcf467e13c232d34bcd0aefd1fac2438efe26d6417e3cac3(
    value: typing.Optional[StoragegatewayGatewaySmbActiveDirectorySettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__926baa1344db951a1689e32ad62084f5a9838947d3f5d1d74c79c2ffb41326ba(
    *,
    create: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3ab5baeb3b64bece7f1502d8d927d53d3323344f67747a7dc1864297cecfb3f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70bf8115e644f4ac35f9c18eb351a40e9f700508beeb946c643e017caa134e4b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__417a137764b7b2a120000494129f442d4fdeb40ac15fca528cc6d995608b6cd4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StoragegatewayGatewayTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
