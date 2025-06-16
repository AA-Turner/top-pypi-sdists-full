r'''
# `google_privateca_ca_pool`

Refer to the Terraform Registry for docs: [`google_privateca_ca_pool`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool).
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


class GooglePrivatecaCaPool(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePrivatecaCaPool.GooglePrivatecaCaPool",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool google_privateca_ca_pool}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        tier: builtins.str,
        id: typing.Optional[builtins.str] = None,
        issuance_policy: typing.Optional[typing.Union["GooglePrivatecaCaPoolIssuancePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        publishing_options: typing.Optional[typing.Union["GooglePrivatecaCaPoolPublishingOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GooglePrivatecaCaPoolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool google_privateca_ca_pool} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Location of the CaPool. A full list of valid locations can be found by running 'gcloud privateca locations list'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#location GooglePrivatecaCaPool#location}
        :param name: The name for this CaPool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#name GooglePrivatecaCaPool#name}
        :param tier: The Tier of this CaPool. Possible values: ["ENTERPRISE", "DEVOPS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#tier GooglePrivatecaCaPool#tier}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#id GooglePrivatecaCaPool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param issuance_policy: issuance_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#issuance_policy GooglePrivatecaCaPool#issuance_policy}
        :param labels: Labels with user-defined metadata. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#labels GooglePrivatecaCaPool#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#project GooglePrivatecaCaPool#project}.
        :param publishing_options: publishing_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#publishing_options GooglePrivatecaCaPool#publishing_options}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#timeouts GooglePrivatecaCaPool#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__085a59c349be0f9ebbae0291ef2d9f5152449ad3c9d6aa231a14493915bea21d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GooglePrivatecaCaPoolConfig(
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
        '''Generates CDKTF code for importing a GooglePrivatecaCaPool resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GooglePrivatecaCaPool to import.
        :param import_from_id: The id of the existing GooglePrivatecaCaPool that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GooglePrivatecaCaPool to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfedca677d2f64c190f036f08a6f9e84664eb667bff843017e6d92a1068b6354)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putIssuancePolicy")
    def put_issuance_policy(
        self,
        *,
        allowed_issuance_modes: typing.Optional[typing.Union["GooglePrivatecaCaPoolIssuancePolicyAllowedIssuanceModes", typing.Dict[builtins.str, typing.Any]]] = None,
        allowed_key_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        backdate_duration: typing.Optional[builtins.str] = None,
        baseline_values: typing.Optional[typing.Union["GooglePrivatecaCaPoolIssuancePolicyBaselineValues", typing.Dict[builtins.str, typing.Any]]] = None,
        identity_constraints: typing.Optional[typing.Union["GooglePrivatecaCaPoolIssuancePolicyIdentityConstraints", typing.Dict[builtins.str, typing.Any]]] = None,
        maximum_lifetime: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allowed_issuance_modes: allowed_issuance_modes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#allowed_issuance_modes GooglePrivatecaCaPool#allowed_issuance_modes}
        :param allowed_key_types: allowed_key_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#allowed_key_types GooglePrivatecaCaPool#allowed_key_types}
        :param backdate_duration: The duration to backdate all certificates issued from this CaPool. If not set, the certificates will be issued with a not_before_time of the issuance time (i.e. the current time). If set, the certificates will be issued with a not_before_time of the issuance time minus the backdate_duration. The not_after_time will be adjusted to preserve the requested lifetime. The backdate_duration must be less than or equal to 48 hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#backdate_duration GooglePrivatecaCaPool#backdate_duration}
        :param baseline_values: baseline_values block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#baseline_values GooglePrivatecaCaPool#baseline_values}
        :param identity_constraints: identity_constraints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#identity_constraints GooglePrivatecaCaPool#identity_constraints}
        :param maximum_lifetime: The maximum lifetime allowed for issued Certificates. Note that if the issuing CertificateAuthority expires before a Certificate's requested maximumLifetime, the effective lifetime will be explicitly truncated to match it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#maximum_lifetime GooglePrivatecaCaPool#maximum_lifetime}
        '''
        value = GooglePrivatecaCaPoolIssuancePolicy(
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
        :param publish_ca_cert: When true, publishes each CertificateAuthority's CA certificate and includes its URL in the "Authority Information Access" X.509 extension in all issued Certificates. If this is false, the CA certificate will not be published and the corresponding X.509 extension will not be written in issued certificates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#publish_ca_cert GooglePrivatecaCaPool#publish_ca_cert}
        :param publish_crl: When true, publishes each CertificateAuthority's CRL and includes its URL in the "CRL Distribution Points" X.509 extension in all issued Certificates. If this is false, CRLs will not be published and the corresponding X.509 extension will not be written in issued certificates. CRLs will expire 7 days from their creation. However, we will rebuild daily. CRLs are also rebuilt shortly after a certificate is revoked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#publish_crl GooglePrivatecaCaPool#publish_crl}
        :param encoding_format: Specifies the encoding format of each CertificateAuthority's CA certificate and CRLs. If this is omitted, CA certificates and CRLs will be published in PEM. Possible values: ["PEM", "DER"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#encoding_format GooglePrivatecaCaPool#encoding_format}
        '''
        value = GooglePrivatecaCaPoolPublishingOptions(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#create GooglePrivatecaCaPool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#delete GooglePrivatecaCaPool#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#update GooglePrivatecaCaPool#update}.
        '''
        value = GooglePrivatecaCaPoolTimeouts(
            create=create, delete=delete, update=update
        )

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
    def issuance_policy(self) -> "GooglePrivatecaCaPoolIssuancePolicyOutputReference":
        return typing.cast("GooglePrivatecaCaPoolIssuancePolicyOutputReference", jsii.get(self, "issuancePolicy"))

    @builtins.property
    @jsii.member(jsii_name="publishingOptions")
    def publishing_options(
        self,
    ) -> "GooglePrivatecaCaPoolPublishingOptionsOutputReference":
        return typing.cast("GooglePrivatecaCaPoolPublishingOptionsOutputReference", jsii.get(self, "publishingOptions"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GooglePrivatecaCaPoolTimeoutsOutputReference":
        return typing.cast("GooglePrivatecaCaPoolTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="issuancePolicyInput")
    def issuance_policy_input(
        self,
    ) -> typing.Optional["GooglePrivatecaCaPoolIssuancePolicy"]:
        return typing.cast(typing.Optional["GooglePrivatecaCaPoolIssuancePolicy"], jsii.get(self, "issuancePolicyInput"))

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
    ) -> typing.Optional["GooglePrivatecaCaPoolPublishingOptions"]:
        return typing.cast(typing.Optional["GooglePrivatecaCaPoolPublishingOptions"], jsii.get(self, "publishingOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="tierInput")
    def tier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tierInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GooglePrivatecaCaPoolTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GooglePrivatecaCaPoolTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeb43b0f48095a786bed060b48ce011eeb7c9b8b711eee8ed332fff244139c74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ced63f440816be0c61738f073515f9ff3af86103471948100dbaec0f9bc1d27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f82dbd7cbc77d5444b42407afa8dc0c9ba39a45bd3bb67d50fb99df64704e54d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aa3da31723a044776044c14396a97359710b8ed147370a9ae799c5256eb91c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdaecba69fef06885b594da2c2af102894acb6533cbf759324ac154de3690d86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tier")
    def tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tier"))

    @tier.setter
    def tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6d03c392cb022ac36aef8ddf83429c679416265929869fe46588b8aa1e9a598)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tier", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePrivatecaCaPool.GooglePrivatecaCaPoolConfig",
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
class GooglePrivatecaCaPoolConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        issuance_policy: typing.Optional[typing.Union["GooglePrivatecaCaPoolIssuancePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        publishing_options: typing.Optional[typing.Union["GooglePrivatecaCaPoolPublishingOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GooglePrivatecaCaPoolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Location of the CaPool. A full list of valid locations can be found by running 'gcloud privateca locations list'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#location GooglePrivatecaCaPool#location}
        :param name: The name for this CaPool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#name GooglePrivatecaCaPool#name}
        :param tier: The Tier of this CaPool. Possible values: ["ENTERPRISE", "DEVOPS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#tier GooglePrivatecaCaPool#tier}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#id GooglePrivatecaCaPool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param issuance_policy: issuance_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#issuance_policy GooglePrivatecaCaPool#issuance_policy}
        :param labels: Labels with user-defined metadata. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#labels GooglePrivatecaCaPool#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#project GooglePrivatecaCaPool#project}.
        :param publishing_options: publishing_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#publishing_options GooglePrivatecaCaPool#publishing_options}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#timeouts GooglePrivatecaCaPool#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(issuance_policy, dict):
            issuance_policy = GooglePrivatecaCaPoolIssuancePolicy(**issuance_policy)
        if isinstance(publishing_options, dict):
            publishing_options = GooglePrivatecaCaPoolPublishingOptions(**publishing_options)
        if isinstance(timeouts, dict):
            timeouts = GooglePrivatecaCaPoolTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0b9ce151835ed0876e1c3b731a91cfd516d4860faabb4c738f1c6873d8f3bb7)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#location GooglePrivatecaCaPool#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name for this CaPool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#name GooglePrivatecaCaPool#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tier(self) -> builtins.str:
        '''The Tier of this CaPool. Possible values: ["ENTERPRISE", "DEVOPS"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#tier GooglePrivatecaCaPool#tier}
        '''
        result = self._values.get("tier")
        assert result is not None, "Required property 'tier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#id GooglePrivatecaCaPool#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def issuance_policy(self) -> typing.Optional["GooglePrivatecaCaPoolIssuancePolicy"]:
        '''issuance_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#issuance_policy GooglePrivatecaCaPool#issuance_policy}
        '''
        result = self._values.get("issuance_policy")
        return typing.cast(typing.Optional["GooglePrivatecaCaPoolIssuancePolicy"], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels with user-defined metadata.

        An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass":
        "1.3kg", "count": "3" }.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#labels GooglePrivatecaCaPool#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#project GooglePrivatecaCaPool#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publishing_options(
        self,
    ) -> typing.Optional["GooglePrivatecaCaPoolPublishingOptions"]:
        '''publishing_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#publishing_options GooglePrivatecaCaPool#publishing_options}
        '''
        result = self._values.get("publishing_options")
        return typing.cast(typing.Optional["GooglePrivatecaCaPoolPublishingOptions"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GooglePrivatecaCaPoolTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#timeouts GooglePrivatecaCaPool#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GooglePrivatecaCaPoolTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePrivatecaCaPoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePrivatecaCaPool.GooglePrivatecaCaPoolIssuancePolicy",
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
class GooglePrivatecaCaPoolIssuancePolicy:
    def __init__(
        self,
        *,
        allowed_issuance_modes: typing.Optional[typing.Union["GooglePrivatecaCaPoolIssuancePolicyAllowedIssuanceModes", typing.Dict[builtins.str, typing.Any]]] = None,
        allowed_key_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        backdate_duration: typing.Optional[builtins.str] = None,
        baseline_values: typing.Optional[typing.Union["GooglePrivatecaCaPoolIssuancePolicyBaselineValues", typing.Dict[builtins.str, typing.Any]]] = None,
        identity_constraints: typing.Optional[typing.Union["GooglePrivatecaCaPoolIssuancePolicyIdentityConstraints", typing.Dict[builtins.str, typing.Any]]] = None,
        maximum_lifetime: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allowed_issuance_modes: allowed_issuance_modes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#allowed_issuance_modes GooglePrivatecaCaPool#allowed_issuance_modes}
        :param allowed_key_types: allowed_key_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#allowed_key_types GooglePrivatecaCaPool#allowed_key_types}
        :param backdate_duration: The duration to backdate all certificates issued from this CaPool. If not set, the certificates will be issued with a not_before_time of the issuance time (i.e. the current time). If set, the certificates will be issued with a not_before_time of the issuance time minus the backdate_duration. The not_after_time will be adjusted to preserve the requested lifetime. The backdate_duration must be less than or equal to 48 hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#backdate_duration GooglePrivatecaCaPool#backdate_duration}
        :param baseline_values: baseline_values block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#baseline_values GooglePrivatecaCaPool#baseline_values}
        :param identity_constraints: identity_constraints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#identity_constraints GooglePrivatecaCaPool#identity_constraints}
        :param maximum_lifetime: The maximum lifetime allowed for issued Certificates. Note that if the issuing CertificateAuthority expires before a Certificate's requested maximumLifetime, the effective lifetime will be explicitly truncated to match it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#maximum_lifetime GooglePrivatecaCaPool#maximum_lifetime}
        '''
        if isinstance(allowed_issuance_modes, dict):
            allowed_issuance_modes = GooglePrivatecaCaPoolIssuancePolicyAllowedIssuanceModes(**allowed_issuance_modes)
        if isinstance(baseline_values, dict):
            baseline_values = GooglePrivatecaCaPoolIssuancePolicyBaselineValues(**baseline_values)
        if isinstance(identity_constraints, dict):
            identity_constraints = GooglePrivatecaCaPoolIssuancePolicyIdentityConstraints(**identity_constraints)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d678d2107965d6379128e969c869f9a701e9cbca28473b6ab22967457fbedd51)
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
    ) -> typing.Optional["GooglePrivatecaCaPoolIssuancePolicyAllowedIssuanceModes"]:
        '''allowed_issuance_modes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#allowed_issuance_modes GooglePrivatecaCaPool#allowed_issuance_modes}
        '''
        result = self._values.get("allowed_issuance_modes")
        return typing.cast(typing.Optional["GooglePrivatecaCaPoolIssuancePolicyAllowedIssuanceModes"], result)

    @builtins.property
    def allowed_key_types(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypes"]]]:
        '''allowed_key_types block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#allowed_key_types GooglePrivatecaCaPool#allowed_key_types}
        '''
        result = self._values.get("allowed_key_types")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypes"]]], result)

    @builtins.property
    def backdate_duration(self) -> typing.Optional[builtins.str]:
        '''The duration to backdate all certificates issued from this CaPool.

        If not set, the
        certificates will be issued with a not_before_time of the issuance time (i.e. the current
        time). If set, the certificates will be issued with a not_before_time of the issuance
        time minus the backdate_duration. The not_after_time will be adjusted to preserve the
        requested lifetime. The backdate_duration must be less than or equal to 48 hours.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#backdate_duration GooglePrivatecaCaPool#backdate_duration}
        '''
        result = self._values.get("backdate_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def baseline_values(
        self,
    ) -> typing.Optional["GooglePrivatecaCaPoolIssuancePolicyBaselineValues"]:
        '''baseline_values block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#baseline_values GooglePrivatecaCaPool#baseline_values}
        '''
        result = self._values.get("baseline_values")
        return typing.cast(typing.Optional["GooglePrivatecaCaPoolIssuancePolicyBaselineValues"], result)

    @builtins.property
    def identity_constraints(
        self,
    ) -> typing.Optional["GooglePrivatecaCaPoolIssuancePolicyIdentityConstraints"]:
        '''identity_constraints block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#identity_constraints GooglePrivatecaCaPool#identity_constraints}
        '''
        result = self._values.get("identity_constraints")
        return typing.cast(typing.Optional["GooglePrivatecaCaPoolIssuancePolicyIdentityConstraints"], result)

    @builtins.property
    def maximum_lifetime(self) -> typing.Optional[builtins.str]:
        '''The maximum lifetime allowed for issued Certificates.

        Note that if the issuing CertificateAuthority
        expires before a Certificate's requested maximumLifetime, the effective lifetime will be explicitly truncated to match it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#maximum_lifetime GooglePrivatecaCaPool#maximum_lifetime}
        '''
        result = self._values.get("maximum_lifetime")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePrivatecaCaPoolIssuancePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePrivatecaCaPool.GooglePrivatecaCaPoolIssuancePolicyAllowedIssuanceModes",
    jsii_struct_bases=[],
    name_mapping={
        "allow_config_based_issuance": "allowConfigBasedIssuance",
        "allow_csr_based_issuance": "allowCsrBasedIssuance",
    },
)
class GooglePrivatecaCaPoolIssuancePolicyAllowedIssuanceModes:
    def __init__(
        self,
        *,
        allow_config_based_issuance: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        allow_csr_based_issuance: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param allow_config_based_issuance: When true, allows callers to create Certificates by specifying a CertificateConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#allow_config_based_issuance GooglePrivatecaCaPool#allow_config_based_issuance}
        :param allow_csr_based_issuance: When true, allows callers to create Certificates by specifying a CSR. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#allow_csr_based_issuance GooglePrivatecaCaPool#allow_csr_based_issuance}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c05d14ffaf38907b3d545f57e2692665accad07c47c1e034e30149dcf694467)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#allow_config_based_issuance GooglePrivatecaCaPool#allow_config_based_issuance}
        '''
        result = self._values.get("allow_config_based_issuance")
        assert result is not None, "Required property 'allow_config_based_issuance' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def allow_csr_based_issuance(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''When true, allows callers to create Certificates by specifying a CSR.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#allow_csr_based_issuance GooglePrivatecaCaPool#allow_csr_based_issuance}
        '''
        result = self._values.get("allow_csr_based_issuance")
        assert result is not None, "Required property 'allow_csr_based_issuance' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePrivatecaCaPoolIssuancePolicyAllowedIssuanceModes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePrivatecaCaPoolIssuancePolicyAllowedIssuanceModesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePrivatecaCaPool.GooglePrivatecaCaPoolIssuancePolicyAllowedIssuanceModesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__93fa3fb49e8589e56721f6e9132d71f0a87e2f248d9874ae66933752e67b869b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9522c3197b8446a945f746f09e93819b6cb3f59c494042a15b2e97fec89a02e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c9b323f755473ba498b2e14aaa17b8df876813fc0c60645129556a7742dda10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowCsrBasedIssuance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GooglePrivatecaCaPoolIssuancePolicyAllowedIssuanceModes]:
        return typing.cast(typing.Optional[GooglePrivatecaCaPoolIssuancePolicyAllowedIssuanceModes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePrivatecaCaPoolIssuancePolicyAllowedIssuanceModes],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab416ce782d20b0822231c2f9c5bd8e73a31288aff66953d14392741ecad4f9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePrivatecaCaPool.GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypes",
    jsii_struct_bases=[],
    name_mapping={"elliptic_curve": "ellipticCurve", "rsa": "rsa"},
)
class GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypes:
    def __init__(
        self,
        *,
        elliptic_curve: typing.Optional[typing.Union["GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesEllipticCurve", typing.Dict[builtins.str, typing.Any]]] = None,
        rsa: typing.Optional[typing.Union["GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesRsa", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param elliptic_curve: elliptic_curve block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#elliptic_curve GooglePrivatecaCaPool#elliptic_curve}
        :param rsa: rsa block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#rsa GooglePrivatecaCaPool#rsa}
        '''
        if isinstance(elliptic_curve, dict):
            elliptic_curve = GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesEllipticCurve(**elliptic_curve)
        if isinstance(rsa, dict):
            rsa = GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesRsa(**rsa)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98bd419020674acaaeb95ecef804e7d8db98ca23f19a9549cf148f7e7ad60406)
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
    ) -> typing.Optional["GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesEllipticCurve"]:
        '''elliptic_curve block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#elliptic_curve GooglePrivatecaCaPool#elliptic_curve}
        '''
        result = self._values.get("elliptic_curve")
        return typing.cast(typing.Optional["GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesEllipticCurve"], result)

    @builtins.property
    def rsa(
        self,
    ) -> typing.Optional["GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesRsa"]:
        '''rsa block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#rsa GooglePrivatecaCaPool#rsa}
        '''
        result = self._values.get("rsa")
        return typing.cast(typing.Optional["GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesRsa"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePrivatecaCaPool.GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesEllipticCurve",
    jsii_struct_bases=[],
    name_mapping={"signature_algorithm": "signatureAlgorithm"},
)
class GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesEllipticCurve:
    def __init__(self, *, signature_algorithm: builtins.str) -> None:
        '''
        :param signature_algorithm: The algorithm used. Possible values: ["ECDSA_P256", "ECDSA_P384", "EDDSA_25519"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#signature_algorithm GooglePrivatecaCaPool#signature_algorithm}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f845af5bb986970d072df619576de75d041365f6dfc687115b42934b8c0cdcb7)
            check_type(argname="argument signature_algorithm", value=signature_algorithm, expected_type=type_hints["signature_algorithm"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "signature_algorithm": signature_algorithm,
        }

    @builtins.property
    def signature_algorithm(self) -> builtins.str:
        '''The algorithm used. Possible values: ["ECDSA_P256", "ECDSA_P384", "EDDSA_25519"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#signature_algorithm GooglePrivatecaCaPool#signature_algorithm}
        '''
        result = self._values.get("signature_algorithm")
        assert result is not None, "Required property 'signature_algorithm' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesEllipticCurve(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesEllipticCurveOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePrivatecaCaPool.GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesEllipticCurveOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9c03f90052a82ecdf34af785879ce54f856e2afdfd07be5cc5664052bb93487)
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
            type_hints = typing.get_type_hints(_typecheckingstub__388e6b8f1bcbc222ece31354cc28804fc243dc808f986565b6beb6df6b8fe3ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signatureAlgorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesEllipticCurve]:
        return typing.cast(typing.Optional[GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesEllipticCurve], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesEllipticCurve],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74cbd4310278cb3940b97aa248ed6f4e01466d356ad51826a14e210bcec565e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePrivatecaCaPool.GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f36226dbe8eac2ec60cf6d8e6bcab57bc9cd95e8742c13016080a04cd85dd3c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2f3d44f9cbb808c1bc31bb28b6bb8df75f8cfcdf62afb16d0d14625b476fadb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6296f611a822c56018f05caded1013230480dbe1904593e242e1abcd034bac72)
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
            type_hints = typing.get_type_hints(_typecheckingstub__78f728ef238e6f216333bbbf1931fbf3511efed7a8a7df1bc3156427b3c7da14)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb73ae6b40b907e3cc8013fd8e3d9b54284518ac419cdde66d7ec2708fe0ad56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52a8e784ab6727ebc79f8e2c060a15af303cc1f6c3df9e1a6e3516ee48f387f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePrivatecaCaPool.GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b89627ef75446618bae38a2374275a079e63c2bdf0fc31040d030dbd0d04282)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEllipticCurve")
    def put_elliptic_curve(self, *, signature_algorithm: builtins.str) -> None:
        '''
        :param signature_algorithm: The algorithm used. Possible values: ["ECDSA_P256", "ECDSA_P384", "EDDSA_25519"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#signature_algorithm GooglePrivatecaCaPool#signature_algorithm}
        '''
        value = GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesEllipticCurve(
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
        :param max_modulus_size: The maximum allowed RSA modulus size, in bits. If this is not set, or if set to zero, the service will not enforce an explicit upper bound on RSA modulus sizes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#max_modulus_size GooglePrivatecaCaPool#max_modulus_size}
        :param min_modulus_size: The minimum allowed RSA modulus size, in bits. If this is not set, or if set to zero, the service-level min RSA modulus size will continue to apply. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#min_modulus_size GooglePrivatecaCaPool#min_modulus_size}
        '''
        value = GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesRsa(
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
    ) -> GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesEllipticCurveOutputReference:
        return typing.cast(GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesEllipticCurveOutputReference, jsii.get(self, "ellipticCurve"))

    @builtins.property
    @jsii.member(jsii_name="rsa")
    def rsa(
        self,
    ) -> "GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesRsaOutputReference":
        return typing.cast("GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesRsaOutputReference", jsii.get(self, "rsa"))

    @builtins.property
    @jsii.member(jsii_name="ellipticCurveInput")
    def elliptic_curve_input(
        self,
    ) -> typing.Optional[GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesEllipticCurve]:
        return typing.cast(typing.Optional[GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesEllipticCurve], jsii.get(self, "ellipticCurveInput"))

    @builtins.property
    @jsii.member(jsii_name="rsaInput")
    def rsa_input(
        self,
    ) -> typing.Optional["GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesRsa"]:
        return typing.cast(typing.Optional["GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesRsa"], jsii.get(self, "rsaInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8938a0435a21e263a93dc69ac485fc0fd301886439d37f4cb601efffe3336632)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePrivatecaCaPool.GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesRsa",
    jsii_struct_bases=[],
    name_mapping={
        "max_modulus_size": "maxModulusSize",
        "min_modulus_size": "minModulusSize",
    },
)
class GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesRsa:
    def __init__(
        self,
        *,
        max_modulus_size: typing.Optional[builtins.str] = None,
        min_modulus_size: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_modulus_size: The maximum allowed RSA modulus size, in bits. If this is not set, or if set to zero, the service will not enforce an explicit upper bound on RSA modulus sizes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#max_modulus_size GooglePrivatecaCaPool#max_modulus_size}
        :param min_modulus_size: The minimum allowed RSA modulus size, in bits. If this is not set, or if set to zero, the service-level min RSA modulus size will continue to apply. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#min_modulus_size GooglePrivatecaCaPool#min_modulus_size}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eb99b06d1d4b180e74e62a4b4e7d0fd3e178e6a7c9de8aaf35e0f8008db0715)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#max_modulus_size GooglePrivatecaCaPool#max_modulus_size}
        '''
        result = self._values.get("max_modulus_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_modulus_size(self) -> typing.Optional[builtins.str]:
        '''The minimum allowed RSA modulus size, in bits.

        If this is not set, or if set to zero, the
        service-level min RSA modulus size will continue to apply.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#min_modulus_size GooglePrivatecaCaPool#min_modulus_size}
        '''
        result = self._values.get("min_modulus_size")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesRsa(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesRsaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePrivatecaCaPool.GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesRsaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3ee1c24cb7ccaa5c9a6fd997061f5a2641842d7c2ce22388d6746aa8d490216)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f38f516acf5991b7a2aa5660706001f0c5b6c9545333b8bd8c025ed28a95295)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxModulusSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minModulusSize")
    def min_modulus_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minModulusSize"))

    @min_modulus_size.setter
    def min_modulus_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea6d7b763106bad725fb3ef8f12c764b2ee6cdfecafecc8970fab828edf82da9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minModulusSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesRsa]:
        return typing.cast(typing.Optional[GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesRsa], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesRsa],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a364d69ec9e8a5e5fbb9717d6722bdf46303d9f189446afbdc8eb034cd586438)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePrivatecaCaPool.GooglePrivatecaCaPoolIssuancePolicyBaselineValues",
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
class GooglePrivatecaCaPoolIssuancePolicyBaselineValues:
    def __init__(
        self,
        *,
        ca_options: typing.Union["GooglePrivatecaCaPoolIssuancePolicyBaselineValuesCaOptions", typing.Dict[builtins.str, typing.Any]],
        key_usage: typing.Union["GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsage", typing.Dict[builtins.str, typing.Any]],
        additional_extensions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        aia_ocsp_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
        name_constraints: typing.Optional[typing.Union["GooglePrivatecaCaPoolIssuancePolicyBaselineValuesNameConstraints", typing.Dict[builtins.str, typing.Any]]] = None,
        policy_ids: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GooglePrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIds", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param ca_options: ca_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#ca_options GooglePrivatecaCaPool#ca_options}
        :param key_usage: key_usage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#key_usage GooglePrivatecaCaPool#key_usage}
        :param additional_extensions: additional_extensions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#additional_extensions GooglePrivatecaCaPool#additional_extensions}
        :param aia_ocsp_servers: Describes Online Certificate Status Protocol (OCSP) endpoint addresses that appear in the "Authority Information Access" extension in the certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#aia_ocsp_servers GooglePrivatecaCaPool#aia_ocsp_servers}
        :param name_constraints: name_constraints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#name_constraints GooglePrivatecaCaPool#name_constraints}
        :param policy_ids: policy_ids block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#policy_ids GooglePrivatecaCaPool#policy_ids}
        '''
        if isinstance(ca_options, dict):
            ca_options = GooglePrivatecaCaPoolIssuancePolicyBaselineValuesCaOptions(**ca_options)
        if isinstance(key_usage, dict):
            key_usage = GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsage(**key_usage)
        if isinstance(name_constraints, dict):
            name_constraints = GooglePrivatecaCaPoolIssuancePolicyBaselineValuesNameConstraints(**name_constraints)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e4b51ba5ad121aebba598f9e79150f752fd027d300e1edd132e91e45544ac1f)
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
    def ca_options(
        self,
    ) -> "GooglePrivatecaCaPoolIssuancePolicyBaselineValuesCaOptions":
        '''ca_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#ca_options GooglePrivatecaCaPool#ca_options}
        '''
        result = self._values.get("ca_options")
        assert result is not None, "Required property 'ca_options' is missing"
        return typing.cast("GooglePrivatecaCaPoolIssuancePolicyBaselineValuesCaOptions", result)

    @builtins.property
    def key_usage(self) -> "GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsage":
        '''key_usage block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#key_usage GooglePrivatecaCaPool#key_usage}
        '''
        result = self._values.get("key_usage")
        assert result is not None, "Required property 'key_usage' is missing"
        return typing.cast("GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsage", result)

    @builtins.property
    def additional_extensions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensions"]]]:
        '''additional_extensions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#additional_extensions GooglePrivatecaCaPool#additional_extensions}
        '''
        result = self._values.get("additional_extensions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensions"]]], result)

    @builtins.property
    def aia_ocsp_servers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Describes Online Certificate Status Protocol (OCSP) endpoint addresses that appear in the "Authority Information Access" extension in the certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#aia_ocsp_servers GooglePrivatecaCaPool#aia_ocsp_servers}
        '''
        result = self._values.get("aia_ocsp_servers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name_constraints(
        self,
    ) -> typing.Optional["GooglePrivatecaCaPoolIssuancePolicyBaselineValuesNameConstraints"]:
        '''name_constraints block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#name_constraints GooglePrivatecaCaPool#name_constraints}
        '''
        result = self._values.get("name_constraints")
        return typing.cast(typing.Optional["GooglePrivatecaCaPoolIssuancePolicyBaselineValuesNameConstraints"], result)

    @builtins.property
    def policy_ids(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GooglePrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIds"]]]:
        '''policy_ids block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#policy_ids GooglePrivatecaCaPool#policy_ids}
        '''
        result = self._values.get("policy_ids")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GooglePrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIds"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePrivatecaCaPoolIssuancePolicyBaselineValues(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePrivatecaCaPool.GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensions",
    jsii_struct_bases=[],
    name_mapping={"critical": "critical", "object_id": "objectId", "value": "value"},
)
class GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensions:
    def __init__(
        self,
        *,
        critical: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        object_id: typing.Union["GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsObjectId", typing.Dict[builtins.str, typing.Any]],
        value: builtins.str,
    ) -> None:
        '''
        :param critical: Indicates whether or not this extension is critical (i.e., if the client does not know how to handle this extension, the client should consider this to be an error). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#critical GooglePrivatecaCaPool#critical}
        :param object_id: object_id block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#object_id GooglePrivatecaCaPool#object_id}
        :param value: The value of this X.509 extension. A base64-encoded string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#value GooglePrivatecaCaPool#value}
        '''
        if isinstance(object_id, dict):
            object_id = GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsObjectId(**object_id)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a190eaf4b3e14cdd220d2accfa9b1814061e97d03c898265103b2e91864d4094)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#critical GooglePrivatecaCaPool#critical}
        '''
        result = self._values.get("critical")
        assert result is not None, "Required property 'critical' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def object_id(
        self,
    ) -> "GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsObjectId":
        '''object_id block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#object_id GooglePrivatecaCaPool#object_id}
        '''
        result = self._values.get("object_id")
        assert result is not None, "Required property 'object_id' is missing"
        return typing.cast("GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsObjectId", result)

    @builtins.property
    def value(self) -> builtins.str:
        '''The value of this X.509 extension. A base64-encoded string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#value GooglePrivatecaCaPool#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePrivatecaCaPool.GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1ab10cdd74d6bd4be726224d011ebee7b357b19eaac01a6634d85bf749df323)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d759d7fd3e4fb53f41e3c9c3e1378cac9b9e2dbbbf7d07d86517fd805db97fd4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ebe6337a1aa12135f7a3fcd0a13606ad28ae2248512b60a34417606c765b36f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1604c1ff0984dcf2523db2716b34bc24b066f9c09c8c218e5e184751986ead05)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2cda4347ab82f78dee075038c975049eb8b97385c2cb2dbf08f4b7174fdd5215)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b87fb0e44bda422991b449542c3309b31349847f064c6207d139c074c264e6b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePrivatecaCaPool.GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsObjectId",
    jsii_struct_bases=[],
    name_mapping={"object_id_path": "objectIdPath"},
)
class GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsObjectId:
    def __init__(self, *, object_id_path: typing.Sequence[jsii.Number]) -> None:
        '''
        :param object_id_path: An ObjectId specifies an object identifier (OID). These provide context and describe types in ASN.1 messages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#object_id_path GooglePrivatecaCaPool#object_id_path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd7979f7454acb0062773b99241e65f690bb2f9e76429fa67e421944bbefe7ab)
            check_type(argname="argument object_id_path", value=object_id_path, expected_type=type_hints["object_id_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object_id_path": object_id_path,
        }

    @builtins.property
    def object_id_path(self) -> typing.List[jsii.Number]:
        '''An ObjectId specifies an object identifier (OID). These provide context and describe types in ASN.1 messages.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#object_id_path GooglePrivatecaCaPool#object_id_path}
        '''
        result = self._values.get("object_id_path")
        assert result is not None, "Required property 'object_id_path' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsObjectId(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsObjectIdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePrivatecaCaPool.GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsObjectIdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a984453b5cf29bedaf5042320f29bad5634c4c19e4085b6ec07f970f46281796)
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
            type_hints = typing.get_type_hints(_typecheckingstub__62c1bb59c4d21ed808befd3327af99710489d0259d5e897e2f6fa31388007325)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectIdPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsObjectId]:
        return typing.cast(typing.Optional[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsObjectId], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsObjectId],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76d4470a89193677c51141175f7daf8e32835978010e70ac932a8a18971bf499)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePrivatecaCaPool.GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__89850d95b721c39373887c253ef8848d0643562f92cab2fb1d2e5cad07b951fc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putObjectId")
    def put_object_id(self, *, object_id_path: typing.Sequence[jsii.Number]) -> None:
        '''
        :param object_id_path: An ObjectId specifies an object identifier (OID). These provide context and describe types in ASN.1 messages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#object_id_path GooglePrivatecaCaPool#object_id_path}
        '''
        value = GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsObjectId(
            object_id_path=object_id_path
        )

        return typing.cast(None, jsii.invoke(self, "putObjectId", [value]))

    @builtins.property
    @jsii.member(jsii_name="objectId")
    def object_id(
        self,
    ) -> GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsObjectIdOutputReference:
        return typing.cast(GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsObjectIdOutputReference, jsii.get(self, "objectId"))

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
    ) -> typing.Optional[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsObjectId]:
        return typing.cast(typing.Optional[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsObjectId], jsii.get(self, "objectIdInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__64809fcbe298f405b306a8c6f4bf5f149485d221cb02a0bc27b567996ab6d7e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "critical", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b36c01d3e523739c6cf6e49dcf615de0ba9f758083ea8216a6b034e1bb864b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c2e08ad02ad1b8ec185665934ab4f35a1ba0029df9e0dff754efa39ae03a2f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePrivatecaCaPool.GooglePrivatecaCaPoolIssuancePolicyBaselineValuesCaOptions",
    jsii_struct_bases=[],
    name_mapping={
        "is_ca": "isCa",
        "max_issuer_path_length": "maxIssuerPathLength",
        "non_ca": "nonCa",
        "zero_max_issuer_path_length": "zeroMaxIssuerPathLength",
    },
)
class GooglePrivatecaCaPoolIssuancePolicyBaselineValuesCaOptions:
    def __init__(
        self,
        *,
        is_ca: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_issuer_path_length: typing.Optional[jsii.Number] = None,
        non_ca: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        zero_max_issuer_path_length: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param is_ca: When true, the "CA" in Basic Constraints extension will be set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#is_ca GooglePrivatecaCaPool#is_ca}
        :param max_issuer_path_length: Refers to the "path length constraint" in Basic Constraints extension. For a CA certificate, this value describes the depth of subordinate CA certificates that are allowed. If this value is less than 0, the request will fail. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#max_issuer_path_length GooglePrivatecaCaPool#max_issuer_path_length}
        :param non_ca: When true, the "CA" in Basic Constraints extension will be set to false. If both 'is_ca' and 'non_ca' are unset, the extension will be omitted from the CA certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#non_ca GooglePrivatecaCaPool#non_ca}
        :param zero_max_issuer_path_length: When true, the "path length constraint" in Basic Constraints extension will be set to 0. if both 'max_issuer_path_length' and 'zero_max_issuer_path_length' are unset, the max path length will be omitted from the CA certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#zero_max_issuer_path_length GooglePrivatecaCaPool#zero_max_issuer_path_length}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24a27556b1a1603b29fb2b6cd2b9a47038f069de130abede38be2defba360dbd)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#is_ca GooglePrivatecaCaPool#is_ca}
        '''
        result = self._values.get("is_ca")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def max_issuer_path_length(self) -> typing.Optional[jsii.Number]:
        '''Refers to the "path length constraint" in Basic Constraints extension.

        For a CA certificate, this value describes the depth of
        subordinate CA certificates that are allowed. If this value is less than 0, the request will fail.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#max_issuer_path_length GooglePrivatecaCaPool#max_issuer_path_length}
        '''
        result = self._values.get("max_issuer_path_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def non_ca(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When true, the "CA" in Basic Constraints extension will be set to false.

        If both 'is_ca' and 'non_ca' are unset, the extension will be omitted from the CA certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#non_ca GooglePrivatecaCaPool#non_ca}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#zero_max_issuer_path_length GooglePrivatecaCaPool#zero_max_issuer_path_length}
        '''
        result = self._values.get("zero_max_issuer_path_length")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePrivatecaCaPoolIssuancePolicyBaselineValuesCaOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePrivatecaCaPoolIssuancePolicyBaselineValuesCaOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePrivatecaCaPool.GooglePrivatecaCaPoolIssuancePolicyBaselineValuesCaOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8fe9a409e68f12e9a1ac5bc71e5eee41f155073547ee66c1951710873511b0a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8fb1b75a0e9de67a9987b7a76421fa49ea701824d40cf7c0707f8b0bc4b1e54e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isCa", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxIssuerPathLength")
    def max_issuer_path_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxIssuerPathLength"))

    @max_issuer_path_length.setter
    def max_issuer_path_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f440decfc106bb84baa93d0f68ae8ddd789be1fbce96445e877946a6491a79b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__da20546ba52912b7c8add7a07efaa00ba253a5551b85c954819cee6e09e5b9fa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__caa30e8a3686fda3c8d39914bfeed0ae4d72321f5927ac13e27cd5e3e2a22b3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zeroMaxIssuerPathLength", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesCaOptions]:
        return typing.cast(typing.Optional[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesCaOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesCaOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be556fa913baac4c5fe27b110c627e23aae8f0803e95b8257a1837dcf46b1da3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePrivatecaCaPool.GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsage",
    jsii_struct_bases=[],
    name_mapping={
        "base_key_usage": "baseKeyUsage",
        "extended_key_usage": "extendedKeyUsage",
        "unknown_extended_key_usages": "unknownExtendedKeyUsages",
    },
)
class GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsage:
    def __init__(
        self,
        *,
        base_key_usage: typing.Union["GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageBaseKeyUsage", typing.Dict[builtins.str, typing.Any]],
        extended_key_usage: typing.Union["GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageExtendedKeyUsage", typing.Dict[builtins.str, typing.Any]],
        unknown_extended_key_usages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsages", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param base_key_usage: base_key_usage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#base_key_usage GooglePrivatecaCaPool#base_key_usage}
        :param extended_key_usage: extended_key_usage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#extended_key_usage GooglePrivatecaCaPool#extended_key_usage}
        :param unknown_extended_key_usages: unknown_extended_key_usages block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#unknown_extended_key_usages GooglePrivatecaCaPool#unknown_extended_key_usages}
        '''
        if isinstance(base_key_usage, dict):
            base_key_usage = GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageBaseKeyUsage(**base_key_usage)
        if isinstance(extended_key_usage, dict):
            extended_key_usage = GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageExtendedKeyUsage(**extended_key_usage)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54a9f207be1d91ca90db067e6c2eb21d2ff4280d51e812ec410a066dd77b3bac)
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
    ) -> "GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageBaseKeyUsage":
        '''base_key_usage block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#base_key_usage GooglePrivatecaCaPool#base_key_usage}
        '''
        result = self._values.get("base_key_usage")
        assert result is not None, "Required property 'base_key_usage' is missing"
        return typing.cast("GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageBaseKeyUsage", result)

    @builtins.property
    def extended_key_usage(
        self,
    ) -> "GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageExtendedKeyUsage":
        '''extended_key_usage block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#extended_key_usage GooglePrivatecaCaPool#extended_key_usage}
        '''
        result = self._values.get("extended_key_usage")
        assert result is not None, "Required property 'extended_key_usage' is missing"
        return typing.cast("GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageExtendedKeyUsage", result)

    @builtins.property
    def unknown_extended_key_usages(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsages"]]]:
        '''unknown_extended_key_usages block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#unknown_extended_key_usages GooglePrivatecaCaPool#unknown_extended_key_usages}
        '''
        result = self._values.get("unknown_extended_key_usages")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsages"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePrivatecaCaPool.GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageBaseKeyUsage",
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
class GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageBaseKeyUsage:
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
        :param cert_sign: The key may be used to sign certificates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#cert_sign GooglePrivatecaCaPool#cert_sign}
        :param content_commitment: The key may be used for cryptographic commitments. Note that this may also be referred to as "non-repudiation". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#content_commitment GooglePrivatecaCaPool#content_commitment}
        :param crl_sign: The key may be used sign certificate revocation lists. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#crl_sign GooglePrivatecaCaPool#crl_sign}
        :param data_encipherment: The key may be used to encipher data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#data_encipherment GooglePrivatecaCaPool#data_encipherment}
        :param decipher_only: The key may be used to decipher only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#decipher_only GooglePrivatecaCaPool#decipher_only}
        :param digital_signature: The key may be used for digital signatures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#digital_signature GooglePrivatecaCaPool#digital_signature}
        :param encipher_only: The key may be used to encipher only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#encipher_only GooglePrivatecaCaPool#encipher_only}
        :param key_agreement: The key may be used in a key agreement protocol. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#key_agreement GooglePrivatecaCaPool#key_agreement}
        :param key_encipherment: The key may be used to encipher other keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#key_encipherment GooglePrivatecaCaPool#key_encipherment}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54f550f8c0e0e5946ed62f6bee38df14d848a8dc7336496c927caf8d016efd32)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#cert_sign GooglePrivatecaCaPool#cert_sign}
        '''
        result = self._values.get("cert_sign")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def content_commitment(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The key may be used for cryptographic commitments. Note that this may also be referred to as "non-repudiation".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#content_commitment GooglePrivatecaCaPool#content_commitment}
        '''
        result = self._values.get("content_commitment")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def crl_sign(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The key may be used sign certificate revocation lists.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#crl_sign GooglePrivatecaCaPool#crl_sign}
        '''
        result = self._values.get("crl_sign")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def data_encipherment(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The key may be used to encipher data.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#data_encipherment GooglePrivatecaCaPool#data_encipherment}
        '''
        result = self._values.get("data_encipherment")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def decipher_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The key may be used to decipher only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#decipher_only GooglePrivatecaCaPool#decipher_only}
        '''
        result = self._values.get("decipher_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def digital_signature(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The key may be used for digital signatures.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#digital_signature GooglePrivatecaCaPool#digital_signature}
        '''
        result = self._values.get("digital_signature")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encipher_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The key may be used to encipher only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#encipher_only GooglePrivatecaCaPool#encipher_only}
        '''
        result = self._values.get("encipher_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def key_agreement(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The key may be used in a key agreement protocol.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#key_agreement GooglePrivatecaCaPool#key_agreement}
        '''
        result = self._values.get("key_agreement")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def key_encipherment(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The key may be used to encipher other keys.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#key_encipherment GooglePrivatecaCaPool#key_encipherment}
        '''
        result = self._values.get("key_encipherment")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageBaseKeyUsage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageBaseKeyUsageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePrivatecaCaPool.GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageBaseKeyUsageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__603b3333b32bac61c10c691971e993fded7dd566f7283e9323570cba880d3d02)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb979fc464a7934a0feadaa85fdf0a01b9983a399830662210f747be75174e0e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__50f7cd0499892b9f42508b5af5b3a9e41be63ba383d09a8ae7e01db82934f36b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__df8449aef674d0e19106b0915fe326538a3002efd2cfa0e7346e3467799c8735)
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
            type_hints = typing.get_type_hints(_typecheckingstub__55f523c246e0f2860040c8fe5946f15513ddd6d81b69bc99a5e0331bd626c997)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3bd10b418916e515bff73c94d78fed61bbbfe63c2a8fdba7e9dbb256e9f8e761)
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
            type_hints = typing.get_type_hints(_typecheckingstub__00ff234d6afc61e580b9cd84bf76594b45a33713f649bc91f8766b58862e902a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f524bdc368aa26eee2cdd161dfa15290f15943770989cca90f5af33d0a0ede7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f84bc4d01e20603da0a86ded70085912f15977a53186bccdbcf3348ab3568a5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9066c0ee0b86bce4238ef9dea05e8aefa3202a724ed05803b4d4c2d1b73671f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyEncipherment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageBaseKeyUsage]:
        return typing.cast(typing.Optional[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageBaseKeyUsage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageBaseKeyUsage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe75e6d24ad58cde66bc0d1286885bc9d3c92aeb516aec2a1e5dd3111ae63768)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePrivatecaCaPool.GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageExtendedKeyUsage",
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
class GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageExtendedKeyUsage:
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
        :param client_auth: Corresponds to OID 1.3.6.1.5.5.7.3.2. Officially described as "TLS WWW client authentication", though regularly used for non-WWW TLS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#client_auth GooglePrivatecaCaPool#client_auth}
        :param code_signing: Corresponds to OID 1.3.6.1.5.5.7.3.3. Officially described as "Signing of downloadable executable code client authentication". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#code_signing GooglePrivatecaCaPool#code_signing}
        :param email_protection: Corresponds to OID 1.3.6.1.5.5.7.3.4. Officially described as "Email protection". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#email_protection GooglePrivatecaCaPool#email_protection}
        :param ocsp_signing: Corresponds to OID 1.3.6.1.5.5.7.3.9. Officially described as "Signing OCSP responses". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#ocsp_signing GooglePrivatecaCaPool#ocsp_signing}
        :param server_auth: Corresponds to OID 1.3.6.1.5.5.7.3.1. Officially described as "TLS WWW server authentication", though regularly used for non-WWW TLS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#server_auth GooglePrivatecaCaPool#server_auth}
        :param time_stamping: Corresponds to OID 1.3.6.1.5.5.7.3.8. Officially described as "Binding the hash of an object to a time". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#time_stamping GooglePrivatecaCaPool#time_stamping}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8377bc2150c99140c4d27fb2a7c4ab90c63f0d4c87c3837b1d8a1fb709385fa6)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#client_auth GooglePrivatecaCaPool#client_auth}
        '''
        result = self._values.get("client_auth")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def code_signing(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Corresponds to OID 1.3.6.1.5.5.7.3.3. Officially described as "Signing of downloadable executable code client authentication".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#code_signing GooglePrivatecaCaPool#code_signing}
        '''
        result = self._values.get("code_signing")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def email_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Corresponds to OID 1.3.6.1.5.5.7.3.4. Officially described as "Email protection".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#email_protection GooglePrivatecaCaPool#email_protection}
        '''
        result = self._values.get("email_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ocsp_signing(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Corresponds to OID 1.3.6.1.5.5.7.3.9. Officially described as "Signing OCSP responses".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#ocsp_signing GooglePrivatecaCaPool#ocsp_signing}
        '''
        result = self._values.get("ocsp_signing")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def server_auth(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Corresponds to OID 1.3.6.1.5.5.7.3.1. Officially described as "TLS WWW server authentication", though regularly used for non-WWW TLS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#server_auth GooglePrivatecaCaPool#server_auth}
        '''
        result = self._values.get("server_auth")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def time_stamping(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Corresponds to OID 1.3.6.1.5.5.7.3.8. Officially described as "Binding the hash of an object to a time".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#time_stamping GooglePrivatecaCaPool#time_stamping}
        '''
        result = self._values.get("time_stamping")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageExtendedKeyUsage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageExtendedKeyUsageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePrivatecaCaPool.GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageExtendedKeyUsageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__30d5382262e62b99f25568a91a25a5250857e206edafea2b522b0ed442e2c00a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e45f58b0e92df2c2a44a6116f39b07832e2009b432c3edc46f2fa2dfe899ef9c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__41d93d14c999f3f8ed816b744a93495ab49cfb5b511cfe63fc2fc8dbbebb4772)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f1634ef7448b23797640d2568a4a49b5c03432543b88abe0c49b678226464b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__755fa445988683225b4e2f04bd46e27193bda96c8935893dd48d095fc28e0c14)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4013069bfe325635f79c80de74e58e711aba765e68435a8ab9b270ab8fb6743d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1dc2a92e63d4ddfdb8b7eb375070bb8daa01aaf0cf4718b1bc5c7ef204f38dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeStamping", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageExtendedKeyUsage]:
        return typing.cast(typing.Optional[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageExtendedKeyUsage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageExtendedKeyUsage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d39c5566875a31058fdf95a696a293562637a44d19e3815d4e9b9e3db9b9509)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePrivatecaCaPool.GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce5db9806802d77aacc5cf05234c921c81dfc9648973fdf2d69d7ae03b37d4b2)
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
        :param cert_sign: The key may be used to sign certificates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#cert_sign GooglePrivatecaCaPool#cert_sign}
        :param content_commitment: The key may be used for cryptographic commitments. Note that this may also be referred to as "non-repudiation". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#content_commitment GooglePrivatecaCaPool#content_commitment}
        :param crl_sign: The key may be used sign certificate revocation lists. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#crl_sign GooglePrivatecaCaPool#crl_sign}
        :param data_encipherment: The key may be used to encipher data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#data_encipherment GooglePrivatecaCaPool#data_encipherment}
        :param decipher_only: The key may be used to decipher only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#decipher_only GooglePrivatecaCaPool#decipher_only}
        :param digital_signature: The key may be used for digital signatures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#digital_signature GooglePrivatecaCaPool#digital_signature}
        :param encipher_only: The key may be used to encipher only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#encipher_only GooglePrivatecaCaPool#encipher_only}
        :param key_agreement: The key may be used in a key agreement protocol. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#key_agreement GooglePrivatecaCaPool#key_agreement}
        :param key_encipherment: The key may be used to encipher other keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#key_encipherment GooglePrivatecaCaPool#key_encipherment}
        '''
        value = GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageBaseKeyUsage(
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
        :param client_auth: Corresponds to OID 1.3.6.1.5.5.7.3.2. Officially described as "TLS WWW client authentication", though regularly used for non-WWW TLS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#client_auth GooglePrivatecaCaPool#client_auth}
        :param code_signing: Corresponds to OID 1.3.6.1.5.5.7.3.3. Officially described as "Signing of downloadable executable code client authentication". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#code_signing GooglePrivatecaCaPool#code_signing}
        :param email_protection: Corresponds to OID 1.3.6.1.5.5.7.3.4. Officially described as "Email protection". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#email_protection GooglePrivatecaCaPool#email_protection}
        :param ocsp_signing: Corresponds to OID 1.3.6.1.5.5.7.3.9. Officially described as "Signing OCSP responses". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#ocsp_signing GooglePrivatecaCaPool#ocsp_signing}
        :param server_auth: Corresponds to OID 1.3.6.1.5.5.7.3.1. Officially described as "TLS WWW server authentication", though regularly used for non-WWW TLS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#server_auth GooglePrivatecaCaPool#server_auth}
        :param time_stamping: Corresponds to OID 1.3.6.1.5.5.7.3.8. Officially described as "Binding the hash of an object to a time". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#time_stamping GooglePrivatecaCaPool#time_stamping}
        '''
        value = GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageExtendedKeyUsage(
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
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsages", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__735a6764d142d5f83fcde38887ede154f57b8c65c9465477a0fcd82077bbc204)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putUnknownExtendedKeyUsages", [value]))

    @jsii.member(jsii_name="resetUnknownExtendedKeyUsages")
    def reset_unknown_extended_key_usages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnknownExtendedKeyUsages", []))

    @builtins.property
    @jsii.member(jsii_name="baseKeyUsage")
    def base_key_usage(
        self,
    ) -> GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageBaseKeyUsageOutputReference:
        return typing.cast(GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageBaseKeyUsageOutputReference, jsii.get(self, "baseKeyUsage"))

    @builtins.property
    @jsii.member(jsii_name="extendedKeyUsage")
    def extended_key_usage(
        self,
    ) -> GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageExtendedKeyUsageOutputReference:
        return typing.cast(GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageExtendedKeyUsageOutputReference, jsii.get(self, "extendedKeyUsage"))

    @builtins.property
    @jsii.member(jsii_name="unknownExtendedKeyUsages")
    def unknown_extended_key_usages(
        self,
    ) -> "GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsagesList":
        return typing.cast("GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsagesList", jsii.get(self, "unknownExtendedKeyUsages"))

    @builtins.property
    @jsii.member(jsii_name="baseKeyUsageInput")
    def base_key_usage_input(
        self,
    ) -> typing.Optional[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageBaseKeyUsage]:
        return typing.cast(typing.Optional[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageBaseKeyUsage], jsii.get(self, "baseKeyUsageInput"))

    @builtins.property
    @jsii.member(jsii_name="extendedKeyUsageInput")
    def extended_key_usage_input(
        self,
    ) -> typing.Optional[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageExtendedKeyUsage]:
        return typing.cast(typing.Optional[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageExtendedKeyUsage], jsii.get(self, "extendedKeyUsageInput"))

    @builtins.property
    @jsii.member(jsii_name="unknownExtendedKeyUsagesInput")
    def unknown_extended_key_usages_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsages"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsages"]]], jsii.get(self, "unknownExtendedKeyUsagesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsage]:
        return typing.cast(typing.Optional[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b82b6aaef42ec3b2f3774b03a681627075499d733b8f0f8ffe72cc304b75bd5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePrivatecaCaPool.GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsages",
    jsii_struct_bases=[],
    name_mapping={"object_id_path": "objectIdPath"},
)
class GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsages:
    def __init__(self, *, object_id_path: typing.Sequence[jsii.Number]) -> None:
        '''
        :param object_id_path: An ObjectId specifies an object identifier (OID). These provide context and describe types in ASN.1 messages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#object_id_path GooglePrivatecaCaPool#object_id_path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f6e9b6626a1c1c99f39184bf29d454561b10511939e2c0b8e397e9be03f2793)
            check_type(argname="argument object_id_path", value=object_id_path, expected_type=type_hints["object_id_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object_id_path": object_id_path,
        }

    @builtins.property
    def object_id_path(self) -> typing.List[jsii.Number]:
        '''An ObjectId specifies an object identifier (OID). These provide context and describe types in ASN.1 messages.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#object_id_path GooglePrivatecaCaPool#object_id_path}
        '''
        result = self._values.get("object_id_path")
        assert result is not None, "Required property 'object_id_path' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsages(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsagesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePrivatecaCaPool.GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsagesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7de05d3de8f8c6c929ea28e1a9d02b31f8290f92c4ce7ace570a023d31c059a2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsagesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43a69b43e653f5f6c89355117122e1572c5d3dd82ea804978625367fdb631763)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsagesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef47eaeaabd4075ff385251b186eaea6be4b201f826ea9393b271971bd75ae3a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__efb9fbdf6c34d9086bb7a2e7b111a74124c7694d3ed07a9bd9cce5ec2dd48fb3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0492be2deba4897ec34256b54c681251d3de466ca079ee8ce90f78e5b1caea4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsages]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsages]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsages]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7172c190679f96b069f0be1815734d540eedd8a5fccb611847c24d0ee7402ec1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsagesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePrivatecaCaPool.GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsagesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a01bae66c312d6f0e0acd40ea6d845a42b5e6fd317485b1789d9c217a3ed710)
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
            type_hints = typing.get_type_hints(_typecheckingstub__23ace5199fb7ede47758db3760f662f70c9f3014e24378b8149b3cd0b6725e28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectIdPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsages]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsages]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsages]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d90e6da4ebdad828ba3f6a15dec1927c1f815a4796100e02a55b738e6fc8005)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePrivatecaCaPool.GooglePrivatecaCaPoolIssuancePolicyBaselineValuesNameConstraints",
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
class GooglePrivatecaCaPoolIssuancePolicyBaselineValuesNameConstraints:
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
        :param critical: Indicates whether or not the name constraints are marked critical. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#critical GooglePrivatecaCaPool#critical}
        :param excluded_dns_names: Contains excluded DNS names. Any DNS name that can be constructed by simply adding zero or more labels to the left-hand side of the name satisfies the name constraint. For example, 'example.com', 'www.example.com', 'www.sub.example.com' would satisfy 'example.com' while 'example1.com' does not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#excluded_dns_names GooglePrivatecaCaPool#excluded_dns_names}
        :param excluded_email_addresses: Contains the excluded email addresses. The value can be a particular email address, a hostname to indicate all email addresses on that host or a domain with a leading period (e.g. '.example.com') to indicate all email addresses in that domain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#excluded_email_addresses GooglePrivatecaCaPool#excluded_email_addresses}
        :param excluded_ip_ranges: Contains the excluded IP ranges. For IPv4 addresses, the ranges are expressed using CIDR notation as specified in RFC 4632. For IPv6 addresses, the ranges are expressed in similar encoding as IPv4 addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#excluded_ip_ranges GooglePrivatecaCaPool#excluded_ip_ranges}
        :param excluded_uris: Contains the excluded URIs that apply to the host part of the name. The value can be a hostname or a domain with a leading period (like '.example.com') Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#excluded_uris GooglePrivatecaCaPool#excluded_uris}
        :param permitted_dns_names: Contains permitted DNS names. Any DNS name that can be constructed by simply adding zero or more labels to the left-hand side of the name satisfies the name constraint. For example, 'example.com', 'www.example.com', 'www.sub.example.com' would satisfy 'example.com' while 'example1.com' does not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#permitted_dns_names GooglePrivatecaCaPool#permitted_dns_names}
        :param permitted_email_addresses: Contains the permitted email addresses. The value can be a particular email address, a hostname to indicate all email addresses on that host or a domain with a leading period (e.g. '.example.com') to indicate all email addresses in that domain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#permitted_email_addresses GooglePrivatecaCaPool#permitted_email_addresses}
        :param permitted_ip_ranges: Contains the permitted IP ranges. For IPv4 addresses, the ranges are expressed using CIDR notation as specified in RFC 4632. For IPv6 addresses, the ranges are expressed in similar encoding as IPv4 addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#permitted_ip_ranges GooglePrivatecaCaPool#permitted_ip_ranges}
        :param permitted_uris: Contains the permitted URIs that apply to the host part of the name. The value can be a hostname or a domain with a leading period (like '.example.com') Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#permitted_uris GooglePrivatecaCaPool#permitted_uris}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3e0d0dde74213d6c4c377846c16bfaa990e85c1042aa5380a34f48d8ef1e475)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#critical GooglePrivatecaCaPool#critical}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#excluded_dns_names GooglePrivatecaCaPool#excluded_dns_names}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#excluded_email_addresses GooglePrivatecaCaPool#excluded_email_addresses}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#excluded_ip_ranges GooglePrivatecaCaPool#excluded_ip_ranges}
        '''
        result = self._values.get("excluded_ip_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def excluded_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Contains the excluded URIs that apply to the host part of the name.

        The value can be a hostname or a domain with a
        leading period (like '.example.com')

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#excluded_uris GooglePrivatecaCaPool#excluded_uris}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#permitted_dns_names GooglePrivatecaCaPool#permitted_dns_names}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#permitted_email_addresses GooglePrivatecaCaPool#permitted_email_addresses}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#permitted_ip_ranges GooglePrivatecaCaPool#permitted_ip_ranges}
        '''
        result = self._values.get("permitted_ip_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def permitted_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Contains the permitted URIs that apply to the host part of the name.

        The value can be a hostname or a domain with a
        leading period (like '.example.com')

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#permitted_uris GooglePrivatecaCaPool#permitted_uris}
        '''
        result = self._values.get("permitted_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePrivatecaCaPoolIssuancePolicyBaselineValuesNameConstraints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePrivatecaCaPoolIssuancePolicyBaselineValuesNameConstraintsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePrivatecaCaPool.GooglePrivatecaCaPoolIssuancePolicyBaselineValuesNameConstraintsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__521fefda8c602932b1faf3fccffd49e93044660e64f9d68081f806cb72922f97)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9bbdb0147eee16183a9df37bdc24f3cde2f4e887cd8f451774a057e16ec3896)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "critical", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludedDnsNames")
    def excluded_dns_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludedDnsNames"))

    @excluded_dns_names.setter
    def excluded_dns_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d249f89651a27725ab97e4cedae90237f7d598b29b83d058b28a98c7b1ba3187)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludedDnsNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludedEmailAddresses")
    def excluded_email_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludedEmailAddresses"))

    @excluded_email_addresses.setter
    def excluded_email_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88ade72263bea0a8d291383d3e20bd4c955e5f9c1d09a15e47070c80801ef17f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludedEmailAddresses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludedIpRanges")
    def excluded_ip_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludedIpRanges"))

    @excluded_ip_ranges.setter
    def excluded_ip_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8622fbe3c7f1468af78653cff41170b3dbb6613ed577d758bdc05e4b5e2eb153)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludedIpRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludedUris")
    def excluded_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludedUris"))

    @excluded_uris.setter
    def excluded_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7121ca026bae0fb193c699a65a263088b613f3f5e24e88a7af69677fd3c37f2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludedUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permittedDnsNames")
    def permitted_dns_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "permittedDnsNames"))

    @permitted_dns_names.setter
    def permitted_dns_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80404b6cd466f470e393fc760adaf71f61ae665c7f8b88a8478866bb1f8cf64f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permittedDnsNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permittedEmailAddresses")
    def permitted_email_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "permittedEmailAddresses"))

    @permitted_email_addresses.setter
    def permitted_email_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ed9dd74295b2ce3bfa56717022787310ae884e35c79bd3a4f444a31c117add3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permittedEmailAddresses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permittedIpRanges")
    def permitted_ip_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "permittedIpRanges"))

    @permitted_ip_ranges.setter
    def permitted_ip_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7675da1b26021a6b2e98f8618ffbce232f338229a9ec338bc6ebcdae027b2dd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permittedIpRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permittedUris")
    def permitted_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "permittedUris"))

    @permitted_uris.setter
    def permitted_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f5246e8f1d2cc84d1abbc292b6271da39721334cd235c52db1b2437468b6433)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permittedUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesNameConstraints]:
        return typing.cast(typing.Optional[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesNameConstraints], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesNameConstraints],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24f2d80b29eaafd21baa7392e49927295b5a279c99f98758538c7db6d629630a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GooglePrivatecaCaPoolIssuancePolicyBaselineValuesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePrivatecaCaPool.GooglePrivatecaCaPoolIssuancePolicyBaselineValuesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__840ed1060d7e38ed21860770ee126050f585712d01a78e005382aaf7b57e7276)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdditionalExtensions")
    def put_additional_extensions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfe193da71a4897a0fb2fa49c32fb838fc41826cf9d3160078f9e1b9dc3a2c36)
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
        :param is_ca: When true, the "CA" in Basic Constraints extension will be set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#is_ca GooglePrivatecaCaPool#is_ca}
        :param max_issuer_path_length: Refers to the "path length constraint" in Basic Constraints extension. For a CA certificate, this value describes the depth of subordinate CA certificates that are allowed. If this value is less than 0, the request will fail. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#max_issuer_path_length GooglePrivatecaCaPool#max_issuer_path_length}
        :param non_ca: When true, the "CA" in Basic Constraints extension will be set to false. If both 'is_ca' and 'non_ca' are unset, the extension will be omitted from the CA certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#non_ca GooglePrivatecaCaPool#non_ca}
        :param zero_max_issuer_path_length: When true, the "path length constraint" in Basic Constraints extension will be set to 0. if both 'max_issuer_path_length' and 'zero_max_issuer_path_length' are unset, the max path length will be omitted from the CA certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#zero_max_issuer_path_length GooglePrivatecaCaPool#zero_max_issuer_path_length}
        '''
        value = GooglePrivatecaCaPoolIssuancePolicyBaselineValuesCaOptions(
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
        base_key_usage: typing.Union[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageBaseKeyUsage, typing.Dict[builtins.str, typing.Any]],
        extended_key_usage: typing.Union[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageExtendedKeyUsage, typing.Dict[builtins.str, typing.Any]],
        unknown_extended_key_usages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsages, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param base_key_usage: base_key_usage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#base_key_usage GooglePrivatecaCaPool#base_key_usage}
        :param extended_key_usage: extended_key_usage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#extended_key_usage GooglePrivatecaCaPool#extended_key_usage}
        :param unknown_extended_key_usages: unknown_extended_key_usages block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#unknown_extended_key_usages GooglePrivatecaCaPool#unknown_extended_key_usages}
        '''
        value = GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsage(
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
        :param critical: Indicates whether or not the name constraints are marked critical. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#critical GooglePrivatecaCaPool#critical}
        :param excluded_dns_names: Contains excluded DNS names. Any DNS name that can be constructed by simply adding zero or more labels to the left-hand side of the name satisfies the name constraint. For example, 'example.com', 'www.example.com', 'www.sub.example.com' would satisfy 'example.com' while 'example1.com' does not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#excluded_dns_names GooglePrivatecaCaPool#excluded_dns_names}
        :param excluded_email_addresses: Contains the excluded email addresses. The value can be a particular email address, a hostname to indicate all email addresses on that host or a domain with a leading period (e.g. '.example.com') to indicate all email addresses in that domain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#excluded_email_addresses GooglePrivatecaCaPool#excluded_email_addresses}
        :param excluded_ip_ranges: Contains the excluded IP ranges. For IPv4 addresses, the ranges are expressed using CIDR notation as specified in RFC 4632. For IPv6 addresses, the ranges are expressed in similar encoding as IPv4 addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#excluded_ip_ranges GooglePrivatecaCaPool#excluded_ip_ranges}
        :param excluded_uris: Contains the excluded URIs that apply to the host part of the name. The value can be a hostname or a domain with a leading period (like '.example.com') Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#excluded_uris GooglePrivatecaCaPool#excluded_uris}
        :param permitted_dns_names: Contains permitted DNS names. Any DNS name that can be constructed by simply adding zero or more labels to the left-hand side of the name satisfies the name constraint. For example, 'example.com', 'www.example.com', 'www.sub.example.com' would satisfy 'example.com' while 'example1.com' does not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#permitted_dns_names GooglePrivatecaCaPool#permitted_dns_names}
        :param permitted_email_addresses: Contains the permitted email addresses. The value can be a particular email address, a hostname to indicate all email addresses on that host or a domain with a leading period (e.g. '.example.com') to indicate all email addresses in that domain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#permitted_email_addresses GooglePrivatecaCaPool#permitted_email_addresses}
        :param permitted_ip_ranges: Contains the permitted IP ranges. For IPv4 addresses, the ranges are expressed using CIDR notation as specified in RFC 4632. For IPv6 addresses, the ranges are expressed in similar encoding as IPv4 addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#permitted_ip_ranges GooglePrivatecaCaPool#permitted_ip_ranges}
        :param permitted_uris: Contains the permitted URIs that apply to the host part of the name. The value can be a hostname or a domain with a leading period (like '.example.com') Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#permitted_uris GooglePrivatecaCaPool#permitted_uris}
        '''
        value = GooglePrivatecaCaPoolIssuancePolicyBaselineValuesNameConstraints(
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
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GooglePrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIds", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e60c87537f2e010d9a13e905fe24c5a667b0acf30facc55fa893af4ef125bb3)
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
    ) -> GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsList:
        return typing.cast(GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsList, jsii.get(self, "additionalExtensions"))

    @builtins.property
    @jsii.member(jsii_name="caOptions")
    def ca_options(
        self,
    ) -> GooglePrivatecaCaPoolIssuancePolicyBaselineValuesCaOptionsOutputReference:
        return typing.cast(GooglePrivatecaCaPoolIssuancePolicyBaselineValuesCaOptionsOutputReference, jsii.get(self, "caOptions"))

    @builtins.property
    @jsii.member(jsii_name="keyUsage")
    def key_usage(
        self,
    ) -> GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageOutputReference:
        return typing.cast(GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageOutputReference, jsii.get(self, "keyUsage"))

    @builtins.property
    @jsii.member(jsii_name="nameConstraints")
    def name_constraints(
        self,
    ) -> GooglePrivatecaCaPoolIssuancePolicyBaselineValuesNameConstraintsOutputReference:
        return typing.cast(GooglePrivatecaCaPoolIssuancePolicyBaselineValuesNameConstraintsOutputReference, jsii.get(self, "nameConstraints"))

    @builtins.property
    @jsii.member(jsii_name="policyIds")
    def policy_ids(
        self,
    ) -> "GooglePrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIdsList":
        return typing.cast("GooglePrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIdsList", jsii.get(self, "policyIds"))

    @builtins.property
    @jsii.member(jsii_name="additionalExtensionsInput")
    def additional_extensions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensions]]], jsii.get(self, "additionalExtensionsInput"))

    @builtins.property
    @jsii.member(jsii_name="aiaOcspServersInput")
    def aia_ocsp_servers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "aiaOcspServersInput"))

    @builtins.property
    @jsii.member(jsii_name="caOptionsInput")
    def ca_options_input(
        self,
    ) -> typing.Optional[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesCaOptions]:
        return typing.cast(typing.Optional[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesCaOptions], jsii.get(self, "caOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="keyUsageInput")
    def key_usage_input(
        self,
    ) -> typing.Optional[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsage]:
        return typing.cast(typing.Optional[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsage], jsii.get(self, "keyUsageInput"))

    @builtins.property
    @jsii.member(jsii_name="nameConstraintsInput")
    def name_constraints_input(
        self,
    ) -> typing.Optional[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesNameConstraints]:
        return typing.cast(typing.Optional[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesNameConstraints], jsii.get(self, "nameConstraintsInput"))

    @builtins.property
    @jsii.member(jsii_name="policyIdsInput")
    def policy_ids_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GooglePrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIds"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GooglePrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIds"]]], jsii.get(self, "policyIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="aiaOcspServers")
    def aia_ocsp_servers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "aiaOcspServers"))

    @aia_ocsp_servers.setter
    def aia_ocsp_servers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__754cc69c5ea510175c3b743453b6d285d20f392c8cb34466eeb3773310dff172)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aiaOcspServers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GooglePrivatecaCaPoolIssuancePolicyBaselineValues]:
        return typing.cast(typing.Optional[GooglePrivatecaCaPoolIssuancePolicyBaselineValues], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePrivatecaCaPoolIssuancePolicyBaselineValues],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a374b9c33b89020286b516b5d3058b9aaba36906cb8fbbfeb2af544156cc220)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePrivatecaCaPool.GooglePrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIds",
    jsii_struct_bases=[],
    name_mapping={"object_id_path": "objectIdPath"},
)
class GooglePrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIds:
    def __init__(self, *, object_id_path: typing.Sequence[jsii.Number]) -> None:
        '''
        :param object_id_path: An ObjectId specifies an object identifier (OID). These provide context and describe types in ASN.1 messages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#object_id_path GooglePrivatecaCaPool#object_id_path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c3ee5d78e13355a7e338e88808232e7609fce29bb6fa5cdb77e4469bdd0c9ff)
            check_type(argname="argument object_id_path", value=object_id_path, expected_type=type_hints["object_id_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object_id_path": object_id_path,
        }

    @builtins.property
    def object_id_path(self) -> typing.List[jsii.Number]:
        '''An ObjectId specifies an object identifier (OID). These provide context and describe types in ASN.1 messages.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#object_id_path GooglePrivatecaCaPool#object_id_path}
        '''
        result = self._values.get("object_id_path")
        assert result is not None, "Required property 'object_id_path' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIdsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePrivatecaCaPool.GooglePrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIdsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0adf0cefcc69eef6d30ebb936ba3ef15fe13abaf0c25e72989440cc2c311206a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GooglePrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIdsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7e893f65c9b12a1a4f04c1a07934b9784a5832dbd1ae78bc272b80339cfcba9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GooglePrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIdsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9096f203c3b6862d76960e912fc26f6151dfa9e99174c4e059529db2b3e28a62)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9739f2f910e1b408543e2758778b9033fe457bd14cb61d5aad026b494139ca8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__11c5045a872446cfecadfd89a7c2e7f7f49fe1636d55d6b97ca1195bc04fcef6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIds]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIds]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIds]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08df2942b098625b0cbb9b6ce4b407dcf600f4764a5334aec5ecf0786bc75cae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GooglePrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIdsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePrivatecaCaPool.GooglePrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIdsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__490f622a2351b2c99fda0462d8984c133d5115a593c935b2786f8448a6a83d47)
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
            type_hints = typing.get_type_hints(_typecheckingstub__125fe2f35e1906006e3802f33946eef318ac86feb8c91bdd5faa28b3111403d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectIdPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIds]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIds]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIds]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26ee5a451cb3e7da7e1b594f84ae6a82ea72b82249fd4e74198f718b3128dacf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePrivatecaCaPool.GooglePrivatecaCaPoolIssuancePolicyIdentityConstraints",
    jsii_struct_bases=[],
    name_mapping={
        "allow_subject_alt_names_passthrough": "allowSubjectAltNamesPassthrough",
        "allow_subject_passthrough": "allowSubjectPassthrough",
        "cel_expression": "celExpression",
    },
)
class GooglePrivatecaCaPoolIssuancePolicyIdentityConstraints:
    def __init__(
        self,
        *,
        allow_subject_alt_names_passthrough: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        allow_subject_passthrough: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        cel_expression: typing.Optional[typing.Union["GooglePrivatecaCaPoolIssuancePolicyIdentityConstraintsCelExpression", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_subject_alt_names_passthrough: If this is set, the SubjectAltNames extension may be copied from a certificate request into the signed certificate. Otherwise, the requested SubjectAltNames will be discarded. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#allow_subject_alt_names_passthrough GooglePrivatecaCaPool#allow_subject_alt_names_passthrough}
        :param allow_subject_passthrough: If this is set, the Subject field may be copied from a certificate request into the signed certificate. Otherwise, the requested Subject will be discarded. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#allow_subject_passthrough GooglePrivatecaCaPool#allow_subject_passthrough}
        :param cel_expression: cel_expression block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#cel_expression GooglePrivatecaCaPool#cel_expression}
        '''
        if isinstance(cel_expression, dict):
            cel_expression = GooglePrivatecaCaPoolIssuancePolicyIdentityConstraintsCelExpression(**cel_expression)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e888ef922fe9729f226c26a7f6ff6d986a245d1a7f7cda34353f25ba7c8a4748)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#allow_subject_alt_names_passthrough GooglePrivatecaCaPool#allow_subject_alt_names_passthrough}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#allow_subject_passthrough GooglePrivatecaCaPool#allow_subject_passthrough}
        '''
        result = self._values.get("allow_subject_passthrough")
        assert result is not None, "Required property 'allow_subject_passthrough' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def cel_expression(
        self,
    ) -> typing.Optional["GooglePrivatecaCaPoolIssuancePolicyIdentityConstraintsCelExpression"]:
        '''cel_expression block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#cel_expression GooglePrivatecaCaPool#cel_expression}
        '''
        result = self._values.get("cel_expression")
        return typing.cast(typing.Optional["GooglePrivatecaCaPoolIssuancePolicyIdentityConstraintsCelExpression"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePrivatecaCaPoolIssuancePolicyIdentityConstraints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePrivatecaCaPool.GooglePrivatecaCaPoolIssuancePolicyIdentityConstraintsCelExpression",
    jsii_struct_bases=[],
    name_mapping={
        "expression": "expression",
        "description": "description",
        "location": "location",
        "title": "title",
    },
)
class GooglePrivatecaCaPoolIssuancePolicyIdentityConstraintsCelExpression:
    def __init__(
        self,
        *,
        expression: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#expression GooglePrivatecaCaPool#expression}
        :param description: Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#description GooglePrivatecaCaPool#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#location GooglePrivatecaCaPool#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#title GooglePrivatecaCaPool#title}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__904c2b90906ac4ead3ea616f87be9161fe3a0e4a73802e5a78e00a57073f3174)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#expression GooglePrivatecaCaPool#expression}
        '''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the expression.

        This is a longer text which describes the expression, e.g. when hovered over it in a UI.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#description GooglePrivatecaCaPool#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''String indicating the location of the expression for error reporting, e.g. a file name and a position in the file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#location GooglePrivatecaCaPool#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#title GooglePrivatecaCaPool#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePrivatecaCaPoolIssuancePolicyIdentityConstraintsCelExpression(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePrivatecaCaPoolIssuancePolicyIdentityConstraintsCelExpressionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePrivatecaCaPool.GooglePrivatecaCaPoolIssuancePolicyIdentityConstraintsCelExpressionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffb823eacea15eda20f3e778f52ad5009b54d654a9d6e5a302a7048c7b7aaf29)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2e31d81410efad504dec1c0681ebf139bde62b661e086cafc4b0ec15ea3ccd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__038a00a3314b0220677309561a93eded6d7e7d169c344117e3a7bdbd9692acbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec2d47f02f11387d5f8a943bfac96fb93ca164f44384b75905254a4c9f957613)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d6d31309a29aa5e17b3f7151b1c788058ef8ccf5e633e047d94d3b4a6f0b07f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GooglePrivatecaCaPoolIssuancePolicyIdentityConstraintsCelExpression]:
        return typing.cast(typing.Optional[GooglePrivatecaCaPoolIssuancePolicyIdentityConstraintsCelExpression], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePrivatecaCaPoolIssuancePolicyIdentityConstraintsCelExpression],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5803bfab5324f3eceb1194c6e39cc9e5b5148eaa3e18b7134fb90200c2514dc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GooglePrivatecaCaPoolIssuancePolicyIdentityConstraintsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePrivatecaCaPool.GooglePrivatecaCaPoolIssuancePolicyIdentityConstraintsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7d34ad1fae8f6320bc75480b460bb16c4133a9bb20edf03589f571e71fe1e91)
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
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#expression GooglePrivatecaCaPool#expression}
        :param description: Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#description GooglePrivatecaCaPool#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#location GooglePrivatecaCaPool#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#title GooglePrivatecaCaPool#title}
        '''
        value = GooglePrivatecaCaPoolIssuancePolicyIdentityConstraintsCelExpression(
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
    ) -> GooglePrivatecaCaPoolIssuancePolicyIdentityConstraintsCelExpressionOutputReference:
        return typing.cast(GooglePrivatecaCaPoolIssuancePolicyIdentityConstraintsCelExpressionOutputReference, jsii.get(self, "celExpression"))

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
    ) -> typing.Optional[GooglePrivatecaCaPoolIssuancePolicyIdentityConstraintsCelExpression]:
        return typing.cast(typing.Optional[GooglePrivatecaCaPoolIssuancePolicyIdentityConstraintsCelExpression], jsii.get(self, "celExpressionInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__1fe361c82dc6f74d2fad11e259a48e3a5d2f0101dea45cd12c4badb402533eb6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__19a46a312ea77a4dd8f1f7a47c699bcaa3318ec88cef7589a14d3751b131a5ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowSubjectPassthrough", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GooglePrivatecaCaPoolIssuancePolicyIdentityConstraints]:
        return typing.cast(typing.Optional[GooglePrivatecaCaPoolIssuancePolicyIdentityConstraints], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePrivatecaCaPoolIssuancePolicyIdentityConstraints],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d43556e353d698a0efb70032d91191f9ae57c8219b49c45418bb6c17c2f52ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GooglePrivatecaCaPoolIssuancePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePrivatecaCaPool.GooglePrivatecaCaPoolIssuancePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5976bd59eae857e6491de19150f6270f295c3d5d78d9086b9014f7d19de743ff)
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
        :param allow_config_based_issuance: When true, allows callers to create Certificates by specifying a CertificateConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#allow_config_based_issuance GooglePrivatecaCaPool#allow_config_based_issuance}
        :param allow_csr_based_issuance: When true, allows callers to create Certificates by specifying a CSR. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#allow_csr_based_issuance GooglePrivatecaCaPool#allow_csr_based_issuance}
        '''
        value = GooglePrivatecaCaPoolIssuancePolicyAllowedIssuanceModes(
            allow_config_based_issuance=allow_config_based_issuance,
            allow_csr_based_issuance=allow_csr_based_issuance,
        )

        return typing.cast(None, jsii.invoke(self, "putAllowedIssuanceModes", [value]))

    @jsii.member(jsii_name="putAllowedKeyTypes")
    def put_allowed_key_types(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypes, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4de02a3ce48da07b37d5df2a193a50041eb8bf249ce4af170ac496eb5f0f2fd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAllowedKeyTypes", [value]))

    @jsii.member(jsii_name="putBaselineValues")
    def put_baseline_values(
        self,
        *,
        ca_options: typing.Union[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesCaOptions, typing.Dict[builtins.str, typing.Any]],
        key_usage: typing.Union[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsage, typing.Dict[builtins.str, typing.Any]],
        additional_extensions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensions, typing.Dict[builtins.str, typing.Any]]]]] = None,
        aia_ocsp_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
        name_constraints: typing.Optional[typing.Union[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesNameConstraints, typing.Dict[builtins.str, typing.Any]]] = None,
        policy_ids: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIds, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param ca_options: ca_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#ca_options GooglePrivatecaCaPool#ca_options}
        :param key_usage: key_usage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#key_usage GooglePrivatecaCaPool#key_usage}
        :param additional_extensions: additional_extensions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#additional_extensions GooglePrivatecaCaPool#additional_extensions}
        :param aia_ocsp_servers: Describes Online Certificate Status Protocol (OCSP) endpoint addresses that appear in the "Authority Information Access" extension in the certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#aia_ocsp_servers GooglePrivatecaCaPool#aia_ocsp_servers}
        :param name_constraints: name_constraints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#name_constraints GooglePrivatecaCaPool#name_constraints}
        :param policy_ids: policy_ids block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#policy_ids GooglePrivatecaCaPool#policy_ids}
        '''
        value = GooglePrivatecaCaPoolIssuancePolicyBaselineValues(
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
        cel_expression: typing.Optional[typing.Union[GooglePrivatecaCaPoolIssuancePolicyIdentityConstraintsCelExpression, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_subject_alt_names_passthrough: If this is set, the SubjectAltNames extension may be copied from a certificate request into the signed certificate. Otherwise, the requested SubjectAltNames will be discarded. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#allow_subject_alt_names_passthrough GooglePrivatecaCaPool#allow_subject_alt_names_passthrough}
        :param allow_subject_passthrough: If this is set, the Subject field may be copied from a certificate request into the signed certificate. Otherwise, the requested Subject will be discarded. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#allow_subject_passthrough GooglePrivatecaCaPool#allow_subject_passthrough}
        :param cel_expression: cel_expression block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#cel_expression GooglePrivatecaCaPool#cel_expression}
        '''
        value = GooglePrivatecaCaPoolIssuancePolicyIdentityConstraints(
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
    ) -> GooglePrivatecaCaPoolIssuancePolicyAllowedIssuanceModesOutputReference:
        return typing.cast(GooglePrivatecaCaPoolIssuancePolicyAllowedIssuanceModesOutputReference, jsii.get(self, "allowedIssuanceModes"))

    @builtins.property
    @jsii.member(jsii_name="allowedKeyTypes")
    def allowed_key_types(
        self,
    ) -> GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesList:
        return typing.cast(GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesList, jsii.get(self, "allowedKeyTypes"))

    @builtins.property
    @jsii.member(jsii_name="baselineValues")
    def baseline_values(
        self,
    ) -> GooglePrivatecaCaPoolIssuancePolicyBaselineValuesOutputReference:
        return typing.cast(GooglePrivatecaCaPoolIssuancePolicyBaselineValuesOutputReference, jsii.get(self, "baselineValues"))

    @builtins.property
    @jsii.member(jsii_name="identityConstraints")
    def identity_constraints(
        self,
    ) -> GooglePrivatecaCaPoolIssuancePolicyIdentityConstraintsOutputReference:
        return typing.cast(GooglePrivatecaCaPoolIssuancePolicyIdentityConstraintsOutputReference, jsii.get(self, "identityConstraints"))

    @builtins.property
    @jsii.member(jsii_name="allowedIssuanceModesInput")
    def allowed_issuance_modes_input(
        self,
    ) -> typing.Optional[GooglePrivatecaCaPoolIssuancePolicyAllowedIssuanceModes]:
        return typing.cast(typing.Optional[GooglePrivatecaCaPoolIssuancePolicyAllowedIssuanceModes], jsii.get(self, "allowedIssuanceModesInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedKeyTypesInput")
    def allowed_key_types_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypes]]], jsii.get(self, "allowedKeyTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="backdateDurationInput")
    def backdate_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "backdateDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="baselineValuesInput")
    def baseline_values_input(
        self,
    ) -> typing.Optional[GooglePrivatecaCaPoolIssuancePolicyBaselineValues]:
        return typing.cast(typing.Optional[GooglePrivatecaCaPoolIssuancePolicyBaselineValues], jsii.get(self, "baselineValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="identityConstraintsInput")
    def identity_constraints_input(
        self,
    ) -> typing.Optional[GooglePrivatecaCaPoolIssuancePolicyIdentityConstraints]:
        return typing.cast(typing.Optional[GooglePrivatecaCaPoolIssuancePolicyIdentityConstraints], jsii.get(self, "identityConstraintsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__2054a4be1b527527f3600cc914e66e8b52cda4b12fd252c1866dad6dcbb55366)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backdateDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumLifetime")
    def maximum_lifetime(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maximumLifetime"))

    @maximum_lifetime.setter
    def maximum_lifetime(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9993338b50d9006d103905e0a81ade9d601838c871eda3de81594b0883a614e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumLifetime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GooglePrivatecaCaPoolIssuancePolicy]:
        return typing.cast(typing.Optional[GooglePrivatecaCaPoolIssuancePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePrivatecaCaPoolIssuancePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5fc2003e9ede5f82f085152db512f2c1baafab6ac5e80b50997c3d5a585ab60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePrivatecaCaPool.GooglePrivatecaCaPoolPublishingOptions",
    jsii_struct_bases=[],
    name_mapping={
        "publish_ca_cert": "publishCaCert",
        "publish_crl": "publishCrl",
        "encoding_format": "encodingFormat",
    },
)
class GooglePrivatecaCaPoolPublishingOptions:
    def __init__(
        self,
        *,
        publish_ca_cert: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        publish_crl: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        encoding_format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param publish_ca_cert: When true, publishes each CertificateAuthority's CA certificate and includes its URL in the "Authority Information Access" X.509 extension in all issued Certificates. If this is false, the CA certificate will not be published and the corresponding X.509 extension will not be written in issued certificates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#publish_ca_cert GooglePrivatecaCaPool#publish_ca_cert}
        :param publish_crl: When true, publishes each CertificateAuthority's CRL and includes its URL in the "CRL Distribution Points" X.509 extension in all issued Certificates. If this is false, CRLs will not be published and the corresponding X.509 extension will not be written in issued certificates. CRLs will expire 7 days from their creation. However, we will rebuild daily. CRLs are also rebuilt shortly after a certificate is revoked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#publish_crl GooglePrivatecaCaPool#publish_crl}
        :param encoding_format: Specifies the encoding format of each CertificateAuthority's CA certificate and CRLs. If this is omitted, CA certificates and CRLs will be published in PEM. Possible values: ["PEM", "DER"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#encoding_format GooglePrivatecaCaPool#encoding_format}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59ce820a8dd1398ce4bdff389668c9215e0a9d60b90557291d26b707e20093f5)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#publish_ca_cert GooglePrivatecaCaPool#publish_ca_cert}
        '''
        result = self._values.get("publish_ca_cert")
        assert result is not None, "Required property 'publish_ca_cert' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def publish_crl(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''When true, publishes each CertificateAuthority's CRL and includes its URL in the "CRL Distribution Points" X.509 extension in all issued Certificates. If this is false, CRLs will not be published and the corresponding X.509 extension will not be written in issued certificates. CRLs will expire 7 days from their creation. However, we will rebuild daily. CRLs are also rebuilt shortly after a certificate is revoked.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#publish_crl GooglePrivatecaCaPool#publish_crl}
        '''
        result = self._values.get("publish_crl")
        assert result is not None, "Required property 'publish_crl' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def encoding_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the encoding format of each CertificateAuthority's CA certificate and CRLs.

        If this is omitted, CA certificates and CRLs
        will be published in PEM. Possible values: ["PEM", "DER"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#encoding_format GooglePrivatecaCaPool#encoding_format}
        '''
        result = self._values.get("encoding_format")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePrivatecaCaPoolPublishingOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePrivatecaCaPoolPublishingOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePrivatecaCaPool.GooglePrivatecaCaPoolPublishingOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8fc8ab6f244e442db396875aa819d41087c65fa362f39f151fde443aa64a030)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8044a10cc24f59b07b4096906bd0fbdb79805e6d0641095a8d2aa9a71ea217fe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bfc880058fc78650c4d571254c68cff2cb76fb7e2ad0fb5b089e9a8c788e0c69)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bdc49d5b59aefdee5572ccc4a4307c5f13650bec79ea70ed6d317a3d96737bc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publishCrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GooglePrivatecaCaPoolPublishingOptions]:
        return typing.cast(typing.Optional[GooglePrivatecaCaPoolPublishingOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePrivatecaCaPoolPublishingOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__221dee593b9c1c62f9da4a36f3487b956e6a95e5c599baf284496654a806689d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePrivatecaCaPool.GooglePrivatecaCaPoolTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GooglePrivatecaCaPoolTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#create GooglePrivatecaCaPool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#delete GooglePrivatecaCaPool#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#update GooglePrivatecaCaPool#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b010534f94e8843036964347cce4d035d45629f6f70ba20250731f829f3f4a1)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#create GooglePrivatecaCaPool#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#delete GooglePrivatecaCaPool#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_privateca_ca_pool#update GooglePrivatecaCaPool#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePrivatecaCaPoolTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePrivatecaCaPoolTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePrivatecaCaPool.GooglePrivatecaCaPoolTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9a6a4dacd093b420f73b5a808ae5e3e7b8152520aa9f44d40f90dfb7349e16b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__41ca9a212104eb058f7736c08fc69822bc6de5a0fb552970b77574b4069c1eb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16e71d5cbdd0836acfbe923942ff2e1669ecae19fed014c6bc6c7249659d05f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e1d5585eaac7ddc1700cc65453ebf3e986cb6e6f1a9dbc3fefe046c3a86ae8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePrivatecaCaPoolTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePrivatecaCaPoolTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePrivatecaCaPoolTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1f2235bc14f065cbad0898e74cbd93f0ed2639eeb439cc522a77daf3258bf76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GooglePrivatecaCaPool",
    "GooglePrivatecaCaPoolConfig",
    "GooglePrivatecaCaPoolIssuancePolicy",
    "GooglePrivatecaCaPoolIssuancePolicyAllowedIssuanceModes",
    "GooglePrivatecaCaPoolIssuancePolicyAllowedIssuanceModesOutputReference",
    "GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypes",
    "GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesEllipticCurve",
    "GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesEllipticCurveOutputReference",
    "GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesList",
    "GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesOutputReference",
    "GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesRsa",
    "GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesRsaOutputReference",
    "GooglePrivatecaCaPoolIssuancePolicyBaselineValues",
    "GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensions",
    "GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsList",
    "GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsObjectId",
    "GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsObjectIdOutputReference",
    "GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsOutputReference",
    "GooglePrivatecaCaPoolIssuancePolicyBaselineValuesCaOptions",
    "GooglePrivatecaCaPoolIssuancePolicyBaselineValuesCaOptionsOutputReference",
    "GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsage",
    "GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageBaseKeyUsage",
    "GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageBaseKeyUsageOutputReference",
    "GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageExtendedKeyUsage",
    "GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageExtendedKeyUsageOutputReference",
    "GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageOutputReference",
    "GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsages",
    "GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsagesList",
    "GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsagesOutputReference",
    "GooglePrivatecaCaPoolIssuancePolicyBaselineValuesNameConstraints",
    "GooglePrivatecaCaPoolIssuancePolicyBaselineValuesNameConstraintsOutputReference",
    "GooglePrivatecaCaPoolIssuancePolicyBaselineValuesOutputReference",
    "GooglePrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIds",
    "GooglePrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIdsList",
    "GooglePrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIdsOutputReference",
    "GooglePrivatecaCaPoolIssuancePolicyIdentityConstraints",
    "GooglePrivatecaCaPoolIssuancePolicyIdentityConstraintsCelExpression",
    "GooglePrivatecaCaPoolIssuancePolicyIdentityConstraintsCelExpressionOutputReference",
    "GooglePrivatecaCaPoolIssuancePolicyIdentityConstraintsOutputReference",
    "GooglePrivatecaCaPoolIssuancePolicyOutputReference",
    "GooglePrivatecaCaPoolPublishingOptions",
    "GooglePrivatecaCaPoolPublishingOptionsOutputReference",
    "GooglePrivatecaCaPoolTimeouts",
    "GooglePrivatecaCaPoolTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__085a59c349be0f9ebbae0291ef2d9f5152449ad3c9d6aa231a14493915bea21d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    tier: builtins.str,
    id: typing.Optional[builtins.str] = None,
    issuance_policy: typing.Optional[typing.Union[GooglePrivatecaCaPoolIssuancePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    publishing_options: typing.Optional[typing.Union[GooglePrivatecaCaPoolPublishingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GooglePrivatecaCaPoolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__dfedca677d2f64c190f036f08a6f9e84664eb667bff843017e6d92a1068b6354(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeb43b0f48095a786bed060b48ce011eeb7c9b8b711eee8ed332fff244139c74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ced63f440816be0c61738f073515f9ff3af86103471948100dbaec0f9bc1d27(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f82dbd7cbc77d5444b42407afa8dc0c9ba39a45bd3bb67d50fb99df64704e54d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aa3da31723a044776044c14396a97359710b8ed147370a9ae799c5256eb91c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdaecba69fef06885b594da2c2af102894acb6533cbf759324ac154de3690d86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6d03c392cb022ac36aef8ddf83429c679416265929869fe46588b8aa1e9a598(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0b9ce151835ed0876e1c3b731a91cfd516d4860faabb4c738f1c6873d8f3bb7(
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
    issuance_policy: typing.Optional[typing.Union[GooglePrivatecaCaPoolIssuancePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    publishing_options: typing.Optional[typing.Union[GooglePrivatecaCaPoolPublishingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GooglePrivatecaCaPoolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d678d2107965d6379128e969c869f9a701e9cbca28473b6ab22967457fbedd51(
    *,
    allowed_issuance_modes: typing.Optional[typing.Union[GooglePrivatecaCaPoolIssuancePolicyAllowedIssuanceModes, typing.Dict[builtins.str, typing.Any]]] = None,
    allowed_key_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    backdate_duration: typing.Optional[builtins.str] = None,
    baseline_values: typing.Optional[typing.Union[GooglePrivatecaCaPoolIssuancePolicyBaselineValues, typing.Dict[builtins.str, typing.Any]]] = None,
    identity_constraints: typing.Optional[typing.Union[GooglePrivatecaCaPoolIssuancePolicyIdentityConstraints, typing.Dict[builtins.str, typing.Any]]] = None,
    maximum_lifetime: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c05d14ffaf38907b3d545f57e2692665accad07c47c1e034e30149dcf694467(
    *,
    allow_config_based_issuance: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    allow_csr_based_issuance: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93fa3fb49e8589e56721f6e9132d71f0a87e2f248d9874ae66933752e67b869b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9522c3197b8446a945f746f09e93819b6cb3f59c494042a15b2e97fec89a02e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c9b323f755473ba498b2e14aaa17b8df876813fc0c60645129556a7742dda10(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab416ce782d20b0822231c2f9c5bd8e73a31288aff66953d14392741ecad4f9d(
    value: typing.Optional[GooglePrivatecaCaPoolIssuancePolicyAllowedIssuanceModes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98bd419020674acaaeb95ecef804e7d8db98ca23f19a9549cf148f7e7ad60406(
    *,
    elliptic_curve: typing.Optional[typing.Union[GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesEllipticCurve, typing.Dict[builtins.str, typing.Any]]] = None,
    rsa: typing.Optional[typing.Union[GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesRsa, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f845af5bb986970d072df619576de75d041365f6dfc687115b42934b8c0cdcb7(
    *,
    signature_algorithm: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9c03f90052a82ecdf34af785879ce54f856e2afdfd07be5cc5664052bb93487(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__388e6b8f1bcbc222ece31354cc28804fc243dc808f986565b6beb6df6b8fe3ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74cbd4310278cb3940b97aa248ed6f4e01466d356ad51826a14e210bcec565e9(
    value: typing.Optional[GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesEllipticCurve],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f36226dbe8eac2ec60cf6d8e6bcab57bc9cd95e8742c13016080a04cd85dd3c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2f3d44f9cbb808c1bc31bb28b6bb8df75f8cfcdf62afb16d0d14625b476fadb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6296f611a822c56018f05caded1013230480dbe1904593e242e1abcd034bac72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78f728ef238e6f216333bbbf1931fbf3511efed7a8a7df1bc3156427b3c7da14(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb73ae6b40b907e3cc8013fd8e3d9b54284518ac419cdde66d7ec2708fe0ad56(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52a8e784ab6727ebc79f8e2c060a15af303cc1f6c3df9e1a6e3516ee48f387f1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b89627ef75446618bae38a2374275a079e63c2bdf0fc31040d030dbd0d04282(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8938a0435a21e263a93dc69ac485fc0fd301886439d37f4cb601efffe3336632(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eb99b06d1d4b180e74e62a4b4e7d0fd3e178e6a7c9de8aaf35e0f8008db0715(
    *,
    max_modulus_size: typing.Optional[builtins.str] = None,
    min_modulus_size: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3ee1c24cb7ccaa5c9a6fd997061f5a2641842d7c2ce22388d6746aa8d490216(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f38f516acf5991b7a2aa5660706001f0c5b6c9545333b8bd8c025ed28a95295(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea6d7b763106bad725fb3ef8f12c764b2ee6cdfecafecc8970fab828edf82da9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a364d69ec9e8a5e5fbb9717d6722bdf46303d9f189446afbdc8eb034cd586438(
    value: typing.Optional[GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypesRsa],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e4b51ba5ad121aebba598f9e79150f752fd027d300e1edd132e91e45544ac1f(
    *,
    ca_options: typing.Union[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesCaOptions, typing.Dict[builtins.str, typing.Any]],
    key_usage: typing.Union[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsage, typing.Dict[builtins.str, typing.Any]],
    additional_extensions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    aia_ocsp_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
    name_constraints: typing.Optional[typing.Union[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesNameConstraints, typing.Dict[builtins.str, typing.Any]]] = None,
    policy_ids: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIds, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a190eaf4b3e14cdd220d2accfa9b1814061e97d03c898265103b2e91864d4094(
    *,
    critical: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    object_id: typing.Union[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsObjectId, typing.Dict[builtins.str, typing.Any]],
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1ab10cdd74d6bd4be726224d011ebee7b357b19eaac01a6634d85bf749df323(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d759d7fd3e4fb53f41e3c9c3e1378cac9b9e2dbbbf7d07d86517fd805db97fd4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ebe6337a1aa12135f7a3fcd0a13606ad28ae2248512b60a34417606c765b36f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1604c1ff0984dcf2523db2716b34bc24b066f9c09c8c218e5e184751986ead05(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cda4347ab82f78dee075038c975049eb8b97385c2cb2dbf08f4b7174fdd5215(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b87fb0e44bda422991b449542c3309b31349847f064c6207d139c074c264e6b5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd7979f7454acb0062773b99241e65f690bb2f9e76429fa67e421944bbefe7ab(
    *,
    object_id_path: typing.Sequence[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a984453b5cf29bedaf5042320f29bad5634c4c19e4085b6ec07f970f46281796(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62c1bb59c4d21ed808befd3327af99710489d0259d5e897e2f6fa31388007325(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76d4470a89193677c51141175f7daf8e32835978010e70ac932a8a18971bf499(
    value: typing.Optional[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensionsObjectId],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89850d95b721c39373887c253ef8848d0643562f92cab2fb1d2e5cad07b951fc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64809fcbe298f405b306a8c6f4bf5f149485d221cb02a0bc27b567996ab6d7e9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b36c01d3e523739c6cf6e49dcf615de0ba9f758083ea8216a6b034e1bb864b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c2e08ad02ad1b8ec185665934ab4f35a1ba0029df9e0dff754efa39ae03a2f4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24a27556b1a1603b29fb2b6cd2b9a47038f069de130abede38be2defba360dbd(
    *,
    is_ca: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    max_issuer_path_length: typing.Optional[jsii.Number] = None,
    non_ca: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    zero_max_issuer_path_length: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8fe9a409e68f12e9a1ac5bc71e5eee41f155073547ee66c1951710873511b0a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fb1b75a0e9de67a9987b7a76421fa49ea701824d40cf7c0707f8b0bc4b1e54e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f440decfc106bb84baa93d0f68ae8ddd789be1fbce96445e877946a6491a79b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da20546ba52912b7c8add7a07efaa00ba253a5551b85c954819cee6e09e5b9fa(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caa30e8a3686fda3c8d39914bfeed0ae4d72321f5927ac13e27cd5e3e2a22b3d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be556fa913baac4c5fe27b110c627e23aae8f0803e95b8257a1837dcf46b1da3(
    value: typing.Optional[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesCaOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54a9f207be1d91ca90db067e6c2eb21d2ff4280d51e812ec410a066dd77b3bac(
    *,
    base_key_usage: typing.Union[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageBaseKeyUsage, typing.Dict[builtins.str, typing.Any]],
    extended_key_usage: typing.Union[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageExtendedKeyUsage, typing.Dict[builtins.str, typing.Any]],
    unknown_extended_key_usages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsages, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54f550f8c0e0e5946ed62f6bee38df14d848a8dc7336496c927caf8d016efd32(
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

def _typecheckingstub__603b3333b32bac61c10c691971e993fded7dd566f7283e9323570cba880d3d02(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb979fc464a7934a0feadaa85fdf0a01b9983a399830662210f747be75174e0e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50f7cd0499892b9f42508b5af5b3a9e41be63ba383d09a8ae7e01db82934f36b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df8449aef674d0e19106b0915fe326538a3002efd2cfa0e7346e3467799c8735(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55f523c246e0f2860040c8fe5946f15513ddd6d81b69bc99a5e0331bd626c997(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bd10b418916e515bff73c94d78fed61bbbfe63c2a8fdba7e9dbb256e9f8e761(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00ff234d6afc61e580b9cd84bf76594b45a33713f649bc91f8766b58862e902a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f524bdc368aa26eee2cdd161dfa15290f15943770989cca90f5af33d0a0ede7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f84bc4d01e20603da0a86ded70085912f15977a53186bccdbcf3348ab3568a5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9066c0ee0b86bce4238ef9dea05e8aefa3202a724ed05803b4d4c2d1b73671f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe75e6d24ad58cde66bc0d1286885bc9d3c92aeb516aec2a1e5dd3111ae63768(
    value: typing.Optional[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageBaseKeyUsage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8377bc2150c99140c4d27fb2a7c4ab90c63f0d4c87c3837b1d8a1fb709385fa6(
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

def _typecheckingstub__30d5382262e62b99f25568a91a25a5250857e206edafea2b522b0ed442e2c00a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e45f58b0e92df2c2a44a6116f39b07832e2009b432c3edc46f2fa2dfe899ef9c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41d93d14c999f3f8ed816b744a93495ab49cfb5b511cfe63fc2fc8dbbebb4772(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f1634ef7448b23797640d2568a4a49b5c03432543b88abe0c49b678226464b7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__755fa445988683225b4e2f04bd46e27193bda96c8935893dd48d095fc28e0c14(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4013069bfe325635f79c80de74e58e711aba765e68435a8ab9b270ab8fb6743d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1dc2a92e63d4ddfdb8b7eb375070bb8daa01aaf0cf4718b1bc5c7ef204f38dd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d39c5566875a31058fdf95a696a293562637a44d19e3815d4e9b9e3db9b9509(
    value: typing.Optional[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageExtendedKeyUsage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce5db9806802d77aacc5cf05234c921c81dfc9648973fdf2d69d7ae03b37d4b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__735a6764d142d5f83fcde38887ede154f57b8c65c9465477a0fcd82077bbc204(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsages, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b82b6aaef42ec3b2f3774b03a681627075499d733b8f0f8ffe72cc304b75bd5e(
    value: typing.Optional[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f6e9b6626a1c1c99f39184bf29d454561b10511939e2c0b8e397e9be03f2793(
    *,
    object_id_path: typing.Sequence[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7de05d3de8f8c6c929ea28e1a9d02b31f8290f92c4ce7ace570a023d31c059a2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43a69b43e653f5f6c89355117122e1572c5d3dd82ea804978625367fdb631763(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef47eaeaabd4075ff385251b186eaea6be4b201f826ea9393b271971bd75ae3a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efb9fbdf6c34d9086bb7a2e7b111a74124c7694d3ed07a9bd9cce5ec2dd48fb3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0492be2deba4897ec34256b54c681251d3de466ca079ee8ce90f78e5b1caea4f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7172c190679f96b069f0be1815734d540eedd8a5fccb611847c24d0ee7402ec1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsages]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a01bae66c312d6f0e0acd40ea6d845a42b5e6fd317485b1789d9c217a3ed710(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23ace5199fb7ede47758db3760f662f70c9f3014e24378b8149b3cd0b6725e28(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d90e6da4ebdad828ba3f6a15dec1927c1f815a4796100e02a55b738e6fc8005(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePrivatecaCaPoolIssuancePolicyBaselineValuesKeyUsageUnknownExtendedKeyUsages]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3e0d0dde74213d6c4c377846c16bfaa990e85c1042aa5380a34f48d8ef1e475(
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

def _typecheckingstub__521fefda8c602932b1faf3fccffd49e93044660e64f9d68081f806cb72922f97(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9bbdb0147eee16183a9df37bdc24f3cde2f4e887cd8f451774a057e16ec3896(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d249f89651a27725ab97e4cedae90237f7d598b29b83d058b28a98c7b1ba3187(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88ade72263bea0a8d291383d3e20bd4c955e5f9c1d09a15e47070c80801ef17f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8622fbe3c7f1468af78653cff41170b3dbb6613ed577d758bdc05e4b5e2eb153(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7121ca026bae0fb193c699a65a263088b613f3f5e24e88a7af69677fd3c37f2c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80404b6cd466f470e393fc760adaf71f61ae665c7f8b88a8478866bb1f8cf64f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ed9dd74295b2ce3bfa56717022787310ae884e35c79bd3a4f444a31c117add3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7675da1b26021a6b2e98f8618ffbce232f338229a9ec338bc6ebcdae027b2dd1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f5246e8f1d2cc84d1abbc292b6271da39721334cd235c52db1b2437468b6433(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24f2d80b29eaafd21baa7392e49927295b5a279c99f98758538c7db6d629630a(
    value: typing.Optional[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesNameConstraints],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__840ed1060d7e38ed21860770ee126050f585712d01a78e005382aaf7b57e7276(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfe193da71a4897a0fb2fa49c32fb838fc41826cf9d3160078f9e1b9dc3a2c36(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesAdditionalExtensions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e60c87537f2e010d9a13e905fe24c5a667b0acf30facc55fa893af4ef125bb3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIds, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__754cc69c5ea510175c3b743453b6d285d20f392c8cb34466eeb3773310dff172(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a374b9c33b89020286b516b5d3058b9aaba36906cb8fbbfeb2af544156cc220(
    value: typing.Optional[GooglePrivatecaCaPoolIssuancePolicyBaselineValues],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c3ee5d78e13355a7e338e88808232e7609fce29bb6fa5cdb77e4469bdd0c9ff(
    *,
    object_id_path: typing.Sequence[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0adf0cefcc69eef6d30ebb936ba3ef15fe13abaf0c25e72989440cc2c311206a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7e893f65c9b12a1a4f04c1a07934b9784a5832dbd1ae78bc272b80339cfcba9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9096f203c3b6862d76960e912fc26f6151dfa9e99174c4e059529db2b3e28a62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9739f2f910e1b408543e2758778b9033fe457bd14cb61d5aad026b494139ca8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11c5045a872446cfecadfd89a7c2e7f7f49fe1636d55d6b97ca1195bc04fcef6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08df2942b098625b0cbb9b6ce4b407dcf600f4764a5334aec5ecf0786bc75cae(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GooglePrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIds]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__490f622a2351b2c99fda0462d8984c133d5115a593c935b2786f8448a6a83d47(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__125fe2f35e1906006e3802f33946eef318ac86feb8c91bdd5faa28b3111403d1(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26ee5a451cb3e7da7e1b594f84ae6a82ea72b82249fd4e74198f718b3128dacf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePrivatecaCaPoolIssuancePolicyBaselineValuesPolicyIds]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e888ef922fe9729f226c26a7f6ff6d986a245d1a7f7cda34353f25ba7c8a4748(
    *,
    allow_subject_alt_names_passthrough: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    allow_subject_passthrough: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    cel_expression: typing.Optional[typing.Union[GooglePrivatecaCaPoolIssuancePolicyIdentityConstraintsCelExpression, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__904c2b90906ac4ead3ea616f87be9161fe3a0e4a73802e5a78e00a57073f3174(
    *,
    expression: builtins.str,
    description: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffb823eacea15eda20f3e778f52ad5009b54d654a9d6e5a302a7048c7b7aaf29(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2e31d81410efad504dec1c0681ebf139bde62b661e086cafc4b0ec15ea3ccd5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__038a00a3314b0220677309561a93eded6d7e7d169c344117e3a7bdbd9692acbe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec2d47f02f11387d5f8a943bfac96fb93ca164f44384b75905254a4c9f957613(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d6d31309a29aa5e17b3f7151b1c788058ef8ccf5e633e047d94d3b4a6f0b07f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5803bfab5324f3eceb1194c6e39cc9e5b5148eaa3e18b7134fb90200c2514dc7(
    value: typing.Optional[GooglePrivatecaCaPoolIssuancePolicyIdentityConstraintsCelExpression],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7d34ad1fae8f6320bc75480b460bb16c4133a9bb20edf03589f571e71fe1e91(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fe361c82dc6f74d2fad11e259a48e3a5d2f0101dea45cd12c4badb402533eb6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19a46a312ea77a4dd8f1f7a47c699bcaa3318ec88cef7589a14d3751b131a5ff(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d43556e353d698a0efb70032d91191f9ae57c8219b49c45418bb6c17c2f52ec(
    value: typing.Optional[GooglePrivatecaCaPoolIssuancePolicyIdentityConstraints],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5976bd59eae857e6491de19150f6270f295c3d5d78d9086b9014f7d19de743ff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4de02a3ce48da07b37d5df2a193a50041eb8bf249ce4af170ac496eb5f0f2fd7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GooglePrivatecaCaPoolIssuancePolicyAllowedKeyTypes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2054a4be1b527527f3600cc914e66e8b52cda4b12fd252c1866dad6dcbb55366(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9993338b50d9006d103905e0a81ade9d601838c871eda3de81594b0883a614e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5fc2003e9ede5f82f085152db512f2c1baafab6ac5e80b50997c3d5a585ab60(
    value: typing.Optional[GooglePrivatecaCaPoolIssuancePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59ce820a8dd1398ce4bdff389668c9215e0a9d60b90557291d26b707e20093f5(
    *,
    publish_ca_cert: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    publish_crl: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    encoding_format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8fc8ab6f244e442db396875aa819d41087c65fa362f39f151fde443aa64a030(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8044a10cc24f59b07b4096906bd0fbdb79805e6d0641095a8d2aa9a71ea217fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfc880058fc78650c4d571254c68cff2cb76fb7e2ad0fb5b089e9a8c788e0c69(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdc49d5b59aefdee5572ccc4a4307c5f13650bec79ea70ed6d317a3d96737bc4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__221dee593b9c1c62f9da4a36f3487b956e6a95e5c599baf284496654a806689d(
    value: typing.Optional[GooglePrivatecaCaPoolPublishingOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b010534f94e8843036964347cce4d035d45629f6f70ba20250731f829f3f4a1(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9a6a4dacd093b420f73b5a808ae5e3e7b8152520aa9f44d40f90dfb7349e16b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41ca9a212104eb058f7736c08fc69822bc6de5a0fb552970b77574b4069c1eb0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16e71d5cbdd0836acfbe923942ff2e1669ecae19fed014c6bc6c7249659d05f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e1d5585eaac7ddc1700cc65453ebf3e986cb6e6f1a9dbc3fefe046c3a86ae8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1f2235bc14f065cbad0898e74cbd93f0ed2639eeb439cc522a77daf3258bf76(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePrivatecaCaPoolTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
