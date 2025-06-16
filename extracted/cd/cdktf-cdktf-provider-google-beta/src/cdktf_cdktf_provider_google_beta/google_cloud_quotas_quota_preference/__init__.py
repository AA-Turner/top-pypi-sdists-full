r'''
# `google_cloud_quotas_quota_preference`

Refer to the Terraform Registry for docs: [`google_cloud_quotas_quota_preference`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference).
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


class GoogleCloudQuotasQuotaPreference(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudQuotasQuotaPreference.GoogleCloudQuotasQuotaPreference",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference google_cloud_quotas_quota_preference}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        quota_config: typing.Union["GoogleCloudQuotasQuotaPreferenceQuotaConfig", typing.Dict[builtins.str, typing.Any]],
        contact_email: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        ignore_safety_checks: typing.Optional[builtins.str] = None,
        justification: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        parent: typing.Optional[builtins.str] = None,
        quota_id: typing.Optional[builtins.str] = None,
        service: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleCloudQuotasQuotaPreferenceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference google_cloud_quotas_quota_preference} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param quota_config: quota_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#quota_config GoogleCloudQuotasQuotaPreference#quota_config}
        :param contact_email: An email address that can be used for quota related communication between the Google Cloud and the user in case the Google Cloud needs further information to make a decision on whether the user preferred quota can be granted. The Google account for the email address must have quota update permission for the project, folder or organization this quota preference is for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#contact_email GoogleCloudQuotasQuotaPreference#contact_email}
        :param dimensions: The dimensions that this quota preference applies to. The key of the map entry is the name of a dimension, such as "region", "zone", "network_id", and the value of the map entry is the dimension value. If a dimension is missing from the map of dimensions, the quota preference applies to all the dimension values except for those that have other quota preferences configured for the specific value. NOTE: QuotaPreferences can only be applied across all values of "user" and "resource" dimension. Do not set values for "user" or "resource" in the dimension map. Example: '{"provider": "Foo Inc"}' where "provider" is a service specific dimension. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#dimensions GoogleCloudQuotasQuotaPreference#dimensions}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#id GoogleCloudQuotasQuotaPreference#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ignore_safety_checks: The list of quota safety checks to be ignored. Default value: "QUOTA_SAFETY_CHECK_UNSPECIFIED" Possible values: ["QUOTA_SAFETY_CHECK_UNSPECIFIED", "QUOTA_DECREASE_BELOW_USAGE", "QUOTA_DECREASE_PERCENTAGE_TOO_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#ignore_safety_checks GoogleCloudQuotasQuotaPreference#ignore_safety_checks}
        :param justification: The reason / justification for this quota preference. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#justification GoogleCloudQuotasQuotaPreference#justification}
        :param name: The resource name of the quota preference. Required except in the CREATE requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#name GoogleCloudQuotasQuotaPreference#name}
        :param parent: The parent of the quota preference. Allowed parents are "projects/[project-id / number]" or "folders/[folder-id / number]" or "organizations/[org-id / number]". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#parent GoogleCloudQuotasQuotaPreference#parent}
        :param quota_id: The id of the quota to which the quota preference is applied. A quota id is unique in the service. Example: 'CPUS-per-project-region'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#quota_id GoogleCloudQuotasQuotaPreference#quota_id}
        :param service: The name of the service to which the quota preference is applied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#service GoogleCloudQuotasQuotaPreference#service}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#timeouts GoogleCloudQuotasQuotaPreference#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c391be8bfbcc777d3a7eeed1515218fb716b8451f9c6055aa6fc0a4f04df814c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleCloudQuotasQuotaPreferenceConfig(
            quota_config=quota_config,
            contact_email=contact_email,
            dimensions=dimensions,
            id=id,
            ignore_safety_checks=ignore_safety_checks,
            justification=justification,
            name=name,
            parent=parent,
            quota_id=quota_id,
            service=service,
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
        '''Generates CDKTF code for importing a GoogleCloudQuotasQuotaPreference resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleCloudQuotasQuotaPreference to import.
        :param import_from_id: The id of the existing GoogleCloudQuotasQuotaPreference that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleCloudQuotasQuotaPreference to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afa5d7a4bf1612b959af69e88c72343107f5048d3d96aa85ea6c6bfab338f9b0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putQuotaConfig")
    def put_quota_config(
        self,
        *,
        preferred_value: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param preferred_value: The preferred value. Must be greater than or equal to -1. If set to -1, it means the value is "unlimited". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#preferred_value GoogleCloudQuotasQuotaPreference#preferred_value}
        :param annotations: The annotations map for clients to store small amounts of arbitrary data. Do not put PII or other sensitive information here. See https://google.aip.dev/128#annotations. An object containing a list of "key: value" pairs. Example: '{ "name": "wrench", "mass": "1.3kg", "count": "3" }'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#annotations GoogleCloudQuotasQuotaPreference#annotations}
        '''
        value = GoogleCloudQuotasQuotaPreferenceQuotaConfig(
            preferred_value=preferred_value, annotations=annotations
        )

        return typing.cast(None, jsii.invoke(self, "putQuotaConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#create GoogleCloudQuotasQuotaPreference#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#delete GoogleCloudQuotasQuotaPreference#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#update GoogleCloudQuotasQuotaPreference#update}.
        '''
        value = GoogleCloudQuotasQuotaPreferenceTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetContactEmail")
    def reset_contact_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContactEmail", []))

    @jsii.member(jsii_name="resetDimensions")
    def reset_dimensions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDimensions", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIgnoreSafetyChecks")
    def reset_ignore_safety_checks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreSafetyChecks", []))

    @jsii.member(jsii_name="resetJustification")
    def reset_justification(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJustification", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetParent")
    def reset_parent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParent", []))

    @jsii.member(jsii_name="resetQuotaId")
    def reset_quota_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuotaId", []))

    @jsii.member(jsii_name="resetService")
    def reset_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetService", []))

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
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="quotaConfig")
    def quota_config(
        self,
    ) -> "GoogleCloudQuotasQuotaPreferenceQuotaConfigOutputReference":
        return typing.cast("GoogleCloudQuotasQuotaPreferenceQuotaConfigOutputReference", jsii.get(self, "quotaConfig"))

    @builtins.property
    @jsii.member(jsii_name="reconciling")
    def reconciling(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "reconciling"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleCloudQuotasQuotaPreferenceTimeoutsOutputReference":
        return typing.cast("GoogleCloudQuotasQuotaPreferenceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="contactEmailInput")
    def contact_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contactEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="dimensionsInput")
    def dimensions_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "dimensionsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreSafetyChecksInput")
    def ignore_safety_checks_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ignoreSafetyChecksInput"))

    @builtins.property
    @jsii.member(jsii_name="justificationInput")
    def justification_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "justificationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parentInput")
    def parent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentInput"))

    @builtins.property
    @jsii.member(jsii_name="quotaConfigInput")
    def quota_config_input(
        self,
    ) -> typing.Optional["GoogleCloudQuotasQuotaPreferenceQuotaConfig"]:
        return typing.cast(typing.Optional["GoogleCloudQuotasQuotaPreferenceQuotaConfig"], jsii.get(self, "quotaConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="quotaIdInput")
    def quota_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "quotaIdInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceInput")
    def service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleCloudQuotasQuotaPreferenceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleCloudQuotasQuotaPreferenceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="contactEmail")
    def contact_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contactEmail"))

    @contact_email.setter
    def contact_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc417e7a138dd6519048cf78295c4f1108b45960b8aca4dc46eeb5c636927066)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contactEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dimensions")
    def dimensions(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "dimensions"))

    @dimensions.setter
    def dimensions(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aedc0038163c07b1ad9b3627e6b5933f94bd91aa1e4f5308f4b14fbc1db2b887)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dimensions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4558770bde9a908a7d22a424fb5861de759cdaa7a2b34fdb807834dfcf9aee2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignoreSafetyChecks")
    def ignore_safety_checks(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ignoreSafetyChecks"))

    @ignore_safety_checks.setter
    def ignore_safety_checks(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58625e2a4b7c3887c18738c1d0492e92d5d4f2287425a848430181dac84f545d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreSafetyChecks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="justification")
    def justification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "justification"))

    @justification.setter
    def justification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff81c6113d2c5d546ba2f30420dd9f0c99c077cc1f36698169af1004c94f0ca0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "justification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51addd945ca15d1ffb04603ba5d2cbd180a2290791ef25720f54303b03d153d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @parent.setter
    def parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a8319ab02bc9124997ebd5cabb81a250e965db40855a6ca289bd87839ce4b4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="quotaId")
    def quota_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "quotaId"))

    @quota_id.setter
    def quota_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11686b39bd610e45c1ba076f5b2c94c293f0e6f3102d112e851333ddd108f612)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "quotaId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__532d38e90b5644b209ae9c30047c32fb7cecbc35a960aa98efbada25da3caef7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudQuotasQuotaPreference.GoogleCloudQuotasQuotaPreferenceConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "quota_config": "quotaConfig",
        "contact_email": "contactEmail",
        "dimensions": "dimensions",
        "id": "id",
        "ignore_safety_checks": "ignoreSafetyChecks",
        "justification": "justification",
        "name": "name",
        "parent": "parent",
        "quota_id": "quotaId",
        "service": "service",
        "timeouts": "timeouts",
    },
)
class GoogleCloudQuotasQuotaPreferenceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        quota_config: typing.Union["GoogleCloudQuotasQuotaPreferenceQuotaConfig", typing.Dict[builtins.str, typing.Any]],
        contact_email: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        ignore_safety_checks: typing.Optional[builtins.str] = None,
        justification: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        parent: typing.Optional[builtins.str] = None,
        quota_id: typing.Optional[builtins.str] = None,
        service: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleCloudQuotasQuotaPreferenceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param quota_config: quota_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#quota_config GoogleCloudQuotasQuotaPreference#quota_config}
        :param contact_email: An email address that can be used for quota related communication between the Google Cloud and the user in case the Google Cloud needs further information to make a decision on whether the user preferred quota can be granted. The Google account for the email address must have quota update permission for the project, folder or organization this quota preference is for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#contact_email GoogleCloudQuotasQuotaPreference#contact_email}
        :param dimensions: The dimensions that this quota preference applies to. The key of the map entry is the name of a dimension, such as "region", "zone", "network_id", and the value of the map entry is the dimension value. If a dimension is missing from the map of dimensions, the quota preference applies to all the dimension values except for those that have other quota preferences configured for the specific value. NOTE: QuotaPreferences can only be applied across all values of "user" and "resource" dimension. Do not set values for "user" or "resource" in the dimension map. Example: '{"provider": "Foo Inc"}' where "provider" is a service specific dimension. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#dimensions GoogleCloudQuotasQuotaPreference#dimensions}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#id GoogleCloudQuotasQuotaPreference#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ignore_safety_checks: The list of quota safety checks to be ignored. Default value: "QUOTA_SAFETY_CHECK_UNSPECIFIED" Possible values: ["QUOTA_SAFETY_CHECK_UNSPECIFIED", "QUOTA_DECREASE_BELOW_USAGE", "QUOTA_DECREASE_PERCENTAGE_TOO_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#ignore_safety_checks GoogleCloudQuotasQuotaPreference#ignore_safety_checks}
        :param justification: The reason / justification for this quota preference. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#justification GoogleCloudQuotasQuotaPreference#justification}
        :param name: The resource name of the quota preference. Required except in the CREATE requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#name GoogleCloudQuotasQuotaPreference#name}
        :param parent: The parent of the quota preference. Allowed parents are "projects/[project-id / number]" or "folders/[folder-id / number]" or "organizations/[org-id / number]". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#parent GoogleCloudQuotasQuotaPreference#parent}
        :param quota_id: The id of the quota to which the quota preference is applied. A quota id is unique in the service. Example: 'CPUS-per-project-region'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#quota_id GoogleCloudQuotasQuotaPreference#quota_id}
        :param service: The name of the service to which the quota preference is applied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#service GoogleCloudQuotasQuotaPreference#service}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#timeouts GoogleCloudQuotasQuotaPreference#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(quota_config, dict):
            quota_config = GoogleCloudQuotasQuotaPreferenceQuotaConfig(**quota_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleCloudQuotasQuotaPreferenceTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3c9664ca312118b6d6ecd2c755736b521954b02994a46b628f208ab5e03101c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument quota_config", value=quota_config, expected_type=type_hints["quota_config"])
            check_type(argname="argument contact_email", value=contact_email, expected_type=type_hints["contact_email"])
            check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ignore_safety_checks", value=ignore_safety_checks, expected_type=type_hints["ignore_safety_checks"])
            check_type(argname="argument justification", value=justification, expected_type=type_hints["justification"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument quota_id", value=quota_id, expected_type=type_hints["quota_id"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "quota_config": quota_config,
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
        if contact_email is not None:
            self._values["contact_email"] = contact_email
        if dimensions is not None:
            self._values["dimensions"] = dimensions
        if id is not None:
            self._values["id"] = id
        if ignore_safety_checks is not None:
            self._values["ignore_safety_checks"] = ignore_safety_checks
        if justification is not None:
            self._values["justification"] = justification
        if name is not None:
            self._values["name"] = name
        if parent is not None:
            self._values["parent"] = parent
        if quota_id is not None:
            self._values["quota_id"] = quota_id
        if service is not None:
            self._values["service"] = service
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
    def quota_config(self) -> "GoogleCloudQuotasQuotaPreferenceQuotaConfig":
        '''quota_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#quota_config GoogleCloudQuotasQuotaPreference#quota_config}
        '''
        result = self._values.get("quota_config")
        assert result is not None, "Required property 'quota_config' is missing"
        return typing.cast("GoogleCloudQuotasQuotaPreferenceQuotaConfig", result)

    @builtins.property
    def contact_email(self) -> typing.Optional[builtins.str]:
        '''An email address that can be used for quota related communication between the Google Cloud and the user in case the Google Cloud needs further information to make a decision on whether the user preferred quota can be granted.

        The Google account for the email address must have quota update permission for the project, folder or organization this quota preference is for.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#contact_email GoogleCloudQuotasQuotaPreference#contact_email}
        '''
        result = self._values.get("contact_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dimensions(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The dimensions that this quota preference applies to.

        The key of the map entry is the name of a dimension, such as "region", "zone", "network_id", and the value of the map entry is the dimension value. If a dimension is missing from the map of dimensions, the quota preference applies to all the dimension values except for those that have other quota preferences configured for the specific value.

        NOTE: QuotaPreferences can only be applied across all values of "user" and "resource" dimension. Do not set values for "user" or "resource" in the dimension map.

        Example: '{"provider": "Foo Inc"}' where "provider" is a service specific dimension.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#dimensions GoogleCloudQuotasQuotaPreference#dimensions}
        '''
        result = self._values.get("dimensions")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#id GoogleCloudQuotasQuotaPreference#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_safety_checks(self) -> typing.Optional[builtins.str]:
        '''The list of quota safety checks to be ignored. Default value: "QUOTA_SAFETY_CHECK_UNSPECIFIED" Possible values: ["QUOTA_SAFETY_CHECK_UNSPECIFIED", "QUOTA_DECREASE_BELOW_USAGE", "QUOTA_DECREASE_PERCENTAGE_TOO_HIGH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#ignore_safety_checks GoogleCloudQuotasQuotaPreference#ignore_safety_checks}
        '''
        result = self._values.get("ignore_safety_checks")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def justification(self) -> typing.Optional[builtins.str]:
        '''The reason / justification for this quota preference.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#justification GoogleCloudQuotasQuotaPreference#justification}
        '''
        result = self._values.get("justification")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The resource name of the quota preference. Required except in the CREATE requests.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#name GoogleCloudQuotasQuotaPreference#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parent(self) -> typing.Optional[builtins.str]:
        '''The parent of the quota preference.

        Allowed parents are "projects/[project-id / number]" or "folders/[folder-id / number]" or "organizations/[org-id / number]".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#parent GoogleCloudQuotasQuotaPreference#parent}
        '''
        result = self._values.get("parent")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def quota_id(self) -> typing.Optional[builtins.str]:
        '''The id of the quota to which the quota preference is applied.

        A quota id is unique in the service.
        Example: 'CPUS-per-project-region'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#quota_id GoogleCloudQuotasQuotaPreference#quota_id}
        '''
        result = self._values.get("quota_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service(self) -> typing.Optional[builtins.str]:
        '''The name of the service to which the quota preference is applied.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#service GoogleCloudQuotasQuotaPreference#service}
        '''
        result = self._values.get("service")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleCloudQuotasQuotaPreferenceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#timeouts GoogleCloudQuotasQuotaPreference#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleCloudQuotasQuotaPreferenceTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudQuotasQuotaPreferenceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudQuotasQuotaPreference.GoogleCloudQuotasQuotaPreferenceQuotaConfig",
    jsii_struct_bases=[],
    name_mapping={"preferred_value": "preferredValue", "annotations": "annotations"},
)
class GoogleCloudQuotasQuotaPreferenceQuotaConfig:
    def __init__(
        self,
        *,
        preferred_value: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param preferred_value: The preferred value. Must be greater than or equal to -1. If set to -1, it means the value is "unlimited". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#preferred_value GoogleCloudQuotasQuotaPreference#preferred_value}
        :param annotations: The annotations map for clients to store small amounts of arbitrary data. Do not put PII or other sensitive information here. See https://google.aip.dev/128#annotations. An object containing a list of "key: value" pairs. Example: '{ "name": "wrench", "mass": "1.3kg", "count": "3" }'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#annotations GoogleCloudQuotasQuotaPreference#annotations}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce4c316216fba9e721e23807f8db205fa41f32189cab3423ba39a8b44bcc365c)
            check_type(argname="argument preferred_value", value=preferred_value, expected_type=type_hints["preferred_value"])
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "preferred_value": preferred_value,
        }
        if annotations is not None:
            self._values["annotations"] = annotations

    @builtins.property
    def preferred_value(self) -> builtins.str:
        '''The preferred value.

        Must be greater than or equal to -1. If set to -1, it means the value is "unlimited".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#preferred_value GoogleCloudQuotasQuotaPreference#preferred_value}
        '''
        result = self._values.get("preferred_value")
        assert result is not None, "Required property 'preferred_value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The annotations map for clients to store small amounts of arbitrary data.

        Do not put PII or other sensitive information here. See https://google.aip.dev/128#annotations.

        An object containing a list of "key: value" pairs. Example: '{ "name": "wrench", "mass": "1.3kg", "count": "3" }'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#annotations GoogleCloudQuotasQuotaPreference#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudQuotasQuotaPreferenceQuotaConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudQuotasQuotaPreferenceQuotaConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudQuotasQuotaPreference.GoogleCloudQuotasQuotaPreferenceQuotaConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2557fab11b0b2b13dbc78e8a48d94e1c5dca45605111d530fe6ef93a95f099d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @builtins.property
    @jsii.member(jsii_name="grantedValue")
    def granted_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "grantedValue"))

    @builtins.property
    @jsii.member(jsii_name="requestOrigin")
    def request_origin(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestOrigin"))

    @builtins.property
    @jsii.member(jsii_name="stateDetail")
    def state_detail(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stateDetail"))

    @builtins.property
    @jsii.member(jsii_name="traceId")
    def trace_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "traceId"))

    @builtins.property
    @jsii.member(jsii_name="annotationsInput")
    def annotations_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "annotationsInput"))

    @builtins.property
    @jsii.member(jsii_name="preferredValueInput")
    def preferred_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preferredValueInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fb102c24b7fa79e1990c880aac0a359969b8460a93e323d4359109e37c562e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preferredValue")
    def preferred_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preferredValue"))

    @preferred_value.setter
    def preferred_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e777c52b889ca970f4f34a30df31998088e12e820a856ff72910599edea9484b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferredValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudQuotasQuotaPreferenceQuotaConfig]:
        return typing.cast(typing.Optional[GoogleCloudQuotasQuotaPreferenceQuotaConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudQuotasQuotaPreferenceQuotaConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a764dabfad138d262640c831e7a2df26c57179d6070aaad98851c52f564cee5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudQuotasQuotaPreference.GoogleCloudQuotasQuotaPreferenceTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleCloudQuotasQuotaPreferenceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#create GoogleCloudQuotasQuotaPreference#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#delete GoogleCloudQuotasQuotaPreference#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#update GoogleCloudQuotasQuotaPreference#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1069fec51bd97c52c2b4df6eed15d06fbd15ea81df15f998e0521c8098c8537a)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#create GoogleCloudQuotasQuotaPreference#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#delete GoogleCloudQuotasQuotaPreference#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_quotas_quota_preference#update GoogleCloudQuotasQuotaPreference#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudQuotasQuotaPreferenceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudQuotasQuotaPreferenceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudQuotasQuotaPreference.GoogleCloudQuotasQuotaPreferenceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6fd236aa793d78c9d5168398bb799e31a5f20e48c6c3f6af9a970a8ed23904cb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb9461eda2cef203f10abe967a4b2324196630253c2f792289e4b0aa65f90e97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d3a5015134e3c449f14bc95ce2ca2a6a24c0b71dc06bfeff7c2ed674e55fe74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7339cf326edeebff92d4f9e59328047cd1051ff41d7351d6979257a16deef41e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudQuotasQuotaPreferenceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudQuotasQuotaPreferenceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudQuotasQuotaPreferenceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__286952d37986040e586b89733529a80b2172181f6aa02ee7dcdcacd7e732dfd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleCloudQuotasQuotaPreference",
    "GoogleCloudQuotasQuotaPreferenceConfig",
    "GoogleCloudQuotasQuotaPreferenceQuotaConfig",
    "GoogleCloudQuotasQuotaPreferenceQuotaConfigOutputReference",
    "GoogleCloudQuotasQuotaPreferenceTimeouts",
    "GoogleCloudQuotasQuotaPreferenceTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__c391be8bfbcc777d3a7eeed1515218fb716b8451f9c6055aa6fc0a4f04df814c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    quota_config: typing.Union[GoogleCloudQuotasQuotaPreferenceQuotaConfig, typing.Dict[builtins.str, typing.Any]],
    contact_email: typing.Optional[builtins.str] = None,
    dimensions: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    ignore_safety_checks: typing.Optional[builtins.str] = None,
    justification: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    parent: typing.Optional[builtins.str] = None,
    quota_id: typing.Optional[builtins.str] = None,
    service: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleCloudQuotasQuotaPreferenceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__afa5d7a4bf1612b959af69e88c72343107f5048d3d96aa85ea6c6bfab338f9b0(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc417e7a138dd6519048cf78295c4f1108b45960b8aca4dc46eeb5c636927066(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aedc0038163c07b1ad9b3627e6b5933f94bd91aa1e4f5308f4b14fbc1db2b887(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4558770bde9a908a7d22a424fb5861de759cdaa7a2b34fdb807834dfcf9aee2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58625e2a4b7c3887c18738c1d0492e92d5d4f2287425a848430181dac84f545d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff81c6113d2c5d546ba2f30420dd9f0c99c077cc1f36698169af1004c94f0ca0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51addd945ca15d1ffb04603ba5d2cbd180a2290791ef25720f54303b03d153d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a8319ab02bc9124997ebd5cabb81a250e965db40855a6ca289bd87839ce4b4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11686b39bd610e45c1ba076f5b2c94c293f0e6f3102d112e851333ddd108f612(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__532d38e90b5644b209ae9c30047c32fb7cecbc35a960aa98efbada25da3caef7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3c9664ca312118b6d6ecd2c755736b521954b02994a46b628f208ab5e03101c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    quota_config: typing.Union[GoogleCloudQuotasQuotaPreferenceQuotaConfig, typing.Dict[builtins.str, typing.Any]],
    contact_email: typing.Optional[builtins.str] = None,
    dimensions: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    ignore_safety_checks: typing.Optional[builtins.str] = None,
    justification: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    parent: typing.Optional[builtins.str] = None,
    quota_id: typing.Optional[builtins.str] = None,
    service: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleCloudQuotasQuotaPreferenceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce4c316216fba9e721e23807f8db205fa41f32189cab3423ba39a8b44bcc365c(
    *,
    preferred_value: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2557fab11b0b2b13dbc78e8a48d94e1c5dca45605111d530fe6ef93a95f099d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fb102c24b7fa79e1990c880aac0a359969b8460a93e323d4359109e37c562e9(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e777c52b889ca970f4f34a30df31998088e12e820a856ff72910599edea9484b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a764dabfad138d262640c831e7a2df26c57179d6070aaad98851c52f564cee5f(
    value: typing.Optional[GoogleCloudQuotasQuotaPreferenceQuotaConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1069fec51bd97c52c2b4df6eed15d06fbd15ea81df15f998e0521c8098c8537a(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fd236aa793d78c9d5168398bb799e31a5f20e48c6c3f6af9a970a8ed23904cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb9461eda2cef203f10abe967a4b2324196630253c2f792289e4b0aa65f90e97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d3a5015134e3c449f14bc95ce2ca2a6a24c0b71dc06bfeff7c2ed674e55fe74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7339cf326edeebff92d4f9e59328047cd1051ff41d7351d6979257a16deef41e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__286952d37986040e586b89733529a80b2172181f6aa02ee7dcdcacd7e732dfd2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudQuotasQuotaPreferenceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
