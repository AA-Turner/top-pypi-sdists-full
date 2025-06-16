r'''
# `google_looker_instance`

Refer to the Terraform Registry for docs: [`google_looker_instance`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance).
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


class GoogleLookerInstance(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleLookerInstance.GoogleLookerInstance",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance google_looker_instance}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        oauth_config: typing.Union["GoogleLookerInstanceOauthConfig", typing.Dict[builtins.str, typing.Any]],
        admin_settings: typing.Optional[typing.Union["GoogleLookerInstanceAdminSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        consumer_network: typing.Optional[builtins.str] = None,
        custom_domain: typing.Optional[typing.Union["GoogleLookerInstanceCustomDomain", typing.Dict[builtins.str, typing.Any]]] = None,
        deletion_policy: typing.Optional[builtins.str] = None,
        deny_maintenance_period: typing.Optional[typing.Union["GoogleLookerInstanceDenyMaintenancePeriod", typing.Dict[builtins.str, typing.Any]]] = None,
        encryption_config: typing.Optional[typing.Union["GoogleLookerInstanceEncryptionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        fips_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        maintenance_window: typing.Optional[typing.Union["GoogleLookerInstanceMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]] = None,
        platform_edition: typing.Optional[builtins.str] = None,
        private_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project: typing.Optional[builtins.str] = None,
        psc_config: typing.Optional[typing.Union["GoogleLookerInstancePscConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        psc_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        public_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        region: typing.Optional[builtins.str] = None,
        reserved_range: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleLookerInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        user_metadata: typing.Optional[typing.Union["GoogleLookerInstanceUserMetadata", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance google_looker_instance} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The ID of the instance or a fully qualified identifier for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#name GoogleLookerInstance#name}
        :param oauth_config: oauth_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#oauth_config GoogleLookerInstance#oauth_config}
        :param admin_settings: admin_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#admin_settings GoogleLookerInstance#admin_settings}
        :param consumer_network: Network name in the consumer project in the format of: projects/{project}/global/networks/{network} Note that the consumer network may be in a different GCP project than the consumer project that is hosting the Looker Instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#consumer_network GoogleLookerInstance#consumer_network}
        :param custom_domain: custom_domain block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#custom_domain GoogleLookerInstance#custom_domain}
        :param deletion_policy: Policy to determine if the cluster should be deleted forcefully. If setting deletion_policy = "FORCE", the Looker instance will be deleted regardless of its nested resources. If set to "DEFAULT", Looker instances that still have nested resources will return an error. Possible values: DEFAULT, FORCE Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#deletion_policy GoogleLookerInstance#deletion_policy}
        :param deny_maintenance_period: deny_maintenance_period block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#deny_maintenance_period GoogleLookerInstance#deny_maintenance_period}
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#encryption_config GoogleLookerInstance#encryption_config}
        :param fips_enabled: FIPS 140-2 Encryption enablement for Looker (Google Cloud Core). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#fips_enabled GoogleLookerInstance#fips_enabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#id GoogleLookerInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param maintenance_window: maintenance_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#maintenance_window GoogleLookerInstance#maintenance_window}
        :param platform_edition: Platform editions for a Looker instance. Each edition maps to a set of instance features, like its size. Must be one of these values: - LOOKER_CORE_TRIAL: trial instance (Currently Unavailable) - LOOKER_CORE_STANDARD: pay as you go standard instance (Currently Unavailable) - LOOKER_CORE_STANDARD_ANNUAL: subscription standard instance - LOOKER_CORE_ENTERPRISE_ANNUAL: subscription enterprise instance - LOOKER_CORE_EMBED_ANNUAL: subscription embed instance - LOOKER_CORE_NONPROD_STANDARD_ANNUAL: nonprod subscription standard instance - LOOKER_CORE_NONPROD_ENTERPRISE_ANNUAL: nonprod subscription enterprise instance - LOOKER_CORE_NONPROD_EMBED_ANNUAL: nonprod subscription embed instance Default value: "LOOKER_CORE_TRIAL" Possible values: ["LOOKER_CORE_TRIAL", "LOOKER_CORE_STANDARD", "LOOKER_CORE_STANDARD_ANNUAL", "LOOKER_CORE_ENTERPRISE_ANNUAL", "LOOKER_CORE_EMBED_ANNUAL", "LOOKER_CORE_NONPROD_STANDARD_ANNUAL", "LOOKER_CORE_NONPROD_ENTERPRISE_ANNUAL", "LOOKER_CORE_NONPROD_EMBED_ANNUAL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#platform_edition GoogleLookerInstance#platform_edition}
        :param private_ip_enabled: Whether private IP is enabled on the Looker instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#private_ip_enabled GoogleLookerInstance#private_ip_enabled}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#project GoogleLookerInstance#project}.
        :param psc_config: psc_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#psc_config GoogleLookerInstance#psc_config}
        :param psc_enabled: Whether Public Service Connect (PSC) is enabled on the Looker instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#psc_enabled GoogleLookerInstance#psc_enabled}
        :param public_ip_enabled: Whether public IP is enabled on the Looker instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#public_ip_enabled GoogleLookerInstance#public_ip_enabled}
        :param region: The name of the Looker region of the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#region GoogleLookerInstance#region}
        :param reserved_range: Name of a reserved IP address range within the consumer network, to be used for private service access connection. User may or may not specify this in a request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#reserved_range GoogleLookerInstance#reserved_range}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#timeouts GoogleLookerInstance#timeouts}
        :param user_metadata: user_metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#user_metadata GoogleLookerInstance#user_metadata}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75fc0bd078a1f4d6b895160bbb3e361c144807f6702482438fcaa6fb2acfaac5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleLookerInstanceConfig(
            name=name,
            oauth_config=oauth_config,
            admin_settings=admin_settings,
            consumer_network=consumer_network,
            custom_domain=custom_domain,
            deletion_policy=deletion_policy,
            deny_maintenance_period=deny_maintenance_period,
            encryption_config=encryption_config,
            fips_enabled=fips_enabled,
            id=id,
            maintenance_window=maintenance_window,
            platform_edition=platform_edition,
            private_ip_enabled=private_ip_enabled,
            project=project,
            psc_config=psc_config,
            psc_enabled=psc_enabled,
            public_ip_enabled=public_ip_enabled,
            region=region,
            reserved_range=reserved_range,
            timeouts=timeouts,
            user_metadata=user_metadata,
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
        '''Generates CDKTF code for importing a GoogleLookerInstance resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleLookerInstance to import.
        :param import_from_id: The id of the existing GoogleLookerInstance that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleLookerInstance to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0be6f0bfbfcdbe7eabbe6a668e3d435cdc129b1156c363db412595a747bea5c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAdminSettings")
    def put_admin_settings(
        self,
        *,
        allowed_email_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allowed_email_domains: Email domain allowlist for the instance. Define the email domains to which your users can deliver Looker (Google Cloud core) content. Updating this list will restart the instance. Updating the allowed email domains from terraform means the value provided will be considered as the entire list and not an amendment to the existing list of allowed email domains. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#allowed_email_domains GoogleLookerInstance#allowed_email_domains}
        '''
        value = GoogleLookerInstanceAdminSettings(
            allowed_email_domains=allowed_email_domains
        )

        return typing.cast(None, jsii.invoke(self, "putAdminSettings", [value]))

    @jsii.member(jsii_name="putCustomDomain")
    def put_custom_domain(
        self,
        *,
        domain: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param domain: Domain name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#domain GoogleLookerInstance#domain}
        '''
        value = GoogleLookerInstanceCustomDomain(domain=domain)

        return typing.cast(None, jsii.invoke(self, "putCustomDomain", [value]))

    @jsii.member(jsii_name="putDenyMaintenancePeriod")
    def put_deny_maintenance_period(
        self,
        *,
        end_date: typing.Union["GoogleLookerInstanceDenyMaintenancePeriodEndDate", typing.Dict[builtins.str, typing.Any]],
        start_date: typing.Union["GoogleLookerInstanceDenyMaintenancePeriodStartDate", typing.Dict[builtins.str, typing.Any]],
        time: typing.Union["GoogleLookerInstanceDenyMaintenancePeriodTime", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param end_date: end_date block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#end_date GoogleLookerInstance#end_date}
        :param start_date: start_date block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#start_date GoogleLookerInstance#start_date}
        :param time: time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#time GoogleLookerInstance#time}
        '''
        value = GoogleLookerInstanceDenyMaintenancePeriod(
            end_date=end_date, start_date=start_date, time=time
        )

        return typing.cast(None, jsii.invoke(self, "putDenyMaintenancePeriod", [value]))

    @jsii.member(jsii_name="putEncryptionConfig")
    def put_encryption_config(
        self,
        *,
        kms_key_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_name: Name of the customer managed encryption key (CMEK) in KMS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#kms_key_name GoogleLookerInstance#kms_key_name}
        '''
        value = GoogleLookerInstanceEncryptionConfig(kms_key_name=kms_key_name)

        return typing.cast(None, jsii.invoke(self, "putEncryptionConfig", [value]))

    @jsii.member(jsii_name="putMaintenanceWindow")
    def put_maintenance_window(
        self,
        *,
        day_of_week: builtins.str,
        start_time: typing.Union["GoogleLookerInstanceMaintenanceWindowStartTime", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param day_of_week: Required. Day of the week for this MaintenanceWindow (in UTC). - MONDAY: Monday - TUESDAY: Tuesday - WEDNESDAY: Wednesday - THURSDAY: Thursday - FRIDAY: Friday - SATURDAY: Saturday - SUNDAY: Sunday Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#day_of_week GoogleLookerInstance#day_of_week}
        :param start_time: start_time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#start_time GoogleLookerInstance#start_time}
        '''
        value = GoogleLookerInstanceMaintenanceWindow(
            day_of_week=day_of_week, start_time=start_time
        )

        return typing.cast(None, jsii.invoke(self, "putMaintenanceWindow", [value]))

    @jsii.member(jsii_name="putOauthConfig")
    def put_oauth_config(
        self,
        *,
        client_id: builtins.str,
        client_secret: builtins.str,
    ) -> None:
        '''
        :param client_id: The client ID for the Oauth config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#client_id GoogleLookerInstance#client_id}
        :param client_secret: The client secret for the Oauth config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#client_secret GoogleLookerInstance#client_secret}
        '''
        value = GoogleLookerInstanceOauthConfig(
            client_id=client_id, client_secret=client_secret
        )

        return typing.cast(None, jsii.invoke(self, "putOauthConfig", [value]))

    @jsii.member(jsii_name="putPscConfig")
    def put_psc_config(
        self,
        *,
        allowed_vpcs: typing.Optional[typing.Sequence[builtins.str]] = None,
        service_attachments: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleLookerInstancePscConfigServiceAttachments", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param allowed_vpcs: List of VPCs that are allowed ingress into the Looker instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#allowed_vpcs GoogleLookerInstance#allowed_vpcs}
        :param service_attachments: service_attachments block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#service_attachments GoogleLookerInstance#service_attachments}
        '''
        value = GoogleLookerInstancePscConfig(
            allowed_vpcs=allowed_vpcs, service_attachments=service_attachments
        )

        return typing.cast(None, jsii.invoke(self, "putPscConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#create GoogleLookerInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#delete GoogleLookerInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#update GoogleLookerInstance#update}.
        '''
        value = GoogleLookerInstanceTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putUserMetadata")
    def put_user_metadata(
        self,
        *,
        additional_developer_user_count: typing.Optional[jsii.Number] = None,
        additional_standard_user_count: typing.Optional[jsii.Number] = None,
        additional_viewer_user_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param additional_developer_user_count: Number of additional Developer Users to allocate to the Looker Instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#additional_developer_user_count GoogleLookerInstance#additional_developer_user_count}
        :param additional_standard_user_count: Number of additional Standard Users to allocate to the Looker Instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#additional_standard_user_count GoogleLookerInstance#additional_standard_user_count}
        :param additional_viewer_user_count: Number of additional Viewer Users to allocate to the Looker Instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#additional_viewer_user_count GoogleLookerInstance#additional_viewer_user_count}
        '''
        value = GoogleLookerInstanceUserMetadata(
            additional_developer_user_count=additional_developer_user_count,
            additional_standard_user_count=additional_standard_user_count,
            additional_viewer_user_count=additional_viewer_user_count,
        )

        return typing.cast(None, jsii.invoke(self, "putUserMetadata", [value]))

    @jsii.member(jsii_name="resetAdminSettings")
    def reset_admin_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminSettings", []))

    @jsii.member(jsii_name="resetConsumerNetwork")
    def reset_consumer_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsumerNetwork", []))

    @jsii.member(jsii_name="resetCustomDomain")
    def reset_custom_domain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomDomain", []))

    @jsii.member(jsii_name="resetDeletionPolicy")
    def reset_deletion_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeletionPolicy", []))

    @jsii.member(jsii_name="resetDenyMaintenancePeriod")
    def reset_deny_maintenance_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDenyMaintenancePeriod", []))

    @jsii.member(jsii_name="resetEncryptionConfig")
    def reset_encryption_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionConfig", []))

    @jsii.member(jsii_name="resetFipsEnabled")
    def reset_fips_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFipsEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMaintenanceWindow")
    def reset_maintenance_window(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintenanceWindow", []))

    @jsii.member(jsii_name="resetPlatformEdition")
    def reset_platform_edition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlatformEdition", []))

    @jsii.member(jsii_name="resetPrivateIpEnabled")
    def reset_private_ip_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateIpEnabled", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetPscConfig")
    def reset_psc_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPscConfig", []))

    @jsii.member(jsii_name="resetPscEnabled")
    def reset_psc_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPscEnabled", []))

    @jsii.member(jsii_name="resetPublicIpEnabled")
    def reset_public_ip_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicIpEnabled", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetReservedRange")
    def reset_reserved_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReservedRange", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUserMetadata")
    def reset_user_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserMetadata", []))

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
    @jsii.member(jsii_name="adminSettings")
    def admin_settings(self) -> "GoogleLookerInstanceAdminSettingsOutputReference":
        return typing.cast("GoogleLookerInstanceAdminSettingsOutputReference", jsii.get(self, "adminSettings"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="customDomain")
    def custom_domain(self) -> "GoogleLookerInstanceCustomDomainOutputReference":
        return typing.cast("GoogleLookerInstanceCustomDomainOutputReference", jsii.get(self, "customDomain"))

    @builtins.property
    @jsii.member(jsii_name="denyMaintenancePeriod")
    def deny_maintenance_period(
        self,
    ) -> "GoogleLookerInstanceDenyMaintenancePeriodOutputReference":
        return typing.cast("GoogleLookerInstanceDenyMaintenancePeriodOutputReference", jsii.get(self, "denyMaintenancePeriod"))

    @builtins.property
    @jsii.member(jsii_name="egressPublicIp")
    def egress_public_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "egressPublicIp"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfig")
    def encryption_config(
        self,
    ) -> "GoogleLookerInstanceEncryptionConfigOutputReference":
        return typing.cast("GoogleLookerInstanceEncryptionConfigOutputReference", jsii.get(self, "encryptionConfig"))

    @builtins.property
    @jsii.member(jsii_name="ingressPrivateIp")
    def ingress_private_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ingressPrivateIp"))

    @builtins.property
    @jsii.member(jsii_name="ingressPublicIp")
    def ingress_public_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ingressPublicIp"))

    @builtins.property
    @jsii.member(jsii_name="lookerUri")
    def looker_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lookerUri"))

    @builtins.property
    @jsii.member(jsii_name="lookerVersion")
    def looker_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lookerVersion"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindow")
    def maintenance_window(
        self,
    ) -> "GoogleLookerInstanceMaintenanceWindowOutputReference":
        return typing.cast("GoogleLookerInstanceMaintenanceWindowOutputReference", jsii.get(self, "maintenanceWindow"))

    @builtins.property
    @jsii.member(jsii_name="oauthConfig")
    def oauth_config(self) -> "GoogleLookerInstanceOauthConfigOutputReference":
        return typing.cast("GoogleLookerInstanceOauthConfigOutputReference", jsii.get(self, "oauthConfig"))

    @builtins.property
    @jsii.member(jsii_name="pscConfig")
    def psc_config(self) -> "GoogleLookerInstancePscConfigOutputReference":
        return typing.cast("GoogleLookerInstancePscConfigOutputReference", jsii.get(self, "pscConfig"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleLookerInstanceTimeoutsOutputReference":
        return typing.cast("GoogleLookerInstanceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="userMetadata")
    def user_metadata(self) -> "GoogleLookerInstanceUserMetadataOutputReference":
        return typing.cast("GoogleLookerInstanceUserMetadataOutputReference", jsii.get(self, "userMetadata"))

    @builtins.property
    @jsii.member(jsii_name="adminSettingsInput")
    def admin_settings_input(
        self,
    ) -> typing.Optional["GoogleLookerInstanceAdminSettings"]:
        return typing.cast(typing.Optional["GoogleLookerInstanceAdminSettings"], jsii.get(self, "adminSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="consumerNetworkInput")
    def consumer_network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "consumerNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="customDomainInput")
    def custom_domain_input(
        self,
    ) -> typing.Optional["GoogleLookerInstanceCustomDomain"]:
        return typing.cast(typing.Optional["GoogleLookerInstanceCustomDomain"], jsii.get(self, "customDomainInput"))

    @builtins.property
    @jsii.member(jsii_name="deletionPolicyInput")
    def deletion_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deletionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="denyMaintenancePeriodInput")
    def deny_maintenance_period_input(
        self,
    ) -> typing.Optional["GoogleLookerInstanceDenyMaintenancePeriod"]:
        return typing.cast(typing.Optional["GoogleLookerInstanceDenyMaintenancePeriod"], jsii.get(self, "denyMaintenancePeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfigInput")
    def encryption_config_input(
        self,
    ) -> typing.Optional["GoogleLookerInstanceEncryptionConfig"]:
        return typing.cast(typing.Optional["GoogleLookerInstanceEncryptionConfig"], jsii.get(self, "encryptionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="fipsEnabledInput")
    def fips_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fipsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindowInput")
    def maintenance_window_input(
        self,
    ) -> typing.Optional["GoogleLookerInstanceMaintenanceWindow"]:
        return typing.cast(typing.Optional["GoogleLookerInstanceMaintenanceWindow"], jsii.get(self, "maintenanceWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthConfigInput")
    def oauth_config_input(self) -> typing.Optional["GoogleLookerInstanceOauthConfig"]:
        return typing.cast(typing.Optional["GoogleLookerInstanceOauthConfig"], jsii.get(self, "oauthConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="platformEditionInput")
    def platform_edition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "platformEditionInput"))

    @builtins.property
    @jsii.member(jsii_name="privateIpEnabledInput")
    def private_ip_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "privateIpEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="pscConfigInput")
    def psc_config_input(self) -> typing.Optional["GoogleLookerInstancePscConfig"]:
        return typing.cast(typing.Optional["GoogleLookerInstancePscConfig"], jsii.get(self, "pscConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="pscEnabledInput")
    def psc_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "pscEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="publicIpEnabledInput")
    def public_ip_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "publicIpEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="reservedRangeInput")
    def reserved_range_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "reservedRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleLookerInstanceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleLookerInstanceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="userMetadataInput")
    def user_metadata_input(
        self,
    ) -> typing.Optional["GoogleLookerInstanceUserMetadata"]:
        return typing.cast(typing.Optional["GoogleLookerInstanceUserMetadata"], jsii.get(self, "userMetadataInput"))

    @builtins.property
    @jsii.member(jsii_name="consumerNetwork")
    def consumer_network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerNetwork"))

    @consumer_network.setter
    def consumer_network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18493d6bd0e6723c395eb6de7369469e7eabd3fb29911166e612dec98ac9a8ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerNetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deletionPolicy")
    def deletion_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deletionPolicy"))

    @deletion_policy.setter
    def deletion_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fcda5af44dc743230fd8dbed2de5212fcd0fe655f73e13e22473fac0dbb5349)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fipsEnabled")
    def fips_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fipsEnabled"))

    @fips_enabled.setter
    def fips_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4d4b57132b18f16fa66ef2c32d26f721b1ea7e88d5dc7eac67743790d178cb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fipsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00bbdb09d647145d752cf43d5a3042a65c868c549932e57b57535f748f14ae55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43e13ab5078202e657db43dc73fd16782024d2f14ba147986983e757389c65e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="platformEdition")
    def platform_edition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "platformEdition"))

    @platform_edition.setter
    def platform_edition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb6a20acf53b78f46d488b8a6ed3b3d42d0c5aaa2b4856fad3ce72d497fb920a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "platformEdition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateIpEnabled")
    def private_ip_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "privateIpEnabled"))

    @private_ip_enabled.setter
    def private_ip_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f6fc4975fce9f545448dafc7da40223caf321410e965eb93d9800f5cceaa6c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateIpEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd4b3095879edaae560c2be91d3e753bd3f5b8dd10fc6b4ff3fe10a9e9962e91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pscEnabled")
    def psc_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "pscEnabled"))

    @psc_enabled.setter
    def psc_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__361dd1c8ca2b2ca1deda9d4c05bf40d94c34988c3e93d0ded8f1b0687e10c61c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pscEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicIpEnabled")
    def public_ip_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "publicIpEnabled"))

    @public_ip_enabled.setter
    def public_ip_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0348c3a5894e9b43f3639c66e7947bb14220e07279127590df4bfc41945ed306)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicIpEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0f829e1d3a8b3de80a5158a560e0063585a0315437d25fde82a17580a6a35f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reservedRange")
    def reserved_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reservedRange"))

    @reserved_range.setter
    def reserved_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00e54345fba86c628adb59708d2bf97b96503795ce7eba3e93cfd63197d41eb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reservedRange", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleLookerInstance.GoogleLookerInstanceAdminSettings",
    jsii_struct_bases=[],
    name_mapping={"allowed_email_domains": "allowedEmailDomains"},
)
class GoogleLookerInstanceAdminSettings:
    def __init__(
        self,
        *,
        allowed_email_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allowed_email_domains: Email domain allowlist for the instance. Define the email domains to which your users can deliver Looker (Google Cloud core) content. Updating this list will restart the instance. Updating the allowed email domains from terraform means the value provided will be considered as the entire list and not an amendment to the existing list of allowed email domains. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#allowed_email_domains GoogleLookerInstance#allowed_email_domains}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b6b382d3a78184a830957f242d602ed68856fd02c2c34bf1b5781206ce95cee)
            check_type(argname="argument allowed_email_domains", value=allowed_email_domains, expected_type=type_hints["allowed_email_domains"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_email_domains is not None:
            self._values["allowed_email_domains"] = allowed_email_domains

    @builtins.property
    def allowed_email_domains(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Email domain allowlist for the instance.

        Define the email domains to which your users can deliver Looker (Google Cloud core) content.
        Updating this list will restart the instance. Updating the allowed email domains from terraform
        means the value provided will be considered as the entire list and not an amendment to the
        existing list of allowed email domains.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#allowed_email_domains GoogleLookerInstance#allowed_email_domains}
        '''
        result = self._values.get("allowed_email_domains")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleLookerInstanceAdminSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleLookerInstanceAdminSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleLookerInstance.GoogleLookerInstanceAdminSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5d11181e6dcef4772ba023c1f51ab87aca6cfddb7b86682eb46817923813dde)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowedEmailDomains")
    def reset_allowed_email_domains(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedEmailDomains", []))

    @builtins.property
    @jsii.member(jsii_name="allowedEmailDomainsInput")
    def allowed_email_domains_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedEmailDomainsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedEmailDomains")
    def allowed_email_domains(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedEmailDomains"))

    @allowed_email_domains.setter
    def allowed_email_domains(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78bf0b287304c2b1741dd0d1f8ddff244d42b9b1fceaacc3fefec66f3b58a78e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedEmailDomains", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleLookerInstanceAdminSettings]:
        return typing.cast(typing.Optional[GoogleLookerInstanceAdminSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleLookerInstanceAdminSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04e19c845f874e605600fcf92f84254eff8505174c77bc5133ed14e24a08b8a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleLookerInstance.GoogleLookerInstanceConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "oauth_config": "oauthConfig",
        "admin_settings": "adminSettings",
        "consumer_network": "consumerNetwork",
        "custom_domain": "customDomain",
        "deletion_policy": "deletionPolicy",
        "deny_maintenance_period": "denyMaintenancePeriod",
        "encryption_config": "encryptionConfig",
        "fips_enabled": "fipsEnabled",
        "id": "id",
        "maintenance_window": "maintenanceWindow",
        "platform_edition": "platformEdition",
        "private_ip_enabled": "privateIpEnabled",
        "project": "project",
        "psc_config": "pscConfig",
        "psc_enabled": "pscEnabled",
        "public_ip_enabled": "publicIpEnabled",
        "region": "region",
        "reserved_range": "reservedRange",
        "timeouts": "timeouts",
        "user_metadata": "userMetadata",
    },
)
class GoogleLookerInstanceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        oauth_config: typing.Union["GoogleLookerInstanceOauthConfig", typing.Dict[builtins.str, typing.Any]],
        admin_settings: typing.Optional[typing.Union[GoogleLookerInstanceAdminSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        consumer_network: typing.Optional[builtins.str] = None,
        custom_domain: typing.Optional[typing.Union["GoogleLookerInstanceCustomDomain", typing.Dict[builtins.str, typing.Any]]] = None,
        deletion_policy: typing.Optional[builtins.str] = None,
        deny_maintenance_period: typing.Optional[typing.Union["GoogleLookerInstanceDenyMaintenancePeriod", typing.Dict[builtins.str, typing.Any]]] = None,
        encryption_config: typing.Optional[typing.Union["GoogleLookerInstanceEncryptionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        fips_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        maintenance_window: typing.Optional[typing.Union["GoogleLookerInstanceMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]] = None,
        platform_edition: typing.Optional[builtins.str] = None,
        private_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project: typing.Optional[builtins.str] = None,
        psc_config: typing.Optional[typing.Union["GoogleLookerInstancePscConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        psc_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        public_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        region: typing.Optional[builtins.str] = None,
        reserved_range: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleLookerInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        user_metadata: typing.Optional[typing.Union["GoogleLookerInstanceUserMetadata", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The ID of the instance or a fully qualified identifier for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#name GoogleLookerInstance#name}
        :param oauth_config: oauth_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#oauth_config GoogleLookerInstance#oauth_config}
        :param admin_settings: admin_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#admin_settings GoogleLookerInstance#admin_settings}
        :param consumer_network: Network name in the consumer project in the format of: projects/{project}/global/networks/{network} Note that the consumer network may be in a different GCP project than the consumer project that is hosting the Looker Instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#consumer_network GoogleLookerInstance#consumer_network}
        :param custom_domain: custom_domain block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#custom_domain GoogleLookerInstance#custom_domain}
        :param deletion_policy: Policy to determine if the cluster should be deleted forcefully. If setting deletion_policy = "FORCE", the Looker instance will be deleted regardless of its nested resources. If set to "DEFAULT", Looker instances that still have nested resources will return an error. Possible values: DEFAULT, FORCE Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#deletion_policy GoogleLookerInstance#deletion_policy}
        :param deny_maintenance_period: deny_maintenance_period block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#deny_maintenance_period GoogleLookerInstance#deny_maintenance_period}
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#encryption_config GoogleLookerInstance#encryption_config}
        :param fips_enabled: FIPS 140-2 Encryption enablement for Looker (Google Cloud Core). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#fips_enabled GoogleLookerInstance#fips_enabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#id GoogleLookerInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param maintenance_window: maintenance_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#maintenance_window GoogleLookerInstance#maintenance_window}
        :param platform_edition: Platform editions for a Looker instance. Each edition maps to a set of instance features, like its size. Must be one of these values: - LOOKER_CORE_TRIAL: trial instance (Currently Unavailable) - LOOKER_CORE_STANDARD: pay as you go standard instance (Currently Unavailable) - LOOKER_CORE_STANDARD_ANNUAL: subscription standard instance - LOOKER_CORE_ENTERPRISE_ANNUAL: subscription enterprise instance - LOOKER_CORE_EMBED_ANNUAL: subscription embed instance - LOOKER_CORE_NONPROD_STANDARD_ANNUAL: nonprod subscription standard instance - LOOKER_CORE_NONPROD_ENTERPRISE_ANNUAL: nonprod subscription enterprise instance - LOOKER_CORE_NONPROD_EMBED_ANNUAL: nonprod subscription embed instance Default value: "LOOKER_CORE_TRIAL" Possible values: ["LOOKER_CORE_TRIAL", "LOOKER_CORE_STANDARD", "LOOKER_CORE_STANDARD_ANNUAL", "LOOKER_CORE_ENTERPRISE_ANNUAL", "LOOKER_CORE_EMBED_ANNUAL", "LOOKER_CORE_NONPROD_STANDARD_ANNUAL", "LOOKER_CORE_NONPROD_ENTERPRISE_ANNUAL", "LOOKER_CORE_NONPROD_EMBED_ANNUAL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#platform_edition GoogleLookerInstance#platform_edition}
        :param private_ip_enabled: Whether private IP is enabled on the Looker instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#private_ip_enabled GoogleLookerInstance#private_ip_enabled}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#project GoogleLookerInstance#project}.
        :param psc_config: psc_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#psc_config GoogleLookerInstance#psc_config}
        :param psc_enabled: Whether Public Service Connect (PSC) is enabled on the Looker instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#psc_enabled GoogleLookerInstance#psc_enabled}
        :param public_ip_enabled: Whether public IP is enabled on the Looker instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#public_ip_enabled GoogleLookerInstance#public_ip_enabled}
        :param region: The name of the Looker region of the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#region GoogleLookerInstance#region}
        :param reserved_range: Name of a reserved IP address range within the consumer network, to be used for private service access connection. User may or may not specify this in a request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#reserved_range GoogleLookerInstance#reserved_range}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#timeouts GoogleLookerInstance#timeouts}
        :param user_metadata: user_metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#user_metadata GoogleLookerInstance#user_metadata}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(oauth_config, dict):
            oauth_config = GoogleLookerInstanceOauthConfig(**oauth_config)
        if isinstance(admin_settings, dict):
            admin_settings = GoogleLookerInstanceAdminSettings(**admin_settings)
        if isinstance(custom_domain, dict):
            custom_domain = GoogleLookerInstanceCustomDomain(**custom_domain)
        if isinstance(deny_maintenance_period, dict):
            deny_maintenance_period = GoogleLookerInstanceDenyMaintenancePeriod(**deny_maintenance_period)
        if isinstance(encryption_config, dict):
            encryption_config = GoogleLookerInstanceEncryptionConfig(**encryption_config)
        if isinstance(maintenance_window, dict):
            maintenance_window = GoogleLookerInstanceMaintenanceWindow(**maintenance_window)
        if isinstance(psc_config, dict):
            psc_config = GoogleLookerInstancePscConfig(**psc_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleLookerInstanceTimeouts(**timeouts)
        if isinstance(user_metadata, dict):
            user_metadata = GoogleLookerInstanceUserMetadata(**user_metadata)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88b271d42a1265e510434620991bc659d6e8f5967bdfc689386ec953e98d3be4)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument oauth_config", value=oauth_config, expected_type=type_hints["oauth_config"])
            check_type(argname="argument admin_settings", value=admin_settings, expected_type=type_hints["admin_settings"])
            check_type(argname="argument consumer_network", value=consumer_network, expected_type=type_hints["consumer_network"])
            check_type(argname="argument custom_domain", value=custom_domain, expected_type=type_hints["custom_domain"])
            check_type(argname="argument deletion_policy", value=deletion_policy, expected_type=type_hints["deletion_policy"])
            check_type(argname="argument deny_maintenance_period", value=deny_maintenance_period, expected_type=type_hints["deny_maintenance_period"])
            check_type(argname="argument encryption_config", value=encryption_config, expected_type=type_hints["encryption_config"])
            check_type(argname="argument fips_enabled", value=fips_enabled, expected_type=type_hints["fips_enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument maintenance_window", value=maintenance_window, expected_type=type_hints["maintenance_window"])
            check_type(argname="argument platform_edition", value=platform_edition, expected_type=type_hints["platform_edition"])
            check_type(argname="argument private_ip_enabled", value=private_ip_enabled, expected_type=type_hints["private_ip_enabled"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument psc_config", value=psc_config, expected_type=type_hints["psc_config"])
            check_type(argname="argument psc_enabled", value=psc_enabled, expected_type=type_hints["psc_enabled"])
            check_type(argname="argument public_ip_enabled", value=public_ip_enabled, expected_type=type_hints["public_ip_enabled"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument reserved_range", value=reserved_range, expected_type=type_hints["reserved_range"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument user_metadata", value=user_metadata, expected_type=type_hints["user_metadata"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "oauth_config": oauth_config,
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
        if admin_settings is not None:
            self._values["admin_settings"] = admin_settings
        if consumer_network is not None:
            self._values["consumer_network"] = consumer_network
        if custom_domain is not None:
            self._values["custom_domain"] = custom_domain
        if deletion_policy is not None:
            self._values["deletion_policy"] = deletion_policy
        if deny_maintenance_period is not None:
            self._values["deny_maintenance_period"] = deny_maintenance_period
        if encryption_config is not None:
            self._values["encryption_config"] = encryption_config
        if fips_enabled is not None:
            self._values["fips_enabled"] = fips_enabled
        if id is not None:
            self._values["id"] = id
        if maintenance_window is not None:
            self._values["maintenance_window"] = maintenance_window
        if platform_edition is not None:
            self._values["platform_edition"] = platform_edition
        if private_ip_enabled is not None:
            self._values["private_ip_enabled"] = private_ip_enabled
        if project is not None:
            self._values["project"] = project
        if psc_config is not None:
            self._values["psc_config"] = psc_config
        if psc_enabled is not None:
            self._values["psc_enabled"] = psc_enabled
        if public_ip_enabled is not None:
            self._values["public_ip_enabled"] = public_ip_enabled
        if region is not None:
            self._values["region"] = region
        if reserved_range is not None:
            self._values["reserved_range"] = reserved_range
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if user_metadata is not None:
            self._values["user_metadata"] = user_metadata

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
    def name(self) -> builtins.str:
        '''The ID of the instance or a fully qualified identifier for the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#name GoogleLookerInstance#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def oauth_config(self) -> "GoogleLookerInstanceOauthConfig":
        '''oauth_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#oauth_config GoogleLookerInstance#oauth_config}
        '''
        result = self._values.get("oauth_config")
        assert result is not None, "Required property 'oauth_config' is missing"
        return typing.cast("GoogleLookerInstanceOauthConfig", result)

    @builtins.property
    def admin_settings(self) -> typing.Optional[GoogleLookerInstanceAdminSettings]:
        '''admin_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#admin_settings GoogleLookerInstance#admin_settings}
        '''
        result = self._values.get("admin_settings")
        return typing.cast(typing.Optional[GoogleLookerInstanceAdminSettings], result)

    @builtins.property
    def consumer_network(self) -> typing.Optional[builtins.str]:
        '''Network name in the consumer project in the format of: projects/{project}/global/networks/{network} Note that the consumer network may be in a different GCP project than the consumer project that is hosting the Looker Instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#consumer_network GoogleLookerInstance#consumer_network}
        '''
        result = self._values.get("consumer_network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_domain(self) -> typing.Optional["GoogleLookerInstanceCustomDomain"]:
        '''custom_domain block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#custom_domain GoogleLookerInstance#custom_domain}
        '''
        result = self._values.get("custom_domain")
        return typing.cast(typing.Optional["GoogleLookerInstanceCustomDomain"], result)

    @builtins.property
    def deletion_policy(self) -> typing.Optional[builtins.str]:
        '''Policy to determine if the cluster should be deleted forcefully.

        If setting deletion_policy = "FORCE", the Looker instance will be deleted regardless
        of its nested resources. If set to "DEFAULT", Looker instances that still have
        nested resources will return an error. Possible values: DEFAULT, FORCE

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#deletion_policy GoogleLookerInstance#deletion_policy}
        '''
        result = self._values.get("deletion_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deny_maintenance_period(
        self,
    ) -> typing.Optional["GoogleLookerInstanceDenyMaintenancePeriod"]:
        '''deny_maintenance_period block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#deny_maintenance_period GoogleLookerInstance#deny_maintenance_period}
        '''
        result = self._values.get("deny_maintenance_period")
        return typing.cast(typing.Optional["GoogleLookerInstanceDenyMaintenancePeriod"], result)

    @builtins.property
    def encryption_config(
        self,
    ) -> typing.Optional["GoogleLookerInstanceEncryptionConfig"]:
        '''encryption_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#encryption_config GoogleLookerInstance#encryption_config}
        '''
        result = self._values.get("encryption_config")
        return typing.cast(typing.Optional["GoogleLookerInstanceEncryptionConfig"], result)

    @builtins.property
    def fips_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''FIPS 140-2 Encryption enablement for Looker (Google Cloud Core).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#fips_enabled GoogleLookerInstance#fips_enabled}
        '''
        result = self._values.get("fips_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#id GoogleLookerInstance#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintenance_window(
        self,
    ) -> typing.Optional["GoogleLookerInstanceMaintenanceWindow"]:
        '''maintenance_window block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#maintenance_window GoogleLookerInstance#maintenance_window}
        '''
        result = self._values.get("maintenance_window")
        return typing.cast(typing.Optional["GoogleLookerInstanceMaintenanceWindow"], result)

    @builtins.property
    def platform_edition(self) -> typing.Optional[builtins.str]:
        '''Platform editions for a Looker instance.

        Each edition maps to a set of instance features, like its size. Must be one of these values:

        - LOOKER_CORE_TRIAL: trial instance (Currently Unavailable)
        - LOOKER_CORE_STANDARD: pay as you go standard instance (Currently Unavailable)
        - LOOKER_CORE_STANDARD_ANNUAL: subscription standard instance
        - LOOKER_CORE_ENTERPRISE_ANNUAL: subscription enterprise instance
        - LOOKER_CORE_EMBED_ANNUAL: subscription embed instance
        - LOOKER_CORE_NONPROD_STANDARD_ANNUAL: nonprod subscription standard instance
        - LOOKER_CORE_NONPROD_ENTERPRISE_ANNUAL: nonprod subscription enterprise instance
        - LOOKER_CORE_NONPROD_EMBED_ANNUAL: nonprod subscription embed instance Default value: "LOOKER_CORE_TRIAL" Possible values: ["LOOKER_CORE_TRIAL", "LOOKER_CORE_STANDARD", "LOOKER_CORE_STANDARD_ANNUAL", "LOOKER_CORE_ENTERPRISE_ANNUAL", "LOOKER_CORE_EMBED_ANNUAL", "LOOKER_CORE_NONPROD_STANDARD_ANNUAL", "LOOKER_CORE_NONPROD_ENTERPRISE_ANNUAL", "LOOKER_CORE_NONPROD_EMBED_ANNUAL"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#platform_edition GoogleLookerInstance#platform_edition}
        '''
        result = self._values.get("platform_edition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_ip_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether private IP is enabled on the Looker instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#private_ip_enabled GoogleLookerInstance#private_ip_enabled}
        '''
        result = self._values.get("private_ip_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#project GoogleLookerInstance#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def psc_config(self) -> typing.Optional["GoogleLookerInstancePscConfig"]:
        '''psc_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#psc_config GoogleLookerInstance#psc_config}
        '''
        result = self._values.get("psc_config")
        return typing.cast(typing.Optional["GoogleLookerInstancePscConfig"], result)

    @builtins.property
    def psc_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether Public Service Connect (PSC) is enabled on the Looker instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#psc_enabled GoogleLookerInstance#psc_enabled}
        '''
        result = self._values.get("psc_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def public_ip_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether public IP is enabled on the Looker instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#public_ip_enabled GoogleLookerInstance#public_ip_enabled}
        '''
        result = self._values.get("public_ip_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The name of the Looker region of the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#region GoogleLookerInstance#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reserved_range(self) -> typing.Optional[builtins.str]:
        '''Name of a reserved IP address range within the consumer network, to be used for private service access connection.

        User may or may not specify this in a request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#reserved_range GoogleLookerInstance#reserved_range}
        '''
        result = self._values.get("reserved_range")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleLookerInstanceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#timeouts GoogleLookerInstance#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleLookerInstanceTimeouts"], result)

    @builtins.property
    def user_metadata(self) -> typing.Optional["GoogleLookerInstanceUserMetadata"]:
        '''user_metadata block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#user_metadata GoogleLookerInstance#user_metadata}
        '''
        result = self._values.get("user_metadata")
        return typing.cast(typing.Optional["GoogleLookerInstanceUserMetadata"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleLookerInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleLookerInstance.GoogleLookerInstanceCustomDomain",
    jsii_struct_bases=[],
    name_mapping={"domain": "domain"},
)
class GoogleLookerInstanceCustomDomain:
    def __init__(self, *, domain: typing.Optional[builtins.str] = None) -> None:
        '''
        :param domain: Domain name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#domain GoogleLookerInstance#domain}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__970246e31f61542a823f0e6f4459c17c692e6d04e0aabc4915af08d9e788b072)
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if domain is not None:
            self._values["domain"] = domain

    @builtins.property
    def domain(self) -> typing.Optional[builtins.str]:
        '''Domain name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#domain GoogleLookerInstance#domain}
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleLookerInstanceCustomDomain(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleLookerInstanceCustomDomainOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleLookerInstance.GoogleLookerInstanceCustomDomainOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__025f8710b82e51bc625964c38192c42325f7305eb7822d1e1ea43d6954fc244e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDomain")
    def reset_domain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomain", []))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="domainInput")
    def domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainInput"))

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domain"))

    @domain.setter
    def domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a7d3bfcbccd33e592776c98b7cb58f49d23d8574cbf0e85efdb515ac6cca99e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleLookerInstanceCustomDomain]:
        return typing.cast(typing.Optional[GoogleLookerInstanceCustomDomain], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleLookerInstanceCustomDomain],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b135f8adc56bf82951c64f60f9c2feb52c2ea95319c8055aba390ae966422d4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleLookerInstance.GoogleLookerInstanceDenyMaintenancePeriod",
    jsii_struct_bases=[],
    name_mapping={"end_date": "endDate", "start_date": "startDate", "time": "time"},
)
class GoogleLookerInstanceDenyMaintenancePeriod:
    def __init__(
        self,
        *,
        end_date: typing.Union["GoogleLookerInstanceDenyMaintenancePeriodEndDate", typing.Dict[builtins.str, typing.Any]],
        start_date: typing.Union["GoogleLookerInstanceDenyMaintenancePeriodStartDate", typing.Dict[builtins.str, typing.Any]],
        time: typing.Union["GoogleLookerInstanceDenyMaintenancePeriodTime", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param end_date: end_date block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#end_date GoogleLookerInstance#end_date}
        :param start_date: start_date block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#start_date GoogleLookerInstance#start_date}
        :param time: time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#time GoogleLookerInstance#time}
        '''
        if isinstance(end_date, dict):
            end_date = GoogleLookerInstanceDenyMaintenancePeriodEndDate(**end_date)
        if isinstance(start_date, dict):
            start_date = GoogleLookerInstanceDenyMaintenancePeriodStartDate(**start_date)
        if isinstance(time, dict):
            time = GoogleLookerInstanceDenyMaintenancePeriodTime(**time)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fce11a4cd688551c648e6e78e7527af046b1efc2c7c2c1631c8a6f6e05e63f51)
            check_type(argname="argument end_date", value=end_date, expected_type=type_hints["end_date"])
            check_type(argname="argument start_date", value=start_date, expected_type=type_hints["start_date"])
            check_type(argname="argument time", value=time, expected_type=type_hints["time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "end_date": end_date,
            "start_date": start_date,
            "time": time,
        }

    @builtins.property
    def end_date(self) -> "GoogleLookerInstanceDenyMaintenancePeriodEndDate":
        '''end_date block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#end_date GoogleLookerInstance#end_date}
        '''
        result = self._values.get("end_date")
        assert result is not None, "Required property 'end_date' is missing"
        return typing.cast("GoogleLookerInstanceDenyMaintenancePeriodEndDate", result)

    @builtins.property
    def start_date(self) -> "GoogleLookerInstanceDenyMaintenancePeriodStartDate":
        '''start_date block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#start_date GoogleLookerInstance#start_date}
        '''
        result = self._values.get("start_date")
        assert result is not None, "Required property 'start_date' is missing"
        return typing.cast("GoogleLookerInstanceDenyMaintenancePeriodStartDate", result)

    @builtins.property
    def time(self) -> "GoogleLookerInstanceDenyMaintenancePeriodTime":
        '''time block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#time GoogleLookerInstance#time}
        '''
        result = self._values.get("time")
        assert result is not None, "Required property 'time' is missing"
        return typing.cast("GoogleLookerInstanceDenyMaintenancePeriodTime", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleLookerInstanceDenyMaintenancePeriod(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleLookerInstance.GoogleLookerInstanceDenyMaintenancePeriodEndDate",
    jsii_struct_bases=[],
    name_mapping={"day": "day", "month": "month", "year": "year"},
)
class GoogleLookerInstanceDenyMaintenancePeriodEndDate:
    def __init__(
        self,
        *,
        day: typing.Optional[jsii.Number] = None,
        month: typing.Optional[jsii.Number] = None,
        year: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param day: Day of a month. Must be from 1 to 31 and valid for the year and month, or 0 to specify a year by itself or a year and month where the day isn't significant. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#day GoogleLookerInstance#day}
        :param month: Month of a year. Must be from 1 to 12, or 0 to specify a year without a month and day. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#month GoogleLookerInstance#month}
        :param year: Year of the date. Must be from 1 to 9999, or 0 to specify a date without a year. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#year GoogleLookerInstance#year}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01be8b5b242a38500b9b8ecacdeaaf4095ecda06968f79da5a0de875db15563d)
            check_type(argname="argument day", value=day, expected_type=type_hints["day"])
            check_type(argname="argument month", value=month, expected_type=type_hints["month"])
            check_type(argname="argument year", value=year, expected_type=type_hints["year"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if day is not None:
            self._values["day"] = day
        if month is not None:
            self._values["month"] = month
        if year is not None:
            self._values["year"] = year

    @builtins.property
    def day(self) -> typing.Optional[jsii.Number]:
        '''Day of a month.

        Must be from 1 to 31 and valid for the year and month, or 0
        to specify a year by itself or a year and month where the day isn't significant.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#day GoogleLookerInstance#day}
        '''
        result = self._values.get("day")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def month(self) -> typing.Optional[jsii.Number]:
        '''Month of a year.

        Must be from 1 to 12, or 0 to specify a year without a
        month and day.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#month GoogleLookerInstance#month}
        '''
        result = self._values.get("month")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def year(self) -> typing.Optional[jsii.Number]:
        '''Year of the date. Must be from 1 to 9999, or 0 to specify a date without a year.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#year GoogleLookerInstance#year}
        '''
        result = self._values.get("year")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleLookerInstanceDenyMaintenancePeriodEndDate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleLookerInstanceDenyMaintenancePeriodEndDateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleLookerInstance.GoogleLookerInstanceDenyMaintenancePeriodEndDateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__761a5fc41ebc01904d75e038d1bbeee2faa51b208225afb151e38623c37222d0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDay")
    def reset_day(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDay", []))

    @jsii.member(jsii_name="resetMonth")
    def reset_month(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonth", []))

    @jsii.member(jsii_name="resetYear")
    def reset_year(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetYear", []))

    @builtins.property
    @jsii.member(jsii_name="dayInput")
    def day_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dayInput"))

    @builtins.property
    @jsii.member(jsii_name="monthInput")
    def month_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "monthInput"))

    @builtins.property
    @jsii.member(jsii_name="yearInput")
    def year_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "yearInput"))

    @builtins.property
    @jsii.member(jsii_name="day")
    def day(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "day"))

    @day.setter
    def day(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6112883115ddaf7ba6cff7f512f45f3e5130ad7a93133e29da61dbb08643caf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "day", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="month")
    def month(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "month"))

    @month.setter
    def month(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67626b57acc06098438b5a12bcbe56e6c8456ed7af2e9e93df4f70b3dc516839)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "month", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="year")
    def year(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "year"))

    @year.setter
    def year(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dfcbe5a8c15139e888a898f9caf3bef607fba58affdfae82534d7ab3ff91de3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "year", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleLookerInstanceDenyMaintenancePeriodEndDate]:
        return typing.cast(typing.Optional[GoogleLookerInstanceDenyMaintenancePeriodEndDate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleLookerInstanceDenyMaintenancePeriodEndDate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__585ba5c4bf73a2d0c0f4fadfb9d63fbb387144aff884add9eec88270d674880a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleLookerInstanceDenyMaintenancePeriodOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleLookerInstance.GoogleLookerInstanceDenyMaintenancePeriodOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4787e391a86f22a772531dae4690d52cfa383babbb689a798bc68a42ff3ebafd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEndDate")
    def put_end_date(
        self,
        *,
        day: typing.Optional[jsii.Number] = None,
        month: typing.Optional[jsii.Number] = None,
        year: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param day: Day of a month. Must be from 1 to 31 and valid for the year and month, or 0 to specify a year by itself or a year and month where the day isn't significant. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#day GoogleLookerInstance#day}
        :param month: Month of a year. Must be from 1 to 12, or 0 to specify a year without a month and day. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#month GoogleLookerInstance#month}
        :param year: Year of the date. Must be from 1 to 9999, or 0 to specify a date without a year. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#year GoogleLookerInstance#year}
        '''
        value = GoogleLookerInstanceDenyMaintenancePeriodEndDate(
            day=day, month=month, year=year
        )

        return typing.cast(None, jsii.invoke(self, "putEndDate", [value]))

    @jsii.member(jsii_name="putStartDate")
    def put_start_date(
        self,
        *,
        day: typing.Optional[jsii.Number] = None,
        month: typing.Optional[jsii.Number] = None,
        year: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param day: Day of a month. Must be from 1 to 31 and valid for the year and month, or 0 to specify a year by itself or a year and month where the day isn't significant. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#day GoogleLookerInstance#day}
        :param month: Month of a year. Must be from 1 to 12, or 0 to specify a year without a month and day. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#month GoogleLookerInstance#month}
        :param year: Year of the date. Must be from 1 to 9999, or 0 to specify a date without a year. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#year GoogleLookerInstance#year}
        '''
        value = GoogleLookerInstanceDenyMaintenancePeriodStartDate(
            day=day, month=month, year=year
        )

        return typing.cast(None, jsii.invoke(self, "putStartDate", [value]))

    @jsii.member(jsii_name="putTime")
    def put_time(
        self,
        *,
        hours: typing.Optional[jsii.Number] = None,
        minutes: typing.Optional[jsii.Number] = None,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hours: Hours of day in 24 hour format. Should be from 0 to 23. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#hours GoogleLookerInstance#hours}
        :param minutes: Minutes of hour of day. Must be from 0 to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#minutes GoogleLookerInstance#minutes}
        :param nanos: Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#nanos GoogleLookerInstance#nanos}
        :param seconds: Seconds of minutes of the time. Must normally be from 0 to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#seconds GoogleLookerInstance#seconds}
        '''
        value = GoogleLookerInstanceDenyMaintenancePeriodTime(
            hours=hours, minutes=minutes, nanos=nanos, seconds=seconds
        )

        return typing.cast(None, jsii.invoke(self, "putTime", [value]))

    @builtins.property
    @jsii.member(jsii_name="endDate")
    def end_date(
        self,
    ) -> GoogleLookerInstanceDenyMaintenancePeriodEndDateOutputReference:
        return typing.cast(GoogleLookerInstanceDenyMaintenancePeriodEndDateOutputReference, jsii.get(self, "endDate"))

    @builtins.property
    @jsii.member(jsii_name="startDate")
    def start_date(
        self,
    ) -> "GoogleLookerInstanceDenyMaintenancePeriodStartDateOutputReference":
        return typing.cast("GoogleLookerInstanceDenyMaintenancePeriodStartDateOutputReference", jsii.get(self, "startDate"))

    @builtins.property
    @jsii.member(jsii_name="time")
    def time(self) -> "GoogleLookerInstanceDenyMaintenancePeriodTimeOutputReference":
        return typing.cast("GoogleLookerInstanceDenyMaintenancePeriodTimeOutputReference", jsii.get(self, "time"))

    @builtins.property
    @jsii.member(jsii_name="endDateInput")
    def end_date_input(
        self,
    ) -> typing.Optional[GoogleLookerInstanceDenyMaintenancePeriodEndDate]:
        return typing.cast(typing.Optional[GoogleLookerInstanceDenyMaintenancePeriodEndDate], jsii.get(self, "endDateInput"))

    @builtins.property
    @jsii.member(jsii_name="startDateInput")
    def start_date_input(
        self,
    ) -> typing.Optional["GoogleLookerInstanceDenyMaintenancePeriodStartDate"]:
        return typing.cast(typing.Optional["GoogleLookerInstanceDenyMaintenancePeriodStartDate"], jsii.get(self, "startDateInput"))

    @builtins.property
    @jsii.member(jsii_name="timeInput")
    def time_input(
        self,
    ) -> typing.Optional["GoogleLookerInstanceDenyMaintenancePeriodTime"]:
        return typing.cast(typing.Optional["GoogleLookerInstanceDenyMaintenancePeriodTime"], jsii.get(self, "timeInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleLookerInstanceDenyMaintenancePeriod]:
        return typing.cast(typing.Optional[GoogleLookerInstanceDenyMaintenancePeriod], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleLookerInstanceDenyMaintenancePeriod],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__995966fbd40da78cf9fd23fc6495939939ddae52b4077bb5e814b0c25bfa105a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleLookerInstance.GoogleLookerInstanceDenyMaintenancePeriodStartDate",
    jsii_struct_bases=[],
    name_mapping={"day": "day", "month": "month", "year": "year"},
)
class GoogleLookerInstanceDenyMaintenancePeriodStartDate:
    def __init__(
        self,
        *,
        day: typing.Optional[jsii.Number] = None,
        month: typing.Optional[jsii.Number] = None,
        year: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param day: Day of a month. Must be from 1 to 31 and valid for the year and month, or 0 to specify a year by itself or a year and month where the day isn't significant. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#day GoogleLookerInstance#day}
        :param month: Month of a year. Must be from 1 to 12, or 0 to specify a year without a month and day. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#month GoogleLookerInstance#month}
        :param year: Year of the date. Must be from 1 to 9999, or 0 to specify a date without a year. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#year GoogleLookerInstance#year}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b1cdfa5b03960fe09dade3279ed1077b13d64997de50dca9a6273593d30dabf)
            check_type(argname="argument day", value=day, expected_type=type_hints["day"])
            check_type(argname="argument month", value=month, expected_type=type_hints["month"])
            check_type(argname="argument year", value=year, expected_type=type_hints["year"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if day is not None:
            self._values["day"] = day
        if month is not None:
            self._values["month"] = month
        if year is not None:
            self._values["year"] = year

    @builtins.property
    def day(self) -> typing.Optional[jsii.Number]:
        '''Day of a month.

        Must be from 1 to 31 and valid for the year and month, or 0
        to specify a year by itself or a year and month where the day isn't significant.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#day GoogleLookerInstance#day}
        '''
        result = self._values.get("day")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def month(self) -> typing.Optional[jsii.Number]:
        '''Month of a year.

        Must be from 1 to 12, or 0 to specify a year without a
        month and day.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#month GoogleLookerInstance#month}
        '''
        result = self._values.get("month")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def year(self) -> typing.Optional[jsii.Number]:
        '''Year of the date. Must be from 1 to 9999, or 0 to specify a date without a year.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#year GoogleLookerInstance#year}
        '''
        result = self._values.get("year")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleLookerInstanceDenyMaintenancePeriodStartDate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleLookerInstanceDenyMaintenancePeriodStartDateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleLookerInstance.GoogleLookerInstanceDenyMaintenancePeriodStartDateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aed90be17dc5ce477fe14f8976fb139076c1a90c4a53ebd959b524eed77e4d6a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDay")
    def reset_day(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDay", []))

    @jsii.member(jsii_name="resetMonth")
    def reset_month(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonth", []))

    @jsii.member(jsii_name="resetYear")
    def reset_year(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetYear", []))

    @builtins.property
    @jsii.member(jsii_name="dayInput")
    def day_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dayInput"))

    @builtins.property
    @jsii.member(jsii_name="monthInput")
    def month_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "monthInput"))

    @builtins.property
    @jsii.member(jsii_name="yearInput")
    def year_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "yearInput"))

    @builtins.property
    @jsii.member(jsii_name="day")
    def day(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "day"))

    @day.setter
    def day(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8041f6e722ac3ebdd6b255aeee677ef722f01553e9b78d35d3f21402c6448068)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "day", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="month")
    def month(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "month"))

    @month.setter
    def month(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9da88b7c197e0b35dcf6f9dde3cf0becd9e6d1914f611b4cb708f926e9d3f405)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "month", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="year")
    def year(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "year"))

    @year.setter
    def year(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef1a900272e837b0f1c3083406bf0a6275176a662b300e26da2ef727256c4fdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "year", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleLookerInstanceDenyMaintenancePeriodStartDate]:
        return typing.cast(typing.Optional[GoogleLookerInstanceDenyMaintenancePeriodStartDate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleLookerInstanceDenyMaintenancePeriodStartDate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb825ec4ee6df0e53819d6e8532a3d22b937b0be488dcf431591a2e1fa3bbf27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleLookerInstance.GoogleLookerInstanceDenyMaintenancePeriodTime",
    jsii_struct_bases=[],
    name_mapping={
        "hours": "hours",
        "minutes": "minutes",
        "nanos": "nanos",
        "seconds": "seconds",
    },
)
class GoogleLookerInstanceDenyMaintenancePeriodTime:
    def __init__(
        self,
        *,
        hours: typing.Optional[jsii.Number] = None,
        minutes: typing.Optional[jsii.Number] = None,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hours: Hours of day in 24 hour format. Should be from 0 to 23. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#hours GoogleLookerInstance#hours}
        :param minutes: Minutes of hour of day. Must be from 0 to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#minutes GoogleLookerInstance#minutes}
        :param nanos: Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#nanos GoogleLookerInstance#nanos}
        :param seconds: Seconds of minutes of the time. Must normally be from 0 to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#seconds GoogleLookerInstance#seconds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0791b6087d52db8fbe26eb542a1af81237bc0123aa75d488cb13dd6689f8eb0d)
            check_type(argname="argument hours", value=hours, expected_type=type_hints["hours"])
            check_type(argname="argument minutes", value=minutes, expected_type=type_hints["minutes"])
            check_type(argname="argument nanos", value=nanos, expected_type=type_hints["nanos"])
            check_type(argname="argument seconds", value=seconds, expected_type=type_hints["seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if hours is not None:
            self._values["hours"] = hours
        if minutes is not None:
            self._values["minutes"] = minutes
        if nanos is not None:
            self._values["nanos"] = nanos
        if seconds is not None:
            self._values["seconds"] = seconds

    @builtins.property
    def hours(self) -> typing.Optional[jsii.Number]:
        '''Hours of day in 24 hour format. Should be from 0 to 23.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#hours GoogleLookerInstance#hours}
        '''
        result = self._values.get("hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minutes(self) -> typing.Optional[jsii.Number]:
        '''Minutes of hour of day. Must be from 0 to 59.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#minutes GoogleLookerInstance#minutes}
        '''
        result = self._values.get("minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nanos(self) -> typing.Optional[jsii.Number]:
        '''Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#nanos GoogleLookerInstance#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def seconds(self) -> typing.Optional[jsii.Number]:
        '''Seconds of minutes of the time. Must normally be from 0 to 59.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#seconds GoogleLookerInstance#seconds}
        '''
        result = self._values.get("seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleLookerInstanceDenyMaintenancePeriodTime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleLookerInstanceDenyMaintenancePeriodTimeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleLookerInstance.GoogleLookerInstanceDenyMaintenancePeriodTimeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e00a649febe793cc7104e9979e4cd065fa52faee850222ea15c130b46cd7173)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHours")
    def reset_hours(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHours", []))

    @jsii.member(jsii_name="resetMinutes")
    def reset_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinutes", []))

    @jsii.member(jsii_name="resetNanos")
    def reset_nanos(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNanos", []))

    @jsii.member(jsii_name="resetSeconds")
    def reset_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="hoursInput")
    def hours_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hoursInput"))

    @builtins.property
    @jsii.member(jsii_name="minutesInput")
    def minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minutesInput"))

    @builtins.property
    @jsii.member(jsii_name="nanosInput")
    def nanos_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nanosInput"))

    @builtins.property
    @jsii.member(jsii_name="secondsInput")
    def seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "secondsInput"))

    @builtins.property
    @jsii.member(jsii_name="hours")
    def hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hours"))

    @hours.setter
    def hours(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3476e9691c975c74b0ff2073603efddbd9425385389aae6bf4990e5182fa5e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minutes")
    def minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minutes"))

    @minutes.setter
    def minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__860075542ef78f730675d2017da17a939ae440fc465fce8566e08691768601e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @nanos.setter
    def nanos(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f81137fbe4c01a625cb6b115ad55920a80672f4bf7c75666f81349ef28d7ea50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e615236c3c4c8d99ab1f3b20b665a9c66cef406a2c041184aff061e6938bef3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleLookerInstanceDenyMaintenancePeriodTime]:
        return typing.cast(typing.Optional[GoogleLookerInstanceDenyMaintenancePeriodTime], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleLookerInstanceDenyMaintenancePeriodTime],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59e2bf33bc74608ae4dbeec02432ab6f20c6bf4b71b62c12cd05fe0cdff08f3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleLookerInstance.GoogleLookerInstanceEncryptionConfig",
    jsii_struct_bases=[],
    name_mapping={"kms_key_name": "kmsKeyName"},
)
class GoogleLookerInstanceEncryptionConfig:
    def __init__(self, *, kms_key_name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param kms_key_name: Name of the customer managed encryption key (CMEK) in KMS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#kms_key_name GoogleLookerInstance#kms_key_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__755585655e778e16507f1f0e180bc0a2249d75e390beede780d93ac40bfb34db)
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kms_key_name is not None:
            self._values["kms_key_name"] = kms_key_name

    @builtins.property
    def kms_key_name(self) -> typing.Optional[builtins.str]:
        '''Name of the customer managed encryption key (CMEK) in KMS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#kms_key_name GoogleLookerInstance#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleLookerInstanceEncryptionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleLookerInstanceEncryptionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleLookerInstance.GoogleLookerInstanceEncryptionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7769340f9d6ace473261ea07c4e930b633e33e49c12c89515cae082c71f460a0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKmsKeyName")
    def reset_kms_key_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyName", []))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyNameVersion")
    def kms_key_name_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyNameVersion"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyState")
    def kms_key_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyState"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__00f35b68617915176c8fb4023f9d396408e4a2d16af74fad94b09d8ce39a8917)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleLookerInstanceEncryptionConfig]:
        return typing.cast(typing.Optional[GoogleLookerInstanceEncryptionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleLookerInstanceEncryptionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92a50b48c73762a535f6c9759793e8416d035778c31bc850668a1afc22258fc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleLookerInstance.GoogleLookerInstanceMaintenanceWindow",
    jsii_struct_bases=[],
    name_mapping={"day_of_week": "dayOfWeek", "start_time": "startTime"},
)
class GoogleLookerInstanceMaintenanceWindow:
    def __init__(
        self,
        *,
        day_of_week: builtins.str,
        start_time: typing.Union["GoogleLookerInstanceMaintenanceWindowStartTime", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param day_of_week: Required. Day of the week for this MaintenanceWindow (in UTC). - MONDAY: Monday - TUESDAY: Tuesday - WEDNESDAY: Wednesday - THURSDAY: Thursday - FRIDAY: Friday - SATURDAY: Saturday - SUNDAY: Sunday Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#day_of_week GoogleLookerInstance#day_of_week}
        :param start_time: start_time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#start_time GoogleLookerInstance#start_time}
        '''
        if isinstance(start_time, dict):
            start_time = GoogleLookerInstanceMaintenanceWindowStartTime(**start_time)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5c77d3a8091e310b30a46fb7c3b5c64c1967237b840aa39f51c1197dba06b8f)
            check_type(argname="argument day_of_week", value=day_of_week, expected_type=type_hints["day_of_week"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "day_of_week": day_of_week,
            "start_time": start_time,
        }

    @builtins.property
    def day_of_week(self) -> builtins.str:
        '''Required. Day of the week for this MaintenanceWindow (in UTC).

        - MONDAY: Monday
        - TUESDAY: Tuesday
        - WEDNESDAY: Wednesday
        - THURSDAY: Thursday
        - FRIDAY: Friday
        - SATURDAY: Saturday
        - SUNDAY: Sunday Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#day_of_week GoogleLookerInstance#day_of_week}
        '''
        result = self._values.get("day_of_week")
        assert result is not None, "Required property 'day_of_week' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_time(self) -> "GoogleLookerInstanceMaintenanceWindowStartTime":
        '''start_time block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#start_time GoogleLookerInstance#start_time}
        '''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast("GoogleLookerInstanceMaintenanceWindowStartTime", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleLookerInstanceMaintenanceWindow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleLookerInstanceMaintenanceWindowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleLookerInstance.GoogleLookerInstanceMaintenanceWindowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6a248d9e288d8f81c80b772209e2c349e4ff967929f2fb0b23d50b3f4ea0776)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putStartTime")
    def put_start_time(
        self,
        *,
        hours: typing.Optional[jsii.Number] = None,
        minutes: typing.Optional[jsii.Number] = None,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hours: Hours of day in 24 hour format. Should be from 0 to 23. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#hours GoogleLookerInstance#hours}
        :param minutes: Minutes of hour of day. Must be from 0 to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#minutes GoogleLookerInstance#minutes}
        :param nanos: Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#nanos GoogleLookerInstance#nanos}
        :param seconds: Seconds of minutes of the time. Must normally be from 0 to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#seconds GoogleLookerInstance#seconds}
        '''
        value = GoogleLookerInstanceMaintenanceWindowStartTime(
            hours=hours, minutes=minutes, nanos=nanos, seconds=seconds
        )

        return typing.cast(None, jsii.invoke(self, "putStartTime", [value]))

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(
        self,
    ) -> "GoogleLookerInstanceMaintenanceWindowStartTimeOutputReference":
        return typing.cast("GoogleLookerInstanceMaintenanceWindowStartTimeOutputReference", jsii.get(self, "startTime"))

    @builtins.property
    @jsii.member(jsii_name="dayOfWeekInput")
    def day_of_week_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dayOfWeekInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(
        self,
    ) -> typing.Optional["GoogleLookerInstanceMaintenanceWindowStartTime"]:
        return typing.cast(typing.Optional["GoogleLookerInstanceMaintenanceWindowStartTime"], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="dayOfWeek")
    def day_of_week(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dayOfWeek"))

    @day_of_week.setter
    def day_of_week(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c928c49dd3401ec8ea7a599b8b70473e0557e567cce4ee5deeec85e8b00d1813)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dayOfWeek", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleLookerInstanceMaintenanceWindow]:
        return typing.cast(typing.Optional[GoogleLookerInstanceMaintenanceWindow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleLookerInstanceMaintenanceWindow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a27b531e494512cf0fe9ebe385452e775ac34934c8c5319204a9c3551693d83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleLookerInstance.GoogleLookerInstanceMaintenanceWindowStartTime",
    jsii_struct_bases=[],
    name_mapping={
        "hours": "hours",
        "minutes": "minutes",
        "nanos": "nanos",
        "seconds": "seconds",
    },
)
class GoogleLookerInstanceMaintenanceWindowStartTime:
    def __init__(
        self,
        *,
        hours: typing.Optional[jsii.Number] = None,
        minutes: typing.Optional[jsii.Number] = None,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hours: Hours of day in 24 hour format. Should be from 0 to 23. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#hours GoogleLookerInstance#hours}
        :param minutes: Minutes of hour of day. Must be from 0 to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#minutes GoogleLookerInstance#minutes}
        :param nanos: Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#nanos GoogleLookerInstance#nanos}
        :param seconds: Seconds of minutes of the time. Must normally be from 0 to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#seconds GoogleLookerInstance#seconds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a0827b2b0cd6c13c3539d9425d33e27b3edc8ee3bc59c8380281b5bf12a5161)
            check_type(argname="argument hours", value=hours, expected_type=type_hints["hours"])
            check_type(argname="argument minutes", value=minutes, expected_type=type_hints["minutes"])
            check_type(argname="argument nanos", value=nanos, expected_type=type_hints["nanos"])
            check_type(argname="argument seconds", value=seconds, expected_type=type_hints["seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if hours is not None:
            self._values["hours"] = hours
        if minutes is not None:
            self._values["minutes"] = minutes
        if nanos is not None:
            self._values["nanos"] = nanos
        if seconds is not None:
            self._values["seconds"] = seconds

    @builtins.property
    def hours(self) -> typing.Optional[jsii.Number]:
        '''Hours of day in 24 hour format. Should be from 0 to 23.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#hours GoogleLookerInstance#hours}
        '''
        result = self._values.get("hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minutes(self) -> typing.Optional[jsii.Number]:
        '''Minutes of hour of day. Must be from 0 to 59.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#minutes GoogleLookerInstance#minutes}
        '''
        result = self._values.get("minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nanos(self) -> typing.Optional[jsii.Number]:
        '''Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#nanos GoogleLookerInstance#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def seconds(self) -> typing.Optional[jsii.Number]:
        '''Seconds of minutes of the time. Must normally be from 0 to 59.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#seconds GoogleLookerInstance#seconds}
        '''
        result = self._values.get("seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleLookerInstanceMaintenanceWindowStartTime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleLookerInstanceMaintenanceWindowStartTimeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleLookerInstance.GoogleLookerInstanceMaintenanceWindowStartTimeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9bfd514a161d30c4a1ccafdebba6967075ad96dedcbe873c1c9df098f4f917ca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHours")
    def reset_hours(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHours", []))

    @jsii.member(jsii_name="resetMinutes")
    def reset_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinutes", []))

    @jsii.member(jsii_name="resetNanos")
    def reset_nanos(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNanos", []))

    @jsii.member(jsii_name="resetSeconds")
    def reset_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="hoursInput")
    def hours_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hoursInput"))

    @builtins.property
    @jsii.member(jsii_name="minutesInput")
    def minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minutesInput"))

    @builtins.property
    @jsii.member(jsii_name="nanosInput")
    def nanos_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nanosInput"))

    @builtins.property
    @jsii.member(jsii_name="secondsInput")
    def seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "secondsInput"))

    @builtins.property
    @jsii.member(jsii_name="hours")
    def hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hours"))

    @hours.setter
    def hours(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf2c4ca33d7d85305036f8e2c64117005f179e7d3504e303376223b06d1bf223)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minutes")
    def minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minutes"))

    @minutes.setter
    def minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3a4dc0414216c4e84aa78be0855d211118dca6542c899d5e513d69f2adf9871)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @nanos.setter
    def nanos(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__907576ba20aed0821880bcdda4c8ac72f08925c06f524b390aacf0aa65f4b9c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93b39c7ae1189189e4f1f04665da754a6b029585472e937d75d93fa15d555216)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleLookerInstanceMaintenanceWindowStartTime]:
        return typing.cast(typing.Optional[GoogleLookerInstanceMaintenanceWindowStartTime], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleLookerInstanceMaintenanceWindowStartTime],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b83b9196a7118c64e42d95bd2d9033192cd3a6e7d982b0ef217ab5d10994e35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleLookerInstance.GoogleLookerInstanceOauthConfig",
    jsii_struct_bases=[],
    name_mapping={"client_id": "clientId", "client_secret": "clientSecret"},
)
class GoogleLookerInstanceOauthConfig:
    def __init__(self, *, client_id: builtins.str, client_secret: builtins.str) -> None:
        '''
        :param client_id: The client ID for the Oauth config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#client_id GoogleLookerInstance#client_id}
        :param client_secret: The client secret for the Oauth config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#client_secret GoogleLookerInstance#client_secret}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4c14b47faf5ead24b5f2821a6d812bb06770cc4a4fbae367fdc51d27634bc1a)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
            "client_secret": client_secret,
        }

    @builtins.property
    def client_id(self) -> builtins.str:
        '''The client ID for the Oauth config.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#client_id GoogleLookerInstance#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(self) -> builtins.str:
        '''The client secret for the Oauth config.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#client_secret GoogleLookerInstance#client_secret}
        '''
        result = self._values.get("client_secret")
        assert result is not None, "Required property 'client_secret' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleLookerInstanceOauthConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleLookerInstanceOauthConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleLookerInstance.GoogleLookerInstanceOauthConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d766e99d3c4553dc794006897dba5463e563623c09a245147875466eb91ecf69)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edb6f6372192aefa1d4b41c1430818ed8e9d3584240b303a41cf4868a6fba05f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc3c8e2d341bad9b8433c53fac293da82d02eec9e172ab4cc8168268180455b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleLookerInstanceOauthConfig]:
        return typing.cast(typing.Optional[GoogleLookerInstanceOauthConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleLookerInstanceOauthConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e7268d51bb6dbd484044884ca83846147ac3868df6ea8229deb5433b88dd367)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleLookerInstance.GoogleLookerInstancePscConfig",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_vpcs": "allowedVpcs",
        "service_attachments": "serviceAttachments",
    },
)
class GoogleLookerInstancePscConfig:
    def __init__(
        self,
        *,
        allowed_vpcs: typing.Optional[typing.Sequence[builtins.str]] = None,
        service_attachments: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleLookerInstancePscConfigServiceAttachments", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param allowed_vpcs: List of VPCs that are allowed ingress into the Looker instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#allowed_vpcs GoogleLookerInstance#allowed_vpcs}
        :param service_attachments: service_attachments block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#service_attachments GoogleLookerInstance#service_attachments}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b217e9a0281809d608549889693c9ff50e344e566a257d1fa184c9502fedf01)
            check_type(argname="argument allowed_vpcs", value=allowed_vpcs, expected_type=type_hints["allowed_vpcs"])
            check_type(argname="argument service_attachments", value=service_attachments, expected_type=type_hints["service_attachments"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_vpcs is not None:
            self._values["allowed_vpcs"] = allowed_vpcs
        if service_attachments is not None:
            self._values["service_attachments"] = service_attachments

    @builtins.property
    def allowed_vpcs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of VPCs that are allowed ingress into the Looker instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#allowed_vpcs GoogleLookerInstance#allowed_vpcs}
        '''
        result = self._values.get("allowed_vpcs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def service_attachments(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleLookerInstancePscConfigServiceAttachments"]]]:
        '''service_attachments block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#service_attachments GoogleLookerInstance#service_attachments}
        '''
        result = self._values.get("service_attachments")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleLookerInstancePscConfigServiceAttachments"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleLookerInstancePscConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleLookerInstancePscConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleLookerInstance.GoogleLookerInstancePscConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4738db210bf3e54781bda001ada6686ba52b5ad9578ecd5dea4933a7d98898e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putServiceAttachments")
    def put_service_attachments(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleLookerInstancePscConfigServiceAttachments", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c73c33ce21a54c11fe0b7894b3286b2b991d3b9f33c55504076adcc0870ee54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putServiceAttachments", [value]))

    @jsii.member(jsii_name="resetAllowedVpcs")
    def reset_allowed_vpcs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedVpcs", []))

    @jsii.member(jsii_name="resetServiceAttachments")
    def reset_service_attachments(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAttachments", []))

    @builtins.property
    @jsii.member(jsii_name="lookerServiceAttachmentUri")
    def looker_service_attachment_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lookerServiceAttachmentUri"))

    @builtins.property
    @jsii.member(jsii_name="serviceAttachments")
    def service_attachments(
        self,
    ) -> "GoogleLookerInstancePscConfigServiceAttachmentsList":
        return typing.cast("GoogleLookerInstancePscConfigServiceAttachmentsList", jsii.get(self, "serviceAttachments"))

    @builtins.property
    @jsii.member(jsii_name="allowedVpcsInput")
    def allowed_vpcs_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedVpcsInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAttachmentsInput")
    def service_attachments_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleLookerInstancePscConfigServiceAttachments"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleLookerInstancePscConfigServiceAttachments"]]], jsii.get(self, "serviceAttachmentsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedVpcs")
    def allowed_vpcs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedVpcs"))

    @allowed_vpcs.setter
    def allowed_vpcs(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94c440b2bdcc57aebfeefb5f15a002ad04ba50d5acb61392bed2513d95657a39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedVpcs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleLookerInstancePscConfig]:
        return typing.cast(typing.Optional[GoogleLookerInstancePscConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleLookerInstancePscConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39f82e00398ab35f0055d707ad679d83d2df3eae43d49f01eef5883251bbbf78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleLookerInstance.GoogleLookerInstancePscConfigServiceAttachments",
    jsii_struct_bases=[],
    name_mapping={
        "local_fqdn": "localFqdn",
        "target_service_attachment_uri": "targetServiceAttachmentUri",
    },
)
class GoogleLookerInstancePscConfigServiceAttachments:
    def __init__(
        self,
        *,
        local_fqdn: typing.Optional[builtins.str] = None,
        target_service_attachment_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param local_fqdn: Fully qualified domain name that will be used in the private DNS record created for the service attachment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#local_fqdn GoogleLookerInstance#local_fqdn}
        :param target_service_attachment_uri: URI of the service attachment to connect to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#target_service_attachment_uri GoogleLookerInstance#target_service_attachment_uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3c0955372ad90de980a986ddf180b7a6bd66ec67a3e3c1a47d5056b676638c6)
            check_type(argname="argument local_fqdn", value=local_fqdn, expected_type=type_hints["local_fqdn"])
            check_type(argname="argument target_service_attachment_uri", value=target_service_attachment_uri, expected_type=type_hints["target_service_attachment_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if local_fqdn is not None:
            self._values["local_fqdn"] = local_fqdn
        if target_service_attachment_uri is not None:
            self._values["target_service_attachment_uri"] = target_service_attachment_uri

    @builtins.property
    def local_fqdn(self) -> typing.Optional[builtins.str]:
        '''Fully qualified domain name that will be used in the private DNS record created for the service attachment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#local_fqdn GoogleLookerInstance#local_fqdn}
        '''
        result = self._values.get("local_fqdn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_service_attachment_uri(self) -> typing.Optional[builtins.str]:
        '''URI of the service attachment to connect to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#target_service_attachment_uri GoogleLookerInstance#target_service_attachment_uri}
        '''
        result = self._values.get("target_service_attachment_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleLookerInstancePscConfigServiceAttachments(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleLookerInstancePscConfigServiceAttachmentsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleLookerInstance.GoogleLookerInstancePscConfigServiceAttachmentsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd76b2729e432fb4337228e61cecd190c3ef159a56d9e807237db6398b4dd751)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleLookerInstancePscConfigServiceAttachmentsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__510644b7919eeb4212469a5d769fc8a2fca66a87cc6bdf5984fef510d3e0eaf4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleLookerInstancePscConfigServiceAttachmentsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e2418deb9acceada5f3aee5a4a8462e1fae3835ccb6ba48d2bf0ee3628f72dd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__392733c3aefc048cb6bee609996c64e6324463ef3e0fc6103ac3e40e75d04d10)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb0e262b78a14d729953f8edcc6dc2d58dd874dcd394237c457a6b9e2ca3f81b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleLookerInstancePscConfigServiceAttachments]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleLookerInstancePscConfigServiceAttachments]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleLookerInstancePscConfigServiceAttachments]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c620a9222eab88ec3ae7942b0f65967e1856b1bf8fea56cf983934473556d97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleLookerInstancePscConfigServiceAttachmentsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleLookerInstance.GoogleLookerInstancePscConfigServiceAttachmentsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__956cf4046d6f2e6235068a28fc18c01468d7abaa01aa2ab461633b64b74dae88)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetLocalFqdn")
    def reset_local_fqdn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalFqdn", []))

    @jsii.member(jsii_name="resetTargetServiceAttachmentUri")
    def reset_target_service_attachment_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetServiceAttachmentUri", []))

    @builtins.property
    @jsii.member(jsii_name="connectionStatus")
    def connection_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionStatus"))

    @builtins.property
    @jsii.member(jsii_name="localFqdnInput")
    def local_fqdn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localFqdnInput"))

    @builtins.property
    @jsii.member(jsii_name="targetServiceAttachmentUriInput")
    def target_service_attachment_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetServiceAttachmentUriInput"))

    @builtins.property
    @jsii.member(jsii_name="localFqdn")
    def local_fqdn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localFqdn"))

    @local_fqdn.setter
    def local_fqdn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d464a8f33d2c2408b47c6d78e5833ce56af5133c7c91458969bb27df813ba5f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localFqdn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetServiceAttachmentUri")
    def target_service_attachment_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetServiceAttachmentUri"))

    @target_service_attachment_uri.setter
    def target_service_attachment_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ab982f58828a18bb5c3e0254642168ccd956000245e699519f5d5140c9ae6cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetServiceAttachmentUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleLookerInstancePscConfigServiceAttachments]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleLookerInstancePscConfigServiceAttachments]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleLookerInstancePscConfigServiceAttachments]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__227a76ae1af798e50e18c2b3b60050dc8b953c8fe6aeaede3f3fd8742d604e9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleLookerInstance.GoogleLookerInstanceTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleLookerInstanceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#create GoogleLookerInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#delete GoogleLookerInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#update GoogleLookerInstance#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__279b3118a6780f9f8bd7b4dfe4d4cfdcb72968bcc614576ecad61155d93ae2a1)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#create GoogleLookerInstance#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#delete GoogleLookerInstance#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#update GoogleLookerInstance#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleLookerInstanceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleLookerInstanceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleLookerInstance.GoogleLookerInstanceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5515811fb892a6e478307a0da248ecc2ba6b5f4e49309ec111351f92a78bd2b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__19bee73677e2218aef1bdc77dd1b3ef0726594867e7331e35d47197e328ca4ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__227373481bf3d5dc6a8e32707bd5fec84ddd21bbb850d582c1c63e10ed07d2cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22c0e360d68579f1b1618b009a1f09df95c064c00ba6155263340bfcb1fbbc1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleLookerInstanceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleLookerInstanceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleLookerInstanceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39865c1c5698eca2c01e50eae785c3a25fe40588452736aae930f4f38ef97426)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleLookerInstance.GoogleLookerInstanceUserMetadata",
    jsii_struct_bases=[],
    name_mapping={
        "additional_developer_user_count": "additionalDeveloperUserCount",
        "additional_standard_user_count": "additionalStandardUserCount",
        "additional_viewer_user_count": "additionalViewerUserCount",
    },
)
class GoogleLookerInstanceUserMetadata:
    def __init__(
        self,
        *,
        additional_developer_user_count: typing.Optional[jsii.Number] = None,
        additional_standard_user_count: typing.Optional[jsii.Number] = None,
        additional_viewer_user_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param additional_developer_user_count: Number of additional Developer Users to allocate to the Looker Instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#additional_developer_user_count GoogleLookerInstance#additional_developer_user_count}
        :param additional_standard_user_count: Number of additional Standard Users to allocate to the Looker Instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#additional_standard_user_count GoogleLookerInstance#additional_standard_user_count}
        :param additional_viewer_user_count: Number of additional Viewer Users to allocate to the Looker Instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#additional_viewer_user_count GoogleLookerInstance#additional_viewer_user_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9685fd13ef5866d8dcd12f723139a4d56d005aa7c87793c9da6175d00063fec)
            check_type(argname="argument additional_developer_user_count", value=additional_developer_user_count, expected_type=type_hints["additional_developer_user_count"])
            check_type(argname="argument additional_standard_user_count", value=additional_standard_user_count, expected_type=type_hints["additional_standard_user_count"])
            check_type(argname="argument additional_viewer_user_count", value=additional_viewer_user_count, expected_type=type_hints["additional_viewer_user_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if additional_developer_user_count is not None:
            self._values["additional_developer_user_count"] = additional_developer_user_count
        if additional_standard_user_count is not None:
            self._values["additional_standard_user_count"] = additional_standard_user_count
        if additional_viewer_user_count is not None:
            self._values["additional_viewer_user_count"] = additional_viewer_user_count

    @builtins.property
    def additional_developer_user_count(self) -> typing.Optional[jsii.Number]:
        '''Number of additional Developer Users to allocate to the Looker Instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#additional_developer_user_count GoogleLookerInstance#additional_developer_user_count}
        '''
        result = self._values.get("additional_developer_user_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def additional_standard_user_count(self) -> typing.Optional[jsii.Number]:
        '''Number of additional Standard Users to allocate to the Looker Instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#additional_standard_user_count GoogleLookerInstance#additional_standard_user_count}
        '''
        result = self._values.get("additional_standard_user_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def additional_viewer_user_count(self) -> typing.Optional[jsii.Number]:
        '''Number of additional Viewer Users to allocate to the Looker Instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_looker_instance#additional_viewer_user_count GoogleLookerInstance#additional_viewer_user_count}
        '''
        result = self._values.get("additional_viewer_user_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleLookerInstanceUserMetadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleLookerInstanceUserMetadataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleLookerInstance.GoogleLookerInstanceUserMetadataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cded1f00a4df05847d996360a94bc28f3f3ea7f91d0251cdc25fa10842a700c2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAdditionalDeveloperUserCount")
    def reset_additional_developer_user_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalDeveloperUserCount", []))

    @jsii.member(jsii_name="resetAdditionalStandardUserCount")
    def reset_additional_standard_user_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalStandardUserCount", []))

    @jsii.member(jsii_name="resetAdditionalViewerUserCount")
    def reset_additional_viewer_user_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalViewerUserCount", []))

    @builtins.property
    @jsii.member(jsii_name="additionalDeveloperUserCountInput")
    def additional_developer_user_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "additionalDeveloperUserCountInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalStandardUserCountInput")
    def additional_standard_user_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "additionalStandardUserCountInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalViewerUserCountInput")
    def additional_viewer_user_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "additionalViewerUserCountInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalDeveloperUserCount")
    def additional_developer_user_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "additionalDeveloperUserCount"))

    @additional_developer_user_count.setter
    def additional_developer_user_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8e97702e493601236a96b9f154252ff6ce8ace57c7c1af5926a01e9196f389d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalDeveloperUserCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="additionalStandardUserCount")
    def additional_standard_user_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "additionalStandardUserCount"))

    @additional_standard_user_count.setter
    def additional_standard_user_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__756064b1234e5e0eeb6ce558a2fcc9abd5d06818d8424b979d0621810e07070c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalStandardUserCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="additionalViewerUserCount")
    def additional_viewer_user_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "additionalViewerUserCount"))

    @additional_viewer_user_count.setter
    def additional_viewer_user_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d79f98a0a1370768268174c2e76028d76f7d9206aa897a6fa2c24aa615b0045)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalViewerUserCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleLookerInstanceUserMetadata]:
        return typing.cast(typing.Optional[GoogleLookerInstanceUserMetadata], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleLookerInstanceUserMetadata],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__545dc0774c77811c987613f076b2e321a1e289e9ed2befe60713209ae205476f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleLookerInstance",
    "GoogleLookerInstanceAdminSettings",
    "GoogleLookerInstanceAdminSettingsOutputReference",
    "GoogleLookerInstanceConfig",
    "GoogleLookerInstanceCustomDomain",
    "GoogleLookerInstanceCustomDomainOutputReference",
    "GoogleLookerInstanceDenyMaintenancePeriod",
    "GoogleLookerInstanceDenyMaintenancePeriodEndDate",
    "GoogleLookerInstanceDenyMaintenancePeriodEndDateOutputReference",
    "GoogleLookerInstanceDenyMaintenancePeriodOutputReference",
    "GoogleLookerInstanceDenyMaintenancePeriodStartDate",
    "GoogleLookerInstanceDenyMaintenancePeriodStartDateOutputReference",
    "GoogleLookerInstanceDenyMaintenancePeriodTime",
    "GoogleLookerInstanceDenyMaintenancePeriodTimeOutputReference",
    "GoogleLookerInstanceEncryptionConfig",
    "GoogleLookerInstanceEncryptionConfigOutputReference",
    "GoogleLookerInstanceMaintenanceWindow",
    "GoogleLookerInstanceMaintenanceWindowOutputReference",
    "GoogleLookerInstanceMaintenanceWindowStartTime",
    "GoogleLookerInstanceMaintenanceWindowStartTimeOutputReference",
    "GoogleLookerInstanceOauthConfig",
    "GoogleLookerInstanceOauthConfigOutputReference",
    "GoogleLookerInstancePscConfig",
    "GoogleLookerInstancePscConfigOutputReference",
    "GoogleLookerInstancePscConfigServiceAttachments",
    "GoogleLookerInstancePscConfigServiceAttachmentsList",
    "GoogleLookerInstancePscConfigServiceAttachmentsOutputReference",
    "GoogleLookerInstanceTimeouts",
    "GoogleLookerInstanceTimeoutsOutputReference",
    "GoogleLookerInstanceUserMetadata",
    "GoogleLookerInstanceUserMetadataOutputReference",
]

publication.publish()

def _typecheckingstub__75fc0bd078a1f4d6b895160bbb3e361c144807f6702482438fcaa6fb2acfaac5(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    oauth_config: typing.Union[GoogleLookerInstanceOauthConfig, typing.Dict[builtins.str, typing.Any]],
    admin_settings: typing.Optional[typing.Union[GoogleLookerInstanceAdminSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    consumer_network: typing.Optional[builtins.str] = None,
    custom_domain: typing.Optional[typing.Union[GoogleLookerInstanceCustomDomain, typing.Dict[builtins.str, typing.Any]]] = None,
    deletion_policy: typing.Optional[builtins.str] = None,
    deny_maintenance_period: typing.Optional[typing.Union[GoogleLookerInstanceDenyMaintenancePeriod, typing.Dict[builtins.str, typing.Any]]] = None,
    encryption_config: typing.Optional[typing.Union[GoogleLookerInstanceEncryptionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    fips_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    maintenance_window: typing.Optional[typing.Union[GoogleLookerInstanceMaintenanceWindow, typing.Dict[builtins.str, typing.Any]]] = None,
    platform_edition: typing.Optional[builtins.str] = None,
    private_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project: typing.Optional[builtins.str] = None,
    psc_config: typing.Optional[typing.Union[GoogleLookerInstancePscConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    psc_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    public_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    region: typing.Optional[builtins.str] = None,
    reserved_range: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleLookerInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    user_metadata: typing.Optional[typing.Union[GoogleLookerInstanceUserMetadata, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__e0be6f0bfbfcdbe7eabbe6a668e3d435cdc129b1156c363db412595a747bea5c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18493d6bd0e6723c395eb6de7369469e7eabd3fb29911166e612dec98ac9a8ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fcda5af44dc743230fd8dbed2de5212fcd0fe655f73e13e22473fac0dbb5349(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4d4b57132b18f16fa66ef2c32d26f721b1ea7e88d5dc7eac67743790d178cb6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00bbdb09d647145d752cf43d5a3042a65c868c549932e57b57535f748f14ae55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43e13ab5078202e657db43dc73fd16782024d2f14ba147986983e757389c65e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb6a20acf53b78f46d488b8a6ed3b3d42d0c5aaa2b4856fad3ce72d497fb920a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f6fc4975fce9f545448dafc7da40223caf321410e965eb93d9800f5cceaa6c7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd4b3095879edaae560c2be91d3e753bd3f5b8dd10fc6b4ff3fe10a9e9962e91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__361dd1c8ca2b2ca1deda9d4c05bf40d94c34988c3e93d0ded8f1b0687e10c61c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0348c3a5894e9b43f3639c66e7947bb14220e07279127590df4bfc41945ed306(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0f829e1d3a8b3de80a5158a560e0063585a0315437d25fde82a17580a6a35f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00e54345fba86c628adb59708d2bf97b96503795ce7eba3e93cfd63197d41eb0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b6b382d3a78184a830957f242d602ed68856fd02c2c34bf1b5781206ce95cee(
    *,
    allowed_email_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5d11181e6dcef4772ba023c1f51ab87aca6cfddb7b86682eb46817923813dde(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78bf0b287304c2b1741dd0d1f8ddff244d42b9b1fceaacc3fefec66f3b58a78e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04e19c845f874e605600fcf92f84254eff8505174c77bc5133ed14e24a08b8a2(
    value: typing.Optional[GoogleLookerInstanceAdminSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88b271d42a1265e510434620991bc659d6e8f5967bdfc689386ec953e98d3be4(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    oauth_config: typing.Union[GoogleLookerInstanceOauthConfig, typing.Dict[builtins.str, typing.Any]],
    admin_settings: typing.Optional[typing.Union[GoogleLookerInstanceAdminSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    consumer_network: typing.Optional[builtins.str] = None,
    custom_domain: typing.Optional[typing.Union[GoogleLookerInstanceCustomDomain, typing.Dict[builtins.str, typing.Any]]] = None,
    deletion_policy: typing.Optional[builtins.str] = None,
    deny_maintenance_period: typing.Optional[typing.Union[GoogleLookerInstanceDenyMaintenancePeriod, typing.Dict[builtins.str, typing.Any]]] = None,
    encryption_config: typing.Optional[typing.Union[GoogleLookerInstanceEncryptionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    fips_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    maintenance_window: typing.Optional[typing.Union[GoogleLookerInstanceMaintenanceWindow, typing.Dict[builtins.str, typing.Any]]] = None,
    platform_edition: typing.Optional[builtins.str] = None,
    private_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project: typing.Optional[builtins.str] = None,
    psc_config: typing.Optional[typing.Union[GoogleLookerInstancePscConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    psc_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    public_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    region: typing.Optional[builtins.str] = None,
    reserved_range: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleLookerInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    user_metadata: typing.Optional[typing.Union[GoogleLookerInstanceUserMetadata, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__970246e31f61542a823f0e6f4459c17c692e6d04e0aabc4915af08d9e788b072(
    *,
    domain: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__025f8710b82e51bc625964c38192c42325f7305eb7822d1e1ea43d6954fc244e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a7d3bfcbccd33e592776c98b7cb58f49d23d8574cbf0e85efdb515ac6cca99e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b135f8adc56bf82951c64f60f9c2feb52c2ea95319c8055aba390ae966422d4a(
    value: typing.Optional[GoogleLookerInstanceCustomDomain],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fce11a4cd688551c648e6e78e7527af046b1efc2c7c2c1631c8a6f6e05e63f51(
    *,
    end_date: typing.Union[GoogleLookerInstanceDenyMaintenancePeriodEndDate, typing.Dict[builtins.str, typing.Any]],
    start_date: typing.Union[GoogleLookerInstanceDenyMaintenancePeriodStartDate, typing.Dict[builtins.str, typing.Any]],
    time: typing.Union[GoogleLookerInstanceDenyMaintenancePeriodTime, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01be8b5b242a38500b9b8ecacdeaaf4095ecda06968f79da5a0de875db15563d(
    *,
    day: typing.Optional[jsii.Number] = None,
    month: typing.Optional[jsii.Number] = None,
    year: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__761a5fc41ebc01904d75e038d1bbeee2faa51b208225afb151e38623c37222d0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6112883115ddaf7ba6cff7f512f45f3e5130ad7a93133e29da61dbb08643caf2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67626b57acc06098438b5a12bcbe56e6c8456ed7af2e9e93df4f70b3dc516839(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dfcbe5a8c15139e888a898f9caf3bef607fba58affdfae82534d7ab3ff91de3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__585ba5c4bf73a2d0c0f4fadfb9d63fbb387144aff884add9eec88270d674880a(
    value: typing.Optional[GoogleLookerInstanceDenyMaintenancePeriodEndDate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4787e391a86f22a772531dae4690d52cfa383babbb689a798bc68a42ff3ebafd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__995966fbd40da78cf9fd23fc6495939939ddae52b4077bb5e814b0c25bfa105a(
    value: typing.Optional[GoogleLookerInstanceDenyMaintenancePeriod],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b1cdfa5b03960fe09dade3279ed1077b13d64997de50dca9a6273593d30dabf(
    *,
    day: typing.Optional[jsii.Number] = None,
    month: typing.Optional[jsii.Number] = None,
    year: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aed90be17dc5ce477fe14f8976fb139076c1a90c4a53ebd959b524eed77e4d6a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8041f6e722ac3ebdd6b255aeee677ef722f01553e9b78d35d3f21402c6448068(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9da88b7c197e0b35dcf6f9dde3cf0becd9e6d1914f611b4cb708f926e9d3f405(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef1a900272e837b0f1c3083406bf0a6275176a662b300e26da2ef727256c4fdb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb825ec4ee6df0e53819d6e8532a3d22b937b0be488dcf431591a2e1fa3bbf27(
    value: typing.Optional[GoogleLookerInstanceDenyMaintenancePeriodStartDate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0791b6087d52db8fbe26eb542a1af81237bc0123aa75d488cb13dd6689f8eb0d(
    *,
    hours: typing.Optional[jsii.Number] = None,
    minutes: typing.Optional[jsii.Number] = None,
    nanos: typing.Optional[jsii.Number] = None,
    seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e00a649febe793cc7104e9979e4cd065fa52faee850222ea15c130b46cd7173(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3476e9691c975c74b0ff2073603efddbd9425385389aae6bf4990e5182fa5e6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__860075542ef78f730675d2017da17a939ae440fc465fce8566e08691768601e3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f81137fbe4c01a625cb6b115ad55920a80672f4bf7c75666f81349ef28d7ea50(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e615236c3c4c8d99ab1f3b20b665a9c66cef406a2c041184aff061e6938bef3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59e2bf33bc74608ae4dbeec02432ab6f20c6bf4b71b62c12cd05fe0cdff08f3f(
    value: typing.Optional[GoogleLookerInstanceDenyMaintenancePeriodTime],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__755585655e778e16507f1f0e180bc0a2249d75e390beede780d93ac40bfb34db(
    *,
    kms_key_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7769340f9d6ace473261ea07c4e930b633e33e49c12c89515cae082c71f460a0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00f35b68617915176c8fb4023f9d396408e4a2d16af74fad94b09d8ce39a8917(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92a50b48c73762a535f6c9759793e8416d035778c31bc850668a1afc22258fc9(
    value: typing.Optional[GoogleLookerInstanceEncryptionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5c77d3a8091e310b30a46fb7c3b5c64c1967237b840aa39f51c1197dba06b8f(
    *,
    day_of_week: builtins.str,
    start_time: typing.Union[GoogleLookerInstanceMaintenanceWindowStartTime, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6a248d9e288d8f81c80b772209e2c349e4ff967929f2fb0b23d50b3f4ea0776(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c928c49dd3401ec8ea7a599b8b70473e0557e567cce4ee5deeec85e8b00d1813(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a27b531e494512cf0fe9ebe385452e775ac34934c8c5319204a9c3551693d83(
    value: typing.Optional[GoogleLookerInstanceMaintenanceWindow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a0827b2b0cd6c13c3539d9425d33e27b3edc8ee3bc59c8380281b5bf12a5161(
    *,
    hours: typing.Optional[jsii.Number] = None,
    minutes: typing.Optional[jsii.Number] = None,
    nanos: typing.Optional[jsii.Number] = None,
    seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bfd514a161d30c4a1ccafdebba6967075ad96dedcbe873c1c9df098f4f917ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf2c4ca33d7d85305036f8e2c64117005f179e7d3504e303376223b06d1bf223(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3a4dc0414216c4e84aa78be0855d211118dca6542c899d5e513d69f2adf9871(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__907576ba20aed0821880bcdda4c8ac72f08925c06f524b390aacf0aa65f4b9c9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93b39c7ae1189189e4f1f04665da754a6b029585472e937d75d93fa15d555216(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b83b9196a7118c64e42d95bd2d9033192cd3a6e7d982b0ef217ab5d10994e35(
    value: typing.Optional[GoogleLookerInstanceMaintenanceWindowStartTime],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4c14b47faf5ead24b5f2821a6d812bb06770cc4a4fbae367fdc51d27634bc1a(
    *,
    client_id: builtins.str,
    client_secret: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d766e99d3c4553dc794006897dba5463e563623c09a245147875466eb91ecf69(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edb6f6372192aefa1d4b41c1430818ed8e9d3584240b303a41cf4868a6fba05f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc3c8e2d341bad9b8433c53fac293da82d02eec9e172ab4cc8168268180455b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e7268d51bb6dbd484044884ca83846147ac3868df6ea8229deb5433b88dd367(
    value: typing.Optional[GoogleLookerInstanceOauthConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b217e9a0281809d608549889693c9ff50e344e566a257d1fa184c9502fedf01(
    *,
    allowed_vpcs: typing.Optional[typing.Sequence[builtins.str]] = None,
    service_attachments: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleLookerInstancePscConfigServiceAttachments, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4738db210bf3e54781bda001ada6686ba52b5ad9578ecd5dea4933a7d98898e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c73c33ce21a54c11fe0b7894b3286b2b991d3b9f33c55504076adcc0870ee54(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleLookerInstancePscConfigServiceAttachments, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94c440b2bdcc57aebfeefb5f15a002ad04ba50d5acb61392bed2513d95657a39(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39f82e00398ab35f0055d707ad679d83d2df3eae43d49f01eef5883251bbbf78(
    value: typing.Optional[GoogleLookerInstancePscConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3c0955372ad90de980a986ddf180b7a6bd66ec67a3e3c1a47d5056b676638c6(
    *,
    local_fqdn: typing.Optional[builtins.str] = None,
    target_service_attachment_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd76b2729e432fb4337228e61cecd190c3ef159a56d9e807237db6398b4dd751(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__510644b7919eeb4212469a5d769fc8a2fca66a87cc6bdf5984fef510d3e0eaf4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e2418deb9acceada5f3aee5a4a8462e1fae3835ccb6ba48d2bf0ee3628f72dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__392733c3aefc048cb6bee609996c64e6324463ef3e0fc6103ac3e40e75d04d10(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb0e262b78a14d729953f8edcc6dc2d58dd874dcd394237c457a6b9e2ca3f81b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c620a9222eab88ec3ae7942b0f65967e1856b1bf8fea56cf983934473556d97(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleLookerInstancePscConfigServiceAttachments]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__956cf4046d6f2e6235068a28fc18c01468d7abaa01aa2ab461633b64b74dae88(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d464a8f33d2c2408b47c6d78e5833ce56af5133c7c91458969bb27df813ba5f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ab982f58828a18bb5c3e0254642168ccd956000245e699519f5d5140c9ae6cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__227a76ae1af798e50e18c2b3b60050dc8b953c8fe6aeaede3f3fd8742d604e9f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleLookerInstancePscConfigServiceAttachments]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__279b3118a6780f9f8bd7b4dfe4d4cfdcb72968bcc614576ecad61155d93ae2a1(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5515811fb892a6e478307a0da248ecc2ba6b5f4e49309ec111351f92a78bd2b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19bee73677e2218aef1bdc77dd1b3ef0726594867e7331e35d47197e328ca4ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__227373481bf3d5dc6a8e32707bd5fec84ddd21bbb850d582c1c63e10ed07d2cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22c0e360d68579f1b1618b009a1f09df95c064c00ba6155263340bfcb1fbbc1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39865c1c5698eca2c01e50eae785c3a25fe40588452736aae930f4f38ef97426(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleLookerInstanceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9685fd13ef5866d8dcd12f723139a4d56d005aa7c87793c9da6175d00063fec(
    *,
    additional_developer_user_count: typing.Optional[jsii.Number] = None,
    additional_standard_user_count: typing.Optional[jsii.Number] = None,
    additional_viewer_user_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cded1f00a4df05847d996360a94bc28f3f3ea7f91d0251cdc25fa10842a700c2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8e97702e493601236a96b9f154252ff6ce8ace57c7c1af5926a01e9196f389d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__756064b1234e5e0eeb6ce558a2fcc9abd5d06818d8424b979d0621810e07070c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d79f98a0a1370768268174c2e76028d76f7d9206aa897a6fa2c24aa615b0045(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__545dc0774c77811c987613f076b2e321a1e289e9ed2befe60713209ae205476f(
    value: typing.Optional[GoogleLookerInstanceUserMetadata],
) -> None:
    """Type checking stubs"""
    pass
