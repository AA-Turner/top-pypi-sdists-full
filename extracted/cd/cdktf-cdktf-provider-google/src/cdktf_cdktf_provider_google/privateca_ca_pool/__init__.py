r'''
# `google_privateca_ca_pool`

Refer to the Terraform Registry for docs: [`google_privateca_ca_pool`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool).
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


class PrivatecaCaPool(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCaPool.PrivatecaCaPool",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool google_privateca_ca_pool}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        tier: builtins.str,
        id: typing.Optional[builtins.str] = None,
        issuance_policy: typing.Optional[typing.Union["PrivatecaCaPoolIssuancePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        publishing_options: typing.Optional[typing.Union["PrivatecaCaPoolPublishingOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["PrivatecaCaPoolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool google_privateca_ca_pool} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Location of the CaPool. A full list of valid locations can be found by running 'gcloud privateca locations list'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#location PrivatecaCaPool#location}
        :param name: The name for this CaPool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#name PrivatecaCaPool#name}
        :param tier: The Tier of this CaPool. Possible values: ["ENTERPRISE", "DEVOPS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#tier PrivatecaCaPool#tier}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#id PrivatecaCaPool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param issuance_policy: issuance_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#issuance_policy PrivatecaCaPool#issuance_policy}
        :param labels: Labels with user-defined metadata. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#labels PrivatecaCaPool#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#project PrivatecaCaPool#project}.
        :param publishing_options: publishing_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#publishing_options PrivatecaCaPool#publishing_options}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#timeouts PrivatecaCaPool#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db6ffc6ad50722486da237cc9e4761430dcac0ac3e3cc538706105caa0c5274b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = PrivatecaCaPoolConfig(
            location=location,
            name=name,
            tier=tier,
            id=id,
            issuance_policy=issuance_policy,
            labels=labels,
            project=project,
            publishing_options=publishing_options,
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
        '''Generates CDKTF code for importing a PrivatecaCaPool resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the PrivatecaCaPool to import.
        :param import_from_id: The id of the existing PrivatecaCaPool that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the PrivatecaCaPool to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc353b9de9771a9f7af3468b59164cdcf85da0ca3b64b155c4bb375ba7f78615)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putIssuancePolicy")
    def put_issuance_policy(
        self,
        *,
        allowed_issuance_modes: typing.Optional[typing.Union["PrivatecaCaPoolIssuancePolicyAllowedIssuanceModes", typing.Dict[builtins.str, typing.Any]]] = None,
        allowed_key_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PrivatecaCaPoolIssuancePolicyAllowedKeyTypes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        backdate_duration: typing.Optional[builtins.str] = None,
        baseline_values: typing.Optional[typing.Union["PrivatecaCaPoolIssuancePolicyBaselineValues", typing.Dict[builtins.str, typing.Any]]] = None,
        identity_constraints: typing.Optional[typing.Union["PrivatecaCaPoolIssuancePolicyIdentityConstraints", typing.Dict[builtins.str, typing.Any]]] = None,
        maximum_lifetime: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allowed_issuance_modes: allowed_issuance_modes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#allowed_issuance_modes PrivatecaCaPool#allowed_issuance_modes}
        :param allowed_key_types: allowed_key_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#allowed_key_types PrivatecaCaPool#allowed_key_types}
        :param backdate_duration: The duration to backdate all certificates issued from this CaPool. If not set, the certificates will be issued with a not_before_time of the issuance time (i.e. the current time). If set, the certificates will be issued with a not_before_time of the issuance time minus the backdate_duration. The not_after_time will be adjusted to preserve the requested lifetime. The backdate_duration must be less than or equal to 48 hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#backdate_duration PrivatecaCaPool#backdate_duration}
        :param baseline_values: baseline_values block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#baseline_values PrivatecaCaPool#baseline_values}
        :param identity_constraints: identity_constraints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#identity_constraints PrivatecaCaPool#identity_constraints}
        :param maximum_lifetime: The maximum lifetime allowed for issued Certificates. Note that if the issuing CertificateAuthority expires before a Certificate's requested maximumLifetime, the effective lifetime will be explicitly truncated to match it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#maximum_lifetime PrivatecaCaPool#maximum_lifetime}
        '''
        value = PrivatecaCaPoolIssuancePolicy(
            allowed_issuance_modes=allowed_issuance_modes,
            allowed_key_types=allowed_key_types,
            backdate_duration=backdate_duration,
            baseline_values=baseline_values,
            identity_constraints=identity_constraints,
            maximum_lifetime=maximum_lifetime,
        )

        return typing.cast(None, jsii.invoke(self, "putIssuancePolicy", [value]))

    @jsii.member(jsii_name="putPublishingOptions")
    def put_publishing_options(
        self,
        *,
        publish_ca_cert: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        publish_crl: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        encoding_format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param publish_ca_cert: When true, publishes each CertificateAuthority's CA certificate and includes its URL in the "Authority Information Access" X.509 extension in all issued Certificates. If this is false, the CA certificate will not be published and the corresponding X.509 extension will not be written in issued certificates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#publish_ca_cert PrivatecaCaPool#publish_ca_cert}
        :param publish_crl: When true, publishes each CertificateAuthority's CRL and includes its URL in the "CRL Distribution Points" X.509 extension in all issued Certificates. If this is false, CRLs will not be published and the corresponding X.509 extension will not be written in issued certificates. CRLs will expire 7 days from their creation. However, we will rebuild daily. CRLs are also rebuilt shortly after a certificate is revoked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#publish_crl PrivatecaCaPool#publish_crl}
        :param encoding_format: Specifies the encoding format of each CertificateAuthority's CA certificate and CRLs. If this is omitted, CA certificates and CRLs will be published in PEM. Possible values: ["PEM", "DER"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#encoding_format PrivatecaCaPool#encoding_format}
        '''
        value = PrivatecaCaPoolPublishingOptions(
            publish_ca_cert=publish_ca_cert,
            publish_crl=publish_crl,
            encoding_format=encoding_format,
        )

        return typing.cast(None, jsii.invoke(self, "putPublishingOptions", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#create PrivatecaCaPool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#delete PrivatecaCaPool#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#update PrivatecaCaPool#update}.
        '''
        value = PrivatecaCaPoolTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIssuancePolicy")
    def reset_issuance_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIssuancePolicy", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetPublishingOptions")
    def reset_publishing_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublishingOptions", []))

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
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="issuancePolicy")
    def issuance_policy(self) -> "PrivatecaCaPoolIssuancePolicyOutputReference":
        return typing.cast("PrivatecaCaPoolIssuancePolicyOutputReference", jsii.get(self, "issuancePolicy"))

    @builtins.property
    @jsii.member(jsii_name="publishingOptions")
    def publishing_options(self) -> "PrivatecaCaPoolPublishingOptionsOutputReference":
        return typing.cast("PrivatecaCaPoolPublishingOptionsOutputReference", jsii.get(self, "publishingOptions"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "PrivatecaCaPoolTimeoutsOutputReference":
        return typing.cast("PrivatecaCaPoolTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="issuancePolicyInput")
    def issuance_policy_input(self) -> typing.Optional["PrivatecaCaPoolIssuancePolicy"]:
        return typing.cast(typing.Optional["PrivatecaCaPoolIssuancePolicy"], jsii.get(self, "issuancePolicyInput"))

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
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="publishingOptionsInput")
    def publishing_options_input(
        self,
    ) -> typing.Optional["PrivatecaCaPoolPublishingOptions"]:
        return typing.cast(typing.Optional["PrivatecaCaPoolPublishingOptions"], jsii.get(self, "publishingOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="tierInput")
    def tier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tierInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "PrivatecaCaPoolTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "PrivatecaCaPoolTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c615f86e46c45d946a6303ef13ac36ca7b2a96a8e164465a803cae634c177bc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96897488896425286df1853bdbff779e00b36a403025242f80cd8fd1f4a4c2e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__864451c5c6c455f9a9f81829dcad94177b3a22222483e34724feb430ccb49906)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__361ca9f123742dd7166d21f4cb83f470da453dcaabdb469b92777a6485229798)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03995b1fa3115893e2da34fc277f67f50eb0a0feff6fee2931c89f011e728e6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tier")
    def tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tier"))

    @tier.setter
    def tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__448a7d0d52ef406864fd8adab391aa68719ea1772943cc126331fe7013f76a9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tier", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCaPool.PrivatecaCaPoolConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "name": "name",
        "tier": "tier",
        "id": "id",
        "issuance_policy": "issuancePolicy",
        "labels": "labels",
        "project": "project",
        "publishing_options": "publishingOptions",
        "timeouts": "timeouts",
    },
)
class PrivatecaCaPoolConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        location: builtins.str,
        name: builtins.str,
        tier: builtins.str,
        id: typing.Optional[builtins.str] = None,
        issuance_policy: typing.Optional[typing.Union["PrivatecaCaPoolIssuancePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        publishing_options: typing.Optional[typing.Union["PrivatecaCaPoolPublishingOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["PrivatecaCaPoolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Location of the CaPool. A full list of valid locations can be found by running 'gcloud privateca locations list'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#location PrivatecaCaPool#location}
        :param name: The name for this CaPool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#name PrivatecaCaPool#name}
        :param tier: The Tier of this CaPool. Possible values: ["ENTERPRISE", "DEVOPS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#tier PrivatecaCaPool#tier}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#id PrivatecaCaPool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param issuance_policy: issuance_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#issuance_policy PrivatecaCaPool#issuance_policy}
        :param labels: Labels with user-defined metadata. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#labels PrivatecaCaPool#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#project PrivatecaCaPool#project}.
        :param publishing_options: publishing_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#publishing_options PrivatecaCaPool#publishing_options}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#timeouts PrivatecaCaPool#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(issuance_policy, dict):
            issuance_policy = PrivatecaCaPoolIssuancePolicy(**issuance_policy)
        if isinstance(publishing_options, dict):
            publishing_options = PrivatecaCaPoolPublishingOptions(**publishing_options)
        if isinstance(timeouts, dict):
            timeouts = PrivatecaCaPoolTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6797ca494db177a4f78345de9d686c0c9409ea1366b21bbe4898d21251d37578)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tier", value=tier, expected_type=type_hints["tier"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument issuance_policy", value=issuance_policy, expected_type=type_hints["issuance_policy"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument publishing_options", value=publishing_options, expected_type=type_hints["publishing_options"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "name": name,
            "tier": tier,
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
        if id is not None:
            self._values["id"] = id
        if issuance_policy is not None:
            self._values["issuance_policy"] = issuance_policy
        if labels is not None:
            self._values["labels"] = labels
        if project is not None:
            self._values["project"] = project
        if publishing_options is not None:
            self._values["publishing_options"] = publishing_options
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
    def location(self) -> builtins.str:
        '''Location of the CaPool. A full list of valid locations can be found by running 'gcloud privateca locations list'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#location PrivatecaCaPool#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name for this CaPool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#name PrivatecaCaPool#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tier(self) -> builtins.str:
        '''The Tier of this CaPool. Possible values: ["ENTERPRISE", "DEVOPS"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#tier PrivatecaCaPool#tier}
        '''
        result = self._values.get("tier")
        assert result is not None, "Required property 'tier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#id PrivatecaCaPool#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def issuance_policy(self) -> typing.Optional["PrivatecaCaPoolIssuancePolicy"]:
        '''issuance_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#issuance_policy PrivatecaCaPool#issuance_policy}
        '''
        result = self._values.get("issuance_policy")
        return typing.cast(typing.Optional["PrivatecaCaPoolIssuancePolicy"], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels with user-defined metadata.

        An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass":
        "1.3kg", "count": "3" }.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#labels PrivatecaCaPool#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#project PrivatecaCaPool#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publishing_options(self) -> typing.Optional["PrivatecaCaPoolPublishingOptions"]:
        '''publishing_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#publishing_options PrivatecaCaPool#publishing_options}
        '''
        result = self._values.get("publishing_options")
        return typing.cast(typing.Optional["PrivatecaCaPoolPublishingOptions"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["PrivatecaCaPoolTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#timeouts PrivatecaCaPool#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["PrivatecaCaPoolTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCaPoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCaPool.PrivatecaCaPoolIssuancePolicy",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_issuance_modes": "allowedIssuanceModes",
        "allowed_key_types": "allowedKeyTypes",
        "backdate_duration": "backdateDuration",
        "baseline_values": "baselineValues",
        "identity_constraints": "identityConstraints",
        "maximum_lifetime": "maximumLifetime",
    },
)
class PrivatecaCaPoolIssuancePolicy:
    def __init__(
        self,
        *,
        allowed_issuance_modes: typing.Optional[typing.Union["PrivatecaCaPoolIssuancePolicyAllowedIssuanceModes", typing.Dict[builtins.str, typing.Any]]] = None,
        allowed_key_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PrivatecaCaPoolIssuancePolicyAllowedKeyTypes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        backdate_duration: typing.Optional[builtins.str] = None,
        baseline_values: typing.Optional[typing.Union["PrivatecaCaPoolIssuancePolicyBaselineValues", typing.Dict[builtins.str, typing.Any]]] = None,
        identity_constraints: typing.Optional[typing.Union["PrivatecaCaPoolIssuancePolicyIdentityConstraints", typing.Dict[builtins.str, typing.Any]]] = None,
        maximum_lifetime: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allowed_issuance_modes: allowed_issuance_modes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#allowed_issuance_modes PrivatecaCaPool#allowed_issuance_modes}
        :param allowed_key_types: allowed_key_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#allowed_key_types PrivatecaCaPool#allowed_key_types}
        :param backdate_duration: The duration to backdate all certificates issued from this CaPool. If not set, the certificates will be issued with a not_before_time of the issuance time (i.e. the current time). If set, the certificates will be issued with a not_before_time of the issuance time minus the backdate_duration. The not_after_time will be adjusted to preserve the requested lifetime. The backdate_duration must be less than or equal to 48 hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#backdate_duration PrivatecaCaPool#backdate_duration}
        :param baseline_values: baseline_values block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#baseline_values PrivatecaCaPool#baseline_values}
        :param identity_constraints: identity_constraints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#identity_constraints PrivatecaCaPool#identity_constraints}
        :param maximum_lifetime: The maximum lifetime allowed for issued Certificates. Note that if the issuing CertificateAuthority expires before a Certificate's requested maximumLifetime, the effective lifetime will be explicitly truncated to match it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#maximum_lifetime PrivatecaCaPool#maximum_lifetime}
        '''
        if isinstance(allowed_issuance_modes, dict):
            allowed_issuance_modes = PrivatecaCaPoolIssuancePolicyAllowedIssuanceModes(**allowed_issuance_modes)
        if isinstance(baseline_values, dict):
            baseline_values = PrivatecaCaPoolIssuancePolicyBaselineValues(**baseline_values)
        if isinstance(identity_constraints, dict):
            identity_constraints = PrivatecaCaPoolIssuancePolicyIdentityConstraints(**identity_constraints)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c34981f55d89202df2cdff59e35210d6d45f460e3b87bbed180286cbe9c642b1)
            check_type(argname="argument allowed_issuance_modes", value=allowed_issuance_modes, expected_type=type_hints["allowed_issuance_modes"])
            check_type(argname="argument allowed_key_types", value=allowed_key_types, expected_type=type_hints["allowed_key_types"])
            check_type(argname="argument backdate_duration", value=backdate_duration, expected_type=type_hints["backdate_duration"])
            check_type(argname="argument baseline_values", value=baseline_values, expected_type=type_hints["baseline_values"])
            check_type(argname="argument identity_constraints", value=identity_constraints, expected_type=type_hints["identity_constraints"])
            check_type(argname="argument maximum_lifetime", value=maximum_lifetime, expected_type=type_hints["maximum_lifetime"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_issuance_modes is not None:
            self._values["allowed_issuance_modes"] = allowed_issuance_modes
        if allowed_key_types is not None:
            self._values["allowed_key_types"] = allowed_key_types
        if backdate_duration is not None:
            self._values["backdate_duration"] = backdate_duration
        if baseline_values is not None:
            self._values["baseline_values"] = baseline_values
        if identity_constraints is not None:
            self._values["identity_constraints"] = identity_constraints
        if maximum_lifetime is not None:
            self._values["maximum_lifetime"] = maximum_lifetime

    @builtins.property
    def allowed_issuance_modes(
        self,
    ) -> typing.Optional["PrivatecaCaPoolIssuancePolicyAllowedIssuanceModes"]:
        '''allowed_issuance_modes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#allowed_issuance_modes PrivatecaCaPool#allowed_issuance_modes}
        '''
        result = self._values.get("allowed_issuance_modes")
        return typing.cast(typing.Optional["PrivatecaCaPoolIssuancePolicyAllowedIssuanceModes"], result)

    @builtins.property
    def allowed_key_types(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivatecaCaPoolIssuancePolicyAllowedKeyTypes"]]]:
        '''allowed_key_types block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#allowed_key_types PrivatecaCaPool#allowed_key_types}
        '''
        result = self._values.get("allowed_key_types")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivatecaCaPoolIssuancePolicyAllowedKeyTypes"]]], result)

    @builtins.property
    def backdate_duration(self) -> typing.Optional[builtins.str]:
        '''The duration to backdate all certificates issued from this CaPool.

        If not set, the
        certificates will be issued with a not_before_time of the issuance time (i.e. the current
        time). If set, the certificates will be issued with a not_before_time of the issuance
        time minus the backdate_duration. The not_after_time will be adjusted to preserve the
        requested lifetime. The backdate_duration must be less than or equal to 48 hours.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#backdate_duration PrivatecaCaPool#backdate_duration}
        '''
        result = self._values.get("backdate_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def baseline_values(
        self,
    ) -> typing.Optional["PrivatecaCaPoolIssuancePolicyBaselineValues"]:
        '''baseline_values block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#baseline_values PrivatecaCaPool#baseline_values}
        '''
        result = self._values.get("baseline_values")
        return typing.cast(typing.Optional["PrivatecaCaPoolIssuancePolicyBaselineValues"], result)

    @builtins.property
    def identity_constraints(
        self,
    ) -> typing.Optional["PrivatecaCaPoolIssuancePolicyIdentityConstraints"]:
        '''identity_constraints block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#identity_constraints PrivatecaCaPool#identity_constraints}
        '''
        result = self._values.get("identity_constraints")
        return typing.cast(typing.Optional["PrivatecaCaPoolIssuancePolicyIdentityConstraints"], result)

    @builtins.property
    def maximum_lifetime(self) -> typing.Optional[builtins.str]:
        '''The maximum lifetime allowed for issued Certificates.

        Note that if the issuing CertificateAuthority
        expires before a Certificate's requested maximumLifetime, the effective lifetime will be explicitly truncated to match it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#maximum_lifetime PrivatecaCaPool#maximum_lifetime}
        '''
        result = self._values.get("maximum_lifetime")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCaPoolIssuancePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCaPool.PrivatecaCaPoolIssuancePolicyAllowedIssuanceModes",
    jsii_struct_bases=[],
    name_mapping={
        "allow_config_based_issuance": "allowConfigBasedIssuance",
        "allow_csr_based_issuance": "allowCsrBasedIssuance",
    },
)
class PrivatecaCaPoolIssuancePolicyAllowedIssuanceModes:
    def __init__(
        self,
        *,
        allow_config_based_issuance: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        allow_csr_based_issuance: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param allow_config_based_issuance: When true, allows callers to create Certificates by specifying a CertificateConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#allow_config_based_issuance PrivatecaCaPool#allow_config_based_issuance}
        :param allow_csr_based_issuance: When true, allows callers to create Certificates by specifying a CSR. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#allow_csr_based_issuance PrivatecaCaPool#allow_csr_based_issuance}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14c2d7ef77fba497d5afc66c970e461f4e13ab5c60598011e01763ca4c5e4d34)
            check_type(argname="argument allow_config_based_issuance", value=allow_config_based_issuance, expected_type=type_hints["allow_config_based_issuance"])
            check_type(argname="argument allow_csr_based_issuance", value=allow_csr_based_issuance, expected_type=type_hints["allow_csr_based_issuance"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allow_config_based_issuance": allow_config_based_issuance,
            "allow_csr_based_issuance": allow_csr_based_issuance,
        }

    @builtins.property
    def allow_config_based_issuance(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''When true, allows callers to create Certificates by specifying a CertificateConfig.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#allow_config_based_issuance PrivatecaCaPool#allow_config_based_issuance}
        '''
        result = self._values.get("allow_config_based_issuance")
        assert result is not None, "Required property 'allow_config_based_issuance' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def allow_csr_based_issuance(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''When true, allows callers to create Certificates by specifying a CSR.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#allow_csr_based_issuance PrivatecaCaPool#allow_csr_based_issuance}
        '''
        result = self._values.get("allow_csr_based_issuance")
        assert result is not None, "Required property 'allow_csr_based_issuance' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCaPoolIssuancePolicyAllowedIssuanceModes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCaPoolIssuancePolicyAllowedIssuanceModesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCaPool.PrivatecaCaPoolIssuancePolicyAllowedIssuanceModesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c8a631f85467f1a85e3e78fe5436bd30100ec5da356b41309e2d9fa5c9bebba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="allowConfigBasedIssuanceInput")
    def allow_config_based_issuance_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowConfigBasedIssuanceInput"))

    @builtins.property
    @jsii.member(jsii_name="allowCsrBasedIssuanceInput")
    def allow_csr_based_issuance_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowCsrBasedIssuanceInput"))

    @builtins.property
    @jsii.member(jsii_name="allowConfigBasedIssuance")
    def allow_config_based_issuance(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowConfigBasedIssuance"))

    @allow_config_based_issuance.setter
    def allow_config_based_issuance(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d7f9c01f530c56bb541dda8590591f0fb1bddf23f7d2e201fe4d295681babb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowConfigBasedIssuance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowCsrBasedIssuance")
    def allow_csr_based_issuance(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowCsrBasedIssuance"))

    @allow_csr_based_issuance.setter
    def allow_csr_based_issuance(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bedbd66ba0d2d6b08b21cc60db36cf9216cccf7ec1faebe84be60777516d23a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowCsrBasedIssuance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCaPoolIssuancePolicyAllowedIssuanceModes]:
        return typing.cast(typing.Optional[PrivatecaCaPoolIssuancePolicyAllowedIssuanceModes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCaPoolIssuancePolicyAllowedIssuanceModes],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87cc6e7ed240a3b5f3a7b04b42b8628e278405192d610d056d27392fefa45df6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCaPool.PrivatecaCaPoolIssuancePolicyAllowedKeyTypes",
    jsii_struct_bases=[],
    name_mapping={"elliptic_curve": "ellipticCurve", "rsa": "rsa"},
)
class PrivatecaCaPoolIssuancePolicyAllowedKeyTypes:
    def __init__(
        self,
        *,
        elliptic_curve: typing.Optional[typing.Union["PrivatecaCaPoolIssuancePolicyAllowedKeyTypesEllipticCurve", typing.Dict[builtins.str, typing.Any]]] = None,
        rsa: typing.Optional[typing.Union["PrivatecaCaPoolIssuancePolicyAllowedKeyTypesRsa", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param elliptic_curve: elliptic_curve block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#elliptic_curve PrivatecaCaPool#elliptic_curve}
        :param rsa: rsa block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#rsa PrivatecaCaPool#rsa}
        '''
        if isinstance(elliptic_curve, dict):
            elliptic_curve = PrivatecaCaPoolIssuancePolicyAllowedKeyTypesEllipticCurve(**elliptic_curve)
        if isinstance(rsa, dict):
            rsa = PrivatecaCaPoolIssuancePolicyAllowedKeyTypesRsa(**rsa)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61ea4a8205502675ebda1063465fd03db70b0363487cd01469bde009cfddd88f)
            check_type(argname="argument elliptic_curve", value=elliptic_curve, expected_type=type_hints["elliptic_curve"])
            check_type(argname="argument rsa", value=rsa, expected_type=type_hints["rsa"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if elliptic_curve is not None:
            self._values["elliptic_curve"] = elliptic_curve
        if rsa is not None:
            self._values["rsa"] = rsa

    @builtins.property
    def elliptic_curve(
        self,
    ) -> typing.Optional["PrivatecaCaPoolIssuancePolicyAllowedKeyTypesEllipticCurve"]:
        '''elliptic_curve block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#elliptic_curve PrivatecaCaPool#elliptic_curve}
        '''
        result = self._values.get("elliptic_curve")
        return typing.cast(typing.Optional["PrivatecaCaPoolIssuancePolicyAllowedKeyTypesEllipticCurve"], result)

    @builtins.property
    def rsa(self) -> typing.Optional["PrivatecaCaPoolIssuancePolicyAllowedKeyTypesRsa"]:
        '''rsa block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#rsa PrivatecaCaPool#rsa}
        '''
        result = self._values.get("rsa")
        return typing.cast(typing.Optional["PrivatecaCaPoolIssuancePolicyAllowedKeyTypesRsa"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCaPoolIssuancePolicyAllowedKeyTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCaPool.PrivatecaCaPoolIssuancePolicyAllowedKeyTypesEllipticCurve",
    jsii_struct_bases=[],
    name_mapping={"signature_algorithm": "signatureAlgorithm"},
)
class PrivatecaCaPoolIssuancePolicyAllowedKeyTypesEllipticCurve:
    def __init__(self, *, signature_algorithm: builtins.str) -> None:
        '''
        :param signature_algorithm: The algorithm used. Possible values: ["ECDSA_P256", "ECDSA_P384", "EDDSA_25519"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#signature_algorithm PrivatecaCaPool#signature_algorithm}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3b7a5f9a80bf962a83840784d468311067a8f6695124f220a0524cf96679711)
            check_type(argname="argument signature_algorithm", value=signature_algorithm, expected_type=type_hints["signature_algorithm"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "signature_algorithm": signature_algorithm,
        }

    @builtins.property
    def signature_algorithm(self) -> builtins.str:
        '''The algorithm used. Possible values: ["ECDSA_P256", "ECDSA_P384", "EDDSA_25519"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#signature_algorithm PrivatecaCaPool#signature_algorithm}
        '''
        result = self._values.get("signature_algorithm")
        assert result is not None, "Required property 'signature_algorithm' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCaPoolIssuancePolicyAllowedKeyTypesEllipticCurve(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCaPoolIssuancePolicyAllowedKeyTypesEllipticCurveOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCaPool.PrivatecaCaPoolIssuancePolicyAllowedKeyTypesEllipticCurveOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d30cf8c461f544d11254d1d3ff3aa75577aaa0d8e486a07f10fb4692a47e27f2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="signatureAlgorithmInput")
    def signature_algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "signatureAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="signatureAlgorithm")
    def signature_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "signatureAlgorithm"))

    @signature_algorithm.setter
    def signature_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8ec3c49fe6b8953b190f4b20cb8c3167457a97e71bb8d2a4a418c20d944480f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signatureAlgorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCaPoolIssuancePolicyAllowedKeyTypesEllipticCurve]:
        return typing.cast(typing.Optional[PrivatecaCaPoolIssuancePolicyAllowedKeyTypesEllipticCurve], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCaPoolIssuancePolicyAllowedKeyTypesEllipticCurve],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5078b24a194ae388492d8a6f0848f39429a06447dd61e7afe942fd978c49079)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PrivatecaCaPoolIssuancePolicyAllowedKeyTypesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCaPool.PrivatecaCaPoolIssuancePolicyAllowedKeyTypesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__71ba8a1524de5b72834a99ee5e324aafb04e3f888d7f8ab8cf85e8f457fe3d28)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PrivatecaCaPoolIssuancePolicyAllowedKeyTypesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa30517fc092660b9411cf047c9d5d41ffbfe085624f7f83d3cd5e26fcf62a55)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PrivatecaCaPoolIssuancePolicyAllowedKeyTypesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18fd014757adbfbf7c86271593b0807eb070fb77369ca30c3a581bbd4b5a8a65)
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
            type_hints = typing.get_type_hints(_typecheckingstub__117c0a3da3caca609dbb7d699ba801bf9f6682fe8b5a6e1a9f742fc437c1e9d2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d680a2f0f44a4ddf05459b972c1ea5f4abb696df68b6b3333748f53fdbb64ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCaPoolIssuancePolicyAllowedKeyTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCaPoolIssuancePolicyAllowedKeyTypes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCaPoolIssuancePolicyAllowedKeyTypes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bfa5becaef27e1f4f2752b0e0a16d7df67126769f9336a9bdd528e359d3c6c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PrivatecaCaPoolIssuancePolicyAllowedKeyTypesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCaPool.PrivatecaCaPoolIssuancePolicyAllowedKeyTypesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__30fff330aafdaafbbcd7b0dd9b7c380d004b7afe0628af0ad7f470f7245365d0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEllipticCurve")
    def put_elliptic_curve(self, *, signature_algorithm: builtins.str) -> None:
        '''
        :param signature_algorithm: The algorithm used. Possible values: ["ECDSA_P256", "ECDSA_P384", "EDDSA_25519"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#signature_algorithm PrivatecaCaPool#signature_algorithm}
        '''
        value = PrivatecaCaPoolIssuancePolicyAllowedKeyTypesEllipticCurve(
            signature_algorithm=signature_algorithm
        )

        return typing.cast(None, jsii.invoke(self, "putEllipticCurve", [value]))

    @jsii.member(jsii_name="putRsa")
    def put_rsa(
        self,
        *,
        max_modulus_size: typing.Optional[builtins.str] = None,
        min_modulus_size: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_modulus_size: The maximum allowed RSA modulus size, in bits. If this is not set, or if set to zero, the service will not enforce an explicit upper bound on RSA modulus sizes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#max_modulus_size PrivatecaCaPool#max_modulus_size}
        :param min_modulus_size: The minimum allowed RSA modulus size, in bits. If this is not set, or if set to zero, the service-level min RSA modulus size will continue to apply. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#min_modulus_size PrivatecaCaPool#min_modulus_size}
        '''
        value = PrivatecaCaPoolIssuancePolicyAllowedKeyTypesRsa(
            max_modulus_size=max_modulus_size, min_modulus_size=min_modulus_size
        )

        return typing.cast(None, jsii.invoke(self, "putRsa", [value]))

    @jsii.member(jsii_name="resetEllipticCurve")
    def reset_elliptic_curve(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEllipticCurve", []))

    @jsii.member(jsii_name="resetRsa")
    def reset_rsa(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRsa", []))

    @builtins.property
    @jsii.member(jsii_name="ellipticCurve")
    def elliptic_curve(
        self,
    ) -> PrivatecaCaPoolIssuancePolicyAllowedKeyTypesEllipticCurveOutputReference:
        return typing.cast(PrivatecaCaPoolIssuancePolicyAllowedKeyTypesEllipticCurveOutputReference, jsii.get(self, "ellipticCurve"))

    @builtins.property
    @jsii.member(jsii_name="rsa")
    def rsa(self) -> "PrivatecaCaPoolIssuancePolicyAllowedKeyTypesRsaOutputReference":
        return typing.cast("PrivatecaCaPoolIssuancePolicyAllowedKeyTypesRsaOutputReference", jsii.get(self, "rsa"))

    @builtins.property
    @jsii.member(jsii_name="ellipticCurveInput")
    def elliptic_curve_input(
        self,
    ) -> typing.Optional[PrivatecaCaPoolIssuancePolicyAllowedKeyTypesEllipticCurve]:
        return typing.cast(typing.Optional[PrivatecaCaPoolIssuancePolicyAllowedKeyTypesEllipticCurve], jsii.get(self, "ellipticCurveInput"))

    @builtins.property
    @jsii.member(jsii_name="rsaInput")
    def rsa_input(
        self,
    ) -> typing.Optional["PrivatecaCaPoolIssuancePolicyAllowedKeyTypesRsa"]:
        return typing.cast(typing.Optional["PrivatecaCaPoolIssuancePolicyAllowedKeyTypesRsa"], jsii.get(self, "rsaInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCaPoolIssuancePolicyAllowedKeyTypes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCaPoolIssuancePolicyAllowedKeyTypes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCaPoolIssuancePolicyAllowedKeyTypes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fd81a962459134f7693fdd7e8187b5df3b7882b6832ba4f630806fecab344b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCaPool.PrivatecaCaPoolIssuancePolicyAllowedKeyTypesRsa",
    jsii_struct_bases=[],
    name_mapping={
        "max_modulus_size": "maxModulusSize",
        "min_modulus_size": "minModulusSize",
    },
)
class PrivatecaCaPoolIssuancePolicyAllowedKeyTypesRsa:
    def __init__(
        self,
        *,
        max_modulus_size: typing.Optional[builtins.str] = None,
        min_modulus_size: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_modulus_size: The maximum allowed RSA modulus size, in bits. If this is not set, or if set to zero, the service will not enforce an explicit upper bound on RSA modulus sizes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#max_modulus_size PrivatecaCaPool#max_modulus_size}
        :param min_modulus_size: The minimum allowed RSA modulus size, in bits. If this is not set, or if set to zero, the service-level min RSA modulus size will continue to apply. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#min_modulus_size PrivatecaCaPool#min_modulus_size}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c04325f9ba0d2172dfebc86d266be57602fba64fe8c75004e1b94d0c9975e55c)
            check_type(argname="argument max_modulus_size", value=max_modulus_size, expected_type=type_hints["max_modulus_size"])
            check_type(argname="argument min_modulus_size", value=min_modulus_size, expected_type=type_hints["min_modulus_size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_modulus_size is not None:
            self._values["max_modulus_size"] = max_modulus_size
        if min_modulus_size is not None:
            self._values["min_modulus_size"] = min_modulus_size

    @builtins.property
    def max_modulus_size(self) -> typing.Optional[builtins.str]:
        '''The maximum allowed RSA modulus size, in bits.

        If this is not set, or if set to zero, the
        service will not enforce an explicit upper bound on RSA modulus sizes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#max_modulus_size PrivatecaCaPool#max_modulus_size}
        '''
        result = self._values.get("max_modulus_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_modulus_size(self) -> typing.Optional[builtins.str]:
        '''The minimum allowed RSA modulus size, in bits.

        If this is not set, or if set to zero, the
        service-level min RSA modulus size will continue to apply.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#min_modulus_size PrivatecaCaPool#min_modulus_size}
        '''
        result = self._values.get("min_modulus_size")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCaPoolIssuancePolicyAllowedKeyTypesRsa(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCaPoolIssuancePolicyAllowedKeyTypesRsaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCaPool.PrivatecaCaPoolIssuancePolicyAllowedKeyTypesRsaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f918b2a71d967e6f6e56867f6bb4064539440d57f261905f73937eea27b3d612)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxModulusSize")
    def reset_max_modulus_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxModulusSize", []))

    @jsii.member(jsii_name="resetMinModulusSize")
    def reset_min_modulus_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinModulusSize", []))

    @builtins.property
    @jsii.member(jsii_name="maxModulusSizeInput")
    def max_modulus_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxModulusSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="minModulusSizeInput")
    def min_modulus_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minModulusSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxModulusSize")
    def max_modulus_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxModulusSize"))

    @max_modulus_size.setter
    def max_modulus_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fa2db75e59d98fe7e08f65d6678cd67616b23ca5839d01c331fcb7b54bbdf7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxModulusSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minModulusSize")
    def min_modulus_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minModulusSize"))

    @min_modulus_size.setter
    def min_modulus_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b15a0b49d2b2c424c089f09d826dc7f0b11c1e51bce63212d24cc4986b05680)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minModulusSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCaPoolIssuancePolicyAllowedKeyTypesRsa]:
        return typing.cast(typing.Optional[PrivatecaCaPoolIssuancePolicyAllowedKeyTypesRsa], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCaPoolIssuancePolicyAllowedKeyTypesRsa],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aea21260fdcda85c23d6edb5f8a9b7a0bd87186b38f2d9769f6cb93d4aed71a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCaPool.PrivatecaCaPoolIssuancePolicyBaselineValues",
    jsii_struct_bases=[],
    name_mapping={
        "ca_options": "caOptions",
        "key_usage": "keyUsage",
        "additional_extensions": "additionalExtensions",
        "aia_ocsp_servers": "aiaOcspServers",
        "name_constraints": "nameConstraints",
        "policy_ids": "policyIds",
    },
)
class PrivatecaCaPoolIssuancePolicyBaselineValues:
    def __init__(
        self,
        *,
        ca_options: typing.Union["PrivatecaCaPoolIssuancePolicyBaselineValuesCaOptions", typing.Dict[builtins.str, typing.Any]],
        key_usage: typing.Union["PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsage", typing.Dict[builtins.str, typing.Any]],
        additional_extensions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        aia_ocsp_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
        name_constraints: typing.Optional[typing.Union["PrivatecaCaPoolIssuancePolicyBaselineValuesNameConstraints", typing.Dict[builtins.str, typing.Any]]] = None,
        policy_ids: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIds", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param ca_options: ca_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#ca_options PrivatecaCaPool#ca_options}
        :param key_usage: key_usage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#key_usage PrivatecaCaPool#key_usage}
        :param additional_extensions: additional_extensions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#additional_extensions PrivatecaCaPool#additional_extensions}
        :param aia_ocsp_servers: Describes Online Certificate Status Protocol (OCSP) endpoint addresses that appear in the "Authority Information Access" extension in the certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#aia_ocsp_servers PrivatecaCaPool#aia_ocsp_servers}
        :param name_constraints: name_constraints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#name_constraints PrivatecaCaPool#name_constraints}
        :param policy_ids: policy_ids block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#policy_ids PrivatecaCaPool#policy_ids}
        '''
        if isinstance(ca_options, dict):
            ca_options = PrivatecaCaPoolIssuancePolicyBaselineValuesCaOptions(**ca_options)
        if isinstance(key_usage, dict):
            key_usage = PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsage(**key_usage)
        if isinstance(name_constraints, dict):
            name_constraints = PrivatecaCaPoolIssuancePolicyBaselineValuesNameConstraints(**name_constraints)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d39365a30de45728b1053e44b0e5636058a8acfe98e7ade410ae5f6d1bb2ae18)
            check_type(argname="argument ca_options", value=ca_options, expected_type=type_hints["ca_options"])
            check_type(argname="argument key_usage", value=key_usage, expected_type=type_hints["key_usage"])
            check_type(argname="argument additional_extensions", value=additional_extensions, expected_type=type_hints["additional_extensions"])
            check_type(argname="argument aia_ocsp_servers", value=aia_ocsp_servers, expected_type=type_hints["aia_ocsp_servers"])
            check_type(argname="argument name_constraints", value=name_constraints, expected_type=type_hints["name_constraints"])
            check_type(argname="argument policy_ids", value=policy_ids, expected_type=type_hints["policy_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ca_options": ca_options,
            "key_usage": key_usage,
        }
        if additional_extensions is not None:
            self._values["additional_extensions"] = additional_extensions
        if aia_ocsp_servers is not None:
            self._values["aia_ocsp_servers"] = aia_ocsp_servers
        if name_constraints is not None:
            self._values["name_constraints"] = name_constraints
        if policy_ids is not None:
            self._values["policy_ids"] = policy_ids

    @builtins.property
    def ca_options(self) -> "PrivatecaCaPoolIssuancePolicyBaselineValuesCaOptions":
        '''ca_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#ca_options PrivatecaCaPool#ca_options}
        '''
        result = self._values.get("ca_options")
        assert result is not None, "Required property 'ca_options' is missing"
        return typing.cast("PrivatecaCaPoolIssuancePolicyBaselineValuesCaOptions", result)

    @builtins.property
    def key_usage(self) -> "PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsage":
        '''key_usage block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#key_usage PrivatecaCaPool#key_usage}
        '''
        result = self._values.get("key_usage")
        assert result is not None, "Required property 'key_usage' is missing"
        return typing.cast("PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsage", result)

    @builtins.property
    def additional_extensions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensions"]]]:
        '''additional_extensions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#additional_extensions PrivatecaCaPool#additional_extensions}
        '''
        result = self._values.get("additional_extensions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensions"]]], result)

    @builtins.property
    def aia_ocsp_servers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Describes Online Certificate Status Protocol (OCSP) endpoint addresses that appear in the "Authority Information Access" extension in the certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#aia_ocsp_servers PrivatecaCaPool#aia_ocsp_servers}
        '''
        result = self._values.get("aia_ocsp_servers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name_constraints(
        self,
    ) -> typing.Optional["PrivatecaCaPoolIssuancePolicyBaselineValuesNameConstraints"]:
        '''name_constraints block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#name_constraints PrivatecaCaPool#name_constraints}
        '''
        result = self._values.get("name_constraints")
        return typing.cast(typing.Optional["PrivatecaCaPoolIssuancePolicyBaselineValuesNameConstraints"], result)

    @builtins.property
    def policy_ids(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIds"]]]:
        '''policy_ids block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#policy_ids PrivatecaCaPool#policy_ids}
        '''
        result = self._values.get("policy_ids")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIds"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCaPoolIssuancePolicyBaselineValues(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCaPool.PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensions",
    jsii_struct_bases=[],
    name_mapping={"critical": "critical", "object_id": "objectId", "value": "value"},
)
class PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensions:
    def __init__(
        self,
        *,
        critical: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        object_id: typing.Union["PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsObjectId", typing.Dict[builtins.str, typing.Any]],
        value: builtins.str,
    ) -> None:
        '''
        :param critical: Indicates whether or not this extension is critical (i.e., if the client does not know how to handle this extension, the client should consider this to be an error). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#critical PrivatecaCaPool#critical}
        :param object_id: object_id block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#object_id PrivatecaCaPool#object_id}
        :param value: The value of this X.509 extension. A base64-encoded string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#value PrivatecaCaPool#value}
        '''
        if isinstance(object_id, dict):
            object_id = PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsObjectId(**object_id)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8657478a79939b26d65c5af5888e9e4fddc840ac8a44fd3a0a3f4dd31ac3ac7a)
            check_type(argname="argument critical", value=critical, expected_type=type_hints["critical"])
            check_type(argname="argument object_id", value=object_id, expected_type=type_hints["object_id"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "critical": critical,
            "object_id": object_id,
            "value": value,
        }

    @builtins.property
    def critical(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Indicates whether or not this extension is critical (i.e., if the client does not know how to handle this extension, the client should consider this to be an error).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#critical PrivatecaCaPool#critical}
        '''
        result = self._values.get("critical")
        assert result is not None, "Required property 'critical' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def object_id(
        self,
    ) -> "PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsObjectId":
        '''object_id block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#object_id PrivatecaCaPool#object_id}
        '''
        result = self._values.get("object_id")
        assert result is not None, "Required property 'object_id' is missing"
        return typing.cast("PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsObjectId", result)

    @builtins.property
    def value(self) -> builtins.str:
        '''The value of this X.509 extension. A base64-encoded string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#value PrivatecaCaPool#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCaPool.PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5946fd95c806e8c8320748219d52d4f53b4d2cc933b442d6ea60beb2f1603d49)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66c62f4867c2b992f0bae3727c70657bc944d0587cbe8032d713005aeca759a3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0905a3bfd50bf29403cc8e11f6554921fc5102bdc5b4d2f24c5d17c4192b7c9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__188559a6fd7259f427bf1855765e2b7680585d98d6513d224b0e12030351b82c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb0f40760cb9c9ffeaa5e5d408d04630349d7259cc20a6d34681ca7e01b80ea9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28cd72e1563389b54cfaaccecbd10fae59013a96d35aef2809be9202982f4ecc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCaPool.PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsObjectId",
    jsii_struct_bases=[],
    name_mapping={"object_id_path": "objectIdPath"},
)
class PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsObjectId:
    def __init__(self, *, object_id_path: typing.Sequence[jsii.Number]) -> None:
        '''
        :param object_id_path: An ObjectId specifies an object identifier (OID). These provide context and describe types in ASN.1 messages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#object_id_path PrivatecaCaPool#object_id_path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d437e32b954ac5be4babec809a244dd34878bc4abac73dd3c8667f1a8962ce6)
            check_type(argname="argument object_id_path", value=object_id_path, expected_type=type_hints["object_id_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object_id_path": object_id_path,
        }

    @builtins.property
    def object_id_path(self) -> typing.List[jsii.Number]:
        '''An ObjectId specifies an object identifier (OID). These provide context and describe types in ASN.1 messages.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#object_id_path PrivatecaCaPool#object_id_path}
        '''
        result = self._values.get("object_id_path")
        assert result is not None, "Required property 'object_id_path' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsObjectId(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsObjectIdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCaPool.PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsObjectIdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e71f033d162065334610f934ccc705fc28dbeddcfedb51307e0bb2cd58468a04)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="objectIdPathInput")
    def object_id_path_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "objectIdPathInput"))

    @builtins.property
    @jsii.member(jsii_name="objectIdPath")
    def object_id_path(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "objectIdPath"))

    @object_id_path.setter
    def object_id_path(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d16e23ec3eaa33c11d49f66d6420f1302701cfa202437c0287da68280b8b5b90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectIdPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsObjectId]:
        return typing.cast(typing.Optional[PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsObjectId], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsObjectId],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32fb0abfe7de5f22d9decf40e6e7e463bd456dff846083d6da0e242cbefe35d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCaPool.PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df76079eb2bd18df362284781d727c0db8320c36e46420721a5ada1d719181b7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putObjectId")
    def put_object_id(self, *, object_id_path: typing.Sequence[jsii.Number]) -> None:
        '''
        :param object_id_path: An ObjectId specifies an object identifier (OID). These provide context and describe types in ASN.1 messages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#object_id_path PrivatecaCaPool#object_id_path}
        '''
        value = PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsObjectId(
            object_id_path=object_id_path
        )

        return typing.cast(None, jsii.invoke(self, "putObjectId", [value]))

    @builtins.property
    @jsii.member(jsii_name="objectId")
    def object_id(
        self,
    ) -> PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsObjectIdOutputReference:
        return typing.cast(PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsObjectIdOutputReference, jsii.get(self, "objectId"))

    @builtins.property
    @jsii.member(jsii_name="criticalInput")
    def critical_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "criticalInput"))

    @builtins.property
    @jsii.member(jsii_name="objectIdInput")
    def object_id_input(
        self,
    ) -> typing.Optional[PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsObjectId]:
        return typing.cast(typing.Optional[PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsObjectId], jsii.get(self, "objectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="critical")
    def critical(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "critical"))

    @critical.setter
    def critical(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4fbe73822f980ea26101a0faaa252ad6acc2e726683a391aed4d6a416155369)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "critical", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1466d6a155b8bf4839053105bb7cb165ea5e5c29b396be0b03adba7315a3490)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42eea13eacfb22a8d88590176e74498312a618e9339567ea8c9336f6299b55d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCaPool.PrivatecaCaPoolIssuancePolicyBaselineValuesCaOptions",
    jsii_struct_bases=[],
    name_mapping={
        "is_ca": "isCa",
        "max_issuer_path_length": "maxIssuerPathLength",
        "non_ca": "nonCa",
        "zero_max_issuer_path_length": "zeroMaxIssuerPathLength",
    },
)
class PrivatecaCaPoolIssuancePolicyBaselineValuesCaOptions:
    def __init__(
        self,
        *,
        is_ca: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_issuer_path_length: typing.Optional[jsii.Number] = None,
        non_ca: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        zero_max_issuer_path_length: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param is_ca: When true, the "CA" in Basic Constraints extension will be set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#is_ca PrivatecaCaPool#is_ca}
        :param max_issuer_path_length: Refers to the "path length constraint" in Basic Constraints extension. For a CA certificate, this value describes the depth of subordinate CA certificates that are allowed. If this value is less than 0, the request will fail. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#max_issuer_path_length PrivatecaCaPool#max_issuer_path_length}
        :param non_ca: When true, the "CA" in Basic Constraints extension will be set to false. If both 'is_ca' and 'non_ca' are unset, the extension will be omitted from the CA certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#non_ca PrivatecaCaPool#non_ca}
        :param zero_max_issuer_path_length: When true, the "path length constraint" in Basic Constraints extension will be set to 0. if both 'max_issuer_path_length' and 'zero_max_issuer_path_length' are unset, the max path length will be omitted from the CA certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#zero_max_issuer_path_length PrivatecaCaPool#zero_max_issuer_path_length}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d720f20b2e23d63e789f4e593f924c9981f1ea4f267976273533320be3a13f2)
            check_type(argname="argument is_ca", value=is_ca, expected_type=type_hints["is_ca"])
            check_type(argname="argument max_issuer_path_length", value=max_issuer_path_length, expected_type=type_hints["max_issuer_path_length"])
            check_type(argname="argument non_ca", value=non_ca, expected_type=type_hints["non_ca"])
            check_type(argname="argument zero_max_issuer_path_length", value=zero_max_issuer_path_length, expected_type=type_hints["zero_max_issuer_path_length"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if is_ca is not None:
            self._values["is_ca"] = is_ca
        if max_issuer_path_length is not None:
            self._values["max_issuer_path_length"] = max_issuer_path_length
        if non_ca is not None:
            self._values["non_ca"] = non_ca
        if zero_max_issuer_path_length is not None:
            self._values["zero_max_issuer_path_length"] = zero_max_issuer_path_length

    @builtins.property
    def is_ca(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When true, the "CA" in Basic Constraints extension will be set to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#is_ca PrivatecaCaPool#is_ca}
        '''
        result = self._values.get("is_ca")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def max_issuer_path_length(self) -> typing.Optional[jsii.Number]:
        '''Refers to the "path length constraint" in Basic Constraints extension.

        For a CA certificate, this value describes the depth of
        subordinate CA certificates that are allowed. If this value is less than 0, the request will fail.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#max_issuer_path_length PrivatecaCaPool#max_issuer_path_length}
        '''
        result = self._values.get("max_issuer_path_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def non_ca(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When true, the "CA" in Basic Constraints extension will be set to false.

        If both 'is_ca' and 'non_ca' are unset, the extension will be omitted from the CA certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#non_ca PrivatecaCaPool#non_ca}
        '''
        result = self._values.get("non_ca")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def zero_max_issuer_path_length(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When true, the "path length constraint" in Basic Constraints extension will be set to 0.

        if both 'max_issuer_path_length' and 'zero_max_issuer_path_length' are unset,
        the max path length will be omitted from the CA certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#zero_max_issuer_path_length PrivatecaCaPool#zero_max_issuer_path_length}
        '''
        result = self._values.get("zero_max_issuer_path_length")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCaPoolIssuancePolicyBaselineValuesCaOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCaPoolIssuancePolicyBaselineValuesCaOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCaPool.PrivatecaCaPoolIssuancePolicyBaselineValuesCaOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__318ac8581bcd0be1def6dc68e19f47ea7e1a76d60127db15f86b00daae4d5af8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIsCa")
    def reset_is_ca(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsCa", []))

    @jsii.member(jsii_name="resetMaxIssuerPathLength")
    def reset_max_issuer_path_length(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxIssuerPathLength", []))

    @jsii.member(jsii_name="resetNonCa")
    def reset_non_ca(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNonCa", []))

    @jsii.member(jsii_name="resetZeroMaxIssuerPathLength")
    def reset_zero_max_issuer_path_length(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZeroMaxIssuerPathLength", []))

    @builtins.property
    @jsii.member(jsii_name="isCaInput")
    def is_ca_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isCaInput"))

    @builtins.property
    @jsii.member(jsii_name="maxIssuerPathLengthInput")
    def max_issuer_path_length_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxIssuerPathLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="nonCaInput")
    def non_ca_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "nonCaInput"))

    @builtins.property
    @jsii.member(jsii_name="zeroMaxIssuerPathLengthInput")
    def zero_max_issuer_path_length_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "zeroMaxIssuerPathLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="isCa")
    def is_ca(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isCa"))

    @is_ca.setter
    def is_ca(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc21192ab2a987739f9e554abf683e28f027410ac112fd40462931cb525d8a28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isCa", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxIssuerPathLength")
    def max_issuer_path_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxIssuerPathLength"))

    @max_issuer_path_length.setter
    def max_issuer_path_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0332af6191f6f75ab0d30067f1dde29d941fa8f9ff57488e7fb306525b6fe152)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxIssuerPathLength", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nonCa")
    def non_ca(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "nonCa"))

    @non_ca.setter
    def non_ca(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed301db7e00002a2e15db18320d9004a3b54c6d884799301ef198475f8728e41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nonCa", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zeroMaxIssuerPathLength")
    def zero_max_issuer_path_length(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "zeroMaxIssuerPathLength"))

    @zero_max_issuer_path_length.setter
    def zero_max_issuer_path_length(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02e63cc69ef5447344bab0603f3458683279a32002723b399f7567456cd2d702)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zeroMaxIssuerPathLength", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCaPoolIssuancePolicyBaselineValuesCaOptions]:
        return typing.cast(typing.Optional[PrivatecaCaPoolIssuancePolicyBaselineValuesCaOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCaPoolIssuancePolicyBaselineValuesCaOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73751c49aee3fc220f5624c1053b093c5ceba3cab27b4836a5253168ab6b9dfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCaPool.PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsage",
    jsii_struct_bases=[],
    name_mapping={
        "base_key_usage": "baseKeyUsage",
        "extended_key_usage": "extendedKeyUsage",
        "unknown_extended_key_usages": "unknownExtendedKeyUsages",
    },
)
class PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsage:
    def __init__(
        self,
        *,
        base_key_usage: typing.Union["PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageBaseKeyUsage", typing.Dict[builtins.str, typing.Any]],
        extended_key_usage: typing.Union["PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageExtendedKeyUsage", typing.Dict[builtins.str, typing.Any]],
        unknown_extended_key_usages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsages", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param base_key_usage: base_key_usage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#base_key_usage PrivatecaCaPool#base_key_usage}
        :param extended_key_usage: extended_key_usage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#extended_key_usage PrivatecaCaPool#extended_key_usage}
        :param unknown_extended_key_usages: unknown_extended_key_usages block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#unknown_extended_key_usages PrivatecaCaPool#unknown_extended_key_usages}
        '''
        if isinstance(base_key_usage, dict):
            base_key_usage = PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageBaseKeyUsage(**base_key_usage)
        if isinstance(extended_key_usage, dict):
            extended_key_usage = PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageExtendedKeyUsage(**extended_key_usage)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34da08d868bbad98948824da90ff7750e0738e5f25a8554a9648aa2439c58c71)
            check_type(argname="argument base_key_usage", value=base_key_usage, expected_type=type_hints["base_key_usage"])
            check_type(argname="argument extended_key_usage", value=extended_key_usage, expected_type=type_hints["extended_key_usage"])
            check_type(argname="argument unknown_extended_key_usages", value=unknown_extended_key_usages, expected_type=type_hints["unknown_extended_key_usages"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "base_key_usage": base_key_usage,
            "extended_key_usage": extended_key_usage,
        }
        if unknown_extended_key_usages is not None:
            self._values["unknown_extended_key_usages"] = unknown_extended_key_usages

    @builtins.property
    def base_key_usage(
        self,
    ) -> "PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageBaseKeyUsage":
        '''base_key_usage block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#base_key_usage PrivatecaCaPool#base_key_usage}
        '''
        result = self._values.get("base_key_usage")
        assert result is not None, "Required property 'base_key_usage' is missing"
        return typing.cast("PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageBaseKeyUsage", result)

    @builtins.property
    def extended_key_usage(
        self,
    ) -> "PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageExtendedKeyUsage":
        '''extended_key_usage block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#extended_key_usage PrivatecaCaPool#extended_key_usage}
        '''
        result = self._values.get("extended_key_usage")
        assert result is not None, "Required property 'extended_key_usage' is missing"
        return typing.cast("PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageExtendedKeyUsage", result)

    @builtins.property
    def unknown_extended_key_usages(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsages"]]]:
        '''unknown_extended_key_usages block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#unknown_extended_key_usages PrivatecaCaPool#unknown_extended_key_usages}
        '''
        result = self._values.get("unknown_extended_key_usages")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsages"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCaPool.PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageBaseKeyUsage",
    jsii_struct_bases=[],
    name_mapping={
        "cert_sign": "certSign",
        "content_commitment": "contentCommitment",
        "crl_sign": "crlSign",
        "data_encipherment": "dataEncipherment",
        "decipher_only": "decipherOnly",
        "digital_signature": "digitalSignature",
        "encipher_only": "encipherOnly",
        "key_agreement": "keyAgreement",
        "key_encipherment": "keyEncipherment",
    },
)
class PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageBaseKeyUsage:
    def __init__(
        self,
        *,
        cert_sign: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        content_commitment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        crl_sign: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        data_encipherment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        decipher_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        digital_signature: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encipher_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key_agreement: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key_encipherment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param cert_sign: The key may be used to sign certificates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#cert_sign PrivatecaCaPool#cert_sign}
        :param content_commitment: The key may be used for cryptographic commitments. Note that this may also be referred to as "non-repudiation". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#content_commitment PrivatecaCaPool#content_commitment}
        :param crl_sign: The key may be used sign certificate revocation lists. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#crl_sign PrivatecaCaPool#crl_sign}
        :param data_encipherment: The key may be used to encipher data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#data_encipherment PrivatecaCaPool#data_encipherment}
        :param decipher_only: The key may be used to decipher only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#decipher_only PrivatecaCaPool#decipher_only}
        :param digital_signature: The key may be used for digital signatures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#digital_signature PrivatecaCaPool#digital_signature}
        :param encipher_only: The key may be used to encipher only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#encipher_only PrivatecaCaPool#encipher_only}
        :param key_agreement: The key may be used in a key agreement protocol. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#key_agreement PrivatecaCaPool#key_agreement}
        :param key_encipherment: The key may be used to encipher other keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#key_encipherment PrivatecaCaPool#key_encipherment}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21d272d78e3036f98796c5d27a688a7dd8cd5bb1be520053f0ef700938a6f402)
            check_type(argname="argument cert_sign", value=cert_sign, expected_type=type_hints["cert_sign"])
            check_type(argname="argument content_commitment", value=content_commitment, expected_type=type_hints["content_commitment"])
            check_type(argname="argument crl_sign", value=crl_sign, expected_type=type_hints["crl_sign"])
            check_type(argname="argument data_encipherment", value=data_encipherment, expected_type=type_hints["data_encipherment"])
            check_type(argname="argument decipher_only", value=decipher_only, expected_type=type_hints["decipher_only"])
            check_type(argname="argument digital_signature", value=digital_signature, expected_type=type_hints["digital_signature"])
            check_type(argname="argument encipher_only", value=encipher_only, expected_type=type_hints["encipher_only"])
            check_type(argname="argument key_agreement", value=key_agreement, expected_type=type_hints["key_agreement"])
            check_type(argname="argument key_encipherment", value=key_encipherment, expected_type=type_hints["key_encipherment"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cert_sign is not None:
            self._values["cert_sign"] = cert_sign
        if content_commitment is not None:
            self._values["content_commitment"] = content_commitment
        if crl_sign is not None:
            self._values["crl_sign"] = crl_sign
        if data_encipherment is not None:
            self._values["data_encipherment"] = data_encipherment
        if decipher_only is not None:
            self._values["decipher_only"] = decipher_only
        if digital_signature is not None:
            self._values["digital_signature"] = digital_signature
        if encipher_only is not None:
            self._values["encipher_only"] = encipher_only
        if key_agreement is not None:
            self._values["key_agreement"] = key_agreement
        if key_encipherment is not None:
            self._values["key_encipherment"] = key_encipherment

    @builtins.property
    def cert_sign(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The key may be used to sign certificates.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#cert_sign PrivatecaCaPool#cert_sign}
        '''
        result = self._values.get("cert_sign")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def content_commitment(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The key may be used for cryptographic commitments. Note that this may also be referred to as "non-repudiation".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#content_commitment PrivatecaCaPool#content_commitment}
        '''
        result = self._values.get("content_commitment")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def crl_sign(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The key may be used sign certificate revocation lists.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#crl_sign PrivatecaCaPool#crl_sign}
        '''
        result = self._values.get("crl_sign")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def data_encipherment(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The key may be used to encipher data.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#data_encipherment PrivatecaCaPool#data_encipherment}
        '''
        result = self._values.get("data_encipherment")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def decipher_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The key may be used to decipher only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#decipher_only PrivatecaCaPool#decipher_only}
        '''
        result = self._values.get("decipher_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def digital_signature(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The key may be used for digital signatures.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#digital_signature PrivatecaCaPool#digital_signature}
        '''
        result = self._values.get("digital_signature")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encipher_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The key may be used to encipher only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#encipher_only PrivatecaCaPool#encipher_only}
        '''
        result = self._values.get("encipher_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def key_agreement(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The key may be used in a key agreement protocol.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#key_agreement PrivatecaCaPool#key_agreement}
        '''
        result = self._values.get("key_agreement")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def key_encipherment(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The key may be used to encipher other keys.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#key_encipherment PrivatecaCaPool#key_encipherment}
        '''
        result = self._values.get("key_encipherment")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageBaseKeyUsage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageBaseKeyUsageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCaPool.PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageBaseKeyUsageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__00543fe1860e31887682eb8dceabd365c8c8b465a455269ce4322f1896de4b31)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCertSign")
    def reset_cert_sign(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertSign", []))

    @jsii.member(jsii_name="resetContentCommitment")
    def reset_content_commitment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentCommitment", []))

    @jsii.member(jsii_name="resetCrlSign")
    def reset_crl_sign(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrlSign", []))

    @jsii.member(jsii_name="resetDataEncipherment")
    def reset_data_encipherment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataEncipherment", []))

    @jsii.member(jsii_name="resetDecipherOnly")
    def reset_decipher_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDecipherOnly", []))

    @jsii.member(jsii_name="resetDigitalSignature")
    def reset_digital_signature(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDigitalSignature", []))

    @jsii.member(jsii_name="resetEncipherOnly")
    def reset_encipher_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncipherOnly", []))

    @jsii.member(jsii_name="resetKeyAgreement")
    def reset_key_agreement(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyAgreement", []))

    @jsii.member(jsii_name="resetKeyEncipherment")
    def reset_key_encipherment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyEncipherment", []))

    @builtins.property
    @jsii.member(jsii_name="certSignInput")
    def cert_sign_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "certSignInput"))

    @builtins.property
    @jsii.member(jsii_name="contentCommitmentInput")
    def content_commitment_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "contentCommitmentInput"))

    @builtins.property
    @jsii.member(jsii_name="crlSignInput")
    def crl_sign_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "crlSignInput"))

    @builtins.property
    @jsii.member(jsii_name="dataEnciphermentInput")
    def data_encipherment_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dataEnciphermentInput"))

    @builtins.property
    @jsii.member(jsii_name="decipherOnlyInput")
    def decipher_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "decipherOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="digitalSignatureInput")
    def digital_signature_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "digitalSignatureInput"))

    @builtins.property
    @jsii.member(jsii_name="encipherOnlyInput")
    def encipher_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "encipherOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="keyAgreementInput")
    def key_agreement_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "keyAgreementInput"))

    @builtins.property
    @jsii.member(jsii_name="keyEnciphermentInput")
    def key_encipherment_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "keyEnciphermentInput"))

    @builtins.property
    @jsii.member(jsii_name="certSign")
    def cert_sign(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "certSign"))

    @cert_sign.setter
    def cert_sign(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02a2bb1f4dd6c3b410bc4498ba695c2e42314a60bee89f1bfd8996c8c69368b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certSign", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contentCommitment")
    def content_commitment(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "contentCommitment"))

    @content_commitment.setter
    def content_commitment(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fee78c6a9f435de3acf9edf9c29355f784940b9fd3e44ac4c1f4b1ecda16e4f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentCommitment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="crlSign")
    def crl_sign(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "crlSign"))

    @crl_sign.setter
    def crl_sign(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0770c4eea9bbd3845a5de8064dbdef989472241956b0c61ac400b5174a6ec532)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crlSign", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataEncipherment")
    def data_encipherment(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dataEncipherment"))

    @data_encipherment.setter
    def data_encipherment(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79945b92f87a3aad0a926dafc93cec50a8c1876b994f8ab0c1eb4c54401b33bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataEncipherment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="decipherOnly")
    def decipher_only(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "decipherOnly"))

    @decipher_only.setter
    def decipher_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a627d2bc983dc3ec8284c2467dbfa8948454d38caa04cdfe66e8864536f9bf9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "decipherOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="digitalSignature")
    def digital_signature(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "digitalSignature"))

    @digital_signature.setter
    def digital_signature(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__269c215802152b4615a73f3256982ec211e76460de89b4b224985fb65a24748c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "digitalSignature", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encipherOnly")
    def encipher_only(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "encipherOnly"))

    @encipher_only.setter
    def encipher_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dbca81ecea17ba4e87d1651b90e48be582c3c1e8d1bdc4b12663bf51eb4432d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encipherOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyAgreement")
    def key_agreement(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "keyAgreement"))

    @key_agreement.setter
    def key_agreement(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e27896a64bbd63b493afc76dbce805e951fa05611f58416e41bae7783f61f414)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyAgreement", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyEncipherment")
    def key_encipherment(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "keyEncipherment"))

    @key_encipherment.setter
    def key_encipherment(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fcd6e35e913188759898fec421dd9b0978c158b59c348a4da9d9bc3fc85eea5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyEncipherment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageBaseKeyUsage]:
        return typing.cast(typing.Optional[PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageBaseKeyUsage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageBaseKeyUsage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84b3937c3a7a5de2941a9e2c096140138d5015888c81d714b3a949bd433e0066)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCaPool.PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageExtendedKeyUsage",
    jsii_struct_bases=[],
    name_mapping={
        "client_auth": "clientAuth",
        "code_signing": "codeSigning",
        "email_protection": "emailProtection",
        "ocsp_signing": "ocspSigning",
        "server_auth": "serverAuth",
        "time_stamping": "timeStamping",
    },
)
class PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageExtendedKeyUsage:
    def __init__(
        self,
        *,
        client_auth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        code_signing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        email_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ocsp_signing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        server_auth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        time_stamping: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param client_auth: Corresponds to OID 1.3.6.1.5.5.7.3.2. Officially described as "TLS WWW client authentication", though regularly used for non-WWW TLS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#client_auth PrivatecaCaPool#client_auth}
        :param code_signing: Corresponds to OID 1.3.6.1.5.5.7.3.3. Officially described as "Signing of downloadable executable code client authentication". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#code_signing PrivatecaCaPool#code_signing}
        :param email_protection: Corresponds to OID 1.3.6.1.5.5.7.3.4. Officially described as "Email protection". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#email_protection PrivatecaCaPool#email_protection}
        :param ocsp_signing: Corresponds to OID 1.3.6.1.5.5.7.3.9. Officially described as "Signing OCSP responses". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#ocsp_signing PrivatecaCaPool#ocsp_signing}
        :param server_auth: Corresponds to OID 1.3.6.1.5.5.7.3.1. Officially described as "TLS WWW server authentication", though regularly used for non-WWW TLS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#server_auth PrivatecaCaPool#server_auth}
        :param time_stamping: Corresponds to OID 1.3.6.1.5.5.7.3.8. Officially described as "Binding the hash of an object to a time". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#time_stamping PrivatecaCaPool#time_stamping}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd9aa2f52ed6f03bb512ae801af7233ed7cc6904fdb8c270166a8c7874e61936)
            check_type(argname="argument client_auth", value=client_auth, expected_type=type_hints["client_auth"])
            check_type(argname="argument code_signing", value=code_signing, expected_type=type_hints["code_signing"])
            check_type(argname="argument email_protection", value=email_protection, expected_type=type_hints["email_protection"])
            check_type(argname="argument ocsp_signing", value=ocsp_signing, expected_type=type_hints["ocsp_signing"])
            check_type(argname="argument server_auth", value=server_auth, expected_type=type_hints["server_auth"])
            check_type(argname="argument time_stamping", value=time_stamping, expected_type=type_hints["time_stamping"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_auth is not None:
            self._values["client_auth"] = client_auth
        if code_signing is not None:
            self._values["code_signing"] = code_signing
        if email_protection is not None:
            self._values["email_protection"] = email_protection
        if ocsp_signing is not None:
            self._values["ocsp_signing"] = ocsp_signing
        if server_auth is not None:
            self._values["server_auth"] = server_auth
        if time_stamping is not None:
            self._values["time_stamping"] = time_stamping

    @builtins.property
    def client_auth(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Corresponds to OID 1.3.6.1.5.5.7.3.2. Officially described as "TLS WWW client authentication", though regularly used for non-WWW TLS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#client_auth PrivatecaCaPool#client_auth}
        '''
        result = self._values.get("client_auth")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def code_signing(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Corresponds to OID 1.3.6.1.5.5.7.3.3. Officially described as "Signing of downloadable executable code client authentication".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#code_signing PrivatecaCaPool#code_signing}
        '''
        result = self._values.get("code_signing")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def email_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Corresponds to OID 1.3.6.1.5.5.7.3.4. Officially described as "Email protection".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#email_protection PrivatecaCaPool#email_protection}
        '''
        result = self._values.get("email_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ocsp_signing(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Corresponds to OID 1.3.6.1.5.5.7.3.9. Officially described as "Signing OCSP responses".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#ocsp_signing PrivatecaCaPool#ocsp_signing}
        '''
        result = self._values.get("ocsp_signing")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def server_auth(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Corresponds to OID 1.3.6.1.5.5.7.3.1. Officially described as "TLS WWW server authentication", though regularly used for non-WWW TLS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#server_auth PrivatecaCaPool#server_auth}
        '''
        result = self._values.get("server_auth")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def time_stamping(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Corresponds to OID 1.3.6.1.5.5.7.3.8. Officially described as "Binding the hash of an object to a time".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#time_stamping PrivatecaCaPool#time_stamping}
        '''
        result = self._values.get("time_stamping")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageExtendedKeyUsage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageExtendedKeyUsageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCaPool.PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageExtendedKeyUsageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aad0568f743e8c662b03ea193300c764f14f57e2a82d33006337c6d93f9269b7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetClientAuth")
    def reset_client_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientAuth", []))

    @jsii.member(jsii_name="resetCodeSigning")
    def reset_code_signing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCodeSigning", []))

    @jsii.member(jsii_name="resetEmailProtection")
    def reset_email_protection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailProtection", []))

    @jsii.member(jsii_name="resetOcspSigning")
    def reset_ocsp_signing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOcspSigning", []))

    @jsii.member(jsii_name="resetServerAuth")
    def reset_server_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerAuth", []))

    @jsii.member(jsii_name="resetTimeStamping")
    def reset_time_stamping(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeStamping", []))

    @builtins.property
    @jsii.member(jsii_name="clientAuthInput")
    def client_auth_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "clientAuthInput"))

    @builtins.property
    @jsii.member(jsii_name="codeSigningInput")
    def code_signing_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "codeSigningInput"))

    @builtins.property
    @jsii.member(jsii_name="emailProtectionInput")
    def email_protection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "emailProtectionInput"))

    @builtins.property
    @jsii.member(jsii_name="ocspSigningInput")
    def ocsp_signing_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ocspSigningInput"))

    @builtins.property
    @jsii.member(jsii_name="serverAuthInput")
    def server_auth_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "serverAuthInput"))

    @builtins.property
    @jsii.member(jsii_name="timeStampingInput")
    def time_stamping_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeStampingInput"))

    @builtins.property
    @jsii.member(jsii_name="clientAuth")
    def client_auth(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "clientAuth"))

    @client_auth.setter
    def client_auth(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a37847cd3356e628455b55e452d45a300207c78f4dd51c9eb39f48c9c9ca506)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientAuth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="codeSigning")
    def code_signing(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "codeSigning"))

    @code_signing.setter
    def code_signing(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61e46389385c93acb8beecb7fca8c5caf3e9c579416ac060e3931fb86fe7076e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "codeSigning", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="emailProtection")
    def email_protection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "emailProtection"))

    @email_protection.setter
    def email_protection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd7fd9363a71ed7f730198d07c8f1726bd6280426ee94df07fb292f40f7927ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailProtection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ocspSigning")
    def ocsp_signing(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ocspSigning"))

    @ocsp_signing.setter
    def ocsp_signing(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a81383e818e764d29c2db0216ad5ced77e95b43426e48b0c7db653ac9c10a84a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ocspSigning", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serverAuth")
    def server_auth(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "serverAuth"))

    @server_auth.setter
    def server_auth(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0152b0760cacabe01ca64dd573ae20017f3ac911482ef9914b9755beff8b5b27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverAuth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeStamping")
    def time_stamping(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "timeStamping"))

    @time_stamping.setter
    def time_stamping(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d216c5d9fd97c45bbed9e01daff99190456cfd09ee50d45ac80701ff4d6dca35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeStamping", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageExtendedKeyUsage]:
        return typing.cast(typing.Optional[PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageExtendedKeyUsage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageExtendedKeyUsage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c37c9a1d02565a5817928fecbfe9b249d357cef0769f4e1727208528f2c12c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCaPool.PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__979c3f9c7806d3e462c5273f7f032ee81c774dce044dfdb0fb2bd7d4779c42b6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBaseKeyUsage")
    def put_base_key_usage(
        self,
        *,
        cert_sign: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        content_commitment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        crl_sign: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        data_encipherment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        decipher_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        digital_signature: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encipher_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key_agreement: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key_encipherment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param cert_sign: The key may be used to sign certificates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#cert_sign PrivatecaCaPool#cert_sign}
        :param content_commitment: The key may be used for cryptographic commitments. Note that this may also be referred to as "non-repudiation". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#content_commitment PrivatecaCaPool#content_commitment}
        :param crl_sign: The key may be used sign certificate revocation lists. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#crl_sign PrivatecaCaPool#crl_sign}
        :param data_encipherment: The key may be used to encipher data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#data_encipherment PrivatecaCaPool#data_encipherment}
        :param decipher_only: The key may be used to decipher only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#decipher_only PrivatecaCaPool#decipher_only}
        :param digital_signature: The key may be used for digital signatures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#digital_signature PrivatecaCaPool#digital_signature}
        :param encipher_only: The key may be used to encipher only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#encipher_only PrivatecaCaPool#encipher_only}
        :param key_agreement: The key may be used in a key agreement protocol. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#key_agreement PrivatecaCaPool#key_agreement}
        :param key_encipherment: The key may be used to encipher other keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#key_encipherment PrivatecaCaPool#key_encipherment}
        '''
        value = PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageBaseKeyUsage(
            cert_sign=cert_sign,
            content_commitment=content_commitment,
            crl_sign=crl_sign,
            data_encipherment=data_encipherment,
            decipher_only=decipher_only,
            digital_signature=digital_signature,
            encipher_only=encipher_only,
            key_agreement=key_agreement,
            key_encipherment=key_encipherment,
        )

        return typing.cast(None, jsii.invoke(self, "putBaseKeyUsage", [value]))

    @jsii.member(jsii_name="putExtendedKeyUsage")
    def put_extended_key_usage(
        self,
        *,
        client_auth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        code_signing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        email_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ocsp_signing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        server_auth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        time_stamping: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param client_auth: Corresponds to OID 1.3.6.1.5.5.7.3.2. Officially described as "TLS WWW client authentication", though regularly used for non-WWW TLS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#client_auth PrivatecaCaPool#client_auth}
        :param code_signing: Corresponds to OID 1.3.6.1.5.5.7.3.3. Officially described as "Signing of downloadable executable code client authentication". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#code_signing PrivatecaCaPool#code_signing}
        :param email_protection: Corresponds to OID 1.3.6.1.5.5.7.3.4. Officially described as "Email protection". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#email_protection PrivatecaCaPool#email_protection}
        :param ocsp_signing: Corresponds to OID 1.3.6.1.5.5.7.3.9. Officially described as "Signing OCSP responses". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#ocsp_signing PrivatecaCaPool#ocsp_signing}
        :param server_auth: Corresponds to OID 1.3.6.1.5.5.7.3.1. Officially described as "TLS WWW server authentication", though regularly used for non-WWW TLS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#server_auth PrivatecaCaPool#server_auth}
        :param time_stamping: Corresponds to OID 1.3.6.1.5.5.7.3.8. Officially described as "Binding the hash of an object to a time". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#time_stamping PrivatecaCaPool#time_stamping}
        '''
        value = PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageExtendedKeyUsage(
            client_auth=client_auth,
            code_signing=code_signing,
            email_protection=email_protection,
            ocsp_signing=ocsp_signing,
            server_auth=server_auth,
            time_stamping=time_stamping,
        )

        return typing.cast(None, jsii.invoke(self, "putExtendedKeyUsage", [value]))

    @jsii.member(jsii_name="putUnknownExtendedKeyUsages")
    def put_unknown_extended_key_usages(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsages", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3777050ca072603beb2bcd509a5b7558f69d22083ab3650d275cd1b66d36484)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putUnknownExtendedKeyUsages", [value]))

    @jsii.member(jsii_name="resetUnknownExtendedKeyUsages")
    def reset_unknown_extended_key_usages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnknownExtendedKeyUsages", []))

    @builtins.property
    @jsii.member(jsii_name="baseKeyUsage")
    def base_key_usage(
        self,
    ) -> PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageBaseKeyUsageOutputReference:
        return typing.cast(PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageBaseKeyUsageOutputReference, jsii.get(self, "baseKeyUsage"))

    @builtins.property
    @jsii.member(jsii_name="extendedKeyUsage")
    def extended_key_usage(
        self,
    ) -> PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageExtendedKeyUsageOutputReference:
        return typing.cast(PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageExtendedKeyUsageOutputReference, jsii.get(self, "extendedKeyUsage"))

    @builtins.property
    @jsii.member(jsii_name="unknownExtendedKeyUsages")
    def unknown_extended_key_usages(
        self,
    ) -> "PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsagesList":
        return typing.cast("PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsagesList", jsii.get(self, "unknownExtendedKeyUsages"))

    @builtins.property
    @jsii.member(jsii_name="baseKeyUsageInput")
    def base_key_usage_input(
        self,
    ) -> typing.Optional[PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageBaseKeyUsage]:
        return typing.cast(typing.Optional[PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageBaseKeyUsage], jsii.get(self, "baseKeyUsageInput"))

    @builtins.property
    @jsii.member(jsii_name="extendedKeyUsageInput")
    def extended_key_usage_input(
        self,
    ) -> typing.Optional[PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageExtendedKeyUsage]:
        return typing.cast(typing.Optional[PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageExtendedKeyUsage], jsii.get(self, "extendedKeyUsageInput"))

    @builtins.property
    @jsii.member(jsii_name="unknownExtendedKeyUsagesInput")
    def unknown_extended_key_usages_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsages"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsages"]]], jsii.get(self, "unknownExtendedKeyUsagesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsage]:
        return typing.cast(typing.Optional[PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4897e1cce7f10dabb4ffa58cc27159134c44304ffed3658728979b5d577b811)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCaPool.PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsages",
    jsii_struct_bases=[],
    name_mapping={"object_id_path": "objectIdPath"},
)
class PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsages:
    def __init__(self, *, object_id_path: typing.Sequence[jsii.Number]) -> None:
        '''
        :param object_id_path: An ObjectId specifies an object identifier (OID). These provide context and describe types in ASN.1 messages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#object_id_path PrivatecaCaPool#object_id_path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__500f7d68c807fe6815b2925dda14e8203332c3ed14cb4f3f386ff8b23f77d4b2)
            check_type(argname="argument object_id_path", value=object_id_path, expected_type=type_hints["object_id_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object_id_path": object_id_path,
        }

    @builtins.property
    def object_id_path(self) -> typing.List[jsii.Number]:
        '''An ObjectId specifies an object identifier (OID). These provide context and describe types in ASN.1 messages.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#object_id_path PrivatecaCaPool#object_id_path}
        '''
        result = self._values.get("object_id_path")
        assert result is not None, "Required property 'object_id_path' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsages(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsagesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCaPool.PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsagesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0edb3822c48e59b859f9e79ab482228a1c6947a4eafc8f90d86f8fae601027ac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsagesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7d942ae374ee9fd27b25dd0ff418ac7e047f8133d0306d9663d93502c67c96f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsagesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4569617f3916d1542de29f216d2e7edddd320dc3ba5dc2b5378efe803e8f8999)
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
            type_hints = typing.get_type_hints(_typecheckingstub__906757478437dd3fb01d5c01fc132c90fe777225f6b3e661eb46e4b8453cffb2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7a891f78e207717e80c28c024963b51ee6fc5e138c89c0531fb0dd0aa20a3e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsages]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsages]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsages]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58a74596b6ef5f25dd6a13511483c204b49043a53db2fadbe87d5da3f8be9e54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsagesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCaPool.PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsagesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d70984429689597c37c17901d55e82207d73d786cdf6f141f349c399158b5e3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="objectIdPathInput")
    def object_id_path_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "objectIdPathInput"))

    @builtins.property
    @jsii.member(jsii_name="objectIdPath")
    def object_id_path(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "objectIdPath"))

    @object_id_path.setter
    def object_id_path(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efca8c5e9205e306048b77170985ac69c973d876ae7d50d0c1690bcec71a0e8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectIdPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsages]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsages]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsages]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__998a963444c70207c929a4ec62906dd658feadca11288768ff985361d4077027)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCaPool.PrivatecaCaPoolIssuancePolicyBaselineValuesNameConstraints",
    jsii_struct_bases=[],
    name_mapping={
        "critical": "critical",
        "excluded_dns_names": "excludedDnsNames",
        "excluded_email_addresses": "excludedEmailAddresses",
        "excluded_ip_ranges": "excludedIpRanges",
        "excluded_uris": "excludedUris",
        "permitted_dns_names": "permittedDnsNames",
        "permitted_email_addresses": "permittedEmailAddresses",
        "permitted_ip_ranges": "permittedIpRanges",
        "permitted_uris": "permittedUris",
    },
)
class PrivatecaCaPoolIssuancePolicyBaselineValuesNameConstraints:
    def __init__(
        self,
        *,
        critical: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        excluded_dns_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        excluded_email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        excluded_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        excluded_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        permitted_dns_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        permitted_email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        permitted_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        permitted_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param critical: Indicates whether or not the name constraints are marked critical. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#critical PrivatecaCaPool#critical}
        :param excluded_dns_names: Contains excluded DNS names. Any DNS name that can be constructed by simply adding zero or more labels to the left-hand side of the name satisfies the name constraint. For example, 'example.com', 'www.example.com', 'www.sub.example.com' would satisfy 'example.com' while 'example1.com' does not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#excluded_dns_names PrivatecaCaPool#excluded_dns_names}
        :param excluded_email_addresses: Contains the excluded email addresses. The value can be a particular email address, a hostname to indicate all email addresses on that host or a domain with a leading period (e.g. '.example.com') to indicate all email addresses in that domain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#excluded_email_addresses PrivatecaCaPool#excluded_email_addresses}
        :param excluded_ip_ranges: Contains the excluded IP ranges. For IPv4 addresses, the ranges are expressed using CIDR notation as specified in RFC 4632. For IPv6 addresses, the ranges are expressed in similar encoding as IPv4 addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#excluded_ip_ranges PrivatecaCaPool#excluded_ip_ranges}
        :param excluded_uris: Contains the excluded URIs that apply to the host part of the name. The value can be a hostname or a domain with a leading period (like '.example.com') Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#excluded_uris PrivatecaCaPool#excluded_uris}
        :param permitted_dns_names: Contains permitted DNS names. Any DNS name that can be constructed by simply adding zero or more labels to the left-hand side of the name satisfies the name constraint. For example, 'example.com', 'www.example.com', 'www.sub.example.com' would satisfy 'example.com' while 'example1.com' does not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#permitted_dns_names PrivatecaCaPool#permitted_dns_names}
        :param permitted_email_addresses: Contains the permitted email addresses. The value can be a particular email address, a hostname to indicate all email addresses on that host or a domain with a leading period (e.g. '.example.com') to indicate all email addresses in that domain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#permitted_email_addresses PrivatecaCaPool#permitted_email_addresses}
        :param permitted_ip_ranges: Contains the permitted IP ranges. For IPv4 addresses, the ranges are expressed using CIDR notation as specified in RFC 4632. For IPv6 addresses, the ranges are expressed in similar encoding as IPv4 addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#permitted_ip_ranges PrivatecaCaPool#permitted_ip_ranges}
        :param permitted_uris: Contains the permitted URIs that apply to the host part of the name. The value can be a hostname or a domain with a leading period (like '.example.com') Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#permitted_uris PrivatecaCaPool#permitted_uris}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8289a5563e4508871934f6027d172e923a002b2dbb9d4444d63fcb5ae6456066)
            check_type(argname="argument critical", value=critical, expected_type=type_hints["critical"])
            check_type(argname="argument excluded_dns_names", value=excluded_dns_names, expected_type=type_hints["excluded_dns_names"])
            check_type(argname="argument excluded_email_addresses", value=excluded_email_addresses, expected_type=type_hints["excluded_email_addresses"])
            check_type(argname="argument excluded_ip_ranges", value=excluded_ip_ranges, expected_type=type_hints["excluded_ip_ranges"])
            check_type(argname="argument excluded_uris", value=excluded_uris, expected_type=type_hints["excluded_uris"])
            check_type(argname="argument permitted_dns_names", value=permitted_dns_names, expected_type=type_hints["permitted_dns_names"])
            check_type(argname="argument permitted_email_addresses", value=permitted_email_addresses, expected_type=type_hints["permitted_email_addresses"])
            check_type(argname="argument permitted_ip_ranges", value=permitted_ip_ranges, expected_type=type_hints["permitted_ip_ranges"])
            check_type(argname="argument permitted_uris", value=permitted_uris, expected_type=type_hints["permitted_uris"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "critical": critical,
        }
        if excluded_dns_names is not None:
            self._values["excluded_dns_names"] = excluded_dns_names
        if excluded_email_addresses is not None:
            self._values["excluded_email_addresses"] = excluded_email_addresses
        if excluded_ip_ranges is not None:
            self._values["excluded_ip_ranges"] = excluded_ip_ranges
        if excluded_uris is not None:
            self._values["excluded_uris"] = excluded_uris
        if permitted_dns_names is not None:
            self._values["permitted_dns_names"] = permitted_dns_names
        if permitted_email_addresses is not None:
            self._values["permitted_email_addresses"] = permitted_email_addresses
        if permitted_ip_ranges is not None:
            self._values["permitted_ip_ranges"] = permitted_ip_ranges
        if permitted_uris is not None:
            self._values["permitted_uris"] = permitted_uris

    @builtins.property
    def critical(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Indicates whether or not the name constraints are marked critical.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#critical PrivatecaCaPool#critical}
        '''
        result = self._values.get("critical")
        assert result is not None, "Required property 'critical' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def excluded_dns_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Contains excluded DNS names.

        Any DNS name that can be
        constructed by simply adding zero or more labels to
        the left-hand side of the name satisfies the name constraint.
        For example, 'example.com', 'www.example.com', 'www.sub.example.com'
        would satisfy 'example.com' while 'example1.com' does not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#excluded_dns_names PrivatecaCaPool#excluded_dns_names}
        '''
        result = self._values.get("excluded_dns_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def excluded_email_addresses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Contains the excluded email addresses.

        The value can be a particular
        email address, a hostname to indicate all email addresses on that host or
        a domain with a leading period (e.g. '.example.com') to indicate
        all email addresses in that domain.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#excluded_email_addresses PrivatecaCaPool#excluded_email_addresses}
        '''
        result = self._values.get("excluded_email_addresses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def excluded_ip_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Contains the excluded IP ranges.

        For IPv4 addresses, the ranges
        are expressed using CIDR notation as specified in RFC 4632.
        For IPv6 addresses, the ranges are expressed in similar encoding as IPv4
        addresses.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#excluded_ip_ranges PrivatecaCaPool#excluded_ip_ranges}
        '''
        result = self._values.get("excluded_ip_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def excluded_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Contains the excluded URIs that apply to the host part of the name.

        The value can be a hostname or a domain with a
        leading period (like '.example.com')

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#excluded_uris PrivatecaCaPool#excluded_uris}
        '''
        result = self._values.get("excluded_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def permitted_dns_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Contains permitted DNS names.

        Any DNS name that can be
        constructed by simply adding zero or more labels to
        the left-hand side of the name satisfies the name constraint.
        For example, 'example.com', 'www.example.com', 'www.sub.example.com'
        would satisfy 'example.com' while 'example1.com' does not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#permitted_dns_names PrivatecaCaPool#permitted_dns_names}
        '''
        result = self._values.get("permitted_dns_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def permitted_email_addresses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Contains the permitted email addresses.

        The value can be a particular
        email address, a hostname to indicate all email addresses on that host or
        a domain with a leading period (e.g. '.example.com') to indicate
        all email addresses in that domain.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#permitted_email_addresses PrivatecaCaPool#permitted_email_addresses}
        '''
        result = self._values.get("permitted_email_addresses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def permitted_ip_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Contains the permitted IP ranges.

        For IPv4 addresses, the ranges
        are expressed using CIDR notation as specified in RFC 4632.
        For IPv6 addresses, the ranges are expressed in similar encoding as IPv4
        addresses.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#permitted_ip_ranges PrivatecaCaPool#permitted_ip_ranges}
        '''
        result = self._values.get("permitted_ip_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def permitted_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Contains the permitted URIs that apply to the host part of the name.

        The value can be a hostname or a domain with a
        leading period (like '.example.com')

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#permitted_uris PrivatecaCaPool#permitted_uris}
        '''
        result = self._values.get("permitted_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCaPoolIssuancePolicyBaselineValuesNameConstraints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCaPoolIssuancePolicyBaselineValuesNameConstraintsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCaPool.PrivatecaCaPoolIssuancePolicyBaselineValuesNameConstraintsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9157daeefcacf169493e1c75d6bedbd130f47f76352d378d437a58be1a3858d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExcludedDnsNames")
    def reset_excluded_dns_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludedDnsNames", []))

    @jsii.member(jsii_name="resetExcludedEmailAddresses")
    def reset_excluded_email_addresses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludedEmailAddresses", []))

    @jsii.member(jsii_name="resetExcludedIpRanges")
    def reset_excluded_ip_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludedIpRanges", []))

    @jsii.member(jsii_name="resetExcludedUris")
    def reset_excluded_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludedUris", []))

    @jsii.member(jsii_name="resetPermittedDnsNames")
    def reset_permitted_dns_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermittedDnsNames", []))

    @jsii.member(jsii_name="resetPermittedEmailAddresses")
    def reset_permitted_email_addresses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermittedEmailAddresses", []))

    @jsii.member(jsii_name="resetPermittedIpRanges")
    def reset_permitted_ip_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermittedIpRanges", []))

    @jsii.member(jsii_name="resetPermittedUris")
    def reset_permitted_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermittedUris", []))

    @builtins.property
    @jsii.member(jsii_name="criticalInput")
    def critical_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "criticalInput"))

    @builtins.property
    @jsii.member(jsii_name="excludedDnsNamesInput")
    def excluded_dns_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludedDnsNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="excludedEmailAddressesInput")
    def excluded_email_addresses_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludedEmailAddressesInput"))

    @builtins.property
    @jsii.member(jsii_name="excludedIpRangesInput")
    def excluded_ip_ranges_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludedIpRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="excludedUrisInput")
    def excluded_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludedUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="permittedDnsNamesInput")
    def permitted_dns_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "permittedDnsNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="permittedEmailAddressesInput")
    def permitted_email_addresses_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "permittedEmailAddressesInput"))

    @builtins.property
    @jsii.member(jsii_name="permittedIpRangesInput")
    def permitted_ip_ranges_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "permittedIpRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="permittedUrisInput")
    def permitted_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "permittedUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="critical")
    def critical(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "critical"))

    @critical.setter
    def critical(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e67104e871aabe711ec14bd8c118110bc3d3623b06ae1c5fc6e1419eecb89a11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "critical", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludedDnsNames")
    def excluded_dns_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludedDnsNames"))

    @excluded_dns_names.setter
    def excluded_dns_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e20d462f4608cce41f60d3cf3efb6b703f0e1bcf2b53de32f007ff77802b6af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludedDnsNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludedEmailAddresses")
    def excluded_email_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludedEmailAddresses"))

    @excluded_email_addresses.setter
    def excluded_email_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__065365f26908abe57bfa18317c327e4f0178abeffeba02f1b1230f5fb9ae9151)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludedEmailAddresses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludedIpRanges")
    def excluded_ip_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludedIpRanges"))

    @excluded_ip_ranges.setter
    def excluded_ip_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6bcb89fdabce01762590fb44fe3a320b1984d5a9f775c29ad6de0eed96e865c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludedIpRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludedUris")
    def excluded_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludedUris"))

    @excluded_uris.setter
    def excluded_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebfc55eb0ab5365381ecfe0f8b25a7ce39a27767e6fa41f826bebc6b5b99ca51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludedUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permittedDnsNames")
    def permitted_dns_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "permittedDnsNames"))

    @permitted_dns_names.setter
    def permitted_dns_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5763056d666a4a5166ee978e870439d2df03e99dc84a5bc36ca1a6618f48284f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permittedDnsNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permittedEmailAddresses")
    def permitted_email_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "permittedEmailAddresses"))

    @permitted_email_addresses.setter
    def permitted_email_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a676bbb60e8b462aa79fd53225a1c6171121e1fae1c80ecec7ff1e6e60927044)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permittedEmailAddresses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permittedIpRanges")
    def permitted_ip_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "permittedIpRanges"))

    @permitted_ip_ranges.setter
    def permitted_ip_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe66c1b8f8715dafa4e71b3e345b1169b83bcf7923fe48a55a77c06b3938d6c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permittedIpRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permittedUris")
    def permitted_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "permittedUris"))

    @permitted_uris.setter
    def permitted_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e2184e3f53c170168bcd7054c903b1998dd20d8bcc18409aea1d31716a6368a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permittedUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCaPoolIssuancePolicyBaselineValuesNameConstraints]:
        return typing.cast(typing.Optional[PrivatecaCaPoolIssuancePolicyBaselineValuesNameConstraints], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCaPoolIssuancePolicyBaselineValuesNameConstraints],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85cb532d75ea096d269dbaaab4877c52d61b187a240e6ae01c548f4ff8835c39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PrivatecaCaPoolIssuancePolicyBaselineValuesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCaPool.PrivatecaCaPoolIssuancePolicyBaselineValuesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4b6c802349840d632ef16e488db2bdbc7c9e0eebee3a8b7ba143892aeb83324)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdditionalExtensions")
    def put_additional_extensions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e7d1595b86737b2368cc92a696faed36320d5ed8402eda2cd442cb63627b01a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdditionalExtensions", [value]))

    @jsii.member(jsii_name="putCaOptions")
    def put_ca_options(
        self,
        *,
        is_ca: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_issuer_path_length: typing.Optional[jsii.Number] = None,
        non_ca: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        zero_max_issuer_path_length: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param is_ca: When true, the "CA" in Basic Constraints extension will be set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#is_ca PrivatecaCaPool#is_ca}
        :param max_issuer_path_length: Refers to the "path length constraint" in Basic Constraints extension. For a CA certificate, this value describes the depth of subordinate CA certificates that are allowed. If this value is less than 0, the request will fail. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#max_issuer_path_length PrivatecaCaPool#max_issuer_path_length}
        :param non_ca: When true, the "CA" in Basic Constraints extension will be set to false. If both 'is_ca' and 'non_ca' are unset, the extension will be omitted from the CA certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#non_ca PrivatecaCaPool#non_ca}
        :param zero_max_issuer_path_length: When true, the "path length constraint" in Basic Constraints extension will be set to 0. if both 'max_issuer_path_length' and 'zero_max_issuer_path_length' are unset, the max path length will be omitted from the CA certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#zero_max_issuer_path_length PrivatecaCaPool#zero_max_issuer_path_length}
        '''
        value = PrivatecaCaPoolIssuancePolicyBaselineValuesCaOptions(
            is_ca=is_ca,
            max_issuer_path_length=max_issuer_path_length,
            non_ca=non_ca,
            zero_max_issuer_path_length=zero_max_issuer_path_length,
        )

        return typing.cast(None, jsii.invoke(self, "putCaOptions", [value]))

    @jsii.member(jsii_name="putKeyUsage")
    def put_key_usage(
        self,
        *,
        base_key_usage: typing.Union[PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageBaseKeyUsage, typing.Dict[builtins.str, typing.Any]],
        extended_key_usage: typing.Union[PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageExtendedKeyUsage, typing.Dict[builtins.str, typing.Any]],
        unknown_extended_key_usages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsages, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param base_key_usage: base_key_usage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#base_key_usage PrivatecaCaPool#base_key_usage}
        :param extended_key_usage: extended_key_usage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#extended_key_usage PrivatecaCaPool#extended_key_usage}
        :param unknown_extended_key_usages: unknown_extended_key_usages block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#unknown_extended_key_usages PrivatecaCaPool#unknown_extended_key_usages}
        '''
        value = PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsage(
            base_key_usage=base_key_usage,
            extended_key_usage=extended_key_usage,
            unknown_extended_key_usages=unknown_extended_key_usages,
        )

        return typing.cast(None, jsii.invoke(self, "putKeyUsage", [value]))

    @jsii.member(jsii_name="putNameConstraints")
    def put_name_constraints(
        self,
        *,
        critical: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        excluded_dns_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        excluded_email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        excluded_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        excluded_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        permitted_dns_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        permitted_email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        permitted_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        permitted_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param critical: Indicates whether or not the name constraints are marked critical. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#critical PrivatecaCaPool#critical}
        :param excluded_dns_names: Contains excluded DNS names. Any DNS name that can be constructed by simply adding zero or more labels to the left-hand side of the name satisfies the name constraint. For example, 'example.com', 'www.example.com', 'www.sub.example.com' would satisfy 'example.com' while 'example1.com' does not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#excluded_dns_names PrivatecaCaPool#excluded_dns_names}
        :param excluded_email_addresses: Contains the excluded email addresses. The value can be a particular email address, a hostname to indicate all email addresses on that host or a domain with a leading period (e.g. '.example.com') to indicate all email addresses in that domain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#excluded_email_addresses PrivatecaCaPool#excluded_email_addresses}
        :param excluded_ip_ranges: Contains the excluded IP ranges. For IPv4 addresses, the ranges are expressed using CIDR notation as specified in RFC 4632. For IPv6 addresses, the ranges are expressed in similar encoding as IPv4 addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#excluded_ip_ranges PrivatecaCaPool#excluded_ip_ranges}
        :param excluded_uris: Contains the excluded URIs that apply to the host part of the name. The value can be a hostname or a domain with a leading period (like '.example.com') Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#excluded_uris PrivatecaCaPool#excluded_uris}
        :param permitted_dns_names: Contains permitted DNS names. Any DNS name that can be constructed by simply adding zero or more labels to the left-hand side of the name satisfies the name constraint. For example, 'example.com', 'www.example.com', 'www.sub.example.com' would satisfy 'example.com' while 'example1.com' does not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#permitted_dns_names PrivatecaCaPool#permitted_dns_names}
        :param permitted_email_addresses: Contains the permitted email addresses. The value can be a particular email address, a hostname to indicate all email addresses on that host or a domain with a leading period (e.g. '.example.com') to indicate all email addresses in that domain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#permitted_email_addresses PrivatecaCaPool#permitted_email_addresses}
        :param permitted_ip_ranges: Contains the permitted IP ranges. For IPv4 addresses, the ranges are expressed using CIDR notation as specified in RFC 4632. For IPv6 addresses, the ranges are expressed in similar encoding as IPv4 addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#permitted_ip_ranges PrivatecaCaPool#permitted_ip_ranges}
        :param permitted_uris: Contains the permitted URIs that apply to the host part of the name. The value can be a hostname or a domain with a leading period (like '.example.com') Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#permitted_uris PrivatecaCaPool#permitted_uris}
        '''
        value = PrivatecaCaPoolIssuancePolicyBaselineValuesNameConstraints(
            critical=critical,
            excluded_dns_names=excluded_dns_names,
            excluded_email_addresses=excluded_email_addresses,
            excluded_ip_ranges=excluded_ip_ranges,
            excluded_uris=excluded_uris,
            permitted_dns_names=permitted_dns_names,
            permitted_email_addresses=permitted_email_addresses,
            permitted_ip_ranges=permitted_ip_ranges,
            permitted_uris=permitted_uris,
        )

        return typing.cast(None, jsii.invoke(self, "putNameConstraints", [value]))

    @jsii.member(jsii_name="putPolicyIds")
    def put_policy_ids(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIds", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f832d8bcea667bb2cab589609c5719f06d4db9bff5386e0441a94bc650967a23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPolicyIds", [value]))

    @jsii.member(jsii_name="resetAdditionalExtensions")
    def reset_additional_extensions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalExtensions", []))

    @jsii.member(jsii_name="resetAiaOcspServers")
    def reset_aia_ocsp_servers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAiaOcspServers", []))

    @jsii.member(jsii_name="resetNameConstraints")
    def reset_name_constraints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNameConstraints", []))

    @jsii.member(jsii_name="resetPolicyIds")
    def reset_policy_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyIds", []))

    @builtins.property
    @jsii.member(jsii_name="additionalExtensions")
    def additional_extensions(
        self,
    ) -> PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsList:
        return typing.cast(PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsList, jsii.get(self, "additionalExtensions"))

    @builtins.property
    @jsii.member(jsii_name="caOptions")
    def ca_options(
        self,
    ) -> PrivatecaCaPoolIssuancePolicyBaselineValuesCaOptionsOutputReference:
        return typing.cast(PrivatecaCaPoolIssuancePolicyBaselineValuesCaOptionsOutputReference, jsii.get(self, "caOptions"))

    @builtins.property
    @jsii.member(jsii_name="keyUsage")
    def key_usage(
        self,
    ) -> PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageOutputReference:
        return typing.cast(PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageOutputReference, jsii.get(self, "keyUsage"))

    @builtins.property
    @jsii.member(jsii_name="nameConstraints")
    def name_constraints(
        self,
    ) -> PrivatecaCaPoolIssuancePolicyBaselineValuesNameConstraintsOutputReference:
        return typing.cast(PrivatecaCaPoolIssuancePolicyBaselineValuesNameConstraintsOutputReference, jsii.get(self, "nameConstraints"))

    @builtins.property
    @jsii.member(jsii_name="policyIds")
    def policy_ids(self) -> "PrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIdsList":
        return typing.cast("PrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIdsList", jsii.get(self, "policyIds"))

    @builtins.property
    @jsii.member(jsii_name="additionalExtensionsInput")
    def additional_extensions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensions]]], jsii.get(self, "additionalExtensionsInput"))

    @builtins.property
    @jsii.member(jsii_name="aiaOcspServersInput")
    def aia_ocsp_servers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "aiaOcspServersInput"))

    @builtins.property
    @jsii.member(jsii_name="caOptionsInput")
    def ca_options_input(
        self,
    ) -> typing.Optional[PrivatecaCaPoolIssuancePolicyBaselineValuesCaOptions]:
        return typing.cast(typing.Optional[PrivatecaCaPoolIssuancePolicyBaselineValuesCaOptions], jsii.get(self, "caOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="keyUsageInput")
    def key_usage_input(
        self,
    ) -> typing.Optional[PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsage]:
        return typing.cast(typing.Optional[PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsage], jsii.get(self, "keyUsageInput"))

    @builtins.property
    @jsii.member(jsii_name="nameConstraintsInput")
    def name_constraints_input(
        self,
    ) -> typing.Optional[PrivatecaCaPoolIssuancePolicyBaselineValuesNameConstraints]:
        return typing.cast(typing.Optional[PrivatecaCaPoolIssuancePolicyBaselineValuesNameConstraints], jsii.get(self, "nameConstraintsInput"))

    @builtins.property
    @jsii.member(jsii_name="policyIdsInput")
    def policy_ids_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIds"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIds"]]], jsii.get(self, "policyIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="aiaOcspServers")
    def aia_ocsp_servers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "aiaOcspServers"))

    @aia_ocsp_servers.setter
    def aia_ocsp_servers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f7171ca5a11f259ad0172b00018377be002ee8ba30a8f1e5e22c652912bf3f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aiaOcspServers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCaPoolIssuancePolicyBaselineValues]:
        return typing.cast(typing.Optional[PrivatecaCaPoolIssuancePolicyBaselineValues], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCaPoolIssuancePolicyBaselineValues],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68e43bafef59ba09acd7d43fd77c2c18da69e4fd64800319f48d790c172a9bcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCaPool.PrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIds",
    jsii_struct_bases=[],
    name_mapping={"object_id_path": "objectIdPath"},
)
class PrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIds:
    def __init__(self, *, object_id_path: typing.Sequence[jsii.Number]) -> None:
        '''
        :param object_id_path: An ObjectId specifies an object identifier (OID). These provide context and describe types in ASN.1 messages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#object_id_path PrivatecaCaPool#object_id_path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b8e19e56035105395e381632e61bf34bf55230f35ba3dcb811b928cebbe937e)
            check_type(argname="argument object_id_path", value=object_id_path, expected_type=type_hints["object_id_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object_id_path": object_id_path,
        }

    @builtins.property
    def object_id_path(self) -> typing.List[jsii.Number]:
        '''An ObjectId specifies an object identifier (OID). These provide context and describe types in ASN.1 messages.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#object_id_path PrivatecaCaPool#object_id_path}
        '''
        result = self._values.get("object_id_path")
        assert result is not None, "Required property 'object_id_path' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIdsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCaPool.PrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIdsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b93e264fb18934a20a82c2b7277838dc2f0f0122fc5388bd9bbc9951f4b92d53)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIdsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__130f6d8471e75c41ce8ee53aeb84ec584e7fc31ec3343035608b7f6bebb02d1e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIdsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45153e12b910462c8a8d9b9900e98fa805e7b9f107da5f644f4a96afad135da3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d9cb9a83d708b4ed99ba72e3ba5c19be98a30313840a16bd39504ad2d96d0e1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__077b9447c61864de409a5c235c2cd0a70e0cad2d96dc4bc47cea1d8cd554159f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIds]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIds]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIds]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0feecd116d2ee436736af6571dcc72300ab9d309112c5ec9d60b9b547c1cdef2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIdsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCaPool.PrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIdsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e694e97092676dd204ce7d5a46c8695244ad849eaff6555aafa6e7f6b8d8349c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="objectIdPathInput")
    def object_id_path_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "objectIdPathInput"))

    @builtins.property
    @jsii.member(jsii_name="objectIdPath")
    def object_id_path(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "objectIdPath"))

    @object_id_path.setter
    def object_id_path(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bae63645bee1de77928ace331b64ae839c9618ab0e85e4754e183cae4039a01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectIdPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIds]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIds]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIds]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc45fcb45c9898aaeed6c7c4f7faead1a25da7e56f2736dd4a18c8c139a1fe42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCaPool.PrivatecaCaPoolIssuancePolicyIdentityConstraints",
    jsii_struct_bases=[],
    name_mapping={
        "allow_subject_alt_names_passthrough": "allowSubjectAltNamesPassthrough",
        "allow_subject_passthrough": "allowSubjectPassthrough",
        "cel_expression": "celExpression",
    },
)
class PrivatecaCaPoolIssuancePolicyIdentityConstraints:
    def __init__(
        self,
        *,
        allow_subject_alt_names_passthrough: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        allow_subject_passthrough: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        cel_expression: typing.Optional[typing.Union["PrivatecaCaPoolIssuancePolicyIdentityConstraintsCelExpression", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_subject_alt_names_passthrough: If this is set, the SubjectAltNames extension may be copied from a certificate request into the signed certificate. Otherwise, the requested SubjectAltNames will be discarded. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#allow_subject_alt_names_passthrough PrivatecaCaPool#allow_subject_alt_names_passthrough}
        :param allow_subject_passthrough: If this is set, the Subject field may be copied from a certificate request into the signed certificate. Otherwise, the requested Subject will be discarded. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#allow_subject_passthrough PrivatecaCaPool#allow_subject_passthrough}
        :param cel_expression: cel_expression block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#cel_expression PrivatecaCaPool#cel_expression}
        '''
        if isinstance(cel_expression, dict):
            cel_expression = PrivatecaCaPoolIssuancePolicyIdentityConstraintsCelExpression(**cel_expression)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e358c87df9812b03ad63c20160398472408c170e10ed9bcc1bd61c1d5e211c24)
            check_type(argname="argument allow_subject_alt_names_passthrough", value=allow_subject_alt_names_passthrough, expected_type=type_hints["allow_subject_alt_names_passthrough"])
            check_type(argname="argument allow_subject_passthrough", value=allow_subject_passthrough, expected_type=type_hints["allow_subject_passthrough"])
            check_type(argname="argument cel_expression", value=cel_expression, expected_type=type_hints["cel_expression"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allow_subject_alt_names_passthrough": allow_subject_alt_names_passthrough,
            "allow_subject_passthrough": allow_subject_passthrough,
        }
        if cel_expression is not None:
            self._values["cel_expression"] = cel_expression

    @builtins.property
    def allow_subject_alt_names_passthrough(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''If this is set, the SubjectAltNames extension may be copied from a certificate request into the signed certificate.

        Otherwise, the requested SubjectAltNames will be discarded.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#allow_subject_alt_names_passthrough PrivatecaCaPool#allow_subject_alt_names_passthrough}
        '''
        result = self._values.get("allow_subject_alt_names_passthrough")
        assert result is not None, "Required property 'allow_subject_alt_names_passthrough' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def allow_subject_passthrough(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''If this is set, the Subject field may be copied from a certificate request into the signed certificate.

        Otherwise, the requested Subject will be discarded.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#allow_subject_passthrough PrivatecaCaPool#allow_subject_passthrough}
        '''
        result = self._values.get("allow_subject_passthrough")
        assert result is not None, "Required property 'allow_subject_passthrough' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def cel_expression(
        self,
    ) -> typing.Optional["PrivatecaCaPoolIssuancePolicyIdentityConstraintsCelExpression"]:
        '''cel_expression block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#cel_expression PrivatecaCaPool#cel_expression}
        '''
        result = self._values.get("cel_expression")
        return typing.cast(typing.Optional["PrivatecaCaPoolIssuancePolicyIdentityConstraintsCelExpression"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCaPoolIssuancePolicyIdentityConstraints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCaPool.PrivatecaCaPoolIssuancePolicyIdentityConstraintsCelExpression",
    jsii_struct_bases=[],
    name_mapping={
        "expression": "expression",
        "description": "description",
        "location": "location",
        "title": "title",
    },
)
class PrivatecaCaPoolIssuancePolicyIdentityConstraintsCelExpression:
    def __init__(
        self,
        *,
        expression: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#expression PrivatecaCaPool#expression}
        :param description: Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#description PrivatecaCaPool#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#location PrivatecaCaPool#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#title PrivatecaCaPool#title}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbe533a3c0150a326eef8f7e7d8fcf87b9d3d6959cbe3b8af569406064bc0dd2)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "expression": expression,
        }
        if description is not None:
            self._values["description"] = description
        if location is not None:
            self._values["location"] = location
        if title is not None:
            self._values["title"] = title

    @builtins.property
    def expression(self) -> builtins.str:
        '''Textual representation of an expression in Common Expression Language syntax.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#expression PrivatecaCaPool#expression}
        '''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the expression.

        This is a longer text which describes the expression, e.g. when hovered over it in a UI.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#description PrivatecaCaPool#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''String indicating the location of the expression for error reporting, e.g. a file name and a position in the file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#location PrivatecaCaPool#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#title PrivatecaCaPool#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCaPoolIssuancePolicyIdentityConstraintsCelExpression(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCaPoolIssuancePolicyIdentityConstraintsCelExpressionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCaPool.PrivatecaCaPoolIssuancePolicyIdentityConstraintsCelExpressionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c10e53b693cdd3746b6ff8afb83a830d1f4f9ee7401d980687cef86b14c9659)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetTitle")
    def reset_title(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTitle", []))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="expressionInput")
    def expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expressionInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b1bdcc4dac7f998a63b301e8c2ce4002d35d63b2f82740ec5aeb8b212306474)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a612cf1304c1f098e04454d1bb9694f36d7261346267baed5d42a7e2835bcd8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b32f60209bcde6d00311f741081e2a2d5ce9b8a97968fa03f76a3d626588e060)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3db8353bfb77c1854c41e9a5f1d4b18234c0daebc8be6bc797bf2347fd58abb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCaPoolIssuancePolicyIdentityConstraintsCelExpression]:
        return typing.cast(typing.Optional[PrivatecaCaPoolIssuancePolicyIdentityConstraintsCelExpression], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCaPoolIssuancePolicyIdentityConstraintsCelExpression],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed48abf0df28acf9c4756cbf15399eb085b0720819d169365de4ad7e02af5b85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PrivatecaCaPoolIssuancePolicyIdentityConstraintsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCaPool.PrivatecaCaPoolIssuancePolicyIdentityConstraintsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9dff1ca98fc3497542e49fc5cda769945ae7905a951a7a58c99bdfc4a82db781)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCelExpression")
    def put_cel_expression(
        self,
        *,
        expression: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#expression PrivatecaCaPool#expression}
        :param description: Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#description PrivatecaCaPool#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#location PrivatecaCaPool#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#title PrivatecaCaPool#title}
        '''
        value = PrivatecaCaPoolIssuancePolicyIdentityConstraintsCelExpression(
            expression=expression,
            description=description,
            location=location,
            title=title,
        )

        return typing.cast(None, jsii.invoke(self, "putCelExpression", [value]))

    @jsii.member(jsii_name="resetCelExpression")
    def reset_cel_expression(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCelExpression", []))

    @builtins.property
    @jsii.member(jsii_name="celExpression")
    def cel_expression(
        self,
    ) -> PrivatecaCaPoolIssuancePolicyIdentityConstraintsCelExpressionOutputReference:
        return typing.cast(PrivatecaCaPoolIssuancePolicyIdentityConstraintsCelExpressionOutputReference, jsii.get(self, "celExpression"))

    @builtins.property
    @jsii.member(jsii_name="allowSubjectAltNamesPassthroughInput")
    def allow_subject_alt_names_passthrough_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowSubjectAltNamesPassthroughInput"))

    @builtins.property
    @jsii.member(jsii_name="allowSubjectPassthroughInput")
    def allow_subject_passthrough_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowSubjectPassthroughInput"))

    @builtins.property
    @jsii.member(jsii_name="celExpressionInput")
    def cel_expression_input(
        self,
    ) -> typing.Optional[PrivatecaCaPoolIssuancePolicyIdentityConstraintsCelExpression]:
        return typing.cast(typing.Optional[PrivatecaCaPoolIssuancePolicyIdentityConstraintsCelExpression], jsii.get(self, "celExpressionInput"))

    @builtins.property
    @jsii.member(jsii_name="allowSubjectAltNamesPassthrough")
    def allow_subject_alt_names_passthrough(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowSubjectAltNamesPassthrough"))

    @allow_subject_alt_names_passthrough.setter
    def allow_subject_alt_names_passthrough(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc1c9e53f98e55d9c6e0d5cbf22ba14818725b5f8c7b4651377cfed28ea6d5e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowSubjectAltNamesPassthrough", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowSubjectPassthrough")
    def allow_subject_passthrough(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowSubjectPassthrough"))

    @allow_subject_passthrough.setter
    def allow_subject_passthrough(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e27b26a016909e74298ca1e5f4299b36eecd878ddf855b15a8a7b6833c565133)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowSubjectPassthrough", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCaPoolIssuancePolicyIdentityConstraints]:
        return typing.cast(typing.Optional[PrivatecaCaPoolIssuancePolicyIdentityConstraints], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCaPoolIssuancePolicyIdentityConstraints],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae26188fbdb1ce1f418a4f287d7b0698158a49e6bd56652f28200d64fd9f5a25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PrivatecaCaPoolIssuancePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCaPool.PrivatecaCaPoolIssuancePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__047a023c4afd18c21099a42b18c64d6fc5cd1a2758bf487a4b7813a4d9cd379b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAllowedIssuanceModes")
    def put_allowed_issuance_modes(
        self,
        *,
        allow_config_based_issuance: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        allow_csr_based_issuance: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param allow_config_based_issuance: When true, allows callers to create Certificates by specifying a CertificateConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#allow_config_based_issuance PrivatecaCaPool#allow_config_based_issuance}
        :param allow_csr_based_issuance: When true, allows callers to create Certificates by specifying a CSR. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#allow_csr_based_issuance PrivatecaCaPool#allow_csr_based_issuance}
        '''
        value = PrivatecaCaPoolIssuancePolicyAllowedIssuanceModes(
            allow_config_based_issuance=allow_config_based_issuance,
            allow_csr_based_issuance=allow_csr_based_issuance,
        )

        return typing.cast(None, jsii.invoke(self, "putAllowedIssuanceModes", [value]))

    @jsii.member(jsii_name="putAllowedKeyTypes")
    def put_allowed_key_types(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivatecaCaPoolIssuancePolicyAllowedKeyTypes, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc922aff631e764eb90d96006994b16a55d582df17462f5996fcb4ac24b0e9c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAllowedKeyTypes", [value]))

    @jsii.member(jsii_name="putBaselineValues")
    def put_baseline_values(
        self,
        *,
        ca_options: typing.Union[PrivatecaCaPoolIssuancePolicyBaselineValuesCaOptions, typing.Dict[builtins.str, typing.Any]],
        key_usage: typing.Union[PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsage, typing.Dict[builtins.str, typing.Any]],
        additional_extensions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensions, typing.Dict[builtins.str, typing.Any]]]]] = None,
        aia_ocsp_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
        name_constraints: typing.Optional[typing.Union[PrivatecaCaPoolIssuancePolicyBaselineValuesNameConstraints, typing.Dict[builtins.str, typing.Any]]] = None,
        policy_ids: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIds, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param ca_options: ca_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#ca_options PrivatecaCaPool#ca_options}
        :param key_usage: key_usage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#key_usage PrivatecaCaPool#key_usage}
        :param additional_extensions: additional_extensions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#additional_extensions PrivatecaCaPool#additional_extensions}
        :param aia_ocsp_servers: Describes Online Certificate Status Protocol (OCSP) endpoint addresses that appear in the "Authority Information Access" extension in the certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#aia_ocsp_servers PrivatecaCaPool#aia_ocsp_servers}
        :param name_constraints: name_constraints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#name_constraints PrivatecaCaPool#name_constraints}
        :param policy_ids: policy_ids block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#policy_ids PrivatecaCaPool#policy_ids}
        '''
        value = PrivatecaCaPoolIssuancePolicyBaselineValues(
            ca_options=ca_options,
            key_usage=key_usage,
            additional_extensions=additional_extensions,
            aia_ocsp_servers=aia_ocsp_servers,
            name_constraints=name_constraints,
            policy_ids=policy_ids,
        )

        return typing.cast(None, jsii.invoke(self, "putBaselineValues", [value]))

    @jsii.member(jsii_name="putIdentityConstraints")
    def put_identity_constraints(
        self,
        *,
        allow_subject_alt_names_passthrough: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        allow_subject_passthrough: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        cel_expression: typing.Optional[typing.Union[PrivatecaCaPoolIssuancePolicyIdentityConstraintsCelExpression, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_subject_alt_names_passthrough: If this is set, the SubjectAltNames extension may be copied from a certificate request into the signed certificate. Otherwise, the requested SubjectAltNames will be discarded. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#allow_subject_alt_names_passthrough PrivatecaCaPool#allow_subject_alt_names_passthrough}
        :param allow_subject_passthrough: If this is set, the Subject field may be copied from a certificate request into the signed certificate. Otherwise, the requested Subject will be discarded. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#allow_subject_passthrough PrivatecaCaPool#allow_subject_passthrough}
        :param cel_expression: cel_expression block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#cel_expression PrivatecaCaPool#cel_expression}
        '''
        value = PrivatecaCaPoolIssuancePolicyIdentityConstraints(
            allow_subject_alt_names_passthrough=allow_subject_alt_names_passthrough,
            allow_subject_passthrough=allow_subject_passthrough,
            cel_expression=cel_expression,
        )

        return typing.cast(None, jsii.invoke(self, "putIdentityConstraints", [value]))

    @jsii.member(jsii_name="resetAllowedIssuanceModes")
    def reset_allowed_issuance_modes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedIssuanceModes", []))

    @jsii.member(jsii_name="resetAllowedKeyTypes")
    def reset_allowed_key_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedKeyTypes", []))

    @jsii.member(jsii_name="resetBackdateDuration")
    def reset_backdate_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackdateDuration", []))

    @jsii.member(jsii_name="resetBaselineValues")
    def reset_baseline_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBaselineValues", []))

    @jsii.member(jsii_name="resetIdentityConstraints")
    def reset_identity_constraints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityConstraints", []))

    @jsii.member(jsii_name="resetMaximumLifetime")
    def reset_maximum_lifetime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumLifetime", []))

    @builtins.property
    @jsii.member(jsii_name="allowedIssuanceModes")
    def allowed_issuance_modes(
        self,
    ) -> PrivatecaCaPoolIssuancePolicyAllowedIssuanceModesOutputReference:
        return typing.cast(PrivatecaCaPoolIssuancePolicyAllowedIssuanceModesOutputReference, jsii.get(self, "allowedIssuanceModes"))

    @builtins.property
    @jsii.member(jsii_name="allowedKeyTypes")
    def allowed_key_types(self) -> PrivatecaCaPoolIssuancePolicyAllowedKeyTypesList:
        return typing.cast(PrivatecaCaPoolIssuancePolicyAllowedKeyTypesList, jsii.get(self, "allowedKeyTypes"))

    @builtins.property
    @jsii.member(jsii_name="baselineValues")
    def baseline_values(
        self,
    ) -> PrivatecaCaPoolIssuancePolicyBaselineValuesOutputReference:
        return typing.cast(PrivatecaCaPoolIssuancePolicyBaselineValuesOutputReference, jsii.get(self, "baselineValues"))

    @builtins.property
    @jsii.member(jsii_name="identityConstraints")
    def identity_constraints(
        self,
    ) -> PrivatecaCaPoolIssuancePolicyIdentityConstraintsOutputReference:
        return typing.cast(PrivatecaCaPoolIssuancePolicyIdentityConstraintsOutputReference, jsii.get(self, "identityConstraints"))

    @builtins.property
    @jsii.member(jsii_name="allowedIssuanceModesInput")
    def allowed_issuance_modes_input(
        self,
    ) -> typing.Optional[PrivatecaCaPoolIssuancePolicyAllowedIssuanceModes]:
        return typing.cast(typing.Optional[PrivatecaCaPoolIssuancePolicyAllowedIssuanceModes], jsii.get(self, "allowedIssuanceModesInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedKeyTypesInput")
    def allowed_key_types_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCaPoolIssuancePolicyAllowedKeyTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCaPoolIssuancePolicyAllowedKeyTypes]]], jsii.get(self, "allowedKeyTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="backdateDurationInput")
    def backdate_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "backdateDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="baselineValuesInput")
    def baseline_values_input(
        self,
    ) -> typing.Optional[PrivatecaCaPoolIssuancePolicyBaselineValues]:
        return typing.cast(typing.Optional[PrivatecaCaPoolIssuancePolicyBaselineValues], jsii.get(self, "baselineValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="identityConstraintsInput")
    def identity_constraints_input(
        self,
    ) -> typing.Optional[PrivatecaCaPoolIssuancePolicyIdentityConstraints]:
        return typing.cast(typing.Optional[PrivatecaCaPoolIssuancePolicyIdentityConstraints], jsii.get(self, "identityConstraintsInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumLifetimeInput")
    def maximum_lifetime_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maximumLifetimeInput"))

    @builtins.property
    @jsii.member(jsii_name="backdateDuration")
    def backdate_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backdateDuration"))

    @backdate_duration.setter
    def backdate_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99a1b62a70e7e5c90a5526a221ca0ad81fa1327d11885a9738627c0c29658dc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backdateDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumLifetime")
    def maximum_lifetime(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maximumLifetime"))

    @maximum_lifetime.setter
    def maximum_lifetime(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f8fb3e2c4f6197ef17c45218bdd4b6d07f0d289df005b6b48f360061c767b38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumLifetime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PrivatecaCaPoolIssuancePolicy]:
        return typing.cast(typing.Optional[PrivatecaCaPoolIssuancePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCaPoolIssuancePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0c168b96fc8c6bdf5394c188920e2a57e028dd983d0ceb117be7166fc3f8593)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCaPool.PrivatecaCaPoolPublishingOptions",
    jsii_struct_bases=[],
    name_mapping={
        "publish_ca_cert": "publishCaCert",
        "publish_crl": "publishCrl",
        "encoding_format": "encodingFormat",
    },
)
class PrivatecaCaPoolPublishingOptions:
    def __init__(
        self,
        *,
        publish_ca_cert: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        publish_crl: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        encoding_format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param publish_ca_cert: When true, publishes each CertificateAuthority's CA certificate and includes its URL in the "Authority Information Access" X.509 extension in all issued Certificates. If this is false, the CA certificate will not be published and the corresponding X.509 extension will not be written in issued certificates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#publish_ca_cert PrivatecaCaPool#publish_ca_cert}
        :param publish_crl: When true, publishes each CertificateAuthority's CRL and includes its URL in the "CRL Distribution Points" X.509 extension in all issued Certificates. If this is false, CRLs will not be published and the corresponding X.509 extension will not be written in issued certificates. CRLs will expire 7 days from their creation. However, we will rebuild daily. CRLs are also rebuilt shortly after a certificate is revoked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#publish_crl PrivatecaCaPool#publish_crl}
        :param encoding_format: Specifies the encoding format of each CertificateAuthority's CA certificate and CRLs. If this is omitted, CA certificates and CRLs will be published in PEM. Possible values: ["PEM", "DER"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#encoding_format PrivatecaCaPool#encoding_format}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c11207cf5e72a126804e8296824f387eedcc285e9f6843c6ce94905a02324dc1)
            check_type(argname="argument publish_ca_cert", value=publish_ca_cert, expected_type=type_hints["publish_ca_cert"])
            check_type(argname="argument publish_crl", value=publish_crl, expected_type=type_hints["publish_crl"])
            check_type(argname="argument encoding_format", value=encoding_format, expected_type=type_hints["encoding_format"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "publish_ca_cert": publish_ca_cert,
            "publish_crl": publish_crl,
        }
        if encoding_format is not None:
            self._values["encoding_format"] = encoding_format

    @builtins.property
    def publish_ca_cert(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''When true, publishes each CertificateAuthority's CA certificate and includes its URL in the "Authority Information Access" X.509 extension in all issued Certificates. If this is false, the CA certificate will not be published and the corresponding X.509 extension will not be written in issued certificates.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#publish_ca_cert PrivatecaCaPool#publish_ca_cert}
        '''
        result = self._values.get("publish_ca_cert")
        assert result is not None, "Required property 'publish_ca_cert' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def publish_crl(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''When true, publishes each CertificateAuthority's CRL and includes its URL in the "CRL Distribution Points" X.509 extension in all issued Certificates. If this is false, CRLs will not be published and the corresponding X.509 extension will not be written in issued certificates. CRLs will expire 7 days from their creation. However, we will rebuild daily. CRLs are also rebuilt shortly after a certificate is revoked.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#publish_crl PrivatecaCaPool#publish_crl}
        '''
        result = self._values.get("publish_crl")
        assert result is not None, "Required property 'publish_crl' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def encoding_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the encoding format of each CertificateAuthority's CA certificate and CRLs.

        If this is omitted, CA certificates and CRLs
        will be published in PEM. Possible values: ["PEM", "DER"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#encoding_format PrivatecaCaPool#encoding_format}
        '''
        result = self._values.get("encoding_format")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCaPoolPublishingOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCaPoolPublishingOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCaPool.PrivatecaCaPoolPublishingOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c80e1f128354432ce2d7ecd70052cfa70ff7d0c24d648ce1a32a840bf17e0a1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEncodingFormat")
    def reset_encoding_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncodingFormat", []))

    @builtins.property
    @jsii.member(jsii_name="encodingFormatInput")
    def encoding_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encodingFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="publishCaCertInput")
    def publish_ca_cert_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "publishCaCertInput"))

    @builtins.property
    @jsii.member(jsii_name="publishCrlInput")
    def publish_crl_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "publishCrlInput"))

    @builtins.property
    @jsii.member(jsii_name="encodingFormat")
    def encoding_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encodingFormat"))

    @encoding_format.setter
    def encoding_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac769ec097d0e349423a9cf08782d24f27ad585ab928e619cd40377e2645692d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encodingFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publishCaCert")
    def publish_ca_cert(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "publishCaCert"))

    @publish_ca_cert.setter
    def publish_ca_cert(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f18a5db2e80021a92d7c601bf962db1e411ec3c67434174079ff74b1278d0cea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publishCaCert", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publishCrl")
    def publish_crl(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "publishCrl"))

    @publish_crl.setter
    def publish_crl(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc0c83118fe9978cd070306c4e27aa941b6268e22e62d5279c4e6053eb9e97c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publishCrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PrivatecaCaPoolPublishingOptions]:
        return typing.cast(typing.Optional[PrivatecaCaPoolPublishingOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCaPoolPublishingOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a49bbf5929ee5bcf359ba92c56a959d1ff6b5113eb706cde7d769b78fcc76bfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCaPool.PrivatecaCaPoolTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class PrivatecaCaPoolTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#create PrivatecaCaPool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#delete PrivatecaCaPool#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#update PrivatecaCaPool#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2003a96404e3050b94153f2a73b706d29908fa0e7527b2081fc182765a8e140e)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#create PrivatecaCaPool#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#delete PrivatecaCaPool#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_ca_pool#update PrivatecaCaPool#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCaPoolTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCaPoolTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCaPool.PrivatecaCaPoolTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__08725135db2fbc42b8eabf68839984e66415a30acc3591d00a1c642040f7943a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__008a1a101b0572c2f943a735ecf7d5ca49d0b1c431fc7daeb8695207830be4c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__728eb7007db0a40b2049e06eb8c7af86587ec409cff3b985febc41b69e765d98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8520436ac26d6a2fc6689e4cd68209516627a661204d7627fdf7c146136a4af2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCaPoolTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCaPoolTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCaPoolTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47854280253fcf42e256b48e6b379bdd63340fd6ceff7256c7bb22f02db55d63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "PrivatecaCaPool",
    "PrivatecaCaPoolConfig",
    "PrivatecaCaPoolIssuancePolicy",
    "PrivatecaCaPoolIssuancePolicyAllowedIssuanceModes",
    "PrivatecaCaPoolIssuancePolicyAllowedIssuanceModesOutputReference",
    "PrivatecaCaPoolIssuancePolicyAllowedKeyTypes",
    "PrivatecaCaPoolIssuancePolicyAllowedKeyTypesEllipticCurve",
    "PrivatecaCaPoolIssuancePolicyAllowedKeyTypesEllipticCurveOutputReference",
    "PrivatecaCaPoolIssuancePolicyAllowedKeyTypesList",
    "PrivatecaCaPoolIssuancePolicyAllowedKeyTypesOutputReference",
    "PrivatecaCaPoolIssuancePolicyAllowedKeyTypesRsa",
    "PrivatecaCaPoolIssuancePolicyAllowedKeyTypesRsaOutputReference",
    "PrivatecaCaPoolIssuancePolicyBaselineValues",
    "PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensions",
    "PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsList",
    "PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsObjectId",
    "PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsObjectIdOutputReference",
    "PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsOutputReference",
    "PrivatecaCaPoolIssuancePolicyBaselineValuesCaOptions",
    "PrivatecaCaPoolIssuancePolicyBaselineValuesCaOptionsOutputReference",
    "PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsage",
    "PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageBaseKeyUsage",
    "PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageBaseKeyUsageOutputReference",
    "PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageExtendedKeyUsage",
    "PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageExtendedKeyUsageOutputReference",
    "PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageOutputReference",
    "PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsages",
    "PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsagesList",
    "PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsagesOutputReference",
    "PrivatecaCaPoolIssuancePolicyBaselineValuesNameConstraints",
    "PrivatecaCaPoolIssuancePolicyBaselineValuesNameConstraintsOutputReference",
    "PrivatecaCaPoolIssuancePolicyBaselineValuesOutputReference",
    "PrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIds",
    "PrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIdsList",
    "PrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIdsOutputReference",
    "PrivatecaCaPoolIssuancePolicyIdentityConstraints",
    "PrivatecaCaPoolIssuancePolicyIdentityConstraintsCelExpression",
    "PrivatecaCaPoolIssuancePolicyIdentityConstraintsCelExpressionOutputReference",
    "PrivatecaCaPoolIssuancePolicyIdentityConstraintsOutputReference",
    "PrivatecaCaPoolIssuancePolicyOutputReference",
    "PrivatecaCaPoolPublishingOptions",
    "PrivatecaCaPoolPublishingOptionsOutputReference",
    "PrivatecaCaPoolTimeouts",
    "PrivatecaCaPoolTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__db6ffc6ad50722486da237cc9e4761430dcac0ac3e3cc538706105caa0c5274b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    tier: builtins.str,
    id: typing.Optional[builtins.str] = None,
    issuance_policy: typing.Optional[typing.Union[PrivatecaCaPoolIssuancePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    publishing_options: typing.Optional[typing.Union[PrivatecaCaPoolPublishingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[PrivatecaCaPoolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__bc353b9de9771a9f7af3468b59164cdcf85da0ca3b64b155c4bb375ba7f78615(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c615f86e46c45d946a6303ef13ac36ca7b2a96a8e164465a803cae634c177bc8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96897488896425286df1853bdbff779e00b36a403025242f80cd8fd1f4a4c2e9(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__864451c5c6c455f9a9f81829dcad94177b3a22222483e34724feb430ccb49906(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__361ca9f123742dd7166d21f4cb83f470da453dcaabdb469b92777a6485229798(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03995b1fa3115893e2da34fc277f67f50eb0a0feff6fee2931c89f011e728e6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__448a7d0d52ef406864fd8adab391aa68719ea1772943cc126331fe7013f76a9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6797ca494db177a4f78345de9d686c0c9409ea1366b21bbe4898d21251d37578(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    name: builtins.str,
    tier: builtins.str,
    id: typing.Optional[builtins.str] = None,
    issuance_policy: typing.Optional[typing.Union[PrivatecaCaPoolIssuancePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    publishing_options: typing.Optional[typing.Union[PrivatecaCaPoolPublishingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[PrivatecaCaPoolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c34981f55d89202df2cdff59e35210d6d45f460e3b87bbed180286cbe9c642b1(
    *,
    allowed_issuance_modes: typing.Optional[typing.Union[PrivatecaCaPoolIssuancePolicyAllowedIssuanceModes, typing.Dict[builtins.str, typing.Any]]] = None,
    allowed_key_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivatecaCaPoolIssuancePolicyAllowedKeyTypes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    backdate_duration: typing.Optional[builtins.str] = None,
    baseline_values: typing.Optional[typing.Union[PrivatecaCaPoolIssuancePolicyBaselineValues, typing.Dict[builtins.str, typing.Any]]] = None,
    identity_constraints: typing.Optional[typing.Union[PrivatecaCaPoolIssuancePolicyIdentityConstraints, typing.Dict[builtins.str, typing.Any]]] = None,
    maximum_lifetime: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14c2d7ef77fba497d5afc66c970e461f4e13ab5c60598011e01763ca4c5e4d34(
    *,
    allow_config_based_issuance: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    allow_csr_based_issuance: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c8a631f85467f1a85e3e78fe5436bd30100ec5da356b41309e2d9fa5c9bebba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d7f9c01f530c56bb541dda8590591f0fb1bddf23f7d2e201fe4d295681babb0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bedbd66ba0d2d6b08b21cc60db36cf9216cccf7ec1faebe84be60777516d23a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87cc6e7ed240a3b5f3a7b04b42b8628e278405192d610d056d27392fefa45df6(
    value: typing.Optional[PrivatecaCaPoolIssuancePolicyAllowedIssuanceModes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61ea4a8205502675ebda1063465fd03db70b0363487cd01469bde009cfddd88f(
    *,
    elliptic_curve: typing.Optional[typing.Union[PrivatecaCaPoolIssuancePolicyAllowedKeyTypesEllipticCurve, typing.Dict[builtins.str, typing.Any]]] = None,
    rsa: typing.Optional[typing.Union[PrivatecaCaPoolIssuancePolicyAllowedKeyTypesRsa, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3b7a5f9a80bf962a83840784d468311067a8f6695124f220a0524cf96679711(
    *,
    signature_algorithm: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d30cf8c461f544d11254d1d3ff3aa75577aaa0d8e486a07f10fb4692a47e27f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8ec3c49fe6b8953b190f4b20cb8c3167457a97e71bb8d2a4a418c20d944480f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5078b24a194ae388492d8a6f0848f39429a06447dd61e7afe942fd978c49079(
    value: typing.Optional[PrivatecaCaPoolIssuancePolicyAllowedKeyTypesEllipticCurve],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71ba8a1524de5b72834a99ee5e324aafb04e3f888d7f8ab8cf85e8f457fe3d28(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa30517fc092660b9411cf047c9d5d41ffbfe085624f7f83d3cd5e26fcf62a55(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18fd014757adbfbf7c86271593b0807eb070fb77369ca30c3a581bbd4b5a8a65(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__117c0a3da3caca609dbb7d699ba801bf9f6682fe8b5a6e1a9f742fc437c1e9d2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d680a2f0f44a4ddf05459b972c1ea5f4abb696df68b6b3333748f53fdbb64ee(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bfa5becaef27e1f4f2752b0e0a16d7df67126769f9336a9bdd528e359d3c6c4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCaPoolIssuancePolicyAllowedKeyTypes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30fff330aafdaafbbcd7b0dd9b7c380d004b7afe0628af0ad7f470f7245365d0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fd81a962459134f7693fdd7e8187b5df3b7882b6832ba4f630806fecab344b4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCaPoolIssuancePolicyAllowedKeyTypes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c04325f9ba0d2172dfebc86d266be57602fba64fe8c75004e1b94d0c9975e55c(
    *,
    max_modulus_size: typing.Optional[builtins.str] = None,
    min_modulus_size: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f918b2a71d967e6f6e56867f6bb4064539440d57f261905f73937eea27b3d612(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fa2db75e59d98fe7e08f65d6678cd67616b23ca5839d01c331fcb7b54bbdf7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b15a0b49d2b2c424c089f09d826dc7f0b11c1e51bce63212d24cc4986b05680(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aea21260fdcda85c23d6edb5f8a9b7a0bd87186b38f2d9769f6cb93d4aed71a4(
    value: typing.Optional[PrivatecaCaPoolIssuancePolicyAllowedKeyTypesRsa],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d39365a30de45728b1053e44b0e5636058a8acfe98e7ade410ae5f6d1bb2ae18(
    *,
    ca_options: typing.Union[PrivatecaCaPoolIssuancePolicyBaselineValuesCaOptions, typing.Dict[builtins.str, typing.Any]],
    key_usage: typing.Union[PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsage, typing.Dict[builtins.str, typing.Any]],
    additional_extensions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    aia_ocsp_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
    name_constraints: typing.Optional[typing.Union[PrivatecaCaPoolIssuancePolicyBaselineValuesNameConstraints, typing.Dict[builtins.str, typing.Any]]] = None,
    policy_ids: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIds, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8657478a79939b26d65c5af5888e9e4fddc840ac8a44fd3a0a3f4dd31ac3ac7a(
    *,
    critical: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    object_id: typing.Union[PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsObjectId, typing.Dict[builtins.str, typing.Any]],
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5946fd95c806e8c8320748219d52d4f53b4d2cc933b442d6ea60beb2f1603d49(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66c62f4867c2b992f0bae3727c70657bc944d0587cbe8032d713005aeca759a3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0905a3bfd50bf29403cc8e11f6554921fc5102bdc5b4d2f24c5d17c4192b7c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__188559a6fd7259f427bf1855765e2b7680585d98d6513d224b0e12030351b82c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb0f40760cb9c9ffeaa5e5d408d04630349d7259cc20a6d34681ca7e01b80ea9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28cd72e1563389b54cfaaccecbd10fae59013a96d35aef2809be9202982f4ecc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d437e32b954ac5be4babec809a244dd34878bc4abac73dd3c8667f1a8962ce6(
    *,
    object_id_path: typing.Sequence[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e71f033d162065334610f934ccc705fc28dbeddcfedb51307e0bb2cd58468a04(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d16e23ec3eaa33c11d49f66d6420f1302701cfa202437c0287da68280b8b5b90(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32fb0abfe7de5f22d9decf40e6e7e463bd456dff846083d6da0e242cbefe35d7(
    value: typing.Optional[PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsObjectId],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df76079eb2bd18df362284781d727c0db8320c36e46420721a5ada1d719181b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4fbe73822f980ea26101a0faaa252ad6acc2e726683a391aed4d6a416155369(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1466d6a155b8bf4839053105bb7cb165ea5e5c29b396be0b03adba7315a3490(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42eea13eacfb22a8d88590176e74498312a618e9339567ea8c9336f6299b55d1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d720f20b2e23d63e789f4e593f924c9981f1ea4f267976273533320be3a13f2(
    *,
    is_ca: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    max_issuer_path_length: typing.Optional[jsii.Number] = None,
    non_ca: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    zero_max_issuer_path_length: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__318ac8581bcd0be1def6dc68e19f47ea7e1a76d60127db15f86b00daae4d5af8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc21192ab2a987739f9e554abf683e28f027410ac112fd40462931cb525d8a28(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0332af6191f6f75ab0d30067f1dde29d941fa8f9ff57488e7fb306525b6fe152(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed301db7e00002a2e15db18320d9004a3b54c6d884799301ef198475f8728e41(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02e63cc69ef5447344bab0603f3458683279a32002723b399f7567456cd2d702(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73751c49aee3fc220f5624c1053b093c5ceba3cab27b4836a5253168ab6b9dfa(
    value: typing.Optional[PrivatecaCaPoolIssuancePolicyBaselineValuesCaOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34da08d868bbad98948824da90ff7750e0738e5f25a8554a9648aa2439c58c71(
    *,
    base_key_usage: typing.Union[PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageBaseKeyUsage, typing.Dict[builtins.str, typing.Any]],
    extended_key_usage: typing.Union[PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageExtendedKeyUsage, typing.Dict[builtins.str, typing.Any]],
    unknown_extended_key_usages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsages, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21d272d78e3036f98796c5d27a688a7dd8cd5bb1be520053f0ef700938a6f402(
    *,
    cert_sign: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    content_commitment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    crl_sign: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    data_encipherment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    decipher_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    digital_signature: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encipher_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    key_agreement: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    key_encipherment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00543fe1860e31887682eb8dceabd365c8c8b465a455269ce4322f1896de4b31(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02a2bb1f4dd6c3b410bc4498ba695c2e42314a60bee89f1bfd8996c8c69368b2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fee78c6a9f435de3acf9edf9c29355f784940b9fd3e44ac4c1f4b1ecda16e4f6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0770c4eea9bbd3845a5de8064dbdef989472241956b0c61ac400b5174a6ec532(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79945b92f87a3aad0a926dafc93cec50a8c1876b994f8ab0c1eb4c54401b33bf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a627d2bc983dc3ec8284c2467dbfa8948454d38caa04cdfe66e8864536f9bf9b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__269c215802152b4615a73f3256982ec211e76460de89b4b224985fb65a24748c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dbca81ecea17ba4e87d1651b90e48be582c3c1e8d1bdc4b12663bf51eb4432d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e27896a64bbd63b493afc76dbce805e951fa05611f58416e41bae7783f61f414(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fcd6e35e913188759898fec421dd9b0978c158b59c348a4da9d9bc3fc85eea5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84b3937c3a7a5de2941a9e2c096140138d5015888c81d714b3a949bd433e0066(
    value: typing.Optional[PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageBaseKeyUsage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd9aa2f52ed6f03bb512ae801af7233ed7cc6904fdb8c270166a8c7874e61936(
    *,
    client_auth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    code_signing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    email_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ocsp_signing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    server_auth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    time_stamping: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aad0568f743e8c662b03ea193300c764f14f57e2a82d33006337c6d93f9269b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a37847cd3356e628455b55e452d45a300207c78f4dd51c9eb39f48c9c9ca506(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61e46389385c93acb8beecb7fca8c5caf3e9c579416ac060e3931fb86fe7076e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd7fd9363a71ed7f730198d07c8f1726bd6280426ee94df07fb292f40f7927ed(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a81383e818e764d29c2db0216ad5ced77e95b43426e48b0c7db653ac9c10a84a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0152b0760cacabe01ca64dd573ae20017f3ac911482ef9914b9755beff8b5b27(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d216c5d9fd97c45bbed9e01daff99190456cfd09ee50d45ac80701ff4d6dca35(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c37c9a1d02565a5817928fecbfe9b249d357cef0769f4e1727208528f2c12c2(
    value: typing.Optional[PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageExtendedKeyUsage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__979c3f9c7806d3e462c5273f7f032ee81c774dce044dfdb0fb2bd7d4779c42b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3777050ca072603beb2bcd509a5b7558f69d22083ab3650d275cd1b66d36484(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsages, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4897e1cce7f10dabb4ffa58cc27159134c44304ffed3658728979b5d577b811(
    value: typing.Optional[PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__500f7d68c807fe6815b2925dda14e8203332c3ed14cb4f3f386ff8b23f77d4b2(
    *,
    object_id_path: typing.Sequence[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0edb3822c48e59b859f9e79ab482228a1c6947a4eafc8f90d86f8fae601027ac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7d942ae374ee9fd27b25dd0ff418ac7e047f8133d0306d9663d93502c67c96f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4569617f3916d1542de29f216d2e7edddd320dc3ba5dc2b5378efe803e8f8999(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__906757478437dd3fb01d5c01fc132c90fe777225f6b3e661eb46e4b8453cffb2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7a891f78e207717e80c28c024963b51ee6fc5e138c89c0531fb0dd0aa20a3e5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58a74596b6ef5f25dd6a13511483c204b49043a53db2fadbe87d5da3f8be9e54(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsages]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d70984429689597c37c17901d55e82207d73d786cdf6f141f349c399158b5e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efca8c5e9205e306048b77170985ac69c973d876ae7d50d0c1690bcec71a0e8c(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__998a963444c70207c929a4ec62906dd658feadca11288768ff985361d4077027(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsages]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8289a5563e4508871934f6027d172e923a002b2dbb9d4444d63fcb5ae6456066(
    *,
    critical: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    excluded_dns_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    excluded_email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    excluded_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    excluded_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    permitted_dns_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    permitted_email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    permitted_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    permitted_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9157daeefcacf169493e1c75d6bedbd130f47f76352d378d437a58be1a3858d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e67104e871aabe711ec14bd8c118110bc3d3623b06ae1c5fc6e1419eecb89a11(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e20d462f4608cce41f60d3cf3efb6b703f0e1bcf2b53de32f007ff77802b6af(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__065365f26908abe57bfa18317c327e4f0178abeffeba02f1b1230f5fb9ae9151(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6bcb89fdabce01762590fb44fe3a320b1984d5a9f775c29ad6de0eed96e865c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebfc55eb0ab5365381ecfe0f8b25a7ce39a27767e6fa41f826bebc6b5b99ca51(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5763056d666a4a5166ee978e870439d2df03e99dc84a5bc36ca1a6618f48284f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a676bbb60e8b462aa79fd53225a1c6171121e1fae1c80ecec7ff1e6e60927044(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe66c1b8f8715dafa4e71b3e345b1169b83bcf7923fe48a55a77c06b3938d6c2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e2184e3f53c170168bcd7054c903b1998dd20d8bcc18409aea1d31716a6368a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85cb532d75ea096d269dbaaab4877c52d61b187a240e6ae01c548f4ff8835c39(
    value: typing.Optional[PrivatecaCaPoolIssuancePolicyBaselineValuesNameConstraints],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4b6c802349840d632ef16e488db2bdbc7c9e0eebee3a8b7ba143892aeb83324(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e7d1595b86737b2368cc92a696faed36320d5ed8402eda2cd442cb63627b01a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f832d8bcea667bb2cab589609c5719f06d4db9bff5386e0441a94bc650967a23(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIds, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f7171ca5a11f259ad0172b00018377be002ee8ba30a8f1e5e22c652912bf3f3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68e43bafef59ba09acd7d43fd77c2c18da69e4fd64800319f48d790c172a9bcf(
    value: typing.Optional[PrivatecaCaPoolIssuancePolicyBaselineValues],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b8e19e56035105395e381632e61bf34bf55230f35ba3dcb811b928cebbe937e(
    *,
    object_id_path: typing.Sequence[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b93e264fb18934a20a82c2b7277838dc2f0f0122fc5388bd9bbc9951f4b92d53(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__130f6d8471e75c41ce8ee53aeb84ec584e7fc31ec3343035608b7f6bebb02d1e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45153e12b910462c8a8d9b9900e98fa805e7b9f107da5f644f4a96afad135da3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d9cb9a83d708b4ed99ba72e3ba5c19be98a30313840a16bd39504ad2d96d0e1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__077b9447c61864de409a5c235c2cd0a70e0cad2d96dc4bc47cea1d8cd554159f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0feecd116d2ee436736af6571dcc72300ab9d309112c5ec9d60b9b547c1cdef2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIds]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e694e97092676dd204ce7d5a46c8695244ad849eaff6555aafa6e7f6b8d8349c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bae63645bee1de77928ace331b64ae839c9618ab0e85e4754e183cae4039a01(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc45fcb45c9898aaeed6c7c4f7faead1a25da7e56f2736dd4a18c8c139a1fe42(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIds]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e358c87df9812b03ad63c20160398472408c170e10ed9bcc1bd61c1d5e211c24(
    *,
    allow_subject_alt_names_passthrough: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    allow_subject_passthrough: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    cel_expression: typing.Optional[typing.Union[PrivatecaCaPoolIssuancePolicyIdentityConstraintsCelExpression, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbe533a3c0150a326eef8f7e7d8fcf87b9d3d6959cbe3b8af569406064bc0dd2(
    *,
    expression: builtins.str,
    description: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c10e53b693cdd3746b6ff8afb83a830d1f4f9ee7401d980687cef86b14c9659(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b1bdcc4dac7f998a63b301e8c2ce4002d35d63b2f82740ec5aeb8b212306474(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a612cf1304c1f098e04454d1bb9694f36d7261346267baed5d42a7e2835bcd8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b32f60209bcde6d00311f741081e2a2d5ce9b8a97968fa03f76a3d626588e060(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3db8353bfb77c1854c41e9a5f1d4b18234c0daebc8be6bc797bf2347fd58abb3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed48abf0df28acf9c4756cbf15399eb085b0720819d169365de4ad7e02af5b85(
    value: typing.Optional[PrivatecaCaPoolIssuancePolicyIdentityConstraintsCelExpression],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dff1ca98fc3497542e49fc5cda769945ae7905a951a7a58c99bdfc4a82db781(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc1c9e53f98e55d9c6e0d5cbf22ba14818725b5f8c7b4651377cfed28ea6d5e4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e27b26a016909e74298ca1e5f4299b36eecd878ddf855b15a8a7b6833c565133(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae26188fbdb1ce1f418a4f287d7b0698158a49e6bd56652f28200d64fd9f5a25(
    value: typing.Optional[PrivatecaCaPoolIssuancePolicyIdentityConstraints],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__047a023c4afd18c21099a42b18c64d6fc5cd1a2758bf487a4b7813a4d9cd379b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc922aff631e764eb90d96006994b16a55d582df17462f5996fcb4ac24b0e9c6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivatecaCaPoolIssuancePolicyAllowedKeyTypes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99a1b62a70e7e5c90a5526a221ca0ad81fa1327d11885a9738627c0c29658dc1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f8fb3e2c4f6197ef17c45218bdd4b6d07f0d289df005b6b48f360061c767b38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0c168b96fc8c6bdf5394c188920e2a57e028dd983d0ceb117be7166fc3f8593(
    value: typing.Optional[PrivatecaCaPoolIssuancePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c11207cf5e72a126804e8296824f387eedcc285e9f6843c6ce94905a02324dc1(
    *,
    publish_ca_cert: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    publish_crl: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    encoding_format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c80e1f128354432ce2d7ecd70052cfa70ff7d0c24d648ce1a32a840bf17e0a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac769ec097d0e349423a9cf08782d24f27ad585ab928e619cd40377e2645692d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f18a5db2e80021a92d7c601bf962db1e411ec3c67434174079ff74b1278d0cea(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc0c83118fe9978cd070306c4e27aa941b6268e22e62d5279c4e6053eb9e97c7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a49bbf5929ee5bcf359ba92c56a959d1ff6b5113eb706cde7d769b78fcc76bfd(
    value: typing.Optional[PrivatecaCaPoolPublishingOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2003a96404e3050b94153f2a73b706d29908fa0e7527b2081fc182765a8e140e(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08725135db2fbc42b8eabf68839984e66415a30acc3591d00a1c642040f7943a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__008a1a101b0572c2f943a735ecf7d5ca49d0b1c431fc7daeb8695207830be4c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__728eb7007db0a40b2049e06eb8c7af86587ec409cff3b985febc41b69e765d98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8520436ac26d6a2fc6689e4cd68209516627a661204d7627fdf7c146136a4af2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47854280253fcf42e256b48e6b379bdd63340fd6ceff7256c7bb22f02db55d63(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCaPoolTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
