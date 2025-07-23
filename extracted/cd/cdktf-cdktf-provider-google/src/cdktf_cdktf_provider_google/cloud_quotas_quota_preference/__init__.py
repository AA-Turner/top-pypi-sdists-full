r'''
# `google_cloud_quotas_quota_preference`

Refer to the Terraform Registry for docs: [`google_cloud_quotas_quota_preference`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference).
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


class CloudQuotasQuotaPreference(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudQuotasQuotaPreference.CloudQuotasQuotaPreference",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference google_cloud_quotas_quota_preference}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        quota_config: typing.Union["CloudQuotasQuotaPreferenceQuotaConfig", typing.Dict[builtins.str, typing.Any]],
        contact_email: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        ignore_safety_checks: typing.Optional[builtins.str] = None,
        justification: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        parent: typing.Optional[builtins.str] = None,
        quota_id: typing.Optional[builtins.str] = None,
        service: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["CloudQuotasQuotaPreferenceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference google_cloud_quotas_quota_preference} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param quota_config: quota_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#quota_config CloudQuotasQuotaPreference#quota_config}
        :param contact_email: An email address that can be used for quota related communication between the Google Cloud and the user in case the Google Cloud needs further information to make a decision on whether the user preferred quota can be granted. The Google account for the email address must have quota update permission for the project, folder or organization this quota preference is for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#contact_email CloudQuotasQuotaPreference#contact_email}
        :param dimensions: The dimensions that this quota preference applies to. The key of the map entry is the name of a dimension, such as "region", "zone", "network_id", and the value of the map entry is the dimension value. If a dimension is missing from the map of dimensions, the quota preference applies to all the dimension values except for those that have other quota preferences configured for the specific value. NOTE: QuotaPreferences can only be applied across all values of "user" and "resource" dimension. Do not set values for "user" or "resource" in the dimension map. Example: '{"provider": "Foo Inc"}' where "provider" is a service specific dimension. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#dimensions CloudQuotasQuotaPreference#dimensions}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#id CloudQuotasQuotaPreference#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ignore_safety_checks: The list of quota safety checks to be ignored. Default value: "QUOTA_SAFETY_CHECK_UNSPECIFIED" Possible values: ["QUOTA_SAFETY_CHECK_UNSPECIFIED", "QUOTA_DECREASE_BELOW_USAGE", "QUOTA_DECREASE_PERCENTAGE_TOO_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#ignore_safety_checks CloudQuotasQuotaPreference#ignore_safety_checks}
        :param justification: The reason / justification for this quota preference. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#justification CloudQuotasQuotaPreference#justification}
        :param name: The resource name of the quota preference. Required except in the CREATE requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#name CloudQuotasQuotaPreference#name}
        :param parent: The parent of the quota preference. Allowed parents are "projects/[project-id / number]" or "folders/[folder-id / number]" or "organizations/[org-id / number]". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#parent CloudQuotasQuotaPreference#parent}
        :param quota_id: The id of the quota to which the quota preference is applied. A quota id is unique in the service. Example: 'CPUS-per-project-region'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#quota_id CloudQuotasQuotaPreference#quota_id}
        :param service: The name of the service to which the quota preference is applied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#service CloudQuotasQuotaPreference#service}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#timeouts CloudQuotasQuotaPreference#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9571566c3b1677d89beec7f647b2523bc6e7843adb0d39a0bd29d7e3ee08c86f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CloudQuotasQuotaPreferenceConfig(
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
        '''Generates CDKTF code for importing a CloudQuotasQuotaPreference resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CloudQuotasQuotaPreference to import.
        :param import_from_id: The id of the existing CloudQuotasQuotaPreference that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CloudQuotasQuotaPreference to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7461de16f2383d3bfb48641d3a710d1c9601e18e0f2e65090f5b3b5d1565f79c)
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
        :param preferred_value: The preferred value. Must be greater than or equal to -1. If set to -1, it means the value is "unlimited". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#preferred_value CloudQuotasQuotaPreference#preferred_value}
        :param annotations: The annotations map for clients to store small amounts of arbitrary data. Do not put PII or other sensitive information here. See https://google.aip.dev/128#annotations. An object containing a list of "key: value" pairs. Example: '{ "name": "wrench", "mass": "1.3kg", "count": "3" }'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#annotations CloudQuotasQuotaPreference#annotations}
        '''
        value = CloudQuotasQuotaPreferenceQuotaConfig(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#create CloudQuotasQuotaPreference#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#delete CloudQuotasQuotaPreference#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#update CloudQuotasQuotaPreference#update}.
        '''
        value = CloudQuotasQuotaPreferenceTimeouts(
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
    def quota_config(self) -> "CloudQuotasQuotaPreferenceQuotaConfigOutputReference":
        return typing.cast("CloudQuotasQuotaPreferenceQuotaConfigOutputReference", jsii.get(self, "quotaConfig"))

    @builtins.property
    @jsii.member(jsii_name="reconciling")
    def reconciling(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "reconciling"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "CloudQuotasQuotaPreferenceTimeoutsOutputReference":
        return typing.cast("CloudQuotasQuotaPreferenceTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["CloudQuotasQuotaPreferenceQuotaConfig"]:
        return typing.cast(typing.Optional["CloudQuotasQuotaPreferenceQuotaConfig"], jsii.get(self, "quotaConfigInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CloudQuotasQuotaPreferenceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CloudQuotasQuotaPreferenceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="contactEmail")
    def contact_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contactEmail"))

    @contact_email.setter
    def contact_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9c158058da236bc053580fca598b9a7aa7e288bc1c275787124d98e38c63dd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contactEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dimensions")
    def dimensions(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "dimensions"))

    @dimensions.setter
    def dimensions(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2eb4022ca98534f0a341428c53bacc5c8ae43ceb2ad44115ce5a17fe7fefe16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dimensions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32fa49b43cd12c01db50f99c2c89602f7e86bfeaa1f25177bed5a973cf7834a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignoreSafetyChecks")
    def ignore_safety_checks(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ignoreSafetyChecks"))

    @ignore_safety_checks.setter
    def ignore_safety_checks(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__689d99a45ba1e1b265cea46015d1e8532617ce468fd0d794e301ea7c465e6c8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreSafetyChecks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="justification")
    def justification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "justification"))

    @justification.setter
    def justification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e018e829d3712253247a4a5889209f0ffd5ebe278119cf25d6ad551f77ea31d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "justification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9725bd3bdd05820923441a85278d8b5c58d6148937734e5688306bef2b92ce47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @parent.setter
    def parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__091a8d8a245b3e4bd0d9b765d219f1eb75717c3486d59c6c094f6e49b7dba470)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="quotaId")
    def quota_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "quotaId"))

    @quota_id.setter
    def quota_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__925a50c839a14feee85547437edfb04b5894f2c79f9126bfc6c55b577873a05b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "quotaId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc2919c815d9b66bf2291236c763bdeef584034366fa0517122806a1fe4a8a02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudQuotasQuotaPreference.CloudQuotasQuotaPreferenceConfig",
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
class CloudQuotasQuotaPreferenceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        quota_config: typing.Union["CloudQuotasQuotaPreferenceQuotaConfig", typing.Dict[builtins.str, typing.Any]],
        contact_email: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        ignore_safety_checks: typing.Optional[builtins.str] = None,
        justification: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        parent: typing.Optional[builtins.str] = None,
        quota_id: typing.Optional[builtins.str] = None,
        service: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["CloudQuotasQuotaPreferenceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param quota_config: quota_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#quota_config CloudQuotasQuotaPreference#quota_config}
        :param contact_email: An email address that can be used for quota related communication between the Google Cloud and the user in case the Google Cloud needs further information to make a decision on whether the user preferred quota can be granted. The Google account for the email address must have quota update permission for the project, folder or organization this quota preference is for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#contact_email CloudQuotasQuotaPreference#contact_email}
        :param dimensions: The dimensions that this quota preference applies to. The key of the map entry is the name of a dimension, such as "region", "zone", "network_id", and the value of the map entry is the dimension value. If a dimension is missing from the map of dimensions, the quota preference applies to all the dimension values except for those that have other quota preferences configured for the specific value. NOTE: QuotaPreferences can only be applied across all values of "user" and "resource" dimension. Do not set values for "user" or "resource" in the dimension map. Example: '{"provider": "Foo Inc"}' where "provider" is a service specific dimension. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#dimensions CloudQuotasQuotaPreference#dimensions}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#id CloudQuotasQuotaPreference#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ignore_safety_checks: The list of quota safety checks to be ignored. Default value: "QUOTA_SAFETY_CHECK_UNSPECIFIED" Possible values: ["QUOTA_SAFETY_CHECK_UNSPECIFIED", "QUOTA_DECREASE_BELOW_USAGE", "QUOTA_DECREASE_PERCENTAGE_TOO_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#ignore_safety_checks CloudQuotasQuotaPreference#ignore_safety_checks}
        :param justification: The reason / justification for this quota preference. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#justification CloudQuotasQuotaPreference#justification}
        :param name: The resource name of the quota preference. Required except in the CREATE requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#name CloudQuotasQuotaPreference#name}
        :param parent: The parent of the quota preference. Allowed parents are "projects/[project-id / number]" or "folders/[folder-id / number]" or "organizations/[org-id / number]". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#parent CloudQuotasQuotaPreference#parent}
        :param quota_id: The id of the quota to which the quota preference is applied. A quota id is unique in the service. Example: 'CPUS-per-project-region'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#quota_id CloudQuotasQuotaPreference#quota_id}
        :param service: The name of the service to which the quota preference is applied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#service CloudQuotasQuotaPreference#service}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#timeouts CloudQuotasQuotaPreference#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(quota_config, dict):
            quota_config = CloudQuotasQuotaPreferenceQuotaConfig(**quota_config)
        if isinstance(timeouts, dict):
            timeouts = CloudQuotasQuotaPreferenceTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d9328a582c734d45521a4d521cbed5f15f385f90d9959fd46243985341e6dc5)
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
    def quota_config(self) -> "CloudQuotasQuotaPreferenceQuotaConfig":
        '''quota_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#quota_config CloudQuotasQuotaPreference#quota_config}
        '''
        result = self._values.get("quota_config")
        assert result is not None, "Required property 'quota_config' is missing"
        return typing.cast("CloudQuotasQuotaPreferenceQuotaConfig", result)

    @builtins.property
    def contact_email(self) -> typing.Optional[builtins.str]:
        '''An email address that can be used for quota related communication between the Google Cloud and the user in case the Google Cloud needs further information to make a decision on whether the user preferred quota can be granted.

        The Google account for the email address must have quota update permission for the project, folder or organization this quota preference is for.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#contact_email CloudQuotasQuotaPreference#contact_email}
        '''
        result = self._values.get("contact_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dimensions(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The dimensions that this quota preference applies to.

        The key of the map entry is the name of a dimension, such as "region", "zone", "network_id", and the value of the map entry is the dimension value. If a dimension is missing from the map of dimensions, the quota preference applies to all the dimension values except for those that have other quota preferences configured for the specific value.

        NOTE: QuotaPreferences can only be applied across all values of "user" and "resource" dimension. Do not set values for "user" or "resource" in the dimension map.

        Example: '{"provider": "Foo Inc"}' where "provider" is a service specific dimension.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#dimensions CloudQuotasQuotaPreference#dimensions}
        '''
        result = self._values.get("dimensions")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#id CloudQuotasQuotaPreference#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_safety_checks(self) -> typing.Optional[builtins.str]:
        '''The list of quota safety checks to be ignored. Default value: "QUOTA_SAFETY_CHECK_UNSPECIFIED" Possible values: ["QUOTA_SAFETY_CHECK_UNSPECIFIED", "QUOTA_DECREASE_BELOW_USAGE", "QUOTA_DECREASE_PERCENTAGE_TOO_HIGH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#ignore_safety_checks CloudQuotasQuotaPreference#ignore_safety_checks}
        '''
        result = self._values.get("ignore_safety_checks")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def justification(self) -> typing.Optional[builtins.str]:
        '''The reason / justification for this quota preference.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#justification CloudQuotasQuotaPreference#justification}
        '''
        result = self._values.get("justification")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The resource name of the quota preference. Required except in the CREATE requests.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#name CloudQuotasQuotaPreference#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parent(self) -> typing.Optional[builtins.str]:
        '''The parent of the quota preference.

        Allowed parents are "projects/[project-id / number]" or "folders/[folder-id / number]" or "organizations/[org-id / number]".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#parent CloudQuotasQuotaPreference#parent}
        '''
        result = self._values.get("parent")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def quota_id(self) -> typing.Optional[builtins.str]:
        '''The id of the quota to which the quota preference is applied.

        A quota id is unique in the service.
        Example: 'CPUS-per-project-region'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#quota_id CloudQuotasQuotaPreference#quota_id}
        '''
        result = self._values.get("quota_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service(self) -> typing.Optional[builtins.str]:
        '''The name of the service to which the quota preference is applied.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#service CloudQuotasQuotaPreference#service}
        '''
        result = self._values.get("service")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CloudQuotasQuotaPreferenceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#timeouts CloudQuotasQuotaPreference#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CloudQuotasQuotaPreferenceTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudQuotasQuotaPreferenceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudQuotasQuotaPreference.CloudQuotasQuotaPreferenceQuotaConfig",
    jsii_struct_bases=[],
    name_mapping={"preferred_value": "preferredValue", "annotations": "annotations"},
)
class CloudQuotasQuotaPreferenceQuotaConfig:
    def __init__(
        self,
        *,
        preferred_value: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param preferred_value: The preferred value. Must be greater than or equal to -1. If set to -1, it means the value is "unlimited". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#preferred_value CloudQuotasQuotaPreference#preferred_value}
        :param annotations: The annotations map for clients to store small amounts of arbitrary data. Do not put PII or other sensitive information here. See https://google.aip.dev/128#annotations. An object containing a list of "key: value" pairs. Example: '{ "name": "wrench", "mass": "1.3kg", "count": "3" }'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#annotations CloudQuotasQuotaPreference#annotations}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f8ce101a3f6fa42862652ab50fd1b19773d76fb177acd148f4c7f91797e370a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#preferred_value CloudQuotasQuotaPreference#preferred_value}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#annotations CloudQuotasQuotaPreference#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudQuotasQuotaPreferenceQuotaConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudQuotasQuotaPreferenceQuotaConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudQuotasQuotaPreference.CloudQuotasQuotaPreferenceQuotaConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3dc76da43a9a1122c049dff49555d0f27374db4bda4bc346ba43e5c6f47e974f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a54832f02a34da175ecdb8b0253913c7dc24421fce4edbd4ae30c3c5caaf8227)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preferredValue")
    def preferred_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preferredValue"))

    @preferred_value.setter
    def preferred_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17bf189b2ecfd192ec29df504136fbfff15814c2aa4dc6087a9b8d195aafe399)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferredValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudQuotasQuotaPreferenceQuotaConfig]:
        return typing.cast(typing.Optional[CloudQuotasQuotaPreferenceQuotaConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudQuotasQuotaPreferenceQuotaConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20078a26fda2753d77b52177c408ca50b6a3424af177d06877021df6682ad1d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudQuotasQuotaPreference.CloudQuotasQuotaPreferenceTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class CloudQuotasQuotaPreferenceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#create CloudQuotasQuotaPreference#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#delete CloudQuotasQuotaPreference#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#update CloudQuotasQuotaPreference#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fe0d4868863f5078a4ebb43c2b688a414a0ef0e8bfb565972b3bbfde56dfd74)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#create CloudQuotasQuotaPreference#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#delete CloudQuotasQuotaPreference#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_quotas_quota_preference#update CloudQuotasQuotaPreference#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudQuotasQuotaPreferenceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudQuotasQuotaPreferenceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudQuotasQuotaPreference.CloudQuotasQuotaPreferenceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d91ecbb842e27a9f40eabaabcf13c5420a51e83ac6085cf6fa1d39a14079937a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c863c64904f4e798aec7f4ab8c50fe313c8d6b3f654c69d1798c02ee35232bb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__089ff23842495579ae1a195cbd2c9ab911bcce5dc5fdbb226aafc36acbe44ea2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f1918960bf18f55ff0d1edeac39bc4a1f3d8f4f67a57e3913e2358972d67786)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudQuotasQuotaPreferenceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudQuotasQuotaPreferenceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudQuotasQuotaPreferenceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00101fc905a1db4ea9bd92a3a46384ade2c1ef90fe4ef7b64eac26d1186f01a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CloudQuotasQuotaPreference",
    "CloudQuotasQuotaPreferenceConfig",
    "CloudQuotasQuotaPreferenceQuotaConfig",
    "CloudQuotasQuotaPreferenceQuotaConfigOutputReference",
    "CloudQuotasQuotaPreferenceTimeouts",
    "CloudQuotasQuotaPreferenceTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__9571566c3b1677d89beec7f647b2523bc6e7843adb0d39a0bd29d7e3ee08c86f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    quota_config: typing.Union[CloudQuotasQuotaPreferenceQuotaConfig, typing.Dict[builtins.str, typing.Any]],
    contact_email: typing.Optional[builtins.str] = None,
    dimensions: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    ignore_safety_checks: typing.Optional[builtins.str] = None,
    justification: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    parent: typing.Optional[builtins.str] = None,
    quota_id: typing.Optional[builtins.str] = None,
    service: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[CloudQuotasQuotaPreferenceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__7461de16f2383d3bfb48641d3a710d1c9601e18e0f2e65090f5b3b5d1565f79c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9c158058da236bc053580fca598b9a7aa7e288bc1c275787124d98e38c63dd3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2eb4022ca98534f0a341428c53bacc5c8ae43ceb2ad44115ce5a17fe7fefe16(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32fa49b43cd12c01db50f99c2c89602f7e86bfeaa1f25177bed5a973cf7834a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__689d99a45ba1e1b265cea46015d1e8532617ce468fd0d794e301ea7c465e6c8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e018e829d3712253247a4a5889209f0ffd5ebe278119cf25d6ad551f77ea31d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9725bd3bdd05820923441a85278d8b5c58d6148937734e5688306bef2b92ce47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__091a8d8a245b3e4bd0d9b765d219f1eb75717c3486d59c6c094f6e49b7dba470(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__925a50c839a14feee85547437edfb04b5894f2c79f9126bfc6c55b577873a05b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc2919c815d9b66bf2291236c763bdeef584034366fa0517122806a1fe4a8a02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d9328a582c734d45521a4d521cbed5f15f385f90d9959fd46243985341e6dc5(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    quota_config: typing.Union[CloudQuotasQuotaPreferenceQuotaConfig, typing.Dict[builtins.str, typing.Any]],
    contact_email: typing.Optional[builtins.str] = None,
    dimensions: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    ignore_safety_checks: typing.Optional[builtins.str] = None,
    justification: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    parent: typing.Optional[builtins.str] = None,
    quota_id: typing.Optional[builtins.str] = None,
    service: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[CloudQuotasQuotaPreferenceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f8ce101a3f6fa42862652ab50fd1b19773d76fb177acd148f4c7f91797e370a(
    *,
    preferred_value: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dc76da43a9a1122c049dff49555d0f27374db4bda4bc346ba43e5c6f47e974f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a54832f02a34da175ecdb8b0253913c7dc24421fce4edbd4ae30c3c5caaf8227(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17bf189b2ecfd192ec29df504136fbfff15814c2aa4dc6087a9b8d195aafe399(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20078a26fda2753d77b52177c408ca50b6a3424af177d06877021df6682ad1d3(
    value: typing.Optional[CloudQuotasQuotaPreferenceQuotaConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fe0d4868863f5078a4ebb43c2b688a414a0ef0e8bfb565972b3bbfde56dfd74(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d91ecbb842e27a9f40eabaabcf13c5420a51e83ac6085cf6fa1d39a14079937a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c863c64904f4e798aec7f4ab8c50fe313c8d6b3f654c69d1798c02ee35232bb6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__089ff23842495579ae1a195cbd2c9ab911bcce5dc5fdbb226aafc36acbe44ea2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f1918960bf18f55ff0d1edeac39bc4a1f3d8f4f67a57e3913e2358972d67786(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00101fc905a1db4ea9bd92a3a46384ade2c1ef90fe4ef7b64eac26d1186f01a7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudQuotasQuotaPreferenceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
